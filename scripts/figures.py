"""Paper figures (PDF, vector). Palette: validated categorical slots 1-3
(#2a78d6 blue, #eb6834 orange, #1baf7a aqua) on white; text in neutral ink.

Usage: python scripts/figures.py
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent.parent
RES, FIG = HERE / "results", HERE / "paper" / "figures"
BLUE, ORANGE, AQUA, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#1f1f1e", "#6b6a63", "#e4e3dc"

plt.rcParams.update({
    "font.family": "serif", "font.size": 7.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "lines.linewidth": 1.4,
    "legend.frameon": False, "pdf.fonttype": 42,
})


def grounding():
    raw = next(r for r in json.loads((RES / "grounding_raw.json").read_text()) if r["file"] == "boss_idle.fbx")
    z = np.array([f["zmin"] for f in raw["frames"]])
    s = 10.0 / (raw["rest_zmax"] - raw["rest_zmin"])
    t = np.arange(len(z)) / raw["fps"]
    y = (z - raw["rest_zmin"]) * s  # height of the true lowest point above the bind-pose foot line, metres
    fps = raw["fps"]
    samples = [np.interp(2 + k * 0.16 * fps, np.arange(len(z)), y) for k in range(10)]
    fig, ax = plt.subplots(figsize=(3.3, 1.55))
    ax.plot(t, y, color=INK, lw=1.4, label="true lowest vertex")
    ax.axhline(0, color=ORANGE, lw=1.2, ls="--")
    ax.text(t[-1], 0.03, "bind-pose bounds (ground)", color=INK, ha="right", va="bottom", fontsize=6.5)
    ax.axhline(min(samples), color=BLUE, lw=1.2, ls="--")
    ax.text(t[-1], min(samples) - 0.03, "10 samples, 0.16 s apart (shipped)", color=INK, ha="right", va="top", fontsize=6.5)
    st = 2 + np.arange(10) * 0.16 * fps
    ax.plot(st / fps, samples, "o", ms=3.2, color=BLUE, mec="white", mew=0.6)
    ax.text(0.36, 0.585, "true lowest vertex", color=INK, fontsize=6.5)
    ax.set_xlabel("idle loop time (s)")
    ax.set_ylabel("height above\nbind-pose feet (m)")
    ax.set_ylim(-0.1, 0.8)
    ax.set_xlim(0, t[-1])
    fig.tight_layout(pad=0.3)
    fig.savefig(FIG / "grounding_idle.pdf")


def decimation():
    rows = [json.loads(l) for l in (RES / "decimation.jsonl").read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r["id"] != "xuanji_raw"]
    fracs = [0.5, 0.25, 0.125, 0.0625]
    fig, axes = plt.subplots(1, 2, figsize=(3.3, 1.6))
    names = {"S": "seam-split + UV (as shipped)", "W": "welded + UV", "N": "welded, no UV"}
    for cond, col, mk in (("S", ORANGE, "o"), ("W", BLUE, "s"), ("N", AQUA, "^")):
        med_b = [np.median([r["boundary_edges_after_weld"] for r in rows if r["cond"] == cond and r["target_frac"] == f]) for f in fracs]
        med_h = [np.median([r["hausdorff_mean_pct"] for r in rows if r["cond"] == cond and r["target_frac"] == f]) for f in fracs]
        x = [100 * f for f in fracs]
        axes[0].plot(x, med_b, marker=mk, ms=3.5, color=col, mec="white", mew=0.6, label=names[cond])
        axes[1].plot(x, med_h, marker=mk, ms=3.5, color=col, mec="white", mew=0.6)
    for ax in axes:
        ax.set_xscale("log", base=2)
        ax.set_xticks([50, 25, 12.5, 6.25])
        ax.set_xticklabels(["50", "25", "12.5", "6.25"])
        ax.invert_xaxis()
        ax.set_xlabel("target (% of faces)")
    axes[0].set_ylabel("open edges after\nwelding (median)")
    axes[1].set_ylabel("mean Hausdorff\n(% of bbox diag.)")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="upper center", ncol=3, fontsize=6, bbox_to_anchor=(0.5, 1.02),
               handlelength=1.4, columnspacing=0.8)
    fig.tight_layout(pad=0.3, rect=(0, 0, 1, 0.88))
    fig.savefig(FIG / "decimation.pdf")


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    grounding()
    if (RES / "decimation.jsonl").exists():
        decimation()
