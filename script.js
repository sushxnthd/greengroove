const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const revealItems=[...document.querySelectorAll('.reveal')];
const sideLinks=[...document.querySelectorAll('.side-link[href^="#"]')];
const onPageLinks=[...document.querySelectorAll('.on-page a')];
const mobileButton=document.querySelector('.mobile-menu-button');
const mobileDrawer=document.querySelector('.mobile-drawer');
const copyBrief=document.querySelector('.copy-brief');
const copyToast=document.querySelector('.copy-toast');
const statusTabs=[...document.querySelectorAll('[data-status-tab]')];
const statusPanels=[...document.querySelectorAll('[data-status-panel]')];
const modeButtons=[...document.querySelectorAll('.mode')];

const glyphSets={
  hero:['·','+','×','○','◇','□','▦','┼','⌁','◎','◉','░','▒','▓'],
  cloud:['·','·','·','○','◌','◇','✣','+','×','░','▒','▦'],
  ring:['·','+','×','○','□','┼','▦','⌁'],
  divider:['·','+','×','-','—','○','□','┼','░']
};

function seededValue(i,seed=17){
  const x=Math.sin((i+1)*12.9898+seed*78.233)*43758.5453;
  return x-Math.floor(x);
}

function buildGlyphField(el){
  const type=el.dataset.glyphField||'hero';
  const set=glyphSets[type]||glyphSets.hero;
  const styles=getComputedStyle(el);
  const cols=styles.gridTemplateColumns.split(' ').length||24;
  const rows=styles.gridTemplateRows.split(' ').length||12;
  const count=Math.min(cols*rows,650);
  const frag=document.createDocumentFragment();
  for(let i=0;i<count;i++){
    const span=document.createElement('span');
    const r=seededValue(i,type.length*11);
    span.textContent=set[Math.floor(r*set.length)%set.length];
    if(r>.92) span.classList.add('hot');
    else if(r>.82) span.classList.add('blue');
    else if(r<.28) span.classList.add('dim');
    span.style.animationDelay=`${(seededValue(i,41)*3.8).toFixed(2)}s`;
    span.style.animationDuration=`${(3+seededValue(i,71)*3).toFixed(2)}s`;
    frag.appendChild(span);
  }
  el.replaceChildren(frag);
}

document.querySelectorAll('[data-glyph-field]').forEach(buildGlyphField);

document.querySelectorAll('[data-mini-matrix]').forEach(el=>{
  const frag=document.createDocumentFragment();
  for(let i=0;i<49;i++) frag.appendChild(document.createElement('i'));
  el.appendChild(frag);
});

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
    const active=entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
    if(!active) return;
    const id=active.target.id;
    sideLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===`#${id}`));
    onPageLinks.forEach(link=>link.classList.toggle('active',link.dataset.section===id));
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
    temp.value=text;document.body.appendChild(temp);temp.select();document.execCommand('copy');temp.remove();
  }
  copyToast?.classList.add('show');
  window.setTimeout(()=>copyToast?.classList.remove('show'),1500);
});

statusTabs.forEach(tab=>tab.addEventListener('click',()=>{
  const key=tab.dataset.statusTab;
  statusTabs.forEach(t=>t.classList.toggle('active',t===tab));
  statusPanels.forEach(panel=>panel.classList.toggle('active',panel.dataset.statusPanel===key));
}));

modeButtons.forEach(button=>button.addEventListener('click',()=>{
  modeButtons.forEach(b=>b.classList.toggle('active',b===button));
  const mode=button.dataset.mode;
  if(mode==='research') document.querySelector('#evidence')?.scrollIntoView({behavior:reduceMotion?'auto':'smooth'});
  else document.querySelector('#home')?.scrollIntoView({behavior:reduceMotion?'auto':'smooth'});
}));

if(!reduceMotion){
  const matrixPoster=document.querySelector('.matrix-landscape');
  const ringPoster=document.querySelector('.ring-poster');
  let ticking=false;
  const update=()=>{
    const vh=window.innerHeight;
    [matrixPoster,ringPoster].filter(Boolean).forEach((el,index)=>{
      const r=el.getBoundingClientRect();
      if(r.bottom<0||r.top>vh) return;
      const p=((r.top+r.height/2)-vh/2)/vh;
      el.style.setProperty('--shift',`${Math.max(-12,Math.min(12,p*-10))}px`);
      if(index===1){
        el.querySelectorAll('.ring').forEach((ring,i)=>ring.style.translate=`0 ${p*(i+1)*3}px`);
      }
    });
    ticking=false;
  };
  window.addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(update);ticking=true;}},{passive:true});
  window.addEventListener('resize',update,{passive:true});
  update();
}

const year=document.getElementById('year');
if(year) year.textContent=new Date().getFullYear();
