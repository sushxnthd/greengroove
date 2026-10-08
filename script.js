const header=document.querySelector('.site-header');
const hero=document.querySelector('.hero');
const mobileToggle=document.querySelector('.mobile-menu-toggle');
const mobileMenu=document.querySelector('.mobile-menu');
const mobileLinks=[...document.querySelectorAll('.mobile-menu a')];
const navLinks=[...document.querySelectorAll('.desktop-nav .nav-link')];
const revealItems=[...document.querySelectorAll('.reveal')];
const staggerGroups=[...document.querySelectorAll('.stagger-group')];
const parallaxItems=[...document.querySelectorAll('.media-parallax')];
const roleTabs=[...document.querySelectorAll('.role-tab')];
const rolePanels=[...document.querySelectorAll('.role-copy')];
const rolePanel=document.querySelector('.role-panel');
const mediaTrack=document.querySelector('.media-track');
const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* Admissions-facing polish: preserve expandable media areas without exposing placeholder language. */
const heroStatus=document.querySelector('.hero-meta div:nth-child(3) strong');
if(heroStatus) heroStatus.textContent='NCERT PRAYAAS · ₹50K reported support';

const featureCaption=document.querySelector('.feature-media figcaption');
if(featureCaption){
  const parts=featureCaption.querySelectorAll('span');
  if(parts[0]) parts[0].textContent='Project visual';
  if(parts[1]) parts[1].textContent='Product + system exploration';
}

const mediaNativeCopy=[
  ['Prototype evidence','Hardware / wristband photography','Physical build evidence: wristband, shelf and component detail.'],
  ['Field evidence','In-store demo / test sequence','Shopper interaction, pick/return sequence, or field-test evidence.'],
  ['Hardware detail','RFID / electronics close-up','RFID, load sensing, electronics or shelf-build evidence.']
];
document.querySelectorAll('.media-native').forEach((card,index)=>{
  const copy=mediaNativeCopy[index];
  if(!copy) return;
  const label=card.querySelector('span');
  const title=card.querySelector('h3');
  const body=card.querySelector('p');
  if(label) label.textContent=copy[0];
  if(title) title.textContent=copy[1];
  if(body) body.textContent=copy[2];
});

const galleryHeading=document.querySelector('.media-gallery .split-heading h2');
const galleryDeck=document.querySelector('.media-gallery .split-heading p');
if(galleryHeading) galleryHeading.textContent='Visual evidence, from concept to system.';
if(galleryDeck) galleryDeck.textContent='The media system is deliberately expandable: prototype photography, electronics close-ups, system diagrams, field-test frames and process evidence can slot into the same visual language.';

document.querySelectorAll('.gallery-native').forEach((card,index)=>{
  const body=card.querySelector('p');
  if(!body) return;
  body.textContent=index===0?'RFID, electronics and shelf-sensing evidence.':'Shopper interaction, demo footage or an annotated test sequence.';
});

const riskTags={
  'edge-return':'Core invariant',
  'edge-sensors':'High-priority unknown',
  'edge-overlap':'Association risk',
  'edge-identity':'Foundational constraint'
};
Object.entries(riskTags).forEach(([id,label])=>{
  const top=document.querySelector(`#${id} .risk-top`);
  if(!top||top.querySelector('.risk-priority')) return;
  const tag=document.createElement('span');
  tag.className='risk-priority';
  tag.textContent=label;
  top.appendChild(tag);
});

const roleArtifacts={
  research:['problem framing','assumptions','failure questions'],
  architecture:['identity','event','cart','settlement'],
  interaction:['shopper action','system response','uncertainty'],
  prototyping:['visual model','critique','iteration']
};
rolePanels.forEach(panel=>{
  const key=panel.dataset.rolePanel;
  const items=roleArtifacts[key];
  if(!items||panel.querySelector('.role-artifact')) return;
  const artifact=document.createElement('div');
  artifact.className=`role-artifact role-artifact-${key}`;
  artifact.innerHTML=items.map((item,index)=>`<span><i>${String(index+1).padStart(2,'0')}</i>${item}</span>`).join('<b>→</b>');
  panel.appendChild(artifact);
});

requestAnimationFrame(()=>requestAnimationFrame(()=>hero?.classList.add('ready')));

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
    item.style.setProperty('--delay',`${Math.min(index*85,340)}ms`);
  });
});

if('IntersectionObserver' in window){
  const revealObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('in');
        revealObserver.unobserve(entry.target);
      }
    });
  },{threshold:.08,rootMargin:'0px 0px -42px'});
  revealItems.forEach(item=>revealObserver.observe(item));
}else{
  revealItems.forEach(item=>item.classList.add('in'));
}

const navTargets={
  research:'#research',
  system:'#system',
  architecture:'#system',
  engineering:'#engineering',
  method:'#engineering',
  validation:'#validation',
  contribution:'#contribution',
  next:'#contribution',
  archive:'#contribution',
  reflection:'#contribution',
  team:'#contribution'
};
const trackedSections=[...document.querySelectorAll('main section[id]')].filter(section=>navTargets[section.id]);
if('IntersectionObserver' in window){
  const navObserver=new IntersectionObserver(entries=>{
    const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
    if(!visible[0]) return;
    const href=navTargets[visible[0].target.id];
    navLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===href));
  },{rootMargin:'-24% 0px -62% 0px',threshold:[0,.16,.35,.6]});
  trackedSections.forEach(section=>navObserver.observe(section));
}

let roleSwitchTimer;
roleTabs.forEach(tab=>tab.addEventListener('click',()=>{
  if(tab.classList.contains('active')) return;
  const role=tab.dataset.role;
  roleTabs.forEach(item=>item.classList.toggle('active',item===tab));
  clearTimeout(roleSwitchTimer);
  rolePanel?.classList.add('switching');
  roleSwitchTimer=setTimeout(()=>{
    rolePanels.forEach(panel=>panel.classList.toggle('active',panel.dataset.rolePanel===role));
    requestAnimationFrame(()=>rolePanel?.classList.remove('switching'));
  },150);
}));

if(!reduceMotion&&parallaxItems.length){
  let ticking=false;
  const updateParallax=()=>{
    const vh=window.innerHeight;
    parallaxItems.forEach(item=>{
      const rect=item.getBoundingClientRect();
      if(rect.bottom<0||rect.top>vh) return;
      const center=rect.top+rect.height/2;
      const normalized=(center-vh/2)/vh;
      item.style.setProperty('--parallax',String(Math.max(-14,Math.min(14,normalized*-18))));
    });
    ticking=false;
  };
  const requestParallax=()=>{
    if(!ticking){requestAnimationFrame(updateParallax);ticking=true;}
  };
  window.addEventListener('scroll',requestParallax,{passive:true});
  window.addEventListener('resize',requestParallax,{passive:true});
  updateParallax();
}

if(mediaTrack){
  let dragging=false;
  let startX=0;
  let startScroll=0;
  mediaTrack.addEventListener('pointerdown',event=>{
    dragging=true;
    startX=event.clientX;
    startScroll=mediaTrack.scrollLeft;
    mediaTrack.setPointerCapture?.(event.pointerId);
    mediaTrack.style.cursor='grabbing';
  });
  mediaTrack.addEventListener('pointermove',event=>{
    if(!dragging) return;
    mediaTrack.scrollLeft=startScroll-(event.clientX-startX);
  });
  const endDrag=()=>{dragging=false;mediaTrack.style.cursor='grab';};
  mediaTrack.addEventListener('pointerup',endDrag);
  mediaTrack.addEventListener('pointercancel',endDrag);
  mediaTrack.addEventListener('lostpointercapture',endDrag);
}

if(document.getElementById('year')) document.getElementById('year').textContent=new Date().getFullYear();
