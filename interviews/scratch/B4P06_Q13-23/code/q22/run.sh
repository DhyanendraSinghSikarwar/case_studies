. "$(dirname "$0")/../env.sh"; D=$(cd "$(dirname "$0")" && pwd)
export BENTOML_HOME=$W/q22_home; rm -rf $BENTOML_HOME $W/q22_proj; mkdir -p $W/q22_proj
cp $D/service.py $D/bentofile.yaml $W/model/iris.onnx $W/q22_proj/
cd $W/q22_proj; export MODEL_PATH=$W/q22_proj/iris.onnx; BIN=$(dirname $PY)
$BIN/bentoml serve service:Iris --port 8222 > $W/q22_serve.log 2>&1 &
SRV=$!
for i in $(seq 60); do curl -sf localhost:8222/readyz >/dev/null && break; sleep 0.5; done
echo "livez: $(curl -s -o /dev/null -w '%{http_code}' localhost:8222/livez)  readyz: $(curl -s -o /dev/null -w '%{http_code}' localhost:8222/readyz)"
echo -n "predict [6.7,3.0,5.2,2.3] -> "; curl -s -XPOST localhost:8222/predict -H 'content-type: application/json' -d '{"features":[6.7,3.0,5.2,2.3]}'; echo
echo -n "bad input (a string instead of a list), HTTP status -> "; curl -s -o /dev/null -w '%{http_code}' -XPOST localhost:8222/predict -H 'content-type: application/json' -d '{"features":"oops"}'; echo
kill $SRV; wait $SRV 2>/dev/null; echo "server stopped"
echo '--- bentoml build'; $BIN/bentoml build -f bentofile.yaml 2>&1 | grep -E "Successfully|containerize"
echo '--- bentoml list'; $BIN/bentoml list 2>&1 | tail -4
