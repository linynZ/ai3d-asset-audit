# Round-2 fact-check: revised paper (7 pp., working tree after 1715f6d, uncommitted)

Date: 2026-10-05. Scope: all sections that `main.tex` inputs (abstract, introduction, related, corpus, method, results with results_b4, discussion, limitations/deviations, acks). `results_b4_xuanji.tex` is **not input** anywhere, so it was not checked as paper text.
Sources: `PLAN.md` (2b0bc54), `results/*.json(l)`, `scripts/*.py`, `facing_sheet.png`, `paper/figures/assets_strip.jpg`, the game repo (read-only), and the shipped build `D:\ChronoTraveler\ChronoTraveler_Data`. I also recomputed several values independently: build texture totals with UnityPy, E1 phase errors from `grounding_raw.json`, baseline coverage from `baseline.json`, and per-asset B4 rows from both jsonl files.

Verdicts: **WRONG** = contradicted by the data · **OVERSTATED** = right direction, stronger than the evidence · **UNSUPPORTED** = no released evidence, or not produced by any released script · **OK**.

---

## A. Problems, ranked by severity

### Critical

| # | Location | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|---|
| 1 | Method B5 ("and the author signed off"); Limitations "Not blind" ("reviewed by the AI assistant and the author"); Acks ("The author reviewed the labels") | The author signed off the labels | **WRONG (as of now)** | `results/history_labels.json` → `"status": "drafted by two AI labellers; reviewed by the AI assistant (two rounds, see overrides); awaiting author sign-off"`. This is round-1 #6 and is still open. | Have the author do the sign-off and update the status field, or change all three passages to "awaiting author sign-off". |
| 2 | Abstract ("We release scripts, measurements, labelled commit history and review reports"); Limitations/Authorship ("are public") | The materials are public | **WRONG (as of now)** | `gh repo view linynZ/ai3d-asset-audit` → `PRIVATE`. The whole revision is also uncommitted in the working tree (`git status`: sections, figures, bib and main.pdf all modified). This is round-1 #7 and is still open. | Commit the revision, make the repo public or archive it on Zenodo, and give the URL/DOI in the paper. |

### Major

| # | Location | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|---|
| 3 | Results 5.3 ("Together the 24 maps are 2,056 MiB") | 24 maps = 2,056 MiB | **WRONG** | `build_textures.json` "generated" has **26** textures: 24 × ARGB32 4096² at 89,478,484 B = **2,048.0 MiB**, plus two 2048² `texture_pbr_20250901*` maps (DXT1 base 2.67 MiB, DXT5 `_normal` 5.33 MiB), which are not NPC or prop maps. 2,056 is the 26-texture total. The share is 2,048 / 2,943.5 = 69.6 %, so "70 %" survives. | "Together the 24 maps are 2,048 MiB, 70 % of the 2,944 MiB…" |
| 4 | results_b4 ("Welding … removes the dilemma at little cost: … and mean surface distance is lower") | W has lower mean distance than S | **WRONG at 12.5 %** (true only at 6.25 %) | `report.json` B4 median mean distance, S vs W: 50 % 0.017 vs 0.022; 25 % 0.040 vs 0.051; **12.5 % 0.089 vs 0.098**; 6.25 % 0.241 vs 0.169. The sentence covers 12.5 % and 6.25 %, but W is lower only at 6.25 %. | "…and at 6.25 % mean surface distance is lower (0.17 vs 0.24 %); at the other targets it is slightly higher." |
| 5 | Abstract ("stored each asset's 4096² base map uncompressed **with a CPU copy**"); Intro ("kept a CPU copy"); Discussion ("kept a CPU copy") | Every asset keeps a CPU copy | **OVERSTATED** | 21 of 24 are `readable=True`; 3 are not (`B3_build`). Results 5.3 states this correctly ("21 of the 24"). | "…uncompressed, in 21 of 24 cases with a CPU copy". |
| 6 | Results 5.3 ("Imported through the texture importer, as the boss's and companion's textures were, the same base map would be 21.3 MiB in BC7.") | The texture importer gives BC7 | **OVERSTATED / misleading** | In the build, the textures that did go through Unity's importer are **DXT1 (BC1)** base maps: `xuanji_basecolor` 2048² DXT1, and the 2048² generated `texture_pbr_20250901` DXT1 (plus DXT5 normals). Neither is BC7. With the importer's actual choice, a 4096² base map would be **10.7 MiB** (BC1), not 21.3. 21.3 MiB in BC7 is correct arithmetic, but the build gives no evidence that the importer would choose BC7. | "…would be 10.7 MiB with the DXT1 compression the importer gave the boss's and companion's base maps (21.3 MiB in BC7)". |
| 7 | Method B5 / Results 5.5 (3 fixes; "two of the three fixes repaired a step we had added"; H5 outcome) | The plan's rule ("ambiguous cases go to OTHER") was applied in round 2 | **OVERSTATED (inconsistent application)** | Round 2 moved `dc81a43` to OTHER with the reason "Labeller confidence **low** and cause mixed … the plan sends ambiguous cases to OTHER". `9760126` (the boss hover, the only generator-origin fix) also has `confidence: low` and stays ASSET. Applying the same rule would leave 9 ASSET commits and 2 fixes, both own-pipeline and both countable. H5 would still be supported, but "two of three" would become "both", and the only generator-origin fix would disappear from the ASSET set. Round-1 #5 had already flagged 9760126 as low-confidence. | Either justify keeping 9760126 (e.g. E1 independently confirms that the cause is the generated animation, so it is not ambiguous) in the text or the override log, or move it and restate the counts. |
| 8 | Results 5.3 "2,944 MiB"/"70 %"; Results 5.6 "within 20 mm", "median 4 mm"; sink figures 0.27/0.08/1.19 m | Numbers come from released scripts | **UNSUPPORTED (provenance)** | `texture_totals_MiB` (in `build_textures.json`) and every `phase_analysis` block (in `grounding.json`) are written by **no released script**. `build_textures.py` does not compute totals. `grounding_analysis.py` writes `grounding.json` without `phase_analysis`, so rerunning it **deletes** these fields. `report_extra.py` only copies them. My independent recomputation confirms the values: the UnityPy total is 2,943.5 MiB over 282 textures; the sinks are 0.268/0.079/1.189 m; the idle phase median is 3.9 mm; my wrap-around phase implementation gives a worst case of **19.7 mm** (the file says 20.4). | Add the totals to `build_textures.py` and the phase analysis to `grounding_analysis.py`, rerun, and quote the regenerated numbers. |
| 9 | Table 2, H4 row ("not supported (1/24)") | The outcome under the plan's condition | **OVERSTATED (post-hoc condition shown as the result)** | The plan's with-UV run loads the GLB directly, which is condition **S**. Under S, 6/24 miss 6.25 %. 1/24 is condition W, which was added after B2. The verdict "not supported" holds under both. | "not supported (S: 6/24; W: 1/24)". |

### Minor

| # | Location | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|---|
| 10 | Results 5.2 | "14–64 per thousand triangles" | **WRONG (rounding)** | `B2_generated_uv.charts_per_1k` = 14.06–**63.46** (median 31.57). | 14–63. |
| 11 | Results 5.1 | origin "within 0.43–0.58 of its width" | **WRONG (rounding)** | pivot_x_frac min = 0.435, which rounds to 0.44. Depth 0.295–0.692 → 0.30–0.69 is OK. | 0.44–0.58 (or 0.435–0.576). |
| 12 | Method | "committed together 22 minutes later"; plan "16:32" | **WRONG (by about 1 min)** | `2b0bc54` 16:31:49 (push 16:32:05); `1715f6d` 16:53:15, which is 21.4 min after the commit and 21.2 min after the push. | "21 minutes later"; "committed at 16:31 and pushed at 16:32". |
| 13 | Results 5.6 + Fig. 2 caption | "lands within 20 mm … at any starting phase" | **WRONG (rounding)** | `phase_worst_mm` = 20.4. | "within about 20 mm" or "within 21 mm". |
| 14 | Abstract ("…crack-free at a similar colour error"); results_b4 ("at little cost") | Welding has a similar colour cost | **OVERSTATED** | The medians are similar only at 6.25 % (3.7 vs 3.5). At 12.5 % W is 1.5 vs S 0.1. The worst case is W 37.1 vs S 9.6 (the stalled engineer). | Say "a median colour error 1–4 levels above the noise floor (seam-split: 0.1–3.5)". |
| 15 | Discussion checklist item 3 | A seam-split buffer "returns the requested triangle count" | **OVERSTATED** | At 6.25 %, 6/24 S runs did not reach the target within 3 passes. | "…usually returns the requested count". |
| 16 | results_b4 | "The torn mesh shipped after a play check in which no one reported a crack." | **UNSUPPORTED** (round-1 #28 still open) | No playtest record is cited. The commit `a870939` says "user Play-verified", which supports "a play check" but not "no one reported a crack". | "…shipped after a play check (commit a870939); no commit mentions cracks." |
| 17 | Discussion checklist intro | "each item is a script that runs in seconds per asset" | **UNSUPPORTED** | No checklist scripts are released as such. Reading the build with UnityPy and evaluating four clips in Blender have not been timed. | Drop "in seconds", or report timings. |
| 18 | Discussion ¶1 | texture problems left no trace "because nothing looked wrong" | **UNSUPPORTED (causal)** | The absence of commits is verified (keyword search over 484 commits for ARGB/readable/compress/BC7/DXT/4096/normal map: no hit concerns the generated textures). The reason is speculation. | "…left no trace in the commit history." |
| 19 | Results 5.2 | "studies of **other** generators describe their output as noisy or non-manifold [wang2025partuv, bhosikar2026faqem]" | **OVERSTATED** | Bhosikar et al. test on **Hunyuan3D 2.0** outputs (prior_experience §2.8), which is not another generator. | "studies of other generators and of earlier Hunyuan versions…" |
| 20 | Related, Simplification | "Seam-aware methods preserve the parametrisation exactly [sander2001tmpm, liu2017seamless]" | **OVERSTATED for Sander** | TMPM builds and optimises a parametrisation for the progressive mesh (stretch metric); it does not preserve an existing one exactly. The "exactly" claim fits Seamless (Liu 2017). | Split: "Sander et al. optimise a parametrisation shared across LODs; Liu et al. preserve seams exactly." |
| 21 | Related | Galashots "adopted the same fix, welding first" | **Slightly OVERSTATED** | Their PR welds, collapses **without** UV delimit, re-unwraps and re-bakes (prior_experience §1.3). Welding is shared; the rest is not. | "…adopted the same first step, welding…". |
| 22 | Results 5.2 | licensed character "covers 96 %" | **OVERSTATED as a packing comparison** | `baseline.json`: union coverage 0.961, but `uv_area_sum` = **4.449**. Its UVs are heavily stacked or overlapping (or tiled), so union coverage does not mean packing efficiency here. | Add "(UVs stacked: summed chart area 4.4× the square)" or drop the 96 %. |
| 23 | Results 5.6 / Related | The game read "the renderer's bounds" = bind-pose bounds, while Related cites Unity: skinned bounds are "precomputed … from its animations" | **UNSUPPORTED / unreconciled** (round-1 #13, partly open) | The only evidence for bind-pose renderer bounds is the developer's comment in `GroundSnap.cs` l.10. The cited doc says otherwise. | One sentence: "the game's code assumed the renderer bounds were the bind pose; Unity documents them as precomputed from the clips. Either way they are not per-frame." |
| 24 | Deviations | Completeness | **Incomplete** | Not listed: (a) the plan's E1 estimator "the shipped constant offset" was not scored, and "minimum over the first N frames" became "10 samples 0.16 s apart" (round-1 #14 still open); (b) the H2 Wilson 95 % CI planned in PLAN.md was dropped; (c) the planned outputs `cost.json`/`decimation.json` became other files; (d) the welded companion at 82,829 triangles in Fig. 1 (bottom) is produced by no released script (`crack_render_blender.py` only renders given OBJs). | Add (a)–(c) to Deviations; release the script for (d). |
| 25 | Corpus | "model 3.1, '50k faces' setting" | **UNSUPPORTED by artifacts** (round-1 #25 open) | Nothing in the files records the service version. | "(version as recorded by the author at generation time)". |
| 26 | Abstract | "Simplifying the seam-split vertex buffer **that a glTF loader returns** tore the companion" | **Slightly OVERSTATED (generalisation)** | Tearing depends on the simplifier. meshoptimizer infers seams from positions and stalls instead of tearing (prior_experience §2.3). Only MeshLab was tested (peer-review M5(b′) open). | "…that MeshLab's glTF loader returns…" |
| 27 | Results 5.2 | "seams duplicate 1.31–1.81 vertices per welded vertex" | **Wording** | `seam_split_factor` = raw/welded vertices, so a seam-split mesh **stores** 1.31–1.81 vertices per welded vertex (0.31–0.81 duplicates). | Reword. |
| 28 | Discussion | "Items 1 and 3 restate existing guidance on real-world scale and **origin**" | **Mismatch** | Item 1 covers size and front, not origin. The Khronos guideline wording is verified ("1:1 the size of the real item"; "bottom center … at 0,0,0"). | "on real-world scale [khronos3dc]…" or add origin to item 1. |
| 29 | Corpus | "between June and August 2026" | **Minor / ambiguous** (round-1 #27) | Git runs from 2026-06-11 to 2026-08-10, but the project notes (CLAUDE.md change log "2026-05~06: URP 迁移 + ECS…") record work in May. | "version-controlled from June to August 2026". |
| 30 | Terminology | triangles vs faces | **Inconsistent (minor)** | `figures.py` x-axis label is "target (% of faces)"; the paper text uses triangles. | Relabel the axis "% of triangles". |
| 31 | Intro | "extends our earlier audits of AI-generated game content [featureorleak, countingwhat]" | **Loose** (round-1 #36 open) | featureorleak audits an LLM NPC's guardrails (answer leakage), not generated content as such. Both DOIs resolve (Zenodo 23150869 and 23150165, HTTP 200). | "earlier audits of LLM components and LLM-generated content in the same game". |
| 32 | Reproducibility | `conventions.json` from the released `conventions.py` | **Check** (round-1 #33 open) | The output mtime (16:32) is still earlier than the script mtime (16:35). | Rerun `conventions.py` and `report.py` and confirm identical output. |
| 33 | Results intro vs Abstract | Which "three" failed | **Potentially confusing** | Abstract: H1, H2 and H4 not supported. Results intro: "none of the three that had not been looked at" (H2, H4, H5) "held as first analysed". Both are true, but the two sentences describe different sets of three. | Name the hypotheses in one of them. |
| 34 | acmart | build warning | Minor | "No city present for an affiliation" (`main.log`). | Add a city. |

**Counts:** WRONG 8 (#1, 2, 3, 4, 10, 11, 12, 13). OVERSTATED 11 (#5, 6, 7, 9, 14, 15, 19, 20, 21, 22, 26). UNSUPPORTED 7 (#8, 16, 17, 18, 23, 24, 25). Wording/consistency 8 (#27–34).

---

## B. Round-1 items: status

**factcheck.md**
- #1 facing → **fixed**. All 15 NPCs face +Z in `facing_sheet.png` (checked visually: the +Z panel shows the face and the −Z panel the back, for every NPC). UniGLTF `ScriptedImporterAxes.Default` → `UniGLTFPreference.GltfIOAxis`, whose default is `default(Axes)` = `Axes.Z` (reverse Z) when the EditorPrefs key `UNIGLTF_IO_AXIS` is unset. No such key exists in this machine's registry (HKCU\Software\Unity Technologies\Unity Editor 5.x), so the default was in force. All `.glb.meta` have `reverseAxis: 0`. The label was moved to ENGINE.
- #2 build premise → **fixed** (build readout; NPCModelSetupTool `CopyTex` copies only the main texture; `_BumpMap`/`_MetallicGlossMap` empty in all 24 NPC/prop mats).
- #3 H1 → **fixed** ("not met (23/24)").
- #4 is_fix → **fixed** (listed in Deviations; both readings given).
- #5 ambiguous to OTHER → **partly**: dc81a43 moved, 9760126 (also low confidence) kept; see A#7.
- #6 sign-off → **OPEN** (A#1).
- #7 public → **OPEN** (A#2).
- #8 overlap → fixed (claim removed, deviation listed).
- #9 coverage bias → fixed (an upper bound of about 2 points is stated).
- #10 −Z up → fixed.
- #11 genus → fixed (removed).
- #12 6 mm → fixed (phase and all clips reported); provenance see A#8; rounding see A#13.
- #13 bounds vs Unity doc → **partly open** (A#23).
- #14 E1 constant-offset estimator not scored → **OPEN** (A#24a).
- #15 106k note → fixed ("earlier trial run").
- #16 component metric → fixed (B4 components no longer quoted).
- #17 Wilson CI → removed, but the removal is not listed as a deviation (A#24b).
- #18, #19, #20, #21, #22, #23, #24 → fixed.
- #25 version 3.1 → **OPEN** (A#25).
- #26 "defaults" / API default 500k → minor, still "our defaults" and "higher setting"; acceptable.
- #27 dates → minor, open (A#29).
- #28 play check → **OPEN** (A#16).
- #29 tolerance sweep → fixed (removed).
- #30 S schedule → fixed in results_b4 (the 0.55 schedule is explained).
- #31 Hausdorff → fixed.
- #32 B3 as stored → fixed (Deviations).
- #33 conventions.json mtime → **OPEN** (A#32).
- #35 "weeks" → fixed.
- #36 featureorleak → open (A#31).
- #37 → fine.
- #38 → fixed (0.9 removed).

**peer_review.md**
- M1 → fixed.
- M2 → fixed ("not a registered report"; investigator knowledge stated; title changed), apart from the sign-off.
- M3 → fixed ("closed and edge-manifold"; self-intersections reported).
- M4 → fixed (81-mesh baseline). The studio boss was not given B2/B3 rows: open, minor.
- M5 → (a) colour error added; (b) S + boundary preservation added; normal flag equalised; (b′) meshoptimizer/gltfpack comparison **not done** (A#26); novelty reframed with hoppe1996pm. Fixed apart from b′.
- M6 → fixed.
- M7 → fixed (build readout replaces the benchmark).
- M8 → fixed ("derived here and not yet validated").
- M9 → mostly fixed (Khronos guidelines, Blender IO, meshopt, PyMeshLab, Liu 2025 cited). glTF-Validator and atlas packing-efficiency work are still not cited (minor).
- M10 → fixed ("completed"; "26 meshes, of which 25 shipped").
- Minor items: figure `\Description` added; affiliation city still missing (A#34); "% of faces" axis (A#30); Table 2 caption now notes the stalled asset (fixed).

**prior_experience.md**
- "No independent audit" claim → fixed (Begemann cited).
- "Not encoded anywhere" → fixed.
- Bind-pose / localBounds nuance → partly open (A#23).
- Rig type → verified (`boss_idle.fbx.meta` `animationType: 2` = Generic).

---

## C. Checked OK

**Abstract / Intro:** 26 meshes = 15 + 9 + companion raw/shipped + boss; 24 from one setting; raw meshes closed and edge-manifold (24/24); UVs within the range of purchased meshes; dropped normal/MR maps (NPCModelSetupTool `CopyTex`); 70 % of build texture data (69.6–69.8 %); no commit history trace (keyword check); 2,433 pieces; about 1 m scale (0.895–1.151); 0.46–0.68 m lift and 0.22 m bob (0.224).

**Corpus:** 87fdd16 (2026-08-10) is the final build; 484 non-merge commits; UniGLTF 0.131.1; reverse-Z default (see B); 1.7 m / 180° / URP/Lit (`NPCModelSetupTool.cs` l.33–34, 173–174); props use the same tool (`Resources/CharacterModels/prop_trade_*_Mats`); 497,850 → 82,829; 28 bones, 9,038 triangles ×4 FBX (`grounding_raw.json`); manifest with SHA-256.

**Method:** plan before scripts (2b0bc54 16:31:49 < first script); 25-term pattern; 156 matches; 200,000 Hausdorff samples (`decimation.py` l.90); 60,000 colour samples (`decimation_extra.py` l.28); 60 fps (111 frames / 1.85 s); 10 m scaling (`GAME_HEIGHT = 10.0`); 10 × 0.16 s (`GroundSnap.cs` l.27–30).

**Results 5.1:** rotation [0.7071,0,0,0.7071] ×24 (+90° X; local −Z → +Y); double-sided ×24; KHR_materials_specular ×24; 3×4096² PNG ×24; Blender I/O generator ×24; median 1.082; milestone 0.89501; pivot y = 0; depth 0.30–0.69; all 15 NPCs face +Z (facing_sheet, Fig. 1 top).

**Results 5.2:** closed/edge-/vertex-manifold 24/24 (non-manifold vertices max 0); 0 degenerate/duplicate; 19 single component + 5 with 2–4; self-intersections 11–524, median 64 (63.5); charts 703–3,088; median 32/1k; coverage 48–68 %, median 53 %; seam split 1.31–1.81; baseline 81 meshes, 54 self-intersecting, 41 not closed (40 closed); Nike 10–44 charts/1k and 36–99 %; Altar median 14 %; Egypt median 0 (max 41 %); companion 44,316 / 1,442 / 2,433 / 9,868 (19 raw).

**Results 5.3:** geometry 1.28–1.60 MiB; 256/64/32 MiB; 20–25× (20.04–25.05); companion raw 3×4096², BC7 ratio 4.25 → 4.3; 85.3 MiB ARGB32 (format 5) 4096² with 13 mips; 21/24 readable; UniGLTF `new Texture2D(…ARGB32…)` + `LoadImage`; build total 2,943.5 MiB (recomputed, 282 textures); largest other texture 21.33 MiB 4096² BC7 (format 25, `LVL3_hdrp_Albedo`; tied with three DXT5 4096² normals). Format codes 5 = ARGB32, 10 = DXT1, 12 = DXT5, 25 = BC7: correct.

**Results 5.4 / Table 3:** S 18/24/0.24 [0.32]/3.5 [9.6]; S_pb 0/0/–/2.4 [16.7]; W 23/0/0.17 [1.40]/3.7 [37.1]; N 24/0/0.12 [0.20]; N without normal flag 24 reached, 0 cracked. Both W maxima are `npc_rome_engineer`, which has the most charts (3,088) and stalled at 3,896 (main run) and 3,824 (extra run). 23/24 W reached in 1 pass; about 3,100 (median 3,119); S@50 % median 13,924; 6 S assets missed 6.25 %; S_pb minimum 13,238, median 21,939 (≈ 44.0 % of the median 49,890); colour 1.45 → 1.5, 0.14 → 0.1, 3.68 → 3.7, 3.5; companion W 31,116 in one pass with 0 boundary edges; 497,850 × 0.55³ ≈ 82,830; Fig. 1 description values (≈14,000 → 6,000; 0.02 → 0.24 %).

**Results 5.5:** 61/78/7/10 = 156; 7 features (c21ea44, 953f004, c1ff678, 40f7193, 61f3e91, 37e5b4e, c217b9b) as described; 3 fixes (9760126, 95cf232, 288327d); 2 of 3 countable; 9 of 10 countable; 2 of 3 own pipeline; first labelling 6 fixes, 3/6 countable; the moves of f3da6c2 to ENGINE and cca41fd/dc81a43 to OTHER match the override log.

**Results 5.6:** idle 1.85 s; 1.44 s window (77.8 %); median 4 mm (3.9); sinks 0.27/0.08/1.19 m (recomputed 0.268/0.079/1.189); single frame anywhere in the 0.22 m bob (max sink 0.222); Generic rig (`animationType: 2`); Settle 0.30 m and the BakeMesh comment (`GroundSnap.cs` l.48, 64–71).

**Related-work quotes** (against prior_experience.md): "generates over-fragmented cuts"; "rarely reported" / "almost never quantified"; PartUV 114 TRELLIS meshes with median 895 / mean 1,542; Begemann (fragmented UVs, texture loss under decimation); "a jumbled mess"; "identical vertices"; "does not merge superfluous vertices"; Bhosikar's pre-merge step; Galashots (2026-09-23, about two weeks before 10-05); "prevents [the] floating problem", Humanoid only; localBounds precomputed from animations; glTF metres / +Y / +Z / separate vertices; Blender IO merge option; Khronos 3DC 1:1 scale and bottom-centre origin (verified against the live guideline). All verbatim or faithful.

**Citations:** every `\cite` key exists in `references.bib` (0 missing). The 27 uncited bib entries are harmless (bibtex omits them). Each cited key supports its sentence apart from #20, #21 and #31 above.
