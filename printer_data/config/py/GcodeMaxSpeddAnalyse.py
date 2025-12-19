#!/usr/bin/env python3
import sys
import re
import requests
from pathlib import Path

MOONRAKER_URL = "http://127.0.0.1:7125/printer/gcode/script"
TARGET_MACRO = "MAX_SPEED_DATA"
TARGET_VARIABLE = "value"

print("DEBUG: Script iniciado")

if len(sys.argv) < 2:
    print("DEBUG: No se recibió ruta de G-code")
    sys.exit(0)

gcode_path = Path(sys.argv[1])
print(f"DEBUG: Archivo G-code: {gcode_path}")

if not gcode_path.exists():
    print("DEBUG: El archivo no existe")
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
                print(f"DEBUG: Nueva F maxima encontrada: {fval} mm/min")

max_speed_mm_s = round(max_feedrate / 60.0, 2)
print(f"DEBUG: Velocidad maxima final: {max_speed_mm_s} mm/s")

gcode_cmd = (
    f"SET_GCODE_VARIABLE "
    f"MACRO={TARGET_MACRO} "
    f"VARIABLE={TARGET_VARIABLE} "
    f"VALUE={max_speed_mm_s}"
)

print(f"DEBUG: Enviando a Klipper -> {gcode_cmd}")

try:
    r = requests.post(
        MOONRAKER_URL,
        json={"script": gcode_cmd},
        timeout=3
    )
    print(f"DEBUG: Moonraker status_code = {r.status_code}")
except Exception as e:
    print(f"DEBUG: Error enviando a Moonraker: {e}")
