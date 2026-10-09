const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealItems=[...document.querySelectorAll('.reveal')];
const menuTrigger=document.querySelector('.menu-trigger');
const menuOverlay=document.querySelector('.menu-overlay');
const menuClose=document.querySelector('.menu-close');
const menuLinks=[...document.querySelectorAll('.menu-overlay a')];
const tiltCards=[...document.querySelectorAll('[data-tilt]')];

function setMenu(open){
  menuOverlay?.classList.toggle('open',open);
  menuOverlay?.setAttribute('aria-hidden',String(!open));
  menuTrigger?.setAttribute('aria-expanded',String(open));
  document.body.classList.toggle('menu-open',open);
}
menuTrigger?.addEventListener('click',()=>setMenu(true));
menuClose?.addEventListener('click',()=>setMenu(false));
menuLinks.forEach(link=>link.addEventListener('click',()=>setMenu(false)));
document.addEventListener('keydown',event=>{if(event.key==='Escape') setMenu(false)});

if('IntersectionObserver' in window && !reduceMotion){
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('in');
        observer.unobserve(entry.target);
      }
    });
  },{threshold:.08,rootMargin:'0px 0px -52px'});
  revealItems.forEach((item,index)=>{
    item.style.transitionDelay=`${Math.min((index%4)*70,210)}ms`;
    observer.observe(item);
  });
}else revealItems.forEach(item=>item.classList.add('in'));

if(!reduceMotion){
  tiltCards.forEach(card=>{
    const initial=getComputedStyle(card).transform;
    card.addEventListener('pointermove',event=>{
      const rect=card.getBoundingClientRect();
      const x=(event.clientX-rect.left)/rect.width-.5;
      const y=(event.clientY-rect.top)/rect.height-.5;
      card.style.transform=`${initial==='none'?'':initial} perspective(900px) rotateX(${(-y*5).toFixed(2)}deg) rotateY(${(x*6).toFixed(2)}deg) translateY(-5px)`;
    });
    card.addEventListener('pointerleave',()=>card.style.transform='');
  });
}

document.querySelectorAll('[data-jump]').forEach(button=>{
  button.addEventListener('click',()=>document.querySelector(button.dataset.jump)?.scrollIntoView({behavior:reduceMotion?'auto':'smooth'}));
});

const year=document.getElementById('year');
if(year) year.textContent=new Date().getFullYear();
