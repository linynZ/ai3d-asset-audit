"""Render the shipped (seam-split simplified) companion next to a welded
simplification at the same face count, flat grey on a bright background so
cracks show as background-coloured lines.

  blender -b --factory-startup -P scripts/crack_render_blender.py -- <out_png_prefix> <obj> [<obj> ...]
"""
import math
import sys

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
prefix, paths = args[0], args[1:]

for i, path in enumerate(paths):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=path)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    sh = scene.display.shading
    sh.light, sh.color_type, sh.single_color = "STUDIO", "SINGLE", (0.62, 0.62, 0.64)
    sh.show_backface_culling = True
    scene.world = bpy.data.worlds.new("w")
    scene.world.color = (1.0, 0.55, 0.15)
    scene.display.shading.background_type = "WORLD"
    scene.render.resolution_x, scene.render.resolution_y = 900, 900
    meshes = [o for o in scene.objects if o.type == "MESH"]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centre, size = (lo + hi) / 2, max(hi - lo)
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = size * 0.55  # close-up on the upper body
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.location = centre + Vector((size * 0.12, -size * 3, size * 0.12))
    cam.rotation_euler = (math.radians(90), 0, 0)
    scene.render.filepath = f"{prefix}_{i}.png"
    bpy.ops.render.render(write_still=True)
