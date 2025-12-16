#!/usr/bin/env python3
import json
from pathlib import Path
from statistics import mean, stdev
from datetime import datetime

# Paths
BASE = Path("/home/biqu/printer_data/config/py")
SRC = BASE / "EddyBedCheck.json"
OUT = BASE / "EddyBedCheck_report.txt"

# Sensor positions → human names
POINT_NAMES = {
    (50.0, 50.0): "BACK-RIGHT",
    (250.0, 50.0): "BACK-LEFT",
    (250.0, 250.0): "FRONT-LEFT",
    (50.0, 250.0): "FRONT-RIGHT",
    (150.0, 150.0): "CENTER",
}

LAST_N = 15  # last run = 3 cycles × 5 points

def main():
    if not SRC.exists():
        print("EddyBedCheck.json not found")
        return

    lines = SRC.read_text().strip().splitlines()[-LAST_N:]
    data = [json.loads(l) for l in lines]

    by_point = {}
    all_values = []

    for d in data:
        key = tuple(d["sensor_cmd"])
        by_point.setdefault(key, []).append(d)
        all_values.append(d["eddy"])

    # Average per point
    point_avg = {
        k: mean(r["eddy"] for r in rows)
        for k, rows in by_point.items()
    }

    with OUT.open("w") as f:
        # Header
        f.write("EDDY BED CHECK REPORT\n")
        f.write(f"Generated : {datetime.now().isoformat()}\n")
        f.write(f"Samples   : {len(data)}\n")
        f.write(f"Cycles    : {len(set(d['cycle'] for d in data))}\n")
        f.write(f"Target Z  : {data[0]['target_z']:.4f}\n\n")

        # Table header
        f.write("POINT         SENSOR       NOZZLE       CYCLE   EDDY     ΔvsAVG\n")
        f.write("-" * 70 + "\n")

        stability = {}

        # Table rows
        for key, rows in by_point.items():
            name = POINT_NAMES.get(key, str(key))
            avg = point_avg[key]
            values = []

            for r in rows:
                sx, sy = r["sensor_cmd"]
                nx, ny = r["nozzle_cmd"]
                delta = r["eddy"] - avg
                values.append(r["eddy"])

                f.write(
                    f"{name:<13} "
                    f"({sx:>3.0f},{sy:>3.0f})   "
                    f"({nx:>3.0f},{ny:>3.0f})     "
                    f"{r['cycle']:>2}    "
                    f"{r['eddy']:.4f}  "
                    f"{delta:+.4f}\n"
                )

            # Delta per point (area stability)
            point_delta = max(values) - min(values)
            stability[name] = point_delta

            f.write(
                f"--> {name} POINT DELTA: {point_delta:.4f} mm\n\n"
            )

        # Bed summary
        f.write("\n=== BED SUMMARY ===\n\n")

        lo = min(data, key=lambda d: d["eddy"])
        hi = max(data, key=lambda d: d["eddy"])

        f.write(
            f"Lowest eddy value  : {lo['eddy']:.4f} "
            f"({POINT_NAMES.get(tuple(lo['sensor_cmd']))}, cycle {lo['cycle']})\n"
        )
        f.write(
            f"Highest eddy value : {hi['eddy']:.4f} "
            f"({POINT_NAMES.get(tuple(hi['sensor_cmd']))}, cycle {hi['cycle']})\n\n"
        )

        f.write(
            f"TOTAL BED DELTA    : {hi['eddy'] - lo['eddy']:.4f} mm\n"
        )
        f.write(
            f"Global average     : {mean(all_values):.4f}\n"
        )

        if len(all_values) > 1:
            f.write(
                f"Std deviation      : {stdev(all_values):.4f}\n"
            )

        worst = max(stability, key=stability.get)
        best = min(stability, key=stability.get)

        f.write(
            f"\nMost unstable point: {worst} (Δ={stability[worst]:.4f})\n"
        )
        f.write(
            f"Most stable point  : {best} (Δ={stability[best]:.4f})\n"
        )

    print(f"Report written to {OUT}")

if __name__ == "__main__":
    main()
