"""C step 3: merge the two extractions. Mutual best matches (paraphrase similarity
+ shared source) were computed automatically and checked by hand; four further
pairs were matched by hand (MANUAL). Unmatched claims are kept, marked single.

Usage: python scripts/claims_merge.py
"""
import difflib
import json
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "results"
MANUAL = [("A013", "B015"), ("A014", "B015"), ("A021", "B018"), ("A071", "B030"), ("A020", "B019")]


def refs(c):
    return {s["ref"][:7] if s["type"] == "commit" else s["ref"].split(":")[0] for s in c["sources"]}


def sim(a, b):
    return difflib.SequenceMatcher(None, a["paraphrase_en"].lower(), b["paraphrase_en"].lower()).ratio() + \
        (0.25 if refs(a) & refs(b) else 0)


def main():
    A = json.loads((RES / "claims_extract_a.json").read_text(encoding="utf-8"))
    B = json.loads((RES / "claims_extract_b.json").read_text(encoding="utf-8"))
    best_a = {a["id"]: max(B, key=lambda b: sim(a, b)) for a in A}
    best_b = {b["id"]: max(A, key=lambda a: sim(a, b)) for b in B}
    pairs = [(a["id"], best_a[a["id"]]["id"]) for a in A
             if best_b[best_a[a["id"]]["id"]]["id"] == a["id"] and sim(a, best_a[a["id"]]) >= 0.6]
    pairs += MANUAL
    Ai, Bi = {c["id"]: c for c in A}, {c["id"]: c for c in B}
    merged, used_a, used_b = [], set(), set()
    for a, b in pairs:
        ca, cb = Ai[a], Bi[b]
        merged.append({"id": f"C{len(merged) + 1:03d}", "from": [a, b], "found_by": "both",
                       "text": ca["text"], "text_b": cb["text"], "paraphrase_en": ca["paraphrase_en"],
                       "sources": ca["sources"] + [s for s in cb["sources"] if s not in ca["sources"]],
                       "first_date": min(d for d in (ca["first_date"], cb["first_date"]) if d) if (ca["first_date"] or cb["first_date"]) else None,
                       "subject": ca["subject"], "subject_b": cb["subject"], "kind": ca["kind"], "kind_b": cb["kind"],
                       "asset_scope": ca["asset_scope"]})
        used_a.add(a)
        used_b.add(b)
    for c, used, who in ((A, used_a, "A only"), (B, used_b, "B only")):
        for x in c:
            if x["id"] not in used:
                merged.append({"id": f"C{len(merged) + 1:03d}", "from": [x["id"]], "found_by": who,
                               "text": x["text"], "paraphrase_en": x["paraphrase_en"], "sources": x["sources"],
                               "first_date": x["first_date"], "subject": x["subject"], "kind": x["kind"],
                               "asset_scope": x["asset_scope"]})
    (RES / "claims_merged.json").write_text(json.dumps(merged, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(merged), "claims;", sum(m["found_by"] == "both" for m in merged), "found by both")


if __name__ == "__main__":
    main()
