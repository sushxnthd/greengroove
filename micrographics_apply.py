from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
import base64
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
soup = BeautifulSoup(path.read_text(encoding='utf8'), 'html.parser')

BG_LIGHT = '#F4F4EF'
BG_DARK = '#1E1E1E'
INK = '#1E1E1E'
PAPER = '#F4F4EF'
GREEN = '#78FF45'
GREEN_DARK = '#039544'

FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_star(draw, cx, cy, radius, color, width):
    import math
    for ang in (0, 45, 90, 135):
        a = math.radians(ang)
        dx, dy = math.cos(a) * radius, math.sin(a) * radius
        draw.line((cx-dx, cy-dy, cx+dx, cy+dy), fill=color, width=width)


def draw_cube(im, x, y, size):
    d = ImageDraw.Draw(im)
    depth = int(size * 0.18)
    d.rectangle((x, y+depth, x+size-depth, y+size), fill=GREEN)
    d.polygon([(x, y+depth), (x+depth, y), (x+size, y), (x+size-depth, y+depth)], fill='#66EF3F')
    d.polygon([(x+size-depth, y+depth), (x+size, y), (x+size, y+size-depth), (x+size-depth, y+size)], fill='#00B84C')
    glow = Image.new('RGBA', im.size, (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle((x+depth//2, y, x+size-depth//2, y+depth*2), fill=(255,255,255,70))
    glow = glow.filter(ImageFilter.GaussianBlur(max(2, depth//3)))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    d.text((x+size*0.68, y+depth+8), '/01', font=font(FONT_REG, max(10, int(size*0.055))), fill=INK)
    label_font = font(FONT_BOLD, max(12, int(size*0.085)))
    d.text((x+size*0.07, y+size*0.73), 'GREEN', font=label_font, fill=INK)
    d.text((x+size*0.07, y+size*0.81), 'GROOVE', font=label_font, fill=INK)


def text_fit(draw, xy, text, max_width, font_path, start_size, min_size, fill):
    size = start_size
    while size > min_size:
        f = font(font_path, size)
        box = draw.textbbox((0,0), text, font=f)
        if box[2]-box[0] <= max_width:
            draw.text(xy, text, font=f, fill=fill)
            return f
        size -= 2
    f = font(font_path, min_size)
    draw.text(xy, text, font=f, fill=fill)
    return f


def make_light():
    W,H = 1448,1086
    im = Image.new('RGBA', (W,H), BG_LIGHT)
    d = ImageDraw.Draw(im)
    d.text((165,340), 'GREEN', font=font(FONT_BOLD, 92), fill=INK)
    d.text((165,420), 'GROOVE', font=font(FONT_BOLD, 92), fill=INK)
    draw_cube(im, 635, 330, 220)
    d.text((870,355), 'RFID BANDS', font=font(FONT_MONO, 38), fill=INK)
    d.text((870,410), 'SMART SHELVES', font=font(FONT_MONO, 38), fill=INK)
    d.text((870,475), 'SENSE  >  ATTRIBUTE  >  BILL', font=font(FONT_MONO, 21), fill=GREEN_DARK)
    d.text((175,555), 'LIVE CARTS   >>>   AUTO BILLING', font=font(FONT_MONO, 31), fill=INK)
    d.text((175,635), 'QUEUE-FREE', font=font(FONT_MONO, 31), fill=INK)
    draw_star(d, 490, 660, 42, GREEN, 6)
    d.text((555,635), 'CHECKOUT', font=font(FONT_MONO, 31), fill=INK)
    return im


def make_dark():
    W,H = 2048,682
    im = Image.new('RGBA', (W,H), BG_DARK)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 4):
        if (x//4) % 2 == 0:
            d.line((x,0,x,H), fill='#202120')
    d.text((120,190), 'RFID BANDS', font=font(FONT_BOLD, 82), fill=PAPER)
    d.text((735,190), 'SMART SHELVES', font=font(FONT_BOLD, 82), fill=GREEN)
    draw_cube(im, 255, 315, 112)
    d.text((410,320), 'LIVE CARTS', font=font(FONT_BOLD, 62), fill=PAPER)
    draw_star(d, 1035, 365, 38, GREEN, 7)
    text_fit(d, (1120,320), 'QUEUE-FREE CHECKOUT', 800, FONT_BOLD, 62, 48, PAPER)
    d.text((470,500), 'SENSE + ATTRIBUTE + BILL', font=font(FONT_MONO, 34), fill=PAPER)
    pill = (1220,485,1740,557)
    d.rounded_rectangle(pill, radius=36, outline=GREEN, width=4)
    d.text((1295,500), 'GREEN GROOVE', font=font(FONT_BOLD, 36), fill=GREEN)
    return im


def webp_uri(im):
    out = BytesIO()
    im.convert('RGB').save(out, format='WEBP', quality=90, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(out.getvalue()).decode('ascii')

light_uri = webp_uri(make_light())
dark_uri = webp_uri(make_dark())

targets = {
    'osmo-micrographic-2.avif': light_uri,
    'osmo-micrographic-3.avif': dark_uri,
}
counts = {k:0 for k in targets}
for img in soup.find_all('img'):
    src = img.get('src','')
    for needle,replacement in targets.items():
        if needle in src:
            img['src'] = replacement
            img.attrs.pop('srcset', None)
            img.attrs.pop('sizes', None)
            counts[needle] += 1

assert counts == {'osmo-micrographic-2.avif':1, 'osmo-micrographic-3.avif':1}, counts
path.write_text(str(soup), encoding='utf8')
print('Installed project-specific raster GreenGroove micrographics:', counts)
