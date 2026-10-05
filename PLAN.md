# Audit plan — written before the audit scripts are run

**Date:** 2026-10-05
**Object:** the image-to-3D generated meshes shipped in ChronoTraveler (game repo
commit 87fdd16), listed with SHA-256 in `data/manifest.json`:

| Group | n | Source | Notes |
|---|---|---|---|
| `npc` | 15 | Tencent Hunyuan 3D web, image-to-3D V3.1, "50k faces" preset, GLB | one front-view AI-drawn image per character; used as-is |
| `prop` | 9 | same pipeline | camels, horse, cart, stupa, milestone, goods |
| `companion_raw` | 1 | same pipeline, higher face preset | 497,850-face original of the companion fox |
| `companion_decimated` | 1 | `companion_raw` after UV-preserving QEM (pymeshlab, 3 rounds) | the OBJ actually shipped |
| `boss_studio` | 4 | Hunyuan 3D Studio "full pipeline": retopology, UV, texture, rig, 4 animations, FBX | same mesh in four FBX files |

All 24 GLBs in the game are byte-identical to the files downloaded from the
generator; nothing was edited before import. Corrections were applied at import
time by Unity editor tools (`NPCModelSetupTool`, `FinaleBossModelTool`) and at
run time by `GroundSnap`.

**Rule:** metrics, hypotheses and decision rules below are fixed before the audit
scripts are written and run. Anything changed afterwards goes into a
"deviations" section of the paper with the reason.

**Pilot disclosure.** While scoping this study (same day, before this plan), a
read-only survey parsed GLB headers and reported: triangle counts of
48,658–50,124; one primitive and one material per file; three 4096² textures per
file; `doubleSided: true`; heights of about 1 unit; a +90° X rotation on the root
node. Hypotheses that restate these observations (H1, part of H3) are therefore
descriptive confirmations, not tests. The geometry-hygiene, decimation and
failure-taxonomy results (H2, H4, H5) and the grounding study (E1) had not been
looked at.

## Question

Image-to-3D generators now deliver textured meshes in minutes, and their output
is judged on how it looks. A real-time engine judges it on other things: units,
axes, pivots, closed and manifold surfaces, triangle and texture budgets, and
whether it can be simplified. What does such an asset need before it is fit for
a shipped game, and which of those needs can be detected by counting before
import rather than discovered in play?

## Audits

### B1 — Conventions (glTF/FBX metadata and bounds, no geometry processing)
Per asset: node transform chain (rotation/scale on non-mesh nodes); up axis and
handedness implied after applying the node chain; bounding box in metres and
its largest extent; pivot position relative to the box (base centre? centroid?);
material flags (`doubleSided`, `alphaMode`, extensions in use); texture count,
pixel size, container format, and bytes; skin/animation presence.
- **H1 (descriptive):** every raw-pipeline asset is scale-normalised (largest
  extent within 0.9–1.2 units regardless of what it depicts), carries a
  non-identity root rotation, and is double-sided. Real-world size must be
  supplied downstream for every asset.

### B2 — Geometry hygiene (pymeshlab, after merging coincident vertices for topology only)
Per asset: connected components; non-manifold edges and vertices; boundary
(open) edges; zero-area / degenerate faces; duplicate faces; self-intersecting
faces; UV charts (islands) and UV-space coverage; vertex-to-triangle ratio as a
measure of seam splitting. Raw vertex buffers are also reported unmerged, since
that is what the engine uploads.
- **H2:** a majority of the 24 raw-pipeline assets fail at least one of
  {watertight, edge-manifold, single component}. Reported as counts with a
  Wilson 95% CI; per-check counts reported separately.

### B3 — Runtime cost estimates
Per asset: GPU geometry bytes (as uploaded: vertices × stride + indices);
texture bytes under three formats (RGBA8 uncompressed with full mip chain,
BC7 = 1 byte/px, BC1 = 0.5 byte/px, all ×4/3 for mips); disk bytes.
- **H3:** texture memory exceeds geometry memory by at least an order of
  magnitude for every raw-pipeline asset, under every format above. The
  "50k faces" setting users choose is not the cost that matters.

### B4 — Simplification floor
For each raw-pipeline asset, run pymeshlab quadric edge collapse with texture
(UV) preservation, boundary preservation off, quality threshold 0.3, at targets
of 50%, 25%, 12.5% and 6.25% of the original face count (single pass, then up
to 3 passes if the target is not reached, as the shipped companion pipeline did).
Record faces achieved and symmetric Hausdorff distance (max and mean, sampled,
as % of the bounding-box diagonal). Repeat without UV preservation as a control.
- **H4:** with UV preservation, a majority of assets cannot reach the 6.25%
  target (~3k faces) within 3 passes, while the no-UV control can; the gap is
  the cost of the generator's UV layout. The companion's shipped 82,829 faces
  (from 497,850) is the in-production instance of the same floor.

### B5 — Failure taxonomy from the game's history
Commits in the game repo (non-merge, up to 87fdd16) whose subject or body match
the case-insensitive pattern
`ground|float|hover|sink|clip|feet|pivot|scale|yaw|facing|rotation|magenta|winding|cull|collider|bounds|hunyuan|glb|fbx|decimat|poly|npc model|boss model|xuanji 3d|companion 3d`
are listed. Each is read and labelled:
- `ASSET` — the root cause is a property of a generated asset (B1–B3 territory);
- `ENGINE` — the root cause is an engine/tool behaviour that any asset would hit;
- `LEVEL` — level geometry / placement unrelated to generated assets;
- `OTHER` — matched the pattern but unrelated.
For `ASSET` commits we record which B1–B3 metric, if any, would have flagged the
property before import. Labelling is drafted by the AI assistant from the diff
and message and signed off by the author; ambiguous cases go to `OTHER` with a
note rather than being forced.
- **H5:** most `ASSET`-labelled fixes concern properties visible to B1/B2
  counting (scale, axis, pivot, sidedness, bounds), not appearance.

### E1 — Exploratory: grounding an animated generated character
The boss (studio pipeline, rigged) was mis-grounded five times in 26 minutes on
2026-07-11 (commits 9760126 → dc81a43). In Blender, evaluate the skinned mesh at
every frame of each of the four animations and record the true lowest vertex.
Compare the estimators the game tried: bind-pose bounds; single-frame minimum;
minimum over the first N frames (N = 10, as shipped); and the shipped constant
offset. Report each estimator's error against the per-frame truth.
Labelled exploratory: the engine-side scale ambiguity the game hit (two BakeMesh
readings, 0.68 and 2.29) is Unity-specific and is reported from the commit
record, not reproduced.

## What this plan does not claim
- One generator, one game, 24 + 2 meshes. No claim about image-to-3D in general.
- No frame-time measurements: the cost figures are memory and budget estimates,
  not profiler readings (the game's benchmarks did not isolate these assets).
- Visual quality is not scored.

## Outputs
`results/conventions.json`, `results/hygiene.json`, `results/cost.json`,
`results/decimation.json`, `results/history_labels.json`, `results/grounding.json`,
and `results/report.md` generated from them by `scripts/report.py`.
