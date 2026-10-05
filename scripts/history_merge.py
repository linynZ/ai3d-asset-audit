"""B5 step 3: merge the two labelling halves and apply the reviewer's overrides.

Two rounds of overrides, each with its reason:
  round 1 - first review by the AI assistant (before the draft);
  round 2 - after the external fact-check and peer review of the draft, which
            showed that the NPCs' "-Z facing" is caused by the importer
            (UniGLTF reverses Z by default; the GLBs face glTF +Z, see
            results/facing_sheet.png), and that two labels broke the plan's
            "ambiguous -> OTHER" rule.
Both rounds are reported as deviations in the paper.

Usage: python scripts/history_merge.py
"""
import json
from collections import Counter
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "results"

# origin of an ASSET defect: did the generator ship it, or did our own processing introduce it?
ORIGIN = {
    "95cf232": "own_pipeline", "288327d": "own_pipeline",  # root rotation node dropped by our GLB->OBJ step
    "37e5b4e": "own_pipeline",                             # our decimation (see B4: it tore the mesh)
}
OVERRIDES = [
    ("round1", "9760126", {"precheck": "per_frame_animation"},
     "E1 shows an offline per-frame evaluation of the FBX finds this hover (0.46-0.68 m at game scale) "
     "before import; no metadata count does."),
    ("round2", "f3da6c2", {"label": "ENGINE", "precheck": None, "property": "importer reverses Z (UniGLTF default)"},
     "Rendering every GLB in glTF coordinates shows the front faces +Z, as the glTF spec requires; the game's "
     "importer (UniGLTF, reverseAxis=Default -> Z) maps it to Unity -Z. A spec-compliant hand-made GLB would "
     "face the same way, so the root cause is the importer convention, not the generated asset."),
    ("round2", "cca41fd", {"label": "OTHER", "precheck": None, "property": None},
     "Two compensating 180-degree turns in our own code cancelled each other on the boss (FBX path, different "
     "importer); which property the first turn compensated is not established, so by the plan's rule the "
     "ambiguous case goes to OTHER."),
    ("round2", "dc81a43", {"label": "OTHER", "precheck": None, "property": None},
     "Labeller confidence low and cause mixed (asset bone/unit scale x Unity BakeMesh semantics); the plan "
     "sends ambiguous cases to OTHER. Round 1 had kept it as ASSET, contrary to that rule."),
]


def main():
    labels = json.loads((RES / "history_labels_part1.json").read_text(encoding="utf-8")) + \
             json.loads((RES / "history_labels_part2.json").read_text(encoding="utf-8"))
    by_hash = {l["hash"]: l for l in labels}
    applied = []
    for rnd, h, changes, reason in OVERRIDES:
        l = by_hash[h]
        for field, new in changes.items():
            applied.append({"round": rnd, "hash": h, "field": field, "from": l.get(field), "to": new, "reason": reason})
            l[field] = new
    for l in labels:
        l["origin"] = ORIGIN.get(l["hash"], "generator") if l["label"] == "ASSET" else None
    out = {"status": "drafted by two AI labellers; reviewed by the AI assistant (two rounds, see overrides); "
                     "signed off by the author 2026-10-05",
           "overrides": applied, "labels": labels}
    (RES / "history_labels.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    asset = [l for l in labels if l["label"] == "ASSET"]
    print(Counter(l["label"] for l in labels))
    print("ASSET fixes:", [(l["hash"], l["precheck"], l["origin"]) for l in asset if l["is_fix"]])
    print("ASSET features:", [(l["hash"], l["precheck"], l["origin"]) for l in asset if not l["is_fix"]])
    print("ENGINE:", [(l["hash"], l["property"]) for l in labels if l["label"] == "ENGINE"])


if __name__ == "__main__":
    main()
