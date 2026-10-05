"""Read the shipped Windows build and list every Texture2D that belongs to a
generated asset (names from the GLB images: texture_pbr_20250901*), with its
stored size, format, mip count and serialized byte size.

Usage: python scripts/build_textures.py <path to *_Data folder>
"""
import json
import sys
from collections import Counter
from pathlib import Path

import UnityPy

HERE = Path(__file__).resolve().parent.parent
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"D:\ChronoTraveler\ChronoTraveler_Data")


def main():
    env = UnityPy.load(str(DATA))
    rows = []
    for obj in env.objects:
        if obj.type.name != "Texture2D":
            continue
        t = obj.read()
        name = getattr(t, "m_Name", "") or getattr(t, "name", "")
        size = getattr(t, "m_CompleteImageSize", None) or getattr(t, "image_data_size", None)
        stream = getattr(t, "m_StreamData", None)
        rows.append({
            "name": name, "file": obj.assets_file.name, "path_id": obj.path_id,
            "width": t.m_Width, "height": t.m_Height,
            "format": str(t.m_TextureFormat).split(".")[-1],
            "mips": getattr(t, "m_MipCount", None),
            "readable": bool(getattr(t, "m_IsReadable", False)),
            "bytes": int(size) if size else None,
            "stream_size": int(getattr(stream, "size", 0) or 0) if stream else 0,
        })
    gen = [r for r in rows if r["name"].startswith("texture_pbr_20250901")]
    size_of = lambda r: r["stream_size"] or r["bytes"] or 0
    glb_maps = [r for r in gen if r["width"] == 4096]  # the 24 GLB assets' base maps (the boss's are 2048)
    mib = 2 ** 20
    out = {"all_textures": len(rows), "generated_textures": gen, "textures": rows,
           "texture_totals_MiB": {
               "all": round(sum(size_of(r) for r in rows) / mib, 1),
               "generated_all": round(sum(size_of(r) for r in gen) / mib, 1),
               "glb_base_maps_n": len(glb_maps),
               "glb_base_maps": round(sum(size_of(r) for r in glb_maps) / mib, 1),
               "glb_base_maps_readable": sum(r["readable"] for r in glb_maps),
               "glb_base_maps_share_pct": round(100 * sum(size_of(r) for r in glb_maps) / sum(size_of(r) for r in rows), 1),
               "largest_other": max(((r["name"], r["format"], round(size_of(r) / mib, 1)) for r in rows
                                     if not r["name"].startswith("texture_pbr_20250901")), key=lambda x: x[2]),
           },
           "generated_by_format_size": Counter(f'{r["format"]} {r["width"]}x{r["height"]} mips={r["mips"]} readable={r["readable"]}' for r in gen),
           "top_by_bytes": sorted(rows, key=lambda r: -(r["stream_size"] or r["bytes"] or 0))[:25]}
    (HERE / "results" / "build_textures.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(len(rows), "textures;", len(gen), "generated")
    for k, v in out["generated_by_format_size"].items():
        print(v, k)
    mib = 2 ** 20
    print("generated total MiB:", round(sum((r["stream_size"] or r["bytes"] or 0) for r in gen) / mib, 1))
    for r in out["top_by_bytes"][:12]:
        print(r["name"], r["format"], r["width"], r["height"], round((r["stream_size"] or r["bytes"] or 0) / mib, 1))


if __name__ == "__main__":
    main()
