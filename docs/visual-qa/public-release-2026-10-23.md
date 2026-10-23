# Green Groove public release — 23 October 2026

## Public-facing changes

- Preserved canonical logo assets and existing page geometry.
- Replaced dense hero thumbnails with nine original technical symbols, reviewed in three batches at 220px. Full diagrams remain available through the system-detail views.
- Replaced the empty video reel with an explicitly illustrative, browser-only shopping-state walkthrough.
- Added inverse returns, held-event handling, invoice blocking, resolution and reset to that model.
- Added specific detail views for all six system layers and gallery components.
- Removed template designers’ social profiles, hidden resource sitemap, unused remote video configuration, account/payment integrations, signup fields and synthetic signup success messages.
- Replaced stale resource dates and inactive labels. Corrected recognition, component, source and roadmap destinations.
- Made the Today/Next control show existing support versus planned validation.
- Added programme-source links and concise questions about prototype status, diagrams and next tests.
- Added native dialog focus/Escape behavior, menu keyboard support, focus outlines, a skip link, gallery previous/next buttons, reduced-motion support and motion control.
- Kept fonts, styles and animation dependencies local; removed third-party runtime requests.
- Repaired the missing social preview, removed duplicate viewport/icon declarations and preserved browser zoom. Added robots.txt and sitemap.xml.
- Retired the auto-regeneration workflow that could overwrite the reviewed public document. Added checks of the actual public document instead.

## Checks completed before publishing

- Static resource, fragment, duplicate-ID, nested-control, image-alt, button/link-name and social-preview checks: passed.
- JavaScript syntax checks: passed.
- Browser inspection at 390px, 768px and 1440px using actual iframe viewports in the connected Chromium browser, including reduced motion: no horizontal page overflow.
- Browser walkthrough: pick milk, pick yogurt, return milk => ₹25; held pickup does not change total; invoice blocked while held; resolve => ₹50; confirm invoice explicitly takes no payment.
- Mobile menu -> Groove Band detail: correct content and diagram.
- Gallery Next -> Green Grooves -> detail: correct shelf-sensing content.
- Today/Next: existing support versus technical testing/field evaluation.
- Founder panel: original creators, with unrelated template accounts removed.

Cross-engine results are recorded separately by CI. Local browser inspection does not assert Firefox or WebKit results.

## Source grounding

The Global Times, 15 December 2025, page 11, reports the creators, PRAYAAS selection, project description and ₹50,000 grant (in two installments): https://theglobaltimes.in/archives/december-15-2025.pdf

Programme information: https://www.ncert.nic.in/desm/prayaas.php?ln=en

Mentor’s institutional profile: https://sense.iitd.ac.in/faculty-profile/7

Institutional mentorship and planned validation are described as development support, not a commercial performance certification. No invented pilot results, testimonials, product photos or app screenshots are introduced.

## Follow-up section review

The full-page screenshot review found residual third-party logo vectors, mismatched social glyphs, unfinished timeline placeholders, diagrams overlapping card text, hidden second-author text, and low-contrast white text on green cards. The follow-up removes those template remnants, keeps both creators visible, uses simple symbols in layer summaries and finding visuals, links full diagrams, and replaces the timeline with semantic project steps. Notes and findings now have visible named previous/next buttons and labelled bullet controls. Build details show the selected component's own illustration. Reduced-motion mode also disables root smooth scrolling and slider tweens.

The static gate now checks local diagram links and rejects the removed template patterns. The browser gate additionally exercises all six layer dialogs, all five project notes, all six findings, the FAQ and mobile footer accordions at each viewport. Static dependency and JavaScript syntax checks passed before publication; browser results are available in the commit's GitHub Actions run.

The final interaction pass also made each project note open its full layer diagram, removed a transparent caption layer from pointer hit testing, kept inactive architecture cards out of the tab order, and verified that explicit motion preferences work in both directions. The regression gate covers the note dialogs and the enable/pause motion cycle.

A screenshot check caught the global asset-visibility rule overriding inactive finding images. Specific opacity rules now keep only the selected symbol visible, with a regression assertion. CI uses the official Playwright Python 1.63.0 Noble image and a matching pinned package, so browser dependencies are preinstalled instead of being downloaded from the slow Ubuntu mirror on every run. Reference: https://playwright.dev/python/docs/docker .
