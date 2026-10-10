(()=>{const q=(s,r=document)=>r.querySelector(s),qa=(s,r=document)=>[...r.querySelectorAll(s)];
// Source reel open/close state. Uses Osmo's own .fixed-reel :has() geometry with Green Groove media.
const player=q('[data-player-id="reel"]');
const setReel=open=>{if(!player)return;player.setAttribute('data-player-open',String(open));player.setAttribute('data-player-status',open?'playing':'paused');document.body.classList.toggle('gg-reel-open',open);if(open)q('[data-player-control-close="reel"]')?.focus({preventScroll:true})};
document.addEventListener('click',e=>{const open=e.target.closest('[data-player-control-open="reel"]');if(open){e.preventDefault();setReel(true);return}const close=e.target.closest('[data-player-control-close="reel"]');if(close){e.preventDefault();setReel(false)}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&player?.getAttribute('data-player-open')==='true')setReel(false)});

// Newsletter: preserve the source interaction without pretending a backend exists.
const form=q('#gg-newsletter');if(form&&!form.dataset.ggBound){form.dataset.ggBound='1';const status=document.createElement('p');status.className='form-status gg-newsletter-status';status.setAttribute('aria-live','polite');form.appendChild(status);form.addEventListener('submit',e=>{e.preventDefault();const email=q('input[type="email"]',form),check=q('input[type="checkbox"]',form);if(!email?.value.trim()||!email.checkValidity()){status.textContent='Enter a valid email address.';email?.focus();return}if(check&&!check.checked){status.textContent='Please confirm you want project updates.';check.focus();return}status.textContent='Thanks — the interface is ready for the Green Groove mailing backend.';const labels=qa('.button-label span',form);labels.forEach(x=>x.textContent='Added');setTimeout(()=>labels.forEach(x=>x.textContent='Get updates'),1800)})}

// Mobile footer accordions reproduce the source open/close convention.
qa('.footer-link__col').forEach(col=>{const top=q('.footer-link__col-top',col);if(!top)return;top.setAttribute('role','button');top.tabIndex=0;const toggle=()=>{if(innerWidth>767)return;const open=col.getAttribute('data-accordion-status')==='active';qa('.footer-link__col').forEach(c=>c.setAttribute('data-accordion-status','not-active'));col.setAttribute('data-accordion-status',open?'not-active':'active')};top.addEventListener('click',toggle);top.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle()}})});

// Green Groove's reel preview needs a visible visual in place of the removed Osmo video asset.
const preview=q('.reel__visual');if(preview&&!q('.gg-preview-state',preview)){const node=document.createElement('div');node.className='gg-preview-state';node.innerHTML='<span>GG-041</span><i></i><b>04</b>';preview.prepend(node)}
})();