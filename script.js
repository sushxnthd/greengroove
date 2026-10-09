const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Load the non-destructive refinement layer after the base replica stylesheet.
if(!document.querySelector('link[href^="refinement.css"]')){
  const refinement=document.createElement('link');
  refinement.rel='stylesheet';
  refinement.href='refinement.css?v=1';
  document.head.appendChild(refinement);
}

// Menu
const menuSheet = document.querySelector('.menu-sheet');
const menuOpen = document.querySelector('.nav-menu');
const menuClose = document.querySelector('.menu-close');
function setMenu(open){
  menuSheet?.classList.toggle('open', open);
  menuSheet?.setAttribute('aria-hidden', String(!open));
  menuOpen?.setAttribute('aria-expanded', String(open));
  document.body.classList.toggle('menu-open', open);
  if(open) menuClose?.focus({preventScroll:true});
}
menuOpen?.addEventListener('click',()=>setMenu(true));
menuClose?.addEventListener('click',()=>setMenu(false));
menuSheet?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));

// Reveal on scroll
const reveals=[...document.querySelectorAll('.reveal')];
if('IntersectionObserver' in window && !reduceMotion){
  const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(entry.isIntersecting){entry.target.classList.add('in');io.unobserve(entry.target)}
  }),{threshold:.08,rootMargin:'0px 0px -45px'});
  reveals.forEach((el,i)=>{el.style.transitionDelay=`${Math.min((i%3)*65,130)}ms`;io.observe(el)});
}else reveals.forEach(el=>el.classList.add('in'));

// Ensure direct anchor navigation never leaves the destination faded while IntersectionObserver catches up.
function revealHashTarget(){
  if(!location.hash)return;
  const target=document.querySelector(location.hash);
  target?.classList.add('in');
  target?.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'));
}
window.addEventListener('hashchange',()=>requestAnimationFrame(revealHashTarget));
window.addEventListener('load',()=>requestAnimationFrame(revealHashTarget));

// Floating nav tucks away on downward scroll, matching the reference behavior.
const floatNav=document.querySelector('.float-nav');
let lastY=window.scrollY, ticking=false;
function updateNav(){
  const y=window.scrollY;
  if(y>220 && y>lastY+5 && !document.body.classList.contains('menu-open')) floatNav?.classList.add('hidden');
  if(y<lastY-4 || y<100) floatNav?.classList.remove('hidden');
  lastY=y;ticking=false;
}
window.addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(updateNav)}},{passive:true});

// Drag rails
function initDragRail(rail){
  let down=false,startX=0,startScroll=0,moved=false;
  rail.addEventListener('pointerdown',e=>{
    if(e.pointerType==='mouse' && e.button!==0) return;
    down=true;moved=false;startX=e.clientX;startScroll=rail.scrollLeft;
    rail.classList.add('dragging');rail.setPointerCapture?.(e.pointerId);
  });
  rail.addEventListener('pointermove',e=>{
    if(!down)return;
    const delta=e.clientX-startX;
    if(Math.abs(delta)>4)moved=true;
    rail.scrollLeft=startScroll-delta*1.15;
  });
  const stop=()=>{down=false;rail.classList.remove('dragging');setTimeout(()=>moved=false,0)};
  rail.addEventListener('pointerup',stop);rail.addEventListener('pointercancel',stop);
  rail.addEventListener('dragstart',e=>e.preventDefault());
  rail.addEventListener('click',e=>{if(moved){e.preventDefault();e.stopPropagation()}},true);
}
const dragRails=[...document.querySelectorAll('[data-drag-rail]')];
dragRails.forEach(initDragRail);

// Updates arrows
const updatesRail=document.querySelector('.updates-rail');
document.querySelector('[data-rail-prev="updates"]')?.addEventListener('click',()=>updatesRail?.scrollBy({left:-430,behavior:reduceMotion?'auto':'smooth'}));
document.querySelector('[data-rail-next="updates"]')?.addEventListener('click',()=>updatesRail?.scrollBy({left:430,behavior:reduceMotion?'auto':'smooth'}));

// Toolkit pills jump the corresponding card into view.
const toolTabs=[...document.querySelectorAll('.tool-tabs button')];
const toolCards=[...document.querySelectorAll('.tool-card')];
toolTabs.forEach((button,index)=>button.addEventListener('click',()=>{
  toolTabs.forEach(b=>b.classList.toggle('active',b===button));
  toolCards[index]?.scrollIntoView({behavior:reduceMotion?'auto':'smooth',block:'nearest',inline:'center'});
}));

// Reflection carousel
const quoteSlides=[...document.querySelectorAll('.quote-slide')];
let quoteIndex=0, quoteTimer=null;
function setQuote(index,user=false){
  if(!quoteSlides.length)return;
  quoteIndex=(index+quoteSlides.length)%quoteSlides.length;
  quoteSlides.forEach((slide,i)=>slide.classList.toggle('active',i===quoteIndex));
  if(user) restartQuotes();
}
function restartQuotes(){
  if(reduceMotion)return;
  clearInterval(quoteTimer);
  quoteTimer=setInterval(()=>setQuote(quoteIndex+1),6500);
}
document.querySelector('[data-quote-prev]')?.addEventListener('click',()=>setQuote(quoteIndex-1,true));
document.querySelector('[data-quote-next]')?.addEventListener('click',()=>setQuote(quoteIndex+1,true));
setQuote(0);restartQuotes();

// Roadmap toggle
const roadmapButtons=[...document.querySelectorAll('[data-roadmap]')];
const roadmapNumbers=[...document.querySelectorAll('.road-number strong[data-current]')];
roadmapButtons.forEach(button=>button.addEventListener('click',()=>{
  roadmapButtons.forEach(b=>b.classList.toggle('active',b===button));
  const mode=button.dataset.roadmap;
  roadmapNumbers.forEach(el=>{
    el.textContent=mode==='next'?el.dataset.next:el.dataset.current;
    if(!reduceMotion)el.animate([{opacity:.2,transform:'translateY(10px)'},{opacity:1,transform:'none'}],{duration:300,easing:'cubic-bezier(.22,1,.36,1)'});
  });
}));

// Showcase modal
const modal=document.querySelector('.detail-modal');
const modalTitle=document.querySelector('#modal-title');
const modalText=document.querySelector('.modal-copy p');
const modalArt=document.querySelector('.modal-art');
const details={
  'Wristband identity':'A persistent shopper session anchors every later event to a known in-store identity. Identity and sensing remain separable so their failure modes can be measured independently.',
  'Smart shelf event':'Products leaving or returning to a shelf become physical events first. They do not become irreversible purchases until the system reaches settlement.',
  'Association logic':'The system links each sensed event to the most plausible active shopper session. Overlap between shoppers is represented explicitly as uncertainty rather than silently forcing a match.',
  'Live cart state':'The cart is continuously derived from the event stream, keeping physical actions and digital state synchronized during the shopping trip.',
  'Return reversal':'A return inverts the state transition produced by its corresponding pick. This keeps the event history coherent instead of depending on ad-hoc correction rules.',
  'Settlement flow':'Checkout finalizes an already-built transaction state rather than reconstructing the shopping trip from scratch at the end.'
};
function openModal(card){
  const title=card.querySelector('h3')?.textContent?.trim()||'Green Groove module';
  const number=card.querySelector('.show-media > span')?.textContent?.trim()||'GG';
  modalTitle.textContent=title;modalText.textContent=details[title]||'A Green Groove system module.';modalArt.textContent=number;
  modal.classList.add('open');modal.setAttribute('aria-hidden','false');document.body.classList.add('modal-open');
  document.querySelector('.modal-close')?.focus({preventScroll:true});
}
function closeModal(){modal?.classList.remove('open');modal?.setAttribute('aria-hidden','true');document.body.classList.remove('modal-open')}
document.querySelectorAll('.show-card').forEach(card=>{
  card.setAttribute('role','button');
  card.setAttribute('aria-label',`Open ${card.querySelector('h3')?.textContent||'module'} details`);
  card.addEventListener('click',()=>openModal(card));
  card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openModal(card)}});
});
document.querySelector('.modal-close')?.addEventListener('click',closeModal);
modal?.addEventListener('pointerdown',e=>{if(e.target===modal)closeModal()});

// Drag cursor seen on the reference rails.
const dragCursor=document.querySelector('.drag-cursor');
if(dragCursor && !reduceMotion && window.matchMedia('(pointer:fine)').matches){
  let raf=0,x=0,y=0;
  document.addEventListener('pointermove',e=>{x=e.clientX;y=e.clientY;if(!raf)raf=requestAnimationFrame(()=>{dragCursor.style.left=`${x}px`;dragCursor.style.top=`${y}px`;raf=0})},{passive:true});
  dragRails.forEach(rail=>{
    rail.addEventListener('pointerenter',()=>dragCursor.classList.add('visible'));
    rail.addEventListener('pointerleave',()=>dragCursor.classList.remove('visible'));
    rail.addEventListener('pointerdown',()=>dragCursor.textContent='HOLD');
    rail.addEventListener('pointerup',()=>dragCursor.textContent='DRAG');
  });
}

// Subtle hero depth. The outer card rotations stay fixed; only the card screens parallax.
const hero=document.querySelector('.hero');
const heroOrbit=document.querySelector('.hero-orbit');
const orbitCards=[...document.querySelectorAll('.orbit-card')];
if(hero && heroOrbit && !reduceMotion){
  window.addEventListener('scroll',()=>{
    const y=Math.min(window.scrollY,650);
    heroOrbit.style.marginTop=`${y*.035}px`;
  },{passive:true});
  hero.addEventListener('pointermove',e=>{
    const rect=hero.getBoundingClientRect();
    const nx=(e.clientX-rect.left)/rect.width-.5;
    const ny=(e.clientY-rect.top)/rect.height-.5;
    orbitCards.forEach((card,index)=>{
      const depth=((index%4)+1)*.9;
      card.style.setProperty('--dx',`${(nx*depth*4).toFixed(2)}px`);
      card.style.setProperty('--dy',`${(ny*depth*3).toFixed(2)}px`);
    });
  });
  hero.addEventListener('pointerleave',()=>orbitCards.forEach(card=>{card.style.setProperty('--dx','0px');card.style.setProperty('--dy','0px')}));
}

// Reel demo button
const play=document.querySelector('.play-disc');
play?.addEventListener('click',()=>{
  const stage=document.querySelector('.dashboard-stage');
  if(!stage)return;
  stage.animate([{filter:'brightness(1)'},{filter:'brightness(1.12)'},{filter:'brightness(1)'}],{duration:900,easing:'ease-out'});
  play.textContent=play.textContent==='▶'?'Ⅱ':'▶';
});

// Newsletter demo validation
const form=document.querySelector('#newsletter-form');
form?.addEventListener('submit',e=>{
  e.preventDefault();
  const status=form.querySelector('.form-status');
  const email=form.querySelector('input[type="email"]');
  const consent=form.querySelector('input[type="checkbox"]');
  if(!email?.value.trim()){status.textContent='Enter an email address first.';email?.focus();return}
  if(consent&&!consent.checked){status.textContent='Please confirm you want project updates.';consent.focus();return}
  status.textContent='Interface ready for a mailing-list backend.';
});

const year=document.querySelector('#year');
if(year)year.textContent=new Date().getFullYear();

document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){
    if(modal?.classList.contains('open')) closeModal();
    else if(menuSheet?.classList.contains('open')) setMenu(false);
  }
});
