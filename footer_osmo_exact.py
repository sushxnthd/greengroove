from bs4 import BeautifulSoup
from pathlib import Path
import base64, gzip, hashlib, sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")

# Exact user-supplied "Group 2.svg" (4485x446), with softened corners.
SOURCE_GZ_B64 = "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"
source_bytes = gzip.decompress(base64.b64decode(SOURCE_GZ_B64))
assert hashlib.sha256(source_bytes).hexdigest() == "2860e8a2df0394914a20ce3b881faaf6a9771348bfbff5284d48e0f8e36c2770"
source = BeautifulSoup(source_bytes.decode("utf8"), "xml")
source_paths = source.find_all("path")
if len(source_paths) != 11:
    raise RuntimeError(f"Expected 11 Green Groove letter paths; found {len(source_paths)}")

# The source path order is not typographic order. Reorder left-to-right to GREEN GROOVE.
LETTER_ORDER = (0, 1, 2, 9, 3, 4, 5, 6, 8, 7, 10)
letters = [source_paths[i] for i in LETTER_ORDER]
GROUPS = ((0,), (1, 2), (3, 4), (5,), (6, 7), (8, 9), (10,))

updated = 0
for wrap in soup.select("[data-footer-logo-wrap]"):
    svg = soup.new_tag("svg")
    svg["viewBox"] = "0 0 4485 446"
    svg["preserveAspectRatio"] = "xMidYMid meet"
    svg["class"] = ["footer-bottom__logo-svg", "gg-footer-wordmark"]
    svg["style"] = "display:block;width:106%;height:auto;max-width:none;overflow:visible;transform:translateX(-3%);"
    svg["role"] = "img"
    svg["aria-label"] = "Green Groove"

    for group in GROUPS:
        p = soup.new_tag("path")
        p["d"] = " ".join(letters[i].get("d", "") for i in group)
        p["fill"] = letters[group[0]].get("fill", "#201D1D")
        svg.append(p)

    wrap.clear()
    wrap.append(svg)
    updated += 1

if not updated:
    raise RuntimeError("No [data-footer-logo-wrap] footer mark found")

path.write_text(str(soup), encoding="utf8")
print(f"Installed softened Group 2.svg as {updated} seven-path Osmo-animated footer mark(s), rendered at 106% width")
