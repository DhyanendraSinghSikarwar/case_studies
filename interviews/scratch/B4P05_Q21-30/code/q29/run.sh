#!/bin/bash
# Q29 driver: compile a KFP pipeline to the YAML Vertex AI Pipelines accepts, inspect it; validate a Step Functions sketch. No cloud call.
D=/tmp/claude-0/b5p05_q21_30/q29; HERE=$(cd "$(dirname "$0")" && pwd); K=/tmp/claude-0/b5p05/kf/bin
rm -rf $D; mkdir -p $D; cp $HERE/*.py $HERE/states.json $D/; cd $D
$K/python -I compile_for_vertex.py && $K/python -I check_yaml.py
python3 -I check_asl.py
