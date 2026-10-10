from __future__ import annotations

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


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


server = ThreadingHTTPServer((HOST, PORT), Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.2)

report = {"critical": [], "warnings": [], "viewports": {}}


def add_critical(view, msg):
    report["critical"].append(f"[{view}] {msg}")


def add_warning(view, msg):
    report["warnings"].append(f"[{view}] {msg}")


viewports = {
    "desktop": {"width": 1440, "height": 1000},
    "mobile": {"width": 390, "height": 844},
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
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
            page.wait_for_timeout(2500)
        except Exception as exc:
            add_critical(name, f"page failed to load: {exc}")
            ctx.close()
            continue

        if page.locator("h1").count() == 0:
            add_critical(name, "no H1 rendered")

        # Exercise lazy media/scroll-triggered sections without altering content.
        total_h = page.evaluate("document.documentElement.scrollHeight")
        step = max(viewport["height"] // 2, 300)
        for y in range(0, min(int(total_h), 50000), step):
            page.evaluate("y => window.scrollTo(0, y)", y)
            page.wait_for_timeout(20)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(300)

        # Validate all anchor destinations and actively click each unique in-page target.
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
                exists = page.locator(f"#{target}").count() > 0
                if not exists:
                    add_critical(name, f"missing hash target: {href}")
                elif href not in unique_hashes:
                    unique_hashes.append(href)
            else:
                parsed = urlparse(href)
                if parsed.scheme in {"http", "https"} and parsed.netloc == PROJECT_HOST:
                    if not (parsed.path == "/greengroove/" or parsed.path.startswith("/greengroove/#")):
                        add_critical(name, f"same-host route escapes project path: {href}")

        clicked = []
        for href in unique_hashes:
            try:
                page.evaluate(
                    "href => { const a=[...document.querySelectorAll('a[href]')].find(x=>x.getAttribute('href')===href); if(a) a.click(); }",
                    href,
                )
                page.wait_for_timeout(50)
                current_hash = page.evaluate("location.hash")
                if current_hash != href:
                    add_warning(name, f"hash click did not update location immediately: {href} -> {current_hash}")
                clicked.append(href)
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

        # Exercise accessible expandable/menu controls where present.
        controlled = page.locator("[aria-expanded][aria-controls]")
        controlled_results = []
        for i in range(min(controlled.count(), 30)):
            el = controlled.nth(i)
            try:
                if not el.is_visible():
                    continue
                before_expanded = el.get_attribute("aria-expanded")
                control_id = el.get_attribute("aria-controls")
                el.click(timeout=2500)
                page.wait_for_timeout(120)
                after_expanded = el.get_attribute("aria-expanded")
                controlled_results.append({"id": control_id, "before": before_expanded, "after": after_expanded})
                if before_expanded == after_expanded:
                    add_warning(name, f"aria-expanded control did not toggle: {control_id}")
                # Restore when possible.
                el.click(timeout=2500)
            except Exception as exc:
                add_warning(name, f"expandable control test could not complete: {exc}")

        # Record every visible button/control so the report proves coverage.
        controls = page.locator("button, input[type=submit], [role=button]").evaluate_all(
            "els => els.filter(e => { const r=e.getBoundingClientRect(); const s=getComputedStyle(e); return r.width>0 && r.height>0 && s.display!=='none' && s.visibility!=='hidden'; }).map(e => ({tag:e.tagName, text:(e.innerText||e.value||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,160), ariaExpanded:e.getAttribute('aria-expanded'), ariaControls:e.getAttribute('aria-controls')}))"
        )

        # Fail only on actionable JS errors. External asset/network noise is recorded as warnings.
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
            "unique_hash_targets_clicked": clicked,
            "visible_controls": controls,
            "expandable_controls_tested": controlled_results,
            "broken_image_count": len(broken_images),
            "page_error_count": len(page_errors),
            "console_error_count": len(console_errors),
        }
        ctx.close()

    browser.close()

server.shutdown()
Path("qa-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))

if report["critical"]:
    raise SystemExit(f"Runtime QA failed with {len(report['critical'])} critical issue(s).")
print("Runtime QA passed with no critical functional issues.")
