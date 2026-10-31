D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q23.XXXX); cd $W
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
python3 -I "$D/make_model.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING"
echo "--- mlflow models predict (batch, CLI) ---"
python3 -I -c "import json;d=json.load(open('in_split.json'));print(json.dumps({'dataframe_split':d}))" > in_req.json
cat in_split.json; echo
echo "bare split file (no wrapper key):"
mlflow models predict -m models:/iris_clf@champion -i in_split.json -t json --env-manager local 2>&1 | grep "^mlflow.exceptions" | cut -c1-200
echo "wrapped file {\"dataframe_split\": ...}:"
mlflow models predict -m models:/iris_clf@champion -i in_req.json -t json --env-manager local 2>&1 | grep -v "INFO\|WARNING\|Downloading"
echo "--- mlflow models serve (localhost:5088) ---"
mlflow models serve -m models:/iris_clf@champion -p 5088 -h 127.0.0.1 --env-manager local > serve.log 2>&1 &
PID=$!
for i in $(seq 1 40); do curl -s http://127.0.0.1:5088/ping -o /dev/null -w "%{http_code}" 2>/dev/null | grep -q 200 && break; sleep 1; done
echo "GET /ping -> $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5088/ping)"
echo "dataframe_split:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d @in_req.json; echo
echo "dataframe_records:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"sepal length (cm)":6.7,"sepal width (cm)":3.0,"petal length (cm)":5.2,"petal width (cm)":2.3}]}'; echo
echo "missing column:"; curl -s -X POST http://127.0.0.1:5088/invocations -H 'Content-Type: application/json' -d '{"dataframe_records":[{"sepal length (cm)":6.7}]}' | cut -c1-260; echo
kill $PID; wait $PID 2>/dev/null
