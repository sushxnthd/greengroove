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

// Footer motion copied from the purchased Osmo source: desktop-only, 7 pieces,
// scrubbed from "top bottom" to the document's "bottom bottom". No hover animation.
const footerWrap=q('[data-footer-logo-wrap]');
const footerImg=footerWrap&&(q('.gg-footer-wordmark',footerWrap)||q('img[alt="Green Groove"]',footerWrap));
if(footerWrap&&footerImg&&!footerWrap.dataset.ggSourceFooter){
  footerWrap.dataset.ggSourceFooter='1';
  const sourceStates=[
    {rotate:-45,yPercent:90},
    {rotate:-22.5,yPercent:35},
    {rotate:-11.25,yPercent:20},
    {rotate:0,yPercent:0},
    {rotate:11.25,yPercent:10},
    {rotate:22.5,yPercent:35},
    {rotate:45,yPercent:90}
  ];
  const setSourceGeometry=()=>{
    const mobile=innerWidth<768;
    Object.assign(footerWrap.style,mobile?{
      width:'210vw',marginTop:'var(--gap-xxl)',marginBottom:'.625em',marginLeft:'-85vw',left:'auto',transform:'none',overflow:'visible',display:'flex',position:'relative'
    }:{
      width:'122vw',marginTop:'',marginBottom:'',marginLeft:'',left:'50%',transform:'translateX(-50%)',overflow:'visible',display:'flex',position:'relative'
    });
    footerImg.style.animation='none';
    footerImg.style.width='100%';
    footerImg.style.maxWidth='none';
    footerImg.style.margin='0';
    footerImg.style.height='auto';
  };
  setSourceGeometry();

  const build=()=>{
    if(footerWrap.dataset.ggSourceFooterBuilt)return;
    footerWrap.dataset.ggSourceFooterBuilt='1';
    const w=footerImg.naturalWidth||170,h=footerImg.naturalHeight||15;
    const ns='http://www.w3.org/2000/svg';
    const svg=document.createElementNS(ns,'svg');
    svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
    svg.setAttribute('aria-hidden','true');
    svg.setAttribute('preserveAspectRatio','xMidYMid meet');
    svg.classList.add('gg-footer-source-svg');
    Object.assign(svg.style,{position:'absolute',inset:'0',width:'100%',height:'100%',overflow:'visible',pointerEvents:'none'});
    const defs=document.createElementNS(ns,'defs');svg.appendChild(defs);
    const pieces=[];
    for(let i=0;i<7;i++){
      const clip=document.createElementNS(ns,'clipPath');clip.id=`gg-footer-clip-${i}`;
      const rect=document.createElementNS(ns,'rect');
      rect.setAttribute('x',String(i*w/7-.02*w/7));rect.setAttribute('y','-1');
      rect.setAttribute('width',String(w/7*1.04));rect.setAttribute('height',String(h+2));
      clip.appendChild(rect);defs.appendChild(clip);
      const g=document.createElementNS(ns,'g');
      g.setAttribute('clip-path',`url(#${clip.id})`);
      g.style.transformBox='fill-box';
      g.style.transformOrigin='center center';
      g.style.willChange='transform';
      const image=document.createElementNS(ns,'image');
      image.setAttribute('href',footerImg.src);image.setAttribute('x','0');image.setAttribute('y','0');
      image.setAttribute('width',String(w));image.setAttribute('height',String(h));
      image.setAttribute('preserveAspectRatio','xMidYMid meet');
      g.appendChild(image);svg.appendChild(g);pieces.push(g);
    }
    footerWrap.appendChild(svg);
    footerImg.style.visibility='hidden';

    const gsap=window.gsap;
    const hasScrollTrigger=!!(gsap&&(gsap.plugins?.ScrollTrigger||window.ScrollTrigger));
    if(hasScrollTrigger&&innerWidth>=768){
      try{
        if(window.ScrollTrigger)gsap.registerPlugin(window.ScrollTrigger);
        gsap.set(pieces,{transformOrigin:'center center'});
        sourceStates.forEach((state,i)=>{if(i!==3)gsap.set(pieces[i],{rotate:state.rotate,yPercent:state.yPercent})});
        gsap.to(pieces,{rotate:0,yPercent:0,ease:'none',scrollTrigger:{trigger:footerWrap,start:'top bottom',endTrigger:document.body,end:'bottom bottom',scrub:true}});
        return;
      }catch(_e){}
    }

    // Fallback reproduces the same linear scrub if GSAP/ScrollTrigger has not initialized yet.
    let raf=0;
    const paint=()=>{
      raf=0;
      if(innerWidth<768){pieces.forEach(p=>p.style.transform='none');return}
      const rect=footerWrap.getBoundingClientRect();
      const start=scrollY+rect.top-innerHeight;
      const end=Math.max(start+1,document.documentElement.scrollHeight-innerHeight);
      const progress=Math.max(0,Math.min(1,(scrollY-start)/(end-start)));
      pieces.forEach((piece,i)=>{
        const s=sourceStates[i];
        const k=1-progress;
        piece.style.transform=`translateY(${s.yPercent*k}%) rotate(${s.rotate*k}deg)`;
      });
    };
    const requestPaint=()=>{if(!raf)raf=requestAnimationFrame(paint)};
    addEventListener('scroll',requestPaint,{passive:true});
    addEventListener('resize',()=>{setSourceGeometry();requestPaint()},{passive:true});
    requestPaint();
  };
  if(footerImg.complete)build();else footerImg.addEventListener('load',build,{once:true});
}
})();
