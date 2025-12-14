#!/usr/bin/env python3
import sys

# Check if enough arguments were passed
if len(sys.argv) > 3:
    param1 = sys.argv[1]
    param2 = sys.argv[2]
    param3 = sys.argv[3]

    # Perform actions with the parameters
    print(f"Received parameter 1: {param1}")
    print(f"Received parameter 2: {param2}")
    print(f"Received parameter 3: {param3}")
else:
    print("Error: Not enough parameters provided.")