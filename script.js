const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Load the final fidelity layer without touching the original design stylesheet. */
if(!document.querySelector('link[href^="osmo-pass.css"]')){
  const pass=document.createElement('link');
  pass.rel='stylesheet';
  pass.href='osmo-pass.css?v=20261009';
  document.head.appendChild(pass);
}

const revealItems=[...document.querySelectorAll('.reveal')];
const menuTrigger=document.querySelector('.menu-trigger');
const menuOverlay=document.querySelector('.menu-overlay');
const menuClose=document.querySelector('.menu-close');
const menuLinks=[...document.querySelectorAll('.menu-overlay a')];
const tiltCards=[...document.querySelectorAll('[data-tilt]')];
const header=document.querySelector('.site-header');

function setMenu(open){
  menuOverlay?.classList.toggle('open',open);
  menuOverlay?.setAttribute('aria-hidden',String(!open));
  menuTrigger?.setAttribute('aria-expanded',String(open));
  document.body.classList.toggle('menu-open',open);
  if(open) menuClose?.focus({preventScroll:true});
}
menuTrigger?.addEventListener('click',()=>setMenu(true));
menuClose?.addEventListener('click',()=>setMenu(false));
menuLinks.forEach(link=>link.addEventListener('click',()=>setMenu(false)));
document.addEventListener('keydown',event=>{
  if(event.key==='Escape'){
    setMenu(false);
    closeShowcaseModal();
  }
});

/* Osmo-like compact header: visible when moving up, tucked away while scrolling down. */
let lastScrollY=window.scrollY;
let headerTick=false;
function updateHeader(){
  const y=window.scrollY;
  header?.classList.toggle('is-compact',y>80);
  if(y>220&&y>lastScrollY+4&&!document.body.classList.contains('menu-open')) header?.classList.add('is-hidden');
  else if(y<lastScrollY-3||y<120) header?.classList.remove('is-hidden');
  lastScrollY=y;
  headerTick=false;
}
window.addEventListener('scroll',()=>{
  if(!headerTick){headerTick=true;requestAnimationFrame(updateHeader)}
},{passive:true});

if('IntersectionObserver' in window&&!reduceMotion){
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      }
    });
  },{threshold:.08,rootMargin:'0px 0px -52px'});
  revealItems.forEach((item,index)=>{
    item.style.transitionDelay=`${Math.min((index%4)*65,195)}ms`;
    observer.observe(item);
  });
}else revealItems.forEach(item=>item.classList.add('in'));

if(!reduceMotion){
  tiltCards.forEach(card=>{
    card.addEventListener('pointermove',event=>{
      const rect=card.getBoundingClientRect();
      const x=(event.clientX-rect.left)/rect.width-.5;
      const y=(event.clientY-rect.top)/rect.height-.5;
      const base=card.classList.contains('card-one')?'rotate(-14deg) rotateY(8deg) translateZ(-34px)':card.classList.contains('card-two')?'rotate(10deg) rotateY(-5deg) translateZ(28px)':card.classList.contains('card-three')?'rotate(-9deg) rotateY(5deg) translateZ(42px)':'rotate(14deg) rotateY(-8deg) translateZ(-20px)';
      card.style.transform=`${base} perspective(900px) rotateX(${(-y*5).toFixed(2)}deg) rotateY(${(x*6).toFixed(2)}deg) translateY(-7px)`;
    });
    card.addEventListener('pointerleave',()=>card.style.transform='');
  });
}

document.querySelectorAll('[data-jump]').forEach(button=>button.addEventListener('click',()=>document.querySelector(button.dataset.jump)?.scrollIntoView({behavior:reduceMotion?'auto':'smooth'})));

/* Generic grab-to-scroll behavior used by the Osmo-style horizontal rails. */
function makeDragRail(rail){
  if(!rail||rail.dataset.dragReady==='true')return;
  rail.dataset.dragReady='true';
  let down=false,startX=0,startScroll=0,moved=false;
  rail.addEventListener('pointerdown',e=>{
    if(e.pointerType==='mouse'&&e.button!==0)return;
    down=true;moved=false;startX=e.clientX;startScroll=rail.scrollLeft;
    rail.setPointerCapture?.(e.pointerId);
    rail.classList.add('is-dragging');
  });
  rail.addEventListener('pointermove',e=>{
    if(!down)return;
    const delta=e.clientX-startX;
    if(Math.abs(delta)>4)moved=true;
    rail.scrollLeft=startScroll-delta*1.18;
  });
  const end=()=>{down=false;rail.classList.remove('is-dragging');setTimeout(()=>{moved=false},0)};
  rail.addEventListener('pointerup',end);
  rail.addEventListener('pointercancel',end);
  rail.addEventListener('dragstart',e=>e.preventDefault());
  rail.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation()}},true);
}

[...document.querySelectorAll('[data-drag-rail],.toolkit-grid,.showcase-grid')].forEach(makeDragRail);

/* Product/toolkit rail arrows. */
const toolkitRail=document.querySelector('.toolkit-grid');
if(toolkitRail&&!document.querySelector('.osmo-rail-controls')){
  const controls=document.createElement('div');
  controls.className='osmo-rail-controls';
  controls.innerHTML='<button type="button" aria-label="Previous toolkit item">←</button><button type="button" aria-label="Next toolkit item">→</button>';
  toolkitRail.after(controls);
  const [prev,next]=controls.querySelectorAll('button');
  const shift=()=>Math.min(toolkitRail.clientWidth*.82,430);
  prev.addEventListener('click',()=>toolkitRail.scrollBy({left:-shift(),behavior:reduceMotion?'auto':'smooth'}));
  next.addEventListener('click',()=>toolkitRail.scrollBy({left:shift(),behavior:reduceMotion?'auto':'smooth'}));
}

/* Roadmap toggle, preserving the existing Green Groove semantics. */
const planButtons=[...document.querySelectorAll('[data-plan]')];
const planNumbers=[...document.querySelectorAll('.price-main strong[data-current]')];
planButtons.forEach(button=>button.addEventListener('click',()=>{
  planButtons.forEach(b=>b.classList.toggle('active',b===button));
  const mode=button.dataset.plan;
  planNumbers.forEach(el=>{
    const next=mode==='next'?el.dataset.next:el.dataset.current;
    if(!reduceMotion)el.animate?.([{opacity:.15,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:260,easing:'cubic-bezier(.22,1,.36,1)'});
    el.textContent=next;
  });
}));

/* Green Groove reflections become an actual vertical quote carousel. */
const testimonialList=document.querySelector('.testimonial-list');
const testimonials=[...document.querySelectorAll('.testimonial')];
let testimonialIndex=0;
let testimonialTimer=null;
function setTestimonial(index,userInitiated=false){
  if(!testimonials.length)return;
  testimonialIndex=(index+testimonials.length)%testimonials.length;
  testimonials.forEach((item,i)=>{
    item.classList.toggle('is-active',i===testimonialIndex);
    item.setAttribute('aria-hidden',String(i!==testimonialIndex));
  });
  const progress=document.querySelector('.testimonial-progress');
  if(progress)progress.textContent=`${String(testimonialIndex+1).padStart(2,'0')} / ${String(testimonials.length).padStart(2,'0')}`;
  if(userInitiated)restartTestimonialAuto();
}
function restartTestimonialAuto(){
  if(reduceMotion)return;
  clearInterval(testimonialTimer);
  testimonialTimer=setInterval(()=>setTestimonial(testimonialIndex+1),6500);
}
if(testimonialList&&testimonials.length){
  testimonials.forEach((item,i)=>{
    item.classList.remove('reveal');
    item.style.transitionDelay='0ms';
    if(i===0)item.classList.add('is-active');
  });
  const controls=document.createElement('div');
  controls.className='testimonial-controls';
  controls.innerHTML=`<span class="testimonial-progress">01 / ${String(testimonials.length).padStart(2,'0')}</span><button type="button" aria-label="Previous reflection">←</button><button type="button" aria-label="Next reflection">→</button>`;
  testimonialList.after(controls);
  const buttons=controls.querySelectorAll('button');
  buttons[0].addEventListener('click',()=>setTestimonial(testimonialIndex-1,true));
  buttons[1].addEventListener('click',()=>setTestimonial(testimonialIndex+1,true));
  testimonialList.addEventListener('mouseenter',()=>clearInterval(testimonialTimer));
  testimonialList.addEventListener('mouseleave',restartTestimonialAuto);
  setTestimonial(0);
  restartTestimonialAuto();
}

/* Flick-style showcase with an accessible detail modal. */
const showcaseDetails={
  'Wristband identity':'A persistent shopper session anchors every later event to a known in-store identity. The module is intentionally separated from sensing so identity failure and sensing failure can be measured independently.',
  'Smart shelf event':'Shelf interactions are represented as physical pick and return events rather than immediate purchases. That keeps the transaction reversible until settlement.',
  'Association logic':'The system links a sensed event to the most plausible active shopper session. Multi-shopper overlap is treated as an explicit ambiguity problem instead of silently forcing a match.',
  'Live cart state':'The cart is derived continuously from the event stream so physical actions and digital state remain synchronized throughout the shopping trip.',
  'Return reversal':'A return should invert the exact state transition created by the corresponding pick. This gives Green Groove a clean event-history model rather than a pile of corrective patches.',
  'Settlement flow':'Checkout becomes the finalization of an already-built transaction state, not the first moment the system tries to reconstruct what happened.'
};
let showcaseModal=null;
function ensureShowcaseModal(){
  if(showcaseModal)return showcaseModal;
  showcaseModal=document.createElement('div');
  showcaseModal.className='gg-modal';
  showcaseModal.setAttribute('aria-hidden','true');
  showcaseModal.innerHTML='<div class="gg-modal-card" role="dialog" aria-modal="true" aria-labelledby="gg-modal-title"><div class="gg-modal-top"><span>Green Groove / module</span><button class="gg-modal-close" type="button">Close ×</button></div><div class="gg-modal-media" aria-hidden="true">GG</div><div class="gg-modal-copy"><h3 id="gg-modal-title"></h3><p></p></div></div>';
  document.body.appendChild(showcaseModal);
  showcaseModal.querySelector('.gg-modal-close').addEventListener('click',closeShowcaseModal);
  showcaseModal.addEventListener('pointerdown',e=>{if(e.target===showcaseModal)closeShowcaseModal()});
  return showcaseModal;
}
function openShowcaseModal(card){
  const modal=ensureShowcaseModal();
  const title=card.querySelector('h3')?.textContent?.trim()||'Green Groove module';
  const number=card.querySelector('.showcase-media span')?.textContent?.trim()||'GG';
  modal.querySelector('#gg-modal-title').textContent=title;
  modal.querySelector('.gg-modal-media').textContent=number;
  modal.querySelector('.gg-modal-copy p').textContent=showcaseDetails[title]||'A Green Groove system module connecting physical retail events to a coherent digital transaction state.';
  modal.classList.add('open');
  modal.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
  modal.querySelector('.gg-modal-close').focus({preventScroll:true});
}
function closeShowcaseModal(){
  if(!showcaseModal?.classList.contains('open'))return;
  showcaseModal.classList.remove('open');
  showcaseModal.setAttribute('aria-hidden','true');
  document.body.style.overflow=document.body.classList.contains('menu-open')?'hidden':'';
}

document.querySelectorAll('.showcase-card').forEach(card=>{
  card.tabIndex=0;
  card.setAttribute('role','button');
  card.setAttribute('aria-label',`Open ${card.querySelector('h3')?.textContent?.trim()||'module'} details`);
  card.addEventListener('click',()=>openShowcaseModal(card));
  card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openShowcaseModal(card)}});
});

/* Floating drag hint, matching Osmo's tactile rail affordance without copying artwork. */
if(!reduceMotion&&window.matchMedia('(pointer:fine)').matches){
  const hint=document.createElement('div');
  hint.className='drag-hint';
  hint.textContent='DRAG';
  document.body.appendChild(hint);
  let x=0,y=0,raf=0;
  const move=e=>{x=e.clientX;y=e.clientY;if(!raf)raf=requestAnimationFrame(()=>{hint.style.left=`${x}px`;hint.style.top=`${y}px`;raf=0})};
  document.addEventListener('pointermove',move,{passive:true});
  document.querySelectorAll('.toolkit-grid,.showcase-grid,[data-drag-rail]').forEach(rail=>{
    rail.addEventListener('pointerenter',()=>hint.classList.add('visible'));
    rail.addEventListener('pointerleave',()=>hint.classList.remove('visible'));
    rail.addEventListener('pointerdown',()=>hint.textContent='HOLD');
    rail.addEventListener('pointerup',()=>hint.textContent='DRAG');
  });
}

/* Footer's oversized wordmark echoes Osmo's giant closing brand moment using Green Groove type only. */
const footer=document.querySelector('.site-footer');
const footerBottom=footer?.querySelector('.footer-bottom');
if(footer&&footerBottom&&!footer.querySelector('.gg-giant-mark')){
  const mark=document.createElement('div');
  mark.className='gg-giant-mark';
  mark.innerHTML='<span>GREEN GROOVE</span>';
  footer.insertBefore(mark,footerBottom);
}

const form=document.getElementById('newsletter-form');
form?.addEventListener('submit',event=>{
  event.preventDefault();
  const status=form.querySelector('.form-status');
  const email=form.querySelector('input[type="email"]');
  const consent=form.querySelector('input[type="checkbox"]');
  if(!email?.value.trim()){
    if(status)status.textContent='Enter an email address first.';
    email?.focus();
    return;
  }
  if(consent&&!consent.checked){
    if(status)status.textContent='Please confirm you want project updates.';
    consent.focus();
    return;
  }
  if(status)status.textContent='Thanks — the interface is ready for a mailing-list backend.';
});

const year=document.getElementById('year');
if(year)year.textContent=new Date().getFullYear();
