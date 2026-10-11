from __future__ import annotations

from pathlib import Path
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

PROJECT = "https://sushxnthd.github.io/greengroove/"
BEHANCE = "https://www.behance.net/gallery/211169339/Green-Groove"
GITHUB = "https://github.com/sushxnthd/greengroove"

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def norm(node) -> str:
    if hasattr(node, "stripped_strings"):
        return " ".join(node.stripped_strings).strip().lower()
    return " ".join(str(node).split()).strip().lower()


def section(class_name: str):
    return soup.find("section", class_=class_name)


def assign_alias(root, ident: str, selectors: tuple[str, ...] = ()):
    """Attach a deep-link id to an existing element without adding visible UI."""
    if soup.find(id=ident):
        return soup.find(id=ident)
    if not root:
        raise SystemExit(f"Semantic route target missing for #{ident}")
    target = None
    for selector in selectors:
        target = root.select_one(selector)
        if target:
            break
    if not target:
        target = root.find(["h1", "h2", "h3", "h4"]) or root
    # Never overwrite the section's canonical id; use a zero-content anchor when
    # the best target already owns another id.
    if target.get("id") and target.get("id") != ident:
        marker = soup.new_tag("span", id=ident)
        marker["aria-hidden"] = "true"
        target.insert_before(marker)
        return marker
    target["id"] = ident
    return target


# Primary one-page destinations. Existing section ids remain intact for backwards
# compatibility; these aliases make labels such as Story and Overview genuinely
# distinct destinations rather than cosmetic names for the same hash.
intro = section("intro")
db = section("db")
product = section("product-slider")
pricing = section("pricing-home")
made = section("made")
testimonial = section("testimonial")
try_section = section("try-vault")

assign_alias(db, "story", (".db__title", "h2", "h3"))
assign_alias(intro, "overview", (".intro__title", "h2", "h3"))
assign_alias(intro, "notes", (".vertical-slider", ".vertical-slider__wrap", ".vertical-slider__list"))
assign_alias(pricing, "roadmap", (".pricing-home__button-row",))

# Deep-link each architecture layer to the actual layer card.
layer_ids = {
    "identity": "layer-identity",
    "shelf events": "layer-shelf-events",
    "association": "layer-association",
    "reversibility": "layer-reversibility",
    "live cart": "layer-live-cart",
    "settlement": "layer-settlement",
}
layer_found = set()
if product:
    for card in product.select(".product-card"):
        heading = card.select_one(".product-card__h")
        label = norm(heading) if heading else ""
        if label in layer_ids:
            card["id"] = layer_ids[label]
            layer_found.add(label)
if layer_found != set(layer_ids):
    raise SystemExit(f"Architecture deep-link targets incomplete: found={sorted(layer_found)}")

# Deep-link the three named physical/digital modules to their actual build cards.
module_ids = {
    "groove band": "groove-band",
    "green grooves": "green-grooves",
    "g/g app": "gg-app",
}
module_found = set()
if made:
    for item in made.select(".flick-group__item"):
        heading = item.select_one('[data-res-used="title"]')
        label = norm(heading) if heading else ""
        if label in module_ids:
            item["id"] = module_ids[label]
            module_found.add(label)
if module_found != set(module_ids):
    raise SystemExit(f"Module deep-link targets incomplete: found={sorted(module_found)}")

# Nav routes: every distinct label gets the destination its wording promises.
nav_routes = [
    ("build gallery", "#build"),
    ("green grooves", "#green-grooves"),
    ("groove band", "#groove-band"),
    ("g/g app", "#gg-app"),
    ("architecture", "#architecture"),
    ("overview", "#overview"),
    ("evidence", "#evidence"),
    ("roadmap", "#roadmap"),
    ("story", "#story"),
    ("source", GITHUB),
]

navs = soup.find_all("nav")
if not navs:
    # Osmo's source can use div-based navigation wrappers in some snapshots.
    navs = soup.select(".nav, .nav-wrap, .nav-menu")

primary_seen: dict[str, set[str]] = {key: set() for key, _ in nav_routes}
for nav in navs:
    for a in nav.find_all("a", href=True):
        label = norm(a)
        for key, dest in nav_routes:
            if key in label:
                a["href"] = dest
                primary_seen[key].add(dest)
                break

# Footer routes: point each label to the most specific real content currently on
# the site, rather than inherited Osmo legal/account destinations.
footer_routes = [
    ("shelf events", "#layer-shelf-events"),
    ("reversibility", "#layer-reversibility"),
    ("identity", "#layer-identity"),
    ("architecture", "#architecture"),
    ("build", "#build"),
    ("notes", "#notes"),
    ("project", "#overview"),
    ("roadmap", "#roadmap"),
    ("questions", "#story"),
    ("methods", "#architecture"),
    ("source", GITHUB),
    ("behance", BEHANCE),
    ("evidence", "#evidence"),
]
footer = soup.find("footer")
if footer:
    for a in footer.find_all("a", href=True):
        label = norm(a)
        for key, dest in footer_routes:
            if key in label:
                a["href"] = dest
                break

# Project-specific social shortcuts must remain honest even though they reuse the
# source site's social icon footprints.
for a in soup.find_all("a", href=True):
    aria = str(a.get("aria-label", "")).strip().lower()
    if aria == "behance project":
        a["href"] = BEHANCE
    elif aria == "github source":
        a["href"] = GITHUB
    elif aria == "green groove website":
        a["href"] = PROJECT

# Static semantic assertions. Browser QA later verifies the same controls are
# actually focusable/clickable; these checks verify that their destinations mean
# what their labels say.
errors: list[str] = []
ids = {str(tag.get("id")) for tag in soup.find_all(id=True)}
required_ids = {
    "story", "overview", "notes", "roadmap", "architecture", "build", "evidence",
    *layer_ids.values(), *module_ids.values(),
}
missing_ids = required_ids - ids
if missing_ids:
    errors.append("missing semantic targets: " + ", ".join(sorted(missing_ids)))

# Every primary menu label that exists must resolve consistently. Responsive copies
# may repeat a label, but a label may not fan out to contradictory destinations.
for key, expected in nav_routes:
    destinations = set()
    for nav in navs:
        for a in nav.find_all("a", href=True):
            if key in norm(a):
                destinations.add(str(a.get("href", "")))
    if destinations and destinations != {expected}:
        errors.append(f"nav label {key!r} routes to {sorted(destinations)!r}, expected {expected!r}")

# Distinct top-level concepts should not collapse onto one generic hash.
primary_expected = {
    "story": "#story",
    "overview": "#overview",
    "architecture": "#architecture",
    "groove band": "#groove-band",
    "green grooves": "#green-grooves",
    "g/g app": "#gg-app",
    "build gallery": "#build",
    "evidence": "#evidence",
    "roadmap": "#roadmap",
    "source": GITHUB,
}
vals = list(primary_expected.values())
if len(vals) != len(set(vals)):
    errors.append("primary semantic route table itself contains collapsed destinations")

for a in soup.find_all("a", href=True):
    href = str(a.get("href", "")).strip()
    if href.startswith("#") and href[1:] and href[1:] not in ids:
        errors.append(f"missing deep-link target: {norm(a)!r} -> {href!r}")

if errors:
    raise SystemExit("Semantic route audit failed:\n- " + "\n- ".join(sorted(set(errors))))

path.write_text(str(soup), encoding="utf-8")
print("Semantic route audit passed: primary labels now resolve to distinct, truthful destinations.")
