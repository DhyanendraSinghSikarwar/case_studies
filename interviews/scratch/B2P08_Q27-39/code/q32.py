# MINI state-graph runner: nodes (functions that update a shared state dict), edges, conditional edges, checkpoints,
# and a human-approval pause. This shows what a graph framework does underneath; it is NOT any real framework's API.
import copy, json

class Graph:
    def __init__(self): self.nodes, self.edges, self.cond = {}, {}, {}
    def node(self, name, fn): self.nodes[name] = fn; return self
    def edge(self, a, b): self.edges[a] = b; return self
    def conditional(self, a, router): self.cond[a] = router; return self    # router(state) -> next node name or "END"
    def run(self, start, state, checkpoints, max_steps=20, resume=False):
        cur = start
        for _ in range(max_steps):
            if cur == "END": return state
            out = self.nodes[cur](state)
            if out == "PAUSE":                                  # human-in-the-loop: save state and stop
                checkpoints.append({"next": cur, "state": copy.deepcopy(state)}); return None
            state.update(out)
            nxt = self.cond[cur](state) if cur in self.cond else self.edges[cur]
            checkpoints.append({"next": nxt, "state": copy.deepcopy(state)})   # checkpoint after every node
            cur = nxt
        raise RuntimeError("max_steps exceeded")                # frameworks also need a recursion/step limit

# mock "agent" nodes: deterministic stand-ins for LLM calls
def draft(s):   return {"draft": f"refund {s['amount']} for {s['order']}", "tries": s.get("tries", 0) + 1}
def check(s):   return {"ok": s["amount"] <= 100}
def approve(s):
    if not s.get("human_ok"): return "PAUSE"
    return {}
def send(s):    return {"sent": True}
def reject(s):  return {"sent": False}

g = (Graph().node("draft", draft).node("check", check).node("approve", approve).node("send", send).node("reject", reject)
     .edge("draft", "check")
     .conditional("check", lambda s: "approve" if s["ok"] else "reject")
     .edge("approve", "send").edge("send", "END").edge("reject", "END"))

cps = []
res = g.run("draft", {"order": "ORD-1", "amount": 40}, cps)
print("paused for human:", res is None, "| paused before node:", cps[-1]["next"])
saved = cps[-1]                                    # resume later from the checkpoint with the human's decision
state = dict(saved["state"], human_ok=True)
final = g.run(saved["next"], state, [])
print("after approval:", {k: final[k] for k in ("draft", "ok", "sent")})
big = g.run("draft", {"order": "ORD-2", "amount": 500}, [])
print("conditional edge, large amount:", {k: big[k] for k in ("ok", "sent")})
print("checkpoints in first run:", len(cps), "->", [c["next"] for c in cps])
assert final["sent"] is True and big["sent"] is False and json.dumps(cps)    # state is plain, serialisable data
print("tests passed")
