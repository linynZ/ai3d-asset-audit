"""Build the corpus manifest: every audited file with size and SHA-256.

The meshes themselves are not redistributed (about 1 GB, and the game repo is
private). Anyone holding the files can check them against data/manifest.json.

Usage: python scripts/manifest.py <game-root>
  <game-root> = the folder that contains ChronoTraveler/ and asset model/
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\Users\linyu\CLionProjects\final project")
GAME = ROOT / "final project" / "ChronoTraveler" / "Assets" / "Art" / "Characters"
RAW = ROOT / "asset model" / "AI model"
OUT = Path(__file__).resolve().parent.parent / "data" / "manifest.json"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    raw = {}
    for p in sorted(RAW.rglob("*")):
        if p.suffix.lower() in {".glb", ".fbx", ".obj"}:
            raw[sha256(p)] = p.relative_to(RAW).as_posix()

    items = []
    for p in sorted(GAME.rglob("*")):
        if p.suffix.lower() not in {".glb", ".fbx", ".obj"}:
            continue
        digest = sha256(p)
        rel = p.relative_to(GAME).as_posix()
        if rel.startswith("Finale/"):
            group = "boss_studio"
        elif rel.startswith("Companion/"):
            group = "companion_decimated"
        elif Path(rel).name.startswith("prop_"):
            group = "prop"
        else:
            group = "npc"
        items.append({
            "id": Path(rel).stem,
            "path": rel,
            "group": group,
            "bytes": p.stat().st_size,
            "sha256": digest,
            "raw_original": raw.get(digest),
        })

    # The companion's raw 497,850-face original is audited too (pre-decimation).
    for digest, rel in raw.items():
        if rel.startswith("player/"):
            p = RAW / rel
            items.append({
                "id": "xuanji_raw",
                "path": "asset model/AI model/" + rel,
                "group": "companion_raw",
                "bytes": p.stat().st_size,
                "sha256": digest,
                "raw_original": rel,
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    groups = {}
    for it in items:
        groups[it["group"]] = groups.get(it["group"], 0) + 1
    print(f"{len(items)} files -> {OUT}")
    print(groups)
    print("byte-identical to a raw download:", sum(1 for it in items if it["raw_original"]))


if __name__ == "__main__":
    main()
