"""B5 step 1: export the commits matched by the pre-registered pattern.

Writes data/history_commits.jsonl: hash, date, subject, body, files changed
(with +/- counts) and a diff excerpt (first 120 lines) for the labeller.

Usage: GAME_REPO=<path to game git repo> python scripts/history_export.py
"""
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = Path(os.environ.get("GAME_REPO") or r"C:\Users\linyu\CLionProjects\final project\final project")
TIP = "87fdd16"
PATTERN = ("ground|float|hover|sink|clip|feet|pivot|scale|yaw|facing|rotation|magenta|winding|cull|"
           "collider|bounds|hunyuan|glb|fbx|decimat|poly|npc model|boss model|xuanji 3d|companion 3d")


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def main():
    hashes = git("log", TIP, "--no-merges", "-i", "-E", f"--grep={PATTERN}", "--format=%H").split()
    total = len(git("log", TIP, "--no-merges", "--format=%H").split())
    out = HERE / "data" / "history_commits.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for h in reversed(hashes):
            meta = git("show", "-s", "--format=%ad%x00%s%x00%b", "--date=iso-strict", h).split("\x00")
            numstat = [l.split("\t") for l in git("show", "--numstat", "--format=", h).splitlines() if l.strip()]
            files = [{"path": p[2], "added": p[0], "deleted": p[1]} for p in numstat if len(p) == 3]
            code_files = [x["path"] for x in files if x["path"].endswith((".cs", ".py", ".shader", ".hlsl"))]
            diff = git("show", "--format=", "--unified=2", h, "--", *code_files[:6]).splitlines()[:120] if code_files else []
            f.write(json.dumps({"hash": h[:7], "date": meta[0], "subject": meta[1], "body": meta[2].strip()[:1500],
                                "files": files[:40], "n_files": len(files), "diff_excerpt": "\n".join(diff)},
                               ensure_ascii=False) + "\n")
    print(f"{len(hashes)} of {total} non-merge commits matched -> {out}")


if __name__ == "__main__":
    main()
