. "$(dirname "$0")/../env.sh"; D=$(cd "$(dirname "$0")" && pwd)
export MODEL_PATH=$W/model/iris.onnx
cd $D; PYTHONPATH=$D/..:$D $PY -m uvicorn app_stall:app --port 8216 --log-level warning > $W/q16_uvicorn.log 2>&1 &
SRV=$!
for i in $(seq 30); do curl -sf localhost:8216/readyz >/dev/null && break; sleep 0.3; done
$PY -I $D/loadgen.py http://localhost:8216
kill $SRV; wait $SRV 2>/dev/null; echo "server stopped"
