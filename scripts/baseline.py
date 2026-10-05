"""Baseline: run the B2 hygiene/UV measurements on the game's non-generated
meshes (exported to OBJ by baseline_export_blender.py).

Usage: python scripts/baseline.py
"""
import json
from pathlib import Path

from hygiene import HERE, load_obj, measure

SRC = HERE / "results" / "cache" / "baseline"
GROUP = {"Astraea": "licensed character", "Mesh": "Temple of Nike pack", "New": "Altar Ruins pack", "Old": "Altar Ruins pack",
         "Meshes": "Altar Ruins pack"}


def group_of(name):
    folder = name.split("__")[0]
    if folder in GROUP:
        return GROUP[folder]
    return "CGM Egypt pack"


def main():
    rows = []
    for p in sorted(SRC.glob("*.obj")):
        try:
            pos, idx, uv = load_obj(p)
        except Exception as e:  # noqa: BLE001
            print("skip", p.name, e)
            continue
        if len(idx) < 50 or uv is None:
            continue
        r = {"id": p.stem, "group": group_of(p.stem), **measure(pos, idx, uv)}
        r["charts_per_1k_tris"] = round(1000 * r["uv_charts"] / r["triangles"], 2)
        rows.append(r)
        print(f'{r["group"]:<22} {r["id"][:40]:<40} tris={r["triangles"]:>7} charts={r["uv_charts"]:>5} '
              f'cov={r["uv_union_coverage"]:.2f} out={r["uv_out_of_unit_fraction"]:.2f} split={r["seam_split_factor"]:.2f} '
              f'wt={r["watertight"]} comp={r["components"]}', flush=True)
    (HERE / "results" / "baseline.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
