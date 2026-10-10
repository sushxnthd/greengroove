from bs4 import BeautifulSoup
from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
s = BeautifulSoup(path.read_text(encoding='utf8'), 'html.parser')
BEHANCE = 'https://www.behance.net/gallery/211169339/Green-Groove'
GITHUB = 'https://github.com/sushxnthd/greengroove'
OG = 'https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/09cb22211169339.67245eac9212c.png'

# Shorter, clearer top-level actions while preserving the exact Osmo button footprints.
for node in list(s.find_all(string=True)):
    if not node.parent or node.parent.name in {'script', 'style', 'title'} or node.find_parent('svg'):
        continue
    value = ' '.join(str(node).split())
    if value == 'Study':
        node.replace_with('Story')

# Tailor the large menu feature card instead of leaving a Page Transition Course artifact.
banner = s.select_one('.nav-banner')
if banner:
    tags = banner.select('.nav-banner__tags .eyebrow')
    if tags:
        tags[0].string = 'System'
    if len(tags) > 1:
        tags[1].string = 'Map'
    title = banner.select_one('.nav-banner__title h2')
    if title:
        title.string = 'Architecture'
    image = banner.select_one('.nav-banner__ptc-preview img.cover-image')
    if image:
        image['src'] = OG
        image['alt'] = 'Green Groove retail-state system architecture'
    video = banner.select_one('.nav-banner__ptc-preview video')
    if video:
        video.attrs.pop('data-video-src', None)
        video.attrs.pop('src', None)
        video['poster'] = OG

# Osmo populates this number from its CMS. Freeze the identical source counter to Green Groove's six layers.
for count in s.select('[data-vault-total]'):
    count.attrs.pop('data-vault-total', None)
    count.string = '06'

# Repair the last semantic leftovers without changing any wrappers/classes/animation hooks.
for a in s.find_all('a', href=True):
    label = ' '.join(a.stripped_strings).strip()
    if label == 'Story':
        a['href'] = BEHANCE
    elif label == 'Source':
        a['href'] = GITHUB
    elif label == 'Contact':
        a['href'] = BEHANCE
    elif label == 'GitHub' and a.get('href') == BEHANCE:
        # This is the original privacy-policy text position, now used as the case-study destination.
        a.string = 'Behance'

# Source menu banner tags are nested, so generic text replacement cannot reliably reach them.
# Keep the exact two-pill composition but make their accessible text project-specific.
if banner:
    for old in ('START LEARNING', 'Start Learning', 'Start Exploring'):
        for node in list(banner.find_all(string=True)):
            if ' '.join(str(node).split()) == old:
                node.replace_with('System Map')

path.write_text(str(s), encoding='utf8')
print('Applied Green Groove micro-tailoring with zero geometry changes.')
