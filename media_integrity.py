from pathlib import Path
import sys

from bs4 import BeautifulSoup

POSTER = "https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/09cb22211169339.67245eac9212c.png"
PLACEHOLDER_MARKERS = (
    "placeholder.60f9b1840c.svg",
    "/plugins/basic/assets/placeholder",
)

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

repaired_images = 0
repaired_videos = 0

# Replace only known Webflow placeholder artwork. Keep element/classes/geometry intact.
for img in soup.find_all("img"):
    src = str(img.get("src", ""))
    if any(marker in src.lower() for marker in PLACEHOLDER_MARKERS):
        img["src"] = POSTER
        repaired_images += 1

# Empty retained source-video shells must still render a complete project surface.
# Supplying a poster fixes blank/broken media without touching sizing or wrappers.
for video in soup.find_all("video"):
    has_src = bool(str(video.get("src", "")).strip()) or any(str(s.get("src", "")).strip() for s in video.find_all("source"))
    if not has_src and not str(video.get("poster", "")).strip():
        video["poster"] = POSTER
        repaired_videos += 1

path.write_text(str(soup), encoding="utf-8")
print(f"Media integrity repaired: {repaired_images} placeholder image(s), {repaired_videos} empty video poster(s).")
