# eddyc_test.py
# Script para registrar tests de repetibilidad del Eddy NG

import os
import time

class EddyCTest:
    def __init__(self, config):
        self.printer = config.get_printer()

        log_dir = "/home/pi/printer_data/logs"
        os.makedirs(log_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.log_path = f"{log_dir}/eddy_test_{timestamp}.txt"

        with open(self.log_path, "w") as f:
            f.write("Eddy NG Test\n")
            f.write("=========================\n\n")

    def record_point(self, nozzle_x, nozzle_y, sensor_x, sensor_y, z, reading):
        with open(self.log_path, "a") as f:
            f.write(
                f"Nozzle=({nozzle_x:.2f},{nozzle_y:.2f}), "
                f"Sensor=({sensor_x:.2f},{sensor_y:.2f}), "
                f"Z={z:.3f}, Eddy={reading}\n"
            )

    def record_message(self, msg):
        with open(self.log_path, "a") as f:
            f.write(msg + "\n")

def load_config(config):
    return EddyCTest(config)
