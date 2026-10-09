const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealItems=[...document.querySelectorAll('.reveal')];
const sideLinks=[...document.querySelectorAll('.side-link[href^="#"]')];
const mobileButton=document.querySelector('.mobile-menu-button');
const mobileDrawer=document.querySelector('.mobile-drawer');
const copyBrief=document.querySelector('.copy-brief');
const copyToast=document.querySelector('.copy-toast');

if('IntersectionObserver' in window && !reduceMotion){
  const revealObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('in');
        revealObserver.unobserve(entry.target);
      }
    });
  },{threshold:.08,rootMargin:'0px 0px -48px'});
  revealItems.forEach((item,index)=>{
    item.style.setProperty('--delay',`${Math.min((index%4)*70,210)}ms`);
    revealObserver.observe(item);
  });
}else{
  revealItems.forEach(item=>item.classList.add('in'));
}

const tracked=[...document.querySelectorAll('.page-section[id]')];
if('IntersectionObserver' in window){
  const navObserver=new IntersectionObserver(entries=>{
    const active=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
    if(!active) return;
    const id=active.target.id;
    sideLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===`#${id}`));
  },{rootMargin:'-16% 0px -70% 0px',threshold:[0,.12,.3,.55]});
  tracked.forEach(section=>navObserver.observe(section));
}

mobileButton?.addEventListener('click',()=>{
  const open=!mobileDrawer?.classList.contains('open');
  mobileDrawer?.classList.toggle('open',open);
  mobileDrawer?.setAttribute('aria-hidden',String(!open));
  mobileButton.setAttribute('aria-expanded',String(open));
});

mobileDrawer?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{
  mobileDrawer.classList.remove('open');
  mobileDrawer.setAttribute('aria-hidden','true');
  mobileButton?.setAttribute('aria-expanded','false');
}));

document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&mobileDrawer?.classList.contains('open')) mobileButton?.click();
});

copyBrief?.addEventListener('click',async()=>{
  const text=copyBrief.dataset.copy||'';
  try{
    await navigator.clipboard.writeText(text);
  }catch{
    const temp=document.createElement('textarea');
    temp.value=text;
    document.body.appendChild(temp);
    temp.select();
    document.execCommand('copy');
    temp.remove();
  }
  copyToast?.classList.add('show');
  window.setTimeout(()=>copyToast?.classList.remove('show'),1500);
});

const year=document.getElementById('year');
if(year) year.textContent=new Date().getFullYear();
