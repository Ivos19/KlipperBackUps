#!/usr/bin/env python3

import sys
import os
import re
import requests

# ==============================
# CONFIG
# ==============================
MOONRAKER_URL = "http://127.0.0.1:7125/printer/gcode/script"

# ==============================
# DEBUG INIT
# ==============================
print("DEBUG: Script iniciado")

# ==============================
# VALIDAR PARAMETROS
# ==============================
if len(sys.argv) < 2:
    print("DEBUG: No se recibió path de G-code")
    sys.exit(0)

gcode_path = sys.argv[1]

print(f"DEBUG: Archivo G-code: {gcode_path}")

if not os.path.isfile(gcode_path):
    print("DEBUG: El archivo no existe")
    sys.exit(0)

# ==============================
# ANALISIS DEL G-CODE
# ==============================
max_feed_mm_min = 0.0

# Regex para capturar F (feedrate)
feedrate_re = re.compile(r"[Ff]([0-9]+(?:\.[0-9]+)?)")

try:
    with open(gcode_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            # Ignorar comentarios
            line = line.split(";")[0]
            if "F" not in line and "f" not in line:
                continue

            match = feedrate_re.search(line)
            if match:
                feed = float(match.group(1))
                if feed > max_feed_mm_min:
                    max_feed_mm_min = feed
                    print(f"DEBUG: Nueva F maxima encontrada: {feed} mm/min")

except Exception as e:
    print("DEBUG: Error leyendo el archivo:", e)
    sys.exit(0)

# ==============================
# CALCULO FINAL
# ==============================
max_speed_mm_s = max_feed_mm_min / 60.0

print(f"DEBUG: Velocidad maxima final: {max_speed_mm_s} mm/s")

# ==============================
# ENVIO A KLIPPER (MOONRAKER)
# ==============================
payload = {
    "script": f"SET_GCODE_VARIABLE MACRO=MAX_SPEED_DATA VARIABLE=value VALUE={max_speed_mm_s}"
}

print(
    "DEBUG: Enviando a Klipper -> "
    f"SET_GCODE_VARIABLE MACRO=MAX_SPEED_DATA VARIABLE=value VALUE={max_speed_mm_s}"
)

try:
    response = requests.post(
        MOONRAKER_URL,
        json=payload,
        timeout=3
    )
    print("DEBUG: Moonraker status_code =", response.status_code)
    if response.status_code != 200:
        print("DEBUG: Moonraker response:", response.text)

except Exception as e:
    print("DEBUG: Error enviando a Moonraker:", e)

# ==============================
# FIN
# ==============================
