from bs4 import BeautifulSoup
from pathlib import Path
import base64, gzip, hashlib, sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
s = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")


def normalize_svg(selector: str, viewbox: str):
    count = 0
    for svg in s.select(selector):
        # html.parser lowercases source attributes, while attributes assigned later
        # can coexist in mixed case. Remove every case variant so browsers never
        # keep the stale source viewBox.
        for key in list(svg.attrs):
            if key.lower() in {"viewbox", "preserveaspectratio"}:
                del svg.attrs[key]
        svg["viewBox"] = viewbox
        svg["preserveAspectRatio"] = "xMidYMid meet"

        for image in svg.find_all("image"):
            for key in list(image.attrs):
                if key.lower() == "preserveaspectratio":
                    del image.attrs[key]
            image["preserveAspectRatio"] = "xMidYMid meet"
        count += 1
    return count


counts = {
    "desktop_wordmark": normalize_svg("svg.nav-logo__wordmark-svg", "0 0 170 15"),
    "compact_cube": normalize_svg("svg.nav-logo__icon-svg", "0 0 136 136"),
    "hero_star": normalize_svg("svg.home-hero__top-logo", "0 0 233 233"),
}

# Exact user-supplied Vector.svg. It stays inline so Osmo's original
# [data-footer-logo-wrap] GSAP/ScrollTrigger routine can animate every path.
FOOTER_MARK_GZ_B64 = "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"
footer_mark_svg = gzip.decompress(base64.b64decode(FOOTER_MARK_GZ_B64))
assert hashlib.sha256(footer_mark_svg).hexdigest() == "4278f2297cfa45e81c8bda3fa0779f1fc00d461c0f8af8d3519af0af4ad71331"
footer_fragment = BeautifulSoup(footer_mark_svg.decode("utf8"), "html.parser")
footer_svg = footer_fragment.find("svg")
for key in list(footer_svg.attrs):
    if key.lower() in {"width", "height", "viewbox", "preserveaspectratio"}:
        del footer_svg.attrs[key]
footer_svg["viewBox"] = "0 0 12578 431"
footer_svg["preserveAspectRatio"] = "xMidYMid meet"
footer_svg["class"] = "gg-footer-wordmark"
footer_svg["role"] = "img"
footer_svg["aria-label"] = "Green Groove"
footer_svg["style"] = "display:block;width:100%;height:auto;max-width:none;overflow:visible;"

footer_slots = s.select("[data-footer-logo-wrap]")
for slot in footer_slots:
    slot.clear()
    # Reparse per slot so every footer gets its own inline path tree.
    slot.append(BeautifulSoup(str(footer_svg), "html.parser"))
counts["animated_footer_mark"] = len(footer_slots)

path.write_text(str(s), encoding="utf8")
print("Normalized canonical Green Groove SVG geometry and installed animated footer mark:", counts)