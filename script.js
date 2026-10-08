const header=document.querySelector('.site-header');
const mobileToggle=document.querySelector('.mobile-menu-toggle');
const mobileMenu=document.querySelector('.mobile-menu');
const mobileLinks=[...document.querySelectorAll('.mobile-menu a')];
const navGroups=[...document.querySelectorAll('.nav-group')];
const revealItems=[...document.querySelectorAll('.reveal')];
const explorer=document.querySelector('#project-explorer');
const projectQuery=document.querySelector('#project-query');
const feedback=document.querySelector('#explorer-feedback');
const moreTrigger=document.querySelector('.more-links-trigger');

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

navGroups.forEach(group=>{
  const trigger=group.querySelector('.nav-trigger');
  trigger?.addEventListener('click',event=>{
    event.stopPropagation();
    navGroups.forEach(other=>{if(other!==group) other.classList.remove('open');});
    group.classList.toggle('open');
  });
});
document.addEventListener('click',()=>navGroups.forEach(group=>group.classList.remove('open')));
document.addEventListener('keydown',event=>{
  if(event.key==='Escape'){
    navGroups.forEach(group=>group.classList.remove('open'));
    if(mobileMenu?.classList.contains('open')) mobileToggle?.click();
  }
});

const observer=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){
      entry.target.classList.add('in');
      observer.unobserve(entry.target);
    }
  });
},{threshold:.08,rootMargin:'0px 0px -36px'});
revealItems.forEach(item=>observer.observe(item));

const destinations={
  overview:['overview','green groove','project','what is','summary'],
  architecture:['system','architecture','flow','how it works','checkout','transaction'],
  components:['components','band','wristband','rfid','shelf','cart','live cart'],
  engineering:['engineering','edge cases','failure','failures','ambiguity','uncertainty'],
  'edge-return':['return','returns','put back','inverse'],
  'edge-sensors':['sensor','sensors','disagree','disagreement','signal','weight'],
  'edge-overlap':['simultaneous','overlap','two shoppers','association'],
  'edge-identity':['identity','session','persistent','shopper id'],
  contribution:['role','my role','contribution','my work','sushanth'],
  evidence:['evidence','validation','prayaas','ncert','grant','50000','50k'],
  reflection:['reflection','learned','learning','what changed','lesson'],
  team:['team','aryan','members']
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
  target.scrollIntoView({behavior:'smooth',block:'start'});
  return true;
}

explorer?.addEventListener('submit',event=>{
  event.preventDefault();
  const value=projectQuery?.value||'';
  const destination=findDestination(value);
  if(destination&&goToSection(destination)){
    if(feedback) feedback.textContent=`Opening ${value.trim()}…`;
  }else{
    if(feedback) feedback.textContent='Try “RFID”, “returns”, “architecture”, “my role”, or “PRAYAAS”.';
    projectQuery?.focus();
  }
});

moreTrigger?.addEventListener('click',()=>{
  if(feedback) feedback.textContent='Try “returns”, “sensor disagreement”, “team”, “reflection”, or “PRAYAAS”.';
  projectQuery?.focus();
});

if(document.getElementById('year')) document.getElementById('year').textContent=new Date().getFullYear();
