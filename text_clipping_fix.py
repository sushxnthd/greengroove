from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def add_class(tag, class_name: str) -> None:
    classes = list(tag.get("class", []))
    if class_name not in classes:
        classes.append(class_name)
        tag["class"] = classes


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    wrap_needles = (
        "Selected in the urban private category under NCERT PRAYAAS",
        "Groove Band + sensor shelves + G/G App turn physical product movement into a live digital cart.",
    )
    viewport_needles = (
        "The queue was the symptom. Manual reconstruction at checkout was the deeper problem.",
        "Returns reverse earlier state instead of silently overwriting history, so the system can recover cleanly.",
    )

    wrap_count = 0
    viewport_count = 0
    for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        text = norm(tag.get_text(" ", strip=True))
        if any(needle in text for needle in wrap_needles):
            add_class(tag, "gg-wrap-copy")
            wrap_count += 1
        if any(needle in text for needle in viewport_needles):
            add_class(tag, "gg-viewport-copy")
            viewport_count += 1

    if not soup.find(id="gg-text-clipping-fix"):
        style = soup.new_tag("style", id="gg-text-clipping-fix")
        style.string = r"""
/* Green Groove: tailored long-form copy must never inherit max-content clipping. */
.pricing-card .gg-wrap-copy {
  display: block !important;
  white-space: normal !important;
  min-width: 0 !important;
  box-sizing: border-box !important;
  overflow-wrap: anywhere !important;
  word-break: normal !important;
}

/* These two narrative lines inherit Osmo's desktop-width grid on narrower screens. */
.gg-viewport-copy {
  white-space: normal !important;
  box-sizing: border-box !important;
  overflow-wrap: anywhere !important;
  word-break: normal !important;
}

/* The source reveal mask becomes 4px shorter than this heading at the mobile breakpoint. */
@media (max-width: 480px) {
  .about-card__text-h:has(#overview) {
    height: 48px !important;
    min-height: 48px !important;
  }
}
"""
        (soup.head or soup).append(style)

    if not soup.find(id="gg-text-clipping-guard"):
        script = soup.new_tag("script", id="gg-text-clipping-guard")
        script.string = r"""
(function () {
  function fitCardCopy() {
    document.querySelectorAll('.pricing-card .gg-wrap-copy').forEach(function (el) {
      el.style.removeProperty('width');
      el.style.removeProperty('max-width');
      el.style.setProperty('display', 'block', 'important');
      el.style.setProperty('white-space', 'normal', 'important');
      el.style.setProperty('min-width', '0', 'important');
      el.style.setProperty('overflow-wrap', 'anywhere', 'important');

      var card = el.closest('.pricing-card');
      if (!card) return;
      var rect = el.getBoundingClientRect();
      var cardRect = card.getBoundingClientRect();
      var gutter = window.innerWidth <= 480 ? 12 : 16;
      var available = Math.max(96, cardRect.right - rect.left - gutter);

      el.style.setProperty('width', available + 'px', 'important');
      el.style.setProperty('max-width', available + 'px', 'important');
    });
  }

  function fitViewportCopy() {
    document.querySelectorAll('.gg-viewport-copy').forEach(function (el) {
      el.style.removeProperty('width');
      el.style.removeProperty('max-width');

      var rect = el.getBoundingClientRect();
      var gutter = window.innerWidth <= 480 ? 16 : 24;
      var available = Math.max(120, window.innerWidth - rect.left - gutter);

      if (rect.width > available + 1) {
        el.style.setProperty('width', available + 'px', 'important');
        el.style.setProperty('max-width', available + 'px', 'important');
      }
    });
  }

  function fitGreenGrooveCopy() {
    fitCardCopy();
    fitViewportCopy();
  }

  var queued = false;
  function queueFit() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () {
      queued = false;
      fitGreenGrooveCopy();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', queueFit, { once: true });
  } else {
    queueFit();
  }
  window.addEventListener('load', queueFit, { once: true });
  window.addEventListener('resize', queueFit, { passive: true });
})();
"""
        (soup.body or soup).append(script)

    if wrap_count < 2:
        raise RuntimeError(f"Expected at least 2 long pricing copy targets, found {wrap_count}")
    if viewport_count < 2:
        raise RuntimeError(f"Expected at least 2 viewport copy targets, found {viewport_count}")

    path.write_text(str(soup), encoding="utf-8")
    print(f"Applied text clipping fixes: pricing={wrap_count}, viewport={viewport_count}")


if __name__ == "__main__":
    main()
