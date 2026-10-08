const sidebar=document.querySelector('.left-sidebar');
const sidebarToggle=document.querySelector('.sidebar-toggle');
const navLinks=[...document.querySelectorAll('.nav-item[href^="#"]')];
const tocLinks=[...document.querySelectorAll('.toc-link')];
const sections=[...document.querySelectorAll('.doc-section[id]')];
const searchTrigger=document.querySelector('.search-trigger');
const searchDialog=document.querySelector('.search-dialog');
const searchBackdrop=document.querySelector('.search-backdrop');
const searchInput=document.querySelector('#project-search');
const searchResults=[...document.querySelectorAll('#search-results a')];
const codeTabs=[...document.querySelectorAll('.code-tab')];
const codePanels=[...document.querySelectorAll('.code-panel')];

sidebarToggle?.addEventListener('click',()=>{
  const open=sidebar?.classList.toggle('open');
  sidebarToggle.setAttribute('aria-expanded',String(Boolean(open)));
});

navLinks.forEach(link=>link.addEventListener('click',()=>{
  sidebar?.classList.remove('open');
  sidebarToggle?.setAttribute('aria-expanded','false');
}));

function setActive(id){
  navLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===`#${id}`));
  tocLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===`#${id}`));
}

const sectionObserver=new IntersectionObserver(entries=>{
  const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
  if(visible[0]) setActive(visible[0].target.id);
},{rootMargin:'-18% 0px -62% 0px',threshold:[0,.15,.4,.7]});
sections.forEach(section=>sectionObserver.observe(section));

codeTabs.forEach(tab=>tab.addEventListener('click',()=>{
  const target=tab.dataset.tab;
  codeTabs.forEach(item=>item.classList.toggle('active',item===tab));
  codePanels.forEach(panel=>panel.classList.toggle('active',panel.dataset.panel===target));
}));

function openSearch(){
  if(!searchDialog) return;
  searchDialog.hidden=false;
  requestAnimationFrame(()=>searchInput?.focus());
}
function closeSearch(){
  if(!searchDialog) return;
  searchDialog.hidden=true;
  if(searchInput){searchInput.value='';filterResults('');}
}
function filterResults(value){
  const q=value.trim().toLowerCase();
  searchResults.forEach(item=>{
    const haystack=(item.dataset.search||item.textContent||'').toLowerCase();
    item.classList.toggle('hidden',Boolean(q)&&!haystack.includes(q));
  });
}

searchTrigger?.addEventListener('click',openSearch);
searchBackdrop?.addEventListener('click',closeSearch);
searchInput?.addEventListener('input',event=>filterResults(event.target.value));
searchResults.forEach(item=>item.addEventListener('click',closeSearch));

document.addEventListener('keydown',event=>{
  if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='k'){
    event.preventDefault();
    if(searchDialog?.hidden) openSearch(); else closeSearch();
  }
  if(event.key==='Escape'&&!searchDialog?.hidden) closeSearch();
});

document.getElementById('year').textContent=new Date().getFullYear();
