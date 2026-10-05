"""B1 conventions + B3 cost estimates for every GLB in the manifest.

Usage: GAME_ROOT=<folder holding ChronoTraveler/ and asset model/> python scripts/conventions.py
"""
import json
import os
from pathlib import Path

import numpy as np

from glb import GLB

HERE = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get("GAME_ROOT") or r"C:\Users\linyu\CLionProjects\final project")
CHAR = ROOT / "final project" / "ChronoTraveler" / "Assets" / "Art" / "Characters"
RAW = ROOT / "asset model" / "AI model"

MIP = 4 / 3
FORMATS = {"rgba8": 4.0, "bc7": 1.0, "bc1": 0.5}  # bytes per pixel


def resolve(item):
    if item["group"] == "companion_raw":
        return RAW / item["raw_original"]
    return CHAR / item["path"]


def audit(item):
    g = GLB(resolve(item))
    prims = list(g.primitives())
    wpos = np.vstack([p["wpos"] for p in prims])
    lo, hi = wpos.min(0), wpos.max(0)
    ext = hi - lo
    # pivot = the asset's local origin, expressed as a fraction of the box on each axis
    pivot_frac = ((0 - lo) / np.where(ext > 0, ext, 1)).round(4)

    nodes = g.json.get("nodes", [])
    non_identity = []
    for p in prims:
        for ni in p["chain"]:
            n = nodes[ni]
            if any(k in n for k in ("rotation", "scale", "translation", "matrix")):
                non_identity.append({"node": ni, "name": n.get("name"),
                                     **{k: n[k] for k in ("rotation", "scale", "translation", "matrix") if k in n}})
    # up axis after the node chain: which world axis the mesh's local +Z/+Y maps to is not needed;
    # what matters for import is the world-space extent per axis.
    mats = g.json.get("materials", [])
    images = g.image_info()
    tex_px = sum((im["width"] or 0) * (im["height"] or 0) for im in images)

    geo_bytes = 0
    verts = tris = 0
    attr_names = set()
    for p in prims:
        verts += len(p["pos"])
        tris += len(p["idx"])
        for name, acc in p["attrs"].items():
            geo_bytes += g.accessor_bytes(acc)
            attr_names.add(name)
        if p["indices_acc"] is not None:
            geo_bytes += g.accessor_bytes(p["indices_acc"])

    return {
        "id": item["id"], "group": item["group"],
        "file_bytes": g.total_bytes,
        "primitives": len(prims), "materials": len(mats),
        "vertices": int(verts), "triangles": int(tris),
        "attributes": sorted(attr_names),
        "bbox_min": lo.round(5).tolist(), "bbox_max": hi.round(5).tolist(),
        "extent_xyz": ext.round(5).tolist(),
        "largest_extent": float(ext.max().round(5)),
        "height_y": float(ext[1].round(5)),
        "pivot_frac_xyz": pivot_frac.tolist(),
        "node_transforms": non_identity,
        "double_sided": [bool(m.get("doubleSided", False)) for m in mats],
        "alpha_mode": [m.get("alphaMode", "OPAQUE") for m in mats],
        "material_extensions": sorted({e for m in mats for e in m.get("extensions", {})}),
        "extensions_used": g.json.get("extensionsUsed", []),
        "generator": g.json.get("asset", {}).get("generator"),
        "skins": len(g.json.get("skins", [])), "animations": len(g.json.get("animations", [])),
        "images": images,
        "cost": {
            "geometry_bytes_as_stored": int(geo_bytes),
            "texture_container_bytes": int(sum(im["bytes"] for im in images)),
            **{f"texture_{k}_mip_bytes": int(tex_px * bpp * MIP) for k, bpp in FORMATS.items()},
        },
    }


def main():
    manifest = json.loads((HERE / "data" / "manifest.json").read_text(encoding="utf-8"))
    rows = [audit(it) for it in manifest if it["path"].lower().endswith(".glb") or it["group"] == "companion_raw"]
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "conventions.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    for r in rows:
        c = r["cost"]
        print(f'{r["id"]:<28} tris={r["triangles"]:>7} h={r["height_y"]:.3f} L={r["largest_extent"]:.3f} '
              f'piv={r["pivot_frac_xyz"]} ds={r["double_sided"]} rot={len(r["node_transforms"])} '
              f'tex/geo(bc7)={c["texture_bc7_mip_bytes"] / c["geometry_bytes_as_stored"]:.1f}')


if __name__ == "__main__":
    main()
