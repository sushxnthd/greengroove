from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString, Tag
from pathlib import Path
import json
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: python ui_invariance.py BEFORE AFTER")

before_path = Path(sys.argv[1])
after_path = Path(sys.argv[2])

before = BeautifulSoup(before_path.read_text(encoding="utf-8"), "html.parser")
after = BeautifulSoup(after_path.read_text(encoding="utf-8"), "html.parser")

# Behavior-only attributes are allowed to change. Everything that can visibly affect
# geometry, typography, copy, artwork, classes or inline styling must remain identical.
IGNORED_ATTRS = {
    "href", "target", "rel", "action", "method", "novalidate",
    "readonly", "autocomplete", "tabindex", "preload",
}


def visible_signature(node):
    if isinstance(node, NavigableString):
        parent = node.parent
        if parent and parent.name in {"script", "style", "noscript"}:
            return None
        # Preserve visible copy exactly apart from serialization-only whitespace.
        text = " ".join(str(node).split())
        return ("text", text) if text else None

    if not isinstance(node, Tag):
        return None
    if node.name in {"script", "style", "noscript"}:
        return None

    attrs = {}
    for key, value in sorted(node.attrs.items()):
        low = key.lower()
        if low in IGNORED_ATTRS or low.startswith("aria-") or low.startswith("data-gg-") or low.startswith("data-o-") or "outseta" in low:
            continue
        # Event-handler attributes are behavior, not UI.
        if low.startswith("on"):
            continue
        if isinstance(value, list):
            value = list(value)
        attrs[key] = value

    children = []
    for child in node.children:
        sig = visible_signature(child)
        if sig is not None:
            children.append(sig)
    return (node.name, attrs, children)


def body_sig(doc):
    root = doc.body or doc
    return visible_signature(root)

b = body_sig(before)
a = body_sig(after)

if b != a:
    # Produce a compact first-difference breadcrumb instead of dumping the whole page.
    def first_diff(x, y, path="body"):
        if type(x) is not type(y):
            return path, x, y
        if isinstance(x, tuple):
            if len(x) != len(y):
                return path, x, y
            for i, (xx, yy) in enumerate(zip(x, y)):
                if xx != yy:
                    return first_diff(xx, yy, f"{path}/{i}")
        elif isinstance(x, list):
            if len(x) != len(y):
                return path + "/len", len(x), len(y)
            for i, (xx, yy) in enumerate(zip(x, y)):
                if xx != yy:
                    return first_diff(xx, yy, f"{path}[{i}]")
        elif isinstance(x, dict):
            if x.keys() != y.keys():
                return path + "/attrs", x, y
            for k in x:
                if x[k] != y[k]:
                    return f"{path}/@{k}", x[k], y[k]
        else:
            return path, x, y
        return path, x, y

    where, bv, av = first_diff(b, a)
    raise SystemExit(
        "UI invariance check FAILED. Production cleanup changed visible DOM.\n"
        f"First difference at {where}:\nBEFORE={json.dumps(bv, ensure_ascii=False)[:1200]}\n"
        f"AFTER={json.dumps(av, ensure_ascii=False)[:1200]}"
    )

print("UI invariance check passed: visible DOM/copy/classes/styles/artwork are unchanged.")
