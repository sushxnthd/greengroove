(()=>{
  const q=(s,r=document)=>r.querySelector(s),qa=(s,r=document)=>[...r.querySelectorAll(s)];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ease='cubic-bezier(.16,1,.3,1)';
  requestAnimationFrame(()=>requestAnimationFrame(()=>document.body.classList.add('gg-ready')));

  // Osmo radial marquee: duplicate once, rotate continuously, pause offscreen.
  qa('[data-radial-marquee]').forEach(root=>{
    if(root.dataset.ggInit)return;
    const ring=q('[data-radial-marquee-rotate]',root);if(!ring)return;
    [...ring.children].forEach(child=>ring.appendChild(child.cloneNode(true)));
    ring.style.animationPlayState='paused';
    const obs=new IntersectionObserver(es=>es.forEach(e=>ring.style.animationPlayState=e.isIntersecting&&!document.hidden?'running':'paused'),{threshold:0});
    obs.observe(ring);
    document.addEventListener('visibilitychange',()=>ring.style.animationPlayState=document.hidden?'paused':'running');
    root.dataset.ggInit='1';
  });

  // Navigation state / scroll-direction behavior.
  const nav=q('.nav');
  const setNav=open=>{nav?.setAttribute('data-nav-status',open?'active':'not-active');document.body.classList.toggle('nav-open',open)};
  qa('[data-nav-toggle]').forEach(el=>el.addEventListener('click',()=>el.getAttribute('data-nav-toggle')==='close'?setNav(false):setNav(nav?.getAttribute('data-nav-status')!=='active')));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')setNav(false)});
  let lastY=scrollY,scrollRAF=false;
  addEventListener('scroll',()=>{if(scrollRAF)return;scrollRAF=true;requestAnimationFrame(()=>{const y=scrollY;nav?.setAttribute('data-scrolling-direction',y>lastY?'down':'up');nav?.setAttribute('data-scrolling-started',y>40?'true':'false');lastY=y;scrollRAF=false})},{passive:true});

  // CSS marquees require two identical lists for a seamless loop.
  qa('[data-css-marquee]').forEach(m=>{const lists=qa('[data-css-marquee-list]',m);if(lists.length===1)m.appendChild(lists[0].cloneNode(true))});

  // Source-equivalent vertical slider geometry, implemented without GSAP.
  function initVerticalSlider(root){
    const list=q('[data-vertical-slider-list]',root);if(!list)return;
    const items=qa('[data-vertical-slider-item]',root);if(items.length<5)return;
    const bullets=qa('[data-vertical-slider-bullet]',root),prev=q('[data-prev]',root),next=q('[data-next]',root),buttonWrap=q('[data-button-wrap]',root);
    const fade=root.hasAttribute('data-fade-slides'),mobile=innerWidth<768,d=mobile?40:30,z=mobile?26:20,rx=mobile?70:60;
    const states={
      '-2':{y:d,z:-z,rx:-rx,o:0},'-1':{y:d,z:-z,rx:-rx,o:fade?0:1},
      '0':{y:0,z:0,rx:0,o:1},'1':{y:-d,z:-z,rx:rx,o:fade?0:1},'2':{y:-d,z:-z,rx:rx,o:0}
    };
    let active=bullets.findIndex(b=>b.getAttribute('data-vertical-slider-bullet')==='active');if(active<0)active=items.findIndex(i=>i.hasAttribute('data-initial'));if(active<0)active=0;
    let timer=null,paused=false;
    const rel=(i,a)=>{let r=((i-a)%items.length+items.length)%items.length;if(r>Math.floor(items.length/2))r-=items.length;return Math.max(-2,Math.min(2,r))};
    const paint=(instant=false)=>{
      items.forEach((item,i)=>{const r=rel(i,active),s=states[String(r)];item.style.transformOrigin='50% 50%';item.style.transition=instant?'none':`transform .725s ${ease},opacity .725s ${ease}`;item.style.transform=`translate3d(0,${s.y}em,${s.z}em) rotateX(${s.rx}deg)`;item.style.opacity=s.o;const is=i===active;item.setAttribute('aria-hidden',String(!is));item.tabIndex=is?0:-1;item.style.zIndex=is?'2':'1';item.style.pointerEvents=is?'auto':'none'});
      bullets.forEach((b,i)=>{const is=i===active;b.setAttribute('data-vertical-slider-bullet',is?'active':'not-active');b.setAttribute('aria-current',is?'true':'false')});
      const current=items[active]?.getAttribute('data-slide-map');if(current)qa('[data-testimonial-map]',root).forEach(m=>m.classList.toggle('is--active',m.getAttribute('data-testimonial-map')===current));
    };
    const stop=()=>{clearTimeout(timer);timer=null};
    const autoplay=()=>{stop();if(reduce||paused||root.dataset.autoplay!=='true')return;const ms=parseInt(root.dataset.autoplayDuration||'0',10)||4000;timer=setTimeout(()=>go(active+1),ms)};
    const go=i=>{active=(i+items.length)%items.length;paint();autoplay()};
    prev?.addEventListener('click',()=>go(active-1));next?.addEventListener('click',()=>go(active+1));
    bullets.forEach((b,i)=>b.addEventListener('click',()=>go(i)));
    buttonWrap?.addEventListener('mouseenter',()=>{paused=true;stop()});buttonWrap?.addEventListener('mouseleave',()=>{paused=false;autoplay()});
    const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)autoplay();else stop()}),{threshold:.08});io.observe(root);
    paint(true);requestAnimationFrame(()=>items.forEach(i=>i.style.transition='transform .725s '+ease+',opacity .725s '+ease));
  }
  qa('[data-vertical-slider]').forEach(initVerticalSlider);

  // Source reel reveal proportions.
  const reel=q('[data-reel-row]');if(reel&&!reduce){const visual=q('[data-reel-visual]',reel),circle=q('[data-reel-circle]',reel),txt=q('[data-reel-visual-text]',reel),scrib=q('[data-reel-scribble]',reel);if(visual){visual.style.width='0em';[circle,txt,scrib].filter(Boolean).forEach(x=>x.style.opacity='0');const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;visual.style.transition=`width 1s ${ease}`;visual.style.width='16em';if(circle){circle.style.transition=`opacity 1s .1s ${ease},transform 1.4s ${ease}`;circle.style.opacity='1';circle.style.transform='rotate(0) scale(1)'}if(txt){txt.style.transition='opacity .8s .5s ease';txt.style.opacity='1'}if(scrib){scrib.style.transition=`opacity .8s .65s ease,transform 1s .65s ${ease}`;scrib.style.opacity='1';scrib.style.transform='none'}io.disconnect()}),{threshold:.25});if(circle)circle.style.transform='rotate(180deg) scale(.5)';if(scrib)scrib.style.transform='translateY(25%) rotate(3deg)';io.observe(reel)}}

  // Osmo product slider: same curved carousel status/rotation model.
  qa('[data-gsap-slider-init]').forEach(root=>{
    const viewport=q('[data-gsap-slider-collection]',root),track=q('[data-gsap-slider-list]',root),items=qa('[data-gsap-slider-item]',root),controls=qa('[data-gsap-slider-control]',root);if(!viewport||!track||!items.length)return;
    const rotation=parseFloat(root.getAttribute('data-gsap-slider-rotate'))||0;let active=0,drag=false,startX=0,virtual=0,startVirtual=0;
    const mod=(n,m)=>(n%m+m)%m;
    const render=()=>{
      if(rotation>0){const w=items[0].getBoundingClientRect().width||1;const gap=parseFloat(getComputedStyle(items[0]).marginRight)||0;const step=w||w+gap;items.forEach((it,i)=>{let d=i-virtual;while(d>items.length/2)d-=items.length;while(d<-items.length/2)d+=items.length;it.style.position='absolute';it.style.left='50%';it.style.top='0';it.style.marginRight='0';it.style.transform=`translateX(calc(-50% + ${d*step}px)) rotate(${d*rotation}deg)`;it.style.transition=drag?'none':`transform .8s ${ease}`;it.setAttribute('data-gsap-slider-item-status',Math.round(d)===0?'active':Math.abs(d)<=2?'inview':'not-active')});track.style.position='relative';track.style.height=(items[0].getBoundingClientRect().height||0)+'px';active=mod(Math.round(virtual),items.length)}else{
        const item=items[0],step=(item.getBoundingClientRect().width||1)+(parseFloat(getComputedStyle(item).marginRight)||0);track.style.transition=drag?'none':`transform .8s ${ease}`;track.style.transform=`translate3d(${-active*step}px,0,0)`;items.forEach((it,i)=>it.setAttribute('data-gsap-slider-item-status',i===active?'active':Math.abs(i-active)<3?'inview':'not-active'));
      }
      controls.forEach(c=>{const raw=c.getAttribute('data-gsap-slider-control');if(/^\d+$/.test(raw))c.setAttribute('data-gsap-slider-control-status',+raw-1===active?'active':'not-active')});
    };
    controls.forEach(c=>c.addEventListener('click',()=>{const raw=c.getAttribute('data-gsap-slider-control');if(raw==='next')rotation?virtual++:active=Math.min(items.length-1,active+1);else if(raw==='prev')rotation?virtual--:active=Math.max(0,active-1);else if(/^\d+$/.test(raw)){rotation?virtual=+raw-1:active=+raw-1}render()}));
    viewport.style.touchAction='pan-y';viewport.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;drag=true;startX=e.clientX;startVirtual=virtual;viewport.setPointerCapture?.(e.pointerId);root.setAttribute('data-gsap-drag-status','grabbing')});viewport.addEventListener('pointermove',e=>{if(!drag)return;if(rotation){const w=items[0].getBoundingClientRect().width||1;virtual=startVirtual-(e.clientX-startX)/w}else{const w=items[0].getBoundingClientRect().width||1;active=Math.round(Math.max(0,Math.min(items.length-1,startVirtual-(e.clientX-startX)/w)))}render()});const release=()=>{if(!drag)return;drag=false;virtual=Math.round(virtual);root.setAttribute('data-gsap-drag-status','grab');render()};viewport.addEventListener('pointerup',release);viewport.addEventListener('pointercancel',release);render();
  });

  // Pricing toggle preserves source data attributes.
  const pricing=q('[data-pricing-section-status]');if(pricing){qa('[data-pricing-button]',pricing).forEach(btn=>btn.addEventListener('click',()=>{const val=btn.getAttribute('data-pricing-button');pricing.setAttribute('data-pricing-section-status',val);qa('[data-pricing-state]',pricing).forEach(el=>el.setAttribute('data-pricing-state',val))}))}

  // Source flick-card stacking geometry and drag threshold.
  qa('[data-flick-cards-init]').forEach(group=>{const list=q('[data-flick-cards-list]',group),cards=qa('[data-flick-cards-item]',group);if(!list||cards.length<3)return;let active=0,down=false,startX=0;const state=(i,a)=>{let d=i-a,n=cards.length;if(d>n/2)d-=n;if(d<-n/2)d+=n;if(d===0)return[0,0,0,1,1,5,'active'];if(d===1)return[25,5,5,.9,1,4,'2-after'];if(d===-1)return[-25,5,-5,.9,1,4,'2-before'];if(d===2)return[45,7,10,.75,1,3,'3-after'];if(d===-2)return[-45,7,-10,.75,1,3,'3-before'];const s=d>0?1:-1;return[55*s,5,15*s,.6,0,2,'hidden']};const paint=()=>cards.forEach((c,i)=>{const v=state(i,active);c.setAttribute('data-flick-cards-item-status',v[6]);c.style.zIndex=v[5];c.style.transition=`transform .6s cubic-bezier(.22,1,.36,1),opacity .45s`;c.style.transform=`translate(${v[0]}%,${v[1]}%) rotate(${v[2]}deg) scale(${v[3]})`;c.style.opacity=v[4]});paint();group.setAttribute('data-flick-drag-status','grab');group.addEventListener('pointerdown',e=>{down=true;startX=e.clientX;group.setPointerCapture?.(e.pointerId);group.setAttribute('data-flick-drag-status','grabbing')});group.addEventListener('pointerup',e=>{if(!down)return;down=false;group.setAttribute('data-flick-drag-status','grab');const dx=e.clientX-startX;if(dx>35)active=(active-1+cards.length)%cards.length;else if(dx<-35)active=(active+1)%cards.length;paint()});group.addEventListener('pointercancel',()=>{down=false;group.setAttribute('data-flick-drag-status','grab')})});

  const applyLabels=()=>qa('[data-gg-module]').forEach(el=>{const visual=q('.radial-marquee__card-visual,[class*="visual"],.showcase-media',el);visual?.setAttribute('data-gg-label',el.getAttribute('data-gg-module'))});applyLabels();setTimeout(applyLabels,50);

  qa('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{const href=a.getAttribute('href');if(!href||href==='#')return;const t=q(href);if(!t)return;e.preventDefault();setNav(false);scrollTo({top:t.getBoundingClientRect().top+scrollY-110,behavior:reduce?'auto':'smooth'})}));
  qa('[data-current-year],#year').forEach(el=>el.textContent=new Date().getFullYear());
})();