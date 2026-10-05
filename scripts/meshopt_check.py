"""B4 follow-up (after review): is the seam-split failure specific to MeshLab?

Runs meshoptimizer's simplifier (Python binding, meshopt_simplify) on the same
inputs: the seam-split buffer as stored in the GLB (S) and the position-welded
buffer (W). meshoptimizer collapses edges onto existing vertices and detects
seams by matching positions, so it is not expected to tear S; the question is
whether it reaches the target. target_error is set to 1.0 (no error limit) so
only the triangle target and the topology rules stop it.

Usage: python scripts/meshopt_check.py
"""
import json

import meshoptimizer as mo
import numpy as np

from conventions import HERE, resolve
from decimation import cracks
from glb import GLB
import pymeshlab

TARGETS = [0.125, 0.0625]


def run(pos, idx, frac):
    flat = idx.reshape(-1).astype(np.uint32)
    dest = np.zeros_like(flat)
    n = mo.simplify(dest, flat, pos.astype(np.float32), target_index_count=int(len(flat) * frac) // 3 * 3,
                    target_error=1.0)
    tri = dest[:n].reshape(-1, 3)
    m = pymeshlab.Mesh(vertex_matrix=pos.astype(np.float64), face_matrix=tri.astype(np.int32))
    bnd, comp = cracks(m)
    return len(tri), bnd, comp


def main():
    manifest = json.loads((HERE / "data" / "manifest.json").read_text(encoding="utf-8"))
    out = HERE / "results" / "meshopt_check.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for it in manifest:
            if it["group"] not in ("npc", "prop"):
                continue
            p = next(GLB(resolve(it)).primitives())
            pos, idx = p["pos"], p["idx"]
            uniq, inv = np.unique(pos.round(7), axis=0, return_inverse=True)
            widx = inv.reshape(-1)[idx]
            for frac in TARGETS:
                target = int(round(len(idx) * frac))
                for cond, (P, I) in (("S", (pos, idx)), ("W", (uniq, widx))):
                    tri, bnd, comp = run(P, I, frac)
                    row = {"id": it["id"], "cond": cond, "target_frac": frac, "target": target,
                           "triangles": tri, "reached": tri <= target * 1.02,
                           "boundary_edges_after_weld": bnd, "components": comp}
                    fh.write(json.dumps(row) + "\n")
                    print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
