"""Facing probe, run inside Blender:

  blender -b --factory-startup -P scripts/facing_blender.py -- <out_dir> <glb> [<glb> ...]

Blender's glTF importer maps glTF +Y-up / +Z to Blender +Z-up / -Y, so a camera
on Blender's -Y axis looking toward +Y sees the side of the asset that faces
glTF +Z (the glTF "front"). For each GLB we render that view and the opposite
one (glTF -Z) with the base-colour texture, so a human can judge which side is
the face. Output: <out_dir>/<name>_pZ.png and <name>_nZ.png.
"""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
out_dir, paths = Path(args[0]), args[1:]
out_dir.mkdir(parents=True, exist_ok=True)

for path in paths:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "FLAT"
    scene.display.shading.color_type = "TEXTURE"
    scene.render.resolution_x = scene.render.resolution_y = 384
    scene.render.film_transparent = False
    meshes = [o for o in scene.objects if o.type == "MESH"]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centre, size = (lo + hi) / 2, max(hi - lo)
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = size * 1.15
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    name = Path(path).stem
    for tag, sign in (("pZ", -1), ("nZ", 1)):
        # pZ: camera at Blender -Y (sees glTF +Z side); nZ: camera at Blender +Y
        cam.location = centre + Vector((0, sign * size * 3, 0))
        cam.rotation_euler = (math.radians(90), 0, 0 if sign < 0 else math.radians(180))
        scene.render.filepath = str(out_dir / f"{name}_{tag}.png")
        bpy.ops.render.render(write_still=True)
    print(f"[facing] {name}", flush=True)
