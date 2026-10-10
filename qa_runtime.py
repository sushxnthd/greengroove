from __future__ import annotations

import hashlib
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

HOST = "127.0.0.1"
PORT = 4173
BASE = f"http://{HOST}:{PORT}/index.html"
PROJECT_HOST = "sushxnthd.github.io"
CONTROL_SELECTOR = "[data-gg-qa-control]"


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


server = ThreadingHTTPServer((HOST, PORT), Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.2)

report = {"critical": [], "warnings": [], "viewports": {}, "external_links": []}


def critical(view, msg):
    report["critical"].append(f"[{view}] {msg}")


def warn(view, msg):
    report["warnings"].append(f"[{view}] {msg}")


def digest(text):
    return hashlib.sha256((text or "").encode("utf-8", "ignore")).hexdigest()


REACHABLE_JS = """e => {
  const s=getComputedStyle(e), r=e.getBoundingClientRect();
  if (!(r.width>0 && r.height>0) || s.display==='none' || s.visibility==='hidden' ||
      parseFloat(s.opacity || '1') <= 0.01 || s.pointerEvents==='none' || e.disabled) return false;
  const x=Math.min(innerWidth-1, Math.max(0, r.left+r.width/2));
  const y=Math.min(innerHeight-1, Math.max(0, r.top+r.height/2));
  if (r.right<=0 || r.bottom<=0 || r.left>=innerWidth || r.top>=innerHeight) return false;
  const top=document.elementFromPoint(x,y);
  return !!top && (top===e || e.contains(top) || top.contains(e));
}"""

STATE_JS = """e => ({
  cls:String(e.className || ''),
  expanded:e.getAttribute('aria-expanded'),
  pressed:e.getAttribute('aria-pressed'),
  current:e.getAttribute('aria-current'),
  selected:e.getAttribute('aria-selected'),
  hidden:e.getAttribute('aria-hidden'),
  disabled:!!e.disabled
})"""

SECTION_JS = """e => {
  const root=e.closest('section,footer,header,[role=dialog],.modal,.menu') || e.parentElement || e;
  return root.outerHTML;
}"""

viewports = {
    "desktop": {"width": 1440, "height": 1000},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    external_urls = set()

    for name, viewport in viewports.items():
        ctx = browser.new_context(viewport=viewport, reduced_motion="reduce")
        page = ctx.new_page()
        page_errors, console_errors = [], []
        page.on("pageerror", lambda exc, b=page_errors: b.append(str(exc)))
        page.on("console", lambda msg, b=console_errors: b.append(msg.text) if msg.type == "error" else None)

        try:
            page.goto(BASE, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(1300)
        except Exception as exc:
            critical(name, f"page failed to load: {exc}")
            ctx.close()
            continue

        if page.locator("h1").count() == 0:
            critical(name, "no H1 rendered")

        # Stable inventory before any scroll-driven animation can mutate the DOM.
        controls = page.locator(CONTROL_SELECTOR).evaluate_all("""els => els.map(e => ({
          id:e.dataset.ggQaControl,
          tag:e.tagName,
          text:(e.innerText||e.value||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,160),
          ariaExpanded:e.getAttribute('aria-expanded')
        }))""")
        at_load_reachable = {}
        for meta in controls:
            loc = page.locator(f'[data-gg-qa-control="{meta["id"]}"]')
            at_load_reachable[meta["id"]] = bool(loc.count() and loc.evaluate(REACHABLE_JS))

        # Full-page scroll pass exercises sticky/lazy/scroll-triggered states.
        total_h = page.evaluate("document.documentElement.scrollHeight")
        step = max(viewport["height"] // 2, 300)
        for y in range(0, min(int(total_h), 60000), step):
            page.evaluate("y => window.scrollTo(0,y)", y)
            page.wait_for_timeout(12)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(220)

        # Every link: no dead hrefs/stale source routes; every unique local section is clicked.
        hrefs = page.locator("a[href]").evaluate_all("els => els.map(a => a.getAttribute('href'))")
        hashes = []
        for href in hrefs:
            if not href:
                critical(name, "anchor with empty href")
                continue
            low = href.lower()
            if href == "#" or low.startswith("javascript:"):
                critical(name, f"non-destination href remains: {href}")
            if "osmo.supply" in low or "/resource/" in low or "sushxnthd.github.io/resource/" in low:
                critical(name, f"stale source route remains: {href}")
            if href.startswith("#") and len(href) > 1:
                target = href[1:]
                if page.locator(f"#{target}").count() == 0:
                    critical(name, f"missing hash target: {href}")
                elif href not in hashes:
                    hashes.append(href)
            else:
                parsed = urlparse(href)
                if parsed.scheme in {"http", "https"}:
                    if parsed.netloc == PROJECT_HOST:
                        if parsed.path.rstrip("/") != "/greengroove":
                            critical(name, f"same-host route escapes project path: {href}")
                    else:
                        external_urls.add(href)

        clicked_hashes = []
        for href in hashes:
            try:
                page.evaluate(
                    "href => { const a=[...document.querySelectorAll('a[href]')].find(x=>x.getAttribute('href')===href); if(a) a.click(); }",
                    href,
                )
                page.wait_for_timeout(180)
                if page.evaluate("location.hash") != href:
                    warn(name, f"URL hash did not settle after anchor click: {href}")
                clicked_hashes.append(href)
            except Exception as exc:
                critical(name, f"anchor click failed for {href}: {exc}")

        # Media integrity.
        broken_images = page.locator("img").evaluate_all(
            "els => els.filter(i => i.currentSrc && i.complete && i.naturalWidth===0).map(i => i.currentSrc)"
        )
        for src in broken_images:
            critical(name, f"broken image: {src}")
        static_media_issues = page.locator("video").evaluate_all(
            "els => els.filter(v => !v.getAttribute('src') && !v.querySelector('source[src]') && (!v.dataset.ggStaticMedia || !v.getAttribute('poster'))).map(v => v.outerHTML.slice(0,300))"
        )
        for item in static_media_issues:
            critical(name, f"empty unfinished video surface: {item}")

        # Footer source/update control must not masquerade as a subscription collector.
        form = page.locator("footer form")
        if form.count():
            info = form.first.evaluate("""f => ({
              action:f.action,target:f.target,
              email:[...f.querySelectorAll('input[type=email]')].map(i=>({required:i.required,readOnly:i.readOnly,name:i.name}))
            })""")
            if "github.com/sushxnthd/greengroove" not in info["action"]:
                critical(name, f"footer form points somewhere unexpected: {info['action']}")
            for email in info["email"]:
                if email["required"] or email["name"] or not email["readOnly"]:
                    critical(name, f"footer field still acts as email collector: {email}")

        # Exhaustively exercise every exact source control/card button. User-reachable
        # controls get a real pointer click. Context-hidden controls (off-canvas modal,
        # non-current carousel card) still have their click handler exercised directly,
        # while opener/closer flows are tested separately below.
        control_results = []
        for meta in controls:
            test = ctx.new_page()
            errors, cerrors = [], []
            test.on("pageerror", lambda exc, b=errors: b.append(str(exc)))
            test.on("console", lambda msg, b=cerrors: b.append(msg.text) if msg.type == "error" else None)
            try:
                test.add_init_script("""
                  window.__qaOpened=[];
                  window.open=(url,target,features)=>{window.__qaOpened.push(String(url||'')); return {closed:false,close(){},focus(){}};};
                """)
                test.goto(BASE, wait_until="domcontentloaded", timeout=30000)
                test.wait_for_timeout(500)
                el = test.locator(f'[data-gg-qa-control="{meta["id"]}"]')
                if el.count() != 1:
                    critical(name, f"QA marker missing/duplicated: {meta['id']} {meta['text']!r}")
                    control_results.append({**meta, "result": "marker-missing"})
                    test.close()
                    continue

                # Center the actual control so sticky bars do not create false negatives.
                el.evaluate("e => e.scrollIntoView({block:'center',inline:'center'})")
                test.wait_for_timeout(100)
                reachable = bool(el.evaluate(REACHABLE_JS))
                before_html = digest(el.evaluate(SECTION_JS))
                before_state = el.evaluate(STATE_JS)
                before_url = test.url
                before_scroll = test.evaluate("window.scrollY")

                mode = "user-click" if reachable else "contextual-handler"
                if reachable:
                    el.click(timeout=1800)
                else:
                    # Off-canvas/modal/carousel controls are not broken simply because their
                    # context is closed. Exercise their registered handler without forcing UI.
                    el.evaluate("e => e.click()")
                test.wait_for_timeout(280)

                opened = test.evaluate("window.__qaOpened || []")
                after_html = digest(el.evaluate(SECTION_JS)) if el.count() else "gone"
                after_state = el.evaluate(STATE_JS) if el.count() else {"gone": True}
                after_url = test.url
                after_scroll = test.evaluate("window.scrollY")
                changed = bool(
                    opened or after_html != before_html or after_state != before_state or
                    after_url != before_url or abs(after_scroll-before_scroll) > 5
                )

                bad = [e for e in errors+cerrors if any(k in e.lower() for k in ("referenceerror", "typeerror", "outseta", "uncaught"))]
                if bad:
                    critical(name, f"control {meta['id']} {meta['text']!r} caused JS error: {bad[0]}")

                # If something was genuinely reachable on initial page load but cannot be
                # pointer-hit even after centering on a clean page, that is a real obstruction.
                if at_load_reachable.get(meta["id"]) and not reachable:
                    critical(name, f"initially exposed control became pointer-obstructed: {meta['id']} {meta['text']!r}")

                result = "clicked-state-changed" if reachable and changed else (
                    "clicked-idempotent" if reachable else "contextual-handler-exercised"
                )
                control_results.append({**meta, "mode": mode, "result": result, "opened": opened})
                if reachable and not changed and meta["text"] and "close" not in meta["text"].lower():
                    warn(name, f"reachable control is idempotent/no detectable state change: {meta['id']} {meta['text']!r}")
            except Exception as exc:
                critical(name, f"control exercise failed {meta['id']} {meta['text']!r}: {exc}")
                control_results.append({**meta, "result": "exercise-failed", "error": str(exc)[:500]})
            finally:
                if not test.is_closed():
                    test.close()

        # Real opener -> close flows for modal/menu interfaces.
        pair_results = []
        for label in ("About", "About the project", "More info"):
            pair = ctx.new_page()
            perrors = []
            pair.on("pageerror", lambda exc, b=perrors: b.append(str(exc)))
            try:
                pair.goto(BASE, wait_until="domcontentloaded", timeout=30000)
                pair.wait_for_timeout(500)
                candidates = pair.get_by_role("button", name=label, exact=False)
                opener = None
                for i in range(candidates.count()):
                    c = candidates.nth(i)
                    c.evaluate("e => e.scrollIntoView({block:'center',inline:'center'})")
                    pair.wait_for_timeout(50)
                    if c.evaluate(REACHABLE_JS):
                        opener = c
                        break
                if opener is None:
                    pair_results.append({"opener": label, "result": "not-currently-exposed"})
                    pair.close()
                    continue
                opener.click(timeout=1800)
                pair.wait_for_timeout(260)
                closes = pair.get_by_role("button", name="Close", exact=False)
                closer = None
                for j in range(closes.count()):
                    c = closes.nth(j)
                    if c.evaluate(REACHABLE_JS):
                        closer = c
                        break
                if closer is not None:
                    closer.click(timeout=1800)
                    pair.wait_for_timeout(180)
                    pair_results.append({"opener": label, "result": "opened-and-closed"})
                else:
                    pair_results.append({"opener": label, "result": "opened-no-close-required"})
                bad = [e for e in perrors if any(k in e.lower() for k in ("referenceerror", "typeerror", "outseta"))]
                if bad:
                    critical(name, f"{label!r} opener flow caused JS error: {bad[0]}")
            except Exception as exc:
                critical(name, f"opener flow failed for {label!r}: {exc}")
            finally:
                if not pair.is_closed():
                    pair.close()

        # Keyboard traversal checks focusability and traps without altering layout.
        keyboard = ctx.new_page()
        kerrors, focus_steps = [], []
        keyboard.on("pageerror", lambda exc, b=kerrors: b.append(str(exc)))
        try:
            keyboard.goto(BASE, wait_until="domcontentloaded", timeout=30000)
            keyboard.wait_for_timeout(450)
            for _ in range(30):
                keyboard.keyboard.press("Tab")
                focus_steps.append(keyboard.evaluate("""() => {
                  const e=document.activeElement; return e ? (e.getAttribute('aria-label')||e.innerText||e.value||e.tagName).trim().replace(/\\s+/g,' ').slice(0,100) : '';
                }"""))
            bad = [e for e in kerrors if any(k in e.lower() for k in ("referenceerror", "typeerror", "outseta"))]
            if bad:
                critical(name, f"keyboard traversal caused JS error: {bad[0]}")
        except Exception as exc:
            warn(name, f"keyboard traversal incomplete: {exc}")
        finally:
            if not keyboard.is_closed():
                keyboard.close()

        for err in page_errors:
            low = err.lower()
            if any(k in low for k in ("outseta", "referenceerror", "typeerror")):
                critical(name, f"runtime page error: {err}")
            else:
                warn(name, f"page error: {err}")
        for err in console_errors:
            low = err.lower()
            if any(k in low for k in ("outseta", "uncaught", "referenceerror", "typeerror")):
                critical(name, f"console error: {err}")
            elif "failed to load resource" not in low:
                warn(name, f"console error: {err}")

        report["viewports"][name] = {
            "anchor_count": len(hrefs),
            "unique_hash_targets_clicked": clicked_hashes,
            "controls_total": len(controls),
            "controls_exercised": control_results,
            "opener_close_flows": pair_results,
            "keyboard_focus_steps": focus_steps,
            "broken_image_count": len(broken_images),
            "page_error_count": len(page_errors),
            "console_error_count": len(console_errors),
        }
        page.close()
        ctx.close()

    # Real external destinations used by cards/CTAs.
    req = p.request.new_context(ignore_https_errors=True)
    for url in sorted(external_urls):
        parsed = urlparse(url)
        if parsed.netloc not in {"github.com", "www.behance.net", "behance.net"}:
            continue
        item = {"url": url}
        try:
            response = req.get(url, timeout=15000, fail_on_status_code=False)
            item["status"] = response.status
            if response.status == 404 or response.status >= 500:
                report["critical"].append(f"[external] broken destination {response.status}: {url}")
        except Exception as exc:
            item["error"] = str(exc)[:300]
            report["warnings"].append(f"[external] could not verify destination {url}: {exc}")
        report["external_links"].append(item)
    req.dispose()
    browser.close()

server.shutdown()
Path("qa-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
if report["critical"]:
    raise SystemExit(f"Runtime QA failed with {len(report['critical'])} critical issue(s).")
print("Runtime QA passed with no critical functional issues.")
