"""C step 4: verdicts drafted by the AI assistant (judge 1), each with the evidence
it rests on. Evidence must be a file in results/ (or a fact already reported in the
paper before extraction began). Judge 2 (an independent agent) re-judges without
seeing these; scripts/claims_compare.py merges both.

Usage: python scripts/claims_verdicts.py
"""
import json
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "results"

C, X, P, U, O = "CONFIRMED", "CONTRADICTED", "PARTLY", "UNTESTABLE", "OUT_OF_SCOPE"
V = {
    "C001": (C, "conventions.json: skins=0, animations=0 for all 15 NPC GLBs"),
    "C002": (C, "conventions.json: NPC heights 0.98-1.15 units, largest extent 0.895-1.151 (all 24)"),
    "C003": (X, "conventions.json pivot_frac y=0 for all 24; claims_measurements.json: origin at base for 25/25 after UniGLTF Z reversal"),
    "C004": (U, "prefab output of the tool not measured"),
    "C005": (C, "conventions.json: historian 49,818 triangles, 3 images, no skin/animation"),
    "C006": (U, "shader behaviour not measured"),
    "C007": (C, "build_textures.json: each GLB asset's base map is present and referenced in the build"),
    "C008": (U, "UniGLTF material output not measured"),
    "C009": (U, "not measured (a later commit in the same history reverses it)"),
    "C010": (X, "facing renders (results/facing, facing_sheet.png): all 15 NPCs show their faces from glTF +Z"),
    "C011": (P, "effect (historian showed its back) true; cause wrong: GLB fronts face +Z, UniGLTF default reverses Z"),
    "C012": (C, "conventions.json: guardian 49,684 triangles, 3 images, no skin"),
    "C013": (U, "height 0.993 confirmed (conventions.json) but the stated cause (polearm) not tested"),
    "C014": (O, "concerns VRM models, not generated assets"),
    "C015": (C, "manifest.json: GLB files 29-52 MB"),
    "C016": (C, "facing renders show all three camels with four separate legs; hygiene.json: camels one component"),
    "C017": (U, "prefab heights not measured"),
    "C018": (C, "grounding_raw.json: 9,038 triangles, 28 bones, four FBX each with an action"),
    "C019": (U, "shader behaviour not measured"),
    "C020": (U, "tool output not measured (FBX bind-pose feet at origin: grounding_raw rest_zmin -0.01, consistent)"),
    "C021": (C, "grounding_raw.json: identical vertex (4,501) and triangle (9,038) counts in all four FBX"),
    "C022": (U, "boss facing not rendered"),
    "C023": (U, "not measured"),
    "C024": (U, "colliders not measured"),
    "C025": (C, "grounding.json: idle loop lowest vertex 0.46-0.68 m above bind-pose feet at game scale"),
    "C026": (U, "Unity renderer bounds not measured; Unity documents skinned bounds as precomputed from animations"),
    "C027": (U, "Unity BakeMesh not measured"),
    "C028": (C, "grounding.json: one sampled frame can be off by up to 0.22 m (idle bob) - matches the 0.1-0.2 residual"),
    "C029": (X, "grounding.json: idle bob range 0.224 m at game scale, >5x the stated 0.04"),
    "C030": (U, "Unity BakeMesh semantics not reproduced"),
    "C031": (U, "Unity prefab scale not measured"),
    "C032": (U, "engine readings not reproduced"),
    "C033": (U, "engine readings not reproduced"),
    "C034": (C, "grounding.json: hover 0.46-0.68 m; 0.9 lies outside that range but within the plan's factor-of-2 rule"),
    "C035": (U, "engine placement not measured"),
    "C036": (C, "conventions.json: xuanji_raw skins=0, animations=0"),
    "C037": (C, "conventions.json: xuanji_raw world extent 0.8725 x 1.1054 x 0.5246"),
    "C038": (C, "manifest.json: 56.6 MB = 54.0 MiB"),
    "C039": (C, "conventions.json: xuanji_raw has three 4096x4096 PNG maps"),
    "C040": (U, "appearance not scored"),
    "C041": (X, "hygiene.json: shipped companion has 82,829 triangles after the three rounds; decimation.jsonl: no floor near 106k"),
    "C042": (X, "decimation.jsonl: xuanji_raw reaches 31,116 triangles (6.25 %) in one pass, welded or seam-split"),
    "C043": (C, "hygiene.json: xuanji_body 82,829 triangles; 497,850 x 0.55^3 ~ 82,830"),
    "C044": (U, "not measured"),
    "C045": (C, "B3 arithmetic: a 4096^2 map in BC7 with mips is 21.3 MiB (visual claim not tested)"),
    "C046": (U, "draw calls not measured"),
    "C047": (U, "rigging not tested"),
    "C048": (U, "not tested"),
    "C049": (U, "companion facing not rendered"),
    "C050": (U, "tool output not measured"),
    "C051": (U, "tool output not measured"),
    "C052": (C, "claims_measurements.json: MeshLab returns untransformed positions, tallest axis z (lying); the GLB node chain makes it y"),
    "C053": (X, "conventions.json: root rotation +90 deg about X, i.e. up is local -Z; a -90 pitch turns the head down"),
    "C054": (C, "conventions.json: root rotation +90 deg about X restores up; +90 pitch is the GLB's own correction"),
    "C055": (U, "inputs not tested"),
    "C056": (U, "inputs not tested"),
    "C057": (U, "not tested"),
    "C058": (C, "conventions.json: artisan 49,772 triangles, 3 images, no skin"),
    "C059": (C, "conventions.json: root rotation [0.7071,0,0,0.7071] (+90 deg X) on all 24"),
    "C060": (C, "conventions.json: 48,658-50,124 triangles"),
    "C061": (U, "inputs not tested"),
    "C062": (U, "not tested"),
    "C063": (X, "facing renders: all 15 NPCs face glTF +Z; the -Z front in Unity comes from the importer"),
    "C064": (U, "prefabs not measured"),
    "C065": (O, "concerns VRM models"),
    "C066": (C, "boss_idle.fbx.meta animationType: 2 (Generic), read for Section 5.6 before extraction"),
    "C067": (U, "engine placement not measured"),
    "C068": (C, "conventions.json: xuanji_raw 497,850 triangles"),
    "C069": (U, "pose not measured"),
    "C070": (C, "conventions.json: up is local -Z, so -90 pitch puts the head down"),
    "C071": (U, "prefab not measured"),
    "C072": (C, "conventions.json: xuanji_raw attributes NORMAL, POSITION, TEXCOORD_0 only; no morph targets, no animation"),
    "C073": (C, "build_textures.json: companion normal map (1024, DXT5) present in the build"),
    "C074": (U, "inputs not tested"),
    "C075": (O, "concerns VRM models"),
    "C076": (C, "effect confirmed (all NPCs face away after import); 'some' understates it"),
    "C077": (U, "identity not tested"),
    "C078": (U, "identity not tested"),
    "C079": (U, "identity not tested"),
    "C080": (U, "not tested"),
    "C081": (C, "grounding_raw.json: four FBX, one action each"),
    "C082": (U, "engine readings not reproduced"),
    "C083": (C, "build_textures.json: companion base 2048 (DXT1), normal 1024 (DXT5), no metallic-roughness map"),
}


def main():
    claims = json.loads((RES / "claims_merged.json").read_text(encoding="utf-8"))
    assert {c["id"] for c in claims} == set(V), "every claim needs a verdict"
    out = [{"id": c["id"], "verdict": V[c["id"]][0], "evidence": V[c["id"]][1]} for c in claims]
    (RES / "claims_judge1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    from collections import Counter
    print(Counter(v[0] for v in V.values()))


if __name__ == "__main__":
    main()
