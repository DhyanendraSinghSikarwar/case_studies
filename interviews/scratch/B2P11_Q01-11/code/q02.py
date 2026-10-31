# TOY trace for: retrieve -> rerank -> llm (fails once, retried) -> tool call -> llm. Virtual clock; durations are SYNTHETIC.
# Attribute names are illustrative; check the live OpenTelemetry GenAI conventions for the real ones.
import itertools
ids = itertools.count(1)
clock = 0.0
spans = []
def run(name, kind, dur=0.0, parent=None, children=None, **attrs):
    """Open a span, advance the clock by own work `dur`, run children, close."""
    global clock
    s = {"span_id": next(ids), "parent_id": parent, "name": name, "kind": kind, "start": clock, **attrs}
    spans.append(s)
    clock += dur
    if children: children(s["span_id"])
    s["end"] = clock
    return s
def pipeline(pid):
    run("retrieve", "retrieval", 0.15, pid, top_k=20)
    run("rerank", "rerank", 0.08, pid, kept=4)
    run("llm_call", "llm", 0.30, pid, attempt=1, model="toy-model", error="Timeout", finish_reason=None)   # failed attempt
    run("backoff_sleep", "wait", 0.50, pid)
    run("llm_call", "llm", 0.95, pid, attempt=2, model="toy-model", tokens_in=900, tokens_out=120, finish_reason="tool_calls", prompt_version="qa@v3")
    run("tool:get_order", "tool", 0.20, pid, tool="get_order", ok=True)
    run("llm_call", "llm", 0.70, pid, attempt=1, model="toy-model", tokens_in=1100, tokens_out=80, finish_reason="stop", prompt_version="qa@v3")
root = run("request", "request", 0.02, None, children=pipeline, trace_id="t-0001")
def depth(s):
    d = 0; p = s["parent_id"]
    while p: d += 1; p = next(x for x in spans if x["span_id"] == p)["parent_id"]
    return d
print("trace_id=t-0001 (one trace, many spans; parent_id links them)")
for s in spans:
    dur = s["end"] - s["start"]
    child = sum(c["end"] - c["start"] for c in spans if c["parent_id"] == s["span_id"])
    extra = {k: v for k, v in s.items() if k in ("attempt", "error", "finish_reason", "tokens_in", "tokens_out")}
    print(f"{'  ' * depth(s)}{s['name']:14} dur={dur:.2f}s self={dur - child:.2f}s {extra if extra else ''}")
llm = [s for s in spans if s["kind"] == "llm"]
wasted = sum(s["end"] - s["start"] for s in llm if s.get("error")) + sum(s["end"] - s["start"] for s in spans if s["kind"] == "wait")
print(f"llm spans: {len(llm)}; total tokens in/out on successful spans: {sum(s.get('tokens_in', 0) for s in llm)}/{sum(s.get('tokens_out', 0) for s in llm)}")
print(f"time lost to the failed attempt + backoff: {wasted:.2f}s of {root['end']-root['start']:.2f}s")
