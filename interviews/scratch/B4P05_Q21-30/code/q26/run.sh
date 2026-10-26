#!/bin/bash
# Q26 driver: compile with kfp 2.17.3 + kfp-kubernetes 2.17.3 (venv kfk), then inspect the YAML. No cluster.
D=/tmp/claude-0/b5p05_q21_30/q26; HERE=$(cd "$(dirname "$0")" && pwd); K=/tmp/claude-0/b5p05_q21_30/kfk/bin
rm -rf $D; mkdir -p $D; cp $HERE/pipeline.py $HERE/inspect_yaml.py $D/; cd $D
$K/pip list 2>/dev/null | grep -E "^kfp(-kubernetes)? "
$K/python -I pipeline.py
$K/python -I inspect_yaml.py
cp pipeline.yaml $HERE/pipeline.yaml
