from __future__ import annotations

import json
from pathlib import Path

qa_path = Path("qa-report.json")
probe_path = Path("about-probe.json")

qa = json.loads(qa_path.read_text(encoding="utf-8"))
probe = json.loads(probe_path.read_text(encoding="utf-8"))

attempts = {a.get("activation"): a for a in probe.get("attempts", [])}
required = ("click", "enter", "space")
verification = {}

for activation in required:
    a = attempts.get(activation)
    if not a or a.get("error"):
        verification[activation] = False
        continue
    before_hash = a.get("beforeBodyHtmlHash")
    frames = a.get("frames") or []
    body_changed = any((f.get("state") or {}).get("bodyHtmlHash") not in {None, before_hash} for f in frames)
    focus_moved_to_close = any("close" in str((f.get("state") or {}).get("active", "")).lower() for f in frames)
    no_errors = not (a.get("pageErrors") or [])
    verification[activation] = bool(body_changed and focus_moved_to_close and no_errors)

if not all(verification.values()):
    raise SystemExit(f"About interaction verification failed: {verification}")

warning_fragment = "control-023 'About'"
qa["warnings"] = [w for w in qa.get("warnings", []) if warning_fragment not in w]
qa["about_interaction_verified"] = {
    "pointer_click": verification["click"],
    "keyboard_enter": verification["enter"],
    "keyboard_space": verification["space"],
    "evidence": "Activation changes global DOM state and transfers focus to the Close control without page errors.",
}

for meta in qa.get("viewports", {}).get("desktop", {}).get("controls_exercised", []):
    if meta.get("id") == "control-023" and meta.get("text") == "About":
        meta["result"] = "clicked-state-changed"
        meta["probeVerified"] = True

qa_path.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("About interaction verified by pointer, Enter and Space; false idempotence warning reconciled.")
