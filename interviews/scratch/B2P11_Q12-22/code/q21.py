# TOY incident toolkit: flag, prompt label rollback, evidence freeze with hash, and incident -> eval case. All in memory, mock data.
import hashlib, json, re
flags = {"feature_on": True, "use_tools": True}
prompts = {"v1": "Answer briefly and cite the source.", "v2": "Answer in detail. Always call the tool first."}
labels = {"production": "v2"}
traces = [dict(id=i, prompt_ver=labels["production"], tokens=900 + (i % 3) * 50, status="ok", user_text="my email is bob@example.com, refund?") for i in range(5)]
# detection: rolling window rule on a metric (synthetic numbers)
window = [0.01, 0.01, 0.02, 0.09, 0.11, 0.12]        # error rate per minute
def breach(w, thr=0.05, k=3): return len(w) >= k and all(x > thr for x in w[-k:])
print("page on-call?", breach(window))
# first-hour actions, each reversible and logged
audit = []
def act(name, fn): fn(); audit.append(name)
act("set use_tools=False", lambda: flags.__setitem__("use_tools", False))
act("move production label v2 -> v1", lambda: labels.__setitem__("production", "v1"))
print("serving prompt:", prompts[labels["production"]], "| flags:", flags, "| audit:", audit)
# evidence preservation: copy suspect traces to a frozen store with a content hash, before TTL sweeps them
suspect = [t for t in traces if t["prompt_ver"] == "v2"]
blob = json.dumps(suspect, sort_keys=True)
frozen = dict(incident="INC-1", sha256=hashlib.sha256(blob.encode()).hexdigest()[:16], n=len(suspect))
print("frozen evidence:", frozen)
# incident -> eval case: mask PII, keep the failing input and the expectation
def mask(t): return re.sub(r"[\w.]+@[\w.]+", "<EMAIL>", t)
case = dict(id="inc1-001", input=mask(suspect[0]["user_text"]), must="not call the tool for plain refund questions", source="INC-1")
print("new eval case:", case)
