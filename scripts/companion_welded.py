"""Figure 1 (bottom right): the companion simplified to the shipped triangle
count (82,829) from the WELDED input, for comparison with the shipped mesh.
The two OBJs are then rendered with scripts/crack_render_blender.py.

Usage: GAME_ROOT=... python scripts/companion_welded.py
"""
import pymeshlab

from conventions import HERE, RAW

SRC = RAW / "player" / "0cf1d3308afdc6f06885627043fc98c0.glb"
OUT = HERE / "results" / "cache" / "companion" / "xuanji_welded_82829.obj"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(str(SRC))
    ms.meshing_remove_duplicate_vertices()
    ms.meshing_decimation_quadric_edge_collapse_with_texture(targetfacenum=82829, qualitythr=0.3,
                                                             preserveboundary=False)
    ms.save_current_mesh(str(OUT), save_textures=False, save_wedge_texcoord=False)
    print(ms.current_mesh().face_number(), "->", OUT)


if __name__ == "__main__":
    main()
