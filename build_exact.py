from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

SOURCE_URL = "https://www.osmo.supply/"
req = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
html = urlopen(req, timeout=30).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Metadata only. Layout, class hierarchy and interaction hooks stay source-faithful.
soup.title.string = "Green Groove — Retail State System"
for meta in soup.find_all("meta"):
    key = meta.get("name") or meta.get("property")
    if key in {"description", "og:description", "twitter:description"}:
        meta["content"] = "A physical-digital retail system connecting RFID identity, shelf events, live cart state, reversibility and settlement."
    elif key in {"og:title", "twitter:title"}:
        meta["content"] = "Green Groove — Retail State System"

for link in soup.find_all("link"):
    rel = " ".join(link.get("rel") or [])
    if "icon" in rel:
        link["href"] = "favicon.svg"

# Exact source geometry, Green Groove copy.
text_map = {
    "Login": "Study", "Join": "View", "Our Products": "System",
    "The Vault": "Overview", "Page Transition Course": "Architecture",
    "Button Pack": "Groove Band", "Icon Library": "Green Grooves",
    "Community": "G/G App", "Easings": "Validation",
    "Osmo Showcase": "Build Gallery", "Collection": "Evidence", "Pricing": "Roadmap",
    "Member Login": "Research", "Join Osmo": "View Project",
    "Demo: Try 20 Resources for Free": "Selected under NCERT PRAYAAS",
    "Dev Toolkit": "Retail State", "Built to Flex": "Built to Flow",
    "Platform packed with": "Retail system linking", "Webflow": "RFID",
    "HTML": "shelf sensing", "resources,": "events,", "icons": "live cart",
    "easings": "returns", "and a page transition": "and settlement", "course": "flow",
    "Mega Navigation (Directional Hover)": "RFID Identity",
    "3D Cards Tornado": "Shelf Event Capture",
    "Shutter Scroll Transition": "Return Reversal",
    "Radial Cards Slider (GSAP)": "Live Cart State",
    "Product Hotspot Modal": "Association Logic",
    "Number Odometer": "Checkout Settlement",
    "Step-by-step Timeline": "Event History",
    "Animated Grid Overlay (Columns)": "Field Validation",
    "Collage Focus Card on Hover": "Product Interaction",
    "Osmo is an ever-growing platform with Webflow & HTML resources. Get exclusive access to the elements, techniques and code behind award-winning work.":
        "Green Groove is a physical-digital retail system built around identity, shelf events, reversible cart state and a legible checkout flow.",
    "Osmo in use": "Green Groove in use", "See what it can do!": "See the system in motion",
    "Join 3K+ others": "Selected under NCERT PRAYAAS", "Dennis": "Sushanth", "Ilja": "Aryan",
    "Snellenberg": "Dasari", "van Eck": "Kumar", "About us": "About the project",
    "Latest updates": "Project notes", "from Osmo": "from Green Groove",
    "New stuff is": "Research and build notes", "added every week!": "from the project.",
    "The platform": "The system", "( The Vault )": "( Green Groove )",
    "Built by two award-winning creative developers, our vault gives you access to the techniques, components, code, and tools behind our projects. Build, tweak, and make them your own.":
        "Green Groove models shopping as observable state transitions: identify the shopper, detect a shelf event, associate it, update the cart, reverse mistakes, then settle cleanly.",
    "We built Osmo to help creative developers work smarter, faster, and better.":
        "The goal is simple: make physical shopping state legible, reversible and reliable.",
    "About the Vault": "Explore the system",
    "A growing toolkit for creative developers": "One retail system, six connected layers",
    "Access everything with a single membership:": "Each layer solves one concrete responsibility:",
    "Buttons": "Association", "Icons": "Live Cart", "Membership": "System",
    "Our ever-growing dashboard packed with ready-to-go components.":
        "Identify a shopper or cart context before any item event is committed.",
    "Learn how to create page transitions that take your websites to the next level.":
        "Detect additions and removals at the shelf as explicit physical events.",
    "100 fully accessible buttons made together with Eduard Bodak.":
        "Resolve which shopper and item belong to each observed event.",
    "Ready-to-paste easings for CSS and GSAP inside the Osmo Vault.":
        "Treat mistakes and returns as reversible state transitions, not exceptions.",
    "A uniform library of clean, scalable SVG icons you can copy or download in seconds.":
        "Maintain a live cart that reflects the current physical state of the journey.",
    "Connect with the people who love building great websites as much as you do.":
        "Close the loop with a clear settlement state at checkout.",
    "Why Osmo?": "Why state?",
    "Level up your game and join a community of creatives who love building great websites as much as you do.":
        "A retail experience becomes trustworthy when each physical action maps to a clear digital state.",
    "Build faster and better": "Observe physical events",
    "Our resources save you hours of rebuilding from scratch. Each one is made for real-world projects, so you can focus on shipping work that stands out.":
        "RFID identity and shelf sensing turn movement in the aisle into explicit, inspectable events.",
    "Speed up your process": "Resolve ambiguity",
    "These aren’t stripped-down templates. Every resource is built to be fast, flexible, and production-ready, so you can ship beautiful work without trading quality for time.":
        "Association logic decides who changed what, while the live cart exposes the resulting state.",
    "A living and growing system": "Reverse safely",
    "We keep adding new resources, ideas, and techniques every week. The Vault evolves with you and your needs, so your toolkit never stops expanding.":
        "Returns and mistakes are handled as reversible events so the system can recover without hiding history.",
    "Trusted by": "Built for", "Industry Giants": "real retail flow", "Connect": "Designed",
    "Worldwide": "end to end", "Osmo’s Global": "Green Groove system",
    "Everything you need in one membership": "Validation & evidence",
    "Quarterly": "System", "Annually": "Prototype", "Save 20%": "Integrated",
    "per user": "components", "1 user": "6 layers", "Solo": "System",
    "25": "6", "20": "3", "EUR": "layers", "Per month, billed": "Identity → settlement",
    "quarterly": "connected", "annually": "physical + digital", "Become a member": "View architecture",
    "Vault Resources, added weekly": "RFID, shelf sensing, association, reversibility, live cart, settlement",
    "View all benefits": "View evidence", "min 2 users": "3 components", "Team": "Prototype",
    "16": "3", "Per person/month, billed": "Band + shelves + app", "Sign up your team": "See the build",
    "Save an extra": "One", "20% per user!": "connected system", "View full pricing": "View roadmap",
    "with": "as", "Osmo": "Green Groove",
    "Garaje Inspiration Fest": "Groove Band", "Extrafazant": "Green Grooves", "Wiemer": "G/G App",
    "Uniserve": "Product Interaction", "LxL Creative": "Circuitry", "Filmbot": "Kano Analysis", "Dkton": "Prospects",
    "Resources Used": "System view", "These folks": "The pieces", "are talented": "work together",
    "Explore showcase": "Explore build", "Try for free": "Explore project",
    "Want a taste before you buy?": "See the system beyond the homepage.",
    "Try the Osmo Demo Vault": "Open the Green Groove project", "Unlock the demo": "View project",
    "Try 20": "Explore", "Resources for Free": "the build",
    "Subscribe to the Osmo Newsletter": "Green Groove project notes", "Get updates": "View research",
    "Product": "Project", "Showcase": "Build", "About Osmo": "About", "Updates": "Notes",
    "FAQs": "Questions", "Support": "Contact", "Licensing": "Research", "T&CS": "Methods",
    "Cookies": "Evidence", "osmo supply b.v.": "green groove", "Project name": "Green Groove",
    "name here": "Retail State System", "Heading": "System layer", "Visit site": "View section",
    "A platform by...": "A project by...",
    "Based in Netherlands and Belgium, and with a combined total of 38 Site of the Day awards on Awwwards, we’ve put our years of experience in to a platform that empowers you to create interactive, animated, one-of-a-kind websites.":
        "Green Groove is a student-built exploration of how identity, shelf sensing and reversible event logic can make retail state easier to understand and recover.",
    "120+": "3", "Sites Pushed Live": "Integrated components", "38": "6", "Site of the Day Awards": "Connected system layers"
}

for node in list(soup.find_all(string=True)):
    if not node.parent or node.parent.name in {"script", "style", "title"} or node.find_parent("svg"):
        continue
    normalized = " ".join(str(node).split())
    if normalized in text_map:
        node.replace_with(text_map[normalized])

# Keep Osmo's exact SVG boxes but replace the artwork with Green Groove branding.
def replace_wordmark(svg):
    svg.clear()
    svg["viewBox"] = "0 0 540 156"
    text = soup.new_tag("text", x="270", y="104")
    text["text-anchor"] = "middle"
    text["fill"] = "currentColor"
    text["font-size"] = "70"
    text["font-weight"] = "700"
    text.string = "GREEN GROOVE"
    svg.append(text)

def replace_icon(svg):
    svg.clear()
    svg["viewBox"] = "0 0 80 80"
    path = soup.new_tag("path")
    path["d"] = "M40 0 L47 32 L80 40 L47 48 L40 80 L33 48 L0 40 L33 32 Z"
    path["fill"] = "currentColor"
    svg.append(path)

for svg in soup.select("svg.nav-logo__wordmark-svg"):
    replace_wordmark(svg)
for svg in soup.select("svg.nav-logo__icon-svg, svg.home-hero__top-logo"):
    replace_icon(svg)

project_media = [
    "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/09cb22211169339.67245eac9212c.png",
    "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/8f77ac211169339.67245eac91a69.png",
    "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/991f2f211169339.67245eac930ce.png",
    "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/d434be211169339.67245eac9258b.png",
    "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/c2fc79211169339.67245eac92c6c.png",
    "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/70a4ef211169339.67245eac915e5.png",
]

for section_class, selector in [
    ("home-hero", "img.resource-card__img"),
    ("intro", "img.cover-image"),
    ("product-slider", "img.cover-image"),
    ("made", "img.showcase-media__image"),
]:
    section = soup.find("section", class_=section_class)
    if section:
        for i, image in enumerate(section.select(selector)):
            image["src"] = project_media[i % len(project_media)]

# Preserve every video box and its animation hooks, but use Green Groove media instead of Osmo footage.
for section_class in ["home-hero", "reel", "intro", "db", "product-slider", "made"]:
    section = soup.find("section", class_=section_class)
    if section:
        for i, video in enumerate(section.find_all("video")):
            video.attrs.pop("data-video-src", None)
            video.attrs.pop("src", None)
            video["poster"] = project_media[i % len(project_media)]

system_section = soup.find("section", class_="db")
if system_section:
    image = system_section.select_one("img.cover-image")
    if image:
        image["src"] = project_media[3]

intro = soup.find("section", class_="intro")
if intro:
    for i, image in enumerate(intro.select("img.about-card__img")):
        image["src"] = project_media[(i + 1) % len(project_media)]

testimonial = soup.find("section", class_="testimonial")
if testimonial:
    for image in testimonial.find_all("img"):
        if "testimonial-globe__img" not in (image.get("class") or []):
            image["src"] = "favicon.svg"

try_section = soup.find("section", class_="try-vault")
if try_section:
    for i, image in enumerate(try_section.select("img.cover-image")):
        image["src"] = project_media[i % len(project_media)]

# Findings replace marketing testimonials; same source card DOM and slider behavior.
findings = [
    ("A cart state is only useful when it can explain how it changed.", "Finding 01", "Event model", "Green Groove treats add, remove and return actions as explicit events rather than silent cart mutations."),
    ("Identity should be resolved before an item event is committed.", "Finding 02", "Association", "Separating detection from association makes multi-shopper ambiguity visible instead of hiding it."),
    ("Reversibility belongs in the model, not in an exception path.", "Finding 03", "Recovery", "Returns and mistakes can be represented as inverse transitions with history preserved."),
    ("The shelf and the cart are two views of the same retail state.", "Finding 04", "State consistency", "Consistency checks between physical inventory events and cart state expose missed or duplicate events."),
    ("A good interface shows uncertainty before it shows confidence.", "Finding 05", "UX", "Ambiguous associations should be surfaced for correction rather than silently committed."),
    ("Checkout should settle a known state, not reconstruct one at the end.", "Finding 06", "Settlement", "Maintaining state throughout the journey reduces the amount of inference required at checkout."),
]
old_names = ["Dang Nguyen", "Cassie Evans", "Huy (by Huy)", "Jordan Gilroy", "Jesper Landberg", "Victor Work"]
old_roles = ["Head of Creative", "Education GSAP", "Designer & YT creator", "Web Designer", "Creative Developer", "VW Lab"]
if testimonial:
    for i, heading in enumerate(testimonial.select("h3.is--testimonial")[:6]):
        heading.string = findings[i][0]
        card = heading
        for _ in range(9):
            card = card.parent
            if card and any(name in " ".join(card.stripped_strings) for name in old_names):
                break
        if card:
            for node in list(card.find_all(string=True)):
                value = " ".join(str(node).split())
                if value in old_names:
                    node.replace_with(findings[i][1])
                elif value in old_roles:
                    node.replace_with(findings[i][2])
            paragraphs = card.find_all("p")
            prose = [p for p in paragraphs if len(" ".join(p.stripped_strings)) > 80]
            if prose:
                prose[-1].string = findings[i][3]

# Useful anchors without changing section wrappers.
for cls, ident in [
    ("home-hero", "home"), ("intro", "project"), ("db", "system"),
    ("product-slider", "architecture"), ("info", "why"), ("testimonial", "findings"),
    ("pricing-home", "evidence"), ("made", "build"), ("try-vault", "research"),
]:
    section = soup.find("section", class_=cls)
    if section:
        section["id"] = ident

nav_targets = {
    "Overview": "#project", "Architecture": "#architecture", "Groove Band": "#build",
    "Green Grooves": "#build", "G/G App": "#build", "Validation": "#evidence",
    "Build Gallery": "#build", "Evidence": "#evidence", "Roadmap": "#research",
    "Research": "#research", "View Project": "#project",
}
for anchor in soup.find_all("a", href=True):
    text = " ".join(anchor.stripped_strings)
    for label, target in nav_targets.items():
        if label in text:
            anchor["href"] = target
            break

# Remove account/analytics integrations; retain Webflow/GSAP/Slater source runtime.
for script in list(soup.find_all("script")):
    src = script.get("src", "")
    body = str(script)
    if "outseta" in src.lower() or "plausible" in src.lower() or "data.outseta" in body.lower():
        script.decompose()

# Minimal branding variables only. No geometry patches.
style = soup.new_tag("style", id="green-groove-tailor")
style.string = """
:root{--color-electric:#78ff45;--color-purple:#18bdf2;--color-purple-copy:#18bdf2}
.nav-logo__wordmark-svg text{font-family:Arial,Helvetica,sans-serif;letter-spacing:-5px}
[data-wf--button-theme--variant='purple']{background:linear-gradient(135deg,#00ef78,#18bdf2)!important}
.home-hero__top-logo{color:#16c6c2}
.resource-card__video,.cover-video,.showcase-media__video,.about-card__img{object-fit:cover}
"""
soup.head.append(style)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Generated source-faithful Green Groove homepage from Osmo DOM.")
