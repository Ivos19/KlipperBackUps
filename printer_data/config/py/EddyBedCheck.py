#!/usr/bin/env python3
import sys
import requests
import json
from pathlib import Path
from datetime import datetime

OUTPUT = Path("/home/biqu/printer_data/config/py")
MOONRAKER = "http://127.0.0.1:7125"
OBJ = "probe_eddy_ng btt_eddy"


def read_eddy_value():
    print("Leyendo valor Eddy NG desde Moonraker")
    try:
        r = requests.get(
            f"{MOONRAKER}/printer/objects/query",
            params={OBJ: ""},
            timeout=2
        )
        r.raise_for_status()
        data = r.json()

        return data["result"]["status"][OBJ]["last_z_result"]

    except Exception as e:
        print("ERROR leyendo Eddy:", e)
        return None


def main():
    print("Main py script")

    if len(sys.argv) != 7:
        print(f"ARGS INVALIDOS: esperaba 6, recibí {len(sys.argv)-1}")
        print("Argumentos recibidos:", sys.argv)
        return

    nx, ny, sx, sy, ztarget, cycle = sys.argv[1:]
    nx, ny = float(nx), float(ny)
    sx, sy = float(sx), float(sy)
    ztarget = float(ztarget)
    cycle = int(cycle)

    value = read_eddy_value()

    OUTPUT.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "cycle": cycle,
        "nozzle": [nx, ny],
        "sensor": [sx, sy],
        "target_z": ztarget,
        "eddy": value
    }

    with open(OUTPUT / "EddyBedCheck.json", "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
