from bs4 import BeautifulSoup
from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")

# Osmo's licensed/source animation in 55554.js is deliberately authored around
# seven path elements. It assigns a fixed seven-point arc to paths 0..6 and
# scrubs them back to their neutral position as the footer enters the viewport.
#
# The supplied Green Groove Vector.svg contains three consecutive GREEN GROOVE
# wordmarks (33 unique letter paths) and then an exact duplicate of those 33
# paths. Leaving all 66 in place causes the transformed paths to have stationary
# duplicates directly underneath them, which visually cancels the animation.
#
# Keep one GREEN GROOVE wordmark and combine its 11 letter paths into seven
# balanced chunks around the central G. That lets the original Osmo routine run
# unchanged and animate every visible part of the mark.
GROUPS = (
    (0,),       # G
    (1, 2),     # R E
    (3, 4),     # E N
    (5,),       # G — center/anchor path, matching Osmo's stationary center
    (6, 7),     # R O
    (8, 9),     # O V
    (10,),      # E
)

updated = 0
for wrap in soup.select("[data-footer-logo-wrap]"):
    svg = wrap.find("svg")
    if not svg:
        continue

    source_paths = svg.find_all("path")
    unique_paths = []
    seen_d = set()
    for source_path in source_paths:
        d = source_path.get("d")
        if not d or d in seen_d:
            continue
        seen_d.add(d)
        unique_paths.append(source_path)

    if len(unique_paths) < 11:
        raise RuntimeError(
            f"Expected at least 11 unique Green Groove letter paths; found {len(unique_paths)}"
        )

    phrase = unique_paths[:11]
    rebuilt = []
    for group in GROUPS:
        path_tag = soup.new_tag("path")
        path_tag["d"] = " ".join(phrase[index].get("d", "") for index in group)
        path_tag["fill"] = phrase[group[0]].get("fill", "#201D1D")
        rebuilt.append(path_tag)

    svg.clear()
    for path_tag in rebuilt:
        svg.append(path_tag)

    # One complete GREEN GROOVE wordmark occupies the first ~4190 units of the
    # user's 12578-unit-wide artwork. Cropping the repeated copies is essential:
    # Osmo animates one oversized footer signature, not an ultra-wide strip.
    for key in list(svg.attrs):
        if key.lower() in {"width", "height", "viewbox", "preserveaspectratio", "class", "style"}:
            del svg.attrs[key]
    svg["viewBox"] = "0 0 4190 431"
    svg["preserveAspectRatio"] = "xMidYMid meet"
    svg["class"] = ["footer-bottom__logo-svg", "gg-footer-wordmark"]
    svg["style"] = "display:block;width:100%;height:auto;max-width:none;overflow:visible;"
    svg["role"] = "img"
    svg["aria-label"] = "Green Groove"

    updated += 1

if not updated:
    raise RuntimeError("No [data-footer-logo-wrap] footer mark found")

path.write_text(str(soup), encoding="utf8")
print(f"Rebuilt {updated} footer mark(s) as seven Osmo-compatible animated path chunks")
