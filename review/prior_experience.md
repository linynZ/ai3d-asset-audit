# Prior experience: what others already reported on our findings

Compiled 2026-10-05 for the Hunyuan 3D asset-audit paper. Every source below was
opened during this search (web page, PDF, GitHub API or arXiv/Crossref API) unless
marked otherwise. Quotes are verbatim from the opened source. "Strength" says how
much weight a source can carry: **strong** = official documentation, a
peer-reviewed paper, or primary source code; **medium** = a named practitioner with
concrete, checkable details, or a non-archival preprint; **weak** = vendor
marketing or anonymous/agent-written posts, kept only when they add a concrete data point.

Bib keys refer to `prior_experience.bib`. Keys already in `paper/references.bib` are
marked *(already cited)*.

Our findings, as referenced below:

- **F1** Raw meshes are watertight and edge-manifold.
- **F2** UVs: about 700–3,000 charts per asset and about 50% UV coverage.
- **F3** Three 4096² PBR maps per asset; texture memory is 40–50× the geometry in BC7.
- **F4** Assets arrive unit-normalised (largest extent about 1) and facing −Z.
- **F5** Texture-aware QEM on the seam-split vertex buffer from a glTF loader tears the mesh, because seams become open boundaries. Welding first is crack-free.
- **F6** A rigged generated boss hovers when grounded by its bind-pose bounds, because the idle animation lifts it. No constant offset can remove the idle bob (0.22 m floor). `BakeMesh` gave inconsistent scalings.
- **F7** Three of six asset fixes repaired bugs our own post-processing introduced.

---

## 0. Two things the paper must change

1. **"We found no independent audit…" (related.tex) is no longer safe.**
   Begemann & Hutson (2026) published a practice-led evaluation of Meshy 6 +
   Hunyuan 3D assets for a game-ready environment. They report fragmented UVs and
   texture loss during decimation (§1.1). Cite it and narrow the claim. Ours is an
   audit of assets *shipped in a finished game* against a *pre-registered plan*, with
   per-asset measurements. Theirs is a comparative case study of building one
   scene.
2. **"The facing direction … is not encoded anywhere" (results.tex l.22) is too strong.**
   The glTF 2.0 spec does state a convention: "the front side of a glTF asset
   faces +Z" (§3.1). A −Z front, if it is measured in glTF coordinates (method.tex
   says it is), *violates the format's stated convention*. That is a sharper and
   more citable finding than "not encoded". Suggested rewording below.

---

## 1. Practitioner and peer experience with AI-generated 3D in games

### 1.1 Begemann & Hutson 2026, "Prompted Props, Human Pipelines" (strength: medium, peer-reviewed but low-profile journal)
- URL: https://zenodo.org/records/21064847 (also https://digitalcommons.lindenwood.edu/faculty-research-papers/813/)
- Andrew Begemann (Game Design) and James Hutson, Lindenwood University. *Int. J. Human Research and Social Science Studies* 3(6):647–661, 30 June 2026. DOI 10.5281/zenodo.21064847.
- What it says: a practice-led comparative case study. One stylised tavern scene was built twice, by hand in Blender and with Meshy 6 + Hunyuan 3D. Hand-made: 716.06 min, 123 objects, 293,828 triangles. AI-assisted: 238 min, 103 objects, **32,781,505 triangles**. They list the problems: "dense triangulated geometry, fragmented UV maps, inconsistent prompt adherence, material-editing constraints, clipping during placement, and loss of texture integrity during attempted decimation."
- Relation:
  - **Agrees** with F2: fragmented UVs.
  - **Agrees** with F5: decimation damages textured generated assets. They do not diagnose a cause; we give one (seam-split buffer, fixed by welding).
  - **Differs in method**: theirs is one scene, not pre-registered, not shipped, and has no per-asset geometry or memory measurements.
  - **We didn't know**: this is the closest prior work. It also contains a Hunyuan triangle-count data point.
- Suggested sentence: *"Begemann and Hutson [begemann2026prompted] rebuilt one game environment with Meshy 6 and Hunyuan 3D and reported fragmented UV maps and loss of texture integrity under decimation; we measure these properties per asset in a shipped game and trace the decimation damage to a specific cause."*

### 1.2 Liz Edwards via Game Developer, "How devs can spot AI-generated 3D models" (strength: medium, named veteran 3D artist, trade press)
- URL: https://www.gamedeveloper.com/art/how-devs-can-spot-ai-generated-3d-models (direct fetch was blocked; read through the Google-translate proxy of the same URL)
- Bryant Francis (Senior Editor), 5 Nov 2024. Source: 3D artist Liz Edwards on Bluesky.
- What it says:
  - The UVs are "automatically unwrapped, leaving a jumbled mess in their wake".
  - The textures carry "baked-in lighting".
  - Wireframes are a "dense automesh".
  - AI crates on Fab had about 50,000 triangles, against roughly 500 for a game crate.
- Relation: **agrees** with F2. It is the practitioner version of our chart counts. It gives no numbers on coverage.
- Suggested sentence: *"Practitioners have described the automatic UVs of generated models as 'a jumbled mess' [edwards2024spot]; we quantify this as 700–3,000 charts and about half the texture unused."*

### 1.3 Galashots, galaquest-public PR #207, "decimate_gear v2: weld seams, decimate, fresh UVs, bake from source (fixes seam cracks)" (strength: weak–medium, public repo, AI-agent-authored PR, but concrete and reproducible)
- URL: https://github.com/Galashots/galaquest-public/pull/207. Opened 2026-09-23, merged the same day. Read via the GitHub API.
- What it says:
  - "Stop gear reduction from **cracking Meshy assets**."
  - "The glTF import splits vertices at every UV seam, and v1's UV-delimited collapse reduced each side separately, so the seams pulled apart. Re-baking the texture alone did not fix it."
  - Fix: "weld the seam-split vertices (1e-5 × the largest dimension); collapse to the budget, without UV delimit; unwrap a fresh UV set…; bake the base colour from the full-resolution source."
  - Helmet 311,626 → 2,000 tris; sword 68,004 → 1,500 tris.
- Relation: **agrees exactly** with F5. The mechanism is the same and so is the fix (weld first), here on Meshy assets in Blender, independently and about two weeks before this review. F5's mechanism is therefore **not new as a practitioner observation**. What remains ours is measuring it (2,433 pieces against 0 after welding, at matched budgets) and linking it to the glTF storage rule.
- Suggested sentence: *"An independent open-source game project hit the same failure on Meshy assets in Blender and adopted the same fix, welding seam-split vertices before collapse [galashots2026weld]."*

### 1.4 raydeStar, reference-asset-compiler (strength: weak–medium, named GitHub author, detailed README)
- URL: https://github.com/raydeStar/reference-asset-compiler. Created 2026-08-31, last push 2026-10-04.
- It is a pipeline from one concept image to a UE5 character, using "Hunyuan3D geometry and PBR, Blender retopo/UV/rig". From the README:
  - "The 2048 Hunyuan atlas spreads to roughly 20 texels/cm² on a Manny-scale body, and Smart Project produces confetti islands."
  - "Blender's FBX export leaves a 100x scale on the root bone with bone offsets in metres."
  - "retargeting … cannot fix roll about a bone axis, so hands with a different palm orientation twist."
- Relation:
  - **Agrees** with F2: low effective texel density and fragmented islands.
  - **Agrees** with F6 in kind: rig scale conventions break downstream tools, like our `BakeMesh` scaling inconsistency.
- Suggested use: a footnote-level corroboration of F2/F6, not a main citation.

### 1.5 SEELE AI, "Optimize Hunyuan 3D Models for Unity" (strength: weak, vendor page, no author or date)
- URL: https://www.seeles.ai/features/tools/optimize-hunyuan-3d-models-for-unity
- What it says: "A model can look correct in a generator preview but land too small, too large, rotated, off-center, or hard to place in a Unity scene." It tells readers to "Inspect scale, pivot, orientation, polygon density, texture references, material slots, file size…".
- Relation: **agrees** with F4 and with our checklist in general. That scale, pivot and orientation need checking is folk knowledge. Do not present the checklist *items* as new; present the *measured values* and the *ordering by what each check caught* as the contribution.
- Use: optional. Cite as "vendor guidance already lists…" if useful.

### 1.6 Hunyuan3D-2.1 open-source code (strength: strong, primary source; code read 2026-10-05)
- URL: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
- `hy3dpaint/textureGenPipeline.py`: `self.render_size = 1024 * 2` and `self.texture_size = 1024 * 4`. The **default texture is 4096²**.
- `hy3dpaint/utils/uvwrap_utils.py`: UVs come from `xatlas.parametrize(mesh.vertices, mesh.faces)` with default options, followed by `mesh.vertices = mesh.vertices[vmapping]`. Vertices are **duplicated at every chart boundary**, so the shipped mesh is seam-split by construction.
- xatlas defaults (`xatlas.h`): `bruteForce = false` ("If false, use random chart placement") and `maxCost = 2.0f` ("Lower values result in more charts").
- `hy3dshape/postprocessors.py`: `reduce_face` runs `meshing_decimation_quadric_edge_collapse` with `preserveboundary=True, preservenormal=True, preservetopology=True` **on the untextured shape, before UV unwrapping**.
- Shape extraction: `box_v=1.01` (marching cubes inside a fixed cube).
- Relation:
  - **Explains** F3: 4096² is the pipeline default.
  - **Plausibly explains** F2: default xatlas on a dense marching-cubes surface, with random placement.
  - **Explains** F5's precondition: the shipped mesh is seam-split.
  - **Shows** that Tencent's own pipeline simplifies *before* UVs exist, which avoids the trap entirely.
  - Our assets came from the commercial service, so present this as "the open-source pipeline does X" and not as proof of what the service does.
- Suggested sentence: *"In the open-source release, textures default to 4096² and UVs come from xatlas with default settings after the shape is simplified [hunyuan21code]; simplifying after unwrapping, as we did, reverses that order."*

### 1.7 Hunyuan3D Studio paper (Lei et al. 2025) *(already cited as lei2025hunyuan3dstudio)* (strength: medium, arXiv tech report)
- URL: https://arxiv.org/abs/2509.12815 (v1, 16 Sep 2025)
- What it says:
  - "XAtlas generates over-fragmented cuts". Their SeamGPT is evaluated with a user study of "20 professional 3D artists" on boundary quality and editability.
  - Generated shapes "typically consist of a huge amount of messy triangles and are hard to be directly applied in downstream applications (e.g., UV segmentation and rigging)".
  - It has a section "4K Material Map Generation".
- Relation: **agrees** with F2 and F3, and comes from the generator's own authors. Use it to say "the developers themselves identify xatlas fragmentation as a problem".
- Suggested sentence: *"Hunyuan's own developers report that xatlas 'generates over-fragmented cuts' [lei2025hunyuan3dstudio]; our audit shows what that costs in texture memory for assets that ship."*

### 1.8 Hunyuan3D 2.1 paper *(already cited as hunyuan2025hunyuan3d21)* (strength: medium, arXiv tech report)
- URL: https://arxiv.org/abs/2506.15442 (18 Jun 2025)
- What it says:
  - Training data get "uniform scaling to fit the object within a unit cube centered at the origin, preserving aspect ratios".
  - Meshes come from marching cubes on an SDF, which produces watertight surfaces.
- Relation: **explains** F4's unit scale, which follows from training normalisation, and F1, since an isosurface of an SDF is watertight by construction. F1 is therefore **expected, not surprising**, for this generator. Say so.
- Suggested sentence: *"Both properties follow from the generator's design: training shapes are normalised to a unit cube [hunyuan2025hunyuan3d21], and surfaces are extracted as isosurfaces, which are closed."*

---

## 2. Simplifying meshes with UV seams (F5)

### 2.1 Hoppe 1999, "New quadric metric for simplifying meshes with appearance attributes" *(already cited)* (strong)
- https://hhoppe.com/proj/newqem/. PDF read.
- "Meshes often have attribute discontinuities, such as surface creases and material boundaries, which require multiple attribute vectors per vertex. We show that a wedge-based mesh data structure captures such discontinuities efficiently…" In Section 5: "A vertex is partitioned into k ≥ 1 wedges, each wedge w_i having its own attribute vector".
- Relation: this is the **textbook statement** behind F5. A seam is one vertex with several wedges. A split buffer turns it into several vertices and an open boundary. F5 is a rediscovery of what happens when the wedge structure is lost.
- Suggested sentence: *"Appearance-aware QEM assumes a wedge structure in which a seam vertex carries several attribute vectors [hoppe1999newqem]; a glTF loader instead returns one vertex per wedge, so to the simplifier every seam is a hole."*

### 2.2 Garland & Heckbert 1998 *(already cited)* (strong)
- DOI 10.1109/VISUAL.1998.745312. Verified on Crossref: *Proc. Visualization '98*, pp. 263–269.
- PyMeshLab's texture-aware filter documents itself as based on this paper (§2.4).

### 2.3 meshoptimizer documentation and maintainer answer (strong, official docs by Arseny Kapoulkine)
- https://meshoptimizer.org/ (same text as the GitHub README):
  - "The algorithm follows the topology of the original mesh in an attempt to preserve attribute seams, borders and overall appearance."
  - "For meshes with inconsistent topology or many seams, such as faceted meshes, it can result in simplifier getting 'stuck' … Therefore it's critical that identical vertices are 'welded' together, that is, the input vertex buffer does not contain duplicates."
  - "`meshopt_SimplifyLockBorder` restricts the simplifier from collapsing edges that are on the border of the mesh."
- https://github.com/zeux/meshoptimizer/discussions/693 (zeux, 22 May 2024): a seam vertex is detected when "the edge was closed from the opposite side by a triangle with same positions but different indices". A border vertex has open edges.
- Relation:
  - **Agrees** with F5 and states the weld-first rule outright.
  - **Nuance**: meshoptimizer *does* accept split buffers. It reconstructs seams from position equality and only gets "stuck", without tearing. A tool that treats split edges as true borders (MeshLab after per-vertex→per-wedge conversion) tears instead. So the failure depends on the tool; it is not universal. Name the tool in the paper.
- Suggested sentence: *"Seam-aware simplifiers such as meshoptimizer infer seams by matching positions and still advise that 'identical vertices are welded' [meshopt]; the MeshLab filter we used does not, and treats each split edge as a border."*

### 2.4 PyMeshLab filter documentation (strong, official docs)
- https://pymeshlab.readthedocs.io/en/latest/filter_list.html (source: `docs/filter_list.rst` in cnr-isti-vclab/PyMeshLab)
- `meshing_decimation_quadric_edge_collapse_with_texture`: "Simplify a textured mesh using a Quadric based Edge Collapse Strategy preserving UV parametrization. Inspired in the QSLIM … See: M. Garland and P. Heckbert. Simplifying Surfaces with Color and Texture using Quadric Error Metrics". Parameters include `preserveboundary : bool = False` ("The simplification process tries not to destroy mesh boundaries") and `boundaryweight`.
- `compute_texcoord_transfer_vertex_to_wedge` ("Convert PerVertex UV into PerWedge UV"): "Converts per Vertex Texture Coordinates to per Wedge Texture Coordinates. **It does not merge superfluous vertices...**"
- `compute_texcoord_transfer_wedge_to_vertex`: "…splitting vertices with not coherent Wedge coordinates."
- `meshing_merge_close_vertices`: "Like a unify duplicated vertices but with some tolerance."
- Relation: **this documents the trap directly.** The usual path (load a glTF, convert per-vertex UVs to per-wedge, simplify with texture) leaves the split vertices in place. `preserveboundary` defaults to False and is only a "tries not to" weight. F5's mechanism is therefore *derivable from the documentation*; what we add is measuring the consequence. Check which settings we actually used and report them.
- Suggested sentence: *"MeshLab's conversion to per-wedge texture coordinates 'does not merge superfluous vertices' [pymeshlabdocs], so unless vertices are merged first the texture-aware collapse sees every seam as a mesh boundary."*

### 2.5 Blender manual, Decimate modifier (strong, official docs; source .rst read from projects.blender.org)
- Collapse mode exposes Ratio, Symmetry, Triangulate and Vertex Group, but **no delimit**. Delimit (Normal / Material / Seam / Sharp / UVs) exists only in Planar mode, e.g. "Seam: Does not dissolve edges marked as UV Seams."
- Relation: background. Blender's general-purpose collapse has no seam awareness, which is why practitioners (§1.3) weld and then re-bake. Optional citation.

### 2.6 Liu, Ferguson, Jacobson & Gingold 2017, "Seamless" (strong, TOG / SIGGRAPH Asia)
- DOI 10.1145/3130800.3130897, TOG 36(6). Project: https://cragl.cs.gmu.edu/seamless/. Code README (github.com/songrun/SeamAwareDecimater): "simplifies a mesh while preserving its UV's boundary", noting that the Garland–Heckbert approach "do[es] not preserve seams precisely, leading to artifacts in the texture."
- Relation: the academic remedy for keeping the *same texture* across simplification with seams intact. Our weld-first fix keeps topology but still needs seam-aware collapse or a re-bake to keep the texture exact. Cite this as the principled alternative.

### 2.7 Liu, Zhang & Yuksel 2025, "Simplifying Textured Triangle Meshes in the Wild" (strong, TOG 44(6))
- DOI 10.1145/3763277. arXiv 2409.15458.
- "Instead of following existing strategies to preserve UVs, we adopt a novel perspective which focuses on computing mesh correspondences throughout the decimation, independent of the UV layout". It "guarantees to avoid common problems in textured mesh simplification, including the prevalent problem of texture bleeding."
- Relation: the state of the art for textured simplification of messy meshes. Cite it as what a production pipeline could use instead of MeshLab.

### 2.8 Bhosikar et al. 2026, "Fast and Robust Mesh Simplification for Generated and Real-World 3D Assets" (FA-QEM) (medium, arXiv preprint)
- https://arxiv.org/abs/2605.14029 (13 May 2026)
- Targets "dense, noisy, and often non-manifold meshes" from 3D generation and tests on Hunyuan3D 2.0 outputs. Implementation: "Pre-emptive Vertex Merging: Before simplification, our mesh loading process includes a standard pre-processing step that merges all vertices that are closer than a small absolute tolerance of 1e-6." It also claims to "resolve issues at UV seams" by not relying on the original UV layout.
- Relation:
  - **Agrees** with F5: they call welding "standard pre-processing" for generated assets.
  - **Differs** on F1: they describe generated meshes as "often non-manifold". Our raw Hunyuan outputs are watertight and manifold *after welding*, so state that F1 is measured after the weld.
- Suggested sentence: *"Recent simplifiers for generated assets merge coincident vertices as a 'standard pre-processing step' [bhosikar2026faqem]; our contribution is to show what is lost when this step is skipped."*

---

## 3. glTF stores split vertices (F5 precondition) and conventions (F4)

### 3.1 Khronos glTF 2.0 Specification (strong) *(already cited as khronos2021gltf)*
- https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html. Source `Specification.adoc` read from KhronosGroup/glTF.
- §3.4 (Coordinate System and Units): "glTF uses a right-handed coordinate system. glTF defines +Y as up; **the front side of a glTF asset faces +Z**, the left side of a glTF asset faces +X. … The units for all linear distances are meters."
- Indexed-geometry implementation note: "If there are multiple vertex attributes, the same index values are used for all of them. For example, it is not possible to specify separate index values for positions and normals, so representing a cube made of twelve triangles with positions and flat normals would require 24 unique index values."
- Relation:
  - **F5**: the split buffer is *required by the format* and is not loader behaviour. Cite this.
  - **F4 (facing)**: the spec defines the front as +Z. A −Z front in glTF coordinates **contradicts the stated convention**. That is a stronger statement than "not encoded anywhere".
  - **F4 (scale)**: the spec says units are metres, so a ~1-unit asset claims to be ~1 m. Scale normalisation is format-legal but semantically wrong for most objects.
- Suggested rewording of results.tex l.22: *"…real-world size must come from outside (glTF declares units to be metres [khronos2021gltf], so every asset claims to be about 1 m tall), and the facing direction is −Z, the opposite of glTF's stated convention that 'the front side of a glTF asset faces +Z' [khronos2021gltf]."*
- **Check before writing**: confirm that the −Z observation was made in glTF coordinates (method.tex says "rendered in glTF coordinates from +Z and −Z"), and not after an importer's handedness flip.

### 3.2 Khronos glTF-Blender-IO documentation, importer option "Merge Vertices" (strong, official Khronos-maintained docs)
- Source: https://github.com/KhronosGroup/glTF-Blender-IO/blob/main/docs/blender_docs/scene_gltf2.rst (published in the Blender manual, "glTF 2.0" add-on page).
- "Merge Vertices: **The glTF format requires discontinuous normals, UVs, and other vertex attributes to be stored as separate vertices**, as required for rendering on typical graphics hardware. This option attempts to combine co-located vertices where possible. Currently cannot combine verts with different normals."
- Exporter side: "Discontinuous UVs and flat-shaded edges may result in moderately higher vertex counts in glTF compared to Blender, as such vertices are separated for export."
- Relation: **agrees** with F5 and is the most quotable official one-liner. Note also that this weld option is **off by default** in Blender. That is the same trap we fell into, in another tool.
- Suggested sentence: *"The format requires 'discontinuous normals, UVs, and other vertex attributes to be stored as separate vertices' [khronos_blenderio]; Blender's importer offers to merge them, but only as an option."*

---

## 4. Texture memory and UV utilisation (F2, F3)

### 4.1 Wang et al. 2025, PartUV (strong, SIGGRAPH Asia 2025)
- DOI 10.1145/3757377.3763843. arXiv 2511.16659.
- On AI-generated meshes: "Such meshes, typically extracted from neural-field isosurfaces (e.g., via marching cubes), tend to have bumpy surfaces, many small triangles, and poor geometric quality … existing methods may time-out or return extremely fragmented atlases in which a single chart holds only one or a handful of triangles. This extreme fragmentation hampers texture painting and editing, introduces texture-bleed and baking or rendering artifacts at chart boundaries…"
- Table, Trellis set (114 AI-generated meshes), charts mean / median:
  - **xatlas: 1,541.6 / 895.0**
  - Blender: 3,352.9 / 1,957.0
  - PartUV: 568.7 / 233.5
- Relation: **agrees closely** with F2's chart counts. Our 700–3,000 brackets their xatlas median and mean. Chart over-fragmentation of generated meshes is **known and quantified**. PartUV does not report *coverage or texture-memory waste*, so our ~50% coverage and memory framing remain new.
- Suggested sentence: *"Our chart counts (700–3,000) match those PartUV reports for xatlas on AI-generated meshes (median 895, mean 1,542) [wang2025partuv]; what has not been reported is how much of the texture those charts leave empty, and what that costs in memory."*

### 4.2 Maggiordomo, Cignoni & Tarini 2021, "Texture Defragmentation for Photo-Reconstructed 3D Models" (strong, CGF 40(2):65–78, Eurographics 2021)
- DOI 10.1111/cgf.142615.
- "…their underlying parametrization typically falls short of many practical requirements, particularly exhibiting excessive fragmentation and consequent problems." The method improves an existing UV map without full re-parametrisation, and is available in MeshLab as "texmap defragmentation".
- Relation: photogrammetry had the **same fragmentation problem** before generative 3D. It is a ready-made remedy that keeps the original texels. Worth a sentence in the discussion ("prior art for repair").

### 4.3 Limper, Vining & Sheffer 2018, "Box Cutter" (strong, TOG 37(4))
- DOI 10.1145/3197517.3201328.
- Defines packing efficiency as "the ratio between the areas of the packed atlas and its bounding box" and notes that it "significantly impacts downstream applications".
- Relation: gives a citable definition for our "UV coverage" metric. Use it to name our metric "packing efficiency" in the standard sense, or say how ours differs.

### 4.4 xatlas header documentation (strong, primary source) *(xatlas already cited as young2018xatlas)*
- https://github.com/jpcy/xatlas/blob/master/source/xatlas/xatlas.h
- `float *utilization; // Normalized atlas texel utilization array. E.g. a value of 0.8 means 20% empty space.` Other comments: `bruteForce`: "Slower, but gives the best result. If false, use random chart placement." `padding = 0`.
- Relation: xatlas computes the same utilisation metric we measure. Our ~0.5 can be stated in xatlas's own terms. The defaults explain part of the waste.

### 4.5 Unity, "Art optimization tips for mobile game developers, part 1" (strong-ish, official Unity guidance, no date)
- https://unity.com/how-to/mobile-game-optimization-tips-part-1
- "**Most of your memory will likely go to textures**, so the import settings here are critical." On Max Size: "Use the minimum settings that produce visually acceptable results. This is nondestructive and can quickly reduce your texture memory."
- Relation: **agrees** with F3. That textures dominate memory is standard engine advice and should not be presented as a discovery. Our contribution is the *measured ratio* (40–50×) for generated assets and the fact that half of it is empty texels.

### 4.6 Android Developers, "Textures" (strong, official Google docs, updated 2026-02-26)
- https://developer.android.com/games/optimize/textures
- "The additional mipmap levels increase the memory footprint of a texture by 33%." Also: "when using a diffuse texture of 1024x1024, reducing the roughness or metallic map texture to 512x512 may be possible with only a minimal impact on image quality."
- Relation: supports a recommendation that the three 4096² maps need not share a resolution. The metallic/roughness maps are the first candidates for downsizing.

### 4.7 BeamNG documentation, "Texture Streaming, Texture Quality and Performance" (medium–strong, official studio docs, no author)
- https://documentation.beamng.com/modding/materials/texture_streaming/ (last modified 23 Jul 2026)
- "BC7 uses about 1 byte per pixel … a 4096x4096 texture with a full mip chain requires roughly: 4096 x 4096 x 4/3 = ~21 MiB."
- Relation: an independent check of our arithmetic (three maps ≈ 64 MiB with mips). Together with Microsoft's BC7 spec ("fixed block size of 16 bytes (128 bits) and a fixed tile size of 4x4 texels") *(already cited as microsoft_bc7)*.

### 4.8 Denys Zadoienyi, "UV Unwrapping for Games: Best Practices for AAA Pipelines" (weak, single practitioner blog, updated 10 Jun 2026)
- https://nastyrodent.com/uv-unwrapping-for-games/
- "for a 2048 × 2048 texture, a minimum of 4–8 texels of padding between islands is typically required". Its tiers put background props at 512–1K and hero characters at 4K.
- Relation: with 700–3,000 charts, padding alone eats a large share of a 4096² atlas. This is a useful back-of-envelope point. **No reliable industry source for a "70–85% utilisation target" was found.** Search results attributed such numbers to blogs that could not be opened or verified, so do **not** cite a utilisation target figure.

---

## 5. Grounding animated characters (F6)

### 5.1 Unity Manual, "Root Motion – how it works" (strong, official)
- https://docs.unity3d.com/Manual/RootMotion.html
- "There is also a Feet option that is very convenient for AnimationClips that change height (Bake Into Pose disabled). **When using Feet the Root Transform Position Y will match the lowest foot Y for all frames. Thus the blending point always remains around the feet which prevents floating problem** when blending or transitioning."
- Class reference (https://docs.unity3d.com/Manual/class-AnimationClip.html): "Feet: Keep feet aligned with the root transform position. **Only available for the Humanoid Animation Type.**"
- Relation:
  - **Agrees** with F6: Unity documents a "floating problem" and a per-frame remedy that tracks the lowest foot. A per-frame solution is the standard answer.
  - **Partly explains** why the problem hit us: the option exists only for Humanoid rigs. A generated boss imported as Generic gets no such help. Check the boss's Animation Type and say so.
  - Our "any constant has a floor equal to the bob" is the quantitative version of why Unity offers a per-frame Feet mode at all.
- Suggested sentence: *"Unity ships a per-frame fix for this 'floating problem', aligning the root with the lowest foot on every frame, but only for Humanoid rigs [unity_rootmotion]; our generated boss, a Generic rig, gets no such help."* (Verify the rig type first.)

### 5.2 Unity Scripting Reference, `Renderer.localBounds` (strong) *(already cited as unity_localbounds; quote it precisely)*
- https://docs.unity3d.com/ScriptReference/Renderer-localBounds.html
- "For a SkinnedMeshRenderer, default local bounds are precomputed based on animations associated with that model, which means that the bounding box might be much bigger than the mesh itself. When SkinnedMeshRenderer.updateWhenOffscreen is enabled, Unity recomputes the local bounds every frame."
- Relation: **nuance for F6.** Our text says engines expose bounds "not recomputed from the current pose". The doc says they are precomputed *from the animations* (so possibly larger than bind pose) and *are* recomputed every frame when `updateWhenOffscreen` is on. Make sure the paper's "bind-pose bounds" refers to `sharedMesh.bounds` (mesh data) and not to `Renderer.bounds`, and mention the `updateWhenOffscreen` alternative.

### 5.3 Unity Scripting Reference, `SkinnedMeshRenderer.BakeMesh` (strong) *(already cited as unity_bakemesh)*
- https://docs.unity3d.com/ScriptReference/SkinnedMeshRenderer.BakeMesh.html
- "useScale: Whether to compensate for the SkinnedMeshRenderer's Transform scale. If true, the baked Mesh is the same size as the original. If false, the baked Mesh matches the scaling of the SkinnedMeshRenderer's Transform component. **The default value is false.**" Also: "The vertices are relative to the SkinnedMeshRenderer Transform component. This function always compensates for the position and rotation values…"
- Relation: our two incompatible scalings (0.68 against 2.29) are probably the `useScale` default interacting with the rig's non-unit root scale (cf. §1.4's "100x scale on the root bone"). Check whether the call passed `useScale` and say which. If not, report it as an unexplained engine/rig interaction. **We found no report of this specific failure.**

### 5.4 Kovar, Schreiner & Gleicher 2002, footskate cleanup *(already cited)* (strong)
- Already used correctly as the per-frame foot-contact reference.

### 5.5 Auto-rig floating and sliding reports (weak; not citable)
- Many Unity forum and YouTube answers about Mixamo characters floating give the same fix (Root Transform Position (Y) → Feet, Foot IK). The meshtint.com tutorial and the strayspark.studio "AI Auto-Rigging Showdown 2026" page (which reportedly measured Meshy hip-pivot offsets of 5–15 cm) **could not be opened** (TLS/403). They are omitted from the bib. **We found no verifiable report of an AI-rigged generated character hovering because its idle animation lifts it.** The specific F6 mechanism (bind pose grounded, idle lifts) looks unreported.

---

## 6. Peer academic work on generated assets for downstream use

### 6.1 Wu et al. 2026, "From Visual Synthesis to Interactive Worlds: Toward Production-Ready 3D Asset Generation" (medium, arXiv survey)
- https://arxiv.org/abs/2604.23629 (v2, 26 Apr 2026). Authors: Jiafeng Wu, Zhuofan Lou, Jian Liu, Dazhao Du, Chunchao Guo, Song Guo.
- "From the production-pipeline perspective, the most critical yet neglected evaluation dimension is whether a generated asset can be used in a downstream engine or tool. … UV parameterization quality includes stretch and angular distortion, seam visibility, chart packing efficiency, and overlap detection—metrics that are well established in geometry processing but **rarely reported in generative papers**." Also: "Topology quality—manifoldness, watertightness, genus correctness, quad ratio, edge flow alignment—is essential for production but **almost never quantified**." And: "Perhaps the most operationally relevant test is engine import success…"
- Relation: **strongly supports our motivation.** A 2026 survey states that the exact metrics we measure are rarely reported. Cite it in the introduction to justify the audit. It replaces our weaker "we searched arXiv and found nothing".
- Suggested sentence: *"A recent survey of production-ready 3D generation notes that packing efficiency, manifoldness and watertightness are 'rarely reported' or 'almost never quantified' for generated assets [wu2026productionready]; we report them for every asset a shipped game contains."*

### 6.2 Zhang 2026, Cyc3D (medium, arXiv)
- https://arxiv.org/abs/2608.28080 (28 Aug 2026). Its benchmark adds "mesh discretization and efficiency, and UV parameterization quality" to image-to-3D evaluation.
- Relation: a concurrent benchmark moving the same way, measuring usability in a lab. Ours measures it in a shipped product. One-line mention in related work.

### 6.3 Wang et al. 2026, AssetGen (Meta) (medium, arXiv)
- https://arxiv.org/abs/2605.26137 (22 May 2026). "…a high-quality mesh with baked normals, a color texture, and a controlled polygon budget suitable for real-time rendering, including mobile use cases" and "a fast parallel UV unwrapping".
- Relation: shows generator authors now treat budgets and UVs as design goals, which supports our point that they matter. Optional.

### 6.4 Panchanadikar & Freeman 2024, "I'm a Solo Developer but AI is My New Ill-Informed Co-Worker" (strong, PACM HCI 8 CHI PLAY, Art. 317)
- DOI 10.1145/3677082. A qualitative analysis of 3,091 posts and comments from indie-developer subreddits and Facebook groups.
- Relation: context for our solo-developer setting. Indie developers already describe generative AI as an "ill-informed co-worker". It does not measure 3D assets. Cite in the introduction for the solo or indie framing.

### 6.5 Ternar et al. 2026, "Generative AI in Game Development: A Qualitative Research Synthesis" (strong, CHI '26)
- DOI 10.1145/3772318.3791206. A meta-ethnography of 10 qualitative studies (2020–2025).
- Relation: the HCI evidence on developer practice is qualitative. Our audit adds artefact-level measurement. One sentence.

### 6.6 Yin et al. 2011, "How do fixes become bugs?" (strong, ESEC/FSE '11, pp. 26–36)
- DOI 10.1145/2025113.2025121. Abstract (as quoted on the Semantic Scholar/ResearchGate listing; the ACM page was not accessible): "At least 14.8%–24.4% of sampled fixes for post-release bugs in large OSes … are incorrect".
- Relation: F7 ("3 of 6 fixes repaired our own processing") has a well-known software-engineering analogue. The *general* phenomenon that fixes and tooling introduce defects is known. What is new is seeing it in an AI-asset import pipeline, where half the fixes were self-inflicted. Use it to frame F7 and not to claim surprise.
- Suggested sentence: *"That fixes and tooling introduce defects is well established in software engineering [yin2011fixes]; in our asset pipeline it accounted for half of all asset fixes."*

### 6.7 ArtUV (Chen et al. 2025, arXiv 2509.20710) and SeamGen (Xu et al. 2026, arXiv 2607.12379) (medium)
- ArtUV: "existing UV unwrapping methods struggle with time-consuming, fragmentation, lack of semanticity, and irregular UV islands." SeamGen: automatic seams "often result[] in layouts that deviate from artist-preferred seam patterns and practical production requirements."
- Relation: active research on the F2 problem. Mention in passing ("learned seam placement is an active remedy").

---

## 7. Summary table

| Finding | Already known? | Best prior sources | What stays ours |
|---|---|---|---|
| F1 watertight/manifold | Expected from SDF + marching cubes; other generators (TRELLIS) are reported as noisy or non-manifold | hunyuan2025hunyuan3d21; wang2025partuv; bhosikar2026faqem (contrast) | The measurement on shipped commercial output; the contrast with "generated = messy" |
| F2 700–3,000 charts | **Known and quantified** (xatlas median 895 on AI meshes) | wang2025partuv; lei2025hunyuan3dstudio; edwards2024spot; begemann2026prompted | ~50% coverage, i.e. how much texture is empty; not found reported |
| F3 4096²×3, 40–50× geometry | Textures dominating memory is standard advice; 4096² is the generator default | unity_mobileart; hunyuan21code; android_textures | The measured ratio for generated assets, combined with 50% unused texels |
| F4 unit scale | Follows from training normalisation; vendors warn about scale | hunyuan2025hunyuan3d21; seele_hunyuanunity; khronos2021gltf (metres) | Measured distribution (0.9–1.2) |
| F4 −Z front | glTF says front = +Z; **no report found that Hunyuan violates it** | khronos2021gltf | Looks new; reword as a violation of the stated convention |
| F5 seam-split QEM tears, weld fixes | **Known**: format rule (Khronos), weld-first rule (meshoptimizer), wedge theory (Hoppe), same bug and fix on Meshy assets (Galashots, Sep 2026), decimation damage (Begemann) | khronos2021gltf; khronos_blenderio; meshopt; hoppe1999newqem; pymeshlabdocs; galashots2026weld | Quantified damage (2,433 pieces against 0) at matched budgets; tool-specific diagnosis |
| F6 bind-pose grounding hovers | The floating problem and per-frame Feet fix are documented by Unity (Humanoid only); foot IK is standard | unity_rootmotion; kovar2002footskate; unity_localbounds | The quantified floor (bob amplitude) for any constant; the generated Generic-rig case; the `BakeMesh` scaling inconsistency (not found reported) |
| F7 3/6 fixes self-inflicted | The general phenomenon is known in SE | yin2011fixes | The asset-pipeline instance and its share |
