"""Semantic, decorative icons for the six engineering challenge cards."""
from pathlib import Path
icons=[
('association','Detection and association','<circle cx="25" cy="26" r="10"/><circle cx="71" cy="26" r="10"/><rect x="35" y="60" width="26" height="22" rx="5"/><path d="M25 36v12q0 23 10 23M71 36v12q0 23-10 23"/><path d="m40 71 5 5 11-13" stroke="#78ff45"/>'),
('reversal','Reversible physical actions','<path d="M24 35a29 29 0 1 1-2 32M12 17v22h22"/><path d="m37 46 11-6 11 6v17l-11 6-11-6Zm0 0 11 6 11-6m-11 6v17"/>'),
('cross-check','Independent sensor cross-check','<path d="m48 12 29 11v25c0 18-14 28-29 36-15-8-29-18-29-36V23Z"/><path d="m32 48 10 11 23-25" stroke="#78ff45"/>'),
('identity','Identity before automation','<rect x="28" y="9" width="40" height="78" rx="18"/><rect x="17" y="29" width="62" height="38" rx="13"/><rect x="36" y="40" width="24" height="16" rx="5" stroke="#78ff45"/>'),
('uncertainty','Make uncertainty visible','<path d="m48 12 37 66H11Z"/><path d="M48 34v20"/><circle cx="48" cy="65" r="2" fill="#f4f4f4"/>'),
('settlement','Settle known cart state','<path d="M22 12h52v71l-9-6-8 6-9-6-9 6-8-6-9 6Z"/><path d="M33 29h29M33 41h19"/><path d="m35 60 8 8 18-20" stroke="#78ff45"/>')]
p=Path('assets/visuals/challenge-icons');p.mkdir(parents=True,exist_ok=True)
for key,title,paths in icons:
 (p/f'{key}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><title>{title}</title><g fill="none" stroke="#f4f4f4" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{paths}</g></svg>')
