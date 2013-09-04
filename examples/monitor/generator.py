#!/usr/bin/python3

import json
import time
import numpy as np
import sys

while True:
    sys.stdout.write(json.dumps({
        "timestamp": time.time(),
        "value": np.random.randn()**3 * 150 + 300,
    }))
    sys.stdout.write("\n")
    sys.stdout.flush()

    time.sleep(0.2)

