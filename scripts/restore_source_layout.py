"""Restore 41859c3's page structure. Alter only assets, routes and interaction semantics."""
from pathlib import Path
from bs4 import BeautifulSoup
from copy import copy
import subprocess
BASE='41859c3'
s=BeautifulSoup(subprocess.check_output(['git','show',BASE+':index.html']).decode(),'html.parser')
def f(t):return BeautifulSoup(t,'html.parser')
# Keep the exact source style order, using the same local CSS/font bytes.
css=['assets/vendor/style-0.css','./visual-polish.css','./assets/visuals/curated-integration.css','assets/vendor/style-1.css','assets/vendor/style-2.css','assets/vendor/style-3.css','assets/vendor/style-4.css']
for e,src in zip(s.select('link[rel=stylesheet]'),css):
 e['href']=src;e.attrs.pop('integrity',None)
for e in s.select('script[src]'):e.decompose()
for e in s.select('#gg-outseta-compat,#gg-production-behavior'):e.decompose()
for e in s.select('script'):
 if 'window.plausible' in e.get_text():e.decompose()
for e in s.select('.sitemap,.fixed-reel'):e.decompose()
for e in s.select('video'):e.decompose()
for e in s.select('[data-bunny-thumbnail-init],[data-player-src],[data-player-id]'):
 for k in list(e.attrs):
  if k.startswith('data-player') or k.startswith('data-bunny'):e.attrs.pop(k,None)
for e in s.select('[data-mapping],[data-form-validate]'):
 e.attrs.pop('data-mapping',None);e.attrs.pop('data-form-validate',None)
# Source-sized visual replacements, never changes to the card geometry or text.
thumbs=['identity','shelf','return','cart','association','settlement','ledger','validation','interaction']
for i,e in enumerate(s.select('.radial-marquee__card img.resource-card__img')):
 e['src']=f'assets/visuals/thumbnails/{thumbs[i%9]}.svg';e['alt']=thumbs[i%9].replace('-',' ')+' — technical symbol'
keys=['identity','shelf','association','return','cart','settlement']
for i,e in enumerate(s.select('.product-card')):
 for im in e.select('img'):
  im['src']='assets/visuals/thumbnails/shelf.svg' if i==1 else f'assets/visuals/source-fit/{keys[i]}-card.svg'
  im['alt']='';im['aria-hidden']='true';im.attrs.pop('data-gg-fit',None);im.attrs.pop('data-gg-asset',None)
 e['data-gg-detail']=str(i);e['aria-label']='Explore '+['Identity','Shelf Events','Association','Reversibility','Live Cart','Settlement'][i]
 if e.name=='a':e['href']='#system-detail'
 else:e['role']='button';e['tabindex']='0'
 for b in e.select('button'):b.name='span';b.attrs.pop('data-gg-qa-control',None)
# Notes retain their source card structure and open the corresponding full diagram.
for card,layer,key in zip(s.select('.latest-resources-slider .resource-card'),[0,1,4,3,2],['identity','shelf','cart','return','association']):
 card['data-gg-detail']=str(layer);card['role']='button';card['tabindex']='0';card['aria-label']='Open project note: '+card.select_one('h4').get_text(strip=True)
 im=card.select_one('img');im['src']='assets/visuals/thumbnails/'+key+'.svg';im['alt']='';im['aria-hidden']='true';im.attrs.pop('data-gg-fit',None)
# Fix the original maps by supplying art matched to the original zoom coordinates.
for im in s.select('[data-testimonial-map]'):
 im['src']='assets/visuals/source-fit/finding-'+im['data-testimonial-map'].lower()+'.svg'
 im['alt']='';im['aria-hidden']='true';im.attrs.pop('data-gg-fit',None);im.attrs.pop('data-gg-asset',None)
for im in s.select('.about-card__img'):
 im.attrs.pop('data-gg-asset',None)
# An unfinished timeline is replaced inside the same image slot.
for im in s.select('img[src="assets/visuals/b04-development-timeline.svg"]'):
 im['src']='assets/visuals/e04-validation-roadmap.svg';im['alt']='Planned technical and field validation'
for im in s.select('.try-vault__visual img'):
 im.attrs.pop('data-gg-asset',None);im.attrs.pop('data-gg-fit',None)
# Preserve the logo row's boxes, replace unrelated company artwork with system symbols.
for i,svg in enumerate(s.select('.trustedby-marquee__item-svg')):
 vb=svg.get('viewbox','0 0 172 42').split();w,h=vb[-2:];svg.clear()
 im=s.new_tag('image',href=f'assets/visuals/thumbnails/{thumbs[i%9]}.svg',x='0',y='0',width=w,height=h,preserveAspectRatio='xMidYMid meet');svg.append(im)
# Existing symbols and native art remain.
for im in s.select('[data-gg-hidden="template-person"]'):im.attrs.pop('data-gg-hidden',None)
# The supplied source already has the About and Showcase modals: reuse those.
modal=s.select_one('[data-modal-target=showcase]');modal['id']='system-detail';modal['role']='dialog';modal['aria-modal']='true';modal['aria-label']='System detail'
modal.select_one('[data-res-used=title]')['id']='gg-native-detail-title'
modal.select_one('[data-res-used=item-title]').string='Technical illustration'
for t in modal.select('[data-res-used=item-catgory] .eyebrow'):t.string='System model'
for im in modal.select('.profile-picture__image'):im['src']='assets/visuals/g02-canonical-g-favicon.svg';im['alt']=''
for b in modal.select('button.tag'):b.name='div'
for a in modal.select('.credit-link'):
 a['href']='#project';a.attrs.pop('target',None)
for a in modal.select('[data-res-used=item-link],[data-res-used=site-url]'):
 a['href']='assets/visuals/a07-full-six-layer-architecture.svg';a['target']='_blank';a['rel']=['noopener','noreferrer'];a['aria-label']='Open full-size system diagram'
 for b in a.select('button'):b.name='span'
about=s.select_one('[data-modal-target=about]');about['role']='dialog';about['aria-modal']='true';about['aria-label']='About Green Groove'
# The original circular map slot needs decorative artwork, not a cropped technical diagram.
for im in about.select('.about-map__inner'):
 im['src']='assets/visuals/g04-signal-motifs.svg';im['alt']='';im['aria-hidden']='true';im.attrs.pop('data-gg-asset',None);im.attrs.pop('data-gg-fit',None)
# Fix foreign profile destinations and glyphs in their original button boxes.
repo='https://github.com/sushxnthd/greengroove';case='https://www.behance.net/gallery/211169339/Green-Groove'
paths={'source':'<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-12-2 14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>','case':'<path d="M14 4h6v6m0-6L10 14M10 5H5v14h14v-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'}
for i,a in enumerate(s.select('a.square-button')):
 href=a.get('href','');mode='source' if 'github' in href or i%2 else 'case';a['href']=repo if mode=='source' else case;a['aria-label']='Project source' if mode=='source' else 'Green Groove case study';a['rel']=['noopener','noreferrer'];a['target']='_blank'
 for svg in a.select('svg'):svg.clear();svg.append(f(paths[mode]));svg['viewBox']='0 0 24 24'
# Canonical wordmark geometry inside the existing About SVG boxes.
canonical=s.select_one('.gg-footer-wordmark') or s.select_one('footer .footer-bottom__logo svg')
if canonical:
 for svg in about.select('.about-hero__logo svg,[data-footer-logo] svg'):
  vb=svg.get('viewbox','0 0 1768 297').split();w,h=map(float,vb[-2:]);scale=w/4485;y=(h-446*scale)/2;svg.clear();g=s.new_tag('g',transform=f'translate(0 {y}) scale({scale})')
  for path in canonical.select('path'):p=copy(path);p['fill']='currentColor';g.append(p)
  svg.append(g)
# Repair existing controls and route targets without adding new page sections.
nav=s.select_one('[data-nav-toggle=toggle]');nav['role']='button';nav['tabindex']='0';nav['aria-label']='Open menu';nav['aria-expanded']='false'
reel=s.select_one('[data-reel-row]');reel['role']='button';reel['tabindex']='0';reel['aria-label']='Open system architecture';reel['data-gg-map']='true'
for t in reel.select('.scribble'):t.string='See the system map'
for i,card in enumerate(s.select('[data-flick-cards-item]')):
 hit=card.select_one('.flick-card__click');title=card.select_one('h3').get_text(strip=True);hit['role']='button';hit['tabindex']='0';hit['aria-label']='Explore '+title;hit['data-gg-build']=str(i);card['data-gg-build-title']=title
for a in s.select('.flick-card__bottom a'):
 a['href']='#project';a['data-modal-trigger']='about';a.attrs.pop('target',None)
for root,kind in [(s.select_one('.latest-resources-slider'),'project note'),(s.select_one('#findings'),'finding')]:
 if root:
  for dr,name in [('prev','Previous'),('next','Next')]:
   b=root.select_one('[data-'+dr+']')
   if b:b['aria-label']=name+' '+kind
  for i,b in enumerate(root.select('[data-vertical-slider-bullet]')):b['role']='button';b['tabindex']='0';b['aria-label']=f'Show {kind} {i+1}'
for i,b in enumerate(s.select('[data-gsap-slider-control]')):b['aria-label']='Show '+['Identity','Shelf Events','Association','Reversibility','Live Cart','Settlement'][i]+' layer'
for i,b in enumerate(s.select('[data-marketing-theme-toggle]')):b['aria-label']='Use dark preview' if i==0 else 'Use light preview';b['data-gg-theme']='dark' if i==0 else 'light'
for a in s.select('a.nav-logo'):a['href']='#home'
# Assign real layer destinations to existing menu/footer links.
layer_ids=['identity','shelf-events','association','reversibility','live-cart','settlement']
for a in s.select('a[href]'):
 if a['href'].startswith('#layer-') and a['href'][7:] in layer_ids:a['data-gg-detail']=str(layer_ids.index(a['href'][7:]))
 label=a.get_text(' ',strip=True)
 if label=='Validation' or label.startswith('Roadmap'):a['data-gg-roadmap']='true'
 if label.startswith('System overview'):a['data-gg-map']='true'
 if label.startswith('Explore build'):a['data-gg-active-build']='true'
 if a.get_text(' ',strip=True) in ['About Sushanth','About Aryan']:a['data-modal-trigger']='about'
 for b in a.select('button'):b.name='span'
for b in s.select('[data-modal-close]'):b['aria-label']='Close '+b.get('data-modal-close','modal')
# Keep existing footer items, repair their routes in place.
for col in s.select('footer .footer-link__col'):
 for a in col.select('a'):
  name=a.get_text(' ',strip=True)
  if name=='Questions':a['href']='https://github.com/sushxnthd/greengroove/issues'
  if name=='Groove Band':a['href']='#groove-band'
  if name=='Green Grooves':a['href']='#green-grooves'
for item in s.select('footer .footer-link__col-li.is--soon'):
 p=item.select_one('p')
 if p:p.name='a';p['href']='#layer-reversibility';p['data-gg-detail']='3'
for a in s.select('#evidence a'):
 name=a.get_text(' ',strip=True)
 if name.startswith('See recognition'):name='See recognition'
 if name.startswith('See the build'):name='See the build'
 if name.startswith('See the validation'):name='See the validation'
 if name in ['See recognition','Programme evidence']:a['href']='https://theglobaltimes.in/archives/december-15-2025.pdf';a['target']='_blank';a['rel']=['noopener','noreferrer']
 if name in ['See the build','View build']:a['href']='#build'
 if name=='See the validation':a['data-gg-roadmap']='true'
for a in s.select('footer .footer-bottom__by a'):
 a['href']='#project';a['data-modal-trigger']='about';a.attrs.pop('target',None)
for a in s.select('a.credit-link'):
 a['data-modal-trigger']='about'
for el in s.select('.nav-bar__small-a.is--inactive'):
 el.name='a';el['href']='#layer-reversibility';el['data-gg-detail']='3';el.attrs.pop('aria-disabled',None)
# The legacy viewport guard must not permanently shrink normal-flow text after a modal transform.
guard=s.select_one('#gg-text-clipping-guard')
if guard:guard.string=guard.get_text().replace("document.querySelectorAll('.gg-viewport-copy').forEach(function (el) {","document.querySelectorAll('.gg-viewport-copy').forEach(function (el) {\n      if (el.closest('.info')) return;")
# Source form keeps its design, links to published work instead of collecting data.
form=s.select_one('footer form')
if form:
 form['novalidate']='novalidate'
 for inp in form.select('input:not([type=submit]):not([type=checkbox])'):
  inp.attrs.pop('name',None);inp.attrs.pop('required',None);inp['readonly']='readonly'
  if inp.get('id')=='newsletter-name':inp['placeholder']='Green Groove build notes';inp['aria-label']='Green Groove build notes'
# Do not reintroduce remote integration hooks, duplicate IDs or hidden account routes.
for e in s.select('[data-o-auth],[data-outseta]'):
 for k in list(e.attrs):
  if k.startswith('data-o-') or k.startswith('data-outseta'):e.attrs.pop(k,None)
seen=set()
for e in s.select('[id]'):
 if e['id'] in seen:e.attrs.pop('id',None)
 else:seen.add(e['id'])
for a in s.select('a[target=_blank]'):a['rel']=['noopener','noreferrer']
# Existing CSS and inline style blocks remain byte-equivalent. One asset/hit-target layer.
s.head.append(f('<link rel="stylesheet" href="source-repair.css">'))
s.head.append(f('<meta name="gg-source-restored" content="41859c3">'))
s.head.append(f('<script>document.documentElement.dataset.ggMotion=(new URLSearchParams(location.search).get("motion")==="reduce"||matchMedia("(prefers-reduced-motion: reduce)").matches)?"reduce":"full"</script>'))
for name in ['script-2.js','script-3.js','script-4.js','script-5.js','native-split-text.js','script-7.js','script-8.js','native-lenis.js','osmo-native-runtime.js']:
 s.body.append(f(f'<script src="assets/vendor/{name}" defer></script>'))
s.body.append(f('<script src="source-repair.js" defer></script>'))
# Remove earlier editorial overrides; retain only Green Groove palette tokens.
for e in s.select('link[href*=visual-polish],link[href*=curated-integration],#gg-pricing-copy-refine,#gg-text-clipping-fix,#gg-text-clipping-guard'):
 e.decompose()
s.select_one('#green-groove-tailor').string=':root{--color-electric:#78ff45;--color-purple:#18bdf2;--color-purple-copy:#18bdf2}'
s.body.append(f('<link rel="stylesheet" href="native-fidelity.css">'))
# Fit tailored copy inside the source heading without changing typography.
for heading in s.select('.home-hero h2'):
 if heading.get_text(strip=True)=='Without the Queue':heading.string='Built to Flow'
# User-supplied transparent portraits use the source's three-layer crossfade.
for layer in s.select('.about-card__img-layer'):
 for im,person in zip(layer.select('img'),['sushanth','aryan']):
  im['src']=f'assets/people/{person}.webp';im.attrs.pop('data-gg-asset',None)
# Restore each original decorative asset in its own source coordinate system.
import json
native_art=json.loads(Path('docs/visual-qa/native-art-provenance.json').read_text())
for item in native_art:
 for im in s.select(item['selector']):
  im['src']=item['path'];im.attrs.pop('data-gg-asset',None)
# Institutional marks fill the existing marquee boxes without changing its motion.
marks=[('amity-emblem.svg','Amity International School, Gurugram Sector 46'),('ncert.png','NCERT — PRAYAAS programme'),('iit-delhi-colour.png','IIT Delhi — associated HEI')]
for i,svg in enumerate(s.select('.trustedby-marquee__item-svg')):
 name,label=marks[(i%8)%3];svg.clear();svg['viewbox']='0 0 42 42';svg['role']='img';svg['aria-label']=label
 vb=svg.get('viewbox','0 0 172 42').split();w,h=vb[-2:]
 svg.append(s.new_tag('image',href='assets/institutions/'+name,x='0',y='0',width=w,height=h,preserveAspectRatio='xMidYMid meet'))
for el,label in zip(s.select('.info .eyebrow.is--relative'),['School · Programme','Associated HEI']):el.string=label
# Real founder portraits replace avatar logos in About and project credits.
people={'sushanth':'Sushanth Dasari','aryan':'Aryan Kumar'}
for item in s.select('.about-item'):
 im=item.select_one('.about-item__img img')
 if im:
  person='sushanth' if 'Sushanth' in item.get_text() else 'aryan'
  im['src']=f'assets/people/{person}.webp';im['alt']=people[person];im.attrs.pop('aria-hidden',None)
for im in s.select('.flick-card__hidden-profile-pic img'):
 person='sushanth' if 'SUSHANTH' in im.find_parent('a').get_text() else 'aryan'
 im['src']=f'assets/people/{person}.webp';im['alt']=people[person];im.attrs.pop('data-gg-asset',None)
for i,im in enumerate(s.select('[data-modal-target=showcase] .profile-picture__image')):
 person=['sushanth','aryan'][i%2];im['src']=f'assets/people/{person}.webp';im['alt']=people[person]
for placeholder in s.select('.profile-picture__placeholder-svg'):placeholder.decompose()
for i,im in enumerate(s.select('.testimonial-item__info-img img')):
 person=['sushanth','aryan'][i%2];im['src']=f'assets/people/{person}.webp';im['alt']=people[person]
# The programme reference uses actual institutional emblems in its existing avatar row.
items=s.select('.join-faces__image-el')
for item,(name,label) in zip(items,[('amity-emblem.svg','Amity International School, Sector 46'),('ncert.png','NCERT'),('iit-delhi-colour.png','IIT Delhi')]):
 im=item.select_one('img');im['src']='assets/institutions/'+name;im['alt']=label;im.attrs.pop('aria-hidden',None);im.attrs.pop('data-gg-asset',None);im['data-institution']=name.split('.')[0]
for item in items[3:]:item.decompose()
# Restore the source cover fitting only in the Built into Green Groove previews.
for im in s.select('#build .showcase-media__image'):im['data-gg-fit']='cover'
Path('index.html').write_text(str(s))
print('Restored source DOM from',BASE)
