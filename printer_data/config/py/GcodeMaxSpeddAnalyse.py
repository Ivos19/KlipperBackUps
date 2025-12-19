#!/usr/bin/env python3

import sys
import os
import re

OUT_FILE = "/home/biqu/printer_data/config/tmp/max_speed.txt"

print("DEBUG: Script iniciado")

if len(sys.argv) < 2:
    print("DEBUG: No se recibió path")
    sys.exit(0)

gcode_path = sys.argv[1]
print(f"DEBUG: Archivo G-code: {gcode_path}")

if not os.path.isfile(gcode_path):
    print("DEBUG: El archivo no existe")
    with open(OUT_FILE, "w") as f:
        f.write("0")
    sys.exit(0)

max_feed_mm_min = 0.0
feedrate_re = re.compile(r"[Ff]([0-9]+(?:\.[0-9]+)?)")

with open(gcode_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.split(";")[0]
        if "F" not in line and "f" not in line:
            continue

        m = feedrate_re.search(line)
        if m:
            feed = float(m.group(1))
            if feed > max_feed_mm_min:
                max_feed_mm_min = feed
                print(f"DEBUG: Nueva F maxima encontrada: {feed} mm/min")

max_speed_mm_s = max_feed_mm_min / 60.0
print(f"DEBUG: Velocidad maxima final: {max_speed_mm_s}")

# 👉 ESCRIBIR RESULTADO
with open(OUT_FILE, "w") as f:
    f.write(str(max_speed_mm_s))

print("DEBUG: Resultado guardado en", OUT_FILE)
