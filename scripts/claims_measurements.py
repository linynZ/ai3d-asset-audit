"""The two new measurements PLAN_v2 allows for judging claims.

(i)  Origin height after the game's import: UniGLTF's default reverses Z
     (x, y, z) -> (x, y, -z) after the glTF node chain; we report where the
     asset's origin sits relative to its bounding box in Unity coordinates.
(ii) Does the GLB's root rotation node survive a loader that ignores the scene
     graph? MeshLab's glTF import returns vertex positions; we compare its up
     axis with the GLB's world up axis (after the node chain), and check what an
     OBJ written by MeshLab contains.

Usage: python scripts/claims_measurements.py
"""
import json

import numpy as np
import pymeshlab

from conventions import HERE, resolve
from glb import GLB


def main():
    manifest = json.loads((HERE / "data" / "manifest.json").read_text(encoding="utf-8"))
    out = {"origin_after_unigltf": [], "meshlab_root_rotation": []}
    for it in manifest:
        if it["group"] not in ("npc", "prop", "companion_raw"):
            continue
        g = GLB(resolve(it))
        p = next(g.primitives())
        w = p["wpos"] * np.array([1.0, 1.0, -1.0])  # UniGLTF default: reverse Z
        lo, hi = w.min(0), w.max(0)
        frac = (0 - lo) / (hi - lo)
        out["origin_after_unigltf"].append({"id": it["id"], "origin_frac_xyz": frac.round(4).tolist(),
                                            "origin_at_base": bool(abs(frac[1]) < 1e-3)})
        if it["group"] == "companion_raw" or it["id"] == "npc_china_artisan":
            ms = pymeshlab.MeshSet()
            ms.load_new_mesh(str(resolve(it)))
            v = ms.current_mesh().vertex_matrix()
            ext_ml = v.max(0) - v.min(0)
            ext_w = p["wpos"].max(0) - p["wpos"].min(0)
            out["meshlab_root_rotation"].append({
                "id": it["id"],
                "glb_world_extent_xyz": ext_w.round(4).tolist(),
                "meshlab_extent_xyz": ext_ml.round(4).tolist(),
                "meshlab_tallest_axis": "xyz"[int(np.argmax(ext_ml))],
                "glb_world_tallest_axis": "xyz"[int(np.argmax(ext_w))],
                "meshlab_equals_untransformed_positions": bool(np.allclose(v[:100], p["pos"][:100], atol=1e-6)),
            })
    s = out["origin_after_unigltf"]
    out["summary"] = {"n": len(s), "origin_at_base": sum(r["origin_at_base"] for r in s)}
    (HERE / "results" / "claims_measurements.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out["summary"]), json.dumps(out["meshlab_root_rotation"], indent=1))


if __name__ == "__main__":
    main()
