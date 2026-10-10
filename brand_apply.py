from bs4 import BeautifulSoup
from pathlib import Path
import base64, gzip, hashlib, sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
s = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")

WORDMARK_GZ_B64 = (
    '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'
)
wordmark_svg = gzip.decompress(base64.b64decode(WORDMARK_GZ_B64))
assert hashlib.sha256(wordmark_svg).hexdigest() == "9e7e838b1c873ad9e751ad5df463c933b019e9ddd35fd70bc18016ae9fd06b6f"
wordmark_uri = "data:image/svg+xml;base64," + base64.b64encode(wordmark_svg).decode("ascii")

def embed_svg_asset(svg, uri, view_box, width, height):
    svg.clear()
    svg["viewBox"] = view_box
    svg["preserveAspectRatio"] = "xMidYMid meet"
    image = s.new_tag("image", attrs={
        "href": uri, "x": "0", "y": "0",
        "width": str(width), "height": str(height),
        "preserveAspectRatio": "xMidYMid meet"
    })
    svg.append(image)

for svg in s.select("svg.nav-logo__wordmark-svg"):
    embed_svg_asset(svg, wordmark_uri, "0 0 170 15", 170, 15)

STAR_PATH = "M116.151 0C116.151 64.1483 64.1483 116.151 0 116.151C64.1483 116.151 116.151 168.153 116.151 232.302C116.151 168.153 168.153 116.151 232.302 116.151C168.153 116.151 116.151 64.1483 116.151 0Z"
for svg in s.select("svg.home-hero__top-logo"):
    svg.clear()
    svg["viewBox"] = "0 0 233 233"
    p = s.new_tag("path", attrs={"d": STAR_PATH, "fill": "#78FF45"})
    svg.append(p)

path.write_text(str(s), encoding="utf8")
print("Applied canonical Green Groove header wordmark and hero star.")
