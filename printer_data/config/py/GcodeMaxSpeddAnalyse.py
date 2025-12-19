#!/usr/bin/env python3
import sys
import re
import requests
from pathlib import Path

MOONRAKER_URL = "http://127.0.0.1:7125"

if len(sys.argv) < 2:
    sys.exit(0)

gcode_path = Path(sys.argv[1])

if not gcode_path.exists():
    sys.exit(0)

max_feedrate = 0.0
re_f = re.compile(r"[Ff]([0-9]+\.?[0-9]*)")

with gcode_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if not line or line.startswith(";"):
            continue
        m = re_f.search(line)
        if m:
            fval = float(m.group(1))
            if fval > max_feedrate:
                max_feedrate = fval

max_speed_mm_s = round(max_feedrate / 60.0, 2)
print(f"Velocidad maxima final: {max_speed_mm_s} mm/s")

# Ejecutar macro TMC según la velocidad
if max_speed_mm_s >= 180:
    macro = "SET_TMC_AUTOTUNE_PERFORMANCE"
else:
    macro = "SET_TMC_AUTOTUNE_SILENT"

payload = {
    "script": macro
}

try:
    r = requests.post(
        f"{MOONRAKER_URL}/printer/gcode/script",
        json=payload,
        timeout=0.5
    )
except requests.exceptions.RequestException:
    pass
