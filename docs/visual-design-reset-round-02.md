# Green Groove visual redesign — Round 02 (19 October 2026)

**Status:** Design reset, prototype batch generated for user review. No production deployment or live-site file replacements.

## Why Round 01 failed
- Nine square slides, not nine usable visual assets.
- Repeated black/lime UI-grid treatments made every feature indistinguishable.
- Microtext was illegible inside real 200–260px cards.
- Decorative bounding boxes and serial numbers copied a generic dashboard aesthetic.
- Visuals tried to be image, explanation and evidence at once.
- A contact sheet was mistaken for website-level QA.

## Applied GitHub design skills
1. Anthropic frontend-design: select an authored, subject-specific direction; object first; no reliance on template styles.
2. Impeccable: visual hierarchy through photography and composition, not gradient/card decoration; restrain lime; move all narrative text into page DOM.
3. Pixel Perfect Design: preview at actual-use dimensions; compare old/new; run browser screenshot loop (blocked in current local sandbox, pending external browser QA).

## Replacement concept
**Material-first industrial documentary.** Physical RFID identity is shown as an object; shelf event as a real-world gesture; sensing layer as inspectable hardware. No words embedded in any photographs. Negative space, natural tonal range, documentary angle and authentic material surfaces. Original logo stays unchanged.

## Assets produced locally (not yet committed to website)
- 01_identity.webp (1200 square) and 560 responsive variant — RFID wearable product study.
- 02_shelf_action.webp (1200 square) and 560 responsive variant — shop interaction at shelf.
- 03_sensor_hardware.webp (1200 square) and 560 responsive variant — technical sensing components.
- review-contact-sheet.png; at-use-size-comparison.png; preview.html; README.md; manifest.json.

These are AI-generated **concept studies**, not actual photographed prototype parts; compare with the real build before putting them on any evidence section.

## Next quality gate
Show the image-led direction at actual rotating-card dimensions to user, obtain approval, then create separate module imagery and perform real-browser screenshot QA on `#home`. The prior batch should not be used as the production visual system.

## References
- https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
- https://github.com/pbakaus/impeccable
- https://github.com/afterxleep/agents/blob/main/skills/pixel-perfect-design/SKILL.md
