const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function initSourceHero(){
  const hero=document.querySelector('.hero');
  const orbit=document.querySelector('.hero-orbit');
  const sub=document.querySelector('.hero-sub');
  if(!hero||!orbit)return;

  if(sub && !sub.parentElement?.classList.contains('hero-description-row')){
    const row=document.createElement('div');
    row.className='hero-description-row';
    sub.before(row);
    row.appendChild(sub);
  }

  const titleWords=[];
  document.querySelectorAll('.hero-title-row h1').forEach((heading)=>{
    if(heading.dataset.ggSplit==='true'){
      titleWords.push(...heading.querySelectorAll('.gg-word'));
      return;
    }
    const words=heading.textContent.trim().split(/\s+/);
    heading.textContent='';
    words.forEach((word,index)=>{
      const span=document.createElement('span');
      span.className='gg-word';
      span.textContent=word;
      heading.appendChild(span);
      if(index<words.length-1) heading.appendChild(document.createTextNode(' '));
      titleWords.push(span);
    });
    heading.dataset.ggSplit='true';
  });

  let list=orbit.querySelector('.hero-orbit-list');
  if(!list){
    const originals=[...orbit.children].filter(el=>el.classList?.contains('orbit-card'));
    const radial=document.createElement('div');
    radial.className='hero-orbit-radial';
    radial.setAttribute('aria-hidden','true');
    const clip=document.createElement('div');
    clip.className='hero-orbit-clip';
    const circle=document.createElement('div');
    circle.className='hero-orbit-circle';
    list=document.createElement('div');
    list.className='hero-orbit-list';

    const cards=[...originals];
    originals.forEach(card=>{
      const clone=card.cloneNode(true);
      clone.classList.add('orbit-clone');
      clone.setAttribute('aria-hidden','true');
      cards.push(clone);
    });
    const step=360/cards.length;
    cards.forEach((card,index)=>{
      card.style.setProperty('--gg-angle',`${(step*index).toFixed(4)}deg`);
      list.appendChild(card);
    });
    circle.appendChild(list);
    clip.appendChild(circle);
    radial.appendChild(clip);
    orbit.appendChild(radial);
  }

  const radial=orbit.querySelector('.hero-orbit-radial');
  if(!reduceMotion){
    const radialObserver=new IntersectionObserver(entries=>{
      entries.forEach(entry=>list?.classList.toggle('is-running',entry.isIntersecting));
    },{threshold:.03});
    radialObserver.observe(orbit);
  }

  if(!reduceMotion){
    requestAnimationFrame(()=>{
      document.querySelector('.float-nav')?.animate([
        {transform:'translate(-50%,-125%)',opacity:0},
        {transform:'translate(-50%,0)',opacity:1}
      ],{duration:1000,easing:'cubic-bezier(.16,1,.3,1)',fill:'backwards'});

      titleWords.forEach((word,index)=>word.animate([
        {transform:'translateY(105%) rotate(10deg)',opacity:.001},
        {transform:'translateY(0) rotate(0deg)',opacity:1}
      ],{duration:1200,delay:90+index*50,easing:'cubic-bezier(.16,1,.3,1)',fill:'backwards'}));

      document.querySelector('.hero-mark')?.animate([
        {transform:'translateY(100%) scale(.3) rotate(-270deg)',opacity:0},
        {transform:'translateY(0) scale(1) rotate(8deg)',opacity:1}
      ],{duration:1200,delay:180,easing:'cubic-bezier(.16,1,.3,1)',fill:'backwards'});

      document.querySelector('.hero-description-row')?.animate([
        {transform:'translateY(2em)',opacity:0},
        {transform:'translateY(0)',opacity:1}
      ],{duration:1200,delay:260,easing:'cubic-bezier(.16,1,.3,1)',fill:'backwards'});

      radial?.animate([
        {transform:'translateX(-50%) rotate(-45deg)',opacity:.2},
        {transform:'translateX(-50%) rotate(0deg)',opacity:1}
      ],{duration:2000,delay:120,easing:'cubic-bezier(.16,1,.3,1)',fill:'backwards'});
    });
  }else{
    list?.classList.remove('is-running');
  }
}
initSourceHero();

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

const reveals=[...document.querySelectorAll('.reveal')];
if('IntersectionObserver' in window && !reduceMotion){
  const io=new IntersectionObserver(entries=>entries.forEach(entry=>{
    if(entry.isIntersecting){entry.target.classList.add('in');io.unobserve(entry.target)}
  }),{threshold:.08,rootMargin:'0px 0px -45px'});
  reveals.forEach((el,i)=>{el.style.transitionDelay=`${Math.min((i%3)*65,130)}ms`;io.observe(el)});
}else reveals.forEach(el=>el.classList.add('in'));

function revealHashTarget(){
  if(!location.hash)return;
  const target=document.querySelector(location.hash);
  target?.classList.add('in');
  target?.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'));
}
window.addEventListener('hashchange',()=>requestAnimationFrame(revealHashTarget));
window.addEventListener('load',()=>requestAnimationFrame(revealHashTarget));

const floatNav=document.querySelector('.float-nav');
let lastY=window.scrollY, navTicking=false;
function updateNav(){
  const y=window.scrollY;
  if(y>220 && y>lastY+5 && !document.body.classList.contains('menu-open')) floatNav?.classList.add('hidden');
  if(y<lastY-4 || y<100) floatNav?.classList.remove('hidden');
  lastY=y;navTicking=false;
}
window.addEventListener('scroll',()=>{if(!navTicking){navTicking=true;requestAnimationFrame(updateNav)}},{passive:true});

function initDragRail(rail){
  let down=false,startX=0,startScroll=0,moved=false;
  rail.addEventListener('pointerdown',e=>{
    if(e.pointerType==='mouse' && e.button!==0)return;
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

const updatesRail=document.querySelector('.updates-rail');
document.querySelector('[data-rail-prev="updates"]')?.addEventListener('click',()=>updatesRail?.scrollBy({left:-430,behavior:reduceMotion?'auto':'smooth'}));
document.querySelector('[data-rail-next="updates"]')?.addEventListener('click',()=>updatesRail?.scrollBy({left:430,behavior:reduceMotion?'auto':'smooth'}));

const toolTabs=[...document.querySelectorAll('.tool-tabs button')];
const toolCards=[...document.querySelectorAll('.tool-card')];
toolTabs.forEach((button,index)=>button.addEventListener('click',()=>{
  toolTabs.forEach(b=>b.classList.toggle('active',b===button));
  toolCards[index]?.scrollIntoView({behavior:reduceMotion?'auto':'smooth',block:'nearest',inline:'center'});
}));

const quoteSlides=[...document.querySelectorAll('.quote-slide')];
let quoteIndex=0, quoteTimer=null;
function setQuote(index,user=false){
  if(!quoteSlides.length)return;
  quoteIndex=(index+quoteSlides.length)%quoteSlides.length;
  quoteSlides.forEach((slide,i)=>slide.classList.toggle('active',i===quoteIndex));
  if(user)restartQuotes();
}
function restartQuotes(){
  if(reduceMotion)return;
  clearInterval(quoteTimer);
  quoteTimer=setInterval(()=>setQuote(quoteIndex+1),6500);
}
document.querySelector('[data-quote-prev]')?.addEventListener('click',()=>setQuote(quoteIndex-1,true));
document.querySelector('[data-quote-next]')?.addEventListener('click',()=>setQuote(quoteIndex+1,true));
setQuote(0);restartQuotes();

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
  if(modalTitle)modalTitle.textContent=title;
  if(modalText)modalText.textContent=details[title]||'A Green Groove system module.';
  if(modalArt)modalArt.textContent=number;
  modal?.classList.add('open');modal?.setAttribute('aria-hidden','false');document.body.classList.add('modal-open');
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

const dragCursor=document.querySelector('.drag-cursor');
if(dragCursor && !reduceMotion && window.matchMedia('(pointer:fine)').matches){
  let cursorRaf=0,x=0,y=0;
  document.addEventListener('pointermove',e=>{
    x=e.clientX;y=e.clientY;
    if(!cursorRaf)cursorRaf=requestAnimationFrame(()=>{dragCursor.style.left=`${x}px`;dragCursor.style.top=`${y}px`;cursorRaf=0});
  },{passive:true});
  dragRails.forEach(rail=>{
    rail.addEventListener('pointerenter',()=>dragCursor.classList.add('visible'));
    rail.addEventListener('pointerleave',()=>dragCursor.classList.remove('visible'));
    rail.addEventListener('pointerdown',()=>dragCursor.textContent='HOLD');
    rail.addEventListener('pointerup',()=>dragCursor.textContent='DRAG');
  });
}

const hero=document.querySelector('.hero');
const orbitCards=[...document.querySelectorAll('.hero-orbit .orbit-card')];
if(hero && !reduceMotion){
  hero.addEventListener('pointermove',e=>{
    const rect=hero.getBoundingClientRect();
    const nx=(e.clientX-rect.left)/rect.width-.5;
    const ny=(e.clientY-rect.top)/rect.height-.5;
    orbitCards.forEach((card,index)=>{
      const depth=((index%4)+1)*.75;
      card.style.setProperty('--dx',`${(nx*depth*3.2).toFixed(2)}px`);
      card.style.setProperty('--dy',`${(ny*depth*2.4).toFixed(2)}px`);
    });
  });
  hero.addEventListener('pointerleave',()=>orbitCards.forEach(card=>{
    card.style.setProperty('--dx','0px');card.style.setProperty('--dy','0px');
  }));
}

const play=document.querySelector('.play-disc');
play?.addEventListener('click',()=>{
  const stage=document.querySelector('.dashboard-stage');
  if(!stage)return;
  stage.animate([{filter:'brightness(1)'},{filter:'brightness(1.12)'},{filter:'brightness(1)'}],{duration:900,easing:'ease-out'});
  play.textContent=play.textContent==='▶'?'Ⅱ':'▶';
});

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
    if(modal?.classList.contains('open'))closeModal();
    else if(menuSheet?.classList.contains('open'))setMenu(false);
  }
});
