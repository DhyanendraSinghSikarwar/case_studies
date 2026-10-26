#!/bin/bash
# Q27 driver: kubernetes-validate on a sketch pod; compile a pipeline with retry/caching/limits; check SDK client methods exist. No cluster.
D=/tmp/claude-0/b5p05_q21_30/q27; HERE=$(cd "$(dirname "$0")" && pwd); K=/tmp/claude-0/b5p05/kf/bin
rm -rf $D; mkdir -p $D; cp $HERE/*.py $HERE/step_pod.yaml $D/; cd $D
kubernetes-validate --strict step_pod.yaml 2>&1 | tail -3; echo "kubernetes-validate exit: ${PIPESTATUS[0]}"
$K/python -I pipeline_ops.py
