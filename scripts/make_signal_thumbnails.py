"""Small-screen technical symbols, not product photographs or measured evidence."""
from pathlib import Path
out=Path('assets/visuals/thumbnails');out.mkdir(exist_ok=True)
base='''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400" role="img"><title>{title}</title><rect width="600" height="400" fill="{bg}"/><g fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>'''
assets=[
('identity','RFID session identity — symbolic band','#171a15','#e8eae3','<ellipse cx="300" cy="214" rx="165" ry="98"/><path d="M135 214v42c0 55 74 98 165 98s165-43 165-98v-42"/><rect x="237" y="140" width="126" height="112" rx="24" fill="#171a15"/><rect x="270" y="170" width="60" height="52" rx="8" stroke="#a1ff62"/><path d="M300 110V86m-30 30-12-22m72 22 12-22" stroke="#a1ff62"/>'),
('shelf','Shelf sensing — product load on a support plate','#e8eae3','#201d1d','<path d="M103 258h394M135 278h330M222 278l-30 49h214l-30-49"/><rect x="245" y="104" width="110" height="130" rx="6"/><path d="M263 104v-22h74v22M300 24v36m-13-13 13 13 13-13" stroke="#4d7830"/><path d="M217 327h166" stroke="#4d7830"/>'),
('return','Return event — an explicit inverse action','#171a15','#e8eae3','<path d="m225 147 75-39 75 39v107l-75 39-75-39zM225 147l75 39 75-39M300 186v107"/><path d="M408 115c36 30 56 68 56 114 0 63-40 110-95 130M157 277c-36-67-11-157 47-198M204 79l-3 56m3-56-55 7" stroke="#18bdf2"/>'),
]
for key,title,bg,ink,body in assets:(out/(key+'.svg')).write_text(base.format(title=title,bg=bg,ink=ink,body=body))
print('Created first three thumbnail studies')
more=[
('cart','Live cart — accepted quantities only','#e8eae3','#201d1d','<rect x="155" y="63" width="290" height="278" rx="13"/><path d="M155 126h290M200 179h95m-95 55h95m-95 55h150"/><rect x="356" y="162" width="42" height="28" rx="4" stroke="#4d7830"/><rect x="356" y="217" width="42" height="28" rx="4" stroke="#4d7830"/>'),
('association','Association — one accepted candidate and one held','#171a15','#e8eae3','<rect x="90" y="146" width="100" height="108" rx="8"/><circle cx="440" cy="108" r="50"/><circle cx="440" cy="295" r="50" stroke="#be9348"/><path d="M190 190C275 190 296 108 390 108" stroke="#a1ff62"/><path d="M190 220c90 0 115 75 165 75" stroke="#be9348" stroke-dasharray="5 16"/><path d="M358 276v38m18-38v38" stroke="#be9348"/>'),
('settlement','Invoice summary — confirmation without payment','#e8eae3','#201d1d','<path d="M175 64h250v280l-25-16-25 16-25-16-25 16-25-16-25 16-25-16-25 16V64z"/><path d="M220 116h156m-156 47h98m-98 47h73"/><circle cx="352" cy="264" r="45" fill="#a1ff62"/><path d="m332 264 14 14 25-30"/>'),
]
for key,title,bg,ink,body in more:(out/(key+'.svg')).write_text(base.format(title=title,bg=bg,ink=ink,body=body))
last=[
('ledger','Event history — accepted and inverse events stay visible','#171a15','#e8eae3','<path d="M135 72v260" stroke="#778078"/><circle cx="135" cy="95" r="13" fill="#a1ff62" stroke="#a1ff62"/><circle cx="135" cy="165" r="13" fill="#a1ff62" stroke="#a1ff62"/><circle cx="135" cy="235" r="13" fill="#18bdf2" stroke="#18bdf2"/><circle cx="135" cy="305" r="13" stroke="#be9348"/><path d="M180 95h250m-250 70h250m-250 70h250m-250 70h175"/><path d="M467 235q70-70 0-140m0 0-7 37m7-37 36 8" stroke="#18bdf2"/>'),
('validation','Validation plan — measurements before performance claims','#e8eae3','#201d1d','<path d="M120 130h370v55H120zM140 130V73h35v57M140 185v116h35V185M370 130V73h35v57M370 185v116h35V185"/><path d="M205 130v18m35-18v30m35-30v18m35-18v30m35-30v18"/><rect x="262" y="202" width="60" height="60" rx="4" stroke="#4d7830"/><path d="M235 302h115" stroke="#4d7830"/>'),
('interaction','Product movement — a package leaves the shelf','#171a15','#e8eae3','<path d="M95 288h410M115 312h370M145 312v40m310-40v40"/><rect x="130" y="148" width="90" height="115" rx="5"/><rect x="335" y="85" width="90" height="115" rx="5"/><path d="M230 155c35-44 60-55 92-55m-25-12 25 12-19 22" stroke="#a1ff62"/>'),
]
for key,title,bg,ink,body in last:(out/(key+'.svg')).write_text(base.format(title=title,bg=bg,ink=ink,body=body))
