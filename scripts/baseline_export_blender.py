"""Baseline: export the game's non-generated meshes (licensed character, purchased
packs) to triangulated OBJ with UVs, one OBJ per source file, so the same
hygiene script can measure them.

  blender -b --factory-startup -P scripts/baseline_export_blender.py -- <out_dir> <fbx|obj> ...
"""
import sys
from pathlib import Path

import bpy

args = sys.argv[sys.argv.index("--") + 1:]
out_dir, paths = Path(args[0]), args[1:]
out_dir.mkdir(parents=True, exist_ok=True)

for path in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ext = Path(path).suffix.lower()
    try:
        if ext == ".fbx":
            bpy.ops.import_scene.fbx(filepath=path)
        elif ext == ".obj":
            bpy.ops.wm.obj_import(filepath=path)
        else:
            continue
    except Exception as e:  # noqa: BLE001
        print(f"[baseline] FAIL {path}: {e}", flush=True)
        continue
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        continue
    for o in bpy.context.scene.objects:
        o.select_set(o.type == "MESH")
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    name = Path(path).parent.name + "__" + Path(path).stem
    bpy.ops.wm.obj_export(filepath=str(out_dir / f"{name}.obj"), export_selected_objects=True,
                          export_triangulated_mesh=True, export_uv=True, export_normals=False,
                          export_materials=False, apply_modifiers=True)
    print(f"[baseline] {name}", flush=True)
