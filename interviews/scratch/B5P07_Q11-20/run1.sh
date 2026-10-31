#!/bin/sh
# usage: sh run1.sh N  -> assembles and runs code/qN.py
cd "$(dirname "$0")/code" && cat prelude.py body_q$1.py > q$1.py && python3 -I q$1.py
