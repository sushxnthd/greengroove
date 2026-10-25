"""Code-native concept illustrations: one clear object/action per carousel card."""
from pathlib import Path
out=Path('assets/visuals/illustrations');out.mkdir(parents=True,exist_ok=True)
INK='#202722';GREEN='#78ff45';BLUE='#18bdf2';CREAM='#f4f1e8'
def write(key,title,bg,body):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400" role="img" aria-labelledby="title"><title id="title">{title}</title><rect width="600" height="400" fill="{bg}"/><g stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>'''
 (out/f'{key}.svg').write_text(svg)
# Thesis: the RFID module is the focal point of a recognisable closed wristband.
write('identity','Illustration: a closed RFID wristband with an embedded identity module','#e9ded0','''
<ellipse cx="300" cy="316" rx="170" ry="24" fill="#c8baaa" stroke="none"/>
<path d="M139 188c0-73 72-126 161-126s161 53 161 126v49c0 68-72 120-161 120s-161-52-161-120Z" fill="#2f6546"/>
<ellipse cx="300" cy="188" rx="161" ry="126" fill="#78ff45"/>
<ellipse cx="300" cy="182" rx="112" ry="79" fill="#e9ded0"/>
<path d="M188 182v30c8-43 53-70 112-70s104 27 112 70v-30c0-44-50-79-112-79s-112 35-112 79Z" fill="#458858"/>
<path d="M139 216c19 67 86 103 161 103s142-36 161-103" fill="none" stroke="#97ff73" stroke-width="3"/>
<g transform="translate(300 266) rotate(-6)"><rect x="-60" y="-39" width="120" height="78" rx="22" fill="#202722"/><rect x="-28" y="-21" width="56" height="42" rx="10" fill="#c4ffad"/><path d="M-41-11q-13 11 0 22m82-22q13 11 0 22" fill="none" stroke="#c4ffad" stroke-width="3"/><path d="M-13-8h26v16h-26z" fill="none" stroke-width="2"/></g>
<path d="M489 87q27 24 25 55m-45-40q17 16 16 35" fill="none" stroke="#237a59" stroke-width="6"/>
''')
# Thesis: shelf sensing lives beneath physical products, not inside an abstract diagram.
write('shelf','Illustration: a sensor-equipped shelf with product packages','#dbe8ec','''
<path d="m102 248 326-57 85 60-325 62Z" fill="#fcfbf4"/><path d="m188 313 325-62v24l-325 62-86-64v-25Z" fill="#91a6a9"/><path d="m188 313 325-62" fill="none"/>
<path d="m146 326 64 38 267-51-63-34Z" fill="#202722"/><rect x="255" y="301" width="61" height="34" rx="5" transform="rotate(-11 285 318)" fill="#18bdf2"/><circle cx="272" cy="319" r="5" fill="#202722"/><circle cx="301" cy="313" r="5" fill="#202722"/>
<path d="m153 150 54-11 42 30-54 11Z" fill="#c8dda5"/><path d="m153 150 42 30v100l-42-29Z" fill="#69a66a"/><path d="m195 180 54-11v99l-54 12Z" fill="#a9d080"/><path d="m161 183 25 17m-25-3 25 17" stroke="#f5f3db"/>
<path d="m275 115 56-10 42 30-56 11Z" fill="#ffe0b0"/><path d="m275 115 42 31v101l-42-30Z" fill="#d49d61"/><path d="m317 146 56-11v101l-56 11Z" fill="#f7c388"/><path d="m326 175 31-6m-31 19 31-6m-31 19 18-3" stroke="#202722"/>
<path d="m393 174 42-8 28 22-42 8Z" fill="#fffef2"/><path d="m393 174 28 22v57l-28-21Z" fill="#8ca5bd"/><path d="m421 196 42-8v56l-42 9Z" fill="#bfd3e1"/>
<path d="m283 278 2 13m-21-10 2 13m37-21 2 13" fill="none" stroke="#237a59"/>
<path d="m495 112 12-5m-10 24 16 2m-26-36 6-12" fill="none" stroke="#237a59" stroke-width="5"/>
''')
# Thesis: a returned carton reverses a pick, with the reverse movement readable at a glance.
write('return','Illustration: a milk carton returning to the shelf','#eee6f0','''
<path d="M93 310h417v35H93z" fill="#c3becb"/><path d="M93 310 151 279h358v31Z" fill="#fffdf6"/>
<ellipse cx="336" cy="287" rx="104" ry="21" fill="#b3b2bc" stroke="none" opacity=".4"/>
<g transform="translate(279 95) rotate(11 50 90)"><path d="m0 45 24-35h58l25 35v142H0Z" fill="#f9f7e9"/><path d="M0 45h107M24 10v35m58-35v35" fill="none"/><path d="M0 98h107v61H0z" fill="#18bdf2"/><path d="m24 10 30-17 28 17" fill="#e8e5d5"/><path d="M20 72h36" fill="none" stroke-width="7"/><path d="M29 129c0-17 25-31 25-31s25 14 25 31a25 25 0 0 1-50 0Z" fill="#effbfb" stroke="none"/></g>
<path d="M181 100c-72 21-88 102-36 149" fill="none" stroke="#237a59" stroke-width="20"/><path d="m118 235 40 32 13-50" fill="#237a59" stroke="none"/>
<path d="M411 264h66m-33-19v38" fill="none" stroke="#237a59" stroke-width="7"/>
''')
# Thesis: the live cart is a persistent basket on a phone, not a checkout scan.
write('cart','Illustration: a phone showing a live shopping basket','#242f2c','''
<ellipse cx="302" cy="350" rx="150" ry="17" fill="#101a16" stroke="none"/>
<g transform="rotate(-8 300 205)"><rect x="203" y="32" width="194" height="331" rx="32" fill="#8da096"/><rect x="212" y="38" width="175" height="313" rx="25" fill="#f5f3eb"/><path d="M264 45h71l-8 12h-55Z" fill="#202722"/>
<path d="m236 90 9 39h100l14-39Z" fill="#78ff45"/><path d="M230 79h10l5 11m18 0 5 39m22-39v39m23-39-5 39m-55 18h92" fill="none"/><circle cx="269" cy="148" r="5" fill="#202722"/><circle cx="330" cy="148" r="5" fill="#202722"/>
<rect x="232" y="173" width="135" height="56" rx="10" fill="#dedfd5" stroke="none"/><path d="m246 188 10-7 16 8v25h-26Z" fill="#18bdf2" stroke-width="2"/><path d="M290 191h50m-50 12h27" stroke-width="5"/>
<rect x="232" y="241" width="135" height="56" rx="10" fill="#dedfd5" stroke="none"/><path d="M249 257c-13 1-12 28 1 28 6 0 6-3 10 0 11 0 15-30 0-28-7 2-4 2-11 0Z" fill="#d5976f" stroke-width="2"/><path d="M290 258h50m-50 12h27M270 325h60" stroke-width="5"/></g>
<circle cx="418" cy="108" r="38" fill="#78ff45" stroke="none"/><path d="m401 109 11 12 23-27" fill="none" stroke-width="7"/>
''')
# Thesis: shelf events must resolve to one shopper's band rather than either nearby shopper.
write('association','Illustration: one item associated with the correct shopper band','#e6e5db','''
<path d="M48 304 233 197l175 97-186 107Z" fill="#d5d9c8" stroke="none"/>
<g transform="translate(100 106) rotate(-18)"><rect width="86" height="195" rx="40" fill="#376b52"/><rect x="9" y="28" width="68" height="137" rx="30" fill="#b6d2b0"/><rect x="-9" y="73" width="104" height="57" rx="19" fill="#78ff45"/><rect x="23" y="86" width="39" height="29" rx="8" fill="#202722"/></g>
<g transform="translate(426 80) rotate(23)"><rect width="86" height="195" rx="40" fill="#989ca5"/><rect x="9" y="28" width="68" height="137" rx="30" fill="#d8d9dd"/><rect x="-9" y="73" width="104" height="57" rx="19" fill="#c1bec8"/><rect x="23" y="86" width="39" height="29" rx="8" fill="#202722"/></g>
<path d="m257 174 49-28 47 28-48 28Z" fill="#ffe2ac"/><path d="m257 174 48 28v70l-48-27Z" fill="#c9925e"/><path d="m305 202 48-28v71l-48 27Z" fill="#e9ba7f"/>
<path d="M253 218c-55 0-40-69-98-69" fill="none" stroke="#237a59" stroke-width="9"/><path d="M358 218c35-4 38-34 53-36" fill="none" stroke="#8c9093" stroke-width="5" stroke-dasharray="6 13"/>
<circle cx="240" cy="111" r="25" fill="#237a59" stroke="none"/><path d="m228 111 8 9 17-19" fill="none" stroke="#f4f1e8" stroke-width="5"/>
''')
# Thesis: final checkout is an invoice of the cart's known state, not a payment claim.
write('settlement','Illustration: a receipt printer producing the basket invoice','#dfE9df','''
<ellipse cx="308" cy="337" rx="157" ry="18" fill="#b6c6b3" stroke="none"/>
<path d="m162 215 54-45h207l39 45v110H162Z" fill="#44584b"/><path d="M162 215h300v110H162Z" fill="#26362b"/><rect x="196" y="236" width="234" height="18" rx="8" fill="#111b15"/>
<path d="M219 246V52l19 10 19-10 19 10 19-10 19 10 19-10 19 10 19-10 20 10 18-10v194Z" fill="#fcfaf0"/>
<path d="M249 97h107M249 117h65M249 151h66m26 0h17m-109 24h66m26 0h17M249 204h109" fill="none" stroke-width="5"/>
<circle cx="426" cy="286" r="7" fill="#78ff45" stroke="none"/><path d="M185 309h48" stroke="#89a28e"/>
<circle cx="427" cy="111" r="37" fill="#78ff45" stroke="none"/><path d="m410 111 12 13 24-29" fill="none" stroke-width="7"/>
''')
# Thesis: event history preserves both picks and inverses as distinct records.
write('ledger','Illustration: a stack of pick, return and held event records','#e6ddd0','''
<path d="m151 244 233-47 82 69-232 51Z" fill="#c9bdad" stroke="none"/>
<g transform="translate(164 154) rotate(-13)"><path d="M0 0h267v109H0l11-17L0 75l11-17L0 41l11-20Z" fill="#c2cad2"/><path d="M73 31h144M73 51h117M73 72h82" stroke="#55616b"/><circle cx="39" cy="54" r="20" fill="#dcc08b"/><path d="M33 44v20m12-20v20" stroke-width="4"/></g>
<g transform="translate(149 112) rotate(-4)"><path d="M0 0h267v109H0l11-17L0 75l11-17L0 41l11-20Z" fill="#eef0e7"/><path d="M73 31h144M73 51h117M73 72h82" stroke="#839184"/><circle cx="39" cy="54" r="20" fill="#18bdf2"/><path d="m44 43-12 11 12 11m-11-11h19" fill="none" stroke-width="4"/></g>
<g transform="translate(156 66) rotate(7)"><path d="M0 0h267v109H0l11-17L0 75l11-17L0 41l11-20Z" fill="#fffaf0"/><path d="M73 31h144M73 51h117M73 72h82" stroke="#839184"/><circle cx="39" cy="54" r="20" fill="#78ff45"/><path d="M28 54h22m-11-11v22" stroke-width="4"/></g>
''')
# Thesis: validation means calibrating real sensing hardware against a known load.
write('validation','Illustration: a calibration weight on a load-cell test platform','#e0e4f0','''
<path d="m101 267 196-51 103 61-197 58Z" fill="#f9f6ec"/><path d="m101 267 102 68 197-58v22l-197 58-102-68Z" fill="#b3bccd"/>
<path d="m210 335 5 27 57-15v-26Z" fill="#18bdf2"/>
<path d="M237 236v-76c0-10 21-18 44-18s44 8 44 18v76c0 10-20 18-44 18s-44-8-44-18Z" fill="#74857f"/><ellipse cx="281" cy="160" rx="44" ry="17" fill="#c7d5c9"/><path d="M264 144v-20a17 17 0 0 1 34 0v20" fill="none" stroke-width="8"/>
<rect x="411" y="97" width="124" height="133" rx="14" fill="#2e4037"/><rect x="426" y="113" width="94" height="75" rx="5" fill="#10251a"/><path d="M438 161h13l9-17 12 35 12-26h23" fill="none" stroke="#78ff45" stroke-width="4"/><circle cx="449" cy="210" r="6" fill="#78ff45"/><circle cx="478" cy="210" r="6" fill="#b2c2b2"/>
<path d="M441 230v54q0 32-63 32h-31" fill="none" stroke-width="5"/><path d="m167 132-8-10m29-3v-14m-40 49h-14" stroke="#556f60"/>
''')
# Thesis: a product lifted from a shelf is one clear, reversible physical action.
write('interaction','Illustration: one carton picked up from a stocked shelf','#efdfd9','''
<ellipse cx="294" cy="347" rx="198" ry="18" fill="#d6bfb3" stroke="none"/>
<path d="m70 286 329-44 132 52-330 48Z" fill="#f4f1e8"/><path d="m70 286 131 56 330-48v24l-330 48-131-55Z" fill="#ac9383"/>
<g transform="translate(116 185)"><path d="m0 19 17-21 33-5 23 19v96l-49 8L0 99Z" fill="#a2b86d"/><path d="m0 19 24 16 49-7M24 35v81" fill="none"/><path d="m35 52 25-4v29l-25 4Z" fill="#e4eccd" stroke="none"/></g>
<g transform="translate(378 185)"><path d="m0 19 17-21 33-5 23 19v96l-49 8L0 99Z" fill="#d49d61"/><path d="m0 19 24 16 49-7M24 35v81" fill="none"/><path d="m35 52 25-4v29l-25 4Z" fill="#f7dfba" stroke="none"/></g>
<g transform="translate(241 62) rotate(-8 45 65)"><path d="M0 30 21 0h46l23 30v115H0Z" fill="#f8f5e9"/><path d="M0 30h90M21 0v30M67 0v30" fill="none"/><path d="M0 68h90v48H0Z" fill="#18bdf2"/><path d="M33 91c0-9 12-18 12-18s12 9 12 18a12 12 0 0 1-24 0Z" fill="#f8f5e9" stroke="none"/></g>
<path d="M303 273v-43m-16 16 16-16 16 16" fill="none" stroke="#237a59" stroke-width="8"/>
<path d="M230 269 319 257 358 273 269 287Z" fill="none" stroke="#a28270" stroke-width="3" stroke-dasharray="6 8"/>
<path d="m214 85-17-9m26-8-6-17m-13 55h-20" stroke="#a28270"/>
''')
