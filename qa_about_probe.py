from __future__ import annotations

import hashlib
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

HOST = "127.0.0.1"
PORT = 4174
URL = f"http://{HOST}:{PORT}/index.html"
TARGET = '[data-gg-qa-control="control-023"]'


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


def sha(s: str) -> str:
    return hashlib.sha256((s or "").encode()).hexdigest()


def snapshot(page):
    return page.evaluate("""() => {
      const all=[...document.querySelectorAll('*')];
      const visible=e=>{
        const s=getComputedStyle(e), r=e.getBoundingClientRect();
        return r.width>0 && r.height>0 && s.display!=='none' && s.visibility!=='hidden' && parseFloat(s.opacity||'1')>0.01;
      };
      const interesting=all.filter(e => {
        const c=String(e.className||'').toLowerCase();
        const id=String(e.id||'').toLowerCase();
        return c.includes('about') || c.includes('modal') || c.includes('overlay') || c.includes('dialog') || id.includes('about') || id.includes('modal') || e.hasAttribute('data-modal') || e.hasAttribute('data-modal-trigger') || e.getAttribute('role')==='dialog';
      }).map(e=>{
        const s=getComputedStyle(e), r=e.getBoundingClientRect();
        return {
          tag:e.tagName,
          id:e.id||'',
          cls:String(e.className||''),
          text:(e.innerText||'').trim().replace(/\\s+/g,' ').slice(0,120),
          dataModal:e.getAttribute('data-modal'),
          dataTrigger:e.getAttribute('data-modal-trigger'),
          ariaHidden:e.getAttribute('aria-hidden'),
          ariaExpanded:e.getAttribute('aria-expanded'),
          visible:visible(e),
          display:s.display,
          visibility:s.visibility,
          opacity:s.opacity,
          pointerEvents:s.pointerEvents,
          transform:s.transform,
          position:s.position,
          rect:[Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]
        };
      });
      const fixed=all.filter(e=>{
        const s=getComputedStyle(e), r=e.getBoundingClientRect();
        return (s.position==='fixed' || s.position==='absolute') && r.width>0 && r.height>0 && (s.display!=='none');
      }).map(e=>{
        const s=getComputedStyle(e), r=e.getBoundingClientRect();
        return [e.tagName,e.id||'',String(e.className||''),s.display,s.visibility,s.opacity,s.pointerEvents,s.transform,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];
      });
      return {
        url:location.href,
        hash:location.hash,
        scrollY:window.scrollY,
        active:(document.activeElement?.innerText || document.activeElement?.getAttribute?.('aria-label') || document.activeElement?.tagName || '').trim().slice(0,120),
        bodyClass:String(document.body.className||''),
        bodyStyle:document.body.getAttribute('style')||'',
        htmlClass:String(document.documentElement.className||''),
        interesting,
        fixed
      };
    }""")


server = ThreadingHTTPServer((HOST, PORT), Quiet)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(0.2)

report = {"attempts": []}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for activation in ("click", "enter", "space"):
        ctx = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
        page = ctx.new_page()
        errors=[]
        page.on("pageerror", lambda exc, b=errors: b.append(str(exc)))
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(1200)
        target=page.locator(TARGET)
        if target.count()!=1:
            report["attempts"].append({"activation":activation,"error":f"target count {target.count()}"})
            ctx.close(); continue
        target.evaluate("e=>e.scrollIntoView({block:'center',inline:'center'})")
        page.wait_for_timeout(150)
        before=snapshot(page)
        before_html=sha(page.locator("body").evaluate("e=>e.outerHTML"))
        if activation=="click":
            target.click(timeout=3000)
        else:
            target.focus()
            page.keyboard.press("Enter" if activation=="enter" else "Space")
        frames=[]
        for delay in (0,50,200,500,1000):
            if delay: page.wait_for_timeout(delay)
            state=snapshot(page)
            state["bodyHtmlHash"]=sha(page.locator("body").evaluate("e=>e.outerHTML"))
            frames.append({"delay_ms":delay,"state":state})
        report["attempts"].append({
            "activation":activation,
            "before":before,
            "beforeBodyHtmlHash":before_html,
            "frames":frames,
            "pageErrors":errors,
        })
        ctx.close()
    browser.close()

server.shutdown()
Path("about-probe.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
