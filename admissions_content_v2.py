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


# AO content pass v2: sharpen the intellectual arc and surface the documented
# NCERT PRAYAAS / IIT Delhi relationship without changing layout or artwork.
meta_description = (
    "Green Groove is a student-built RFID + sensor retail system selected under "
    "NCERT PRAYAAS, supported through IIT Delhi as the associated HEI, and awarded "
    "a ₹50,000 development grant to build a live, reversible transaction state."
)
for tag in soup.find_all("meta"):
    key = tag.get("name") or tag.get("property")
    if key in {"description", "og:description", "twitter:description"}:
        tag["content"] = meta_description

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
        "award": "NCERT PRAYAAS selection; ₹50,000 development grant",
        "description": meta_description,
        "keywords": [
            "RFID retail",
            "sensor shelves",
            "live cart",
            "NCERT PRAYAAS",
            "IIT Delhi",
        ],
    },
    separators=(",", ":"),
)
soup.head.append(ld)

# Hero/origin copy. These exact-text upgrades are opportunistic because portions
# of the source hero are animation-split across spans; the structural sections
# below are the required part of this pass.
hero = section("home-hero")
replace_many(
    hero,
    {
        "NCERT PRAYAAS · ₹50K GRANT": "NCERT PRAYAAS · IIT DELHI · ₹50K GRANT",
        "Student-built RFID + sensor retail system that turns shelf events into a live cart and automates billing as you shop.": "Student-built RFID + sensor retail system that maintains transaction state while shopping happens, turning checkout into settlement.",
    },
)

db = section("db")
replace_many(
    db,
    {
        "A queue was the symptom. The deeper problem was rebuilding a shopping trip only when the shopper reached checkout.": "We started with supermarket queues. The deeper question became: why reconstruct a shopper's basket only when they reach the register?",
        "Green Groove builds that transaction state as the trip happens — through RFID identity, sensor shelves, a live cart and reversible events.": "If identity, shelf events and cart state stay synchronized throughout the trip, checkout becomes confirmation of an already-known transaction.",
    },
)

prod = section("product-slider")
replace_many(
    prod,
    {
        "Six layers. One checkout-free flow.": "Six layers. One trustworthy transaction state.",
        "Each layer removes one step from manual billing:": "Each layer resolves one source of uncertainty:",
    },
)

# Reframe the existing six-card findings carousel around the engineering problems
# the build exposed. It preserves the source card geometry and interaction.
challenges = [
    (
        "Detection is not association.",
        "Challenge 01",
        "Association",
        "A shelf can tell us that an item moved; the harder problem is deciding which shopper changed it before the live cart is allowed to update.",
    ),
    (
        "Physical actions must be reversible.",
        "Challenge 02",
        "State recovery",
        "Shoppers return products and change their minds, so add/remove operations need explicit inverse transitions rather than silent corrections.",
    ),
    (
        "Sensors need a second opinion.",
        "Challenge 03",
        "Consistency",
        "Shelf state and live cart state are two observations of the same transaction; disagreement can reveal missed, duplicate or ambiguous events.",
    ),
    (
        "Identity has to precede automation.",
        "Challenge 04",
        "RFID identity",
        "An event without a reliable shopper or cart context cannot safely modify transaction state, even when the physical detection itself is correct.",
    ),
    (
        "Uncertainty should stay visible.",
        "Challenge 05",
        "Trust",
        "When an association is ambiguous, surfacing uncertainty is safer than silently forcing the event into the wrong shopper's cart.",
    ),
    (
        "Checkout was downstream of the real problem.",
        "Challenge 06",
        "Problem framing",
        "Once transaction state is maintained throughout the trip, final billing becomes settlement of known state rather than reconstruction from scratch.",
    ),
]
testimonial = section("testimonial")
if not testimonial:
    raise SystemExit("AO v2 pass aborted: testimonial/findings section is missing.")
cards = testimonial.select("h3.is--testimonial")[:6]
if len(cards) < 6:
    raise SystemExit(f"AO v2 pass aborted: expected 6 findings cards, found {len(cards)}.")

replace_many(
    testimonial,
    {
        "From": "What became",
        "shelf to cart": "hard to solve",
        "Green Groove": "Engineering",
        "system principles": "lessons from the build",
    },
)
for i, heading in enumerate(cards):
    title, label, role, body_text = challenges[i]
    heading.string = title
    ancestor = heading
    for _ in range(9):
        if ancestor and (
            ancestor.find("h4", class_="scribble")
            or ancestor.find(string=lambda x: x and "Insight 0" in norm(x))
        ):
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

# Use the existing evidence card for institutional validation. Keep tense precise:
# IIT Delhi is the associated HEI; facilities/resources are part of the next phase,
# not represented as work already completed.
pricing = section("pricing-home")
if not pricing:
    raise SystemExit("AO v2 pass aborted: evidence section is missing.")
replace_many(
    pricing,
    {
        "Selected. Funded. Built.": "Selected. Mentored. Building.",
        "See the evidence": "See the validation",
    },
)
pricing_cards = pricing.select(".pricing-card")
if not pricing_cards:
    raise SystemExit("AO v2 pass aborted: evidence cards are missing.")

card = pricing_cards[0]
tag = card.select_one(".tag .eyebrow, .tag span")
if tag:
    tag.string = "PRAYAAS × IIT Delhi"
title = card.select_one(".pricing-card__title")
if title:
    title.string = "Selected + funded"
lead = card.select_one(".pricing-card__sub > .p-m")
if lead:
    lead.string = "₹50,000 awarded"
subs = card.select(".pricing-card__sub-details .p-m")
if subs:
    subs[0].string = "IIT Delhi HEI"
if len(subs) > 1:
    subs[1].string = "SeNSE mentorship"
benefit = card.select_one(".pricing-benefit__start > p")
if benefit:
    benefit.string = (
        "Selected in the urban private category under NCERT PRAYAAS, with IIT Delhi "
        "as the associated HEI and Prof. Satish Kumar Dubey of SeNSE as mentor. The "
        "₹50,000 grant supports the next development phase using institutional "
        "facilities, technical resources and further prototype validation."
    )
under = card.select_one(".underline-link")
if under:
    under.string = "Programme evidence"
scribble = card.select_one(".pricing-card__scribble .scribble")
if scribble:
    scribble.string = "NCERT + IIT Delhi mentorship"

# Finish on the change in problem framing rather than a product-sales CTA.
try_section = section("try-vault")
replace_many(
    try_section,
    {
        "From queue problem to working system.": "A queue problem became a systems problem.",
        "See how Green Groove was built": "See the project story",
    },
)

path.write_text(str(soup), encoding="utf-8")
print("Applied AO content v2: engineering challenges + NCERT PRAYAAS / IIT Delhi validation.")
