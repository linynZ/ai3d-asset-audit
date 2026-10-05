"""C/D step 5: compare the two judges, apply written resolutions, and summarise
H6-H9 into results/report.json and results/claims.json.

RESOLUTIONS: final verdict for every claim where the judges disagree, with reason.
REVISED: for each wrong claim, whether a later commit / comment / doc up to the
final build states the corrected version (H7), with the evidence.

Usage: python scripts/report_cd.py
"""
import json
from collections import Counter
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "results"
# Resolution rule (written before resolving): a verdict needs a measurement of the asset the claim is
# about; inferences from other assets or from offline numbers about engine-side readings -> UNTESTABLE.
RESOLUTIONS = {
    "C009": ("OUT_OF_SCOPE", "J2: the statement concerns VRM/MToon materials (ffe082d), not generated assets"),
    "C013": ("UNTESTABLE", "height 0.993 measured, but the cause (polearm) is not measured; the cross-asset height pattern is mixed (rome_guardian with sword 1.122)"),
    "C016": ("UNTESTABLE", "renders show four legs but tassel fusion is not measurable from them"),
    "C030": ("UNTESTABLE", "engine-side BakeMesh readings not reproduced; E1 does not bear on a constant (non-bobbing) hover"),
    "C032": ("UNTESTABLE", "engine readings not reproduced (J2 notes 0.68 equals the offline max lift 0.684; recorded as a coincidence, not evidence)"),
    "C033": ("UNTESTABLE", "engine readings not reproduced"),
    "C035": ("UNTESTABLE", "engine placement not measured; the other clips never play in the final build (defects.json D10), so they do not bear on it"),
    "C046": ("CONFIRMED", "J2: conventions.json xuanji_raw primitives=1, materials=1, i.e. one draw call per renderer"),
    "C049": ("UNTESTABLE", "the companion's facing was not rendered; inference from the NPCs is not a measurement of this asset"),
    "C051": ("UNTESTABLE", "normalisation axis of the tool output not measured (J2's evidence concerns pitch, not the axis)"),
    "C062": ("CONFIRMED", "J2: every GLB embeds a 4096^2 base-colour image (conventions.json)"),
    "C063": ("PARTLY", "consistency across assets is true (same root rotation, all fronts at +Z), the -Z cause is wrong: rule PARTLY = right observation, wrong cause"),
    "C067": ("UNTESTABLE", "engine placement not measured"),
    "C071": ("UNTESTABLE", "baked prefab not measured; inference from the root rotation only"),
    "C073": ("UNTESTABLE", "normal map present (build_textures.json xuanji_normal) but metallic/smoothness values not measured"),
    "C077": ("UNTESTABLE", "identity of the characters is not part of the audit; the manifest names reflect the developer's later correction, not a measurement"),
    "C078": ("UNTESTABLE", "as C077"),
    "C079": ("UNTESTABLE", "as C077"),
    "C082": ("UNTESTABLE", "engine readings not reproduced"),
    "C083": ("CONFIRMED", "build_textures.json textures: xuanji_basecolor 2048 (DXT1), xuanji_normal 1024 (DXT5), no metallic-roughness map"),
}
REVISED = {        # id -> (True/False, evidence), checked with git grep / git log at 87fdd16
    "C003": (False, "no later commit or comment states that the origin is at the base"),
    "C010": (False, "87fdd16 NPCModelSetupTool.cs:34 still says 'Hunyuan front-view exports face -Z'"),
    "C063": (False, "never withdrawn; the related boss-tool comment (claim C022, FinaleBossModelTool.cs:96) cites the -Z facing as an 'NPC-pipeline finding'"),
    "C011": (False, "no later text attributes the facing to the importer"),
    "C029": (False, "89c36d7's conclusion is never withdrawn; GroundSnap keeps loop sampling without comment on it"),
    "C041": (True, "37e5b4e, 36 minutes later, states the actual result 497,850 -> 82,829 (claim C043); the design note's 'converged at 105,820' was left unchanged"),
    "C042": (False, "87fdd16 tools/decimate_xuanji.py:76 still says 'UV seam islands are the hard floor'"),
    "C053": (True, "288327d and XuanjiModelTool comments replace -90 with +90"),
}


def kappa(a, b):
    cats = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def main():
    claims = {c["id"]: c for c in json.loads((RES / "claims_merged.json").read_text(encoding="utf-8"))}
    j1 = {v["id"]: v for v in json.loads((RES / "claims_judge1.json").read_text(encoding="utf-8"))}
    j2 = {v["id"]: v for v in json.loads((RES / "claims_judge2.json").read_text(encoding="utf-8"))}
    ids = sorted(claims)
    a, b = [j1[i]["verdict"] for i in ids], [j2[i]["verdict"] for i in ids]
    disagree = [i for i in ids if j1[i]["verdict"] != j2[i]["verdict"]]
    final = []
    for i in ids:
        if i in RESOLUTIONS:
            v, why = RESOLUTIONS[i]
        elif j1[i]["verdict"] == j2[i]["verdict"]:
            v, why = j1[i]["verdict"], "judges agree"
        else:
            v, why = None, "UNRESOLVED"
        row = {**claims[i], "judge1": j1[i], "judge2": j2[i], "verdict": v, "resolution": why}
        if v in ("CONTRADICTED", "PARTLY"):
            row["revised_later"], row["revised_evidence"] = REVISED.get(i, (None, "not yet checked"))
        final.append(row)
    status = ("extracted by two AI agents; judged by the AI assistant (judge 1) and an independent AI agent "
              "(judge 2); disagreements resolved by the assistant under written rules; reviewed and signed off by "
              "the author 2026-10-05")
    (RES / "claims.json").write_text(json.dumps({"status": status, "claims": final}, indent=1, ensure_ascii=False),
                                     encoding="utf-8")

    testable = [r for r in final if r["verdict"] in ("CONFIRMED", "CONTRADICTED", "PARTLY")]
    wrong = [r for r in testable if r["verdict"] in ("CONTRADICTED", "PARTLY")]
    by_kind = {k: {"testable": sum(r["kind"] == k for r in testable), "wrong": sum(r["kind"] == k for r in wrong)}
               for k in ("property", "magnitude", "effect", "cause")}
    by_subject = {s: {"testable": sum(r["subject"] == s for r in testable), "wrong": sum(r["subject"] == s for r in wrong)}
                  for s in sorted({r["subject"] for r in final})}
    rep = json.loads((RES / "report.json").read_text(encoding="utf-8"))
    rep["C"] = {
        "claims": len(final), "found_by_both": sum(r["found_by"] == "both" for r in final),
        "judge_agreement": round(1 - len(disagree) / len(ids), 3), "cohen_kappa": kappa(a, b),
        "disagreements": disagree, "unresolved": [r["id"] for r in final if r["verdict"] is None],
        "verdicts": Counter(r["verdict"] for r in final),
        "testable": len(testable), "wrong": len(wrong),
        "wrong_share": round(len(wrong) / len(testable), 3) if testable else None,
        "H6_wrong_ge_20pct": (len(wrong) / len(testable) >= 0.2) if testable else None,
        "by_kind": by_kind, "by_subject": by_subject,
        "wrong_ids": [r["id"] for r in wrong],
        "contradicted_never_revised": sum(r.get("revised_later") is False for r in wrong if r["verdict"] == "CONTRADICTED"),
        "contradicted": sum(r["verdict"] == "CONTRADICTED" for r in wrong),
    }
    if (RES / "defects.json").exists():
        d = json.loads((RES / "defects.json").read_text(encoding="utf-8"))
        d = d["defects"] if isinstance(d, dict) else d
        rep["D"] = {"defects": len(d),
                    "present_in_final_build": [x["id"] for x in d if x.get("present_in_final_build") is True],
                    "visible_on_screen": {str(k): v for k, v in Counter(str(x.get("visible_on_screen")) for x in d).items()},
                    "observed_channel": Counter((x.get("first_observed") or {}).get("channel") for x in d)}
    (RES / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(rep["C"], indent=1, ensure_ascii=False, default=str))
    for i in disagree:
        print(i, j1[i]["verdict"], "|", j2[i]["verdict"], "|", claims[i]["paraphrase_en"][:90])
        print("    J1:", j1[i]["evidence"][:150]); print("    J2:", j2[i]["evidence"][:150])


if __name__ == "__main__":
    main()
