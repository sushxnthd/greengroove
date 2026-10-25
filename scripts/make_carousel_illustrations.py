"""Code-native concept illustrations: one clear object/action per carousel card."""
from pathlib import Path
out=Path('assets/visuals/illustrations');out.mkdir(parents=True,exist_ok=True)
INK='#202722';GREEN='#78ff45';BLUE='#18bdf2';CREAM='#f4f1e8'
def write(key,title,bg,body):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400" role="img" aria-labelledby="title"><title id="title">{title}</title><rect width="600" height="400" fill="{bg}"/><g stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>'''
 (out/f'{key}.svg').write_text(svg)
# Thesis: a wristband establishes identity at the start of a shopping trip.
write('identity','Illustration: an RFID wristband worn on a wrist','#e9ded0','''
<path d="M-20 292 230 153l141 116-222 146" fill="#c68d69"/>
<path d="m210 164 70-51c25-18 61-17 80 1l81 77c14 14 4 37-15 37l-26-5 12 21c10 18-5 37-24 32l-17-7c-34 20-75 25-99 3" fill="#e3b08b"/>
<path d="m158 198 60-35c41-21 120 64 108 100l-57 38c-5-44-60-101-111-103Z" fill="#3b864c"/>
<path d="m164 195 57-32c30-12 106 66 103 101l-51 31c-8-38-60-95-109-100Z" fill="#78ff45"/>
<g transform="translate(241 217) rotate(44)"><rect x="-43" y="-35" width="86" height="70" rx="23" fill="#202722"/><rect x="-19" y="-16" width="38" height="32" rx="9" fill="#a1ff7b"/><path d="M-28-7c-7 5-7 10 0 15m56-15c7 5 7 10 0 15" fill="none" stroke="#a1ff7b" stroke-width="3"/></g>
<path d="M419 70q60 8 79 57m-73-31q30 3 42 27" fill="none" stroke="#237a59" stroke-width="7"/>
<circle cx="430" cy="135" r="7" fill="#237a59" stroke="none"/>
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
# Thesis: one product pick is a physical action, not an abstract state transition.
write('interaction','Illustration: a hand picking an apple from a retail crate','#efdfd9','''
<path d="m67 261 228-27 180 57-230 42Z" fill="#b07951"/><path d="m67 261 178 72 230-42v62l-230 49-178-75Z" fill="#d7a475"/><path d="m84 294 147 60m27 4 194-39M84 316l147 60m27 4 194-39" stroke="#a16b47"/>
<path d="M162 248c-47-6-46 66-9 67 13 1 13-7 24-3 38-1 34-71 0-65-9 3-9 5-15 1Z" fill="#ba6557"/><path d="M164 248c-1-13 8-21 16-25" fill="none" stroke="#476e42"/><path d="M255 244c-39-6-42 62-9 63 13 0 14-7 23-3 33-1 30-68 0-62-8 2-9 4-14 2Z" fill="#a2b86d"/>
<path d="M570 67 473 140l-59-10-66 36-11 46c-5 18 16 23 24 8l12-26 29-9-21 39c-10 18 9 29 23 15l43-43 72-13 84-73Z" fill="#e0aa87"/>
<path d="M339 139c-50-9-59 78-14 85 16 2 21-8 33-2 43 3 49-84 9-82-10 0-19 8-28-1Z" fill="#cb705c"/><path d="M344 139c0-17 12-28 23-31" fill="none" stroke="#476e42" stroke-width="7"/><path d="m355 120 17-10 16 4-17 11Z" fill="#699258"/>
<path d="M298 105 281 91m42 0-4-19m-40 56-23-3" stroke="#9a5b4d" stroke-width="5"/>
''')
