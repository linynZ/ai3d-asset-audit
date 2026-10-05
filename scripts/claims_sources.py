"""C step 1: freeze the source texts the claim extractors read (PLAN_v2.md).

Writes data/claim_sources/: commits.jsonl (hash, date, subject, full body, files),
code_comments.jsonl (file, line, comment text at 87fdd16) and docs/ (copies of the
listed design notes).

Usage: GAME_REPO=... python scripts/claims_sources.py
"""
import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REPO = Path(os.environ.get("GAME_REPO") or r"C:\Users\linyu\CLionProjects\final project\final project")
TIP = "87fdd16"
OUT = HERE / "data" / "claim_sources"
PATTERN = ("ground|float|hover|sink|clip|feet|pivot|scale|yaw|facing|rotation|magenta|winding|cull|"
           "collider|bounds|hunyuan|glb|fbx|decimat|poly|npc model|boss model|xuanji 3d|companion 3d")
PATHS = ["ChronoTraveler/Assets/Art/Characters", "ChronoTraveler/Assets/Resources/CharacterModels",
         "ChronoTraveler/Assets/Editor/NPCModelSetupTool.cs", "ChronoTraveler/Assets/Editor/FinaleBossModelTool.cs",
         "ChronoTraveler/Assets/Editor/XuanjiModelTool.cs", "ChronoTraveler/Assets/Scripts/World/GroundSnap.cs",
         "ChronoTraveler/Assets/Scripts/World/FinaleEmbodiment.cs",
         "ChronoTraveler/Assets/Scripts/Companion/CompanionController.cs",
         "ChronoTraveler/Assets/Scripts/NPC/NPCController.cs", "ChronoTraveler/Assets/Scripts/World/ModelSwapper.cs",
         "tools/decimate_xuanji.py"]
CODE = [p for p in PATHS if p.endswith((".cs", ".py"))]
DOCS = ["docs/superpowers/specs/2026-07-15-xuanji-3d-companion-design.md",
        "docs/superpowers/specs/2026-07-09-finale-battle-design.md",
        "docs/superpowers/specs/2026-06-28-slice-B-xuanji-companion-design.md",
        "docs/pipelines/npc_fullbody_prompts.md", "docs/pipelines/finale_boss_model_prompt.md"]


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    matched = set(git("log", TIP, "--no-merges", "-i", "-E", f"--grep={PATTERN}", "--format=%H").split())
    touched = set(git("log", TIP, "--no-merges", "--format=%H", "--", *PATHS).split())
    hashes = [h for h in git("log", TIP, "--no-merges", "--reverse", "--format=%H").split() if h in matched | touched]
    with (OUT / "commits.jsonl").open("w", encoding="utf-8") as f:
        for h in hashes:
            date, subject, body = git("show", "-s", "--format=%ad%x00%s%x00%b", "--date=iso-strict", h).split("\x00")
            files = git("show", "--name-only", "--format=", h).split()
            f.write(json.dumps({"hash": h[:7], "date": date, "subject": subject, "body": body.strip(),
                                "files": files, "in_b5": h in matched, "touches_asset_paths": h in touched},
                               ensure_ascii=False) + "\n")
    with (OUT / "code_comments.jsonl").open("w", encoding="utf-8") as f:
        for path in CODE:
            text = git("show", f"{TIP}:{path}")
            for i, line in enumerate(text.splitlines(), 1):
                m = re.search(r"(//+|#)\s?(.*)$", line)
                if m and m.group(2).strip():
                    f.write(json.dumps({"file": path, "line": i, "comment": m.group(2).strip()},
                                       ensure_ascii=False) + "\n")
    (OUT / "docs").mkdir(exist_ok=True)
    for d in DOCS:
        (OUT / "docs" / Path(d).name).write_text(git("show", f"{TIP}:{d}"), encoding="utf-8")
    print(len(hashes), "commits;", sum(1 for _ in (OUT / "code_comments.jsonl").open(encoding="utf-8")),
          "comment lines;", len(DOCS), "docs")


if __name__ == "__main__":
    main()
