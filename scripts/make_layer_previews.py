"""Original product-preview compositions for the six native Osmo card slots.

These are conceptual system illustrations, never screenshots of shipped software.
The 1000x1300 artboards leave the source card's text area clear.
"""
from pathlib import Path
import sys

out=Path('assets/visuals/layer-previews');out.mkdir(parents=True,exist_ok=True)
INK='#202722';GREEN='#78ff45';BLUE='#18bdf2';PAPER='#f4f1e8'
def svg(key,title,body):
 height,view=(625,'0 575 1000 625') if key=='shelf' else (1300,'0 0 1000 1300')
 (out/f'{key}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="{view}"><title>{title} — conceptual product preview</title><defs><filter id="shadow" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="16" stdDeviation="16" flood-opacity=".22"/></filter></defs>{body}</svg>')
def panel(x,y,w,h,fill,body,rotate=0):
 return f'<g transform="translate({x} {y}) rotate({rotate} {w/2} {h/2})" filter="url(#shadow)"><rect width="{w}" height="{h}" rx="24" fill="{fill}" stroke="#667268" stroke-opacity=".35" stroke-width="3"/>{body}</g>'
def line(x,y,w,color='#89958b',sw=8):return f'<path d="M{x} {y}h{w}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
def band(cx,cy,scale=1,color=GREEN):
 return f'<g transform="translate({cx} {cy}) scale({scale})" stroke="{INK}" stroke-width="5"><ellipse rx="100" ry="67" fill="{color}"/><ellipse cy="-9" rx="66" ry="40" fill="#263c2c"/><path d="M-100 0v30c0 38 45 67 100 67s100-29 100-67V0c-9 39-49 67-100 67S-91 39-100 0Z" fill="{color}"/><rect x="-41" y="29" width="82" height="55" rx="14" fill="{INK}"/><rect x="-18" y="43" width="36" height="25" rx="5" fill="#c4ffad" stroke="none"/></g>'
def package(x,y,fill=BLUE):
 return f'<g transform="translate({x} {y})" stroke="{INK}" stroke-width="3" stroke-linejoin="round"><path d="M0 24 20 0h43l22 24v103H0Z" fill="{PAPER}"/><path d="M0 24h85M20 0v24m43-24v24" fill="none"/><path d="M0 59h85v40H0Z" fill="{fill}" stroke="none"/></g>'

batch=int(sys.argv[1]) if len(sys.argv)>1 else 0
if batch in (0,1):
 # A module study alongside a layered session card; no invented shopper data.
 svg('identity','RFID identity',panel(140,840,740,390,'#28342d',
  '<rect x="28" y="27" width="100" height="12" rx="6" fill="#87958b"/>'+band(225,181,1.2)+
  '<rect x="435" y="105" width="240" height="170" rx="18" fill="#1b241e"/>'+
  '<rect x="462" y="133" width="57" height="45" rx="10" fill="#78ff45"/>'+line(462,209,145)+line(462,233,99),-7))
 # The oval preview follows the source course-preview slot, with physical shelf sensing.
 svg('shelf','Shelf sensing',f'<g transform="translate(40 350) scale(1.5)"><path d="m70 350 420-45 100 62-420 48Z" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'+package(130,205)+package(267,190,GREEN)+package(402,175,'#e6ad70')+f'<path d="m70 350 100 65 420-48v26l-420 48-100-65Z" fill="#98ae9e" stroke="{INK}" stroke-width="4"/><rect x="265" y="411" width="150" height="40" rx="7" fill="{BLUE}" stroke="{INK}" stroke-width="4"/><circle cx="288" cy="431" r="6" fill="{INK}"/><circle cx="390" cy="431" r="6" fill="{INK}"/></g>')
 # Staggered physical event tiles, rather than another single line icon.
 tiles=''
 for x,y,angle,c in [(70,960,-12,'#53645b'),(365,845,0,'#f4f1e8'),(660,950,12,'#53645b')]:
  subject=package(93,36,GREEN) if c==PAPER else band(135,110,.72,'#809b86')
  tiles+=panel(x,y,270,310,c,subject+f'<path d="M80 225h110" stroke="{INK if c==PAPER else PAPER}" stroke-width="9" stroke-linecap="round"/><circle cx="135" cy="270" r="12" fill="{GREEN}"/>',angle)
 svg('association','Event association',tiles)
if batch in (0,2):
 # Reversibility is a pair of inverse event surfaces connected by a return curve.
 svg('return','Reversible events',panel(170,860,630,185,PAPER,
  '<circle cx="80" cy="92" r="38" fill="#78ff45"/><path d="M60 92h40m-20-20v40" stroke="#202722" stroke-width="7"/>'+line(155,75,320)+line(155,110,220),-8)+
  panel(235,1060,630,185,'#28342d','<circle cx="80" cy="92" r="38" fill="#18bdf2"/><path d="m88 75-18 17 18 17m-18-17h37" fill="none" stroke="#202722" stroke-width="7"/>'+line(155,75,320)+line(155,110,220),5))
 # A basket preview with item rows; a diagram, without fabricated transaction data.
 rows=''
 for y,c in [(160,GREEN),(250,BLUE),(340,'#d6b38b')]:
  rows+=f'<rect x="40" y="{y}" width="520" height="72" rx="12" fill="#25382b"/><rect x="58" y="{y+16}" width="40" height="40" rx="8" fill="{c}"/>'+line(125,y+27,230)+line(125,y+48,150,'#617969',5)+f'<circle cx="510" cy="{y+36}" r="13" fill="{c}"/>'
 svg('cart','Live cart',panel(195,800,610,510,'#17271e','<path d="m45 45 9 48h105l15-48H45Zm-9-12h7m27 21v26m30-26v26m30-26v26" fill="none" stroke="#78ff45" stroke-width="6"/>'+line(218,67,300,PAPER,14)+rows,-5))
 # A receipt slides out of a solid device, mirroring source product-object treatment.
 svg('settlement','Final invoice',panel(195,1045,620,230,'#243d31',
  '<rect x="45" y="45" width="530" height="24" rx="12" fill="#15241c"/><circle cx="550" cy="150" r="13" fill="#78ff45"/>',-7)+
  '<g transform="translate(295 820) rotate(-7 190 200)" filter="url(#shadow)"><path d="M0 0h390v350l-20-12-19 12-20-12-19 12-20-12-19 12-20-12-19 12-20-12-19 12-20-12-19 12-20-12-19 12-20-12-19 12-20-12-19 12V0Z" fill="#f4f1e8"/>'+line(42,55,190,INK,12)+line(42,112,250)+line(42,150,280)+line(42,188,230)+line(42,250,300,INK,12)+'</g>')
print('Layer-preview batch',batch or 'all')
