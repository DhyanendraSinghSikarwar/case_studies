#!/bin/bash
# Q25 driver: real local Prefect runs (ephemeral API, own PREFECT_HOME).
D=/tmp/claude-0/b5p05_q21_30/q25; HERE=$(cd "$(dirname "$0")" && pwd); P=/tmp/claude-0/b5p05/pf/bin
rm -rf $D; mkdir -p $D/home; cp $HERE/ml_flow.py $D/; cd $D
export PREFECT_HOME=$D/home PREFECT_SERVER_ANALYTICS_ENABLED=false
$P/python -I ml_flow.py 2>&1 | grep -vE "telemetry|^\s|^Traceback|^ValueError|^See https|temporary server" | cut -c1-170 | sed -E "s/^[0-9:.]+ \| //"
