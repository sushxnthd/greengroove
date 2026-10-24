"""Guard the restored page against accidental redesign or broken local dependencies."""
from pathlib import Path
from bs4 import BeautifulSoup
import subprocess,json,re
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parents[1]
s=BeautifulSoup((root/'index.html').read_text(),'html.parser')
b=BeautifulSoup(subprocess.check_output(['git','show','41859c3:index.html'],cwd=root),'html.parser')
assert s.select_one('meta[name=gg-source-restored]')['content']=='41859c3'
assert not s.select('#gg-pricing-copy-refine,#gg-text-clipping-fix,#gg-text-clipping-guard'), 'Legacy editorial overrides returned'
assert not s.select('link[href*=visual-polish],link[href*=curated-integration]'), 'Legacy global style layers returned'
assert 'linear-gradient' not in s.select_one('#green-groove-tailor').text, 'Unsupported button gradient returned'
sections=lambda soup:[(x.name,x.get('class')) for x in soup.main.children if x.name and (x.name in ('section','footer') or x.get('class')==['under-nav-bar'])]
assert sections(s)==sections(b),'Original section sequence changed'
headings=lambda soup:[e.get_text(' ',strip=True) for e in soup.select('main section h1,main section h2,main section h3,main section h4') if not e.find_parent(attrs={'data-modal-target':True})]
assert headings(s)==['Built to Flow' if h=='Without the Queue' else h for h in headings(b)],'Original page headings changed'
for p in ['visual-polish.css','assets/visuals/curated-integration.css']:
 assert (root/p).read_bytes()==subprocess.check_output(['git','show','41859c3:'+p],cwd=root),p+' changed'
assert not re.search(r'(?:font(?:-size|-family)?|letter-spacing)\s*:',((root/'source-repair.css').read_text()+(root/'native-fidelity.css').read_text())),'Repair layer changes typography'
for item in json.loads((root/'docs/visual-qa/native-art-provenance.json').read_text()):
 assert s.select_one(item['selector'])['src']==item['path'], 'Native decorative asset replaced'
for layer in s.select('.about-card__img-layer'):
 assert [im['src'] for im in layer.select('img')]==['assets/people/sushanth.webp','assets/people/aryan.webp']
assert not s.select('img[src*=g04]'), 'Additional signal rings returned'
assert not s.select('img[src*=g02]'), 'Placeholder logo remains in a portrait slot'
assert len(s.select('.testimonial-item__info-img img[src*="assets/people/"]'))==6
assert len(s.select('.join-faces__image-el'))==3
assert len(s.select('.about-item__img img[src*="assets/people/"]'))==2
assert 'amity-readable.svg' in str(s.select('.trustedby-marquee__item-svg'))
ids=[e['id'] for e in s.select('[id]')];assert len(ids)==len(set(ids)),'Duplicate IDs'
refs=[]
for e in s.select('[src],link[href],a[href],image[href]'):
 u=e.get('src') or e.get('href')
 if not u:continue
 parts=urlsplit(u)
 if u.startswith('#'):assert not parts.fragment or parts.fragment in ids,u
 elif not parts.scheme and not u.startswith('//'):
  p=root/unquote(parts.path);assert p.is_file(),str(p);refs.append(parts.path)
for e in s.select('script[src],link[rel=stylesheet]'):assert not urlsplit(e.get('src') or e.get('href')).scheme,'Remote runtime'
assert not s.select('video,[data-mapping],[data-form-validate],[data-o-auth]')
assert not s.select('script[src*=public-launch],link[href*=public-launch]')
assert len(s.select('.product-card'))==6
assert len(s.select('[data-flick-cards-item]'))==7
assert len(s.select('#findings [data-vertical-slider-item]'))==6
for e in s.select('footer form input:not([type=submit]):not([type=checkbox])'):assert e.has_attr('readonly') and not e.has_attr('name')
report={'content_baseline':'41859c3','design_reference':'https://www.osmo.supply/','visual_fidelity_complete':False,'original_sections':True,'original_headings':True,'legacy_editorial_overrides_removed':True,'local_references':len(set(refs)),'product_cards':6,'build_cards':7,'findings':6}
out=root/'docs/visual-qa/restored-static-audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
