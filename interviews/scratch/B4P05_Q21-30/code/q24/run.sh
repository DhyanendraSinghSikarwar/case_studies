#!/bin/bash
# Q24 driver: (1) run the flow locally with different parameters; (2) real local Prefect server + flow.serve + one triggered run.
D=/tmp/claude-0/b5p05_q21_30/q24; HERE=$(cd "$(dirname "$0")" && pwd); P=/tmp/claude-0/b5p05/pf/bin
rm -rf $D; mkdir -p $D/home; cp $HERE/*.py $D/; cd $D
export PREFECT_HOME=$D/home PREFECT_SERVER_ANALYTICS_ENABLED=false
echo "--- (1) local runs, no server configured (ephemeral API inside the process)"
$P/python -I train_flow.py 2>&1 | grep -E "rows=|^trained|^skipped|bad parameter"
echo "--- (2) server + flow.serve"
export PREFECT_API_URL=http://127.0.0.1:4299/api
nohup $P/prefect server start --port 4299 > server.log 2>&1 &
SERVER=$!; for i in $(seq 40); do curl -s localhost:4299/api/health >/dev/null && break; sleep 1; done
nohup $P/python serve_it.py > serve.log 2>&1 &
SERVE=$!; sleep 15
$P/prefect deployment run train/nightly --param rows=7 --param dry_run=true 2>&1 | grep -E "Created flow run|Parameters"
sleep 12
grep -E "rows=|Finished in state Completed\(\)" serve.log | grep "Flow run" | cut -c1-160
$P/prefect deployment inspect train/nightly 2>&1 | grep -E "'cron'|'parameters': \{'rows'|'tags'|'work_pool_name'"
kill $SERVE $SERVER 2>/dev/null; sleep 3; kill -9 $SERVE $SERVER 2>/dev/null
echo "--- (3) prefect.yaml parses and its entrypoint points at a real function (nothing deployed)"
cp $HERE/prefect.yaml $HERE/check_yaml.py $D/; cd $D && python3 -I check_yaml.py
