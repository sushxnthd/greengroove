"""Exercise original controls at phone, tablet and desktop widths in three engines."""
import json,threading,traceback
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',4173),Quiet)
threading.Thread(target=server.serve_forever,daemon=True).start()
out=root/'docs/visual-qa/browser';out.mkdir(parents=True,exist_ok=True);report=[]
with sync_playwright() as p:
 for engine in ['chromium','firefox','webkit']:
  browser=getattr(p,engine).launch()
  for width,height in [(390,844),(768,1024),(1440,1000)]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   page=context.new_page();errors=[];external=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:4173/','data:')) else None)
   def close():
    page.get_by_role('button',name='Close showcase',exact=True).click()
    expect(page.locator('[data-modal-target=showcase]')).not_to_have_attribute('data-modal-status','active')
   try:
    page.goto('http://127.0.0.1:4173/',wait_until='load');page.locator('body.gg-repair-ready').wait_for();page.evaluate('document.fonts.ready')
    assert page.locator('.about-card__img').evaluate_all(r'(es)=>es.every(e=>/assets\/people\/(sushanth|aryan)\.webp$/.test(e.getAttribute("src")))'), 'Founder portrait wiring changed'
    assert page.locator('.about-card__img-layer').first.locator('img').first.evaluate('(e)=>getComputedStyle(e).visibility==="visible"'), 'Paused portrait hidden'
    assert page.locator('.about-card__img-layer').nth(1).evaluate('(e)=>getComputedStyle(e).visibility==="hidden"'), 'Paused inner mask hides the portrait'
    assert page.locator('img[src*=g02]').count()==0, 'Placeholder portrait logos returned'
    assert page.locator('.trustedby-marquee__item-svg image[href$="amity-readable.svg"]').first.evaluate('(e)=>getComputedStyle(e).filter==="none"'), 'AISG46 wordmark is blacked out'
    assert page.locator('.trustedby-marquee__item-svg image').evaluate_all('(es)=>es.every(e=>getComputedStyle(e).filter==="none")'), 'Logo colour filter returned'
    assert page.locator('#build .showcase-media__image').evaluate_all('(es)=>es.every(e=>getComputedStyle(e).objectFit==="cover")'), 'Build previews are zoomed out'
    assert page.locator('.join-faces__image-el').evaluate_all('(es)=>es.every(e=>parseFloat(getComputedStyle(e).marginRight)<0)'), 'Native Osmo institution overlap was lost'
    assert page.locator('.join-faces__image-el').evaluate_all('(es)=>es.every(e=>parseFloat(getComputedStyle(e).borderTopLeftRadius)>0)'), 'Native circular institution framing was lost'
    assert page.locator('.trustedby-marquee__item-svg').evaluate_all('(es)=>es.every(e=>e.viewBox.baseVal.width===172&&e.viewBox.baseVal.height===42)'), 'Wide Osmo logo geometry was lost'
    assert page.locator('a[href="https://www.linkedin.com/in/sushxnthd/"]').count()>=1, 'Sushanth LinkedIn missing'
    assert page.locator('a[href="https://www.linkedin.com/in/0aryan-kumar0/"]').count()>=1, 'Aryan LinkedIn missing'
    assert 'Earned to date' in page.locator('body').inner_text(), 'Earned milestone missing'
    assert page.locator('img[src*=g04]').count()==0, 'Additional rings returned'
    assert 'Haffer'  in page.locator('body').evaluate('(e)=>getComputedStyle(e).fontFamily')
    assert page.locator('.home-hero h1').evaluate('(e)=>Math.abs(parseFloat(getComputedStyle(e).letterSpacing)/parseFloat(getComputedStyle(e).fontSize)+.06)<.0001'), 'Hero tracking differs from live Osmo CSS'
    assert page.locator('[data-wf--button-theme--variant=purple]').evaluate_all('(es)=>es.every(e=>getComputedStyle(e).backgroundImage==="none")'), 'Unrequested gradients returned'
    if width>=992:
     assert page.locator('.pricing-card').evaluate_all('(es)=>es.every(e=>Math.abs(e.getBoundingClientRect().width-35*parseFloat(getComputedStyle(e).fontSize))<1)'), 'Evidence cards exceed the measured native 35em width'
    page.screenshot(path=str(out/f'{engine}-{width}-hero.png'))
    page.get_by_role('button',name='Open menu',exact=True).click()
    expect(page.locator('.nav')).to_have_attribute('data-nav-status','active')
    page.locator('.nav-bar__bottom a[href="#groove-band"]').click()
    expect(page.locator('#gg-native-detail-title')).to_have_text('Groove Band');close()
    for name in ['Identity','Shelf Events','Association','Reversibility','Live Cart','Settlement']:
     control=page.get_by_role('button',name='Show '+name+' layer',exact=True);control.click();expect(control).to_have_attribute('aria-pressed','true')
     page.get_by_role('button' if name=='Reversibility' else 'link',name='Explore '+name,exact=True).click()
     expect(page.locator('#gg-native-detail-title')).to_have_text(name)
     image=page.locator('[data-modal-target=showcase] [data-res-used=item-img]');expect(image).to_have_js_property('complete',True);assert image.evaluate('(e)=>e.naturalWidth')>0
     close()
    page.get_by_role('button',name='Show Identity layer',exact=True).click();page.screenshot(path=str(out/f'{engine}-{width}-layers.png'))
    for i in range(5):
     # Keyboard reaches the source bullet controls even when hidden on phones.
     page.get_by_role('button',name='Next project note',exact=True).click()
     note=page.locator('.latest-resources-slider [data-vertical-slider-item][aria-hidden="false"]')
     expect(note).to_have_attribute('data-slide-id',str((i+1)%5))
     note.locator('[data-gg-detail]').press('Enter');expect(page.locator('[data-modal-target=showcase]')).to_have_attribute('data-modal-status','active');close()
    for i in range(6):
     page.get_by_role('button',name='Next finding',exact=True).click()
     active=page.locator('#findings [data-vertical-slider-item][aria-hidden="false"]');expect(active).to_have_attribute('data-slide-id',str((i+1)%6))
     art=page.locator('.testimonial-globe__img.is--active');expect(art).to_have_css('opacity','1')
     if art.is_visible():
      expect(art).to_have_js_property('complete',True);assert art.evaluate('(e)=>e.naturalWidth')>0
    page.screenshot(path=str(out/f'{engine}-{width}-findings.png'))
    page.get_by_role('button',name='Next',exact=True).click();expect(page.locator('.pricing-card__title')).to_have_text(['Technical testing','Field evaluation'])
    page.get_by_role('button',name='Today',exact=True).click();expect(page.locator('.pricing-card__title')).to_have_text(['Selected + funded','Built'])
    page.get_by_role('button',name='Play Green Groove demo',exact=True).click();expect(page.locator('#gg-demo-player')).to_be_visible()
    player=page.locator('#gg-demo-player video');expect(player).to_have_attribute('controls','')
    page.wait_for_function('document.querySelector("#gg-demo-player video").currentTime>0',timeout=12000)
    page.get_by_role('button',name='Close demo',exact=True).click();expect(page.locator('#gg-demo-player')).not_to_be_visible();expect(player).to_have_js_property('paused',True)
    hit=page.locator('[data-flick-cards-item][aria-hidden="false"] [data-gg-build]');hit.press('ArrowRight')
    card=page.locator('[data-flick-cards-item][aria-hidden="false"]');expect(card.locator('h3')).to_have_text('Green Grooves');card.locator('[data-gg-build]').press('Enter');expect(page.locator('#gg-native-detail-title')).to_have_text('Green Grooves');close()
    page.get_by_role('link',name='System overview',exact=True).click();expect(page.locator('#gg-native-detail-title')).to_have_text('Six-layer system');close()
    page.get_by_role('link',name='Explore build',exact=True).click();expect(page.locator('#gg-native-detail-title')).to_have_text('Green Grooves');close()
    page.get_by_role('button',name='About the project',exact=True).click();expect(page.locator('[data-modal-target=about]')).to_have_attribute('data-modal-status','active');page.keyboard.press('Escape');expect(page.locator('[data-modal-target=about]')).not_to_have_attribute('data-modal-status','active')
    page.get_by_role('button',name='Use light preview',exact=True).click();expect(page.locator('[data-marketing-theme]')).to_have_attribute('data-marketing-theme','light');expect(page.locator('.is--try-vault-light')).to_have_css('opacity','1')
    page.get_by_role('button',name='Use dark preview',exact=True).click();expect(page.locator('[data-marketing-theme]')).to_have_attribute('data-marketing-theme','dark')
    if width<768:
     top=page.locator('footer .footer-link__col-top').first;top.click();expect(top).to_have_attribute('aria-expanded','true');top.click();expect(top).to_have_attribute('aria-expanded','false')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    assert page.locator('.info h3').evaluate('(e)=>e.getBoundingClientRect().width>=Math.min(300,innerWidth*.6)'), 'Legacy viewport guard narrowed the heading'
    assert page.locator('.info p.p-m').evaluate_all('(es)=>es.every(e=>e.getBoundingClientRect().width>=Math.min(160,innerWidth*.3))'), 'Legacy viewport guard narrowed body copy'
    assert not errors,errors;assert not external,external
    page.get_by_role('link',name='go to homepage',exact=True).click();page.screenshot(path=str(out/f'{engine}-{width}-full.png'),full_page=True)
    # Normal-motion entrance and native animation smoke check.
    page.emulate_media(reduced_motion='no-preference');page.goto('http://127.0.0.1:4173/');page.locator('body.gg-repair-ready').wait_for()
    page.wait_for_function('getComputedStyle(document.querySelector("main")).height !== innerHeight+"px"')
    page.wait_for_function('[...document.querySelectorAll(".home-hero__title-row .text-line-mask")].every(e=>getComputedStyle(e).overflow==="visible")')
    page.screenshot(path=str(out/f'{engine}-{width}-motion.png'))
    assert not errors,errors
    report.append({'engine':engine,'width':width,'result':'pass'});print(engine,width,'pass',flush=True)
   except Exception as e:
    report.append({'engine':engine,'width':width,'result':'fail','error':str(e),'traceback':traceback.format_exc(),'console':errors,'external':external});page.screenshot(path=str(out/f'{engine}-{width}-failure.png'))
   context.close()
  browser.close()
server.shutdown();(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));raise SystemExit(any(r['result']=='fail' for r in report))
