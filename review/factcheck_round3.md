# Fact-check, round 3: the new material (C attribution audit, D defect lifecycle)

Scope: title, abstract, introduction, method (C, D), results (Table 1 H6-H9, Cost ending, grounding "other clips"), results_cd.tex, discussion.tex, limitations (Claims and lifecycles; Deviations).
Checked against: study repo at 82acd70 (PLAN_v2.md 63b4a34, sources f1c962c, data f0392ca), results/*.json, scripts/report_cd.py and claims_verdicts.py, and the game repo at 87fdd16 (read-only; git grep, git log, git show).
The paper was not edited.

Verdicts: WRONG = contradicted by the record; OVERSTATED = true core, claim goes further than the evidence; UNSUPPORTED = no evidence in the repos, or the evidence points elsewhere.

---

## HIGH

### H1. "Every defect not visible on screen shipped" (abstract, H9, results_cd, discussion)
- **Location:** abstract ("every defect not visible on screen shipped"); results_cd ("every defect not visible on screen is in the final build"); Table 1 H9 "supported"; discussion ("Everything else shipped").
- **Verdict:** WRONG
- **Evidence:** defects.json D13 (boss normal map imported as Default): `visible_on_screen.value = false` ("subtly wrong shading at most; never reported from play"), fixed in ee28566 (2026-07-11, pre-ship audit by four parallel AI reviews), `present_in_final_build = false`. Table 5 itself lists it with Ships = "no". So one invisible defect was caught, and it was caught by a non-visual AI review, which runs against the paper's argument.
- **Fix:** "every defect not visible on screen but one shipped; the exception, a mis-typed normal map, was caught by an AI pre-ship code review". H9 outcome: "supported, one exception". In the discussion, change "Everything else shipped" and say that a non-visual check found the one exception.

### H2. The "0.04" reading and "the logs no longer exist"
- **Location:** results_cd, paragraph after the C-results ("The '0.04' that ruled out the bob matches the bob in the FBX's own units (0.041) ... the development logs that would show which numbers were compared no longer exist"); also "the two wrong numbers ... a 0.04 that ruled out a cause"; Table 4 C029 Measurement column.
- **Verdict:** UNSUPPORTED (the stated reading), and the claim that the logs are gone is WRONG. The commit record gives the numbers.
- **Evidence:** 373126d: "v2 snapped correctly (log: moved -0.72)" (single frame). dc81a43: "Keep the stable reading (0.72/0.68 across runs)". 89c36d7: "v2/v3 logs pinned the real culprit: the loop-min differed from the single frame by only 0.04". 0.72 - 0.68 = 0.04, and the loop-min reading is the smaller one, as it should be. So the 0.04 is most likely a correct engine-side difference between one sampled frame and the loop minimum. E1 lets that difference be anywhere from 0 to 0.22 m (single_frame max_sink 0.222). The 0.041 match (grounding_raw idle zmin 0.0734-0.1140 = 0.0407 FBX units; verified) is probably a coincidence. What is wrong is the inference "bob was NOT the cause": after the snap to the minimum the other frames still hover by up to 0.22 m (min_10_samples max_hover 0.218), and that is the "constant hover" the commit describes. The judges' evidence ("bob 0.224 m, >5x the stated 0.04") compares two different quantities.
- **Fix:** Drop the FBX-units reading and "the two wrong numbers". Describe C029 as a correct reading followed by a wrong inference (a frame near the bottom of the bob differs little from the minimum, which does not rule the bob out). Change the Measurement cell to something like "a single frame can sit 0-0.22 m above the loop minimum; after the snap the rest of the loop still hovers up to 0.22 m". Change C029's kind to cause/inference, or note that the "magnitude" coding is the extractor's. The resolution rule's own second clause (engine-side readings -> UNTESTABLE) would make the number itself untestable.

### H3. "Five of the eight blame the generator for something the pipeline did ... and the origin was where glTF puts it"
- **Location:** abstract ("five blame the generator for what the pipeline did"); results_cd.
- **Verdict:** WRONG, on two counts.
- **Evidence:** (a) glTF sets axes (+Y up, +Z front) and metres. It says nothing about where the origin sits. B1 says the origin is at the base of the box in every raw file, which means the generator put it there. (b) C003 ("AI pivots are not at the feet") therefore describes the generator wrongly. It does not blame the generator for something the pipeline did, because the origin is at the base both before and after import (claims_measurements 25/25) and no pipeline step moved it. That leaves four that fit (C010, C011, C063, C042), and three of those are the same "-Z" explanation counted three times.
- **Fix:** "Four of the eight blame the generator for what the importer or our script did (three of them restate one '-Z' explanation); a fifth says the generator's origins are off the feet when they are at the base." Correct the abstract to match.

### H4. C041 "Revised: no", "Only one wrong claim ... was revised", H7 5/6
- **Location:** Table 4 C041 row; results_cd ("Only one wrong claim, the companion's pitch, was revised"); abstract/intro "never revised"; Table 1 H7 (5/6).
- **Verdict:** WRONG under the plan's own definition ("a later commit, comment or doc ... states the corrected version").
- **Evidence:** The spec 2de7310 (2026-07-15 14:31) says "converged at 105,820". 36 minutes later 37e5b4e (15:07) says "pymeshlab UV-preserving QEM (3 rounds, 497,850 -> 82,829 faces)". That is claim C043, which both judges CONFIRMED. The corrected count was written later. The convergence explanation was not withdrawn, and the spec still says 105,820 at 87fdd16, so the dagger is right. report_cd.py REVISED["C041"] gives only the dagger evidence ("design note still says...") and never checks for a later restatement.
- **Fix:** Mark C041 as "count yes, cause no†" (or "partly"). H7 becomes 4/6 (still a majority, so still supported). Reword to "only the pitch was fully corrected; the face count was restated correctly in the next commit, but the 'converged' explanation stayed in the design note".

### H5. "Every defect clearly visible in play was fixed within an hour of being reported"
- **Location:** abstract; results_cd (H9 paragraph); introduction ("Defects that showed on screen were fixed within the hour"); discussion ("Every defect that a player could see was found and fixed, mostly within the hour").
- **Verdict:** OVERSTATED / UNSUPPORTED, for two reasons.
- **Evidence:** (a) The idle bob (D09) was seen in play and reported ("the rest of the cycle still hovered ~0.1-0.2", user report, kept in the GroundSnap comment at 87fdd16 lines 23-24), and it shipped. The results text protects itself with "clearly visible", but the discussion's "Every defect that a player could see was found and fixed" has no qualifier and is contradicted by D09. (b) The report time is not recorded, because the transcripts are gone. In defects.json `first_observed` is the timestamp of the first commit that describes the symptom, and for D01, D07, D08, D11, D12, D15 and D16 that commit is itself the first fix. Observed-to-fixed is therefore 0 h by construction, or the length of the fix chain (D07 5 min, D08 26 min). "Within an hour of being reported" cannot be measured.
- **Fix:** "Every defect that was clearly visible and reported, apart from the idle bob, was fixed, and each fix chain was finished within 26 minutes of the first commit that describes it; when the developer actually saw the symptom is not recorded." In the discussion, add "except the idle bob, which was accepted". Add one line under Limitations: observation time = first describing commit.

---

## MEDIUM

### M1. Judging and resolution: who judged, how the disagreements went, and what can be verified
- **Location:** method C ("judged by the assistant and, independently, by a second AI judge ... resolved under a rule written before resolving; the author signed off"); results_cd ("rule fixed in advance ... inferences from other assets go to UNTESTABLE"); limitations.
- **Verdict:** UNSUPPORTED (order and sign-off) and incomplete (rule, direction of resolutions).
- **Evidence:**
  - Final verdict = judge 1 for 77 of 83 claims. Of the 20 disagreements, 14 went to judge 1 and 6 to judge 2. All eight claims that only judge 2 called wrong (C030, C032, C033, C035, C049, C051, C077, C082) were moved to UNTESTABLE. The resolved wrong share is exactly judge 1's own share (8/39).
  - "Judge 1 = the assistant": claims_verdicts.py says "verdicts drafted by the AI assistant (judge 1)", and the C/D commits carry the trailer "Claude Opus 5.5". The claims were written by Claude Opus 4.8 and Claude Fable 5. As written, "judged by the assistant" reads as the same assistant judging its own claims. Say which assistant, and say that the resolver was also judge 1.
  - The rule in report_cd.py (lines 15-16) has a second clause, "or from offline numbers about engine-side readings -> UNTESTABLE". The paper leaves it out, yet it decided C030, C032, C033 and C082.
  - Order: extraction, both judges, the resolutions and the defect record are all in one commit (f0392ca, 20:12, 16 minutes after the source freeze f1c962c at 19:56). "Written before resolving" cannot be checked from git, which is the same situation the paper already admits for B ("order ... not separately recorded").
  - Sign-off: there is no record of author sign-off on the C/D verdicts (B5 has 336cf35 "Author sign-off on commit labels"; nothing comparable exists for C/D).
- **Fix:** Name judge 1 as the study's assistant (Claude Opus 5.5) and say it also resolved. Report "14 of 20 disagreements resolved toward judge 1; the resolved share equals judge 1's", give the full rule, say that extraction, judging and resolution were committed together, and either commit a sign-off or delete "the author signed off".

### M2. "The wrong ones are mostly explanations" against the coded kind field
- **Location:** abstract ("the wrong ones mostly explanations"); intro ("mostly explanations rather than readings"); results_cd; discussion ("Explanations are where the assistant went wrong").
- **Verdict:** OVERSTATED. It is an interpretive recoding that the data's own coding does not support.
- **Evidence:** The kind field of the 8 wrong claims: cause 2 (C011, C042), property 3 (C003, C010, C063), magnitude 2 (C029, C041), effect 1 (C053). 3 of the 5 testable causal claims were confirmed (C025, C028, C052). H8 is 2/5 vs 3/14, which the paper itself calls too few to separate. Calling C010, C063, C003 and C041 "explanations" is the author's reading.
- **Fix:** Say it once as a reading: "by our reading six of the eight were offered to explain a symptom, although the extractors coded only two as causal". Soften the abstract to "several of the wrong ones were explanations".

### M3. Intro: "they were written into tool comments, copied to other tools and never revised"
- **Verdict:** OVERSTATED. One case is generalised to all.
- **Evidence:** Only the "-Z" claim was copied between tools. C053 was revised. C003 and C029 exist only in commit messages and are not in any comment at 87fdd16 (git grep).
- **Fix:** "one of them was written into a tool comment and copied into two more tools and notes; most were never revised".

### M4. "Two of the shipped defects had been seen"
- **Location:** results_cd, last paragraph.
- **Verdict:** UNSUPPORTED for the companion cracks.
- **Evidence:** defects.json D06: "No commit, comment or doc ever describes cracks/holes"; a870939 says "user Play-verified" but records nothing about cracks. Only the uncompressed maps (AI review) and the idle bob (reported) count as "seen".
- **Fix:** "Two of the shipped defects were on record: the uncompressed maps (AI review) and the idle bob. The companion's cracks passed a play check recorded as 'Play-verified'."

### M5. Discussion: "the rest belong to the pipeline built around it, most of it written by the assistant"
- **Verdict:** OVERSTATED
- **Evidence:** The front reversal (UniGLTF reverseAxis default) and the uncompressed storage (UniGLTF LoadImage) are behaviours of a third-party importer that was vendored (ed13679), not written by the assistant. Only the dropped maps (NPCModelSetupTool) and the tear (decimate_xuanji.py) are assistant-written code.
- **Fix:** "...the rest belong to the pipeline around it: a third-party importer and tools the assistant wrote".

### M6. Limitations: "Nearly half of the claims could not be tested, mostly those about engine-side readings we did not reproduce"
- **Verdict:** WRONG
- **Evidence:** About 10 of the 40 UNTESTABLE claims are engine-side readings or placement (C019, C026, C027, C030, C032, C033, C082, C035, C067, roughly C006). About 11 are tool or prefab outputs that were not measured (C004, C017, C023, C024, C031, C044, C050, C051, C064, C071, C073). About 17 concern generator inputs, prompts, identity, appearance or rigging (C013, C016, C022, C040, C047, C048, C049, C055-C057, C061, C069, C074, C077-C080).
- **Fix:** "...mostly about prompts and inputs, tool outputs or engine-side readings we did not measure".

### M7. "One assistant" (limitations), "an AI coding assistant" (throughout)
- **Verdict:** OVERSTATED / undisclosed.
- **Evidence:** I counted the trailers on the 484 non-merge commits myself and confirmed 410. They name three models: Claude Opus 4.8 (236), Claude Fable 5 (170), Claude Sonnet 4.6 (4). The 8 wrong claims split 4/4: Opus 4.8 wrote C003, C010, C011 and C063, and Fable 5 wrote C029, C041, C042 and C053. The "-Z" claim crossed models: Opus 4.8 on Jun 23 and Jul 9 (61f3e91), then Fable 5 on Jul 15 (2de7310).
- **Fix:** One sentence in Method C or Limitations: "one assistant product, three model versions (trailers)". The cross-model copying also strengthens the "reused as a fact" point.

### M8. Translated quotations presented as verbatim
- **Location:** Table 4 caption "verbatim, abridged": C041 ("converged at 105,820 faces"; the source is 收敛于 105,820 面) and C042 ("fragmented UV seam islands are a hard floor"; the source is 混元自动 UV 碎接缝岛是硬约束). results_cd: "about 89 MB uncompressed" (the source is 各贡献约 89 MB 未压缩资源).
- **Verdict:** OVERSTATED (presentation)
- **Fix:** Mark these "(translated from Chinese)". For C042 the English script comment at 87fdd16 (decimate_xuanji.py:76, "converged — UV seam islands are the hard floor") could be quoted instead.

---

## LOW

- **L1. C063 dagger.** C063's own text ("consistent across the same Hunyuan pipeline") is only in the f3da6c2 message and is not in the final build. What the build contains is the boss-tool comment "Hunyuan exports face -Z (NPC-pipeline finding)", which is claim C022 (judged UNTESTABLE). Either explain the dagger in a footnote or remove it.
- **L2. Discussion code snippet.** The code is `private float _faceYaw = 180f;  // Hunyuan front-view exports face -Z; ...`, an end-of-line comment, not one "above the line", and it reads `180f`, not `180;`. The message and the comment were written in the same commit (f3da6c2), so the comment did not "become" one later. The copying into the next tool is real (61f3e91, Jul 9).
- **L3. "deferred without a recorded reason".** b91ad03 lists what was adopted and what was "Explicitly NOT adopted", and the texture task is in neither list. Nothing records a decision to defer it. Use "was not acted on, and no reason was recorded".
- **L4. "two of them introduced defects of their own (a fix that changed nothing ...)".** A no-op fix (9760126) introduces no new defect; it just fails. Suggest "two of them failed: one changed nothing, one sank the boss 1.5 m".
- **L5. Table 5 details.** The merged row "fix 1 no-op; fix 4 sank" has Obs 0.2, but the data give D15 0.15 h and D16 0.14 h; write "0.1-0.2". "Other clips sink" shows Obs "--", but defects.json gives 2,104.6 h (introduced -> this audit); either fill it in or say "--" means not observable in play. D14 (shader stripping, not applicable) is dropped silently, so add "D14 omitted: not a generated-asset defect" to the caption.
- **L6. Inconsistencies in the released data (not in the text).** C034 "true hover ~0.9" is CONFIRMED by both judges under the 2x rule, while defects.json D16 says the same figure "does not match" E1 (0.46-0.68). C046 "105k 单 draw call 可接受" is CONFIRMED although 105k is C041's contradicted count. Make the two files agree.
- **L7. Reproducibility.** The claims_verdicts.py docstring refers to `scripts/claims_compare.py`, which does not exist; merging and resolution are in report_cd.py.
- **L8. Intro wording.** "410 of its 484 commits" should be "non-merge commits". "how to collect every claim the assistant made about the assets" should be "every claim in the frozen sources (174 selected commits, tool comments, five notes)".
- **L9. C029 "Revised: no".** This is defensible, but the final GroundSnap (lines 23-24) still carries the earlier bob explanation (from 373126d) through the later rewrites. Worth a footnote, since it makes the final code self-contradictory rather than uncorrected.
- **L10. Style.** Several lines read as slogans: "The pattern is clearer than the rate", "Wrong explanations were not corrected; they were reused", "They also had a life", "here the more lasting product of a fix was its explanation", "earns its keep", the subsection title "what is seen is fixed, what is not seen ships", and "the newest and most conspicuous component" ("newest" is unsupported, since the generator was not demonstrably newer than the importer). Plainer statements would help, especially after H1/H5 make the chiasmus untrue.
- **L11. Rule paraphrase / PARTLY definition.** The plan's PARTLY also covers "true for some assets only"; method C leaves this out.

---

## OK (verified)

- 410/484: counted myself from the trailers on the non-merge commits up to 87fdd16 (484 total; 410 with a Claude co-author).
- Source bundle: commits.jsonl 174 (= 156 B5 + 54 path-touching - 36 overlap), code_comments.jsonl 215 lines, 5 docs; 170/174 have trailers. All 8 wrong claims come from co-authored commits or co-authored docs.
- Order: PLAN_v2 63b4a34 (19:55) -> source freeze f1c962c (19:56) -> extraction/judging/defects f0392ca (20:12) -> paper 82acd70 (20:16). The plan precedes extraction.
- 83 claims; 62 both, 12 A-only, 9 B-only (A file 74 items, B file 70 items; B015 split into two claims).
- Agreement 63/83 = 75.9 % and Cohen's kappa = 0.637, recomputed from claims_judge1/2.json, which match claims.json. 20 disagreements (ids match report.json); none unresolved.
- Verdicts: 31 CONFIRMED, 6 CONTRADICTED, 2 PARTLY, 40 UNTESTABLE, 4 OUT_OF_SCOPE (all four concern VRM/non-generated material). 8/39 = 20.5 %. Judge 2 alone: 16/51 = 31.4 %.
- H8: cause 2/5, property 3/14, magnitude 2/14 (effect 1/6).
- Table 4 verdicts all match claims.json. Quotes C010, C011, C003, C029 and C053 are verbatim from the source commits. Daggers on C010, C011, C041 and C042 confirmed by git grep at 87fdd16 (NPCModelSetupTool.cs:34; companion spec line 27; decimate_xuanji.py:76). C003 and C029 are not in the final build. C053 was revised in 288327d, 5 min after 95cf232, and the final FacePitch = 90f.
- The "-Z" chain: f3da6c2 2026-06-23 (NPC tool) -> 61f3e91 2026-07-09 (FinaleBossModelTool.cs:96 "NPC-pipeline finding") -> 2de7310 2026-07-15 (companion spec line 56, as "既有经验"). It also continues into the plan doc of Jul 15 and the distillation docs of Jul 22 (pitfalls.md, pipelines.md), which is extra support if wanted.
- 0.041: idle zmin range 0.0407 FBX units; x5.519 gives 0.224 m at game scale. (The number is right; the interpretation is not, see H2.)
- Other clips: attack -0.268, knock-down -0.079, leap -1.189 m vs the idle ground (grounding.json).
- No runtime script calls SetTrigger/SetBool/Play on an Animator at 87fdd16; the only Animator call is the player's SetFloat("Speed"). The controller has attack/hit/leap trigger conditions.
- Five hover-fix commits 9760126 11:00:59 -> dc81a43 11:26:57 = 26 min. D15 and D16 are fix-induced.
- Table 5 hours otherwise match defects.json (21.68, 0, 21.55, 0.39/0.09, 0.28/0, 51.58/0.43, 42.84/0, 51.82, 559.84, 2513.46 x2, 1952.88). Channels and Ships match `present_in_final_build`.
- External AI review: DESIGN/ProjectAudit_2026-07-15.md, added in b91ad03 (2026-07-15 14:22). It says "24 个 GLB ... 在构建报告中各贡献约 89 MB 未压缩资源" and proposes downsampling plus GPU texture compression (task 1). b91ad03's adopted list leaves it out, and no later commit touches *.glb/.glb.meta or texture compression.
- "Play-verified": a870939 "(user Play-verified)".
- Dropped normal/MR maps and CPU-readable copies are never mentioned in any commit message (searched).
- Every B5 ASSET/ENGINE commit (17) appears in defects.json.
- All 46 \cite keys resolve in references.bib; main.log has no undefined citations or references; main.pdf (9 pages) was compiled from the current sources.
- The title fits the content now that C/D are core results.
- The abstract's numbers (26 meshes, 70 %, 2,433 pieces, 39/8, 5 of 6) match the body. Only the wording issues above (H1, H3, H4, H5, M2) affect it.
