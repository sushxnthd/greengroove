from bs4 import BeautifulSoup
from pathlib import Path
import base64
import hashlib
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')


def avif_data_uri(parts, expected_sha256):
    encoded = ''.join(
        ''.join(Path(part).read_text(encoding='ascii').split())
        for part in parts
    )
    raw = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, (actual, expected_sha256)
    return 'data:image/avif;base64,' + encoded


# Canonical user-supplied Green Groove graphics, web-optimized while preserving transparency.
light_uri = avif_data_uri(
    [f'assets/uploads/v3-light-{i:02d}.b64' for i in range(1, 8)],
    '42dfc66b859816c85bed92a7e3d5c805ae3b631d5f6ee142aa1cc5ee4406c3f2',
)
dark_uri = avif_data_uri(
    [f'assets/uploads/v3-dark-{i:02d}.b64' for i in range(1, 8)],
    'd604f1945c7cde8c5cb8a19ba6ab8381ba4779bbadeffafec55c9d3b34f34fc3',
)

targets = {
    'osmo-micrographic-2.avif': light_uri,
    'osmo-micrographic-3.avif': dark_uri,
}
counts = {key: 0 for key in targets}

for img in soup.find_all('img'):
    src = img.get('src', '')
    for needle, replacement in targets.items():
        if needle in src:
            img['src'] = replacement
            img.attrs.pop('srcset', None)
            img.attrs.pop('sizes', None)
            counts[needle] += 1

assert counts == {
    'osmo-micrographic-2.avif': 1,
    'osmo-micrographic-3.avif': 1,
}, counts

path.write_text(str(soup), encoding='utf-8')
print('Installed canonical supplied Green Groove micrographics:', counts)
