from bs4 import BeautifulSoup
from pathlib import Path
import base64
import hashlib
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
original_html = path.read_text(encoding='utf-8')
soup = BeautifulSoup(original_html, 'html.parser')


def avif_data_uri(parts, expected_sha256):
    encoded = ''.join(
        ''.join(Path(part).read_text(encoding='ascii').split())
        for part in parts
    )
    raw = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, (actual, expected_sha256)
    return 'data:image/avif;base64,' + encoded


def avif_file_data_uri(file_path, expected_sha256):
    raw = Path(file_path).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, (actual, expected_sha256)
    return 'data:image/avif;base64,' + base64.b64encode(raw).decode('ascii')


# Canonical user-supplied Green Groove graphics, web-optimized while preserving transparency.
light_uri = avif_data_uri(
    [f'assets/uploads/v3-light-{i:02d}.b64' for i in range(1, 8)],
    '42dfc66b859816c85bed92a7e3d5c805ae3b631d5f6ee142aa1cc5ee4406c3f2',
)
dark_uri = avif_data_uri(
    [f'assets/uploads/v3-dark-{i:02d}.b64' for i in range(1, 8)],
    'd604f1945c7cde8c5cb8a19ba6ab8381ba4779bbadeffafec55c9d3b34f34fc3',
)
notes_uri = avif_data_uri(
    [
        'assets/uploads/v4-notes-01a.b64',
        'assets/uploads/v4-notes-01b.b64',
        'assets/uploads/v4-notes-01c.b64',
        'assets/uploads/v4-notes-02.b64',
        'assets/uploads/v4-notes-03.b64',
        'assets/uploads/v4-notes-04.b64',
    ],
    '78b35c12d36b4de9fca6474a4a5d32d3debd541d677ae9cfa76d900953b1cf84',
)

targets = {
    'osmo-micrographic-1.avif': notes_uri,
    'osmo-micrographic-2.avif': light_uri,
    'osmo-micrographic-3.avif': dark_uri,
}
counts = {key: 0 for key in targets}

# Normal img sources: preserve every class, dimension and surrounding DOM node.
for img in soup.find_all('img'):
    src = img.get('src', '')
    for needle, replacement in targets.items():
        if needle in src:
            img['src'] = replacement
            img.attrs.pop('srcset', None)
            img.attrs.pop('sizes', None)
            counts[needle] += 1

assert counts == {
    'osmo-micrographic-1.avif': 1,
    'osmo-micrographic-2.avif': 1,
    'osmo-micrographic-3.avif': 1,
}, counts

# Final safeguard: source templates can carry the same image in picture/source,
# lazy-load attributes or inline markup. Remove any surviving Osmo micrographic
# reference without changing the UI structure around it.
rendered = str(soup)
for needle, replacement in targets.items():
    full_url = 'https://osmo.b-cdn.net/website/bandwidth/' + needle
    rendered = rendered.replace(full_url, replacement)
    assert needle not in rendered, f'Stale Osmo micrographic survived build: {needle}'

path.write_text(rendered, encoding='utf-8')
print('Installed canonical supplied Green Groove micrographics:', counts)
