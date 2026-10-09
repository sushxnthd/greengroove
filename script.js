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
document.addEventListener('keydown',event=>{if(event.key==='Escape')setMenu(false)});

if('IntersectionObserver' in window&&!reduceMotion){
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('in');observer.unobserve(entry.target)}
    });
  },{threshold:.08,rootMargin:'0px 0px -52px'});
  revealItems.forEach((item,index)=>{item.style.transitionDelay=`${Math.min((index%4)*70,210)}ms`;observer.observe(item)});
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

const dragRails=[...document.querySelectorAll('[data-drag-rail]')];
dragRails.forEach(rail=>{
  let down=false,startX=0,startScroll=0;
  rail.addEventListener('pointerdown',e=>{down=true;startX=e.clientX;startScroll=rail.scrollLeft;rail.setPointerCapture?.(e.pointerId);rail.style.cursor='grabbing'});
  rail.addEventListener('pointermove',e=>{if(!down)return;rail.scrollLeft=startScroll-(e.clientX-startX)*1.3});
  const end=()=>{down=false;rail.style.cursor='grab'};
  rail.addEventListener('pointerup',end);rail.addEventListener('pointercancel',end);rail.addEventListener('pointerleave',()=>{if(down)end()});
});

const planButtons=[...document.querySelectorAll('[data-plan]')];
const planNumbers=[...document.querySelectorAll('.price-main strong[data-current]')];
planButtons.forEach(button=>button.addEventListener('click',()=>{
  planButtons.forEach(b=>b.classList.toggle('active',b===button));
  const mode=button.dataset.plan;
  planNumbers.forEach(el=>{
    const next=mode==='next'?el.dataset.next:el.dataset.current;
    el.animate?.([{opacity:.2,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:260,easing:'ease-out'});
    el.textContent=next;
  });
}));

const form=document.getElementById('newsletter-form');
form?.addEventListener('submit',event=>{
  event.preventDefault();
  const status=form.querySelector('.form-status');
  if(status) status.textContent='Thanks — this demo form is ready to connect to your mailing list.';
});

const year=document.getElementById('year');
if(year)year.textContent=new Date().getFullYear();
