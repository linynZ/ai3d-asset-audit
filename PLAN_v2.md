# Addendum to the audit plan — written before any claim is extracted or judged

**Date:** 2026-10-05 (after the author signed off the B5 labels and the repository went public)
**Status of the main audit:** B1–B5 and E1 are complete and reported in the paper (commit 9b710c2 and later).
This addendum adds two analyses that use data only this project has: the AI coding assistant's own
contemporaneous statements about the generated assets, and the full development history, set against
the independent measurements of the main audit.

## Why

The game was built with an AI coding assistant. 410 of the 484 non-merge commits up to the final build
(87fdd16) carry a Claude co-author trailer; their messages, the comments in the asset tools and the
design notes were drafted by the assistant and accepted by the developer. These texts contain causal
explanations ("Hunyuan front-view exports face -Z", "UV seam islands are the hard floor"). The main audit
measured several of the same properties independently. No other study we know of can set an assistant's
explanations of generated-asset problems against measured ground truth from the same project.

Known limitation, stated now: the interactive session transcripts of the development period
(June–August 2026) no longer exist; the earliest surviving transcript is from 2026-09-07. All evidence
for C and D comes from git (messages, diffs, timestamps), source comments and design documents at the
final build. Effort is therefore measured in commits and elapsed time, not in conversation turns.

## C — Attribution audit (assistant claims vs measured ground truth)

**Sources (fixed now):**
1. Subject and body of every non-merge commit up to 87fdd16 that either matched the B5 pattern (156) or
   touched a generated-asset path or asset tool (54): `Assets/Art/Characters`, `Resources/CharacterModels`,
   `Editor/NPCModelSetupTool.cs`, `Editor/FinaleBossModelTool.cs`, `Editor/XuanjiModelTool.cs`,
   `World/GroundSnap.cs`, `World/FinaleEmbodiment.cs`, `Companion/CompanionController.cs`,
   `NPC/NPCController.cs`, `World/ModelSwapper.cs`, `tools/decimate_xuanji.py`.
2. Comments in those source files at 87fdd16.
3. Design notes: `docs/superpowers/specs/2026-07-15-xuanji-3d-companion-design.md`,
   `2026-07-09-finale-battle-design.md`, `2026-06-28-slice-B-xuanji-companion-design.md`,
   `docs/pipelines/npc_fullbody_prompts.md`, `docs/pipelines/finale_boss_model_prompt.md`.

**Unit.** A *claim* is a declarative statement, in these sources, about (a) a property of a generated
asset, (b) what the import or processing pipeline does to it, or (c) the cause of an observed
asset problem. Plans, intentions, instructions to the user and UI text are not claims. Repeated
statements of the same content are one claim, dated at first appearance.

**Extraction.** Two extractors (separate AI agents, no access to each other's output or to the verdicts)
extract claims from the same sources with a fixed instruction. Their lists are merged by the assistant;
a claim found by only one extractor is kept and marked. Recorded per claim: id, verbatim text, source
(commit hash / file:line / doc), date, subject (generator / importer / own tool / engine / animation-rig),
kind (property / cause / magnitude / effect).

**Verdicts.** Each claim is judged against evidence from this repository only:
- `CONFIRMED` — a measurement in results/ agrees;
- `CONTRADICTED` — a measurement in results/ shows it is false;
- `PARTLY` — right observation, wrong cause or wrong magnitude (> 2× off), or true for some assets only;
- `UNTESTABLE` — no measurement in this study bears on it (reported, not counted in rates).
Verdicts are drafted by the assistant with the evidence pointer, independently re-judged by a separate
agent shown the same evidence; disagreements are listed and resolved with a written reason; the author
signs off. No new measurement is made *to rescue or sink a specific claim*; if a claim needs a new
measurement to be judged, it is `UNTESTABLE` unless the measurement is listed below in advance.

Pre-listed new measurements allowed for C: (i) pivot height of each NPC after the game's own import
(UniGLTF axis reversal applied to the B1 boxes, computed offline); (ii) the GLB root rotation and node
chain as seen by MeshLab's and Blender's importers (whether the rotation node survives an OBJ export).

**Hypotheses.**
- **H6:** at least 20 % of testable claims are `CONTRADICTED` or `PARTLY`.
- **H7:** most `CONTRADICTED` claims were never revised later in the history (no later commit, comment
  or doc states the corrected version up to 87fdd16).
- **H8 (exploratory):** claims of kind *cause* are wrong (`CONTRADICTED` + `PARTLY`) more often than
  claims of kind *property*.
Rates are reported as counts with the denominator; no inferential test (claims are not independent).

## D — Defect lifecycle

**Defects.** Every problem the paper identifies (facing via importer; unit scale; base map stored
uncompressed; normal/MR maps dropped; CPU-readable copies; companion torn by simplification; companion
rotation node lost; boss bind-pose hover; idle bob; other clips sinking; Built-in shader magenta) and every
`ASSET`/`ENGINE` fix in B5.

**Per defect:** introduced (first commit where the defect exists in the game), first observed (earliest
commit or doc that describes the symptom; channel = developer play-test / assistant / build / this
audit / never), fixed (commit that removes it, if any), number of fix commits in the chain, elapsed time
introduced→observed and observed→fixed, whether the first explanation recorded for it was later
contradicted (link to C), and whether it is present in the final build.

**H9 (descriptive):** defects visible on screen in play were observed and fixed within the development
period; defects not visible on screen (texture format and maps, mesh cracks seen only up close)
survived to the final build.

## Outputs
`results/claims_extract_a.json`, `results/claims_extract_b.json`, `results/claims.json` (merged, with
verdicts and both judges), `results/defects.json`, summaries appended to `results/report.json` by
`scripts/report_cd.py`.
