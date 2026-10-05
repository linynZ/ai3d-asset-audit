"""B4 simplification floor.

Three input representations of the same raw mesh, each simplified with
pymeshlab quadric edge collapse (quality threshold 0.3, boundary preservation
off) at 50 / 25 / 12.5 / 6.25 % of the original face count, up to 3 passes:

  S  seam-split vertices + per-vertex UV -- what loading the GLB straight into
     MeshLab gives you, and what the shipped companion pipeline did;
  W  welded vertices + per-corner (wedge) UV -- the textbook input for
     texture-aware QEM;
  N  welded vertices, no UV, plain QEM -- control.

Per run: faces reached, cracks (boundary edges after welding coincident
vertices; the input has none), components, and sampled Hausdorff distance to
the original in both directions, as % of the bounding-box diagonal.

Usage: python scripts/decimation.py [id ...]
"""
import json
import sys
import time

import numpy as np
import pymeshlab

from conventions import HERE, resolve

TARGETS = [0.5, 0.25, 0.125, 0.0625]
PASSES = 3
QUAL = 0.3


def welded(pos, idx):
    uniq, inv = np.unique(pos.round(7), axis=0, return_inverse=True)
    return uniq, inv.reshape(-1)[idx]


def build(cond, path):
    # MeshLab's glTF loader keeps the file's seam-split vertex buffer and stores UVs per corner,
    # i.e. exactly what the shipped companion pipeline fed to the simplifier (condition S).
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(str(path))
    if cond in ("W", "N"):
        ms.meshing_remove_duplicate_vertices()  # weld exact duplicates; per-corner UVs survive
    return ms


def simplify(ms, cond, target):
    for p in range(1, PASSES + 1):
        if cond == "N":
            ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target, qualitythr=QUAL,
                                                        preserveboundary=False, preservenormal=True)
        else:
            ms.meshing_decimation_quadric_edge_collapse_with_texture(targetfacenum=target, qualitythr=QUAL,
                                                                     preserveboundary=False)
        if ms.current_mesh().face_number() <= target * 1.02:
            return p
    return PASSES


def cracks(mesh):
    v, f = mesh.vertex_matrix(), mesh.face_matrix()
    wp, wi = welded(v, f)
    t = pymeshlab.MeshSet()
    t.add_mesh(pymeshlab.Mesh(vertex_matrix=wp, face_matrix=wi.astype(np.int32)))
    topo = t.get_topological_measures()
    return int(topo["boundary_edges"]), int(topo["connected_components_number"])


def hausdorff(ms, a, b, n):
    r = ms.get_hausdorff_distance(sampledmesh=a, targetmesh=b, samplenum=n, savesample=False)
    return r["max"], r["mean"], r["diag_mesh_0"]


def run(item):
    path = resolve(item)
    rows = []
    for cond in ("S", "W", "N"):
        for frac in TARGETS:
            ms = build(cond, path)
            f0 = ms.current_mesh().face_number()
            v0 = ms.current_mesh().vertex_number()
            target = int(round(f0 * frac))
            ms.generate_copy_of_current_mesh()  # id 1 = working copy, id 0 = original
            t0 = time.time()
            passes = simplify(ms, cond, target)
            dt = time.time() - t0
            dec = ms.current_mesh()
            bnd, comp = cracks(dec)
            n = 200000
            mx1, mn1, diag = hausdorff(ms, 1, 0, n)
            mx2, mn2, _ = hausdorff(ms, 0, 1, n)
            row = {"id": item["id"], "cond": cond, "input_vertices": v0, "input_faces": f0,
                   "target_frac": frac, "target": target,
                   "faces": dec.face_number(), "reached": dec.face_number() <= target * 1.02,
                   "passes": passes, "seconds": round(dt, 2),
                   "boundary_edges_after_weld": bnd, "components": comp,
                   "hausdorff_max_pct": round(100 * max(mx1, mx2) / diag, 4),
                   "hausdorff_mean_pct": round(100 * max(mn1, mn2) / diag, 4)}
            rows.append(row)
            print(json.dumps(row), flush=True)
    return rows


def main():
    manifest = json.loads((HERE / "data" / "manifest.json").read_text(encoding="utf-8"))
    want = set(sys.argv[1:])
    items = [it for it in manifest if it["group"] in ("npc", "prop", "companion_raw")
             and (not want or it["id"] in want)]
    out = HERE / "results" / "decimation.jsonl"
    done = set()
    if out.exists():
        done = {json.loads(l)["id"] for l in out.read_text(encoding="utf-8").splitlines() if l.strip()}
    with out.open("a", encoding="utf-8") as f:
        for it in items:
            if it["id"] in done:
                continue
            for r in run(it):
                f.write(json.dumps(r) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
