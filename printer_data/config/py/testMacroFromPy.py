import requests

MOONRAKER_URL = "http://127.0.0.1:7125"

macro = "TEST_MACRO"

payload = {
    "script": macro
}

print("Enviando macro a Klipper...")

r = requests.post(
    f"{MOONRAKER_URL}/printer/gcode/script",
    json=payload,
    timeout=5
)

if r.status_code == 200:
    print("Macro ejecutado correctamente")
else:
    print("Error ejecutando macro")
    print(r.text)