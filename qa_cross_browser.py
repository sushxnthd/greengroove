from __future__ import annotations

import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

HOST = "127.0.0.1"
PORT = 4175
URL = f"http://{HOST}:{PORT}/index.html"
CONTROL_SELECTOR = "[data-gg-qa-control]"


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def actionable_error(text: str) -> bool:
    low = str(text).lower()
    return any(k in low for k in ("referenceerror", "typeerror", "uncaught", "outseta"))


REACHABLE_JS = """e => {
  const s=getComputedStyle(e), r=e.getBoundingClientRect();
  if (!(r.width>0 && r.height>0) || s.display==='none' || s.visibility==='hidden' ||
      parseFloat(s.opacity||'1')<=0.01 || s.pointerEvents==='none' || e.disabled) return false;
  const x=Math.min(innerWidth-1,Math.max(0,r.left+r.width/2));
  const y=Math.min(innerHeight-1,Math.max(0,r.top+r.height/2));
  if (r.right<=0 || r.bottom<=0 || r.left>=innerWidth || r.top>=innerHeight) return false;
  const top=document.elementFromPoint(x,y);
  return !!top && (top===e || e.contains(top) || top.contains(e));
}"""

server = ThreadingHTTPServer((HOST, PORT), Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.2)

report = {"critical": [], "browsers": {}}
viewports = {
    "desktop": {"width": 1440, "height": 1000},
    "mobile": {"width": 390, "height": 844},
}

with sync_playwright() as p:
    for browser_name, browser_type in (("firefox", p.firefox), ("webkit", p.webkit)):
        browser = browser_type.launch(headless=True)
        browser_report = {}

        for viewport_name, viewport in viewports.items():
            ctx = browser.new_context(viewport=viewport, reduced_motion="reduce")
            page = ctx.new_page()
            page_errors, console_errors = [], []
            page.on("pageerror", lambda exc, b=page_errors: b.append(str(exc)))
            page.on("console", lambda msg, b=console_errors: b.append(msg.text) if msg.type == "error" else None)

            try:
                page.goto(URL, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(1100)
            except Exception as exc:
                report["critical"].append(f"[{browser_name}/{viewport_name}] load failed: {exc}")
                ctx.close()
                continue

            if page.locator("h1").count() == 0:
                report["critical"].append(f"[{browser_name}/{viewport_name}] H1 missing")

            # Exercise the entire page to trigger lazy/sticky/scroll-bound code.
            total_h = page.evaluate("document.documentElement.scrollHeight")
            step = max(viewport["height"] // 2, 300)
            for y in range(0, min(int(total_h), 60000), step):
                page.evaluate("y => window.scrollTo(0,y)", y)
                page.wait_for_timeout(10)
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(180)

            hrefs = page.locator("a[href]").evaluate_all("els => els.map(a=>a.getAttribute('href'))")
            hashes = []
            for href in hrefs:
                if not href or href == "#" or str(href).lower().startswith("javascript:"):
                    report["critical"].append(f"[{browser_name}/{viewport_name}] dead href: {href!r}")
                    continue
                low = href.lower()
                if "osmo.supply" in low or "/resource/" in low:
                    report["critical"].append(f"[{browser_name}/{viewport_name}] stale route: {href}")
                if href.startswith("#") and len(href) > 1:
                    if page.locator(href).count() == 0:
                        report["critical"].append(f"[{browser_name}/{viewport_name}] missing anchor target: {href}")
                    elif href not in hashes:
                        hashes.append(href)

            for href in hashes:
                try:
                    page.evaluate(
                        "href => { const a=[...document.querySelectorAll('a[href]')].find(x=>x.getAttribute('href')===href); if(a) a.click(); }",
                        href,
                    )
                    page.wait_for_timeout(100)
                except Exception as exc:
                    report["critical"].append(f"[{browser_name}/{viewport_name}] anchor click failed {href}: {exc}")

            broken_images = page.locator("img").evaluate_all(
                "els => els.filter(i=>i.currentSrc && i.complete && i.naturalWidth===0).map(i=>i.currentSrc)"
            )
            for src in broken_images:
                report["critical"].append(f"[{browser_name}/{viewport_name}] broken image: {src}")

            empty_videos = page.locator("video").evaluate_all(
                "els => els.filter(v=>!v.getAttribute('src') && !v.querySelector('source[src]') && (!v.dataset.ggStaticMedia || !v.getAttribute('poster'))).length"
            )
            if empty_videos:
                report["critical"].append(f"[{browser_name}/{viewport_name}] {empty_videos} unfinished video surface(s)")

            controls = page.locator(CONTROL_SELECTOR).evaluate_all(
                "els => els.map(e=>({id:e.dataset.ggQaControl,text:(e.innerText||e.value||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,120)}))"
            )
            exercised = []

            # Each control is tested on a fresh document so one modal/carousel cannot mask another.
            for meta in controls:
                test = ctx.new_page()
                errors, cerrors = [], []
                test.on("pageerror", lambda exc, b=errors: b.append(str(exc)))
                test.on("console", lambda msg, b=cerrors: b.append(msg.text) if msg.type == "error" else None)
                try:
                    test.add_init_script("window.open=(url)=>({closed:false,close(){},focus(){}});")
                    test.goto(URL, wait_until="domcontentloaded", timeout=30000)
                    test.wait_for_timeout(420)
                    el = test.locator(f'[data-gg-qa-control="{meta["id"]}"]')
                    if el.count() != 1:
                        report["critical"].append(f"[{browser_name}/{viewport_name}] missing control marker {meta['id']}")
                        continue
                    el.evaluate("e=>e.scrollIntoView({block:'center',inline:'center'})")
                    test.wait_for_timeout(70)
                    reachable = bool(el.evaluate(REACHABLE_JS))
                    if reachable:
                        el.click(timeout=2200)
                    else:
                        el.evaluate("e=>e.click()")
                    test.wait_for_timeout(220)
                    bad = [e for e in errors + cerrors if actionable_error(e)]
                    if bad:
                        report["critical"].append(
                            f"[{browser_name}/{viewport_name}] control {meta['id']} {meta['text']!r} caused JS error: {bad[0]}"
                        )
                    exercised.append({**meta, "mode": "user-click" if reachable else "contextual-handler"})
                except Exception as exc:
                    report["critical"].append(
                        f"[{browser_name}/{viewport_name}] control {meta['id']} {meta['text']!r} failed: {exc}"
                    )
                finally:
                    if not test.is_closed():
                        test.close()

            # About must activate by pointer and keyboard in desktop layouts across engines.
            about_activation = {}
            if viewport_name == "desktop":
                for activation in ("click", "Enter", "Space"):
                    test = ctx.new_page()
                    errors = []
                    test.on("pageerror", lambda exc, b=errors: b.append(str(exc)))
                    try:
                        test.goto(URL, wait_until="domcontentloaded", timeout=30000)
                        test.wait_for_timeout(500)
                        about = test.locator('[data-gg-qa-control="control-023"]')
                        about.evaluate("e=>e.scrollIntoView({block:'center',inline:'center'})")
                        test.wait_for_timeout(80)
                        before = test.locator("body").evaluate("e=>e.outerHTML")
                        if activation == "click":
                            about.click(timeout=2200)
                        else:
                            about.focus()
                            test.keyboard.press(activation)
                        test.wait_for_timeout(300)
                        after = test.locator("body").evaluate("e=>e.outerHTML")
                        active = test.evaluate("() => (document.activeElement?.innerText || document.activeElement?.getAttribute?.('aria-label') || '').trim().slice(0,80)")
                        ok = before != after and "close" in active.lower() and not any(actionable_error(e) for e in errors)
                        about_activation[activation] = ok
                        if not ok:
                            report["critical"].append(f"[{browser_name}/{viewport_name}] About {activation} activation failed")
                    except Exception as exc:
                        about_activation[activation] = False
                        report["critical"].append(f"[{browser_name}/{viewport_name}] About {activation} probe failed: {exc}")
                    finally:
                        if not test.is_closed():
                            test.close()

            # Keyboard focus traversal smoke test.
            keyboard = ctx.new_page()
            kerrors = []
            keyboard.on("pageerror", lambda exc, b=kerrors: b.append(str(exc)))
            focus_steps = []
            try:
                keyboard.goto(URL, wait_until="domcontentloaded", timeout=30000)
                keyboard.wait_for_timeout(400)
                for _ in range(25):
                    keyboard.keyboard.press("Tab")
                    focus_steps.append(
                        keyboard.evaluate("() => (document.activeElement?.getAttribute?.('aria-label') || document.activeElement?.innerText || document.activeElement?.tagName || '').trim().replace(/\\s+/g,' ').slice(0,80)")
                    )
                bad = [e for e in kerrors if actionable_error(e)]
                if bad:
                    report["critical"].append(f"[{browser_name}/{viewport_name}] keyboard traversal error: {bad[0]}")
            finally:
                keyboard.close()

            for err in page_errors + console_errors:
                if actionable_error(err):
                    report["critical"].append(f"[{browser_name}/{viewport_name}] baseline runtime error: {err}")

            browser_report[viewport_name] = {
                "anchors": len(hrefs),
                "hash_targets_exercised": hashes,
                "controls": len(controls),
                "controls_exercised": len(exercised),
                "broken_images": len(broken_images),
                "unfinished_video_surfaces": empty_videos,
                "about_activation": about_activation,
                "keyboard_focus_steps": focus_steps,
                "page_errors": page_errors,
                "console_errors": [e for e in console_errors if actionable_error(e)],
            }
            page.close()
            ctx.close()

        report["browsers"][browser_name] = browser_report
        browser.close()

server.shutdown()
Path("qa-cross-browser.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
if report["critical"]:
    raise SystemExit(f"Cross-browser QA failed with {len(report['critical'])} critical issue(s).")
print("Cross-browser QA passed with no critical issues in Firefox or WebKit.")
