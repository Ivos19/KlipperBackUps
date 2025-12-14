#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode

OUTPUT = Path("/home/biqu/printer_data/config/py")
MOONRAKER = "http://127.0.0.1:7125"
OBJ = "probe_eddy_ng btt_eddy"

def moonraker_query(params):
    qs = urlencode(params)
    with urlopen(f"{MOONRAKER}/printer/objects/query?{qs}") as r:
        return json.loads(r.read())

def read_eddy_value():
    data = moonraker_query({OBJ: ""})
    try:
        return data["result"]["status"][OBJ]["last_z_result"]
    except KeyError:
        return None

def wait_idle():
    while True:
        data = moonraker_query({"toolhead": ""})
        if data["result"]["status"]["toolhead"]["status"] == "idle":
            return
        time.sleep(0.1)

def main():
    print("Main py script")

    if len(sys.argv) != 7:
        print(f"ARGS INVALIDOS: esperaba 7, recibí {len(sys.argv)}")
        print(sys.argv)
        return

    nx, ny, sx, sy, ztarget, cycle = sys.argv[1:]
    nx, ny = float(nx), float(ny)
    sx, sy = float(sx), float(sy)
    ztarget = float(ztarget)
    cycle = int(cycle)

    wait_idle()
    value = read_eddy_value()

    OUTPUT.mkdir(parents=True, exist_ok=True)

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

    print("EDDY_TEST OK:", value)

if __name__ == "__main__":
    main()