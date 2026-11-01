"""Q41: Lambda-style inference handler, lazy model load, cold vs warm counting. Pure Python, no AWS."""
import json, os, tempfile

MODEL_PATH = os.environ.get("MODEL_PATH", "/opt/ml/model.json")   # layer/image path in real life; env var keeps it testable
_MODEL = None          # module-level cache: survives between invocations in the same execution environment
LOADS = 0              # test-only counter

def load_model(path):
    global LOADS
    LOADS += 1                                   # in real life: this is the slow part (read file, build object)
    with open(path) as f:
        return json.load(f)

def get_model():
    global _MODEL
    if _MODEL is None:                           # first call in this container = cold; later calls reuse
        _MODEL = load_model(MODEL_PATH)
    return _MODEL

def predict(model, features):                    # plain function: unit-testable, no event or context
    z = model["bias"] + sum(w * x for w, x in zip(model["weights"], features))
    return 1.0 / (1.0 + 2.718281828459045 ** (-z))

def handler(event, context=None):                # thin wrapper: parse, validate, call predict, shape response
    try:
        body = json.loads(event["body"]) if isinstance(event.get("body"), str) else event
        feats = [float(v) for v in body["features"]]
    except (KeyError, ValueError, TypeError):
        return {"statusCode": 400, "body": json.dumps({"error": "need numeric 'features'"})}
    model = get_model()
    if len(feats) != len(model["weights"]):
        return {"statusCode": 400, "body": json.dumps({"error": f"expected {len(model['weights'])} features"})}
    return {"statusCode": 200, "body": json.dumps({"score": round(predict(model, feats), 4)})}

def simulate_new_container():                    # what a cold start does to module state
    global _MODEL
    _MODEL = None

if __name__ == "__main__":
    d = tempfile.mkdtemp()
    MODEL_PATH = os.path.join(d, "model.json")
    json.dump({"weights": [0.5, -0.25], "bias": 0.0}, open(MODEL_PATH, "w"))
    # unit test of the pure function (hand check: z = 0.5*2 - 0.25*4 = 0 -> sigmoid(0) = 0.5)
    assert predict({"weights": [0.5, -0.25], "bias": 0.0}, [2, 4]) == 0.5
    ev = {"body": json.dumps({"features": [2, 4]})}
    print("loads before any call:", LOADS)
    r1 = handler(ev); print("call 1 (cold):", r1, "| loads =", LOADS)
    for _ in range(4): handler(ev)
    print("calls 2-5 (warm): loads =", LOADS)
    simulate_new_container()
    handler(ev); print("after new container, call 6: loads =", LOADS)
    print("bad body:", handler({"body": "{}"}))
    print("wrong length:", handler({"features": [1]}))
    assert LOADS == 2
    # size budget helper: what goes into the package
    sizes = {"model.json": os.path.getsize(MODEL_PATH), "handler.py": os.path.getsize(__file__)}
    print("package bytes:", sizes)
