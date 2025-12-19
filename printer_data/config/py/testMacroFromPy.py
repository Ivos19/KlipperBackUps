import requests

MOONRAKER_URL = "http://127.0.0.1:7125"

macro = "TEST_MACRO"

payload = {
    "script": macro
}

print("--Enviando macro a Klipper...")

requests.post(
    f"{MOONRAKER_URL}/printer/gcode/script",
    json=payload,
    timeout=5
)
