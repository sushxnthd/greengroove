# Green Groove — Visual Asset Production Specification
**Version:** 1.0 · **Date:** 19 October 2026  
**Repository:** `sushxnthd/greengroove`  
**Status:** Approved production brief; individual visual assets require generation, review, and integration.

## 1. Objective and audited website map

Replace all unrelated, repetitive, template-derived and placeholder visuals with a cohesive Green Groove visual system. Retain the existing Osmo-inspired **layout and motion geometry**, not its borrowed imagery, brands, profiles, maps or poster files. Keep live HTML headings, cards and copy editable.

Audited source: `index.html` on `main` (as inspected 19 October 2026). It contains **81 `<img>` elements and 27 `<video>` elements**, but the elements substantially reuse a small set of Behance images. All 27 video elements lacked a normal `src` attribute at audit time; the static-poster behavior is intentional in some cases, but should not masquerade as real video. A **47-asset master library** below supports most placements by contextual reuse rather than generating 108 unrelated assets.

| Page region / selector | Required assets | Integration note |
|---|---|---|
| Main navigation, hero and site shell | G01–G05, H01–H09 | 9 rotating cards under `#home .radial-marquee`; keep established radial motion |
| Home motion reel, `section.reel` | H10–H11 | One true motion piece and matching poster; reduced-motion poster fallback |
| `#project` intro / project cards | P01–P05; T01–T02 | Remove Osmo profile alt text and irrelevant thumbnail reuse |
| `#system` | A07, R01 | Replace Osmo Vault preview with Green Groove system state |
| `#architecture` | A01–A06 | Exactly six consistent cards; one accurate diagram per layer |
| `#why` | A07, R02 | Correctly depict observe → associate → reverse rather than decorative filler |
| `#findings` | C01–C06 | Replace globe/map/testimonial imagery with the six engineering challenges |
| `#evidence` | E01–E04 | Only legitimate proof and clearly labeled future validation |
| `#build` | B01–B04, P01–P03, R01 | Seven source carousel placements can reuse tailored module imagery |
| `#research` | R01–R02, F01 | Real system notes and clear case-study CTA |
| About modal / auxiliary used-resources views | T01–T02, B01–B04, A07 | Remove template founder images and Osmo geographic maps |
| Open Graph / browsers | G01–G05 | Ensure branded SVG and social-preview metadata |

### Content ground truth
Green Groove is a student-built retail checkout prototype with three modules: **Groove Band** (RFID shopper identity), **Green Grooves** (RFID readers and shelf load cells), and **G/G App** (live reversible cart). Logical layers: **Identity → Shelf Events → Association → Reversibility → Live Cart → Settlement**. The project was selected under **NCERT PRAYAAS**, awarded **₹50,000 development support**, and associated with **IIT Delhi as the HEI**, with **Prof. Satish Kumar Dubey (SeNSE)** as mentor through the programme. This establishes project support, **not** a production deployment, verified automatic payments, validated carbon reductions, or a commercial pilot.

## 2. Unified art direction and technical defaults

**Composition language.** Editorial Swiss/Osmo-like typographic clarity; documentary engineering detail; minimal CGI where needed. Preserve light page canvases and saturated, dark cards. Prefer product details, flat system schematics, cropped hardware photography, high-resolution app UI; avoid a website full of dark sci-fi store photos. One visual should communicate one central mechanism.

**Colors** (use local site tokens if current source differs): paper `#F4F4F4`, ink `#201D1D`, charcoal card `#171A15`, acid/lime `#A1FF62` with bright variant `#78FF45`, quiet warm grey `#CDD2C9`, off-white `#F3F4EE`, optional cyan `#18BDF2` for exceptions/data only. Legacy purple (`#6840FF`) appears in earlier CSS; **do not promote it to the primary palette**. Aim for 70% neutral, 20% dark, 10% highly saturated accents within any media item.

**Type.** Preserve website’s Haffer XH and Haffer Mono assignments where available and licensed. Do not distribute fonts. Use native HTML for headings, captions and labels. Technical diagram labels should be editable SVG text or native HTML; exported raster art generally has **no embedded words**. Numerals/events should have a monospaced treatment.

**Layouts.** Safe area ≥12% for cropped carousel artwork, 8% for editorial 4:3 media, ≥15% around human faces. Avoid primary detail in the outer 20% of a marquee card. High contrast and real depth hierarchy; use shadows sparingly. No fake blur/glow pretending to be sensor physics.

**Deliverables.** Source: `SVG`/Figma-compatible vector for diagrams/icons; documented layered `PNG` for generated concept renders; authentic original photography where required. Web: optimized `AVIF` with `WebP` fallback (or just WebP if AVIF unsupported), `SVG` for vector; motion `MP4 H.264` + `WebM` optional + poster. Keep image dimensions in attributes to avoid CLS. Prefer square 1280×1280 master for rotating thumbnails, 1600×1200 for editorial 4:3, 2400×1350 for 16:9, 1080×1350 for phone portrait. At export, target ≤140 KB thumbnail, ≤260 KB ordinary card, ≤400 KB large poster wherever possible; use quality measured by legibility. Avoid shipping all 47 assets in first load.

**Motion.** 24 or 30 fps, no continuous scene-wide parallax that blocks reading. 200–550 ms micro-transitions, ease-out. Reduced-motion users receive static poster and no automatic playback. Animations must not invent features.

**Truthfulness labels.** `Concept visualization` for all AI-generated mock photography; `Illustrative interface` where UI is not an actual build; `Diagram` for schematics. Evidence photographs, founder portraits, official correspondence, results and logos must come from **authentic source media**, never fabricated. Do not invent identifiable real people. No claims of computer vision, facial recognition, instantaneous automatic charge, successful retail field pilots, carbon savings, working payment cards, or metrics not substantiated by records.

**Already generated concept references.** The existing seven generated drafts (shopping hero, band, shelves, app, system diagram, prototype scene, retail pilot) are visual *moodboards*, not verified depictions of the hardware or real founders. Their content (particularly fictional UI totals, staged founders, carbon metrics, and futuristic payment claims) must be corrected or discarded before publication.

## 3. Master inventory — 47 unique assets

Notation: `ID | output file | master canvas | mode`. “Artwork” names the content to construct. “Check” is the acceptance condition. Default output directory: `assets/visuals/`. Each asset receives one primary file plus optimized/responsive variants. Visuals can be reused in additional sections, but **do not reuse one identical image for unrelated concepts**.

### G — Brand and reusable art system (5)

**G01 | `g01-wordmark.svg` | vector, scalable | identity master.**
- **Placement:** site nav/footer, media covers, selected illustrated headers.
- **Artwork:** faithfully reconstruct *existing* Green Groove spelling and leaf/mark geometry from the canonical project brand. Horizontal lockup plus reversed light variant; genuine source takes precedence over generated reinterpretation.
- **Check:** optically centered with original nav constraints; crisp at 100–320 px; light/dark contrast; no unrelated Osmo wordmarks or stale colors.

**G02 | `g02-symbol.svg` | square vector + 512×512 PNG | icon identity.**
- **Placement:** favicon, PWA/touch icons, stamped corner of documentation assets.
- **Artwork:** the G01 mark isolated; deliver monotone and lime-on-charcoal variants with at least 10% edge padding. Preserve recognizable silhouette at 16 px.
- **Check:** legible at 16/32/48 px; valid favicon link; transparent background variant; no accidental rounding of original logo.

**G03 | `g03-system-icons.svg` | 24×24 design grid, sprite/symbol collection | vector UI.**
- **Placement:** architecture, challenge cards, card overprints, state ledger.
- **Artwork:** 16 matched single-color icons: wristband/RFID, reader, weight sensor, pick, return, association, identity, cart, mismatch, hold/uncertain, history, settlement, receipt, test, timeline, shop. 1.75 px stroke, 2 px radii; geometric rather than playful.
- **Check:** icons remain identifiable without color alone; accessible labels where semantic; consistent scale/stroke, no emoji icons.

**G04 | `g04-motion-rings.svg` | 1600×1600 vector master | decorative motif family.**
- **Placement:** radial marquee, reel border, product slider rings, `made` decorations.
- **Artwork:** rings/arcs and short tick marks modeled on event signals, using *one shared motif*. Derive 3 crop variants (radial, reel, slider) from this file; delicate lime and charcoal strokes, controlled opacity.
- **Check:** transparent and scalable, no Osmo remote SVG URLs, does not obstruct controls, safe with reduced motion.

**G05 | `g05-og-cover.webp` | 1200×630 (1.90:1) | editorial composition.**
- **Placement:** `og:image`, Twitter preview, share cards.
- **Artwork:** original brand mark, headline “Checkout without the queue” as accurately typeset vector/HTML render, simplified wristband→shelf→cart composition; paper background with dark panel and lime path.
- **Check:** reads at 600 px width; verified URL and 1200×630 metadata; no fake official award badge. Export PNG fallback if social host rejects WebP.

### H — Homepage and motion (11)

All H01–H09 must be **1280×1280 square masters** (responsive 640px WebP/AVIF), safe center 70%; inserted into `#home .radial-marquee__card-visual` by card order and label. Native card labels below images remain in HTML.

**H01 | `h01-rfid-identity.webp` | 1280×1280 | conceptual hardware macro.**
- **Artwork:** anonymous hand wearing a plausible RFID wristband beside an RFID reader zone, with a single clean ID-token motif and subtle connection line; focused shallow-depth scene, not an Apple Watch.
- **Check:** no face scan, biometrics or fake optical sensor; readable in a 200px rotating card.

**H02 | `h02-shelf-event.webp` | 1280×1280 | technical photo/illustration.**
- **Artwork:** one product physically leaving a smart shelf; reveal load cell below shelf plane and RFID read zone, with one small bright event marker. Neutral grocery object, crisp shelf edge.
- **Check:** make detection and the physical pick visibly connected; no fictional camera/vision sensing.

**H03 | `h03-return-reversal.webp` | 1280×1280 | paired-state editorial illustration.**
- **Artwork:** before/after single product placed back, faint inverse arrow and removal from cart; visual chronology via two related positions. Restrained cyan may mark reversal.
- **Check:** visibly reverses an event, not merely a trash/delete command.

**H04 | `h04-live-cart.webp` | 1280×1280 | UI render from real layout.**
- **Artwork:** cropped cart panel showing 2–3 items, a single quantity change and total area; light text, charcoal surface, acid-green changed row.
- **Check:** sample quantities/prices clearly marked illustrative unless copied from actual app; no fake paid status.

**H05 | `h05-association.webp` | 1280×1280 | schematic.**
- **Artwork:** event node at center, two anonymous shopper wristband paths, one valid selected association and one unresolved dashed line.
- **Check:** highlight that event detection ≠ shopper assignment; no promise of infallible matching.

**H06 | `h06-settlement.webp` | 1280×1280 | receipt/state diagram.**
- **Artwork:** a known final cart state becomes a generated invoice; dark receipt on paper background, tiny “finalize” path.
- **Check:** illustrate invoice creation, *not* automatic wallet charging or completed cashierless retail deployment.

**H07 | `h07-event-history.webp` | 1280×1280 | event-ledger UI graphic.**
- **Artwork:** 5 ordered event rows with `PICK`, `RETURN`, `HOLD`; one return visibly references an earlier add. Use abstract IDs instead of user PII.
- **Check:** internally consistent sequence; real sample only if available, otherwise clearly illustrative.

**H08 | `h08-field-validation.webp` | 1280×1280 | roadmap documentary style.**
- **Artwork:** clipboard/test plan + shelf test zones + “planned” visual motif; product-scale store corner but no implied operating commercial installation.
- **Check:** any store/pilot photo used as fact must be an actual pilot photograph; otherwise label `Field validation / planned`.

**H09 | `h09-product-interaction.webp` | 1280×1280 | editorial product crop.**
- **Artwork:** hand moving grocery product on shelf; minimal floating pick-event tile separated from the photograph, matching H02 but different camera angle and storytelling.
- **Check:** shows one physical interaction clearly; no generic holographic AR environment.

**H10 | `h10-reel-poster.webp` | 2400×1350 (16:9) | motion poster.**
- **Artwork:** three-panel journey (wristband → shelf event → digital cart), no baked-in long copy; expressive composition that works behind play control.
- **Check:** strong stationary frame, title remains a true DOM overlay; usable on mobile crop and as reduced-motion fallback.

**H11 | `h11-checkout-journey.mp4` | 1920×1080, 24–30 fps, 16–22 s | actual motion asset.**
- **Sequence:** 0–3s wristband identity; 3–7s shelf pick event; 7–11s association checks; 11–15s cart updates; 15–18s return inverse; 18–22s invoice-state close. Each scene based on the approved A-series semantics.
- **Check:** no auto-payment claim, readable without sound; captions or text equivalents; poster H10; export H.264 MP4 (+ optional WebM), target ≤5 MB, pause/close functional.

### P — Product modules (5)

**P01 | `p01-groove-band.webp` | 1600×1200 | product macro/concept.**
- **Placement:** project modules, build showcase, About cards.
- **Artwork:** wristband shown in exploded two-layer editorial view: outer wearable + internal RFID identity concept; lime reading field but *no* giant glowing electronic ring or display unless present in prototype.
- **Check:** geometry reviewed against actual wearable photo before labeling “prototype”; otherwise visibly labeled concept.

**P02 | `p02-green-grooves-shelf.webp` | 1600×1200 | isometric annotated hardware.**
- **Artwork:** shelf panel, load cell placement, RFID reader/antenna zone, product footprint; clean cutaway rather than visually impossible supermarket.
- **Check:** sensor relationships technically plausible and verified against build notes; no camera/vision module.

**P03 | `p03-gg-app.webp` | 1080×1350 (4:5) | native UI reconstruction.**
- **Artwork:** authentic or accurately reconstructed app screen showing active session, cart rows, explicit pick/return state, pending ambiguity. Phone frame optional; minimal peripheral ornaments.
- **Check:** actual G/G App screenshots preferred; if screen is proposed concept, label as `Interface concept`, remove fictional payment/impact data.

**P04 | `p04-return-state.webp` | 1600×1200 | dual-state interface.**
- **Artwork:** two equal states separated by an inverse event: quantity 1→0, ledger records add and compensating return. Link arrows and highlights drawn in native SVG if feasible.
- **Check:** no disappearing history or manually deleted items masquerading as automatic sensor return.

**P05 | `p05-event-association.webp` | 1600×1200 | association logic.**
- **Artwork:** shelf event `S03/PICK`, active identities `A` and `B`, matching decision and `HOLD` fallback; use abstract simulated input.
- **Check:** careful distinction between sensing and matching, no unsupported confidence accuracy percentage.

### A — Architecture visuals (7)

A01–A06 have **1600×1200 (4:3) masters** with shared 12-column vector grid; use light cards with charcoal nodes and lime edges, consistent icon scale. Text should remain editable vector or HTML, not generated pixels. Link from `#architecture`.

**A01 | `a01-layer-identity.svg` | 1600×1200.** Shopper receives unique RFID token; map `session_id → wristband_id` and active cart. **Check:** unique within session; no facial recognition.
**A02 | `a02-layer-shelf-events.svg` | 1600×1200.** Physical pick/return triggers paired load-cell and RFID observations, producing timestamped candidate event. **Check:** depict reader+weight correctly, not vision.
**A03 | `a03-layer-association.svg` | 1600×1200.** Candidate event links to active shopper/cart after matching; ambiguity branches to pending review. **Check:** clear unmatched state, no assumed 100% accuracy.
**A04 | `a04-layer-reversibility.svg` | 1600×1200.** Event log `PICK(+1) → RETURN(-1)`; old event remains visible, state totals recover. **Check:** mathematically consistent example.
**A05 | `a05-layer-live-cart.svg` | 1600×1200.** Ledger drives live cart materialized view; quantity and subtotal update from accepted events. **Check:** no premature cart change for unresolved events.
**A06 | `a06-layer-settlement.svg` | 1600×1200.** Final accepted cart becomes invoice/checkout summary; clearly end state, not external payment confirmation. **Check:** invoice ≠ auto-charge.
**A07 | `a07-six-layer-system.svg` | 2400×1350 (16:9) | full architecture map.**
- **Artwork:** six labeled nodes in exact sequence, event lane, error/hold lane, return edge to log, and final cart/settlement. White-space sufficient for tablet scaling, with exportable mobile stacked variant.
- **Check:** arrow logic agrees with A01–A06, no direct sensor→payment bypass; diagram readable at 1100 px wide, provide transcript/alt.

### C — Six engineering challenges (6)

All use **1400×1050 (4:3) editable vector + WebP**; editorial two-column visual logic, no fake experiments; placed in `#findings` in challenge order. Separate imagery instead of six copies of the same store scene.

**C01 | `c01-detection-vs-association.svg`.** Shelf reports product removed while two shopper tokens overlap; correct result `candidate event` not direct cart mutation. **Check:** uncertainty is shown.
**C02 | `c02-inverse-transitions.svg`.** Original pick row plus linked return row, quantity recovery in final state, with chronological dotted line. **Check:** append-only audit principle clear.
**C03 | `c03-sensor-crosscheck.svg`.** Two sensor observations vs expected cart state; discrepancy turns into amber/cyan `RECHECK` path. **Check:** don't assert validated failure-detection rates.
**C04 | `c04-identity-first.svg`.** Identity/session gate before cart update; unknown identity stops accepted state transition. **Check:** no unassigned cart.
**C05 | `c05-visible-uncertainty.svg`.** Two plausible shoppers produce a pending/held branch rather than false confidence; show evidence request or resolution step. **Check:** no invented confidence percentages.
**C06 | `c06-known-state-settlement.svg`.** Contrast manual basket reconstruction with settled, already-maintained cart. **Check:** don't imply instant operational rollout or guaranteed zero queues.

### E — Proof and validation (4)

Evidence **MUST NOT be image-generated**. Layout design may be generated, but the supporting content must be traceable. Avoid official institutional emblems without a usable authorized source.

**E01 | `e01-prayaas-selection.webp` | 1600×1200 | documentary evidence tile.**
- **Artwork:** verified programme selection letter/list excerpt or published school/NCERT record, with accurate date and context in HTML side caption.
- **Check:** redactions for private details; selection category confirmed; “selected under” not “run by” or “NCERT-backed company.”

**E02 | `e02-development-grant.webp` | 1600×1200 | documentary evidence tile.**
- **Artwork:** authentic grant notice or permitted excerpt confirming ₹50,000 *development grant*, framed in original graphic system.
- **Check:** do not create a fake cheque/certificate; wording and amount match source.

**E03 | `e03-mentor-hei.webp` | 1600×1200 | sourced identity/evidence.**
- **Artwork:** verifiable programme document naming IIT Delhi HEI and Prof. Satish Kumar Dubey, or a faithfully cited profile/document excerpt. Keep logos optional.
- **Check:** distinction between mentorship/associated institution and endorsement. No fictional collaboration photograph.

**E04 | `e04-validation-roadmap.svg` | 2400×1350 | factual planning chart.**
- **Artwork:** `completed build` / `next technical tests` / `planned field pilots` with separate statuses; planned sensors/state consistency checks and store feedback.
- **Check:** do not invent sample sizes, pilots, calibration numbers, signed retailer agreements, or achievements; update statuses only with records.

### B — Build and engineering process (4)

For B01–B03, authentic prototype photography has priority. AI-generated illustration may be a labeled cutaway, never evidence of a specific actual device build.

**B01 | `b01-prototype-assembly.webp` | 2000×1250 (8:5) | project build overview.**
- **Artwork:** wide engineering workbench with real RFID reader, wristband, scale/shelf mockup, and laptop; optional thin leader-lines as a separate SVG overlay.
- **Check:** actual photos when claiming project build; no synthetic likenesses of real founders or fabricated facilities.

**B02 | `b02-rfid-reader-macro.webp` | 1600×1200 | documentary macro.**
- **Artwork:** reader module and physical wiring on a neutral background with a card/tag read zone and a separate annotatable callout field.
- **Check:** component model, pins and role match source; don't imply range or security without tests.

**B03 | `b03-load-cell-shelf-macro.webp` | 1600×1200 | cutaway/macro.**
- **Artwork:** load-cell support point beneath shelf, product pressure arrow, wire to conditioning electronics; RFID sensing shown as separate subsystem.
- **Check:** load sensor is correctly placed in force path, electronics not physically impossible.

**B04 | `b04-build-milestones.svg` | 2400×1350 | timeline.**
- **Artwork:** four carefully captioned milestone frames: queue problem → RFID identity proof → sensor/cart integration → PRAYAAS-supported next validation. Photos may be clipped into vector grid.
- **Check:** date labels sourced; planned milestones visually distinct from completed; no fabricated “first retail pilot” photo.

### T — Founders and actual project documentation (2)

**T01 | `t01-sushanth-portrait.webp` | 1200×1500 (4:5) | real portrait.**
- **Placement:** `#project` creator intro, About modal, collaboration list/avatar crop.
- **Artwork:** user-provided genuine image, clean crop, neutral tonal grade, eye position at 40% height; optional lime line on an adjacent HTML card.
- **Check:** true identity, consent, no AI-generated synthetic face, alt = “Sushanth Dasari”.

**T02 | `t02-aryan-portrait.webp` | 1200×1500 (4:5) | real portrait.**
- **Placement:** paired creator card, About modal, avatars.
- **Artwork:** user-provided real image, visually matched crop and exposure to T01 without changing facial features.
- **Check:** true identity, consent, alt = “Aryan Kumar”. Don't reuse random Osmo founder images.

### R — Research/system evidence graphics (2)

**R01 | `r01-event-ledger.svg` | 1600×1000 (8:5) | accurately scripted schematic.**
- **Placement:** `#system`, `#research`, resource panel.
- **Artwork:** synthetic yet internally consistent event stream with timestamps, shelf ID, token, action, association and resulting cart; one return and one pending event. Mark `Illustrative event trace`.
- **Check:** sum of accepted events matches displayed cart; never invent real experimental logs.

**R02 | `r02-ambiguity-decision-tree.svg` | 1600×1200 (4:3) | logical decision tree.**
- **Placement:** `#why`, `#research`, about case-study.
- **Artwork:** detect? → valid identity? → unique association? → accept update; otherwise pending/hold and explicit resolution. Include return as inverse event.
- **Check:** all edges properly routed, labels legible at 70% width; no claim of implemented ML confidence system unless code confirms it.

### F — Closing / auxiliary (1)

**F01 | `f01-project-story-cta.webp` | 2400×1350 (16:9) | editorial closing scene.**
- **Placement:** `#research` closing CTA, modal card cover, optionally the home reel end-frame.
- **Artwork:** distinct top-down composition of wristband, RFID module, retail object and cart-state printout on paper/charcoal desk; asymmetrical negative space for real DOM CTA.
- **Check:** no incidental fake certificates, no illegible generated text, responds gracefully to 16:9→4:5 crop.

## 4. Asset-to-placement reuse rules

1. **Homepage feature thumbnails:** H01–H09, exactly one distinct master per topic. Identical images may recur solely as image/video *posters for the same card*; not across different topics.
2. **Project module carousel / “Built into Green Groove”:** use P01–P05 and appropriate A/R assets, not nine extra re-renders of a generic shelf.
3. **Architecture 6:** A01–A06 only; A07 is the full architecture overview, also reusable in `#system`.
4. **Findings 6:** C01–C06 replace the preexisting globe/map portrait/testimonial visual scaffolding; remove unrelated country map assets rather than invent geographic relevance.
5. **Real proof:** E01–E03 require sourced files; E04 is a roadmap, not evidence of a finished test.
6. **About and auxiliary pages:** T01–T02 for real people; B01–B03 for actual project gallery; remove any Osmo staff photos and decorative stock biography cards.
7. **Animation:** H11 is the *only mandatory full-motion media* in Phase 1. Other former video elements should become honest image components with static posters, unless later approved motion is built.

## 5. Creation, review and deployment plan

**Stage 0 — Establish sources and truth gates.** Collect real prototype photos, actual app screenshots, exact brand artwork, evidence records, and founder portraits. Invent nothing absent from them. Establish a reviewed example event trace and accurate physical sensor schematic. Deliverables: source register with proof links, classification `real / illustrative / generated`.

**Stage 1 — Lock visual grammar and first-viewport assets.** Finish G01–G05, H01–H09, H10, H11. Review all 9 thumbnails at actual carousel size, test mobile cropping, compose 20s reel from the actual system flow. Don't spend time on a full redesign of page geometry.

**Stage 2 — Product and architecture.** Build P01–P05, A01–A07. Use shared icon library G03. Perform technical review of all arrows, device physics, state transitions and sensor relationships before raster export.

**Stage 3 — Differentiate lessons.** Build C01–C06 and R01–R02; one technical insight per frame. Verify ledger arithmetic and pending-event behavior. Replace irrelevant map/testimonial imagery, not simply overlay it.

**Stage 4 — Evidence, founders and documentary coverage.** Prepare E01–E04, B01–B04, T01–T02, F01 from actual sources. Where authentic evidence is not available, leave factual slots pending and use clean explanatory diagrams rather than pretend imagery.

**Stage 5 — Integrate and quality-assure.** Introduce versioned manifest mapping each `ID → file → target selector → alt → source classification`. Update `<img src/srcset>` and video poster/src, plus CSS `background-image` overrides. Critical: legacy rules such as `.gg-placeholder-img{opacity:0!important}`, `.gg-placeholder-video{display:none!important}`, and pseudo-element visual placeholders in `source-green.css`, `media-fill.css`, and `fidelity-final.css` must be reconciled or removed. Do **not** globally search-and-replace the 6 reused Behance URLs because each occurrence means something different.

**Stage 6 — Visual QA and Vercel, only after approval.** Check 390, 430, 768, 1024, 1440 and 1920 px; verify full hero radial animation and reduced-motion support; measure initial media weight, LCP/CLS, responsive decoding, keyboard controls; test Chromium, Firefox, WebKit; validate missing requests, alt text, captions, social preview, network independence from Osmo image CDN; and then configure Vercel output for this static repo, preview deployment first, production only after review. Do not describe the site as deployed before then.

## 6. QA acceptance gates for every asset

- [ ] **Semantic fidelity:** visual depicts the corresponding feature/mechanism, not generic “green technology”.
- [ ] **Authenticity:** source type and rights documented; concepts labeled, proof verified.
- [ ] **Consistent appearance:** brand alignment, palette, contrast, typography, icon stroke and corner geometry pass side-by-side comparison.
- [ ] **Anatomy/logic:** hardware physically plausible; cart arithmetic and causal arrows correct.
- [ ] **Real-size readability:** thumbs recognizable at 200–260 px; diagrams readable at 1100 px; crops safe on 390 px mobile.
- [ ] **Format/performance:** appropriate SVG/AVIF/WebP/MP4, bounded dimensions, compressed, no broken links or animation-only content.
- [ ] **Accessibility:** meaningful alt text for content images; purely decorative marked aria-hidden; prefers-reduced-motion respected.
- [ ] **Technical regression:** works within inherited Osmo layout without clipping, hit-target regressions, or large jumps.
- [ ] **Replacement completion:** no accidentally visible Osmo/stock/filler media, no unrelated alt names, no dead poster-only play controls.
- [ ] **Source register:** each approved file has creation date, author/source, consent/license if needed, checksum, reviewer and usage sections.

## 7. Concrete paths / integration conventions

```text
assets/visuals/
  g01-wordmark.svg ... g05-og-cover.webp
  h01-rfid-identity.webp ... h11-checkout-journey.mp4
  p01-groove-band.webp ... p05-event-association.webp
  a01-layer-identity.svg ... a07-six-layer-system.svg
  c01-detection-vs-association.svg ... c06-known-state-settlement.svg
  e01-prayaas-selection.webp ... e04-validation-roadmap.svg
  b01-prototype-assembly.webp ... b04-build-milestones.svg
  t01-sushanth-portrait.webp ... t02-aryan-portrait.webp
  r01-event-ledger.svg ... r02-ambiguity-decision-tree.svg
  f01-project-story-cta.webp
```

Companion files recommended: `assets/visuals/manifest.json` (mapping, alt, proof status, export variants), `docs/visual-source-register.csv` (rights, actual vs concept), `docs/visual-qa-results.md` (screenshots/performance cross-browser). The approved design set is **47 distinct primary assets**: 5 brand, 11 homepage/motion, 5 product, 7 architecture, 6 engineering challenges, 4 evidence, 4 build, 2 founder, 2 research and 1 closing. The initial seven generated scenes are not counted as approved finished replacements; they are references until corrected and integrated.

**Priority order for first visible improvement:** H01–H09 → H10/H11 → P01–P05 → A01–A07 → C01–C06 → the authentic evidence and project-photo items → auxiliary graphics → final QA → Vercel preview.
