from bs4 import BeautifulSoup
from pathlib import Path
import base64
import hashlib
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")


def raster_uri(parts, expected_sha256):
    encoded = "".join(
        "".join(Path(part).read_text(encoding="ascii").split())
        for part in parts
    )
    raw = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, (actual, expected_sha256)
    return "data:image/webp;base64," + encoded


# These are raster derivatives of the two user-approved rendered graphics.
# They are intentionally NOT traced/rebuilt as SVGs: the raster appearance is canonical.
light_uri = raster_uri(
    [
        "assets/raster/light.part1.b64",
        "assets/raster/light.part2.b64",
    ],
    "38d61d0eba9e8346a11c852b5faa2e132e5c4b6b12c9714998a78fc94e233482",
)

dark_uri = raster_uri(
    [
        "assets/raster/dark.part1.b64",
        "assets/raster/dark.part2.b64",
        "assets/raster/dark.part3.b64",
    ],
    "69faf7b63d83a0b2bd1f489ccc55435c21e1013740aa9978fb07f6a247aad718",
)

targets = {
    "osmo-micrographic-2.avif": light_uri,
    "osmo-micrographic-3.avif": dark_uri,
}
counts = {key: 0 for key in targets}

for img in soup.find_all("img"):
    src = img.get("src", "")
    for needle, replacement in targets.items():
        if needle in src:
            img["src"] = replacement
            img.attrs.pop("srcset", None)
            img.attrs.pop("sizes", None)
            counts[needle] += 1

assert counts == {
    "osmo-micrographic-2.avif": 1,
    "osmo-micrographic-3.avif": 1,
}, counts

path.write_text(str(soup), encoding="utf8")
print(
    "Installed approved raster Green Groove micrographics: "
    f"light={counts['osmo-micrographic-2.avif']}, "
    f"dark={counts['osmo-micrographic-3.avif']}"
)
