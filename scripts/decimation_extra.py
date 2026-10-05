"""B4 follow-ups requested in review (added after the plan; reported as such).

1. S_pb  seam-split input with preserveboundary=True: separates "input
         representation" from "boundaries not protected".
2. N_nn  welded, no UV, preservenormal=False: same flag set as S/W, so the
         no-UV control differs from W only in the UV term.
3. Appearance error for S and W: sample points on the simplified surface, look
   up base colour through the simplified UVs, compare with the colour at the
   nearest original vertex looked up through the original UVs. The same
   procedure on the unsimplified mesh gives the noise floor. Reported as RGB
   RMSE (0-255) and the share of samples off by more than 32 levels.

Targets 12.5 % and 6.25 %. Usage: python scripts/decimation_extra.py
"""
import io
import json

import numpy as np
import pymeshlab
from PIL import Image
from scipy.spatial import cKDTree

from conventions import HERE, resolve
from decimation import QUAL, cracks
from glb import GLB

TARGETS = [0.125, 0.0625]
N_SAMPLES = 60000
rng = np.random.default_rng(0)


def base_colour(path):
    g = GLB(path)
    mat = g.json["materials"][0]
    tex_i = mat["pbrMetallicRoughness"]["baseColorTexture"]["index"]
    img_i = g.json["textures"][tex_i]["source"]
    bv = g.json["bufferViews"][g.json["images"][img_i]["bufferView"]]
    blob = g.bin[bv.get("byteOffset", 0): bv.get("byteOffset", 0) + bv["byteLength"]]
    im = Image.open(io.BytesIO(blob)).convert("RGB").resize((1024, 1024), Image.BILINEAR)
    return np.asarray(im, dtype=np.float32)


def lookup(tex, uv):
    h, w, _ = tex.shape
    x = np.clip((uv[:, 0] % 1.0) * (w - 1), 0, w - 1).astype(int)
    y = np.clip((uv[:, 1] % 1.0) * (h - 1), 0, h - 1).astype(int)  # glTF: v=0 is the top row
    return tex[y, x]


def surface_samples(v, f, wuv, n):
    tri = v[f]
    area = 0.5 * np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1)
    pick = rng.choice(len(f), size=n, p=area / area.sum())
    r1, r2 = rng.random(n), rng.random(n)
    s = np.sqrt(r1)
    b = np.c_[1 - s, s * (1 - r2), s * r2]
    p = np.einsum("ij,ijk->ik", b, tri[pick])
    uv = np.einsum("ij,ijk->ik", b, wuv.reshape(-1, 3, 2)[pick])
    return p, uv


def appearance_error(mesh, ref_tree, ref_uv, tex):
    v, f = mesh.vertex_matrix(), mesh.face_matrix()
    wuv = mesh.wedge_tex_coord_matrix().copy()
    wuv[:, 1] = 1.0 - wuv[:, 1]  # MeshLab stores V flipped (OpenGL convention); back to glTF
    p, uv = surface_samples(v, f, wuv, N_SAMPLES)
    _, nn = ref_tree.query(p)
    d = lookup(tex, uv) - lookup(tex, ref_uv[nn])
    err = np.sqrt((d ** 2).mean(axis=1))
    return round(float(np.sqrt((d ** 2).mean())), 2), round(float((err > 32).mean()), 4)


def main():
    manifest = json.loads((HERE / "data" / "manifest.json").read_text(encoding="utf-8"))
    items = [it for it in manifest if it["group"] in ("npc", "prop")]
    out = HERE / "results" / "decimation_extra.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for it in items:
            path = resolve(it)
            g = GLB(path)
            p = next(g.primitives())
            ref_tree, ref_uv = cKDTree(p["pos"]), p["uv"]
            tex = base_colour(path)
            ms0 = pymeshlab.MeshSet()
            ms0.load_new_mesh(str(path))
            floor = appearance_error(ms0.current_mesh(), ref_tree, ref_uv, tex)
            f0 = ms0.current_mesh().face_number()
            for frac in TARGETS:
                target = int(round(f0 * frac))
                for cond in ("S", "S_pb", "W", "N_nn"):
                    ms = pymeshlab.MeshSet()
                    ms.load_new_mesh(str(path))
                    if cond in ("W", "N_nn"):
                        ms.meshing_remove_duplicate_vertices()
                    for _ in range(3):
                        if cond == "N_nn":
                            ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target, qualitythr=QUAL,
                                                                        preserveboundary=False, preservenormal=False)
                        else:
                            ms.meshing_decimation_quadric_edge_collapse_with_texture(
                                targetfacenum=target, qualitythr=QUAL, preserveboundary=(cond == "S_pb"))
                        if ms.current_mesh().face_number() <= target * 1.02:
                            break
                    m = ms.current_mesh()
                    bnd, comp = cracks(m)
                    row = {"id": it["id"], "cond": cond, "target_frac": frac, "target": target,
                           "faces": m.face_number(), "reached": m.face_number() <= target * 1.02,
                           "boundary_edges_after_weld": bnd, "components": comp}
                    if cond in ("S", "S_pb", "W"):
                        rmse, bad = appearance_error(m, ref_tree, ref_uv, tex)
                        row.update({"rgb_rmse": rmse, "share_off_gt32": bad,
                                    "noise_floor_rmse": floor[0], "noise_floor_share": floor[1]})
                    fh.write(json.dumps(row) + "\n")
                    fh.flush()
                    print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
