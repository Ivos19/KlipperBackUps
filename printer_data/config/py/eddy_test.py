#!/usr/bin/env python3
import sys
print("DEBUG argv:", sys.argv)
print("DEBUG len(sys.argv):", len(sys.argv))
print("DEBUG sys.argv[1:]:", sys.argv[1:] if len(sys.argv) > 1 else "NO ARGS")
import time
import json
from pathlib import Path
from datetime import datetime

OUTPUT = Path("/home/biqu/printer_data/config/py") #Path("/home/pi/klipper_logs/eddy_test")

def read_eddy_value():

    # Lee el valor del Eddy NG desde la API de Klipper (consulta stats)

    print("Lee el valor del Eddy NG desde la API de Klipper (consulta stats)")
    try:
        import requests
        r = requests.get("http://127.0.0.1:7125/probe/last")
        data = r.json()
        return data["last_z_result"]
    except:
        return None

def main():
    print("Main py script")
    
    # Validación más informativa
    if len(sys.argv) != 7:
        print(f"ARGS INVALIDOS: esperaba 7, recibí {len(sys.argv)}")
        print(f"Argumentos recibidos: {sys.argv}")
        return

    nx, ny, sx, sy, ztarget, cycle = sys.argv[1:]
    nx, ny = float(nx), float(ny)
    sx, sy = float(sx), float(sy)
    ztarget = float(ztarget)
    cycle = int(cycle)

    # leer Eddy
    value = read_eddy_value()

    # asegurar carpeta
    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Guardar en JSON
    entry = {
        "timestamp": datetime.now().isoformat(),
        "cycle": cycle,
        "nozzle": [nx, ny],
        "sensor": [sx, sy],
        "target_z": ztarget,
        "eddy": value,
    }

    with open(OUTPUT / "raw.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
