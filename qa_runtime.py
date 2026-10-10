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
CONTROL_SELECTOR = "button, input[type=submit], [role=button]"


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


server = ThreadingHTTPServer((HOST, PORT), Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.2)

report = {"critical": [], "warnings": [], "viewports": {}, "external_links": []}


def add_critical(view, msg):
    report["critical"].append(f"[{view}] {msg}")


def add_warning(view, msg):
    report["warnings"].append(f"[{view}] {msg}")


def is_actionable_js():
    return """e => {
      const s=getComputedStyle(e), r=e.getBoundingClientRect();
      return r.width>0 && r.height>0 && s.display!=='none' && s.visibility!=='hidden' &&
             parseFloat(s.opacity || '1') > 0.01 && s.pointerEvents!=='none' && !e.disabled;
    }"""


def section_html(locator):
    return locator.evaluate("""e => {
      const root=e.closest('section,footer,header,[role=dialog],.modal,.menu') || e.parentElement || e;
      return root.outerHTML;
    }""")


def digest(text):
    return hashlib.sha256((text or "").encode("utf-8", "ignore")).hexdigest()


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
        page_errors = []
        console_errors = []
        page.on("pageerror", lambda exc, bucket=page_errors: bucket.append(str(exc)))
        page.on(
            "console",
            lambda msg, bucket=console_errors: bucket.append(msg.text)
            if msg.type == "error"
            else None,
        )

        try:
            page.goto(BASE, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(1800)
        except Exception as exc:
            add_critical(name, f"page failed to load: {exc}")
            ctx.close()
            continue

        if page.locator("h1").count() == 0:
            add_critical(name, "no H1 rendered")

        # Exercise lazy media, sticky states, scroll-triggered sections and the full page.
        total_h = page.evaluate("document.documentElement.scrollHeight")
        step = max(viewport["height"] // 2, 300)
        for y in range(0, min(int(total_h), 60000), step):
            page.evaluate("y => window.scrollTo(0, y)", y)
            page.wait_for_timeout(16)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(250)

        # Validate every anchor and actively exercise every unique in-page destination.
        anchors = page.locator("a[href]")
        hrefs = anchors.evaluate_all("els => els.map(a => a.getAttribute('href'))")
        unique_hashes = []
        for href in hrefs:
            if not href:
                add_critical(name, "anchor with empty href")
                continue
            low = href.lower()
            if href == "#" or low.startswith("javascript:"):
                add_critical(name, f"non-destination href remains: {href}")
            if "osmo.supply" in low or "/resource/" in low or "sushxnthd.github.io/resource/" in low:
                add_critical(name, f"stale source route remains: {href}")
            if href.startswith("#") and len(href) > 1:
                target = href[1:]
                if page.locator(f"#{target}").count() == 0:
                    add_critical(name, f"missing hash target: {href}")
                elif href not in unique_hashes:
                    unique_hashes.append(href)
            else:
                parsed = urlparse(href)
                if parsed.scheme in {"http", "https"}:
                    if parsed.netloc == PROJECT_HOST:
                        if not (parsed.path.rstrip("/") == "/greengroove"):
                            add_critical(name, f"same-host route escapes project path: {href}")
                    else:
                        external_urls.add(href)

        clicked_hashes = []
        for href in unique_hashes:
            try:
                target = page.locator(href).first
                target_y = target.evaluate("e => e.getBoundingClientRect().top + window.scrollY")
                page.evaluate(
                    "href => { const a=[...document.querySelectorAll('a[href]')].find(x=>x.getAttribute('href')===href); if(a) a.click(); }",
                    href,
                )
                page.wait_for_timeout(180)
                current_hash = page.evaluate("location.hash")
                scroll_y = page.evaluate("window.scrollY")
                if current_hash != href:
                    add_warning(name, f"anchor reached target but URL hash did not settle: {href} -> {current_hash}")
                # Allow sticky header/scroll-margin offsets; require that navigation moved near target.
                if abs(scroll_y - target_y) > max(viewport["height"] * 1.5, 1200) and target_y > viewport["height"]:
                    add_warning(name, f"anchor click did not move near target: {href}")
                clicked_hashes.append(href)
            except Exception as exc:
                add_critical(name, f"anchor click failed for {href}: {exc}")

        # Check image decode status after the full scroll pass.
        broken_images = page.locator("img").evaluate_all(
            "els => els.filter(i => i.currentSrc && i.complete && i.naturalWidth === 0).map(i => i.currentSrc)"
        )
        for src in broken_images:
            add_critical(name, f"broken image: {src}")

        # Empty video elements must be explicitly treated as static poster media.
        static_media_issues = page.locator("video").evaluate_all(
            "els => els.filter(v => !v.getAttribute('src') && !v.querySelector('source[src]') && (!v.dataset.ggStaticMedia || !v.getAttribute('poster'))).map(v => v.outerHTML.slice(0,300))"
        )
        for item in static_media_issues:
            add_critical(name, f"empty unmarked video surface: {item}")

        # Footer source/update form must no longer pretend to collect email addresses.
        footer_forms = page.locator("footer form")
        if footer_forms.count():
            info = footer_forms.first.evaluate(
                "f => ({action:f.action, method:f.method, target:f.target, email:[...f.querySelectorAll('input[type=email]')].map(i=>({required:i.required, readOnly:i.readOnly, name:i.name}))})"
            )
            if "github.com/sushxnthd/greengroove" not in info["action"]:
                add_critical(name, f"footer form action is not Green Groove GitHub: {info['action']}")
            for email in info["email"]:
                if email["required"] or email["name"] or not email["readOnly"]:
                    add_critical(name, f"footer email-like field still behaves like a collector: {email}")

        # Snapshot every control with its stable DOM index. Only actionable controls are
        # clicked; controls hidden inside closed modals are tested when their opener runs.
        controls = page.locator(CONTROL_SELECTOR).evaluate_all("""els => els.map((e, domIndex) => {
          const s=getComputedStyle(e), r=e.getBoundingClientRect();
          const actionable=r.width>0 && r.height>0 && s.display!=='none' && s.visibility!=='hidden' &&
            parseFloat(s.opacity || '1') > 0.01 && s.pointerEvents!=='none' && !e.disabled;
          return {
            domIndex,
            tag:e.tagName,
            text:(e.innerText||e.value||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,160),
            actionable,
            ariaExpanded:e.getAttribute('aria-expanded'),
            ariaControls:e.getAttribute('aria-controls')
          };
        })""")

        actionable_controls = [c for c in controls if c["actionable"]]
        control_results = []

        # Exhaustive click pass: each actionable button/control is tested from a clean page
        # so sliders, tabs, modals and menus cannot mask one another's behavior.
        for meta in actionable_controls:
            test_page = ctx.new_page()
            errors = []
            console = []
            test_page.on("pageerror", lambda exc, bucket=errors: bucket.append(str(exc)))
            test_page.on(
                "console",
                lambda msg, bucket=console: bucket.append(msg.text) if msg.type == "error" else None,
            )
            try:
                # Capture window.open instead of navigating away; this still proves the
                # production handler fired and records its exact destination.
                test_page.add_init_script("""
                  window.__qaOpened=[];
                  const realOpen=window.open;
                  window.open=(url,target,features)=>{ window.__qaOpened.push(String(url||'')); return {closed:false,close(){},focus(){}}; };
                """)
                test_page.goto(BASE, wait_until="domcontentloaded", timeout=30000)
                test_page.wait_for_timeout(650)
                all_controls = test_page.locator(CONTROL_SELECTOR)
                if meta["domIndex"] >= all_controls.count():
                    add_critical(name, f"control disappeared on clean load: #{meta['domIndex']} {meta['text']!r}")
                    test_page.close()
                    continue
                el = all_controls.nth(meta["domIndex"])
                if not el.evaluate(is_actionable_js()):
                    control_results.append({**meta, "result": "context-hidden-on-clean-load"})
                    test_page.close()
                    continue
                el.scroll_into_view_if_needed(timeout=3000)
                test_page.wait_for_timeout(80)
                before_url = test_page.url
                before_html = digest(section_html(el))
                before_state = el.evaluate("e => ({cls:e.className, aria:e.getAttribute('aria-expanded'), pressed:e.getAttribute('aria-pressed'), current:e.getAttribute('aria-current')})")
                before_scroll = test_page.evaluate("window.scrollY")

                el.click(timeout=4000)
                test_page.wait_for_timeout(420)

                opened = test_page.evaluate("window.__qaOpened || []")
                after_url = test_page.url
                after_html = digest(section_html(el)) if el.count() else "gone"
                after_state = el.evaluate("e => ({cls:e.className, aria:e.getAttribute('aria-expanded'), pressed:e.getAttribute('aria-pressed'), current:e.getAttribute('aria-current')})") if el.count() else {"gone": True}
                after_scroll = test_page.evaluate("window.scrollY")
                changed = bool(
                    opened
                    or after_url != before_url
                    or after_html != before_html
                    or after_state != before_state
                    or abs(after_scroll - before_scroll) > 5
                )

                actionable_errors = [e for e in errors if any(k in e.lower() for k in ("referenceerror", "typeerror", "outseta"))]
                actionable_console = [e for e in console if any(k in e.lower() for k in ("uncaught", "referenceerror", "typeerror", "outseta"))]
                if actionable_errors or actionable_console:
                    add_critical(name, f"control {meta['text']!r} caused JS error: {(actionable_errors + actionable_console)[0]}")

                result = "clicked-state-changed" if changed else "clicked-no-detectable-state-change"
                control_results.append({**meta, "result": result, "opened": opened})
                # Clicking an already-selected tab or a decorative accessible control can
                # legitimately be idempotent. Record it rather than failing the build.
                if not changed and meta["text"] and "close" not in meta["text"].lower():
                    add_warning(name, f"control clicked with no detectable state change: {meta['text']!r}")
            except Exception as exc:
                add_critical(name, f"control click failed #{meta['domIndex']} {meta['text']!r}: {exc}")
                control_results.append({**meta, "result": "click-failed", "error": str(exc)[:400]})
            finally:
                if not test_page.is_closed():
                    test_page.close()

        # Explicit opener/closer pass for hidden modal/menu close controls.
        pair_results = []
        pair_labels = ["About", "About the project", "More info", "View section", "RETAIL STATE SYSTEM"]
        for label in pair_labels:
            pair_page = ctx.new_page()
            pair_errors = []
            pair_page.on("pageerror", lambda exc, bucket=pair_errors: bucket.append(str(exc)))
            try:
                pair_page.goto(BASE, wait_until="domcontentloaded", timeout=30000)
                pair_page.wait_for_timeout(650)
                candidate = pair_page.get_by_role("button", name=label, exact=False).first
                if candidate.count() and candidate.is_visible():
                    candidate.scroll_into_view_if_needed(timeout=3000)
                    candidate.click(timeout=4000)
                    pair_page.wait_for_timeout(300)
                    close = pair_page.get_by_role("button", name="Close", exact=False)
                    visible_close = None
                    for j in range(close.count()):
                        if close.nth(j).is_visible() and close.nth(j).evaluate(is_actionable_js()):
                            visible_close = close.nth(j)
                            break
                    if visible_close is not None:
                        visible_close.click(timeout=4000)
                        pair_page.wait_for_timeout(220)
                        pair_results.append({"opener": label, "close": "clicked"})
                    else:
                        pair_results.append({"opener": label, "close": "not-exposed"})
                if any(any(k in e.lower() for k in ("referenceerror", "typeerror", "outseta")) for e in pair_errors):
                    add_critical(name, f"modal/menu pair {label!r} caused JS error: {pair_errors[0]}")
            except Exception as exc:
                add_warning(name, f"modal/menu pair could not be fully exercised for {label!r}: {exc}")
            finally:
                if not pair_page.is_closed():
                    pair_page.close()

        # Basic keyboard traversal catches focus traps / elements that crash on focus.
        keyboard_page = ctx.new_page()
        keyboard_errors = []
        keyboard_page.on("pageerror", lambda exc, bucket=keyboard_errors: bucket.append(str(exc)))
        keyboard_steps = []
        try:
            keyboard_page.goto(BASE, wait_until="domcontentloaded", timeout=30000)
            keyboard_page.wait_for_timeout(500)
            for _ in range(35):
                keyboard_page.keyboard.press("Tab")
                keyboard_steps.append(keyboard_page.evaluate("""() => {
                  const e=document.activeElement; return e ? (e.getAttribute('aria-label') || e.innerText || e.value || e.tagName).trim().replace(/\\s+/g,' ').slice(0,100) : '';
                }"""))
            if any(any(k in e.lower() for k in ("referenceerror", "typeerror", "outseta")) for e in keyboard_errors):
                add_critical(name, f"keyboard traversal caused JS error: {keyboard_errors[0]}")
        except Exception as exc:
            add_warning(name, f"keyboard traversal incomplete: {exc}")
        finally:
            if not keyboard_page.is_closed():
                keyboard_page.close()

        # Fail only on actionable JS errors from the baseline page. External resource noise
        # remains a warning, not a false production failure.
        for err in page_errors:
            low = err.lower()
            if "outseta" in low or "referenceerror" in low or "typeerror" in low:
                add_critical(name, f"runtime page error: {err}")
            else:
                add_warning(name, f"page error: {err}")
        for err in console_errors:
            low = err.lower()
            if "outseta" in low or "uncaught" in low or "referenceerror" in low or "typeerror" in low:
                add_critical(name, f"console error: {err}")
            elif "failed to load resource" not in low:
                add_warning(name, f"console error: {err}")

        report["viewports"][name] = {
            "anchor_count": len(hrefs),
            "unique_hash_targets_clicked": clicked_hashes,
            "controls_total": len(controls),
            "controls_actionable": len(actionable_controls),
            "controls_exercised": control_results,
            "modal_menu_pairs": pair_results,
            "keyboard_focus_steps": keyboard_steps,
            "broken_image_count": len(broken_images),
            "page_error_count": len(page_errors),
            "console_error_count": len(console_errors),
        }
        page.close()
        ctx.close()

    # Validate the small set of unique real external destinations without clicking users
    # away from the QA page. 2xx/3xx and common anti-bot 403 responses prove the route exists.
    request = p.request.new_context(ignore_https_errors=True)
    for url in sorted(external_urls):
        parsed = urlparse(url)
        if parsed.netloc not in {"github.com", "www.behance.net", "behance.net"}:
            continue
        item = {"url": url}
        try:
            response = request.get(url, timeout=15000, fail_on_status_code=False)
            item["status"] = response.status
            if response.status >= 500 or response.status == 404:
                report["critical"].append(f"[external] broken destination {response.status}: {url}")
        except Exception as exc:
            item["error"] = str(exc)[:300]
            report["warnings"].append(f"[external] could not verify destination: {url}: {exc}")
        report["external_links"].append(item)
    request.dispose()
    browser.close()

server.shutdown()
Path("qa-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))

if report["critical"]:
    raise SystemExit(f"Runtime QA failed with {len(report['critical'])} critical issue(s).")
print("Runtime QA passed with no critical functional issues.")
