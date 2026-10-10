from bs4 import BeautifulSoup
from pathlib import Path
import json, re, sys

path=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
PROJECT='https://sushxnthd.github.io/greengroove/'
BEHANCE='https://www.behance.net/gallery/211169339/Green-Groove'
GITHUB='https://github.com/sushxnthd/greengroove'
OG='https://mir-s3-cdn-cf.behance.net/project_modules/1400_webp/09cb22211169339.67245eac9212c.png'

def sec(c): return s.find('section',class_=c)
def rep(root,a,b):
    if not root:return 0
    n=0
    for x in list(root.find_all(string=True)):
        if not x.parent or x.parent.name in {'script','style','title'} or x.find_parent('svg'): continue
        if ' '.join(str(x).split())==a: x.replace_with(b); n+=1
    return n
def reps(root,m):
    for a,b in m.items(): rep(root,a,b)

# Metadata: remove Osmo SEO identity without touching runtime geometry.
s.title.string='Green Groove — Retail State System'
for m in list(s.find_all('meta')):
    k=m.get('name') or m.get('property')
    if k=='google-site-verification': m.decompose(); continue
    if k in {'description','og:description','twitter:description'}: m['content']='Green Groove is a student-built physical-digital retail system connecting RFID identity, shelf events, live cart state, reversibility and checkout settlement.'
    elif k in {'og:title','twitter:title'}: m['content']='Green Groove — Retail State System'
    elif k in {'og:image','twitter:image'}: m['content']=OG
for l in s.find_all('link'):
    r=' '.join(l.get('rel') or [])
    if 'canonical' in r:l['href']=PROJECT
    if 'icon' in r:l['href']='favicon.svg'
for sc in list(s.find_all('script',type='application/ld+json')):sc.decompose()
ld=s.new_tag('script',type='application/ld+json')
ld.string=json.dumps({'@context':'https://schema.org','@type':'CreativeWork','name':'Green Groove','url':PROJECT,'image':OG,'creator':[{'@type':'Person','name':'Sushanth Dasari'},{'@type':'Person','name':'Aryan Kumar'}],'description':'A student-built physical-digital retail system connecting RFID identity, shelf events, live cart state, reversibility and checkout settlement.'},separators=(',',':'))
s.head.append(ld)

# Header/menu. Keep short labels so Osmo's button geometry stays intact.
reps(s,{'View':'Source','Validation':'Reversibility','START LEARNING':'VIEW SYSTEM'})

# Hero ring and reel.
reps(s,{'Stacked Drawer Navigation':'Groove Band','Queued Scroll Reveal':'Green Grooves','Globe Gallery':'G/G App','Elastic Line':'Return Reversal','Logo Card Testimonials':'Association Logic'})
reel=sec('reel')
reps(reel,{
'Green Groove is a physical-digital retail system built around identity, shelf events, reversible cart state and a legible checkout flow.':'Green Groove links identity, shelf events, reversible cart state and checkout into one physical-digital retail flow.',
'Green Groove in use':'System in use','See the system in motion':'See the flow in motion!','Reel':'Demo','Play':'View'})

# Creators + project notes, including actual five resource/update cards.
intro=sec('intro')
reps(intro,{'Research and build notes':'New work is','from the project.':'added as we build.'})
specs=[('Groove Band','RFID identity'),('Green Grooves','Shelf sensing'),('G/G App','Live cart'),('Return Reversal','State recovery'),('Association Logic','Event matching')]
if intro:
    for item,(title,cat) in zip(intro.select('.vertical-slider__item')[:5],specs):
        tags=item.select('.button-row .tag .eyebrow')
        if tags: tags[0].string='Prototype'
        if len(tags)>1: tags[1].string='Project module'
        h=item.select_one('h4.h-s'); c=item.select_one('.resource-card__category .eyebrow')
        if h:h.string=title
        if c:c.string=cat

# System story.
db=sec('db')
reps(db,{
'Green Groove models shopping as observable state transitions: identify the shopper, detect a shelf event, associate it, update the cart, reverse mistakes, then settle cleanly.':'A physical-digital retail prototype linking identity, shelf events, association, reversible cart state and settlement.',
'The goal is simple: make physical shopping state legible, reversible and reliable.':'Built so every shopping action can be observed, explained and safely reversed.',
'Explore the system':'System overview'})

# Six connected system layers: source tabs/cards stay untouched structurally.
prod=sec('product-slider')
reps(prod,{'One retail system, six connected layers':'Six layers, one retail state','Each layer solves one concrete responsibility:':'Each layer has one job:'})
layers=[
('Identity','Resolve a shopper or cart context before committing an item event.'),
('Shelf Events','Treat picks and returns at the shelf as explicit physical events.'),
('Association','Match each item event to the most plausible active shopper.'),
('Reversibility','Model mistakes and returns as inverse transitions with history intact.'),
('Live Cart','Keep the live cart synchronized with the latest physical state.'),
('Settlement','Finalize a known cart state instead of reconstructing it at checkout.')]
if prod:
    top=[b for b in prod.find_all('button',class_='button') if not b.find_parent(class_='product-card')][:6]
    for b,(name,_) in zip(top,layers):
        for lab in b.select('.button-label'):
            if lab.find('span'):
                for sp in lab.find_all('span'):sp.string=name
            else:lab.string=name
    for card,(name,desc) in zip(prod.select('.product-card'),layers):
        h=card.select_one('.product-card__h');p=card.select_one('.product-card__p')
        if h:h.string=name
        if p:p.string=desc
        tags=card.select('.product-card__tags .tag .eyebrow')
        if len(tags)>1:tags[1].string='System'

# Why section.
info=sec('info')
reps(info,{
'A retail experience becomes trustworthy when each physical action maps to a clear digital state.':'If the system can explain how state changed, it can recover when the physical world gets messy.',
'Observe physical events':'Observe the aisle','RFID identity and shelf sensing turn movement in the aisle into explicit, inspectable events.':'RFID identity and shelf sensing turn physical actions into inspectable events.',
'Association logic decides who changed what, while the live cart exposes the resulting state.':'Association logic decides who changed what before state is committed.',
'Returns and mistakes are handled as reversible events so the system can recover without hiding history.':'Returns and mistakes become inverse transitions rather than hidden corrections.',
'Built for':'Designed for'})

# Findings carousel: design principles, not fabricated endorsements.
test=sec('testimonial')
reps(test,{'Designed':'From','end to end':'shelf to cart','Green Groove system':'Green Groove','G/G App':'system principles'})
findings=[
('State should explain itself.','Principle 01','Event model','Every cart mutation should point back to an observable add, remove or return event.'),
('Resolve identity before commitment.','Principle 02','Association','Detection and association stay separate so multi-shopper ambiguity remains visible.'),
('Reversibility belongs in the model.','Principle 03','Recovery','Mistakes and returns are inverse transitions with history preserved.'),
('Shelf and cart are two views of one state.','Principle 04','Consistency','Physical events and digital cart state can cross-check one another for missed or duplicate changes.'),
('Show uncertainty before confidence.','Principle 05','Interface','Ambiguous associations should surface for correction instead of being silently forced.'),
('Checkout settles; it should not reconstruct.','Principle 06','Settlement','Maintaining state throughout the journey reduces inference at the final transaction.')]
if test:
    for i,h in enumerate(test.select('h3.is--testimonial')[:6]):
        h.string=findings[i][0]
        anc=h
        for _ in range(8):
            if anc and (anc.find('h4',class_='scribble') or anc.find(string=re.compile('Finding 0'))):break
            anc=anc.parent if anc else None
        if anc:
            scrib=anc.find('h4',class_='scribble');
            if scrib:scrib.string=findings[i][1]
            role=None
            for p in anc.find_all('p'):
                t=' '.join(p.stripped_strings)
                if 2<len(t)<40: role=p;break
            if role:role.string=findings[i][2]
            long=[p for p in anc.find_all('p') if len(' '.join(p.stripped_strings))>60]
            if long:long[-1].string=findings[i][3]

# Roadmap: reinterpret pricing cards without changing their DOM/animation.
pricing=sec('pricing-home')
reps(pricing,{'Validation & evidence':'Prototype today. System next.','System':'Today','Prototype':'Next','Integrated':'Roadmap','components':'view','View full pricing':'View roadmap'})
cards=pricing.select('.pricing-card') if pricing else []
carddata=[
('3 modules','Prototype',['3','3'],'modules','Built as',['hardware','integrated'],'See the build','Groove Band + Green Grooves + G/G App','View build',None),
('6 layers','System',['3','6'],'layers','Expands to',['current','target'],'View architecture','Identity → shelf → association → recovery → cart → settlement','View system','Target 6 connected layers')]
for card,d in zip(cards,carddata):
    tag,title,nums,unit,lead,subs,cta,benefit,under,scrib=d
    e=card.select_one('.tag .eyebrow, .tag span');
    if e:e.string=tag
    e=card.select_one('.pricing-card__title');
    if e:e.string=title
    ps=card.select('.pricing-card__price-h')
    if ps:
        ps[0].string=''
        nps=[p for p in ps[1:] if 'u--opacity-60' not in (p.get('class') or [])]
        for p,v in zip(nps,nums):p.string=v
        u=card.select_one('.u--opacity-60');
        if u:u.string=unit
    e=card.select_one('.pricing-card__sub > .p-m');
    if e:e.string=lead
    for p,v in zip(card.select('.pricing-card__sub-details .p-m'),subs):p.string=v
    for sp in card.select('.button-label span'):sp.string=cta
    e=card.select_one('.pricing-benefit__tag');
    if e:e.string='•'
    e=card.select_one('.pricing-benefit__start > p');
    if e:e.string=benefit
    e=card.select_one('.underline-link');
    if e:e.string=under
    e=card.select_one('.pricing-card__scribble .scribble')
    if e and scrib:e.string=scrib

# Showcase: project modules, same Flick cards.
made=sec('made')
reps(made,{'Made':'Built','as':'into','System view':'Project layer','The pieces':'These parts'})
mods=['Groove Band','Green Grooves','G/G App','RFID Identity','Shelf Sensing','Live Cart','State Recovery']
if made:
    for i,(item,name) in enumerate(zip(made.select('.flick-group__item'),mods)):
        h=item.select_one('[data-res-used="title"]');
        if h:h.string=name
        info=item.select_one('.flick-card__info')
        if info:
            for n in info.find_all(string=True):
                if ' '.join(str(n).split()).isdigit():n.replace_with('1');break
        for j,a in enumerate(item.find_all('a',href=True)):
            a['href']=BEHANCE if (i+j)%2==0 else GITHUB
            for n in list(a.find_all(string=True)):
                if '@' in str(n):n.replace_with('@SUSHANTH' if (i+j)%2==0 else '@ARYAN')

# Final CTA + about/modal/footer.
trysec=sec('try-vault')
reps(trysec,{'Explore project':'Case study','See the system beyond the homepage.':'Want the full project?','Open the Green Groove project':'Explore Green Groove','View project':'View on Behance','Explore':'Full','the build':'case study'})
reps(s,{'Dennis Snellenberg':'Sushanth Dasari','Ilja van Eck':'Aryan Kumar'})
for old,new in [('Dennis','Sushanth'),('Snellenberg','Dasari'),('Ilja','Aryan'),('van Eck','Kumar')]:
    for node in list(s.select('.about-hero .about-item h3, .about-hero .about-item h4')):
        if ' '.join(node.stripped_strings)==old:node.string=new
used=s.find('section',class_='used-credits')
reps(used,{'Resources Used':'System layers','XX':'06'})

footer=s.find('footer')
reps(footer,{
'Green Groove project notes':'Follow the Green Groove build','I agree to the':'Build notes on','Privacy Policy':'GitHub','View research':'Open source',
'Product':'Project','Overview':'Identity','Architecture':'Shelf Events','Validation':'Reversibility','Build':'Build','Notes':'Notes','G/G App':'Project','Roadmap':'Roadmap','Questions':'Questions','Contact':'Contact',
'Research':'Source','Methods':'Methods','Privacy':'Behance','Evidence':'Evidence','created by':'built by','dennis':'Sushanth','ilja':'Aryan','2025':'2026'})
if footer:
    form=footer.find('form')
    if form:
        form['action']=GITHUB;form['method']='get'
        inp=form.find('input',attrs={'type':'email'})
        if inp:inp['placeholder']='Project updates live on GitHub';inp.attrs.pop('required',None);inp.attrs.pop('name',None)
        sub=form.find('input',attrs={'type':'submit'})
        if sub:sub['value']='Open source'

# Brand wordmark: fill Osmo's existing SVG footprint more decisively.
def wordmark(svg):
    svg.clear();svg['viewBox']='0 0 540 156'
    t=s.new_tag('text',x='270',y='112');t['text-anchor']='middle';t['fill']='currentColor';t['font-size']='96';t['font-weight']='900';t['textLength']='500';t['lengthAdjust']='spacingAndGlyphs';t.string='GREEN GROOVE';svg.append(t)
for svg in s.select('svg.nav-logo__wordmark-svg'):wordmark(svg)

# Major section anchors.
for cls,ident in [('home-hero','home'),('intro','project'),('db','system'),('product-slider','architecture'),('info','why'),('testimonial','findings'),('pricing-home','evidence'),('made','build'),('try-vault','research')]:
    e=sec(cls)
    if e:e['id']=ident

# Repair every Osmo route/social to useful Green Groove destinations.
route={'/login':BEHANCE,'/plans':GITHUB,'/product/vault':'#system','/product/page-transition-course':'#architecture','/product/button-pack':'#build','/product/community':'#build','/product/icons':'#build','/showcase':'#build','/collection':'#evidence','/try':BEHANCE,'/updates':'#project','/faq':'#research','/legal/licensing-agreement':GITHUB,'/legal/terms-and-conditions':'#research','/legal/privacy-policy':BEHANCE,'/legal/cookie-policy':'#evidence'}
for a in s.find_all('a',href=True):
    h=a['href']
    if h in {'/','index.html','https://www.osmo.supply','https://www.osmo.supply/'}:a['href']=PROJECT;continue
    if 'linkedin.com/company/osmosupply' in h:a['href']=BEHANCE;a['aria-label']='Behance project';continue
    if 'instagram.com/osmo.supply' in h:a['href']=GITHUB;a['aria-label']='GitHub source';continue
    if 'twitter.com/osmosupply' in h or 'x.com/osmosupply' in h:a['href']=PROJECT;a['aria-label']='Green Groove website';continue
    if 'join.slack.com/t/osmo-headquarters' in h:a['href']=GITHUB;continue
    if 'dennissnellenberg.com' in h:a['href']=BEHANCE;continue
    if 'iljavaneck.com' in h:a['href']=GITHUB;continue
    if 'resource/osmo-scaling-system' in h:a['href']='#architecture';continue
    for p,dst in route.items():
        if h==p or h.endswith('osmo.supply'+p) or h.startswith('https://www.osmo.supply'+p+'?'):a['href']=dst;break
linkmap={'Study':BEHANCE,'Source':GITHUB,'Overview':'#project','Architecture':'#architecture','Groove Band':'#build','Green Grooves':'#build','G/G App':'#build','Reversibility':'#architecture','Build Gallery':'#build','Evidence':'#evidence','Roadmap':'#research','View Project':BEHANCE,'System overview':'#system','Explore build':'#build','View on Behance':BEHANCE,'Open source':GITHUB,'View build':'#build','View system':'#architecture','See the build':'#build','View architecture':'#architecture','View roadmap':'#research'}
for a in s.find_all('a',href=True):
    t=' '.join(a.stripped_strings)
    for k,v in linkmap.items():
        if k in t:a['href']=v;break

# Minimal brand-only CSS. Geometry stays source exact.
style=s.find('style',id='green-groove-tailor')
if not style:style=s.new_tag('style',id='green-groove-tailor');s.head.append(style)
style.string=":root{--color-electric:#78ff45;--color-purple:#18bdf2;--color-purple-copy:#18bdf2}.nav-logo__wordmark-svg text{font-family:Georgia,'Times New Roman',serif;font-weight:900;letter-spacing:-.04em}[data-wf--button-theme--variant='purple']{background:linear-gradient(135deg,#00ef78,#18bdf2)!important}.home-hero__top-logo{color:#16c6c2}.resource-card__video,.cover-video,.showcase-media__video,.about-card__img{object-fit:cover}"

path.write_text(str(s),encoding='utf8')
print('Tailored Green Groove without altering source geometry.')
