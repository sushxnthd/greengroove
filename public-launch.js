/* Green Groove public-site behaviour. No network requests or visitor data storage. */
(() => {
  'use strict';
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => [...r.querySelectorAll(s)];
  const reduced = document.documentElement.dataset.ggMotion==='reduce';
  const motionLink=$('.gg-motion-link');if(motionLink&&reduced){motionLink.href='?motion=full#home';motionLink.textContent='Enable motion'}
  $$('[data-gg-gallery]').forEach(b=>b.addEventListener('click',()=>{$('[data-flick-cards-init]').dispatchEvent(new Event('gg-gallery-'+b.dataset.ggGallery))}));
  const nav = $('.nav'), menu = $('[data-nav-toggle="toggle"]');
  let returnFocus = null;
  function setMenu(open) {
    nav?.setAttribute('data-nav-status',open?'active':'not-active');
    menu?.setAttribute('aria-expanded',String(open));
    menu?.setAttribute('aria-label',open?'Close menu':'Open menu');
    document.body.classList.toggle('gg-menu-open',open);
    $('#gg-navigation')?.setAttribute('aria-hidden',String(!open));
    if ($('#gg-navigation')) $('#gg-navigation').inert = !open;
    if ($('main')) $('main').inert = open;
    if (!open && document.activeElement?.closest('#gg-navigation')) menu?.focus();
  }
  menu?.addEventListener('click',()=>setMenu(nav.getAttribute('data-nav-status')!=='active'));
  $$('[data-nav-toggle="close"]').forEach(e=>e.addEventListener('click',()=>setMenu(false)));
  setMenu(false);
  function openDialog(id) {
    const dialog=document.getElementById(id); if (!dialog) return;
    setMenu(false); returnFocus=document.activeElement;
    if (!dialog.open) dialog.showModal();
    document.body.classList.add('gg-dialog-open');
  }
  $$('dialog').forEach(d=>{
    d.addEventListener('close',()=>{document.body.classList.remove('gg-dialog-open');returnFocus?.focus?.({preventScroll:true})});
    d.addEventListener('click',e=>{if(e.target===d){const b=d.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)d.close()}});
  });
  const layers = [
    ['Identity','a01-identity-layer.svg','A wristband identifies an active shopping session. An identity read establishes cart context; it does not by itself prove who picked up an item.'],
    ['Shelf Events','a02-shelf-events-layer.svg','A load-cell change and RFID observations form a candidate shelf event. Calibration, product weight variation and simultaneous actions still need controlled testing.'],
    ['Association','a03-association-layer.svg','A detected event must be matched to one valid shopping session before a cart changes. Ambiguous candidates stay on hold for review.'],
    ['Reversibility','a04-reversibility-layer.svg','A return references an earlier accepted pickup. The inverse event changes quantity while preserving both actions in the history.'],
    ['Live Cart','a05-live-cart-layer.svg','Accepted events determine quantities and subtotal. Held events stay separate so uncertainty cannot silently become a charge.'],
    ['Settlement','a06-settlement-layer.svg','The final accepted cart becomes an invoice summary. Payment processing and a commercial deployment are separate from this prototype.']
  ];
  function showLayer(i,title,imageSource) {
    const [name,file,copy]=layers[i],src=imageSource||'assets/visuals/'+file;
    $('#gg-layer-title').textContent=title||name;
    $('#gg-layer-description').textContent=copy;
    $('#gg-layer-image').src=src;$('#gg-layer-image').alt=name+' system design';$('#gg-layer-full').href=src;
    openDialog('layer-detail');
  }
  function showBuild(card) {
    const button=$('[data-gg-build]',card),i=+button.dataset.ggBuild;
    showLayer([0,1,4,0,1,4,3][i],card.dataset.ggBuildTitle,$('.showcase-media__image',card)?.getAttribute('src'));
  }
  document.addEventListener('click',e=>{
    const close=e.target.closest('[data-gg-close]');if(close){close.closest('dialog').close();return}
    const layer=e.target.closest('[data-gg-layer]');if(layer){e.preventDefault();showLayer(+layer.dataset.ggLayer);return}
    const build=e.target.closest('[data-gg-build]');if(build){showBuild(build.closest('[data-gg-build-title]'));return}
    const modal=e.target.closest('[data-gg-dialog]');if(modal){e.preventDefault();openDialog(modal.dataset.ggDialog);return}
    const link=e.target.closest('a[href^="#"]');if(link){
      const target=document.getElementById(link.hash.slice(1));if(!target)return;
      e.preventDefault();$$('dialog[open]').forEach(d=>d.close());setMenu(false);
      const card=target.closest('[data-gg-build-title]');
      if(card){showBuild(card);return}
      history.pushState(null,'',link.hash);
      window.scrollTo({top:Math.max(0,target.getBoundingClientRect().top+scrollY-110),behavior:reduced?'auto':'smooth'});
      target.setAttribute('tabindex','-1');target.focus({preventScroll:true});
    }
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape')setMenu(false);
    if((e.key==='Enter'||e.key===' ')&&e.target.matches('[data-gg-dialog][role="button"]')){e.preventDefault();openDialog(e.target.dataset.ggDialog)}
    if(e.key==='Tab'&&nav?.getAttribute('data-nav-status')==='active'){
      const f=$$('button,a[href]',nav).filter(e=>e.getClientRects().length&&!e.closest('[inert]'));
      const first=f[0],last=f[f.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}
    }
  });
  // These cards document present support and the next validation milestone.
  const evidence=$('#evidence'), cards=$$('.pricing-card',evidence);evidence.setAttribute('data-pricing-section-status','quarterly');
  const originals=cards.map(c=>({title:$('.pricing-card__title',c)?.textContent,copy:$('.gg-card-description',c)?.innerHTML,tag:$('.pricing-card__inner > .tag .eyebrow',c)?.textContent}));
  $$('[data-pricing-button]',evidence).forEach(button=>button.addEventListener('click',()=>{
    const next=button.getAttribute('data-pricing-button')==='annually';
    evidence.setAttribute('data-pricing-section-status',next?'annually':'quarterly');
    $$('[data-pricing-button]',evidence).forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    cards.forEach((c,i)=>{
      const h=$('.pricing-card__title',c),p=$('.gg-card-description',c);
      const tag=$('.pricing-card__inner > .tag .eyebrow',c);if(tag)tag.textContent=next?'Planned validation':originals[i].tag;
      if(h)h.textContent=next?['Technical testing','Field evaluation'][i]:originals[i].title;
      if(p)p.innerHTML=next?['<span class="gg-card-lead">Next: controlled tests of sensor calibration, shopper association and reversible event recovery.</span><span class="gg-card-support">Report event-level errors and test conditions before making performance claims.</span>','<span class="gg-card-lead">Planned: observe the prototype under documented retail conditions.</span><span class="gg-card-support">Capture ambiguity, operational recovery and store feedback. No commercial pilot results are claimed.</span>'][i]:originals[i].copy;
    });
    evidence.classList.toggle('gg-next-view',next);
  }));
  $$('[data-pricing-button]',evidence).forEach(b=>b.setAttribute('aria-pressed',String(b.textContent.includes('Today'))));
  // A reversible event model. This is explicitly illustrative, with no sensors or payments.
  let qty={milk:0,yogurt:0},held=0,events=[],settled=false;
  const prices={milk:60,yogurt:25};
  function paint(message){
    $('#gg-cart-lines').textContent=`Milk × ${qty.milk} · Yogurt × ${qty.yogurt}`;
    $('#gg-cart-total').textContent='₹'+(qty.milk*60+qty.yogurt*25);
    $('#gg-demo-status').textContent=message;
    const list=$('#gg-demo-ledger');list.replaceChildren();
    (events.length?events:['No events yet.']).forEach(t=>{const li=document.createElement('li');li.textContent=t;list.append(li)});
    $('[data-gg-event="return-milk"]').disabled=qty.milk===0||settled;
    $('[data-gg-event="resolve"]').disabled=held===0||settled;
    $$('[data-gg-event^="pick-"],[data-gg-event="ambiguous"]').forEach(b=>b.disabled=settled);
    $('[data-gg-event="settle"]').disabled=settled||!qty.milk&&!qty.yogurt;
  }
  function append(text){events.push(String(events.length+1).padStart(2,'0')+' · '+text)}
  $$('[data-gg-event]').forEach(b=>b.addEventListener('click',()=>{
    const action=b.dataset.ggEvent;
    if(action==='reset'){qty={milk:0,yogurt:0};held=0;events=[];settled=false;paint('Ready. Your example cart is empty.');return}
    if(settled)return;
    if(action.startsWith('pick-')){const item=action.slice(5);qty[item]++;append('PICK '+item+' · ACCEPTED');paint('Pickup accepted. The cart is updated.');}
    else if(action==='return-milk'&&qty.milk){qty.milk--;append('RETURN milk · inverse of accepted pickup');paint('Return accepted. The pickup remains visible in history.');}
    else if(action==='ambiguous'){held++;append('PICK yogurt · HOLD · shopper unresolved');paint(`${held} pickup${held===1?'':'s'} held. The subtotal has not changed.`);}
    else if(action==='resolve'&&held){held--;qty.yogurt++;append('RESOLVE held yogurt pickup · ACCEPTED');paint('Held pickup assigned to this example session. The cart is updated.');}
    else if(action==='settle'){
      if(held){append('INVOICE blocked · unresolved pickup');paint('Resolve held events before confirming the invoice.');return}
      settled=true;append('INVOICE confirmed · ₹'+(qty.milk*60+qty.yogurt*25));paint('Example invoice confirmed. No payment was taken. Reset to try another trip.');
    }
  }));
  paint('Ready. Your example cart is empty.');
  // Small-screen footer groups keep collapsed links out of the tab order.
  $$('.footer-link__col').forEach((col,i)=>{
    const top=$('.footer-link__col-top',col),bottom=$('.footer-link__col-bottom',col);if(!top||!bottom)return;
    bottom.id='gg-footer-'+i;top.setAttribute('aria-controls',bottom.id);
    function sync(){
      const mobile=innerWidth<=767,open=!mobile||col.getAttribute('data-accordion-status')==='active';
      top.tabIndex=mobile?0:-1;
      if(mobile)top.setAttribute('role','button');else top.removeAttribute('role');
      top.setAttribute('aria-expanded',String(open));bottom.inert=!open;
    }
    const toggle=()=>{if(innerWidth>767)return;col.setAttribute('data-accordion-status',col.getAttribute('data-accordion-status')==='active'?'not-active':'active');sync()};
    top.addEventListener('click',toggle);top.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle()}});
    addEventListener('resize',sync,{passive:true});sync();
  });
  // Decorative clones must never duplicate focus stops or screen-reader content.
  const hideClones=()=>{
    $$('[data-radial-marquee-rotate]').forEach(r=>{const a=[...r.children];a.slice(9).forEach(e=>{if(e.getAttribute('aria-hidden')!=='true')e.setAttribute('aria-hidden','true');if(!e.inert)e.inert=true})});
    $$('[data-vertical-slider-item]').forEach(item=>{const hidden=item.getAttribute('aria-hidden')==='true';if(item.inert!==hidden)item.inert=hidden});
  };
  hideClones();
  new MutationObserver(hideClones).observe(document.body,{subtree:true,attributes:true,attributeFilter:['aria-hidden']});
  document.body.classList.add('gg-ready');
})();
