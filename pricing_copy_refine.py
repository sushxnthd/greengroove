from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def add_class(tag, class_name: str) -> None:
    classes = list(tag.get("class", []))
    if class_name not in classes:
        classes.append(class_name)
        tag["class"] = classes


def remove_counter(start) -> bool:
    """Remove the decorative source-template `06` badge without touching the copy."""
    matches = [
        node
        for node in start.find_all(True)
        if node.name != "p" and norm(node.get_text(" ", strip=True)) == "06"
    ]
    if not matches:
        return False

    # Remove the outermost wrapper whose complete content is still only `06` so
    # an empty source-template badge shell does not keep taking up horizontal space.
    target = matches[-1]
    while (
        target.parent
        and target.parent is not start
        and norm(target.parent.get_text(" ", strip=True)) == "06"
    ):
        target = target.parent
    target.decompose()
    return True


def set_description(soup, card, lead: str, support: str) -> None:
    start = card.select_one(".pricing-benefit__start")
    body = card.select_one(".pricing-benefit__start > p")
    if not start or not body:
        raise RuntimeError("Pricing card description structure changed unexpectedly.")

    add_class(start, "gg-editorial-description-wrap")
    add_class(body, "gg-card-description")
    add_class(body, "gg-wrap-copy")

    body.clear()
    lead_el = soup.new_tag("span")
    lead_el["class"] = ["gg-card-lead"]
    lead_el.string = lead

    support_el = soup.new_tag("span")
    support_el["class"] = ["gg-card-support"]
    support_el.string = support

    body.append(lead_el)
    body.append(support_el)
    remove_counter(start)


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    pricing = soup.find("section", class_="pricing-home")
    if not pricing:
        raise RuntimeError("Evidence/pricing section is missing.")
    cards = pricing.select(".pricing-card")[:2]
    if len(cards) < 2:
        raise RuntimeError(f"Expected two evidence cards, found {len(cards)}.")

    set_description(
        soup,
        cards[0],
        "Selected for NCERT PRAYAAS with IIT Delhi as the associated HEI, alongside a ₹50,000 development grant and SeNSE mentorship.",
        "Supporting prototype refinement, validation and further development.",
    )
    set_description(
        soup,
        cards[1],
        "A connected retail system combining the Groove Band, sensor-enabled shelves and G/G App.",
        "Physical product movement is translated into a live digital cart.",
    )

    # Keep the source composition, but make these two blocks read like editorial
    # evidence rather than template feature-list copy.
    if not soup.find(id="gg-pricing-copy-refine"):
        style = soup.new_tag("style", id="gg-pricing-copy-refine")
        style.string = r"""
.pricing-card .gg-editorial-description-wrap {
  display: block !important;
  padding-left: 0 !important;
  gap: 0 !important;
}

.pricing-card .gg-card-description {
  display: block !important;
  width: min(100%, 34rem) !important;
  max-width: 34rem !important;
  min-width: 0 !important;
  margin: 0 !important;
  white-space: normal !important;
  font-size: clamp(1.0625rem, 1.08vw, 1.2rem) !important;
  line-height: 1.38 !important;
  letter-spacing: -0.018em !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
  text-wrap: pretty;
}

.pricing-card .gg-card-lead,
.pricing-card .gg-card-support {
  display: block !important;
}

.pricing-card .gg-card-lead {
  font-weight: 500 !important;
}

.pricing-card .gg-card-support {
  margin-top: .55rem !important;
  opacity: .68 !important;
  max-width: 29rem !important;
}

@media (max-width: 767px) {
  .pricing-card .gg-card-description {
    width: 100% !important;
    max-width: 100% !important;
    font-size: 1rem !important;
    line-height: 1.42 !important;
  }
  .pricing-card .gg-card-support {
    margin-top: .45rem !important;
  }
}
"""
        (soup.head or soup).append(style)

    path.write_text(str(soup), encoding="utf-8")
    print("Refined both evidence-card descriptions and removed decorative counters.")


if __name__ == "__main__":
    main()
