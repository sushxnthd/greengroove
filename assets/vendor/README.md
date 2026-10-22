# Existing-site runtime assets

These files make the existing Green Groove layout independent of third-party runtime CDNs. They preserve the typography and layout of the site's prior source.

- `style-0.css`: original Webflow layout CSS. Relative font paths replace CDN paths.
- `style-1.css` through `style-4.css`: existing global, component and layout styles formerly loaded through Slater. Identical font files are deduplicated.
- `script-2.js`, `script-3.js`, `script-4.js`, `script-5.js`, `script-7.js`, `script-8.js`: GSAP 3.15 animation core, Draggable, InertiaPlugin, ScrollTrigger, Observer, and the previously used CustomEase 3.14. Original package copyright/license headers are retained.
- `animation-runtime.js`: only the animation functions required by this static site, adapted from its existing licensed source. Account/authentication, analytics, payment, form submission, remote resource discovery, page fetching, and video streaming integrations are excluded.
- `resource-*`: original site fonts and a legacy checkbox mark referenced by retained CSS.

The page itself makes no third-party runtime requests. Links to public project and programme sources remain ordinary visitor-initiated links.
