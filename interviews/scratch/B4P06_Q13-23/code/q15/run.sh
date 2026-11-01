. "$(dirname "$0")/../env.sh"; D=$(cd "$(dirname "$0")" && pwd)
cd $D && $PY -I -m pytest -q -p no:cacheprovider --rootdir=$D test_capacity.py 2>&1 | tail -4
export MODEL_PATH=$W/model/iris.onnx
cd $D/..; PYTHONPATH=$D/.. $PY -m uvicorn serve_app:app --port 8213 --log-level warning > $W/q15_uvicorn.log 2>&1 &
SRV=$!
for i in $(seq 30); do curl -sf localhost:8213/readyz >/dev/null && break; sleep 0.3; done
curl -s localhost:8213/readyz; echo
$PY -I $D/measure.py http://localhost:8213
kill $SRV; wait $SRV 2>/dev/null; sleep 0.5; echo "server stopped"
