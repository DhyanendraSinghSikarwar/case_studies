# Tracing decorator: nested spans (contextvars), timing, tokens, cost from a price table, error capture, pluggable exporter.
import contextvars, functools, itertools, json, time
PRICES = {"mock-small": {"in": 0.50, "out": 1.50}}      # ASSUMED prices per 1M tokens, version-tagged below
PRICE_VERSION = "2026-01-demo"
_current = contextvars.ContextVar("span", default=None)
_ids = itertools.count(1)
class ListExporter:
    def __init__(self): self.spans = []
    def export(self, span): self.spans.append(span)
class JsonlExporter:
    def __init__(self): self.lines = []
    def export(self, span): self.lines.append(json.dumps(span, sort_keys=True))
EXPORTER = ListExporter()
def traced(name=None, kind="span", model=None):
    def deco(fn):
        @functools.wraps(fn)
        def wrap(*a, **kw):
            parent = _current.get()
            span = {"span_id": f"s{next(_ids)}", "parent_id": parent["span_id"] if parent else None,
                    "trace_id": parent["trace_id"] if parent else f"t{next(_ids)}", "name": name or fn.__name__, "kind": kind}
            tok = _current.set(span); t0 = time.perf_counter()
            try:
                out = fn(*a, **kw)
                if kind == "llm" and isinstance(out, dict) and "usage" in out:
                    u = out["usage"]; p = PRICES[model]
                    span.update(model=model, tokens_in=u["in"], tokens_out=u["out"], price_version=PRICE_VERSION,
                                cost_usd=(u["in"] * p["in"] + u["out"] * p["out"]) / 1e6)
                span["status"] = "ok"; return out
            except Exception as e:
                span["status"] = "error"; span["error"] = type(e).__name__ + ": " + str(e)[:80]; raise       # do not log raw prompts or secrets in the message
            finally:
                span["duration_ms"] = (time.perf_counter() - t0) * 1000; _current.reset(tok); EXPORTER.export(span)
        return wrap
    return deco
# ---- mock model and pipeline
calls = {"n": 0}
@traced("llm.generate", kind="llm", model="mock-small")
def llm(prompt, fail=False):
    calls["n"] += 1
    if fail: raise TimeoutError("provider timed out")
    return {"text": "answer", "usage": {"in": len(prompt.split()), "out": 20}}
@traced("retrieve", kind="retrieval")
def retrieve(q): return ["doc1", "doc2"]
@traced("pipeline")
def pipeline(q, fail_first=False):
    docs = retrieve(q)
    try: return llm(" ".join(docs) + " " + q, fail=fail_first)
    except TimeoutError: return llm(" ".join(docs) + " " + q)             # retry becomes a second sibling span
# ---- tests
pipeline("what is the refund window for annual plans")
sp = EXPORTER.spans; by = {s["name"]: s for s in sp}
assert by["retrieve"]["parent_id"] == by["pipeline"]["span_id"] and by["llm.generate"]["parent_id"] == by["pipeline"]["span_id"]
assert by["pipeline"]["parent_id"] is None and len({s["trace_id"] for s in sp}) == 1
g = by["llm.generate"]; assert g["tokens_in"] == 2 + 8 and abs(g["cost_usd"] - (10 * 0.5 + 20 * 1.5) / 1e6) < 1e-12
print("export order (children finish first):", [s["name"] for s in sp])
print("llm span:", {k: g[k] for k in ["tokens_in", "tokens_out", "cost_usd", "price_version", "status"]})
EXPORTER = ListExporter(); pipeline("q", fail_first=True)
st = [(s["name"], s["status"]) for s in EXPORTER.spans]; print("with a failing first call:", st)
assert ("llm.generate", "error") in st and ("llm.generate", "ok") in st and EXPORTER.spans[-1]["status"] == "ok"
err = [s for s in EXPORTER.spans if s["status"] == "error"][0]["error"]; print("captured error:", err)
EXPORTER = JsonlExporter(); pipeline("hello world"); print("jsonl lines:", len(EXPORTER.lines), "| first line keys:", sorted(json.loads(EXPORTER.lines[0]).keys()))
print("all tests passed")
