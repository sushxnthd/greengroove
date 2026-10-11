from __future__ import annotations

import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

HOST = "127.0.0.1"
PORT = 4177
URL = f"http://{HOST}:{PORT}/index.html"


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


CLIP_AUDIT_JS = r"""() => {
  const semantic = new Set(['H1','H2','H3','H4','H5','H6','P','LI','BLOCKQUOTE','FIGCAPTION','DT','DD','LABEL']);
  const intentional = /(marquee|ticker|carousel|slider|track|duplicate|clone|button-label|nav-marquee|loading|transition)/i;
  const out = [];

  function inViewport(r) {
    return r.bottom > -2 && r.top < innerHeight + 2 && r.right > -2 && r.left < innerWidth + 2;
  }

  function visible(el) {
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1 && inViewport(r) &&
      s.display !== 'none' && s.visibility !== 'hidden' &&
      parseFloat(s.opacity || '1') > 0.02 && el.getAttribute('aria-hidden') !== 'true' &&
      !el.closest('[inert]');
  }

  function ident(el) {
    if (!el) return '';
    const id = el.id ? `#${el.id}` : '';
    const cls = String(el.className || '').trim().split(/\s+/).filter(Boolean).slice(0,4).map(x=>`.${x}`).join('');
    return `${el.tagName.toLowerCase()}${id}${cls}`;
  }

  function clips(el) {
    const s = getComputedStyle(el);
    const oy = s.overflowY, ox = s.overflowX;
    const cp = s.clipPath && s.clipPath !== 'none';
    const mask = s.maskImage && s.maskImage !== 'none';
    return ox === 'hidden' || ox === 'clip' || oy === 'hidden' || oy === 'clip' || cp || mask;
  }

  const all = [...document.body.querySelectorAll('*')];
  for (const el of all) {
    if (!visible(el)) continue;
    if (intentional.test(String(el.className || ''))) continue;

    const direct = [...el.childNodes].filter(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
    if (!direct.length) continue;
    const text = direct.map(n => n.textContent).join(' ').trim().replace(/\s+/g, ' ');
    if (text.length < 4) continue;
    if (!semantic.has(el.tagName) && !(el.tagName === 'SPAN' && text.length >= 28)) continue;
    if (el.closest('button,[role="button"]')) continue;

    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter(r => r.width > .5 && r.height > .5 && inViewport(r));
    if (!rects.length) continue;

    let anc = el;
    let depth = 0;
    while (anc && anc !== document.body && depth++ < 8) {
      if (intentional.test(String(anc.className || ''))) break;
      if (clips(anc)) {
        const ar = anc.getBoundingClientRect();
        const bad = rects.some(r =>
          r.left < ar.left - 1.5 || r.right > ar.right + 1.5 ||
          r.top < ar.top - 1.5 || r.bottom > ar.bottom + 1.5
        );
        if (bad) {
          const s = getComputedStyle(anc);
          out.push({
            text: text.slice(0, 180),
            element: ident(el),
            clipper: ident(anc),
            overflowX: s.overflowX,
            overflowY: s.overflowY,
            clipPath: s.clipPath,
            scrollY: Math.round(scrollY),
            elementRect: (()=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}})(),
            clipperRect: {x:ar.x,y:ar.y,w:ar.width,h:ar.height}
          });
          break;
        }
      }
      anc = anc.parentElement;
    }

    const s = getComputedStyle(el);
    const clamp = s.webkitLineClamp;
    if (clamp && clamp !== 'none' && clamp !== '0' && el.scrollHeight > el.clientHeight + 1) {
      out.push({
        text: text.slice(0,180),
        element: ident(el),
        clipper: ident(el),
        overflowX: s.overflowX,
        overflowY: s.overflowY,
        lineClamp: clamp,
        reason: 'line-clamp-truncation',
        scrollY: Math.round(scrollY)
      });
    }
  }

  const seen = new Set();
  return out.filter(x => {
    const k = `${x.text}|${x.element}|${x.clipper}|${x.reason || ''}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}"""

server = ThreadingHTTPServer((HOST, PORT), Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.2)

report = {"viewports": {}, "candidate_count": 0}
viewports = {
    "desktop": {"width": 1440, "height": 1000},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for name, viewport in viewports.items():
        ctx = browser.new_context(viewport=viewport, reduced_motion="reduce")
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1200)
        page.evaluate("document.documentElement.style.scrollBehavior='auto'")

        total_h = int(page.evaluate("document.documentElement.scrollHeight"))
        step = max(int(viewport["height"] * 0.72), 320)
        merged = {}
        for y in range(0, min(total_h, 60000), step):
            page.evaluate("y => window.scrollTo(0,y)", y)
            page.wait_for_timeout(220)
            for item in page.evaluate(CLIP_AUDIT_JS):
                key = f"{item.get('text')}|{item.get('element')}|{item.get('clipper')}|{item.get('reason','')}"
                merged.setdefault(key, item)

        last_y = max(0, total_h - viewport["height"])
        page.evaluate("y => window.scrollTo(0,y)", last_y)
        page.wait_for_timeout(350)
        for item in page.evaluate(CLIP_AUDIT_JS):
            key = f"{item.get('text')}|{item.get('element')}|{item.get('clipper')}|{item.get('reason','')}"
            merged.setdefault(key, item)

        candidates = list(merged.values())
        report["viewports"][name] = candidates
        report["candidate_count"] += len(candidates)
        ctx.close()
    browser.close()

server.shutdown()
Path("qa-text-clipping.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
print(f"Text clipping audit found {report['candidate_count']} user-visible candidate(s) across three viewports.")
