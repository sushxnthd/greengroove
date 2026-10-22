"""CI regression checks for the published static document (no external requests)."""
import json,threading
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright,expect
import traceback
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',4173),Quiet)
threading.Thread(target=server.serve_forever,daemon=True).start()
out=root/'docs/visual-qa/browser';out.mkdir(exist_ok=True)
report=[]
with sync_playwright() as p:
 for engine in ['chromium','firefox','webkit']:
  browser=getattr(p,engine).launch()
  for width,height in [(390,844),(768,1024),(1440,1000)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   page=context.new_page();errors=[];external=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:4173/','data:')) else None)
   try:
    page.goto('http://127.0.0.1:4173/',wait_until='load')
    page.evaluate('document.fonts.ready')
    page.get_by_role('button',name='Open menu',exact=True).click()
    page.get_by_role('link',name='Groove Band',exact=True).first.click()
    assert page.locator('#gg-layer-title').inner_text()=='Groove Band'
    page.get_by_role('button',name='Close system detail',exact=True).click()
    page.get_by_role('button',name='Open interactive system walkthrough',exact=True).click()
    page.get_by_role('button',name='Pick milk · ₹60',exact=True).click()
    page.get_by_role('button',name='Pick yogurt · ₹25',exact=True).click()
    page.get_by_role('button',name='Return milk',exact=True).click()
    assert page.locator('#gg-cart-total').inner_text()=='₹25'
    page.get_by_role('button',name='Ambiguous pickup',exact=True).click()
    page.get_by_role('button',name='Confirm invoice',exact=True).click()
    assert 'Resolve held events' in page.locator('#gg-demo-status').inner_text()
    assert page.locator('#gg-cart-total').inner_text()=='₹25'
    page.get_by_role('button',name='Resolve held pickup',exact=True).click()
    page.get_by_role('button',name='Confirm invoice',exact=True).click()
    assert page.locator('#gg-cart-total').inner_text()=='₹50'
    assert 'No payment' in page.locator('#gg-demo-status').inner_text()
    page.get_by_role('button',name='Reset walkthrough',exact=True).click()
    assert page.locator('#gg-cart-total').inner_text()=='₹0'
    page.get_by_role('button',name='Close walkthrough',exact=True).click()
    page.get_by_role('button',name='Next',exact=True).click()
    expect(page.locator('.pricing-card__title')).to_have_text(['Technical testing','Field evaluation'])
    page.get_by_role('button',name='Today',exact=True).click()
    page.get_by_role('button',name='Next build component',exact=True).click()
    assert page.locator('#gg-gallery-position').inner_text()=='2 / 7'
    page.get_by_role('button',name='Explore Green Grooves',exact=True).click()
    assert page.locator('#gg-layer-title').inner_text()=='Green Grooves'
    page.get_by_role('button',name='Close system detail',exact=True).click()
    page.get_by_role('button',name='About the project',exact=True).click()
    assert page.locator('#gg-about').is_visible()
    page.keyboard.press('Escape')
    expect(page.locator('#gg-about')).not_to_be_visible()
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    assert not external,external
    assert not errors,errors
    page.get_by_role('link',name='go to homepage',exact=True).click()
    page.screenshot(path=str(out/f'{engine}-{width}.png'),full_page=True)
    report.append({'engine':engine,'width':width,'result':'pass'})
   except Exception as e:
    report.append({'engine':engine,'width':width,'result':'fail','error':str(e),'traceback':traceback.format_exc(),'console':errors,'external':external})
    page.screenshot(path=str(out/f'{engine}-{width}-failure.png'))
   context.close()
  browser.close()
server.shutdown()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
raise SystemExit(any(r['result']=='fail' for r in report))
