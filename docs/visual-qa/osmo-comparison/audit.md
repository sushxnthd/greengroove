# Osmo fidelity audit — 24 October 2026

Reference: https://www.osmo.supply/, inspected live at 1363 × 936. Published Green Groove baseline: `c2ec6687cf0ddc67d26880e92a81fc26c850bf06`, including the founder-portrait revert.

The previous checks proved routes and component behavior. They did not establish visual fidelity. The static guard compared against Green Groove commit `41859c3`, which already contained editorial styling overrides; preserving that snapshot also preserved those overrides.

## Measured differences

| Area | Live Osmo | Published Green Groove | First repair |
| --- | --- | --- | --- |
| Hero heading tracking at 106.011px | -6.361px | -6.891px | -6.361px |
| Second hero heading height | 84.828px | 190.844px | 190.844px; still unresolved |
| Card-ring top | 538.656px | 644.672px | Content-fit work remains |
| Desktop evidence/pricing card width | 530.047px | 643.656px | 530.047px |
| Native colored button fill | Solid | Added green-to-blue gradient | Solid, using the retained Green Groove blue |
| Header wordmark artwork aspect ratio | 540:156 | 170:15 | Not changed in this pass |

The header logo boxes themselves have the same dimensions. The replacement artwork has a much flatter aspect ratio and therefore looks much smaller inside its box. It needs an asset-specific correction, rather than a global navigation resize.

The hero's longer Green Groove wording wraps into two lines at the original type scale. That shifts the description and card ring down by approximately 106px. Restoring tracking alone does not solve the copy-fit conflict. The wording has deliberately not been rewritten or shrunk in this first pass.

Longer evidence copy also changes card height. The first repair corrects width, paragraph type and button styling; it does not claim pixel-identical card heights with Osmo's much shorter pricing copy.

## First scoped repair

- Stop loading the earlier visual-polish and curated-integration global layers.
- Remove the editorial pricing typography overrides, gradient override and DOM width-fitting script.
- Keep original Osmo CSS/fonts, section markup, Green Groove wording and the green/blue brand tokens.
- Constrain adapted prose to the source desktop card width. Keep responsive cards flexible on smaller screens.
- Retain illustration `object-fit` without forcing image opacity, backgrounds or animation transforms.
- Add regressions for measured native tracking, solid fills and desktop card widths.
- Keep the founder-photo revert intact.

## Remaining work — no visual completion claim

1. Hero copy-fit and the resulting vertical rhythm.
2. Header logo artwork sizing within its original box.
3. Founder imagery, using the user's approved one-at-a-time workflow; no portrait swap is included here.
4. Section-by-section asset placement, density and crop review against the live reference.
5. Detailed motion and interaction-state comparison, beyond click-through smoke tests.

Screenshots: [reference](osmo-cards.jpg), [published build](published-cards.jpg), [first repair](repaired-cards.jpg). Raw geometry and type measurements are in [desktop-measurements.json](desktop-measurements.json).

This is a staged repair and audit, not a launch-ready or pixel-perfect certification.
