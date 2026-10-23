"""Finish the public sections without regenerating the source layout."""
from pathlib import Path
from bs4 import BeautifulSoup
p=Path('index.html');s=BeautifulSoup(p.read_text(),'html.parser')
def fragment(markup):return BeautifulSoup(markup,'html.parser')
s.select_one('#gg-motion-preference').string='(()=>{const mode=new URLSearchParams(location.search).get("motion");document.documentElement.dataset.ggMotion=(mode==="reduce"||(mode!=="full"&&matchMedia("(prefers-reduced-motion: reduce)").matches))?"reduce":"full"})()'
# Unrelated company marks must not imply customers or partnerships.
for e in s.select('.trustedby-wrap'):e.decompose()
# Both authors remain visible, including when motion is paused.
name=s.select_one('.about-card__name')
if name:
 name.clear();name.append(fragment('<h3 class="gg-creators" id="overview"><span>Sushanth Dasari</span><span>Aryan Kumar</span></h3>'))
# Compact cards use a single symbol, with the full diagrams in the detail dialog.
keys=['identity','shelf','association','return','cart','settlement']
names=['Identity','Shelf Events','Association','Reversibility','Live Cart','Settlement']
for i,card in enumerate(s.select('.product-card[data-gg-layer]')):
 for e in card.select('.product-card__bg,.product-card__ptc-preview,.gg-discover'):e.decompose()
 card['class']=[x for x in card.get('class',[]) if x!='is--disabled']
 card['aria-label']='Explore '+names[i]+' layer'
 tags=card.select_one('.product-card__tags');tags.clear();tags.append(fragment(f'<span class="gg-layer-index">0{i+1} / 06 · System layer</span>'))
 icon=card.select_one('.product-card__icon');icon.clear()
 icon.append(fragment(f'<img class="gg-layer-symbol" src="assets/visuals/thumbnails/{keys[i]}.svg" width="600" height="400" alt="" aria-hidden="true" loading="lazy" decoding="async">'))
 btn=card.select_one('.product-card__btn');btn.clear();btn.append(fragment('<span class="gg-card-discover">Open layer detail ↗</span>'))
for i,b in enumerate(s.select('[data-gsap-slider-control]')):
 b['aria-label']='Show '+names[i]+' layer';b['aria-pressed']='true' if i==0 else 'false'
# Actual controls replace invisible half-card click zones.
for root,kind in [(s.select_one('.latest-resources-slider'),'project note'),(s.select_one('#findings'),'finding')]:
 if not root:continue
 for direction,label in [('prev','Previous'),('next','Next')]:
  b=root.select_one(f'[data-{direction}]')
  if b:b.clear();b.string=('← Previous' if direction=='prev' else 'Next →');b['aria-label']=label+' '+kind
 for i,b in enumerate(root.select('[data-vertical-slider-bullet]')):
  b.name='button';b['type']='button';b['aria-label']=f'Show {kind} {i+1}'
# The circular visual uses a simple symbol, while diagrams have a readable link.
map_keys={'VNM':'association','UK':'return','AUS':'shelf','NL':'identity','SWE':'ledger','CA':'settlement'}
for im in s.select('[data-testimonial-map]'):
 im['src']='assets/visuals/thumbnails/'+map_keys[im['data-testimonial-map']]+'.svg';im['alt']='';im['aria-hidden']='true';im.attrs.pop('data-gg-fit',None)
for item in s.select('#findings [data-vertical-slider-item]'):
 key=item['data-slide-map'];files={'VNM':'c01-detection-vs-association.svg','UK':'c02-reversible-actions.svg','AUS':'c03-sensor-cross-check.svg','NL':'c04-identity-before-automation.svg','SWE':'c05-visible-uncertainty.svg','CA':'c06-settlement-vs-reconstruction.svg'}
 if not item.select_one('.gg-finding-link'):item.select_one('.testimonial-item').append(fragment(f'<a class="gg-text-link gg-finding-link" href="assets/visuals/{files[key]}" target="_blank" rel="noopener noreferrer">Open explanation diagram ↗</a>'))
# Notes keep their subject legible at card size and open the full design.
for item,layer,key in zip(s.select('.latest-resources-slider [data-vertical-slider-item]'),[0,1,4,3,2],['identity','shelf','cart','return','association']):
 card=item.select_one('.resource-card');title=card.select_one('h4').get_text(strip=True)
 card.name='a';card['href']='#layer-detail';card['data-gg-layer']=str(layer);card['data-gg-layer-title']=title;card['aria-label']='Open project note: '+title
 im=card.select_one('img');im['src']='assets/visuals/thumbnails/'+key+'.svg';im['alt']='';im['aria-hidden']='true';im.attrs.pop('data-gg-fit',None)
# Correct the shelf-sensing gallery visual.
item=s.select_one('[data-gg-build-title="Shelf Sensing"] img')
if item:item['src']='assets/visuals/a02-shelf-events-layer.svg';item['alt']='Shelf sensing: load-cell change and RFID observations form a candidate event'
# A semantic project sequence replaces the unfinished timeline and theme switches.
end=s.select_one('.try-vault__end')
if end:
 end.clear();end.append(fragment('''<div class="gg-project-sequence"><p class="gg-kicker">From observation to prototype</p><ol>
<li><span class="gg-sequence-number">01</span><div><h3>Observe the queue</h3><p>Ask why the basket is reconstructed only at checkout.</p></div></li>
<li><span class="gg-sequence-number">02</span><div><h3>Design the state model</h3><p>Connect identity, shelf events, association, returns, the cart and settlement.</p></div></li>
<li><span class="gg-sequence-number">03</span><div><h3>Build the prototype</h3><p>Bring the Groove Band, sensor shelves and G/G App into one retail flow.</p></div></li>
<li><span class="gg-sequence-number">04</span><div><h3>Test and refine</h3><p>Next: document sensor calibration, ambiguous events and recovery under controlled conditions.</p><span class="gg-sequence-status">Next milestone</span></div></li>
</ol><a class="gg-text-link" href="#programme-sources">Programme support and sources ↗</a></div>'''))
# Template social glyphs must not misrepresent their actual destinations.
for a in s.select('a.square-button'):
 label=a.get('aria-label','')
 if label=='Green Groove website':a.decompose();continue
 a.clear();a['class']=['gg-footer-source'];a.string='Case study ↗' if label=='Behance project' else 'GitHub ↗'
for logo in s.select('.gg-footer-wordmark'):logo['style']='display:block;width:100%;height:auto;max-width:100%;'
for a in s.select('a[href="#system"]'):
 if a.get_text(' ',strip=True).startswith('System overview'):
  a['href']='assets/visuals/a07-full-six-layer-architecture.svg';a['target']='_blank';a['rel']=['noopener','noreferrer'];a['aria-label']='Open full system map'
  for t in a.select('.button-label span'):t.string='Open full system map'
p.write_text(str(s))
print('Refined lower sections, layer cards, authors and controls')
