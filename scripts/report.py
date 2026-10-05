"""Build results/report.json and results/report.md from the per-audit outputs.

Usage: python scripts/report.py
"""
import json
from collections import Counter
from math import sqrt
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
RAW_GROUPS = ("npc", "prop")  # the 24 assets from the "50k faces" preset


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def span(xs, nd=3):
    xs = list(xs)
    return {"min": round(min(xs), nd), "median": round(median(xs), nd), "max": round(max(xs), nd)}


def load(name):
    p = RES / name
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    rep = {}
    conv = [r for r in load("conventions.json") if r["group"] in RAW_GROUPS]
    n = len(conv)
    rep["B1"] = {
        "n": n,
        "largest_extent": span(r["largest_extent"] for r in conv),
        "within_0.9_1.2": sum(0.9 <= r["largest_extent"] <= 1.2 for r in conv),
        "outside_0.9_1.2": [(r["id"], r["largest_extent"]) for r in conv if not 0.9 <= r["largest_extent"] <= 1.2],
        "root_rotation_nonidentity": sum(bool(r["node_transforms"]) for r in conv),
        "root_rotations": Counter(json.dumps(r["node_transforms"][0].get("rotation")) for r in conv if r["node_transforms"]),
        "double_sided": sum(all(r["double_sided"]) for r in conv),
        "pivot_y_frac": span((r["pivot_frac_xyz"][1] for r in conv), 4),
        "pivot_x_frac": span(r["pivot_frac_xyz"][0] for r in conv),
        "pivot_z_frac": span(r["pivot_frac_xyz"][2] for r in conv),
        "triangles": span((r["triangles"] for r in conv), 0),
        "vertices": span((r["vertices"] for r in conv), 0),
        "textures": Counter(json.dumps([(i["width"], i["height"]) for i in r["images"]]) for r in conv),
        "material_extensions": Counter(json.dumps(r["material_extensions"]) for r in conv),
        "generator_field": Counter(r["generator"] for r in conv),
    }
    mib = 2 ** 20
    rep["B3"] = {
        "geometry_MiB": span(r["cost"]["geometry_bytes_as_stored"] / mib for r in conv),
        "texture_rgba8_MiB": span(r["cost"]["texture_rgba8_mip_bytes"] / mib for r in conv),
        "texture_bc7_MiB": span(r["cost"]["texture_bc7_mip_bytes"] / mib for r in conv),
        "texture_bc1_MiB": span(r["cost"]["texture_bc1_mip_bytes"] / mib for r in conv),
        "ratio_bc1_over_geometry": span(r["cost"]["texture_bc1_mip_bytes"] / r["cost"]["geometry_bytes_as_stored"] for r in conv),
        "ratio_bc7_over_geometry": span(r["cost"]["texture_bc7_mip_bytes"] / r["cost"]["geometry_bytes_as_stored"] for r in conv),
        "H3_holds_24": all(r["cost"]["texture_bc1_mip_bytes"] >= 10 * r["cost"]["geometry_bytes_as_stored"] for r in conv),
        "companion_raw": next(({"triangles": r["triangles"],
                                "ratio_bc7": round(r["cost"]["texture_bc7_mip_bytes"] / r["cost"]["geometry_bytes_as_stored"], 2),
                                "ratio_bc1": round(r["cost"]["texture_bc1_mip_bytes"] / r["cost"]["geometry_bytes_as_stored"], 2)}
                               for r in load("conventions.json") if r["group"] == "companion_raw"), None),
        "disk_MiB_total_24": round(sum(r["file_bytes"] for r in conv) / mib, 1),
    }

    hyg_all = load("hygiene.json")
    hyg = [r for r in hyg_all if r["group"] in RAW_GROUPS]
    fail_any = [r for r in hyg if not (r["watertight"] and r["edge_manifold"] and r["single_component"])]
    rep["B2"] = {
        "n": len(hyg),
        "watertight": sum(r["watertight"] for r in hyg),
        "edge_manifold": sum(r["edge_manifold"] for r in hyg),
        "single_component": sum(r["single_component"] for r in hyg),
        "multi_component": [(r["id"], r["components"]) for r in hyg if not r["single_component"]],
        "fail_any": len(fail_any), "fail_any_wilson95": wilson(len(fail_any), len(hyg)),
        "H2_majority_fail": len(fail_any) > len(hyg) / 2,
        "self_intersecting_faces": span((r["self_intersecting_faces"] for r in hyg), 0),
        "with_self_intersections": sum(r["self_intersecting_faces"] > 0 for r in hyg),
        "degenerate_faces_total": sum(r["degenerate_faces"] for r in hyg),
        "duplicate_faces_total": sum(r["duplicate_faces"] for r in hyg),
        "genus": span((r["genus"] for r in hyg if r["genus"] is not None), 0),
        "uv_charts": span((r["uv_charts"] for r in hyg), 0),
        "uv_union_coverage": span(r["uv_union_coverage"] for r in hyg),
        "uv_overlap_ratio_max": round(max(r["uv_overlap_ratio"] for r in hyg), 4),
        "seam_split_factor": span(r["seam_split_factor"] for r in hyg),
        "others": {r["id"]: {k: r[k] for k in ("triangles", "components", "boundary_edges", "non_manifold_edges",
                                                "non_manifold_vertices", "self_intersecting_faces", "uv_charts",
                                                "uv_union_coverage", "seam_split_factor")}
                   for r in hyg_all if r["group"] not in RAW_GROUPS},
    }

    dec = load("decimation.jsonl")
    b4 = {}
    for cond in ("S", "W", "N"):
        for frac in (0.5, 0.25, 0.125, 0.0625):
            rows = [r for r in dec if r["cond"] == cond and r["target_frac"] == frac and r["id"] != "xuanji_raw"]
            if not rows:
                continue
            b4[f"{cond}@{frac}"] = {
                "n": len(rows), "reached": sum(r["reached"] for r in rows),
                "cracked": sum(r["boundary_edges_after_weld"] > 0 for r in rows),
                "boundary_edges": span((r["boundary_edges_after_weld"] for r in rows), 0),
                "components": span((r["components"] for r in rows), 0),
                "hausdorff_max_pct": span(r["hausdorff_max_pct"] for r in rows),
                "hausdorff_mean_pct": span(r["hausdorff_mean_pct"] for r in rows),
                "passes_max": max(r["passes"] for r in rows),
            }
    b4["xuanji_raw"] = [r for r in dec if r["id"] == "xuanji_raw"]
    w_last = [r for r in dec if r["cond"] == "W" and r["target_frac"] == 0.0625 and r["id"] != "xuanji_raw"]
    b4["H4_majority_cannot_reach_6.25pct_with_uv"] = (sum(not r["reached"] for r in w_last) > len(w_last) / 2) if w_last else None
    rep["B4"] = b4

    labels = load("history_labels.json")["labels"] if (RES / "history_labels.json").exists() else []
    if labels:
        countable = {"scale", "axis_rotation", "pivot", "double_sided", "bounds", "material_ext",
                     "texture_budget", "poly_budget", "topology"}
        asset = [l for l in labels if l["label"] == "ASSET"]
        rep["B5"] = {
            "matched": len(labels),
            "by_label": Counter(l["label"] for l in labels),
            "asset_fix": sum(l["is_fix"] for l in asset),
            "asset_feature": sum(not l["is_fix"] for l in asset),
            "asset_by_precheck": Counter(l["precheck"] for l in asset),
            "asset_fix_by_precheck": Counter(l["precheck"] for l in asset if l["is_fix"]),
            "engine_by_property": Counter(l["property"] for l in labels if l["label"] == "ENGINE"),
            "asset_fix_by_origin": Counter(l["origin"] for l in asset if l["is_fix"]),
            "asset_fix_countable_by_metadata": sum(l["precheck"] in countable for l in asset if l["is_fix"]),
            "H5_majority_countable": sum(l["precheck"] in countable for l in asset if l["is_fix"])
                                     > sum(l["is_fix"] for l in asset) / 2,
            "non_merge_commits_total": 484,
        }

    if (RES / "grounding.json").exists():
        rep["E1"] = load("grounding.json")

    (RES / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# Audit report (generated by scripts/report.py)", ""]
    for k, v in rep.items():
        md += [f"## {k}", "", "```json", json.dumps(v, indent=1, ensure_ascii=False), "```", ""]
    (RES / "report.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({k: v for k, v in rep.items() if k in ("B1", "B2", "B3")}, indent=1)[:6000])


if __name__ == "__main__":
    main()
