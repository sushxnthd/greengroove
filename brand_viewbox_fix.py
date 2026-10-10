from bs4 import BeautifulSoup
from pathlib import Path
import sys

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
        svg["viewbox"] = viewbox
        svg["preserveaspectratio"] = "xMidYMid meet"

        for image in svg.find_all("image"):
            for key in list(image.attrs):
                if key.lower() == "preserveaspectratio":
                    del image.attrs[key]
            image["preserveaspectratio"] = "xMidYMid meet"
        count += 1
    return count

counts = {
    "desktop_wordmark": normalize_svg("svg.nav-logo__wordmark-svg", "0 0 170 15"),
    "compact_cube": normalize_svg("svg.nav-logo__icon-svg", "0 0 136 136"),
    "hero_star": normalize_svg("svg.home-hero__top-logo", "0 0 233 233"),
    "footer_wordmark": normalize_svg("svg.footer-bottom__logo", "0 0 170 15"),
}

path.write_text(str(s), encoding="utf8")
print("Normalized canonical Green Groove SVG geometry:", counts)
