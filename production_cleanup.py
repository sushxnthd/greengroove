from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import sys

from bs4 import BeautifulSoup

PROJECT = "https://sushxnthd.github.io/greengroove/"
BEHANCE = "https://www.behance.net/gallery/211169339/Green-Groove"
GITHUB = "https://github.com/sushxnthd/greengroove"
PROJECT_HOST = "sushxnthd.github.io"

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
html = path.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# This pass is intentionally behavior-only. Do not alter visible text, classes,
# inline styles, layout wrappers, media artwork, SVG geometry, or CSS.

# 1) Remove stale Osmo/Outseta account, billing and redirect infrastructure.
for link in list(soup.find_all("link", href=True)):
    href = str(link.get("href", "")).lower()
    rel = {str(x).lower() for x in (link.get("rel") or [])}
    if ("outseta.com" in href or "osmo.b-cdn.net" in href) and rel.intersection({"preconnect", "dns-prefetch"}):
        link.decompose()

stale_script_markers = (
    "osmo.outseta.com",
    "outseta.on(",
    "postlogoutredirect",
    "authenticationcallbackurl",
    "location.pathname.replace(/\\/+$/,'') === '/no-access'",
    'location.pathname.replace(/\\/+$/,"" ) === "/no-access"',
)
for script in list(soup.find_all("script")):
    src = str(script.get("src", "")).lower()
    body = script.get_text(" ", strip=False).lower()
    if "outseta.com" in src or any(marker in body for marker in stale_script_markers):
        script.decompose()

# Remove inert Outseta nocode attributes while preserving all styling hooks.
for tag in soup.find_all(True):
    for attr in list(tag.attrs):
        key = str(attr).lower()
        if key.startswith("data-o-") or "outseta" in key:
            del tag.attrs[attr]

# 2) Repair every residual source-site/root-relative route.
route_map = {
    "/": PROJECT,
    "/login": BEHANCE,
    "/plans": GITHUB,
    "/showcase": "#build",
    "/collection": "#evidence",
    "/try": BEHANCE,
    "/updates": "#project",
    "/faq": "#research",
    "/legal/licensing-agreement": GITHUB,
    "/legal/terms-and-conditions": "#research",
    "/legal/privacy-policy": BEHANCE,
    "/legal/cookie-policy": "#evidence",
    "/product/vault": "#system",
    "/product/page-transition-course": "#architecture",
    "/product/button-pack": "#build",
    "/product/community": "#build",
    "/product/icons": "#build",
}

label_routes = {
    "story": "#project",
    "overview": "#project",
    "architecture": "#architecture",
    "groove band": "#build",
    "green grooves": "#build",
    "g/g app": "#build",
    "build gallery": "#build",
    "evidence": "#evidence",
    "roadmap": "#research",
    "research": "#research",
    "system overview": "#system",
    "identity": "#system",
    "shelf events": "#architecture",
    "association": "#architecture",
    "reversibility": "#architecture",
    "live cart": "#system",
    "settlement": "#system",
    "view project": BEHANCE,
    "open source": GITHUB,
    "source": GITHUB,
}

original_people_domains = (
    "dennissnellenberg.com",
    "iljavaneck.com",
    "instagram.com/by.ilja",
    "instagram.com/osmo",
    "linkedin.com/company/osmosupply",
    "twitter.com/osmosupply",
    "x.com/osmosupply",
    "join.slack.com/t/osmo-headquarters",
)


def normalized_label(a) -> str:
    return " ".join(a.stripped_strings).strip().lower()


def label_destination(label: str) -> str | None:
    if label in label_routes:
        return label_routes[label]
    for key, dest in label_routes.items():
        if key and key in label:
            return dest
    return None


for a in soup.find_all("a", href=True):
    raw = str(a.get("href", "")).strip()
    label = normalized_label(a)
    low = raw.lower()
    dest = None

    if not raw or low.startswith("javascript:"):
        dest = label_destination(label) or "#project"
    elif raw == "#":
        dest = label_destination(label) or "#project"
    elif low.startswith("/resource/") or low.startswith("/preview/") or low.startswith("/no-access") or low.startswith("/logged-out") or low.startswith("/onboarding"):
        dest = label_destination(label) or "#build"
    elif raw.startswith("/"):
        clean_path = urlparse(raw).path.rstrip("/") or "/"
        dest = route_map.get(clean_path) or label_destination(label) or "#project"
    elif any(domain in low for domain in original_people_domains):
        dest = label_destination(label) or (GITHUB if "ilja" in low or "github" in label else BEHANCE)
    elif "osmo.supply" in low:
        parsed = urlparse(raw)
        clean_path = parsed.path.rstrip("/") or "/"
        dest = route_map.get(clean_path) or label_destination(label) or "#project"
    else:
        parsed = urlparse(raw)
        if parsed.scheme in {"http", "https"} and parsed.netloc.lower() == PROJECT_HOST:
            p = parsed.path.rstrip("/") or "/"
            if p.startswith("/resource/") or p.startswith("/preview/"):
                dest = label_destination(label) or "#build"
            elif not (p == "/greengroove" or p.startswith("/greengroove/")):
                dest = route_map.get(p) or label_destination(label) or "#project"

    if dest:
        a["href"] = dest

    href = str(a.get("href", ""))
    parsed_final = urlparse(href)
    is_external = parsed_final.scheme in {"http", "https"} and parsed_final.netloc and parsed_final.netloc.lower() != PROJECT_HOST
    if is_external:
        a["target"] = "_blank"
        rel = set(a.get("rel") or [])
        rel.update({"noopener", "noreferrer"})
        a["rel"] = sorted(rel)
    elif parsed_final.netloc.lower() == PROJECT_HOST:
        a.attrs.pop("target", None)
        a.attrs.pop("rel", None)

# 3) Make the footer's existing update/source control honest and functional.
# Keep the exact form DOM and styling; only its behavior/semantics change.
footer = soup.find("footer")
if footer:
    form = footer.find("form")
    if form:
        form["action"] = GITHUB
        form["method"] = "get"
        form["target"] = "_blank"
        form["aria-label"] = "Open Green Groove source and project updates on GitHub"
        form["novalidate"] = "novalidate"
        email = form.find("input", attrs={"type": "email"})
        if email:
            email.attrs.pop("required", None)
            email.attrs.pop("name", None)
            email["autocomplete"] = "off"
            email["aria-label"] = "Project updates are published on GitHub"
            email["readonly"] = "readonly"
        submit = form.find("input", attrs={"type": "submit"})
        if submit:
            submit["aria-label"] = "Open Green Groove source on GitHub"

# 4) Empty source videos are intentionally static project-media surfaces. Mark them
# as such for accessibility/runtime code without changing their poster or geometry.
for video in soup.find_all("video"):
    has_src = bool(video.get("src")) or any(source.get("src") for source in video.find_all("source"))
    if not has_src:
        video["data-gg-static-media"] = "true"
        video["preload"] = "none"
        video["aria-hidden"] = "true"
        video["tabindex"] = "-1"
        video.attrs.pop("controls", None)

# 5) Add a tiny behavior guard for the existing footer form only. No visual DOM/CSS.
for old in list(soup.find_all("script", attrs={"id": "gg-production-behavior"})):
    old.decompose()
behavior = soup.new_tag("script", id="gg-production-behavior")
behavior.string = f"""
(() => {{
  const form = document.querySelector('footer form');
  if (form) {{
    form.addEventListener('submit', (event) => {{
      event.preventDefault();
      window.open('{GITHUB}', '_blank', 'noopener,noreferrer');
    }});
  }}
}})();
""".strip()
(soup.body or soup).append(behavior)

# 6) Production assertions: fail the build rather than publish known broken residue.
errors = []
ids = {tag.get("id") for tag in soup.find_all(id=True)}
for a in soup.find_all("a", href=True):
    href = str(a.get("href", "")).strip()
    low = href.lower()
    if not href or href == "#" or low.startswith("javascript:"):
        errors.append(f"non-destination link: {normalized_label(a)!r} -> {href!r}")
    if "osmo.supply" in low or "/resource/" in low or "sushxnthd.github.io/resource/" in low:
        errors.append(f"stale source route: {normalized_label(a)!r} -> {href!r}")
    if href.startswith("#") and href[1:] and href[1:] not in ids:
        errors.append(f"missing anchor target: {normalized_label(a)!r} -> {href!r}")

for script in soup.find_all("script"):
    src = str(script.get("src", "")).lower()
    body = script.get_text(" ", strip=False).lower()
    if "outseta.com" in src or "osmo.outseta.com" in body or "outseta.on(" in body:
        errors.append("stale Outseta runtime remains")

if errors:
    raise SystemExit("Production cleanup failed:\n- " + "\n- ".join(sorted(set(errors))))

path.write_text(str(soup), encoding="utf-8")
print("Production cleanup complete: behavior repaired without changing visible UI structure/content.")
