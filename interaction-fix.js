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

// Purchased Osmo footer behavior adapted to the actual Green Groove footer text.
const footerWrap=q('[data-footer-logo-wrap]');
const footerWord=footerWrap&&q('.gg-footer-word',footerWrap);
if(footerWrap&&footerWord&&!footerWrap.dataset.ggSourceFooter){
  footerWrap.dataset.ggSourceFooter='1';
  const chars=[...footerWord.textContent];
  footerWord.textContent='';
  const glyphs=[];
  chars.forEach(ch=>{const span=document.createElement('span');span.textContent=ch===' '?'\u00a0':ch;span.setAttribute('aria-hidden','true');Object.assign(span.style,{display:'inline-block',transformOrigin:'center center',willChange:'transform'});footerWord.appendChild(span);if(ch!==' ')glyphs.push(span)});
  footerWord.setAttribute('aria-label','GREEN GROOVE');

  // Osmo uses seven letter states. Sample that exact state curve across Green Groove's eleven letters.
  const stops=[[-45,90],[-22.5,35],[-11.25,20],[0,0],[11.25,10],[22.5,35],[45,90]];
  const stateAt=t=>{const u=t*6,i=Math.min(5,Math.floor(u)),f=u-i,a=stops[i],b=stops[i+1];return{rotate:a[0]+(b[0]-a[0])*f,yPercent:a[1]+(b[1]-a[1])*f}};
  const states=glyphs.map((_,i)=>stateAt(i/(glyphs.length-1)));
  const setGeometry=()=>{const mobile=innerWidth<768;Object.assign(footerWrap.style,mobile?{width:'210vw',marginTop:'var(--gap-xxl)',marginBottom:'.625em',marginLeft:'-85vw',left:'auto',transform:'none',overflow:'visible',display:'flex',position:'relative'}:{width:'122vw',marginTop:'',marginBottom:'',marginLeft:'',left:'50%',transform:'translateX(-50%)',overflow:'visible',display:'flex',position:'relative'})};
  setGeometry();

  const reset=()=>glyphs.forEach(g=>g.style.transform='');
  const gsap=window.gsap,ScrollTrigger=window.ScrollTrigger||gsap?.plugins?.ScrollTrigger;
  if(gsap&&ScrollTrigger){
    try{
      if(window.ScrollTrigger)gsap.registerPlugin(window.ScrollTrigger);
      if(gsap.matchMedia){
        gsap.matchMedia().add('(min-width: 768px)',()=>{
          states.forEach((s,i)=>gsap.set(glyphs[i],{rotate:s.rotate,yPercent:s.yPercent,transformOrigin:'center center'}));
          const tween=gsap.to(glyphs,{rotate:0,yPercent:0,ease:'none',scrollTrigger:{trigger:footerWrap,start:'top bottom',endTrigger:document.body,end:'bottom bottom',scrub:true}});
          return()=>{tween.scrollTrigger?.kill();tween.kill();reset()};
        });
        addEventListener('resize',setGeometry,{passive:true});
        return;
      }
    }catch(_e){reset()}
  }

  // Native fallback with the same start/end positions when GSAP is not exposed globally.
  let raf=0;
  const paint=()=>{raf=0;if(innerWidth<768){reset();return}const rect=footerWrap.getBoundingClientRect(),start=scrollY+rect.top-innerHeight,end=Math.max(start+1,document.documentElement.scrollHeight-innerHeight),p=Math.max(0,Math.min(1,(scrollY-start)/(end-start))),k=1-p;glyphs.forEach((g,i)=>{const s=states[i];g.style.transform=`translateY(${s.yPercent*k}%) rotate(${s.rotate*k}deg)`})};
  const requestPaint=()=>{if(!raf)raf=requestAnimationFrame(paint)};
  addEventListener('scroll',requestPaint,{passive:true});addEventListener('resize',()=>{setGeometry();requestPaint()},{passive:true});requestPaint();
}
})();
