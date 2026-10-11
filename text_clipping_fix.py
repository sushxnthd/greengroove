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

    viewport_needles = (
        "The queue was the symptom. Manual reconstruction at checkout was the deeper problem.",
        "Returns reverse earlier state instead of silently overwriting history, so the system can recover cleanly.",
    )

    # Target the two evidence-card descriptions structurally rather than by their
    # wording so future editorial copy changes cannot disable the clipping guard.
    pricing_bodies = soup.select(".pricing-card .pricing-benefit__start > p")[:2]
    wrap_count = 0
    for tag in pricing_bodies:
        add_class(tag, "gg-wrap-copy")
        wrap_count += 1

    viewport_count = 0
    for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        text = norm(tag.get_text(" ", strip=True))
        if any(needle in text for needle in viewport_needles):
            add_class(tag, "gg-viewport-copy")
            viewport_count += 1

    if not soup.find(id="gg-text-clipping-fix"):
        style = soup.new_tag("style", id="gg-text-clipping-fix")
        style.string = r"""
/* Green Groove: tailored card copy must never inherit source-template max-content clipping. */
.pricing-card .gg-wrap-copy {
  display: block !important;
  white-space: normal !important;
  min-width: 0 !important;
  box-sizing: border-box !important;
  overflow-wrap: normal !important;
  word-break: normal !important;
}

/* These two narrative lines inherit Osmo's desktop-width grid on narrower screens. */
.gg-viewport-copy {
  white-space: normal !important;
  box-sizing: border-box !important;
  overflow-wrap: anywhere !important;
  word-break: normal !important;
}
"""
        (soup.head or soup).append(style)

    if not soup.find(id="gg-text-clipping-guard"):
        script = soup.new_tag("script", id="gg-text-clipping-guard")
        script.string = r"""
(function () {
  var queued = false;
  var observedCards = new WeakSet();
  var cardObserver = null;

  function fitOverviewMask() {
    var heading = document.getElementById('overview');
    if (!heading) return;
    var mask = heading.closest('.about-card__text-h');
    if (!mask) return;

    var headingRect = heading.getBoundingClientRect();
    var maskRect = mask.getBoundingClientRect();
    var needed = Math.ceil(headingRect.height + 4);
    if (maskRect.height + 0.5 < needed) {
      mask.style.setProperty('height', needed + 'px', 'important');
      mask.style.setProperty('min-height', needed + 'px', 'important');
    }
  }

  function fitCardCopy() {
    document.querySelectorAll('.pricing-card .gg-wrap-copy').forEach(function (el) {
      el.style.setProperty('display', 'block', 'important');
      el.style.setProperty('white-space', 'normal', 'important');
      el.style.setProperty('min-width', '0', 'important');
      el.style.setProperty('overflow-wrap', 'normal', 'important');

      var card = el.closest('.pricing-card');
      if (!card) return;

      if (cardObserver && !observedCards.has(card)) {
        observedCards.add(card);
        cardObserver.observe(card);
      }

      var rect = el.getBoundingClientRect();
      var cardRect = card.getBoundingClientRect();
      var gutter = window.innerWidth <= 480 ? 12 : 16;
      var available = Math.max(96, cardRect.right - rect.left - gutter);
      var editorialCap = window.innerWidth <= 767 ? available : Math.min(544, available);
      var current = rect.width;

      /* Keep the copy inside its card while preserving the deliberate editorial
         line length introduced by pricing_copy_refine.py. */
      if (Math.abs(current - editorialCap) > 0.75) {
        el.style.setProperty('width', editorialCap + 'px', 'important');
        el.style.setProperty('max-width', editorialCap + 'px', 'important');
      }
    });
  }

  function fitViewportCopy() {
    document.querySelectorAll('.gg-viewport-copy').forEach(function (el) {
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
    fitOverviewMask();
    fitCardCopy();
    fitViewportCopy();
  }

  function queueFit() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () {
      queued = false;
      fitGreenGrooveCopy();
    });
  }

  if ('ResizeObserver' in window) {
    cardObserver = new ResizeObserver(function () {
      queueFit();
    });
  }

  function settleFit() {
    queueFit();
    requestAnimationFrame(queueFit);
    setTimeout(queueFit, 50);
    setTimeout(queueFit, 250);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', settleFit, { once: true });
  } else {
    settleFit();
  }
  window.addEventListener('load', settleFit, { once: true });
  window.addEventListener('resize', queueFit, { passive: true });
})();
"""
        (soup.body or soup).append(script)

    if wrap_count < 2:
        raise RuntimeError(f"Expected at least 2 pricing copy targets, found {wrap_count}")
    if viewport_count < 2:
        raise RuntimeError(f"Expected at least 2 viewport copy targets, found {viewport_count}")

    path.write_text(str(soup), encoding="utf-8")
    print(f"Applied text clipping fixes: pricing={wrap_count}, viewport={viewport_count}")


if __name__ == "__main__":
    main()
