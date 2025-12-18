#!/usr/bin/env python3
"""
Analizador simple de G-code (fase mínima)

Objetivo:
- Leer el archivo G-code que se va a imprimir
- Detectar ÚNICAMENTE la velocidad máxima (F)
- Devolverla por stdout en formato JSON

Uso:
  python3 gcode_analyzer.py /ruta/al/archivo.gcode
"""

import sys
import json
from pathlib import Path
import re

if len(sys.argv) < 2:
    print("ERROR: falta ruta del G-code", file=sys.stderr)
    sys.exit(1)

gcode_path = Path(sys.argv[1])

if not gcode_path.exists():
    print(f"ERROR: no existe el archivo {gcode_path}", file=sys.stderr)
    sys.exit(1)

# Velocidad máxima encontrada (mm/min)
max_feedrate = 0.0

# Regex para F
re_f = re.compile(r"F([0-9]+\.?[0-9]*)")

with gcode_path.open("r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith(";"):
            continue

        m_f = re_f.search(line)
        if m_f:
            fval = float(m_f.group(1))
            if fval > max_feedrate:
                max_feedrate = fval

result = {
    "file": str(gcode_path),
    "max_feedrate_mm_min": max_feedrate,
    "max_feedrate_mm_s": round(max_feedrate / 60.0, 2)
}

print(json.dumps(result))
