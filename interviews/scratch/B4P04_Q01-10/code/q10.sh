export PATH=/tmp/claude-0/ven/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1
HERE=$PWD
W=$(mktemp -d); cd $W
echo "=== A. plain file store, default settings"
python3 -I $HERE/q10_client.py file:./fs 2>&1 | grep -v -E 'WARN|warn' | tail -1 | cut -c1-330
echo "=== B. file store with MLFLOW_ALLOW_FILE_STORE=true"
MLFLOW_ALLOW_FILE_STORE=true python3 -I $HERE/q10_client.py file:./fs2 2>&1 | grep -v -E 'INFO|WARN|warn'
echo "    layout:"; (cd fs2; find . -maxdepth 2 | sed 's#/[0-9]\{10,\}#/<exp_id>#' | sort | head -6)
echo "=== C. sqlite backend"
python3 -I $HERE/q10_client.py sqlite:///mlflow.db 2>&1 | grep -v -E 'INFO|WARN|warn'
echo "    tables (sample):"; python3 -I -c "
import sqlite3; c=sqlite3.connect('mlflow.db')
t=[r[0] for r in c.execute(\"select name from sqlite_master where type='table'\")]
print(sorted(t)[:9], '... total', len(t))
print('runs in db:', c.execute('select count(*) from runs').fetchone()[0])"
echo "=== D. local tracking server on localhost:5081"
mlflow server --backend-store-uri sqlite:///srv.db --default-artifact-root ./art --host 127.0.0.1 --port 5081 > server.log 2>&1 &
SP=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5081/health >/dev/null && break; sleep 1; done
echo -n "    /health -> "; curl -s http://127.0.0.1:5081/health; echo
python3 -I $HERE/q10_client.py http://127.0.0.1:5081 2>&1 | grep -v -E 'INFO|WARN|warn|View'
echo "    artifact files on server disk:"; find art -type f | sed 's#^#    #'
kill $SP; wait $SP 2>/dev/null
