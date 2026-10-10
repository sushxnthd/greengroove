from __future__ import annotations

from pathlib import Path
import json
import sys

from bs4 import BeautifulSoup

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def section(class_name: str):
    return soup.find("section", class_=class_name)


def norm(value) -> str:
    return " ".join(str(value).split())


def replace_exact(root, old: str, new: str) -> int:
    if not root:
        return 0
    changed = 0
    for node in list(root.find_all(string=True)):
        if not node.parent or node.parent.name in {"script", "style", "title"} or node.find_parent("svg"):
            continue
        if norm(node) == old:
            node.replace_with(new)
            changed += 1
    return changed


def replace_many(root, mapping: dict[str, str]) -> dict[str, int]:
    return {old: replace_exact(root, old, new) for old, new in mapping.items()}


# Admissions goal: preserve the established UI and technical depth while making the
# first 30 seconds answer four questions immediately: why it matters, what was built,
# who built it, and what external validation it earned.

# Metadata / share cards.
soup.title.string = "Green Groove — Student-Built Checkout System"
meta_description = (
    "Green Groove is a student-built RFID + sensor retail system selected under "
    "NCERT PRAYAAS and awarded a ₹50,000 grant, designed to automate billing through "
    "shopper identity, shelf sensing and a live cart."
)
for tag in soup.find_all("meta"):
    key = tag.get("name") or tag.get("property")
    if key in {"description", "og:description", "twitter:description"}:
        tag["content"] = meta_description
    elif key in {"og:title", "twitter:title"}:
        tag["content"] = "Green Groove — Student-Built Checkout System"

for old in list(soup.find_all("script", type="application/ld+json")):
    old.decompose()
ld = soup.new_tag("script", type="application/ld+json")
ld.string = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": "Green Groove",
        "url": "https://sushxnthd.github.io/greengroove/",
        "creator": [
            {"@type": "Person", "name": "Sushanth Dasari"},
            {"@type": "Person", "name": "Aryan Kumar"},
        ],
        "award": "Selected under NCERT PRAYAAS; ₹50,000 development grant",
        "description": meta_description,
    },
    separators=(",", ":"),
)
soup.head.append(ld)

# Hero: recognition + problem first, architecture second.
hero = section("home-hero")
hero_changes = replace_many(
    hero,
    {
        "Selected under NCERT PRAYAAS": "NCERT PRAYAAS · ₹50K GRANT",
        "Retail State": "Checkout",
        "Built to Flow": "Without the Queue",
        "Retail system linking RFID & shelf sensing events, live cart, returns and settlement flow": "Student-built RFID + sensor retail system that turns shelf events into a live cart and automates billing as you shop.",
        "Retail system linking RFID & shelf sensing events, live cart, returns and settlement.": "Student-built RFID + sensor retail system that turns shelf events into a live cart and automates billing as you shop.",
    },
)

# System story: make the origin/insight legible to a nontechnical reader.
db = section("db")
replace_many(
    db,
    {
        "A physical-digital retail prototype linking identity, shelf events, association, reversible cart state and settlement.": "A queue was the symptom. The deeper problem was rebuilding a shopping trip only when the shopper reached checkout.",
        "Built so every shopping action can be observed, explained and safely reversed.": "Green Groove builds that transaction state as the trip happens — through RFID identity, sensor shelves, a live cart and reversible events.",
    },
)

# Architecture: retain the technically strong six-layer model, but ground every
# layer in something a reader can picture being built or tested.
prod = section("product-slider")
replace_many(
    prod,
    {
        "Six layers, one retail state": "Six layers. One checkout-free flow.",
        "Each layer has one job:": "Each layer removes one step from manual billing:",
    },
)
layer_copy = [
    (
        "Identity",
        "Give each shopper a unique RFID wristband so item events have a known cart context.",
    ),
    (
        "Shelf Events",
        "Use load cells and RFID readers to detect when products leave or return to a shelf.",
    ),
    (
        "Association",
        "Match each shelf event to the right active shopper before changing cart state.",
    ),
    (
        "Reversibility",
        "Treat returns and mistakes as inverse events so recovery stays visible instead of hidden.",
    ),
    (
        "Live Cart",
        "Update the virtual cart in real time as products are picked up or put back.",
    ),
    (
        "Settlement",
        "Generate the final invoice from the cart already built during the shopping trip.",
    ),
]
if prod:
    for card, (name, desc) in zip(prod.select(".product-card"), layer_copy):
        heading = card.select_one(".product-card__h")
        body = card.select_one(".product-card__p")
        if heading:
            heading.string = name
        if body:
            body.string = desc

# Why: problem framing before implementation detail.
info = section("info")
replace_many(
    info,
    {
        "If the system can explain how state changed, it can recover when the physical world gets messy.": "The queue was the symptom. Manual reconstruction at checkout was the deeper problem.",
        "RFID identity and shelf sensing turn physical actions into inspectable events.": "RFID identity, load cells and shelf readers turn a physical pick or return into an explicit event.",
        "Association logic decides who changed what before state is committed.": "Association connects each shelf event to the right shopper before the live cart changes.",
        "Returns and mistakes become inverse transitions rather than hidden corrections.": "Returns reverse earlier state instead of silently overwriting history, so the system can recover cleanly.",
    },
)

# Findings: turn abstract design principles into evidence of intellectual learning.
findings = [
    (
        "The queue was a symptom.",
        "Insight 01",
        "Problem framing",
        "The deeper bottleneck was reconstructing the shopper's basket at checkout after the journey had already happened.",
    ),
    (
        "Identity comes before automation.",
        "Insight 02",
        "RFID identity",
        "A shelf event is only useful when the system knows which shopper or cart context it belongs to.",
    ),
    (
        "Shelf events need context.",
        "Insight 03",
        "Association",
        "Detection and association stay separate so ambiguous multi-shopper events can be surfaced instead of silently forced.",
    ),
    (
        "Reversibility is part of trust.",
        "Insight 04",
        "Recovery",
        "Returns and mistakes should reverse earlier transitions with history intact rather than become unexplained corrections.",
    ),
    (
        "Physical and digital state should cross-check.",
        "Insight 05",
        "Consistency",
        "Shelf state and live cart state are two views of the same transaction and can expose missed or duplicate changes.",
    ),
    (
        "Checkout should settle, not reconstruct.",
        "Insight 06",
        "Settlement",
        "If the cart is maintained throughout the trip, the final transaction becomes confirmation of known state rather than a fresh scan.",
    ),
]
testimonial = section("testimonial")
if testimonial:
    cards = testimonial.select("h3.is--testimonial")[:6]
    for i, heading in enumerate(cards):
        title, label, role, body_text = findings[i]
        heading.string = title
        ancestor = heading
        for _ in range(9):
            if ancestor and (ancestor.find("h4", class_="scribble") or ancestor.find(string=lambda x: x and "Insight 0" in norm(x))):
                break
            ancestor = ancestor.parent if ancestor else None
        if ancestor:
            scribble = ancestor.find("h4", class_="scribble")
            if scribble:
                scribble.string = label
            short_paragraphs = [
                p
                for p in ancestor.find_all("p")
                if 2 < len(norm(p.get_text(" ", strip=True))) < 45
            ]
            if short_paragraphs:
                short_paragraphs[0].string = role
            long_paragraphs = [
                p
                for p in ancestor.find_all("p")
                if len(norm(p.get_text(" ", strip=True))) > 55
            ]
            if long_paragraphs:
                long_paragraphs[-1].string = body_text

# Evidence/roadmap: use the existing two-card composition to surface real external
# validation and the tangible prototype instead of generic product-roadmap language.
pricing = section("pricing-home")
replace_many(
    pricing,
    {
        "Prototype today. System next.": "Selected. Funded. Built.",
        "View roadmap": "See the evidence",
    },
)
if pricing:
    cards = pricing.select(".pricing-card")
    card_data = [
        {
            "tag": "NCERT PRAYAAS",
            "title": "Selected",
            "numbers": ["1", "1"],
            "unit": "grant",
            "lead": "Awarded",
            "subs": ["₹50,000", "support"],
            "cta": "See recognition",
            "benefit": "Selected in the urban private category under NCERT PRAYAAS to develop Green Groove further.",
            "under": "Evidence",
            "scribble": "Externally selected + funded",
        },
        {
            "tag": "3 modules",
            "title": "Built",
            "numbers": ["3", "3"],
            "unit": "modules",
            "lead": "Prototype stack",
            "subs": ["RFID + sensing", "live cart"],
            "cta": "See the build",
            "benefit": "Groove Band + sensor shelves + G/G App turn physical product movement into a live digital cart.",
            "under": "View build",
            "scribble": "Physical + digital prototype",
        },
    ]
    for card, data in zip(cards, card_data):
        tag = card.select_one(".tag .eyebrow, .tag span")
        if tag:
            tag.string = data["tag"]
        title = card.select_one(".pricing-card__title")
        if title:
            title.string = data["title"]
        price_nodes = card.select(".pricing-card__price-h")
        if price_nodes:
            price_nodes[0].string = ""
            numeric_nodes = [
                p for p in price_nodes[1:] if "u--opacity-60" not in (p.get("class") or [])
            ]
            for node, value in zip(numeric_nodes, data["numbers"]):
                node.string = value
            unit = card.select_one(".u--opacity-60")
            if unit:
                unit.string = data["unit"]
        lead = card.select_one(".pricing-card__sub > .p-m")
        if lead:
            lead.string = data["lead"]
        for node, value in zip(card.select(".pricing-card__sub-details .p-m"), data["subs"]):
            node.string = value
        for span in card.select(".button-label span"):
            span.string = data["cta"]
        benefit = card.select_one(".pricing-benefit__start > p")
        if benefit:
            benefit.string = data["benefit"]
        under = card.select_one(".underline-link")
        if under:
            under.string = data["under"]
        scribble = card.select_one(".pricing-card__scribble .scribble")
        if scribble:
            scribble.string = data["scribble"]

# Final CTA: end on the project journey, not generic product language.
try_section = section("try-vault")
replace_many(
    try_section,
    {
        "Case study": "Full case study",
        "Want the full project?": "From queue problem to working system.",
        "Explore Green Groove": "See how Green Groove was built",
        "Full case study": "Project story",
    },
)

# Admissions-safe authorship: make shared creation explicit without inventing a role split.
about = soup.select_one(".about-hero")
if about:
    replace_many(
        about,
        {
            "Founder": "Co-creator",
            "Co-Founder": "Co-creator",
            "Designer": "Co-creator",
            "Developer": "Co-creator",
        },
    )

# Fail loudly if the core hero source unexpectedly changes; this prevents publishing
# a half-applied admissions pass after future upstream edits.
if hero:
    if hero_changes.get("Retail State", 0) == 0 or hero_changes.get("Built to Flow", 0) == 0:
        raise SystemExit(
            "Admissions content pass aborted: canonical hero copy was not found. "
            f"Observed replacement counts: {hero_changes}"
        )

path.write_text(str(soup), encoding="utf-8")
print("Applied admissions-focused content pass without changing layout classes/styles/artwork.")
