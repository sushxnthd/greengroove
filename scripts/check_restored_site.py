"""Guard the restored page against accidental redesign or broken local dependencies."""
from pathlib import Path
from bs4 import BeautifulSoup
import subprocess,json,re
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parents[1]
s=BeautifulSoup((root/'index.html').read_text(),'html.parser')
b=BeautifulSoup(subprocess.check_output(['git','show','41859c3:index.html'],cwd=root),'html.parser')
assert s.select_one('meta[name=gg-source-restored]')['content']=='41859c3'
assert [e.text for e in s.select('style')]==[e.text for e in b.select('style')], 'Original inline layout styles changed'
sections=lambda soup:[(x.name,x.get('class')) for x in soup.main.children if x.name and (x.name in ('section','footer') or x.get('class')==['under-nav-bar'])]
assert sections(s)==sections(b),'Original section sequence changed'
headings=lambda soup:[e.get_text(' ',strip=True) for e in soup.select('main section h1,main section h2,main section h3,main section h4') if not e.find_parent(attrs={'data-modal-target':True})]
assert headings(s)==headings(b),'Original page headings changed'
for p in ['visual-polish.css','assets/visuals/curated-integration.css']:
 assert (root/p).read_bytes()==subprocess.check_output(['git','show','41859c3:'+p],cwd=root),p+' changed'
assert not re.search(r'(?:font(?:-size|-family)?|letter-spacing)\s*:',(root/'source-repair.css').read_text()),'Repair layer changes typography'
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
report={'baseline':'41859c3','original_sections':True,'original_headings':True,'original_inline_styles':True,'local_references':len(set(refs)),'product_cards':6,'build_cards':7,'findings':6}
out=root/'docs/visual-qa/restored-static-audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
