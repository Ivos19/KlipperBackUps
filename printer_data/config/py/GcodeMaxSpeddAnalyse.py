#!/usr/bin/env python3
import sys
import re
import requests
from pathlib import Path

# ----------------------------
# Config
# ----------------------------
MOONRAKER_URL = "http://127.0.0.1:7125/printer/gcode/script"
TARGET_MACRO = "MAX_SPEED_DATA"
TARGET_VARIABLE = "value"

# ----------------------------
# Validaciones
# ----------------------------
if len(sys.argv) < 2:
    sys.exit(0)

gcode_path = Path(sys.argv[1])
if not gcode_path.exists():
    sys.exit(0)

# ----------------------------
# Analisis de velocidad
# ----------------------------
max_feedrate = 0.0
re_f = re.compile(r"F([0-9]+\.?[0-9]*)")

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

# ----------------------------
# Envio a Klipper via Moonraker
# ----------------------------
gcode_cmd = (
    f"SET_GCODE_VARIABLE "
    f"MACRO={TARGET_MACRO} "
    f"VARIABLE={TARGET_VARIABLE} "
    f"VALUE={max_speed_mm_s}"
)

try:
    requests.post(
        MOONRAKER_URL,
        json={"script": gcode_cmd},
        timeout=3
    )
except Exception:
    # No matamos el print por esto
    pass