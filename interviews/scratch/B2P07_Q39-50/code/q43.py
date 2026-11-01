# Standalone, stdlib only. ALL MOCK: tools, planner and "LLM" are canned; a fake clock stands in for wall time. Shows the control flow, budgets and fallbacks.
import unittest
KB = {"claims_2023": "2023 claims paid: 120 on premiums 1000", "claims_2022": "2022 claims paid: 90 on premiums 1000",
      "policy": "Claims above 100 need a manager sign-off"}
class Clock:
    def __init__(self): self.t = 0.0
    def tick(self, s): self.t += s
    def now(self): return self.t

def mock_search(query):                                     # MOCK retrieval tool; returns (doc_id, text) or None; costs fake tokens/time
    for k, v in KB.items():
        if all(w in (k + " " + v).lower() for w in query.lower().split()): return {"id": k, "text": v, "tokens": 50, "secs": 1.0}
    return None
def mock_plan(question):                                    # MOCK planner: fixed decomposition for one known multi-hop question
    if question == "claim ratio 2023 vs 2022": return ["claims_2023", "claims_2022"]
    return [question]
def route(question): return "multihop" if " vs " in question else "single"

class Agent:
    def __init__(self, max_steps=4, max_tokens=300, max_secs=10, clock=None, tool=mock_search, high_stakes=False):
        self.max_steps, self.max_tokens, self.max_secs = max_steps, max_tokens, max_secs
        self.clock, self.tool, self.high_stakes = clock or Clock(), tool, high_stakes
        self.log = []                                       # observability: every step and the final stop reason
    def single_pass(self, q):
        hit = self.tool(q); return {"status": "partial", "answer": hit["text"] if hit else None, "stop": "fallback_single_pass"} if hit else {"status": "abstain", "answer": None, "stop": "no_evidence"}
    def run(self, q):
        if self.high_stakes: return self._end({"status": "handoff", "answer": None, "stop": "high_stakes_human"})
        if route(q) == "single":
            r = self.single_pass(q); r["status"] = "answered" if r["answer"] else r["status"]; return self._end(r)
        t0, tokens, evidence, seen = self.clock.now(), 0, {}, set()
        for step, sub in enumerate(mock_plan(q), 1):
            if step > self.max_steps: return self._end(self._fallback(q, evidence, "step_budget"))
            if tokens >= self.max_tokens: return self._end(self._fallback(q, evidence, "token_budget"))
            if self.clock.now() - t0 >= self.max_secs: return self._end(self._fallback(q, evidence, "time_budget"))
            if sub in seen: return self._end(self._fallback(q, evidence, "loop_detected"))
            seen.add(sub)
            try: hit = self.tool(sub)
            except Exception as e: self.log.append({"step": step, "sub": sub, "error": str(e)}); return self._end(self._fallback(q, evidence, "tool_error"))
            if hit: tokens += hit["tokens"]; self.clock.tick(hit["secs"]); evidence[sub] = hit
            self.log.append({"step": step, "sub": sub, "found": bool(hit), "tokens": tokens})
        if not self.verify(evidence): return self._end({"status": "abstain", "answer": None, "stop": "verifier_failed"})
        return self._end({"status": "answered", "answer": self.synthesise(evidence), "stop": "done", "cites": sorted(evidence)})
    def verify(self, evidence): return len(evidence) == len(mock_plan("claim ratio 2023 vs 2022")) and all(e["text"] for e in evidence.values())   # MOCK verifier: every sub-question has evidence
    def synthesise(self, ev): return "claim ratio 2023 = 12%, 2022 = 9% (from " + ", ".join(sorted(ev)) + ")"            # MOCK synthesiser
    def _fallback(self, q, evidence, why):
        if len(evidence) >= 1: return {"status": "partial", "answer": "partial: " + "; ".join(e["text"] for e in evidence.values()), "stop": why}
        return {"status": "abstain", "answer": None, "stop": why}
    def _end(self, r): self.log.append({"final": r["stop"]}); return r

class T(unittest.TestCase):
    Q = "claim ratio 2023 vs 2022"
    def test_happy_path(self):
        r = Agent().run(self.Q); self.assertEqual((r["status"], r["stop"]), ("answered", "done")); self.assertEqual(r["cites"], ["claims_2022", "claims_2023"])
    def test_simple_question_uses_single_pass(self): a = Agent(); r = a.run("policy"); self.assertEqual((r["status"], r["stop"]), ("answered", "fallback_single_pass")); self.assertEqual(len(a.log), 1)   # one log line, no planner steps
    def test_step_budget(self): r = Agent(max_steps=1).run(self.Q); self.assertEqual((r["status"], r["stop"]), ("partial", "step_budget"))
    def test_token_budget(self): r = Agent(max_tokens=50).run(self.Q); self.assertEqual(r["stop"], "token_budget"); self.assertEqual(r["status"], "partial")
    def test_time_budget(self): r = Agent(max_secs=1.0).run(self.Q); self.assertEqual(r["stop"], "time_budget")
    def test_tool_error_falls_back_not_crashes(self):
        def boom(q): raise RuntimeError("timeout")
        r = Agent(tool=boom).run(self.Q); self.assertEqual((r["status"], r["stop"]), ("abstain", "tool_error"))
    def test_missing_evidence_abstains(self):
        r = Agent(tool=lambda q: mock_search(q) if "2023" in q else None).run(self.Q); self.assertEqual((r["status"], r["stop"]), ("abstain", "verifier_failed"))
    def test_high_stakes_goes_to_human(self): self.assertEqual(Agent(high_stakes=True).run(self.Q)["status"], "handoff")
    def test_no_evidence_single(self): self.assertEqual(Agent().run("zzz unknown")["status"], "abstain")
    def test_every_run_logs_a_stop_reason(self): a = Agent(); a.run(self.Q); self.assertIn("final", a.log[-1])
if __name__ == "__main__":
    a = Agent(); print(a.run("claim ratio 2023 vs 2022")); print(a.log)
    print("budget 1 step ->", Agent(max_steps=1).run("claim ratio 2023 vs 2022"))
    unittest.main(argv=["x"], verbosity=1)
