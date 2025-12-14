#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import urllib.request

MOONRAKER = "http://127.0.0.1:7125"
OBJ = "probe_eddy_ng btt_eddy"

OUTPUT = Path("/home/biqu/printer_data/config/py/EddyBedCheck.json")


def moonraker_get(path, params=None):
    if params:
        query = "&".join(f"{k}=" for k in params.keys())
        url = f"{MOONRAKER}{path}?{query}"
    else:
        url = f"{MOONRAKER}{path}"

    with urllib.request.urlopen(url, timeout=2) as r:
        return json.loads(r.read().decode())


def wait_idle():
    while True:
        r = moonraker_get("/printer/objects/query", {"toolhead": ""})

        status = (
            r.get("result", {})
             .get("status", {})
             .get("toolhead", {})
             .get("status")
        )

        if status == "idle":
            return

        time.sleep(0.1)


def read_eddy_value():
    r = moonraker_get("/printer/objects/query", {OBJ: ""})
    return r["result"]["status"][OBJ]["last_z_result"]


def main():
    print("Main py script")

    if len(sys.argv) != 7:
        print(f"ARGS INVALIDOS: esperaba 6, recibí {len(sys.argv)-1}")
        print("Recibido:", sys.argv)
        return

    nx, ny, sx, sy, ztarget, cycle = sys.argv[1:]
    nx, ny = float(nx), float(ny)
    sx, sy = float(sx), float(sy)
    ztarget = float(ztarget)
    cycle = int(cycle)

    # esperar a que PEPS termine realmente
    # wait_idle()

    value = read_eddy_value()
    print(f"Eddy Z = {value:.6f}")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "cycle": cycle,
        "nozzle": [nx, ny],
        "sensor": [sx, sy],
        "target_z": ztarget,
        "eddy": value
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    main()
