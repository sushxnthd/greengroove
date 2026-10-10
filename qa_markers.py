from pathlib import Path
import sys
from bs4 import BeautifulSoup

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

# Stable, nonvisual identifiers let the browser QA exercise each exact control/card
# without relying on DOM indexes that can shift when source animations initialize.
controls = soup.select('button, input[type="submit"], [role="button"]')
for i, el in enumerate(controls):
    el["data-gg-qa-control"] = f"control-{i:03d}"

links = soup.select('a[href]')
for i, el in enumerate(links):
    el["data-gg-qa-link"] = f"link-{i:03d}"

path.write_text(str(soup), encoding="utf-8")
print(f"QA markers installed: {len(controls)} controls, {len(links)} links.")
