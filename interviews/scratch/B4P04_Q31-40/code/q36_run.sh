set -u; W=$1; rm -rf $W; mkdir -p $W; cd $W
export MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1
mlflow server --backend-store-uri sqlite:///$W/srv.db --artifacts-destination $W/art --host 127.0.0.1 --port 5081 > server.log 2>&1 &
PID=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5081/health >/dev/null && break; sleep 1; done
echo "health: $(curl -s http://127.0.0.1:5081/health)"
python -I $2 http://127.0.0.1:5081 $W 2>&1 | grep -v INFO
echo "--- files on the server side"; find $W/art -type f | sed "s#$W/##" | sed -E 's#[0-9a-f]{32}#<id>#g'
kill $PID; wait $PID 2>/dev/null
echo "--- mlflow db upgrade on the sqlite file (safe to re-run)"
mlflow db upgrade sqlite:///$W/srv.db 2>&1 | grep -v "^$" | tail -3
