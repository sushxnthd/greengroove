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

// Osmo-style footer watermark: oversized, edge-clipped and revealed in a staggered vertical wave.
// Keep the exact supplied Green Groove SVG; only the presentation/interaction is reconstructed here.
const footerLogo=q('[data-footer-logo-wrap]');
const footerImg=footerLogo&&(q('.gg-footer-wordmark',footerLogo)||q('img[alt="Green Groove"]',footerLogo));
if(footerLogo&&footerImg&&!footerLogo.dataset.ggWatermark){
  footerLogo.dataset.ggWatermark='1';
  footerLogo.style.position='relative';
  footerLogo.style.overflow='hidden';
  footerLogo.style.isolation='isolate';
  footerLogo.style.cursor='default';
  footerImg.style.animation='none';
  footerImg.style.display='block';
  footerImg.style.width='112%';
  footerImg.style.maxWidth='none';
  footerImg.style.marginLeft='-6%';
  footerImg.style.height='auto';

  const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!reduceMotion){
    // The original remains in layout so the slot keeps its source dimensions.
    footerImg.style.visibility='hidden';
    const stage=document.createElement('div');
    stage.setAttribute('aria-hidden','true');
    Object.assign(stage.style,{position:'absolute',inset:'0',overflow:'hidden',perspective:'900px'});
    footerLogo.appendChild(stage);

    const slices=14;
    const parts=[];
    for(let i=0;i<slices;i++){
      const mask=document.createElement('span');
      Object.assign(mask.style,{position:'absolute',top:'0',bottom:'0',left:`${i*100/slices}%`,width:`${100/slices+.08}%`,overflow:'hidden'});
      const makeLayer=()=>{
        const im=footerImg.cloneNode(true);
        im.removeAttribute('class');
        Object.assign(im.style,{position:'absolute',top:'0',left:`-${i*100}%`,width:`${slices*112}%`,maxWidth:'none',height:'100%',margin:'0',objectFit:'fill',visibility:'visible',animation:'none',willChange:'transform',backfaceVisibility:'hidden'});
        return im;
      };
      const a=makeLayer(),b=makeLayer();
      a.style.transform='translate3d(0,112%,0) rotateX(-10deg)';
      b.style.transform='translate3d(0,112%,0) rotateX(-10deg)';
      mask.append(a,b);stage.appendChild(mask);parts.push([a,b]);
    }

    let entered=false,hovered=false;
    const move=(showSecond,entry=false)=>{
      parts.forEach(([a,b],i)=>{
        const delay=(entry?i:Math.abs(i-(slices-1)/2))*.032;
        const dur=entry?.82:.66;
        [a,b].forEach(el=>el.style.transition=`transform ${dur}s cubic-bezier(.16,1,.3,1) ${delay}s`);
        if(entry){
          a.style.transform='translate3d(0,0,0) rotateX(0deg)';
          b.style.transform='translate3d(0,112%,0) rotateX(-10deg)';
        }else if(showSecond){
          a.style.transform='translate3d(0,-112%,0) rotateX(10deg)';
          b.style.transform='translate3d(0,0,0) rotateX(0deg)';
        }else{
          a.style.transform='translate3d(0,0,0) rotateX(0deg)';
          b.style.transform='translate3d(0,112%,0) rotateX(-10deg)';
        }
      });
    };
    const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting&&!entered){entered=true;move(false,true);io.disconnect()}}),{threshold:.18});
    io.observe(footerLogo);
    footerLogo.addEventListener('pointerenter',()=>{if(!entered)return;hovered=true;move(true,false)});
    footerLogo.addEventListener('pointerleave',()=>{if(!entered)return;hovered=false;move(false,false)});
  }
}
})();