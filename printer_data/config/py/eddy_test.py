#!/usr/bin/env python3
import sys
print("DEBUG argv:", sys.argv)
import time
import json
from pathlib import Path
from datetime import datetime

OUTPUT = Path("/home/pi/klipper_logs/eddy_test")

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
    attr1 = sys.argv[1]
    attr2 = sys.argv[2]
    attr3 = sys.argv[3]

    print(f"Attribute 1: {attr1}")
    print(f"Attribute 2: {attr2}")
    print(f"Attribute 3: {attr3}")
    
    if len(sys.argv) != 7:
        print("ARGS INVALIDOS")
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
