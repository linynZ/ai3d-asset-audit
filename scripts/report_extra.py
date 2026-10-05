"""Summaries for the analyses added after review (B2 baseline, B3 build readout,
B4 extra conditions, E1 phases). Appends them to results/report.json.

Usage: python scripts/report_extra.py   (run after report.py)
"""
import json
from collections import defaultdict
from statistics import median
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "results"


def main():
    rep = json.loads((RES / "report.json").read_text(encoding="utf-8"))

    rows = [json.loads(l) for l in (RES / "decimation_extra.jsonl").read_text().splitlines() if l.strip()]
    b4 = {}
    for frac in (0.125, 0.0625):
        for c in ("S", "S_pb", "W", "N_nn"):
            v = [r for r in rows if r["cond"] == c and r["target_frac"] == frac]
            d = {"n": len(v), "reached": sum(r["reached"] for r in v),
                 "cracked": sum(r["boundary_edges_after_weld"] > 0 for r in v),
                 "triangles_median": median(r["faces"] for r in v),
                 "triangles_min": min(r["faces"] for r in v), "triangles_max": max(r["faces"] for r in v)}
            if "rgb_rmse" in v[0]:
                dd = [r["rgb_rmse"] - r["noise_floor_rmse"] for r in v]
                worst = max(v, key=lambda r: r["rgb_rmse"] - r["noise_floor_rmse"])
                d.update({"rmse_median": median(r["rgb_rmse"] for r in v),
                          "floor_median": median(r["noise_floor_rmse"] for r in v),
                          "rmse_over_floor_median": round(median(dd), 2),
                          "rmse_over_floor_max": round(max(dd), 2), "worst": worst["id"]})
            b4[f"{c}@{frac}"] = d
    rep["B4_extra"] = b4
    mo = [json.loads(l) for l in (RES / "meshopt_check.jsonl").read_text().splitlines() if l.strip()]
    rep["B4_meshopt"] = {f'{c}@{f}': {"n": len(v), "reached": sum(r["reached"] for r in v),
                                      "cracked": sum(r["boundary_edges_after_weld"] > 0 for r in v),
                                      "triangles_median": median(r["triangles"] for r in v)}
                         for f in (0.125, 0.0625) for c in ("S", "W")
                         for v in [[r for r in mo if r["cond"] == c and r["target_frac"] == f]]}

    base = json.loads((RES / "baseline.json").read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for r in base:
        groups[r["group"]].append(r)
    span = lambda xs: [round(min(xs), 3), round(median(xs), 3), round(max(xs), 3)]
    rep["B2_baseline"] = {
        "n": len(base), "closed": sum(r["watertight"] for r in base),
        "edge_manifold": sum(r["edge_manifold"] for r in base),
        "with_self_intersections": sum(r["self_intersecting_faces"] > 0 for r in base),
        "groups": {g: {"n": len(v), "charts_per_1k": span([r["charts_per_1k_tris"] for r in v]),
                       "uv_area_sum": span([r["uv_area_sum"] for r in v]),
                       "seam_split": span([r["seam_split_factor"] for r in v])} for g, v in groups.items()},
    }
    gen = [r for r in json.loads((RES / "hygiene.json").read_text()) if r["group"] in ("npc", "prop")]
    rep["B2_generated_uv"] = {"charts_per_1k": span([1000 * r["uv_charts"] / r["triangles"] for r in gen]),
                              "uv_area_sum": span([r["uv_area_sum"] for r in gen])}

    bt = json.loads((RES / "build_textures.json").read_text())
    rep["B3_build"] = {"generated_by_format_size": bt["generated_by_format_size"],
                       "texture_totals_MiB": bt.get("texture_totals_MiB")}

    rep["E1_phase"] = {g["file"]: g.get("phase_analysis") for g in json.loads((RES / "grounding.json").read_text())}
    (RES / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    for k in ("B4_extra", "B2_baseline", "B2_generated_uv", "B3_build"):
        print(k, json.dumps(rep[k], ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
