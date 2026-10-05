"""E1 grounding ground truth, run inside Blender:

  blender -b --factory-startup -P scripts/grounding_blender.py -- <fbx> [<fbx> ...] <out.json>

For each FBX: import, then for every frame of its action evaluate the skinned
mesh and record the lowest world-space vertex (Blender is Z-up). Also records
the bind (rest) pose lowest vertex, mesh statistics and the action's frame rate.
"""
import json
import sys

import bpy
import numpy as np

args = sys.argv[sys.argv.index("--") + 1:]
paths, out_path = args[:-1], args[-1]


def lowest_z(obj, depsgraph):
    ev = obj.evaluated_get(depsgraph)
    me = ev.to_mesh()
    co = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    mw = np.array(ev.matrix_world)
    w = co @ mw[:3, :3].T + mw[:3, 3]
    z = w[:, 2]
    res = (float(z.min()), float(z.max()))
    ev.to_mesh_clear()
    return res, len(me.vertices) if False else None


results = []
for path in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    scene = bpy.context.scene
    meshes = [o for o in scene.objects if o.type == "MESH"]
    arms = [o for o in scene.objects if o.type == "ARMATURE"]
    mesh = max(meshes, key=lambda o: len(o.data.vertices))
    arm = arms[0] if arms else None
    action = arm.animation_data.action if arm and arm.animation_data else None
    f0, f1 = (int(action.frame_range[0]), int(action.frame_range[1])) if action else (scene.frame_start, scene.frame_end)
    fps = scene.render.fps / scene.render.fps_base

    dg = bpy.context.evaluated_depsgraph_get()
    if arm:
        arm.data.pose_position = "REST"
        dg.update()
        (rest_min, rest_max), _ = lowest_z(mesh, bpy.context.evaluated_depsgraph_get())
        arm.data.pose_position = "POSE"
    else:
        rest_min = rest_max = None

    frames = []
    for f in range(f0, f1 + 1):
        scene.frame_set(f)
        (zmin, zmax), _ = lowest_z(mesh, bpy.context.evaluated_depsgraph_get())
        frames.append({"frame": f, "zmin": zmin, "zmax": zmax})

    tri = sum(len(p.vertices) - 2 for p in mesh.data.polygons)
    results.append({
        "file": path.replace("\\", "/").split("/")[-1],
        "fps": fps, "frame_start": f0, "frame_end": f1,
        "vertices": len(mesh.data.vertices), "triangles": tri,
        "bones": len(arm.data.bones) if arm else 0,
        "rest_zmin": rest_min, "rest_zmax": rest_max,
        "frames": frames,
    })
    print(f"[grounding] {path}: {f1 - f0 + 1} frames @ {fps} fps, rest zmin {rest_min}", flush=True)

with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1)
