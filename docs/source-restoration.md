# Source restoration

The public page is restored from `41859c3`, before the public-readiness redesign. `scripts/restore_source_layout.py` reproduces the HTML from that baseline. Original section order, headings, inline styles, responsive CSS, Haffer fonts and visual-polish styles are retained.

`assets/vendor/osmo-original-source.js` is an untouched reference copy of the original interaction bundle served at https://slater.app/16596/55554.js. It is not executed. `osmo-native-runtime.js` contains the original page functions needed by this static site, with local GSAP, SplitText and Lenis dependencies. It omits the original service's authentication, navigation fetching, analytics and remote video integration.

Functional adaptations are limited to startup, reduced-motion detection, revealing completed heading masks to prevent clipped descenders, keyboard handling for the original flick cards, and static diagram content in the original modal. `source-repair.js` supplies routes and accessibility state without introducing new sections. `source-repair.css` corrects image fitting, pointer targets and focus visibility without changing typography or section dimensions.

Small technical symbols replace detailed diagrams behind card labels; full diagrams open through the existing modal and full-size link. Illustrations are not prototype photographs or evidence of measured performance. Existing creator logos, original card colors and native animation geometry remain in place.

Run `python scripts/check_restored_site.py` for baseline preservation and local asset checks. GitHub Actions runs `scripts/check_restored_browser.py` at 390, 768 and 1440 pixels in Chromium, Firefox and WebKit, including normal-motion entrances. Historical public-launch scripts belong to the rejected redesign and must not regenerate the current page.
