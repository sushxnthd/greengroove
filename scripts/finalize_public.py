from pathlib import Path
from bs4 import BeautifulSoup
p=Path('index.html');s=BeautifulSoup(p.read_text(),'html.parser')
def f(html):return BeautifulSoup(html,'html.parser')
hero_copy=s.select_one('.home-hero__description-p')
if hero_copy:
 hero_copy.clear();hero_copy.append('RFID wristbands and sensor-equipped shelves connect each pick and return to a live cart.')
# Miniature symbols carry one idea; full technical diagrams remain in detail views.
thumbs=['identity','shelf','return','cart','association','settlement','ledger','validation','interaction']
labels=['RFID session identity','Shelf event capture','Reversible returns','Accepted cart state','Shopper association','Invoice summary','Visible event history','Planned validation','Product movement']
for i,e in enumerate(s.select('.radial-marquee__card')):
 image=e.select_one('img');key=thumbs[i%9]
 if image:image['src']=f'assets/visuals/thumbnails/{key}.svg';image['width']='600';image['height']='400';image['alt']=labels[i%9]+' — technical symbol';image['loading']='eager' if i<5 else 'lazy'
 if e.select_one('.radial-marquee__card-p'):e.select_one('.radial-marquee__card-p').string=labels[i%9]
# No empty badges or inactive-looking routes.
for e in s.select('.nav-bar__a-tag,.footer-link__col-li-tag,.nav-bar__big-span-number'):e.decompose()
for e in s.select('[data-disabled]'):e.attrs.pop('data-disabled',None)
for e in s.select('.nav-bar__small-a.is--inactive'):
 e.name='a';e['href']='#layer-reversibility';e['class']=['nav-bar__small-a','w-inline-block'];e.parent['class']=['nav-bar__small-li']
for e in s.select('.footer-link__col-li.is--soon'):
 e['class']=['footer-link__col-li'];text=e.select_one('p');
 if text:text.name='a';text['href']='#layer-reversibility'
for e in s.select('footer a[href="#build"]'):
 name=e.get_text(' ',strip=True)
 if name in ['Groove Band','Green Grooves']:e['href']='#'+('groove-band' if name=='Groove Band' else 'green-grooves')
for e in s.select('a[href^="#layer-"]'):
 if e['href']!='#layer-detail':
  key=e['href'][7:]
  if key in ['identity','shelf-events','association','reversibility','live-cart','settlement']:e['data-gg-layer']=str(['identity','shelf-events','association','reversibility','live-cart','settlement'].index(key))
# Attribute-bearing wrappers should not create extra, unlabeled click targets.
for e in s.select('[data-gg-dialog="gg-about"]'):
 if e.name!='button':e.attrs.pop('data-gg-dialog',None)
for e in s.select('[data-gg-qa-control="control-001"],footer button'):
 if 'About' in e.get_text():e['data-gg-dialog']='gg-about'
# Menu groups have distinct names; creator names open the actual creator panel.
heads=s.select('footer .footer-link__col-top h4')
for e,name in zip(heads,['System layers','Project','Explore']):e.string=name
for e in s.select('footer a'):
 name=e.get_text(' ',strip=True)
 if name in ['Sushanth Sushanth','Aryan Aryan']:
  e['href']='#gg-about';e['data-gg-dialog']='gg-about';e.attrs.pop('target',None);e['aria-label']='About '+name.split()[0]
# Make the gallery equally usable with pointer and keyboard controls.
gallery=s.select_one('[data-flick-cards-init]')
if gallery and not s.select_one('.gg-gallery-controls'):
 gallery.insert_after(f('<div class="gg-gallery-controls" aria-label="Build gallery controls"><button type="button" data-gg-gallery="prev" aria-label="Previous build component">← Previous</button><span id="gg-gallery-position" role="status" aria-live="polite">1 / 7</span><button type="button" data-gg-gallery="next" aria-label="Next build component">Next →</button></div>'))
# State the visual medium once next to the rotating studies.
hero=s.select_one('.home-hero__description-row')
if hero and not s.select_one('.gg-motion-link'):
 hero.insert_after(f('<div class="gg-hero-meta"><span>Student-built retail prototype · Technical illustrations</span><a class="gg-motion-link" href="?motion=reduce#home">Pause motion</a></div>'))
if not s.select_one('#gg-motion-preference'):
 s.head.append(f('<script id="gg-motion-preference">document.documentElement.dataset.ggMotion=(new URLSearchParams(location.search).get("motion")==="reduce"||matchMedia("(prefers-reduced-motion: reduce)").matches)?"reduce":"full";</script>'))
for e in s.select('[data-vertical-slider]'):e['data-autoplay']='false'
for e in s.select('.pricing-card__price-w'):
 a=e.find_all('p');
 if len(a)>1:a[1]['aria-hidden']='true'
# Alt descriptions explain the picture, not internal asset-production bookkeeping.
for e in s.select('img[alt]'):
 alt=e['alt']
 if 'used until authentic' in alt:
  e['alt']=alt.split(' used until')[0]+' — technical illustration'
for e in s.select('svg:not([aria-label])'):
 e['aria-hidden']='true';e['focusable']='false'
for e in s.select('a.cover-link:not([aria-label])'):e['aria-label']='Explore Green Groove source'
# Native dialogs must have usable, visible close buttons under the inherited global reset.
for e in s.select('dialog button'):e['type']='button'
# A single link name rather than eight repetitions from a decorative marquee.
for e in s.select('a[href="#programme-sources"]'):
 if len(e.select('p'))>2:e['aria-label']='NCERT PRAYAAS selection and supporting sources';[x.__setitem__('aria-hidden','true') for x in e.select('p')]
p.write_text(str(s))
print('Finalized public content, thumbnails, routes and keyboard gallery')
