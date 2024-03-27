#!/usr/bin/env python

import re
import sys

matrix = False
with open(sys.argv[1], "r") as fp:
    for line in fp:
        if line.startswith("["):
            continue
        elif line.startswith("MATRIX"):
            matrix = True
        elif matrix:
            if ";" in line:
                break
            res = re.split(r"\s+", line)
            print(f">{res[0].strip()}")
            print(f"{res[1].strip()}")
