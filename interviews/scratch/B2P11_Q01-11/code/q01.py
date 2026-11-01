# TOY LLM tracer. Virtual clock, mock model, SYNTHETIC prices. Field names are illustrative, not the OpenTelemetry GenAI names.
import hashlib, json
from contextlib import contextmanager
PRICE = {"toy-model-v1": {"in": 0.50, "out": 1.50}}   # SYNTHETIC currency units per 1M tokens, price-table version below
PRICE_VERSION = "2026-10-synthetic"
class Tracer:
    def __init__(self, log_raw):
        self.log_raw, self.spans, self.stack, self.clock = log_raw, [], [], 0.0
    @contextmanager
    def span(self, name, kind, **attrs):
        s = {"id": len(self.spans) + 1, "parent": self.stack[-1] if self.stack else None, "name": name, "kind": kind, "start": self.clock, **attrs}
        self.spans.append(s); self.stack.append(s["id"])
        try: yield s
        except Exception as e: s["error"] = type(e).__name__; raise
        finally: s["end"] = self.clock; self.stack.pop()
    def record_text(self, s, key, text):
        s[key + "_len"] = len(text)
        s[key + "_sha256_12"] = hashlib.sha256(text.encode()).hexdigest()[:12]   # group identical prompts without storing them
        if self.log_raw: s[key] = text
def mock_llm(prompt):
    return "Refunds are allowed within 30 days.", {"in": len(prompt.split()) * 4, "out": 60}   # fake token counts
def handle(tr, user_q):
    with tr.span("request", "request", prompt_template="support_answer@v7", feature="support") as root:
        with tr.span("retrieve", "retrieval", top_k=3) as r:
            tr.clock += 0.12; r["docs_returned"] = 3
        prompt = "Context: refund policy text ... Question: " + user_q
        with tr.span("llm_call", "llm", model="toy-model-v1", temperature=0.2, prompt_template="support_answer@v7") as l:
            tr.record_text(l, "input", prompt)
            out, u = mock_llm(prompt); tr.clock += 0.90
            tr.record_text(l, "output", out)
            l.update(tokens_in=u["in"], tokens_out=u["out"], finish_reason="stop",
                     cost=(u["in"] * PRICE["toy-model-v1"]["in"] + u["out"] * PRICE["toy-model-v1"]["out"]) / 1e6, price_version=PRICE_VERSION)
        root["user_feedback"] = None   # filled later by a thumbs event keyed on the trace id
for log_raw in (True, False):
    tr = Tracer(log_raw); handle(tr, "My order 4471 arrived broken, can I get a refund? My email is a@b.example")
    print(f"--- log_raw={log_raw}")
    for s in tr.spans:
        show = {k: v for k, v in s.items() if k in ("name", "parent", "input_len", "input_sha256_12", "input", "tokens_in", "tokens_out", "cost")}
        print(f"span {s['id']} dur={s['end'] - s['start']:.2f}s", json.dumps(show))
tot = sum(s.get("cost", 0) for s in tr.spans)
print(f"request cost (synthetic units): {tot:.8f}")
