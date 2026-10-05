"""B2 geometry hygiene for every GLB in the manifest (plus the shipped companion OBJ).

Topology is measured after welding vertices with identical positions (seam
splits removed), because a UV seam is not a hole. UV charts are measured on the
unwelded mesh, where seams separate charts.

Usage: python scripts/hygiene.py <game-root>
"""
import json
import sys
from pathlib import Path

import numpy as np
import pymeshlab
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from conventions import CHAR, HERE, resolve
from glb import GLB

UV_RES = 2048


def weld(pos, idx):
    uniq, inv = np.unique(pos.round(7), axis=0, return_inverse=True)
    return uniq, inv.reshape(-1)[idx]


def face_components(n_vert, idx):
    rows = np.repeat(np.arange(len(idx)), 3)
    cols = idx.reshape(-1)
    inc = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(idx), n_vert)).tocsr()
    adj = inc @ inc.T
    n, _ = connected_components(adj, directed=False)
    return int(n)


def uv_coverage(uv, idx):
    tri = uv[idx]  # (F,3,2)
    a = 0.5 * np.abs((tri[:, 1, 0] - tri[:, 0, 0]) * (tri[:, 2, 1] - tri[:, 0, 1])
                     - (tri[:, 2, 0] - tri[:, 0, 0]) * (tri[:, 1, 1] - tri[:, 0, 1]))
    out_of_unit = float(np.mean((tri < 0) | (tri > 1)))
    img = Image.new("1", (UV_RES, UV_RES), 0)
    d = ImageDraw.Draw(img)
    for t in tri:
        d.polygon([(float(x * UV_RES), float((1 - y) * UV_RES)) for x, y in t], fill=1)
    union = np.asarray(img, dtype=bool).mean()
    return {"uv_area_sum": float(a.sum()), "uv_union_coverage": float(union),
            "uv_overlap_ratio": float(max(0.0, a.sum() - union) / a.sum()) if a.sum() else None,
            "uv_out_of_unit_fraction": out_of_unit}


def measure(pos, idx, uv):
    face_area = 0.5 * np.linalg.norm(np.cross(pos[idx[:, 1]] - pos[idx[:, 0]], pos[idx[:, 2]] - pos[idx[:, 0]]), axis=1)
    diag = float(np.linalg.norm(pos.max(0) - pos.min(0)))
    wpos, widx = weld(pos, idx)
    sorted_f = np.sort(widx, axis=1)
    _, counts = np.unique(sorted_f, axis=0, return_counts=True)

    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(vertex_matrix=wpos, face_matrix=widx.astype(np.int32)))
    topo = ms.get_topological_measures()
    ms.compute_selection_by_self_intersections_per_face()
    selfint = ms.current_mesh().selected_face_number()

    out = {
        "raw_vertices": int(len(pos)), "welded_vertices": int(len(wpos)), "triangles": int(len(idx)),
        "seam_split_factor": round(len(pos) / len(wpos), 4),
        "degenerate_faces": int(np.sum(face_area <= 1e-12 * diag * diag)),
        "faces_sharing_welded_vertex_twice": int(np.sum((sorted_f[:, 0] == sorted_f[:, 1]) | (sorted_f[:, 1] == sorted_f[:, 2]))),
        "duplicate_faces": int(np.sum(counts[counts > 1] - 1)),
        "self_intersecting_faces": int(selfint),
        "components": face_components(len(wpos), widx),
        "boundary_edges": int(topo["boundary_edges"]),
        "non_manifold_edges": int(topo["non_two_manifold_edges"]),
        "non_manifold_vertices": int(topo["non_two_manifold_vertices"]),
        "holes": int(topo["number_holes"]) if topo["number_holes"] >= 0 else None,
        "genus": int(topo["genus"]) if topo["genus"] >= 0 else None,
        "uv_charts": face_components(len(pos), idx) if uv is not None else None,
    }
    if uv is not None:
        out.update(uv_coverage(uv, idx))
    out["watertight"] = out["boundary_edges"] == 0
    out["edge_manifold"] = out["non_manifold_edges"] == 0
    out["single_component"] = out["components"] == 1
    return out


def load_obj(path):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(str(path))
    m = ms.current_mesh()
    pos = m.vertex_matrix()
    idx = m.face_matrix().astype(np.int64)
    uv = None
    if m.has_wedge_tex_coord():
        # OBJ carries per-corner UVs; split vertices per (position, uv) like a GPU buffer would
        corner_uv = m.wedge_tex_coord_matrix()  # (3F, 2)
        corner_pos = pos[idx].reshape(-1, 3)
        key = np.c_[corner_pos.round(7), corner_uv.round(7)]
        uk, inv = np.unique(key, axis=0, return_inverse=True)
        pos, uv, idx = uk[:, :3], uk[:, 3:], inv.reshape(-1, 3)
    return pos, idx, uv


def main():
    manifest = json.loads((HERE / "data" / "manifest.json").read_text(encoding="utf-8"))
    rows = []
    for it in manifest:
        if it["group"] == "boss_studio":
            continue  # FBX: measured in Blender (grounding.py), one mesh shared by four files
        if it["group"] == "companion_decimated":
            pos, idx, uv = load_obj(CHAR / it["path"])
        else:
            g = GLB(resolve(it))
            p = next(g.primitives())
            pos, idx, uv = p["pos"], p["idx"], p["uv"]
        r = {"id": it["id"], "group": it["group"], **measure(pos, idx, uv)}
        rows.append(r)
        print(f'{r["id"]:<28} comp={r["components"]:>4} bnd={r["boundary_edges"]:>5} nme={r["non_manifold_edges"]:>4} '
              f'nmv={r["non_manifold_vertices"]:>4} deg={r["degenerate_faces"]:>3} self={r["self_intersecting_faces"]:>5} '
              f'charts={r["uv_charts"]} cov={r.get("uv_union_coverage", 0):.3f} ovl={r.get("uv_overlap_ratio") or 0:.3f}', flush=True)
    (HERE / "results" / "hygiene.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
