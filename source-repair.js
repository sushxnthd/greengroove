/* Routes, control semantics and asset data for the restored source layout. */
(()=>{
 'use strict';const q=(s,r=document)=>r.querySelector(s),qa=(s,r=document)=>[...r.querySelectorAll(s)];
 const layers=[
 ['Identity','a01-identity-layer.svg','A passive RFID band establishes the shopping session. An identity read provides context; it does not prove who picked up an item.'],
 ['Shelf Events','a02-shelf-events-layer.svg','Load-cell changes and RFID observations form candidate events. Association is required before a cart changes.'],
 ['Association','a03-association-layer.svg','A unique shopper association accepts the event. Ambiguous candidates remain on hold without changing a bill.'],
 ['Reversibility','a04-reversibility-layer.svg','An accepted return appends the inverse of an earlier pickup. Both events remain visible in the history.'],
 ['Live Cart','a05-live-cart-layer.svg','Accepted events determine quantities and subtotal. Held events remain separate.'],
 ['Settlement','a06-settlement-layer.svg','The accepted cart produces an invoice summary. Payment processing is separate from invoice generation.']];
 let detailReturn=null;
 function showDetail(index,title,src,description){
  const l=layers[index]||layers[0],modal=q('[data-modal-target=showcase]'),wrap=modal.closest('[data-modal-wrap]');
  q('[data-res-used=title]',modal).textContent=title||l[0];q('[data-res-used=item-title]',modal).textContent=(title||l[0])+' · Technical illustration';
  const image=q('[data-res-used=item-img]',modal);image.src=src||'assets/visuals/'+l[1];image.alt=description||l[2];
  qa('[data-res-used=item-link]',modal).forEach(a=>a.href=image.getAttribute('src'));
  const bottom=q('[data-res-used=site-url]',modal);bottom.href='#architecture';bottom.setAttribute('aria-label','View system section');bottom.removeAttribute('target');
  let copy=q('.source-detail-copy',modal);if(!copy){copy=document.createElement('p');copy.className='p-m source-detail-copy';q('.used-resource-card__info',modal).append(copy)}copy.textContent=description||l[2];
  qa('[data-res-used=author-name-1] .eyebrow',modal).forEach(e=>e.textContent='Sushanth Dasari');qa('[data-res-used=author-name-2] .eyebrow',modal).forEach(e=>e.textContent='Aryan Kumar');
  detailReturn=document.activeElement;modal.inert=false;closeNavigation();wrap._modals.open('showcase',detailReturn);
 }
 function showBuild(card){const hit=q('[data-gg-build]',card),i=+hit.dataset.ggBuild;showDetail([0,1,4,0,1,4,3][i],card.dataset.ggBuildTitle,q('.showcase-media__image',card)?.getAttribute('src'))}
 function sync(){
  const nav=q('.nav'),open=nav.getAttribute('data-nav-status')==='active',toggle=q('[data-nav-toggle=toggle]');toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu');
  const panel=q('.nav-bar__bottom');if(panel)panel.inert=!open;
  qa('[data-gsap-slider-control]').forEach(b=>b.setAttribute('aria-pressed',String(b.getAttribute('data-gsap-slider-control-status')==='active')));
  qa('[data-vertical-slider-item]').forEach(e=>{const hidden=e.getAttribute('aria-hidden')==='true';if(e.inert!==hidden)e.inert=hidden});
  qa('[data-modal-target]').forEach(e=>{const hidden=e.getAttribute('data-modal-status')!=='active';if(e.inert!==hidden)e.inert=hidden});
  qa('.footer-link__col').forEach(e=>{const top=q('.footer-link__col-top',e),bottom=q('.footer-link__col-bottom',e);if(!top||!bottom)return;const mobile=innerWidth<=767,expanded=!mobile||e.getAttribute('data-accordion-status')==='active';top.tabIndex=mobile?0:-1;top.setAttribute('aria-expanded',String(expanded));if(mobile)top.setAttribute('role','button');else top.removeAttribute('role');bottom.inert=!expanded});
 }
 function start(){
  const navDemo=q('[data-gg-nav-demo]');
  if(navDemo){
   const motion=matchMedia('(prefers-reduced-motion: reduce)');
   const updateNavDemo=()=>navDemo.src=(motion.matches||new URLSearchParams(location.search).get('motion')==='reduce')?'assets/media/greengroove-demo-poster.webp':'assets/media/greengroove-demo-nav.gif';
   updateNavDemo();motion.addEventListener('change',updateNavDemo);
  }
  const dialog=q('#gg-demo-player'),player=q('video',dialog),preview=q('[data-gg-preview]');
  const closeDemo=()=>{player.pause();player.currentTime=0;document.body.classList.remove('gg-demo-open');};
  dialog.addEventListener('close',()=>{closeDemo();q('[data-gg-demo]')?.focus();});
  q('.gg-demo-close',dialog).addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  if(preview && !prefersRM){
   const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting && !dialog.open)preview.play().catch(()=>{});else preview.pause();}),{threshold:.25});observer.observe(preview);
  }

  sync();new MutationObserver(sync).observe(document.body,{subtree:true,attributes:true,attributeFilter:['data-nav-status','data-gsap-slider-control-status','data-modal-status','aria-hidden','data-accordion-status']});addEventListener('resize',sync,{passive:true});
  const evidence=q('#evidence'),cards=qa('.pricing-card',evidence),buttons=qa('[data-pricing-button]',evidence);
  evidence.setAttribute('data-pricing-section-status','quarterly');
  const saved=cards.map(c=>({title:q('.pricing-card__title',c).textContent,copy:q('.gg-card-description',c)?.innerHTML}));
  buttons.forEach(b=>b.addEventListener('click',()=>{const next=b.textContent.trim().startsWith('Next');evidence.setAttribute('data-pricing-section-status',next?'annually':'quarterly');buttons.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
   cards.forEach((c,i)=>{q('.pricing-card__title',c).textContent=next?['Technical testing','Field evaluation'][i]:saved[i].title;const p=q('.gg-card-description',c);if(p)p.innerHTML=next?['<span class="gg-card-lead">Planned: controlled tests of calibration, shopper association and reversible event recovery.</span><span class="gg-card-support">Document event-level errors and test conditions before making performance claims.</span>','<span class="gg-card-lead">Planned: evaluate the prototype under documented retail conditions.</span><span class="gg-card-support">Record ambiguity, operational recovery and store feedback. Field results are not yet claimed.</span>'][i]:saved[i].copy;
   });
  }));buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.textContent.includes('Today'))));
  const form=q('footer form');form?.addEventListener('submit',e=>{e.preventDefault();window.open('https://github.com/sushxnthd/greengroove','_blank','noopener,noreferrer')});
  qa('[data-current-year]').forEach(e=>e.textContent=new Date().getFullYear());document.body.classList.add('gg-repair-ready');
 }
 document.addEventListener('click',e=>{
  const demo=e.target.closest('[data-gg-demo]');if(demo){e.preventDefault();e.stopImmediatePropagation();const dialog=q('#gg-demo-player');q('[data-gg-preview]')?.pause();dialog.showModal();document.body.classList.add('gg-demo-open');q('video',dialog).play().catch(()=>{});return}
  const layer=e.target.closest('[data-gg-detail]');if(layer){e.preventDefault();e.stopImmediatePropagation();showDetail(+layer.dataset.ggDetail);return}
  const build=e.target.closest('[data-gg-build]');if(build){e.preventDefault();e.stopImmediatePropagation();showBuild(build.closest('[data-gg-build-title]'));return}
  const activeBuild=e.target.closest('[data-gg-active-build]');if(activeBuild){e.preventDefault();e.stopImmediatePropagation();showBuild(q('[data-flick-cards-item-status=active]'));return}
  const map=e.target.closest('[data-gg-map]');if(map){e.preventDefault();e.stopImmediatePropagation();showDetail(0,'Six-layer system','assets/visuals/a07-full-six-layer-architecture.svg','Identity, shelf events, association, reversibility, the live cart and settlement form one retail-state model. This is a technical illustration of the prototype design.');return}
  const road=e.target.closest('[data-gg-roadmap]');if(road){e.preventDefault();e.stopImmediatePropagation();showDetail(1,'Validation roadmap','assets/visuals/e04-validation-roadmap.svg','Controlled testing and field evaluation remain planned development work.');return}
  const theme=e.target.closest('[data-gg-theme]');if(theme){e.preventDefault();q('[data-marketing-theme]').setAttribute('data-marketing-theme',theme.dataset.ggTheme);qa('[data-gg-theme]').forEach(x=>x.setAttribute('aria-pressed',String(x===theme)));return}
  const a=e.target.closest('a[href^="#"]');if(a){const target=document.getElementById(a.hash.slice(1));if(!target)return;e.preventDefault();closeNavigation();window.closeAllModals?.();const card=target.closest('[data-gg-build-title]');if(card){showBuild(card);return}history.replaceState(null,'',a.hash);lenis.scrollTo(target,{offset:-100,immediate:prefersRM});}
 },true);
 document.addEventListener('keydown',e=>{
  const target=e.target;if((e.key==='Enter'||e.key===' ')&&target.matches('[role=button]:not(button)')){e.preventDefault();target.click()}
  if((e.key==='ArrowRight'||e.key==='ArrowLeft')&&target.closest('[data-flick-cards-init]')){e.preventDefault();target.closest('[data-flick-cards-init]').dispatchEvent(new CustomEvent('gg-flick-step',{detail:e.key==='ArrowRight'?1:-1}))}
 });
 if(document.body.classList.contains('gg-native-ready'))start();else addEventListener('gg-native-ready',start,{once:true});
})();
