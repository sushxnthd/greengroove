# Green Groove | Signal / State
**Asset design language v1.0 — 19 October 2026**
**Status:** Proposed art-direction lock, awaiting user review. No production-site change in this commit.

## North star
**A physical action becomes a trustworthy digital state.**

An editorial, industrial and system-driven identity for a student-built RFID + smart-shelf retail prototype. The visual product is **the mechanism**, not neon-lit science fiction.

### Reference mix
- **30% Chirp IoT** — physical device/product storytelling, compact technical panels, structured modular compositions. https://www.behance.net/gallery/225333513/Chirp-IOT-Branding-SaaS-UXUI
- **25% Verden** — generous negative space, tasteful natural/industrial photography, oversized typographic structure, calm green accents. https://dribbble.com/shots/27362121-Verden-Minimalist-Energy-Company-Corporate-Website-About-Page
- **20% Formeta ASSET TAG** — grounded RFID hardware product shots, legible physical form and real materials. https://www.behance.net/gallery/224810435/ASSET-TAG-RFID-Asset-Tracking-Device
- **15% I/O / translucent hardware exploration** — exposed PCB and clearly separated component layers, *where technically accurate*. https://www.behance.net/gallery/43481607/IO
- **10% MERTECH** — scalable, recognizable modularity across hardware, retail and software. https://www.behance.net/gallery/241929461/Mertech-Brand-identity

These are **inspiration references only**. No images, logos, layouts or proprietary artworks are to be copied verbatim or redistributed.

## Palette: Editorial Lime
| Token | Value | Role |
|---|---|---|
| `--gg-paper` | `#F4F4F4` | primary editorial page ground |
| `--gg-porcelain` | `#E8EAE3` | alternate soft paper/card backing |
| `--gg-ink` | `#201D1D` | primary dark copy; existing site's near-black |
| `--gg-charcoal` | `#171A15` | studio photography backdrops / diagram panels |
| `--gg-lime` | `#A1FF62` | signature accent; focus, selected path, active state |
| `--gg-green-strong` | `#78FF45` | high-intensity accent in very small quantities |
| `--gg-text-muted` | `#778078` | muted diagram labels |
| `--gg-hairline` | `#CBD0C5` | connector lines, technical rules |
| `--gg-return` | `#18BDF2` | inverse / return event, used sparingly |
| `--gg-pending` | `#BE9348` | ambiguous / held events, paired with explicit text |
| `--gg-alert` | `#B65E54` | real errors only, paired with explicit text |

**Ratio** across asset portfolio: ~50% light paper and neutral cards, 30% charcoal technical/physical scenes, 15% authentic photographic textures, 5% saturated active-state accents. Inside individual illustrations, limit solid lime area to 5–12%. **Status meaning always uses icon/text as well as color.** Blue is a state-semantic accent, never a second main brand color.

Retain website's light backgrounds and original logo shape; don't force dark mode site-wide. Legacy purple / cyan gradients may still exist in CSS; remove from *asset generation* except where specific existing UI demands compatibility.

## Typography and grid
- Display & editorial headings: preserve site's Haffer XH or existing licensed stack. Medium weight; tight-but-not-colliding line spacing; no counterfeit “techno font”.
- Technical identifiers and readouts: Haffer Mono when available; local text fallback `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.
- Asset text belongs in **editable SVG or HTML**, not baked into photographic renders. Never ask an image model to spell long UI or precise numbers.
- 12-column compositional grid; 8 px baseline; 32–64 px standard inset on 1600px cards; 8–12% crop-safe outer zone.
- Diagram type minimum 18–24 px on 1600×1200 master. Technical numerals can be smaller only when still readable at planned display size.
- Section cards: consistent inner framing, thin 1px stroke, subtle 2–6px corner radius for technical plates; preserve parent website's higher radius where it is already defined. Avoid proliferating random pill shapes.

## Signature motifs
1. **Evidence wire:** one hairline path from a real physical event to a normalized event node and then a materialized state view. One bright node signals a state update. Avoid imaginary wireless beams.
2. **Event ledger strip:** `09:42:11 · S03 · PICK · PENDING`, precisely typeset and internally coherent. Immutable/inverse events should remain visible.
3. **Physical cross-section:** macro hardware with isolated, labeled force path and reader path; photoreal for material, vector overlay for accurate connection.
4. **Crop-window panel:** one tightly cropped piece of hardware or UI on a light or charcoal editorial ground, with one nearby mono caption outside photo.
5. **Six-layer rail:** standardized numbered squares 01–06 with thin connectors, not glowing glass cards.

## Media families
### Family I: Product studies (P/H/B)
Object-first product photos or honest conceptual renders. Single diffuse large studio key light at 45°, soft thin fill, subtle warm neutral bounce, sharp material detail. Background either warm off-white or charcoal; one tiny lime operational accent. 50–85mm-equivalent editorial macro lens; natural shadows. No chrome pedestal, giant LED ring, oversized translucent HUD, Hollywood supermarket, or fictional “AI” interfaces.

### Family II: State diagrams (A/C/R)
Flat SVG/Figma-compatible vector. Four fundamental primitives: token, observed event, decision/hold, accepted cart. Routing uses 90°/45° lines and deliberate arrowheads; grid and margin rules identical for all six layers and six challenges. Color denotes **meaning**, not decoration. Provide mobile stacked version of master A07. Fully scripted/precisely labeled; never generated as a raster infographic.

### Family III: Interface evidence (H04/P03/P04/R01)
Reconstruct *real* app screenshots when available; otherwise visibly mark `Interface concept`. Use existing G/G App UI tokens; no fake transactions, cards, carbon metrics or payment completion. UI should be front-on, cropped to meaningful state changes, not a tilted smartphone in a glowing environment. Animatable by moving a selection highlight, not a fake cinematic AR overlay.

### Family IV: Documentary proofs (E/T/B)
Actual photos, screenshots, letters and source records, professionally cropped only. Narrow off-white rules and restrained metadata labels; no synthetic people, awards, grants, logos or commercial pilots. Link to original evidence and date in HTML captions. Conceal personal information.

### Family V: Editorial motion (H11)
Length ~20s: identity token (0–3) → shelf pickup (3–7) → event association (7–11) → live cart (11–15) → inverse return (15–18) → invoice state (18–22). Motion measured and physical: 200–450ms, only moving property/value/cursor/state, no meaningless loops. 24/30fps MP4, no audio dependency, captions/transcript; reduced-motion receives H10.

## Mapping to the 47-asset specification
- G01–G05: brand system; paper + lime accents, vector first.
- H01–H09: nine **distinct** small editorial objects or diagrams; when viewed together, alternate light/dark/lime distribution. Proposed cadence: H01 dark, H02 light, H03 dark, H04 light, H05 dark, H06 light, H07 dark, H08 light, H09 dark. Rhythm without monotonous dark tech visuals.
- H10–H11: same graphic language as A07, not a totally different visual universe.
- P01–P05: macro, cross-section and actual UI; no inventions about hardware/software.
- A01–A07, C01–C06, R01–R02: system diagrams with consistent primitives and visual meaning.
- E01–E04, B01–B04, T01–T02: authentic records or clearly designated planned evidence.
- F01: strong final editorial crop, ample space for *native* copy.

## Prompt and illustration templates
### Conceptual hardware render
> Premium product editorial photograph of [exact physically plausible object and component detail], isolated on [warm paper / graphite] sweep, soft diffused studio key at 45 degrees, restrained neutral shadow, tactile material fidelity, documentary industrial aesthetic, minimalist Swiss editorial composition, asymmetrical placement and clear negative space, subtle lime #A1FF62 state cue only where functional, no inscriptions, no UI overlays, no glowing rings, no futuristic holograms, no extra components, no fictional logos, physically realistic, 4:3 composition, 10% crop safe.

### Engineering vector generation (NOT image-generation)
> Construct editable SVG on 12-column 8px grid, background [paper/charcoal], accurate labels [node list] and edges [edge list], accepted=lime, return=cyan, pending=ochre, unresolved state explicit, arrowheads and line thickness consistent, all text editable and live, no impossible shortcuts, include accessible description and a mobile stacked layout.

### Documentary layouts
> Use approved authentic source media only. Crop non-destructively, add 1px caption/keyline outside photograph, note document date, credit and status in HTML. Do not remove essential legal/technical context or imply endorsement.

## Dos, don'ts, approval
**Do:** precise use of negative space; visible real hardware; sparse product macro; split paper/dark composition; system-state storytelling; meaningful lime; accurate inverse events; sober publication-worthy captions.

**Don't:** cyan/purple gradients over everything, cinematic green warehouses, unrealistic wristband LEDs, holographic shopping carts, fabricated photos of creators, invented AI/computer-vision modules, fake pilot photos or logos, deceptive carbon-savings/instant-payment UI, 47 near-identical renders.

**QA gate:** Review a single contact sheet containing (1) H01, (2) H02, (3) H04, (4) A02, (5) C05, (6) P01 and (7) E01's approved placeholder layout. If these seven look like one family at full size *and* 220px thumbnail scale, move to all 47. Only implement after section-level approvals. Do not deploy until Vercel preview QA.

## Reference links
- https://www.behance.net/gallery/225333513/Chirp-IOT-Branding-SaaS-UXUI
- https://www.behance.net/gallery/224810435/ASSET-TAG-RFID-Asset-Tracking-Device
- https://www.behance.net/gallery/43481607/IO
- https://www.behance.net/gallery/241929461/Mertech-Brand-identity
- https://dribbble.com/shots/27362121-Verden-Minimalist-Energy-Company-Corporate-Website-About-Page
- https://dribbble.com/shots/27279488-Admin-Dashboard-UI-Dark-Green-Theme-with-Charts-Data-Tables
