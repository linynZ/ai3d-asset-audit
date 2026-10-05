# Peer review: "Fit for the Engine? Auditing Image-to-3D Generated Meshes in a Shipped Game"

Reviewer stance: an applied venue (FDG short/long paper, a Eurographics short paper, or a games/graphics workshop). Reviewed from `paper/main.pdf` (6 pp.), `paper/sections/*.tex`, `PLAN.md`, `results/*` and the study repository history. I did not edit the paper.

**Recommendation: weak accept at a workshop / major revision for FDG or EG short papers.** The empirical core is useful and unusually honest. The main problems are one probable misattribution (facing), a few framing choices that overstate what pre-registration can buy here, and missing comparators that a graphics reviewer will ask for.

---

## 1. Summary of claims

The paper audits the image-to-3D meshes in a completed Unity game: 24 raw Hunyuan 3D v3.1 "50k faces" GLBs (15 NPCs, 9 props), a high-resolution companion and the version simplified for the game, and one studio-pipeline rigged boss. The analysis plan was committed before the audit scripts were run. Five hypotheses were set.

1. **B1 conventions (H1 "holds"):** every raw asset has a largest extent of about 1 unit (0.895 to 1.151), the same +90 degree X root rotation and `doubleSided: true`, and three 4096^2 PNG maps. The pivot is at the base. Facing (stated as "-Z") is "not encoded anywhere".
2. **B2 hygiene (H2 not supported):** all 24 raw meshes are watertight and edge-manifold, and 19/24 are a single component. All have self-intersections (median 64 faces) and high genus (median 60). UV coverage is 48 to 68 percent, and seam splitting inflates the vertex count 1.31 to 1.81 times. The shipped companion is badly broken: 2,433 components and 44,316 open edges.
3. **B3 cost (H3 holds):** texture memory is 40 to 50 times geometry memory in BC7. A post-hoc check of scene memory is "consistent" with BC7.
4. **B4 simplification (H4 not supported):** given welded input with per-corner UVs, MeshLab's texture-aware QEM reaches 6.25 percent on 23 of 24 assets with no cracks. Given the seam-split buffer that the glTF loader returns, every asset cracks at every target. The authors' earlier "UV floor" diagnosis for the companion was wrong; the loop simply ran out of passes.
5. **B5 history (H5 not supported):** of 484 commits, 156 matched the pattern and 13 were labelled ASSET; 6 of those are fixes, and 3 of the 6 fixed the authors' own processing. Only 3 of 6 were countable before import.
6. **E1 grounding (exploratory):** the boss's idle loop lifts it 0.46 to 0.68 m above the bind pose at 10 m scale. The shipped min-of-10-samples estimator lands within 6 mm of the loop minimum, but any constant offset leaves a 0.22 m floor.
7. **Contribution:** a pre-import checklist ordered by what each check would have caught.

## 2. Strengths

- **Real production data instead of a benchmark render.** Auditing assets that were actually shipped, together with the commit history of the fixes, is rare and valuable. The question (engine readiness, not visual fidelity) is well chosen and under-studied.
- **Negative results are reported plainly.** Three of five hypotheses fail, and the authors' own pipeline is identified as the source of the worst defect. The authors also correct their own earlier diagnosis (the "UV floor"). The arithmetic 497,850 x 0.55^3 = 82,829 checks out and is a nice piece of forensic reasoning.
- **The S/W/N simplification experiment is the paper's strongest technical result.** It is clean, cheap to reproduce, and actionable. The observation that the filter silently returns a cracked mesh with the requested face count is exactly the kind of failure practitioners hit.
- **The grounding analysis reaches a correct conceptual point:** a constant offset has a floor equal to the bob amplitude.
- **Artefact release.** Scripts, raw JSON, labels and the plan are all available, and the numbers I spot-checked against `results/report.md` match the text: geometry 1.277 to 1.597 MiB, ratios 40.08 to 50.11, Wilson CI 0.092 to 0.405, decimation medians, and 31,116 = 6.25 percent of 497,850.
- The paper is short, concrete and mostly free of padding.

## 3. Major concerns

### M1. The "facing" defect is probably an importer axis-conversion convention, not a generator property (affects B1, H5, abstract, discussion, checklist)

The paper states the generator's characters face "-Z, so the character shows its back to a player" and that facing "is not encoded anywhere". Two problems:

- **glTF 2.0 does encode this convention.** The spec states that the front of an asset faces +Z, +Y is up, and units are metres. The paper already cites the spec for +Y up, so this is easy to fix.
- **The "-Z" comes from the developer's commit messages, which describe the Unity frame after import, not the glTF frame.** For example, commit `f3da6c2` reads "Hunyuan exports face -Z, NPC turns +Z to player". The game imports GLBs with UniGLTF (`com.vrmc.gltf` 0.131.1; the `.glb.meta` files show `ScriptedImporter`, `reverseAxis: 0`, i.e. invert Z). Under a Z-inverting conversion, a spec-compliant +Z-front asset ends up facing -Z in Unity. Unity's own glTFast negates X instead and would keep the front at +Z.
- **Direct check:** front/back point-splat renders of `npc_china_artisan.glb` and `npc_rome_senator.glb` in the glTF world frame (node chain applied, viewer on +Z vs -Z; produced with the study's own `glb.py` reader in the session scratchpad) show the face from +Z in both cases. So these assets appear spec-compliant in facing.

If this holds for all 24, then the "first fix", the two "facing" fixes in B5, the double-turn fix, the abstract's "facing away from the viewer", Discussion "the costliest defects, facing and grounding", and checklist item 1 all need to change. Facing becomes an ENGINE/importer convention (any spec-compliant GLB through this importer would hit it), not ASSET. This also shifts H5 (the denominator shrinks to about 4 ASSET fixes) and the "counting vs. looking" argument: facing *is* knowable from the spec plus the importer's documented axis conversion, without looking.

**Fix (under 1 day):** add a facing probe to B1 for all 24 assets (two orthographic renders, or a texture-colour/face-landmark heuristic). Report the frame explicitly ("in glTF coordinates the front is +Z, as the spec requires; UniGLTF's default Z inversion turns it to -Z in Unity"). Relabel the B5 commits and re-state H5. This is the single most important correction, because a games reviewer who knows glTF will catch it.

The same caution applies to "real-world size must come from outside": under the spec, 1 unit = 1 m, so the generator *does* state a size; it is simply wrong (a 1 m camel). Framing this as "the file violates the spec's metre semantics" is stronger and more accurate than "conventions the file does not state".

### M2. "Pre-registered" overstates what was done (title, subtitle, abstract, method)

What the record supports: a plan committed to the authors' own GitHub repo (`2b0bc54`, 16:31) **22 minutes** before a single commit (`1715f6d`, 16:53) that contains every script, every result, 156 commit labels and the full 6-page draft. Concerns:

- **No third-party timestamp.** OSF, AsPredicted or a Zenodo deposit would provide one; a self-hosted git history can be rewritten. The ordering claimed in the Deviations section ("the GLB reader and the hygiene script were run before the B4 script was written") cannot be verified, because all of it is in one commit.
- **The investigator knew far more than the disclosed pilot.** The pilot disclosure covers GLB headers only. But the author built the game and wrote the commit messages that B5 labels, and the plan's E1 paragraph already quotes the exact BakeMesh readings (0.68, 2.29) and the five-fixes-in-26-minutes history. H5 and E1 are therefore not blind in any sense. The plan says this for E1 ("reported from the commit record"), but the paper should say it for B5 as well.
- **The two hypotheses that "held" were the two the pilot had already seen.** H1 restates the pilot. H3 follows arithmetically from the pilot's triangle counts and texture sizes. Every hypothesis that was genuinely untested (H2, H4, H5) failed. "Of five hypotheses, two held and three did not" reads as partial predictive success; the honest statement is stronger and more interesting: *every untested prediction was wrong*.
- **H1 strictly failed.** The plan says "every raw asset ... largest extent within 0.9 to 1.2". The milestone is 0.895. Calling H1 "holds with one marginal exception" is exactly the post-hoc softening that pre-registration exists to prevent. Say "H1 fails on its pre-registered bound (23/24); the exception is 0.005 below it" and move on.
- **The headline finding depends on analysis choices made after seeing data.** These choices are: the S/W split (disclosed); the `is_fix` field that defines H5's denominator of 6 (not in the plan and not listed as a deviation); the `origin` field behind "three of six" (disclosed); and the B3 metric changing from "GPU geometry bytes (as uploaded: vertices x stride + indices)" in the plan to "as stored" in the paper (not disclosed). The plan also lists `results/cost.json` and `decimation.json`, while the repo has `decimation.jsonl` and no `cost.json`.
- **Label sign-off.** `results/history_labels.json` has `"status": "drafted by AI labellers + reviewed by the AI assistant; awaiting author sign-off"`, while Method and Acknowledgements say "the author signed off". Either update the file or the text. As it stands this is an integrity inconsistency that a careful reviewer will find.

**Fix:** drop "Pre-Registered" from the subtitle. Use "an audit plan committed before analysis" in the body, and keep the Deviations section, which is good. Add the missing deviations (is_fix, B3 metric, outputs), restate H1 as failed, add a sentence on investigator knowledge, and fix the sign-off status. Optionally deposit plan, scripts and results on Zenodo now and cite the DOI with an honest date. For the next study, register on OSF.

### M3. "The raw meshes are clean" is overstated for a graphics audience

Every one of the 24 meshes self-intersects (11 to 524 faces). The median genus is 60, up to 361, which is implausible for a person or a camel. Five have 2 to 4 components. "Watertight" in much of the graphics and fabrication literature means closed, manifold and free of self-intersection (a valid solid). These meshes are closed and edge-manifold but not solid. Self-intersections and spurious handles matter for voxelisation, collision proxies, lightmap/AO baking, boolean operations, remeshing and some simplifiers. "None of these showed up in play" is absence of evidence; nobody looked for them.

**Fix:** replace "clean" with "closed and edge-manifold" throughout the abstract, intro, Section 5.2 title and Discussion. Report self-intersection and genus as findings, and offer one cautious hypothesis about their origin (e.g. the service's own reduction to the 50k budget after iso-surface extraction). Note that iso-surface extraction produces closed manifold output by construction, so H2's failure was predictable from the generator design. That weakens "the findings run against our expectations" but strengthens the paper's credibility.

### M4. No baseline: "where the meshes depart from hand-made assets" is asserted, not measured

UV chart counts (703 to 3,088), coverage (48 to 68 percent), seam-split factor (1.31 to 1.81), self-intersections and genus mean little without a comparator. Hand-authored game assets also have split factors around 1.2 to 1.6 from hard edges and UV seams, and automatic atlases commonly pack at 60 to 75 percent. Gutters and padding mean 100 percent is never the target.

**Fix (under 1 day, no new generation):** run B1 to B3 on the non-generated meshes already in the game: the licensed Astraea character, a handful of meshes from the purchased Temple of Nike and Altar Ruins packs. Also run them on the **studio-pipeline boss mesh**, which is never given a B2/B3 row even though it is the generator's own "game-ready" route (retopology plus UV). One extra table column turns three assertions into measurements. If time allows, run xatlas on two raw meshes as an "automatic atlas" reference for packing efficiency.

### M5. The simplification result needs (a) a texture-error measure and (b) a check of whether the effect is loader-specific

- **(a)** Hausdorff distance measures geometry only. W "never cracks", but the paper does not show that W's per-corner UVs are still *correct* after collapse (texture stretch, chart-boundary bleeding). Without that, "welding first ... is the fix" is half-shown. Within a day: render 4 to 8 fixed views of 3 to 4 assets for original/S/W in Blender or pyrender and report image-space error (PSNR/SSIM or a perceptual metric), or a UV-stretch statistic. One figure with an original/S/W crop of the companion would also make the crack finding visible to readers. At the moment there is no image of any asset in the paper.
- **(b)** Parameters interact with the input. All with-UV runs use `preserveboundary=False`. With seam-split input, seams *are* boundaries, so turning boundary preservation on would likely stop the cracks but create a floor. The paper should report S with `preserveboundary=True` (one extra run) so the reader can separate "seam-split input" from "seam-split input with boundaries unprotected". Note also that N uses `preservenormal=True` while S/W do not (`scripts/decimation.py` lines 51 to 55); disclose or equalise.
- **(b')** Is this a MeshLab/PyMeshLab loader quirk or general? One run with a mainstream game-pipeline simplifier (meshoptimizer via `gltfpack -si 0.0625`, or Blender's Decimate on an imported GLB) on a few assets would tell readers whether the pitfall generalises. This is the most practically useful comparison the paper could add.
- **Novelty framing:** treating attribute discontinuities in simplification is classic graphics. Hoppe 1996 handles discontinuity curves and "wedges"; Garland and Heckbert 1998, Hoppe 1999 and Sander et al. 2001 are already cited; Cohen et al. 1998 (appearance-preserving simplification) is not. `hoppe1996pm` is in `references.bib` but never cited. The contribution is not the phenomenon; it is that a common scripted pipeline (glTF loader into texture-aware QEM) silently triggers it, and that this happened in production. Say that explicitly. The welded-with-wedge-UV representation is the textbook input; acknowledge that.

### M6. E1 reports one of four animations

The plan says "every frame of each of the four animations". `results/grounding.json` contains all four, but the paper reports only idle. For attack, hitdown and leap the lowest-point ranges are 1.39, 3.27 and 3.25 m, and the shipped estimator errs by up to 1.28 to 3.24 m. Some of this is intentional airtime, but the reader cannot judge that. Report a 4-row table (range, bind-pose error, single-frame error, min-of-10 error) and say which loops are supposed to leave the ground.

Two related points:
- The ten samples cover 1.44 s of a 1.85 s idle loop, so the "within 6 mm" result is partly fortunate coverage. State the coverage.
- Mention the engine-side tool built for this problem: Unity's animation import "Root Transform Position (Y)" bake/offset options and root-motion settings. "The engine's default" for grounding is ambiguous and should be made concrete.

### M7. The memory "consistency check" is weak and may be measuring the wrong thing

The check attributes the 550 MiB difference between scenes to 9 props (61 MiB each, "close to BC7's 64"), while noting that the scene has other content and that the game's own earlier analysis attributed it elsewhere. Unity's "total allocated memory" counter mainly tracks native/CPU allocations; GPU-resident texture memory is not reliably included on desktop. The paper also never states which importer and texture settings were actually used (UniGLTF ScriptedImporter, with whatever compression and max-size it applies). Separately, the companion's textures were downsized to 2048/1024 (commit `37e5b4e`), yet B3's companion ratio (4.3) appears to assume 3 x 4096^2.

**Fix:** either inspect the actual imported texture assets (format, size, mip count) and report those, or move the check to a footnote labelled "not evidence". Do not let a post-hoc number that agrees with the hypothesis sit in the main results. Clarify which texture sizes the companion ratio uses.

### M8. The checklist is presented as "tested"; it is derived

"What transfers is the checklist and how it was tested" (Intro). The checklist is distilled from one game's history; it has not been applied to any other assets or project. The ordering "by what each check would have caught here" also depends on M1. **Fix:** "what may transfer is the checklist, which we derive from this case and have not validated elsewhere". If there is half a day, applying the checklist script to the purchased/hand-made assets from M4 at least shows its false-positive behaviour.

### M9. Related work misses the practitioner and specification literature that is closest to the checklist

- **Khronos 3D Commerce "Real-time Asset Creation Guidelines" and the Khronos glTF-Validator.** These specify units, orientation, origin placement, texture size and UV usage for real-time assets, and are the most direct precedent for a pre-import checklist. Without them the checklist reads as novel when part of it is an industry standard.
- **Engine import documentation:** Unity model import settings (scale factor, axis conversion), Unity texture import (max size, compression), Unreal FBX import. The UniGLTF / glTFast axis-conversion difference is directly relevant to M1.
- **UV atlas efficiency:** LSCM (Lévy et al. 2002) and xatlas are already in the bib but uncited. Add atlas packing-efficiency work (e.g. Limper et al., "Box Cutter", 2018; Liu et al., "Atlas Refinement with Bounded Packing Efficiency", 2019) to support any statement about "half-empty" atlases.
- **Attribute discontinuities in simplification:** Hoppe 1996 (in the bib, uncited), Cohen, Olano and Manocha 1998. The game-pipeline simplifiers meshoptimizer/gltfpack and Simplygon should be mentioned as the tools practitioners actually use.
- `botsch2010pmp`, `levy2002lscm`, `young2018xatlas`, `unity_ik` and `khronos_khr_materials_specular` sit in `references.bib` uncited. Either cite them where they support a claim or drop them.
- The related-work disclaimer "we searched arXiv and the web rather than every venue, so we claim only that such work is not prominent" is honest but weak. Search the FDG, EG, I3D, HPG and SIGGRAPH Asia programmes and the Games/Graphics tracks of CHI PLAY for "asset pipeline", "glTF", "generated asset" and "production" before submission.

### M10. Title, subtitle and the count of 26

- "Shipped game": the game is a completed MSc project build (87fdd16, 2026-08-10), not a commercial release. Define "shipped" at first use ("the final build of a completed game") or use "a completed game".
- "26 generated assets shipped" (abstract) is wrong. The raw 497,850-triangle companion was not shipped, and the boss is one mesh in four files. It is 25 shipped assets / 26 meshes audited. Pick one count and use it everywhere.
- Suggested title: *Fit for the Engine? An Audit of Image-to-3D Meshes in a Completed Unity Game*, subtitle *Conventions, Texture Budget, Simplification Input and Animated Contact* (or no subtitle). This also puts the findings rather than the method in the subtitle.

## 4. Minor concerns

**Terminology (define at first use, ideally in Section 4):**
- *Seam-split:* "a vertex buffer in which vertices are duplicated wherever a per-vertex attribute (UV, normal) is discontinuous, as glTF requires; the topology-level mesh is recovered by welding positions". Use Hoppe's term *wedge* for per-corner attributes once, since the W condition already uses it.
- *Watertight:* "no boundary edges after welding identical positions" (see M3). Say "closed" if self-intersections remain.
- *Edge-manifold:* "every edge has exactly two incident faces". Also report vertex-manifoldness for the 24 raw meshes, since it is reported only for the companion.
- *"Mean Hausdorff"* is an oxymoron, since Hausdorff is a max. Use "mean and maximum symmetric surface distance (Metro-style sampling, N samples)" and give the sample count and how the two directions are combined.
- *Genus* on meshes with multiple components and self-intersections: state how it is computed (Euler characteristic per component?), or report holes/handles differently.
- *Faces vs. triangles:* both are used for the same thing. Pick "triangles" and keep "50k faces" only as the generator's UI label.
- *Pivot vs. origin:* use one.

**Units:** MiB is used consistently, which is good. State once that MiB = 2^20 bytes. "4 B/pixel" vs "byte/px" vs "B/pixel": unify. Unity's profiler reports "MB" that are actually MiB; say so in the consistency check.

**Number consistency:**
- Abstract "26 assets shipped" vs. 25 shipped (M10).
- "H1 holds" vs. pre-registered bound violated (M2).
- The pivot is "near, but not at, its horizontal centre (0.30 to 0.69 of the depth)". 0.30 is not "near". Data: x 0.435 to 0.576, z 0.295 to 0.692. Report both axes.
- B5 label `c21ea44` records "AI pivots are not at the feet", while B1 reports a vertical pivot fraction of 0.000 for all 24. Either the label refers to another frame or asset, or the note is wrong; reconcile.
- "six assets could not reach 6.25 percent at all" should be "within three passes".
- "23 of 24 ... in a single pass": correct per data. The stalled asset (`npc_rome_engineer`) also has the 9.7 percent max error in Table 2; say so in the caption, since otherwise W's worst case looks worse than S's.
- Shipped companion self-intersections are 9,868 vs. 19 raw. This is a striking number that is not reported.
- "Up to the shipped version (484)": 484 non-merge commits verified.
- "Over two months in 2026": first commit 2026-06-11, 87fdd16 2026-08-10. Consistent.

**Figures and tables:**
- Fig. 1: the x-axis is categorical but the values halve each step; label it as such or use a log2 axis. Medians only: add IQR bands or per-asset faint lines. The left-panel y-label "open edges after welding (median)" confuses because welding is also a condition; say "open edges in output (measured after position welding)".
- Fig. 2: good. Mark the sampled window (1.44 s) on the time axis and add the per-frame curve's min/max annotations.
- There is no image of any asset anywhere. Add one strip: raw NPC, glTF-frame front/back, S-vs-W companion crack close-up, UV layout of one asset. For a graphics venue this is expected.
- Table 1 could carry triangles, vertices and texture sizes per group (and the boss row's B2/B3 values).
- Table 2: add a column for the S + preserveboundary=True run (M5) and a "UV stretch / image error" column.
- acmart warnings: images lack descriptions (add `\Description{}` for accessibility; ACM checks this), and the affiliation has no city.

**Clarity for a graphics reader:**
- Section 5.4 explains the mechanism ("treats each seam as an open boundary and moves its two sides independently") only in prose. One schematic sentence or mini-figure (two wedges sharing a position; collapse moves one copy) would help.
- "Welding exact duplicates first, one call": name it (`meshing_remove_duplicate_vertices` in PyMeshLab) and state that per-corner UVs are kept as wedge attributes. "One call" is unhelpful without the call.
- Section 5.2 jumps forward to Section 5.4 for the cause. Consider moving simplification before hygiene, or adding a one-line explanation in 5.2.
- Grounding: "at game scale (10 m)": say whether 10 m is the height and how scale was applied in Blender.
- "BakeMesh returned two incompatible scalings for this rig (0.68 and 2.29 against a hover of about 0.9 bracketed in play)": opaque to anyone not in the commit history. Either explain in one more sentence or cut it to "an engine-side scale ambiguity we did not reproduce".

**Statistics:** a Wilson CI over 24 non-random assets from one prompt style implies sampling from a population of generator outputs. Either justify it ("if these 24 were a random draw from the service's output at this setting ...") or drop it and report counts.

## 5. Sentences that read as AI-style filler or are overstated (quote, then fix)

| Location | Text | Problem | Suggested fix |
|---|---|---|---|
| Abstract and Intro | "A real-time engine judges other things." / "A real-time engine judges a mesh on other things:" | Personification used twice as a rhetorical beat | "Engine readiness depends on different properties: ..." (say it once) |
| Intro | "where hand modelling would have taken weeks" | Unsupported estimate | Cut, or give a source or estimate basis |
| Intro | "The findings run against the expectations we wrote down." | Dramatic framing; also only partly true (see M2/M3) | "Three of the five pre-stated hypotheses were not supported." |
| Intro | "so this is a case study; what transfers is the checklist and how it was tested" | The checklist was not tested | "...; what may transfer is the checklist, which we derive here but have not validated on other projects" |
| Abstract | "The raw meshes are clean" | Contradicted by self-intersections in 24/24 and genus up to 361 | "The raw meshes are closed and edge-manifold (though every one self-intersects)" |
| Abstract | "facing away from the viewer" | Probably an importer effect (M1); props like a stupa have no front | Remove or restate per M1 |
| Abstract | "with half of each texture unused" | Coverage 48 to 68 percent; gutters are required | "with only 48 to 68 percent of each texture covered by UV charts" |
| 5.1 title | "every asset needs the same three corrections" | Fine, but one of the three may be an importer artefact | Adjust after M1 |
| 5.1 | "The only property a counting check could not see is the one that caused the first fix." | Hard to parse; also likely wrong after M1 | Delete, or "Facing cannot be read from the metadata alone; it caused the first fix." |
| 5.2 | "None of these showed up in play." | Absence of evidence; nobody looked | "We did not observe effects of these in play, but did not test for them (e.g. in baking or collision)." |
| 5.2 title | "the generator's meshes are clean; ours was not" | Overstated (M3) | "Raw meshes are closed and manifold; the simplified one is not" |
| 5.3 title | "the texture is the asset" | Slogan | "Texture memory dominates geometry memory" |
| 5.4 | "the output is a valid mesh with the requested face count, and it renders" | "Valid" contradicts 44k open edges | "the filter reports no error, returns the requested face count, and the result renders" |
| 5.6 title | "the bind pose lies, and any constant has a floor" | Anthropomorphic | "Bind-pose bounds misplace an animated character; a constant offset has a floor" |
| 5.5 | "Generated assets were a small part of the game's spatial trouble" | The keyword pattern was built around asset terms, and LEVEL includes purchased/procedural content, so the comparison is not like-for-like | "Within the matched commits, LEVEL labels outnumber ASSET labels 61 to 13." |
| Discussion | "The mesh was the easy part." | Slogan; see M3 | "Mesh topology caused no fixes." |
| Discussion | "the costliest defects, facing and grounding" | "Costliest" is not measured (no time or effort data); facing likely mislabelled | "the defects with the longest fix chains (grounding, five commits)" |
| Discussion | "Generated meshes partly reverse this." | Rhetorical hinge sentence | Merge with the next sentence: "Unlike the quiz bank, where counting found what inspection missed, here two of the defects needed a render or an animation evaluation." |
| Discussion | "the lesson is less 'inspect the generator' than 'inspect every step you add after it, and the explanation you wrote down for it'" | Aphorism; fine once, but the paper has several of these | Keep this one; cut the others above |
| Checklist item 2 | "most of the half-empty atlas can be dropped by downscaling or re-baking" | Downscaling does not remove empty space proportionally; only re-packing/re-baking does | "re-packing or re-baking the atlas can recover most of the unused area; downscaling reduces cost uniformly" |
| Authorship | "so that the numbers can be checked without trusting either" | "Either" is ambiguous (author/assistant?) | "without trusting the author or the assistant" |

## 6. Prioritised revisions (doable in about 1 day, no large new experiments)

1. **Resolve facing (M1).** Probe all 24 GLBs in the glTF frame, cite the glTF +Z-front / metre conventions, identify UniGLTF's Z inversion as the cause, and relabel the facing commits. Then update H5, the abstract, the Discussion and checklist item 1. (2 to 3 h)
2. **De-inflate "pre-registered" (M2).** Remove it from the subtitle; restate H1 as failed (23/24); add undisclosed deviations (is_fix, B3 "as stored", outputs); add an investigator-knowledge sentence; reconcile the "awaiting author sign-off" status; say that both held hypotheses were pilot-known. (1 h)
3. **Replace "clean" (M3) and fix the related sentence list in Section 5.** Report self-intersections and genus as findings and define terms. (1 h)
4. **Add a baseline column (M4).** Run B1 to B3 on the hand-made/licensed/purchased meshes already in the game and on the studio-pipeline boss. (2 to 3 h)
5. **Strengthen B4 (M5).** Add an S + preserveboundary=True run, an image-space or UV-stretch error for original/S/W on 3 to 4 assets, one figure showing the companion crack, and optionally one gltfpack/meshoptimizer run. Reframe novelty against Hoppe 1996 and Cohen et al. 1998. (3 to 4 h)
6. **Report all four E1 animations (M6)** in a small table; state sampling coverage; mention root-motion/root-transform import options. (1 h)
7. **Demote the memory consistency check to a footnote** or replace it with the actual imported texture format and size; clarify companion texture sizes (M7). (30 min)
8. **Fix related work (M9).** Add the Khronos 3D Commerce guidelines and glTF-Validator, Unity/Unreal import docs, atlas packing efficiency, and the attribute-discontinuity papers; cite or drop uncited bib entries. (1 to 2 h)
9. **Fix counts and wording** (26 vs 25 shipped, "shipped", "at all", pivot description, Table 2 caption, the table in Section 5 of this review) and add `\Description` to the figures. (1 h)
10. **Re-word the checklist as derived, not tested (M8).** If time remains, run the checklist script on the baseline meshes from item 4 to show its false-positive rate. (30 min to 2 h)
