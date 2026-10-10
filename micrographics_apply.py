from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
import base64
import hashlib
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
soup = BeautifulSoup(path.read_text(encoding='utf8'), 'html.parser')

GREEN = (120, 255, 69)
GREEN_DARK = (3, 149, 68)
INK = (25, 25, 25)
PAPER = (246, 246, 242)
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_MONO_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def load_raster(parts, expected_sha256):
    encoded = ''.join(
        ''.join(Path(part).read_text(encoding='ascii').split())
        for part in parts
    )
    raw = base64.b64decode(encoded, validate=True)
    actual = hashlib.sha256(raw).hexdigest()
    assert actual == expected_sha256, (actual, expected_sha256)
    return Image.open(BytesIO(raw)).convert('RGB')


def webp_uri(im):
    out = BytesIO()
    im.save(out, format='WEBP', quality=92, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(out.getvalue()).decode('ascii')


def scale_box(box, sx, sy):
    x0, y0, x1, y1 = box
    return (round(x0*sx), round(y0*sy), round(x1*sx), round(y1*sy))


def recolor_non_background(im, box, light_color, dark_color, threshold, invert=False):
    crop = im.crop(box)
    arr = np.asarray(crop).copy().astype(np.float32)
    gray = arr.mean(axis=2)
    if invert:
        mask = gray > threshold
        shade = np.clip((gray-threshold)/(255-threshold), 0, 1)
    else:
        mask = gray < threshold
        shade = np.clip((gray-20)/220, 0, 1)
    target = np.zeros_like(arr)
    target[...,0] = dark_color[0]*(1-shade) + light_color[0]*shade
    target[...,1] = dark_color[1]*(1-shade) + light_color[1]*shade
    target[...,2] = dark_color[2]*(1-shade) + light_color[2]*shade
    arr[mask] = target[mask]
    im.paste(Image.fromarray(np.clip(arr,0,255).astype(np.uint8)), box)


def make_light(base):
    # Preserve the approved image composition and only edit copy/color regions.
    im = base.copy()
    W,H = im.size
    sx,sy = W/1448, H/1086
    d = ImageDraw.Draw(im)

    # Sample the clean paper background instead of repainting the whole asset.
    sample = np.asarray(im.crop(scale_box((0,0,1448,250),sx,sy))).reshape(-1,3)
    bg = tuple(sample.mean(axis=0).astype(int))

    # Remove only the old copy. Wordmark, cube, star and original whitespace remain.
    for rect in [
        (828,350,1080,480),
        (165,540,900,615),
        (165,615,440,690),
        (555,610,930,700),
    ]:
        d.rectangle(scale_box(rect,sx,sy), fill=bg)

    # Recolor the existing cube/star rather than redrawing them.
    recolor_non_background(
        im, scale_box((645,345,825,530),sx,sy), GREEN, GREEN_DARK, 242, invert=False
    )
    star_box = scale_box((440,615,565,745),sx,sy)
    star = np.asarray(im.crop(star_box)).copy()
    mask = star.mean(axis=2) < 135
    star[mask] = GREEN
    im.paste(Image.fromarray(star), star_box)

    d = ImageDraw.Draw(im)
    # Keep the same typographic zones/hierarchy as the approved graphic.
    d.text((round(838*sx),round(362*sy)), 'RFID BANDS', font=font(FONT_MONO, round(31*sy)), fill=INK)
    d.text((round(838*sx),round(408*sy)), 'SMART SHELVES', font=font(FONT_MONO, round(31*sy)), fill=GREEN_DARK)

    d.text((round(175*sx),round(548*sy)), 'SENSE', font=font(FONT_MONO, round(31*sy)), fill=INK)
    d.text((round(315*sx),round(548*sy)), '>>>', font=font(FONT_MONO_BOLD, round(31*sy)), fill=GREEN_DARK)
    d.text((round(400*sx),round(548*sy)), 'ATTRIBUTE', font=font(FONT_MONO, round(31*sy)), fill=INK)

    d.text((round(175*sx),round(622*sy)), 'LIVE CARTS', font=font(FONT_MONO, round(31*sy)), fill=INK)
    d.text((round(575*sx),round(622*sy)), 'AUTO BILLING', font=font(FONT_MONO, round(31*sy)), fill=INK)
    d.text((round(775*sx),round(668*sy)), 'QUEUE-FREE', font=font(FONT_MONO, round(17*sy)), fill=GREEN_DARK)
    return im


def make_dark(base):
    # Preserve the approved dark banner, including its original texture and proportions.
    im = base.copy()
    W,H = im.size
    sx,sy = W/2048, H/682
    arr = np.asarray(im)

    # Reconstruct cleared copy areas using the banner's own untouched top texture.
    top = arr[round(20*sy):round(160*sy),:,:]
    profile = top.mean(axis=0).astype(np.uint8)
    bgtex = Image.fromarray(np.tile(profile[None,:,:], (H,1,1)))
    def clear(rect):
        box = scale_box(rect,sx,sy)
        im.paste(bgtex.crop(box), box)

    clear((100,175,1950,300))
    clear((395,295,1950,410))
    clear((450,415,1160,505))

    # Keep the original cube/icon/badge geometry; only recolor it.
    recolor_non_background(
        im, scale_box((270,295,390,410),sx,sy), GREEN, GREEN_DARK, 110, invert=True
    )
    icon_box = scale_box((1030,295,1170,415),sx,sy)
    icon = np.asarray(im.crop(icon_box)).copy()
    mask = icon.mean(axis=2) > 145
    icon[mask] = GREEN
    im.paste(Image.fromarray(icon), icon_box)

    badge_box = scale_box((1150,405,1630,510),sx,sy)
    badge = np.asarray(im.crop(badge_box)).copy()
    mask = badge.mean(axis=2) > 135
    badge[mask] = GREEN
    im.paste(Image.fromarray(badge), badge_box)

    d = ImageDraw.Draw(im)
    d.text((round(120*sx),round(188*sy)), 'RFID BANDS', font=font(FONT_BOLD, round(72*sy)), fill=PAPER)
    d.text((round(800*sx),round(188*sy)), 'SMART SHELVES', font=font(FONT_BOLD, round(72*sy)), fill=PAPER)

    d.text((round(435*sx),round(305*sy)), 'LIVE CARTS', font=font(FONT_BOLD, round(64*sy)), fill=PAPER)
    d.text((round(1160*sx),round(305*sy)), 'QUEUE-FREE CHECKOUT', font=font(FONT_BOLD, round(58*sy)), fill=PAPER)

    d.text((round(470*sx),round(430*sy)), 'SENSE', font=font(FONT_MONO, round(29*sy)), fill=PAPER)
    d.text((round(615*sx),round(430*sy)), '+', font=font(FONT_MONO, round(29*sy)), fill=GREEN)
    d.text((round(665*sx),round(430*sy)), 'ATTRIBUTE', font=font(FONT_MONO, round(29*sy)), fill=PAPER)
    d.text((round(885*sx),round(430*sy)), '+', font=font(FONT_MONO, round(29*sy)), fill=GREEN)
    d.text((round(935*sx),round(430*sy)), 'BILL', font=font(FONT_MONO, round(29*sy)), fill=PAPER)
    return im


# Canonical bases are the two user-approved raster graphics from the previous pass.
light_base = load_raster(
    ['assets/raster/light.part1.b64','assets/raster/light.part2.b64'],
    '38d61d0eba9e8346a11c852b5faa2e132e5c4b6b12c9714998a78fc94e233482',
)
dark_base = load_raster(
    ['assets/raster/dark.part1.b64','assets/raster/dark.part2.b64','assets/raster/dark.part3.b64'],
    '69faf7b63d83a0b2bd1f489ccc55435c21e1013740aa9978fb07f6a247aad718',
)

light_uri = webp_uri(make_light(light_base))
dark_uri = webp_uri(make_dark(dark_base))

targets = {
    'osmo-micrographic-2.avif': light_uri,
    'osmo-micrographic-3.avif': dark_uri,
}
counts = {key: 0 for key in targets}
for img in soup.find_all('img'):
    src = img.get('src','')
    for needle,replacement in targets.items():
        if needle in src:
            img['src'] = replacement
            img.attrs.pop('srcset', None)
            img.attrs.pop('sizes', None)
            counts[needle] += 1

assert counts == {'osmo-micrographic-2.avif':1,'osmo-micrographic-3.avif':1}, counts
path.write_text(str(soup), encoding='utf8')
print('Edited the approved raster micrographics in-place:', counts)
