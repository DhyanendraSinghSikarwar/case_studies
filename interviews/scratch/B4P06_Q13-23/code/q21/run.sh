. "$(dirname "$0")/../env.sh"; D=$(cd "$(dirname "$0")" && pwd)
$PY -I $D/nosrv.py
export MODEL_PATH=$W/model/iris.onnx
cd $D; $PY -m uvicorn mock_v2:app --port 8221 --log-level warning > $W/q21.log 2>&1 &
SRV=$!
for i in $(seq 30); do curl -sf localhost:8221/v2/health/ready >/dev/null && break; sleep 0.3; done
echo '--- curl, raw v2 JSON:'
curl -s -XPOST localhost:8221/v2/models/iris_onnx/infer -H 'content-type: application/json' \
 -d '{"inputs":[{"name":"X","shape":[2,4],"datatype":"FP32","data":[6.7,3.0,5.2,2.3,5.1,3.5,1.4,0.2]}]}'; echo
echo '--- tritonclient.http:'
$PY -I $D/client.py
kill $SRV; wait $SRV 2>/dev/null; echo "server stopped"
