(()=>{
  const q=(s,r=document)=>r.querySelector(s), qa=(s,r=document)=>[...r.querySelectorAll(s)];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  requestAnimationFrame(()=>requestAnimationFrame(()=>document.body.classList.add('gg-ready')));
  qa('[data-radial-marquee]').forEach(root=>{
    if(root.dataset.ggInit)return;
    const rotate=q('[data-radial-marquee-rotate]',root);
    if(!rotate)return;
    [...rotate.children].forEach(child=>rotate.appendChild(child.cloneNode(true)));
    const observer=new IntersectionObserver(entries=>entries.forEach(e=>{rotate.style.animationPlayState=e.isIntersecting&&!document.hidden?'running':'paused'}),{threshold:0});
    observer.observe(rotate);
    document.addEventListener('visibilitychange',()=>{rotate.style.animationPlayState=document.hidden?'paused':'running'});
    root.dataset.ggInit='1';
  });
  const nav=q('.nav');
  const setNav=open=>{nav?.setAttribute('data-nav-status',open?'active':'not-active');document.body.classList.toggle('nav-open',open)};
  qa('[data-nav-toggle]').forEach(el=>el.addEventListener('click',()=>{const action=el.getAttribute('data-nav-toggle');if(action==='close')setNav(false);else setNav(nav?.getAttribute('data-nav-status')!=='active')}));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')setNav(false)});
  let lastY=scrollY,raf=false;
  addEventListener('scroll',()=>{if(raf)return;raf=true;requestAnimationFrame(()=>{const y=scrollY,dir=y>lastY?'down':'up';nav?.setAttribute('data-scrolling-direction',dir);nav?.setAttribute('data-scrolling-started',y>40?'true':'false');lastY=y;raf=false})},{passive:true});
  qa('[data-css-marquee]').forEach(m=>{const lists=qa('[data-css-marquee-list]',m);if(lists.length===1)m.appendChild(lists[0].cloneNode(true))});
  qa('[data-gsap-slider-init], .latest-resources-slider, .flick-group').forEach(root=>{
    const track=q('[data-gsap-slider-list]',root)||q('.latest-resources-slider__list',root)||q('.flick-group__list',root)||q('.gsap-slider__list',root);
    const viewport=q('[data-gsap-slider-collection]',root)||q('.latest-resources-slider__collection',root)||q('.flick-group__collection',root)||root;
    if(!track||!viewport)return;
    let down=false,start=0,base=0,current=0,max=0;
    const measure=()=>{max=Math.min(0,viewport.clientWidth-track.scrollWidth)};measure();addEventListener('resize',measure);
    viewport.style.touchAction='pan-y';
    viewport.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;down=true;start=e.clientX;base=current;viewport.setPointerCapture?.(e.pointerId);root.setAttribute('data-gsap-drag-status','grabbing')});
    viewport.addEventListener('pointermove',e=>{if(!down)return;current=Math.max(max,Math.min(0,base+e.clientX-start));track.style.transform=`translate3d(${current}px,0,0)`});
    const up=()=>{down=false;root.setAttribute('data-gsap-drag-status','grab')};viewport.addEventListener('pointerup',up);viewport.addEventListener('pointercancel',up);
  });
  const slider=q('.product-slider .gsap-slider');
  if(slider){const items=qa('[data-gsap-slider-item], .gsap-slider__item',slider);qa('[data-gsap-slider-control]',slider).forEach(control=>control.addEventListener('click',()=>{const raw=control.getAttribute('data-gsap-slider-control');if(!/^\d+$/.test(raw))return;const item=items[Math.max(0,+raw-1)];item?.scrollIntoView({behavior:reduce?'auto':'smooth',block:'nearest',inline:'center'})}))}
  const pricing=q('[data-pricing-section-status]');
  if(pricing){qa('[data-pricing-button]',pricing).forEach(btn=>btn.addEventListener('click',()=>{const next=pricing.getAttribute('data-pricing-section-status')==='annually'?'quarterly':'annually';pricing.setAttribute('data-pricing-section-status',next);qa('[data-pricing-state]',pricing).forEach(el=>el.setAttribute('data-pricing-state',next))}))}
  qa('[data-flick-cards-init], .flick-group').forEach(group=>{
    const list=q('[data-flick-cards-list]',group)||q('.flick-group__list',group);if(!list)return;
    const cards=[...list.children].filter(x=>x.nodeType===1);if(cards.length<3)return;
    let active=0,down=false,startX=0;
    const paint=()=>cards.forEach((c,i)=>{let d=i-active;if(d>cards.length/2)d-=cards.length;if(d<-cards.length/2)d+=cards.length;const map={0:[0,0,0,1,1,5],1:[25,5,5,.9,1,4],'-1':[-25,5,-5,.9,1,4],2:[45,7,10,.75,1,3],'-2':[-45,7,-10,.75,1,3]};const v=map[d]||[55*Math.sign(d||1),5,15*Math.sign(d||1),.6,0,2];Object.assign(c.style,{transform:`translate(${v[0]}%,${v[1]}%) rotate(${v[2]}deg) scale(${v[3]})`,opacity:v[4],zIndex:v[5],transition:'transform .6s cubic-bezier(.22,1,.36,1),opacity .45s'})});
    paint();group.addEventListener('pointerdown',e=>{down=true;startX=e.clientX;group.setPointerCapture?.(e.pointerId)});group.addEventListener('pointerup',e=>{if(!down)return;down=false;const dx=e.clientX-startX;if(Math.abs(dx)>35){active=(active+(dx<0?1:-1)+cards.length)%cards.length;paint()}})
  });
  const applyLabels=()=>qa('[data-gg-module]').forEach(el=>{const visual=q('.radial-marquee__card-visual,[class*="visual"],.showcase-media',el);visual?.setAttribute('data-gg-label',el.getAttribute('data-gg-module'))});
  applyLabels();setTimeout(applyLabels,50);
  qa('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const href=a.getAttribute('href');if(!href||href==='#')return;const t=q(href);if(!t)return;e.preventDefault();setNav(false);const y=t.getBoundingClientRect().top+scrollY-110;scrollTo({top:y,behavior:reduce?'auto':'smooth'})}));
  qa('[data-current-year], #year').forEach(el=>el.textContent=new Date().getFullYear());
})();
