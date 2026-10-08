const header=document.querySelector('.site-header');
const mobileToggle=document.querySelector('.mobile-menu-toggle');
const mobileMenu=document.querySelector('.mobile-menu');
const mobileLinks=[...document.querySelectorAll('.mobile-menu a')];
const navLinks=[...document.querySelectorAll('.desktop-nav .nav-link')];
const revealItems=[...document.querySelectorAll('.reveal')];
const staggerGroups=[...document.querySelectorAll('.stagger-group')];
const parallaxItems=[...document.querySelectorAll('.media-parallax')];
const explorer=document.querySelector('#project-explorer');
const projectQuery=document.querySelector('#project-query');
const feedback=document.querySelector('#explorer-feedback');
const roleChips=[...document.querySelectorAll('.role-chip')];
const rolePanels=[...document.querySelectorAll('.role-copy')];
const rolePanel=document.querySelector('.role-panel');
const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

window.addEventListener('scroll',()=>{
  header?.classList.toggle('scrolled',window.scrollY>8);
},{passive:true});

mobileToggle?.addEventListener('click',()=>{
  const open=mobileMenu?.classList.toggle('open');
  mobileToggle.setAttribute('aria-expanded',String(Boolean(open)));
  mobileMenu?.setAttribute('aria-hidden',String(!open));
  document.body.classList.toggle('menu-open',Boolean(open));
});

mobileLinks.forEach(link=>link.addEventListener('click',()=>{
  mobileMenu?.classList.remove('open');
  mobileToggle?.setAttribute('aria-expanded','false');
  mobileMenu?.setAttribute('aria-hidden','true');
  document.body.classList.remove('menu-open');
}));

document.addEventListener('keydown',event=>{
  if(event.key==='Escape'&&mobileMenu?.classList.contains('open')) mobileToggle?.click();
});

staggerGroups.forEach(group=>{
  [...group.querySelectorAll('.reveal')].forEach((item,index)=>{
    item.style.setProperty('--delay',`${Math.min(index*90,270)}ms`);
  });
});

const revealObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      entry.target.classList.add('in');
      revealObserver.unobserve(entry.target);
    }
  });
},{threshold:.08,rootMargin:'0px 0px -38px'});
revealItems.forEach(item=>revealObserver.observe(item));

const sectionMap={
  overview:'#overview',
  system:'#architecture',
  architecture:'#architecture',
  engineering:'#engineering',
  archive:'#engineering',
  validation:'#validation',
  contribution:'#overview',
  reflection:'#overview',
  team:'#team'
};
const trackedSections=[...document.querySelectorAll('main section[id]')];
const navObserver=new IntersectionObserver(entries=>{
  const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
  if(!visible[0]) return;
  const href=sectionMap[visible[0].target.id];
  navLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===href));
},{rootMargin:'-24% 0px -62% 0px',threshold:[0,.15,.35,.6]});
trackedSections.forEach(section=>navObserver.observe(section));

let roleSwitchTimer;
roleChips.forEach(chip=>chip.addEventListener('click',()=>{
  if(chip.classList.contains('active')) return;
  const role=chip.dataset.role;
  roleChips.forEach(item=>item.classList.toggle('active',item===chip));
  clearTimeout(roleSwitchTimer);
  rolePanel?.classList.add('switching');
  roleSwitchTimer=setTimeout(()=>{
    rolePanels.forEach(panel=>panel.classList.toggle('active',panel.dataset.rolePanel===role));
    requestAnimationFrame(()=>rolePanel?.classList.remove('switching'));
  },150);
}));

const destinations={
  overview:['overview','green groove','project','what is','summary'],
  system:['system','how it works','checkout','transaction','flow'],
  architecture:['architecture','identify','sense','associate','settle'],
  engineering:['engineering','edge cases','failure','failures','ambiguity','uncertainty'],
  'edge-return':['return','returns','put back','inverse'],
  'edge-sensors':['sensor','sensors','disagree','disagreement','signal','weight'],
  'edge-overlap':['simultaneous','overlap','two shoppers','association'],
  'edge-identity':['identity','session','persistent','shopper id','rfid'],
  contribution:['role','my role','contribution','my work','sushanth'],
  validation:['evidence','validation','prayaas','ncert','grant','50000','50k'],
  reflection:['reflection','learned','learning','what changed','lesson'],
  team:['team','aryan','members'],
  archive:['archive','behance','original','artifacts','design']
};

function findDestination(value){
  const q=value.trim().toLowerCase();
  if(!q) return null;
  for(const [id,keywords] of Object.entries(destinations)){
    if(keywords.some(keyword=>q.includes(keyword))) return id;
  }
  return null;
}

function goToSection(id){
  const target=document.getElementById(id);
  if(!target) return false;
  target.scrollIntoView({behavior:reduceMotion?'auto':'smooth',block:'start'});
  if(!reduceMotion){
    target.animate([
      {filter:'brightness(1)'},
      {filter:'brightness(1.12)'},
      {filter:'brightness(1)'}
    ],{duration:900,easing:'cubic-bezier(.22,1,.36,1)'});
  }
  return true;
}

explorer?.addEventListener('submit',event=>{
  event.preventDefault();
  const value=projectQuery?.value||'';
  const destination=findDestination(value);
  if(destination&&goToSection(destination)){
    if(feedback) feedback.textContent=`Opening ${value.trim()}…`;
    window.setTimeout(()=>{if(feedback) feedback.textContent='';},1800);
  }else{
    if(feedback) feedback.textContent='Try “RFID”, “returns”, “architecture”, “my role”, or “PRAYAAS”.';
    projectQuery?.focus();
  }
});

if(!reduceMotion&&parallaxItems.length){
  let ticking=false;
  const updateParallax=()=>{
    const vh=window.innerHeight;
    parallaxItems.forEach(item=>{
      const rect=item.getBoundingClientRect();
      if(rect.bottom<0||rect.top>vh) return;
      const center=rect.top+rect.height/2;
      const normalized=(center-vh/2)/vh;
      item.style.setProperty('--parallax',String(Math.max(-12,Math.min(12,normalized*-16))));
    });
    ticking=false;
  };
  window.addEventListener('scroll',()=>{
    if(!ticking){requestAnimationFrame(updateParallax);ticking=true;}
  },{passive:true});
  window.addEventListener('resize',updateParallax,{passive:true});
  updateParallax();
}

if(document.getElementById('year')) document.getElementById('year').textContent=new Date().getFullYear();
