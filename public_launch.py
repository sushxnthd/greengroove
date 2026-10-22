"""Apply the public-site layer after legacy generation, without changing brand geometry."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
p=Path('index.html'); s=BeautifulSoup(p.read_text(),'html.parser')
if s.select_one('meta[name="gg-public-release"]'): raise SystemExit('Public release already applied')
def fragment(html):return BeautifulSoup(html,'html.parser')
def replace(el,html):el.replace_with(fragment(html)) if el else None
def label(el,text):
 for x in el.select('.button-label span,.button-label.eyebrow,.button-label:not(:has(*))'):x.string=text
# Runtime is entirely local; no account, payment, telemetry or unrelated-video integrations.
for el in s.select('script[src],#gg-outseta-compat,#gg-production-behavior,.sitemap'):el.decompose()
for el in s.select('script'):
 if el.get('type')!='application/ld+json' and ('plausible' in el.text or 'w-mod-' in el.text):el.decompose()
for el in s.select('link[rel=stylesheet]'):
 u=el['href']
 urls=['https://cdn.prod.website-files.com/68a5787bba0829184628bd51/css/osmo-v2.shared.b1655ef4a.min.css','https://slater.app/16596/45154.css','https://slater.app/16596/45446.css','https://slater.app/16596/45511.css','https://slater.app/16596/45156.css']
 if u in urls:
  el['href']=f'assets/vendor/style-{urls.index(u)}.css';el.attrs.pop('integrity',None)
for el in s.select('link[rel=preconnect]'):el.decompose()
for el in s.select('video,.custom-player__loading,.showcase-media__loading,.flick-card__hidden-profile-pic,.used-sitemap'):el.decompose()
for el in s.find_all():
 for a in list(el.attrs):
  if a.startswith(('sm-','data-player-','data-bunny-','data-res-used','data-resources-date','data-updates-date','data-plausible','data-outseta','data-o-')):del el[a]
for el in s.select('img'):
 if not el.get('src'):el.decompose();continue
 el.attrs.pop('srcset',None);el.attrs.pop('sizes',None)
 el['decoding']='async'
# Correct semantics and labels before enhancement runs.
s.html['lang']='en';s.body['data-gg-public']='true'
s.select_one('main')['id']='main-content'
s.body.insert(0,fragment('<a class="gg-skip" href="#main-content">Skip to content</a>'))
for el in s.select('button'):el['type']='button'
for el in s.select('a[href^="#"]'):el.attrs.pop('target',None)
for el in s.select('a[target="_blank"]'):el['rel']='noopener noreferrer'
for el in s.select('a[href="https://sushxnthd.github.io/greengroove/"]'):el['href']='#home'
for el in s.select('a button'):el.name='span';el.attrs.pop('type',None)
for el in s.select('[data-nav-toggle="toggle"]'):
 el.name='button';el['type']='button';el['aria-expanded']='false';el['aria-controls']='gg-navigation';el['aria-label']='Open menu'
s.select_one('.nav-bar__bottom')['id']='gg-navigation' if s.select_one('.nav-bar__bottom') else 'gg-navigation'
for el in s.select('[data-marketing-theme-toggle]'):el['aria-label']='Toggle colour theme'
# Keep the original people and logo; discard template accounts and portraits.
for el in s.select('[data-modal-target="about"] .button-row.mobile--small'):el.decompose()
for el in s.select('[data-gg-hidden="template-person"]'):el.parent.decompose()
for el in s.select('.about-map__outline,.about-gallery,.profile-picture'):el.decompose()
for el in s.select('.about-card__text-h h3'):
 el.attrs.pop('style',None)
for el in s.select('[data-modal-trigger="about"], [data-gg-qa-control="control-001"]'):
 el['data-gg-dialog']='gg-about'
for el in s.select('[data-modal-trigger], [data-modal-close]'):
 el.attrs.pop('data-modal-trigger',None);el.attrs.pop('data-modal-close',None)
about=s.select_one('[data-modal-target="about"]')
intro=about.select_one('.about-intro').get_text(' ',strip=True)
about_html=f'<dialog id="gg-about" class="gg-dialog" aria-labelledby="gg-about-title"><button class="gg-dialog-close" data-gg-close aria-label="Close about the project">Close ×</button><p class="gg-kicker">The people behind the prototype</p><h2 id="gg-about-title">Sushanth Dasari<br>&amp; Aryan Kumar</h2><p>{intro}</p><p>Three connected modules. Six system layers. Developed under NCERT PRAYAAS, with IIT Delhi as the associated HEI.</p><a class="gg-text-link" href="https://www.behance.net/gallery/211169339/Green-Groove" target="_blank" rel="noopener noreferrer">Read the project case study ↗</a></dialog>'
for el in s.select('[data-modal-wrap]'):el.decompose()
s.body.append(fragment(about_html))
# The updates area is a real destination, without collecting names or email addresses.
form=s.select_one('footer form')
replace(form,'<div class="gg-source-follow"><p class="p-m">Build notes, design decisions and source code, published as the project develops.</p><a class="gg-solid-link" href="https://github.com/sushxnthd/greengroove" target="_blank" rel="noopener noreferrer">Explore the source ↗</a><a class="gg-text-link" href="https://www.behance.net/gallery/211169339/Green-Groove" target="_blank" rel="noopener noreferrer">Read the case study ↗</a></div>')
for el in s.select('.w-form-done,.w-form-fail'):el.decompose()
# Remove stale badges and fake template-relative dates.
for el in s.find_all(string=True):
 if el.strip() in ['NEW','new','New']:el.replace_with('')
for el in s.select('[data-updates-date],[data-resources-date]'):el.string='Prototype'
for el in s.select('a'):
 text=el.get_text(' ',strip=True)
 if text in ['See recognition See recognition','Programme evidence']:el['href']='#programme-sources'
 if text in ['See the build See the build','View build']:el['href']='#build'
 if text=='Contact':el.string='Discuss the project';el['href']='https://github.com/sushxnthd/greengroove/issues';el['target']='_blank';el['rel']='noopener noreferrer'
 if text=='Questions':el['href']='#questions'
 if text=='Evidence 06':
  for x in el.select('.tag'):x.decompose()
 if text=='Selected under NCERT PRAYAAS '*7+'Selected under NCERT PRAYAAS':el['href']='#programme-sources';el.attrs.pop('target',None)
# Expose each technical layer through its own readable detail panel.
layers=[('Identity','a01-identity-layer.svg','A wristband identifies an active shopping session. An identity read establishes cart context; it does not by itself prove who picked up an item.'),('Shelf Events','a02-shelf-events-layer.svg','A load-cell change and RFID observations form a candidate shelf event. Calibration, product weight variation and simultaneous actions still need controlled testing.'),('Association','a03-association-layer.svg','A detected event must be matched to one valid shopping session before a cart changes. Ambiguous candidates stay on hold for review.'),('Reversibility','a04-reversibility-layer.svg','A return references an earlier accepted pickup. The inverse event changes quantity while preserving both actions in the history.'),('Live Cart','a05-live-cart-layer.svg','Accepted events determine quantities and subtotal. Held events stay separate so uncertainty cannot silently become a charge.'),('Settlement','a06-settlement-layer.svg','The final accepted cart becomes an invoice summary. Payment processing and a commercial deployment are separate from this prototype.')]
for i,(name,asset,desc) in enumerate(layers):
 el=s.select_one('#layer-'+['identity','shelf-events','association','reversibility','live-cart','settlement'][i])
 if el:
  el.name='a';el['href']='#layer-detail';el['data-gg-layer']=str(i)
  if not el.select_one('.button'):
   el.append(fragment('<span class="gg-discover">Discover ↗</span>'))
  for b in el.select('button'):b.name='span';b.attrs.pop('type',None)
# Build gallery is about components, not template resource credits.
for i,el in enumerate(s.select('[data-flick-cards-item]')):
 title=el.select_one('h3').get_text(' ',strip=True);el['data-gg-build-title']=title
 trigger=el.select_one('.flick-card__click')
 if trigger:trigger.name='button';trigger['type']='button';trigger['aria-label']='Explore '+title;trigger['data-gg-build']=str(i)
 bottom=el.select_one('.flick-card__bottom')
 replace(bottom,'<div class="flick-card__bottom"><span class="eyebrow">Technical illustration · Prototype design</span></div>')
# Replace unused reel/player with an honest, controllable state model.
for el in s.select('.fixed-reel'):el.decompose()
for el in s.select('[data-reel-row]'):
 el['data-gg-dialog']='gg-walkthrough';el['role']='button';el['tabindex']='0';el['aria-label']='Open interactive system walkthrough'
for text in s.find_all(string=True):
 if text.strip()=='See the flow in motion!':text.replace_with('Try the shopping flow')
 if text.strip()=='Demo':text.replace_with('Interactive model')
# Source-backed context and plain-language limitations.
evidence=s.select_one('#evidence')
evidence.append(fragment('''<div class="container is--m gg-evidence-notes" id="programme-sources"><p class="gg-kicker">Recognition &amp; development</p><h3>Programme support is a starting point.</h3><p>Green Groove was selected under NCERT PRAYAAS and awarded a ₹50,000 development grant. IIT Delhi is the associated HEI; Prof. Satish Kumar Dubey of SeNSE mentors the project through the programme. This supports development. It does not certify commercial performance.</p><div class="gg-reference-links"><a href="https://theglobaltimes.in/archives/december-15-2025.pdf" target="_blank" rel="noopener noreferrer">Published school coverage ↗</a><a href="https://www.ncert.nic.in/desm/prayaas.php?ln=en" target="_blank" rel="noopener noreferrer">About NCERT PRAYAAS ↗</a><a href="https://sense.iitd.ac.in/faculty-profile/7" target="_blank" rel="noopener noreferrer">Mentor’s institutional profile ↗</a></div><p class="gg-caption">The diagrams on this page explain the proposed mechanism. Illustrative transactions are not measured pilot results or screenshots of a deployed retail app.</p></div>'''))
research=s.select_one('#research')
research.append(fragment('''<div class="container is--m gg-questions" id="questions"><p class="gg-kicker">Before a store pilot</p><h3>What still needs to be tested?</h3><details><summary>Is Green Groove ready to run a supermarket?</summary><p>It is a student-built prototype. Store-scale reliability, concurrent shoppers, sensor drift, ambiguous events and operational recovery need documented testing before a commercial rollout.</p></details><details><summary>How are returns and uncertain events handled?</summary><p>The system model keeps accepted pickups and inverse returns in an event history. An uncertain association stays on hold until resolved, rather than silently changing a shopper’s bill.</p></details><details><summary>Are the graphics real product photographs?</summary><p>The site currently uses technical illustrations. They explain the design and event logic; they are not photographs of installed hardware, app screenshots or evidence of field performance.</p></details><details><summary>What does the interactive walkthrough show?</summary><p>A browser-only model using example products and prices. It demonstrates pickups, returns, a held event and invoice confirmation. It does not connect to sensors, identify a person or collect payment.</p></details><details><summary>What is the next milestone?</summary><p>Controlled tests with documented conditions, event-level logs, error analysis and recovery checks, followed by field evaluation. Results will be reported with their test conditions.</p></details></div>'''))
# Details and walkthrough dialogs use native focus management and Escape behaviour.
s.body.append(fragment('''<dialog id="layer-detail" class="gg-dialog gg-layer-dialog" aria-labelledby="gg-layer-title"><button class="gg-dialog-close" data-gg-close aria-label="Close system detail">Close ×</button><p class="gg-kicker">System design · Technical illustration</p><h2 id="gg-layer-title"></h2><p id="gg-layer-description"></p><img id="gg-layer-image" alt=""/><a id="gg-layer-full" class="gg-text-link" target="_blank" rel="noopener noreferrer">Open full-size diagram ↗</a></dialog><dialog id="gg-walkthrough" class="gg-dialog gg-demo" aria-labelledby="gg-demo-title"><button class="gg-dialog-close" data-gg-close aria-label="Close walkthrough">Close ×</button><p class="gg-kicker">Interactive model · Example data</p><h2 id="gg-demo-title">One trip. A visible history.</h2><p>Pick an item, put it back, or hold an ambiguous event. Only accepted events reach the cart.</p><div class="gg-demo-grid"><div><h3>Shelf actions</h3><div class="gg-demo-actions"><button data-gg-event="pick-milk">Pick milk · ₹60</button><button data-gg-event="pick-yogurt">Pick yogurt · ₹25</button><button data-gg-event="return-milk">Return milk</button><button data-gg-event="ambiguous">Ambiguous pickup</button><button data-gg-event="resolve">Resolve held pickup</button></div></div><div class="gg-cart"><p class="gg-kicker">Example cart · Session 01</p><div id="gg-cart-lines"></div><p class="gg-total">Subtotal <strong id="gg-cart-total">₹0</strong></p><button class="gg-solid-link" data-gg-event="settle">Confirm invoice</button></div></div><p id="gg-demo-status" role="status" aria-live="polite">Ready. Your example cart is empty.</p><div class="gg-ledger"><h3>Event history</h3><ol id="gg-demo-ledger"><li>No events yet.</li></ol></div><button class="gg-text-link" data-gg-event="reset">Reset walkthrough</button><p class="gg-caption">A browser-only explanation of the system design. No live sensors, personal identity or payment processing.</p></dialog>'''))
# Valid metadata: allow zoom, no duplicate icons or viewports.
for el in s.select('meta[name=viewport]')[1:]:el.decompose()
for el in s.select('link[rel=icon],link[rel="shortcut icon"],link[rel="apple-touch-icon"]'):el.decompose()
s.head.append(fragment('<link rel="icon" href="favicon.svg" type="image/svg+xml"><meta name="gg-public-release" content="2026-10-23"><meta name="theme-color" content="#201d1d"><meta property="og:url" content="https://sushxnthd.github.io/greengroove/"><meta property="og:image:alt" content="Green Groove retail state system"><link rel="stylesheet" href="public-launch.css">'))
s.head.append(fragment('<link rel="preload" href="assets/vendor/resource-1.woff2" as="font" type="font/woff2" crossorigin>'))
for i in [2,3,4,5,7,8]:s.body.append(fragment(f'<script defer src="assets/vendor/script-{i}.js"></script>'))
s.body.append(fragment('<script defer src="assets/vendor/animation-runtime.js"></script><script defer src="public-launch.js"></script>'))
css=s.select_one('link[href="public-launch.css"]');css.extract();s.select('link[rel=stylesheet]')[-1].insert_after(css)
# IDs must be unique even inside decorative SVGs.
seen=set()
for el in s.select('[id]'):
 key=el['id']
 if key in seen:
  new=key+'-'+str(len(seen));scope=el.find_parent('svg')
  if scope:
   for ref in scope.find_all():
    for a,v in list(ref.attrs.items()):
     if isinstance(v,str):ref[a]=v.replace('url(#'+key+')','url(#'+new+')')
  el['id']=new
 seen.add(el['id'])
# Only essential static assets remain. Remove decorative images with empty sources above.
p.write_text(str(s))
Path('assets/visuals/layer-copy.json').write_text(json.dumps(layers,ensure_ascii=False,indent=2))
print('Applied public launch layer:',p.stat().st_size,'bytes')
