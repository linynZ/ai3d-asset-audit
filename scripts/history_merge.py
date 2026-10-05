"""B5 step 3: merge the two labelling halves and apply the reviewer's overrides.

Every override carries a reason. The merged file is what the paper reports and
what the author signs off.

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
    "cca41fd": "own_pipeline",                             # our bake already flipped -Z; a second flip undid it
}
OVERRIDES = {
    "9760126": {"precheck": "per_frame_animation",
                "reason": "E1 shows an offline per-frame evaluation of the FBX finds this hover "
                          "(0.46-0.68 m at game scale) before import; no metadata count does."},
    "dc81a43": {"note_append": " Reviewer: mixed cause (asset bone/unit scale x Unity BakeMesh semantics); "
                               "kept ASSET as labelled, reported as mixed."},
}


def main():
    labels = json.loads((RES / "history_labels_part1.json").read_text(encoding="utf-8")) + \
             json.loads((RES / "history_labels_part2.json").read_text(encoding="utf-8"))
    applied = []
    for l in labels:
        if l["label"] == "ASSET":
            l["origin"] = ORIGIN.get(l["hash"], "generator")
        o = OVERRIDES.get(l["hash"])
        if o:
            if "precheck" in o:
                applied.append({"hash": l["hash"], "field": "precheck", "from": l["precheck"],
                                "to": o["precheck"], "reason": o["reason"]})
                l["precheck"] = o["precheck"]
            if "note_append" in o:
                l["note"] += o["note_append"]
                applied.append({"hash": l["hash"], "field": "note", "reason": o["note_append"].strip()})
    out = {"status": "drafted by AI labellers + reviewed by the AI assistant; awaiting author sign-off",
           "overrides": applied, "labels": labels}
    (RES / "history_labels.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    asset = [l for l in labels if l["label"] == "ASSET"]
    print(Counter(l["label"] for l in labels))
    print("ASSET fixes:", [(l["hash"], l["precheck"], l["origin"]) for l in asset if l["is_fix"]])
    print("ASSET features:", [(l["hash"], l["precheck"], l["origin"]) for l in asset if not l["is_fix"]])


if __name__ == "__main__":
    main()
