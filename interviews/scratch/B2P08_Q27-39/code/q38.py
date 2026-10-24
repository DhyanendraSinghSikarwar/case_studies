# Mock tracer: context-manager spans (run > step > llm/tool), redaction by hash, per-step latency/cost summary, replay from recorded tool results.
# Everything is a MOCK; times come from a fake clock so output is deterministic; prices are ASSUMED.
import hashlib, json, itertools
class Clock:                       # fake clock so the demo is deterministic
    t = 0.0
    @classmethod
    def advance(cls, s): cls.t += s
class Tracer:
    def __init__(self): self.spans, self.stack, self.ids = [], [], itertools.count(1)
    def span(self, kind, name, **attrs):
        tr = self
        class S:
            def __enter__(s):
                s.rec = dict(id=next(tr.ids), parent=tr.stack[-1] if tr.stack else None, kind=kind, name=name, start=Clock.t, attrs=dict(attrs), error=None)
                tr.stack.append(s.rec["id"]); return s.rec
            def __exit__(s, et, ev, tb):
                s.rec["end"] = Clock.t; s.rec["error"] = repr(ev) if ev else None
                tr.stack.pop(); tr.spans.append(s.rec); return False
        return S()
def h(text): return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:10]    # hash instead of storing raw prompt (privacy)
PRICE_PER_1K = 0.01                                                                # ASSUMED $ per 1k tokens
RECORDED = {}                                                                      # tool results saved for replay

def tool(tr, name, args, replay=None):
    with tr.span("tool", name, args=args) as sp:
        if replay is not None: result = replay[(name, json.dumps(args, sort_keys=True))]   # no real call during replay
        else:
            Clock.advance(0.5); result = {"temp_c": 31} if name == "weather" else {"ok": True}
            RECORDED[(name, json.dumps(args, sort_keys=True))] = result
        sp["attrs"]["result"] = result; return result
def llm(tr, prompt, tokens):
    with tr.span("llm", "mock-model", prompt_hash=h(prompt), tokens=tokens, cost=round(tokens / 1000 * PRICE_PER_1K, 5)):
        Clock.advance(1.0 + tokens / 1000)
        return "CALL weather" if "weather" in prompt and "RESULT" not in prompt else "It is 31 C."
def agent(tr, question, replay=None):
    with tr.span("run", "agent_run", question_hash=h(question)):
        with tr.span("step", "step1"):
            act = llm(tr, question, 400); r = tool(tr, "weather", {"city": "Pune"}, replay)
        with tr.span("step", "step2"):
            return llm(tr, question + " RESULT " + json.dumps(r), 600)

tr = Tracer(); Clock.t = 0.0
ans = agent(tr, "weather in Pune?")
steps = {s["id"]: s for s in tr.spans if s["kind"] == "step"}
print("answer:", ans)
for sid, s in sorted(steps.items()):
    kids = [c for c in tr.spans if c["parent"] == sid]
    cost = sum(c["attrs"].get("cost", 0) for c in kids)
    print(f"{s['name']}: latency={s['end'] - s['start']:.1f}s cost=${cost:.4f} children={[c['kind'] + ':' + c['name'] for c in kids]}")
print("redacted prompt attr:", [s["attrs"]["prompt_hash"] for s in tr.spans if s["kind"] == "llm"][0])
Clock.t = 0.0; tr2 = Tracer(); ans2 = agent(tr2, "weather in Pune?", replay=RECORDED)
print("replay gives same answer without calling tools:", ans2 == ans, "| replay tool spans:", sum(s["kind"] == "tool" for s in tr2.spans))
# error capture
t3 = Tracer()
try:
    with t3.span("tool", "boom"): raise TimeoutError("tool timed out")
except TimeoutError: print("error recorded on span:", t3.spans[0]["error"])
assert ans2 == ans and "weather in Pune" not in json.dumps(tr.spans) and t3.spans[0]["error"]
print("tests passed")
