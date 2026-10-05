"""E1 analysis: error of each grounding estimator against the per-frame truth.

An estimator returns m, the height treated as the feet line; the model is moved
so that m sits on the ground. At frame t the true lowest point is z(t), so the
model hovers by z(t) - m (negative = sinks into the ground). Errors are scaled
to the in-game size (the boss is normalised to 10 m tall at bind pose).

Usage: python scripts/grounding_analysis.py   (reads results/grounding_raw.json)
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
GAME_HEIGHT = 10.0
START_FRAMES = 2          # GroundSnap waits two frames
N_SAMPLES, INTERVAL = 10, 0.16   # as shipped


def interp(z, f):
    f = min(max(f, 0), len(z) - 1)
    i = int(np.floor(f))
    j = min(i + 1, len(z) - 1)
    return z[i] + (z[j] - z[i]) * (f - i)


def main():
    raw = json.loads((HERE / "results" / "grounding_raw.json").read_text(encoding="utf-8"))
    out = []
    for r in raw:
        z = np.array([f["zmin"] for f in r["frames"]])
        s = GAME_HEIGHT / (r["rest_zmax"] - r["rest_zmin"])
        fps = r["fps"]
        sampled = [interp(z, START_FRAMES + k * INTERVAL * fps) for k in range(N_SAMPLES)]
        est = {
            "bind_pose_bounds": r["rest_zmin"],
            "single_frame": interp(z, START_FRAMES),
            "min_10_samples_0.16s": min(sampled),
            "min_all_frames": float(z.min()),
        }
        row = {"file": r["file"], "frames": len(z), "seconds": round(len(z) / fps, 3),
               "lowest_point_range_m": round(float(z.max() - z.min()) * s, 3),
               "sampled_window_s": round((N_SAMPLES - 1) * INTERVAL, 2), "estimators": {}}
        for name, m in est.items():
            hover = (z - m) * s
            row["estimators"][name] = {
                "max_hover_m": round(float(hover.max()), 3),
                "max_sink_m": round(float(-hover.min()), 3),
                "mean_abs_m": round(float(np.abs(hover).mean()), 3),
                "share_frames_off_by_more_than_0.1m": round(float(np.mean(np.abs(hover) > 0.1)), 3),
            }
        # Added after review: start the shipped 10-sample schedule at every frame of the loop
        # (wrapping), and express each clip's lowest point against the idle-calibrated ground.
        n = len(z)
        phase_err = np.array([
            (min(z[int(round(st + START_FRAMES + k * INTERVAL * fps)) % n] for k in range(N_SAMPLES)) - z.min()) * s
            for st in range(n)])
        row["phase_analysis"] = {
            "loop_s": round(n / fps, 3),
            "sampled_window_share": round((N_SAMPLES - 1) * INTERVAL / (n / fps), 3),
            "phase_worst_mm": round(float(phase_err.max()) * 1000, 1),
            "phase_median_mm": round(float(np.median(phase_err)) * 1000, 1),
            "min_above_bind_m": round(float(z.min() - r["rest_zmin"]) * s, 3),
            "max_above_bind_m": round(float(z.max() - r["rest_zmin"]) * s, 3),
        }
        out.append(row)
    idle = next(o for o in out if o["file"] == "boss_idle.fbx")["phase_analysis"]["min_above_bind_m"]
    for o in out:
        o["phase_analysis"]["lowest_vs_idle_ground_m"] = round(o["phase_analysis"]["min_above_bind_m"] - idle, 3)
        print(row["file"], row["lowest_point_range_m"],
              {k: (v["max_hover_m"], v["max_sink_m"]) for k, v in row["estimators"].items()})
    (HERE / "results" / "grounding.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
