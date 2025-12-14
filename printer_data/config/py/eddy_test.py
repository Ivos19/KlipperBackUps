#!/usr/bin/env python3
import sys
import requests
import time
import json
from pathlib import Path
from datetime import datetime

OUTPUT = Path("/home/biqu/printer_data/config/py")
MOONRAKER = "http://127.0.0.1:7125"
OBJ = "probe_eddy_ng btt_eddy"

def read_eddy_value():

    # Lee el valor del Eddy NG desde la API de Klipper (consulta stats)

    print("Lee el valor del Eddy NG desde la API de Klipper (consulta stats)")
    try:
        r = requests.get(
        f"{MOONRAKER}/printer/objects/query",
        params={OBJ: ""}
    )
        data = r.json()
        return data["last_z_result"]
    except:
        return None

def gcode(cmd):
    requests.post(
        f"{MOONRAKER}/printer/gcode/script",
        json={"script": cmd}
    ).raise_for_status()

def wait_idle():
    while True:
        r = requests.get(
            f"{MOONRAKER}/printer/objects/query",
            params={"toolhead": ""}
        ).json()
        if r["result"]["status"]["toolhead"]["status"] == "idle":
            break
        time.sleep(0.1)

def read_probe():
    r = requests.get(
        f"{MOONRAKER}/printer/objects/query",
        params={OBJ: ""}
    ).json()
    return r["result"]["status"][OBJ]["last_z_result"]


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
    gcode("PEPS")
    wait_idle()
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

    with open(OUTPUT / "EddyBedCheck.json", "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
