const header=document.querySelector('.site-header');
const menu=document.querySelector('.menu');
window.addEventListener('scroll',()=>header?.classList.toggle('scrolled',scrollY>12),{passive:true});
menu?.addEventListener('click',()=>{const open=header.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
document.querySelectorAll('.desktop-nav a').forEach(a=>a.addEventListener('click',()=>{header.classList.remove('open');menu?.setAttribute('aria-expanded','false');}));
const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{threshold:.1,rootMargin:'0px 0px -40px'});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
document.getElementById('year').textContent=new Date().getFullYear();
