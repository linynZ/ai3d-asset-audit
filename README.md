# ai3d-asset-audit

Audit of the image-to-3D generated meshes in ChronoTraveler, a completed Unity
game: conventions, geometry hygiene, texture memory (estimated and as stored in
the shipped build), simplification, commit history and animated grounding - and an
attribution audit of the AI coding assistant's own written explanations of the
asset problems against those measurements, plus a defect lifecycle record.

- `PLAN.md` - analysis plan, committed before any audit script existed (2b0bc54).
- `PLAN_v2.md` - second plan for the attribution audit and defect lifecycles, committed before any claim was extracted (63b4a34).
- `scripts/` - every measurement (GLB reader, hygiene, baseline, build readout,
  simplification incl. MeshLab and meshoptimizer, Blender grounding and renders,
  history export/merge, report generation, figures).
- `results/` - all outputs; `report.json` / `report.md` are generated from them.
- `review/` - the internal fact-checks, peer-style review and prior-work survey
  that led to the revised paper.
- `paper/` - LaTeX source and PDF; `paper/summary_zh.md` is a one-page Chinese summary.

The meshes themselves are not redistributed; `data/manifest.json` gives every
file's SHA-256. Commit labels in `results/history_labels.json` were drafted by AI
labellers, reviewed by the AI assistant and signed off by the author. Claims
(`results/claims.json`) carry both judges' verdicts and the written resolutions;
`data/claim_sources/` holds the frozen texts they were extracted from.
