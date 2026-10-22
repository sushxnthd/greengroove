"""Static release gate. Validate the actual published document and all of its local dependencies."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
from collections import Counter
import re,json
root=Path(__file__).resolve().parents[1]
s=BeautifulSoup((root/'index.html').read_text(),'html.parser')
errors=[];assets=set()
def check_resource(value,base=root):
 if not value or value.startswith(('data:','#')):return
 parsed=urlsplit(value)
 if parsed.scheme or parsed.netloc:errors.append('External runtime resource: '+value);return
 path=(base/unquote(parsed.path)).resolve()
 if not path.is_file():errors.append('Missing resource: '+str(path.relative_to(root)))
 else:assets.add(path)
for e in s.select('[src],link[href]'):
 if e.name=='link' and e.get('rel')==['canonical']:continue
 check_resource(e.get('src') or e.get('href'))
for e in s.select('a[href^="#"]'):
 if not s.find(id=e['href'][1:]):errors.append('Missing anchor '+e['href'])
ids=Counter(e['id'] for e in s.select('[id]'))
errors += ['Duplicate ID '+key for key,n in ids.items() if n>1]
for e in s.select('a button,a a,button button'):errors.append('Nested interactive element')
for e in s.select('img'):
 if 'alt' not in e.attrs:errors.append('Image has no alt')
for e in s.select('a[target="_blank"]'):
 if 'noopener' not in e.get('rel',[]):errors.append('Unsafe new-tab link')
for e in s.select('button'):
 if not (e.get_text(strip=True) or e.get('aria-label')):errors.append('Button has no name')
if len(s.select('meta[name=viewport]'))!=1:errors.append('Duplicate/missing viewport')
if s.select_one('meta[name=viewport]') and 'maximum-scale' in s.select_one('meta[name=viewport]')['content']:errors.append('Zoom restricted')
if s.select('video,form,.sitemap,[data-player-src]'):errors.append('Unused integration remains')
if not s.select_one('meta[name=gg-public-release]'):errors.append('Public layer missing')
for meta in s.select('meta[property="og:image"],meta[name="twitter:image"]'):
 value=meta.get('content','');prefix='https://sushxnthd.github.io/greengroove/'
 if value.startswith(prefix):check_resource(value[len(prefix):])
for e in s.select('a[href]'):
 if not e.get_text(strip=True) and not e.get('aria-label') and not e.select_one('img[alt]'):errors.append('Link has no name')
html=str(s)
for word in ['codebydennis','dennissnellenberg','ilja-van-eck','iljavaneck','Outseta','slater.app','osmo.b-cdn','bunny-player','data-mapping=']:
 if word in html:errors.append('Template integration remains: '+word)
queue=list(assets)
while queue:
 p=queue.pop()
 if p.suffix=='.css':
  before=set(assets)
  for url in re.findall(r'url\(\s*[\"\x27]?([^\)\"\x27]+)',p.read_text()):check_resource(url,p.parent)
  queue.extend(assets-before)
result={'status':'pass' if not errors else 'fail','local_assets':len(assets),'html_bytes':(root/'index.html').stat().st_size,'runtime_bytes':sum(p.stat().st_size for p in assets),'errors':errors}
(root/'docs/visual-qa/public-static-audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
raise SystemExit(bool(errors))
