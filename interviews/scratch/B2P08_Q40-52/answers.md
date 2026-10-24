### Q40 ⭐⭐ 🟡 What guardrails does an agent need (permission tiers, allowlists, sandboxing, output validation), and how do they differ from model-level safety?
**Asked at:** product, GCC, security-conscious teams
**Say this first (1 line):** An agent needs guardrails in code, outside the model: every tool call goes through a policy layer that checks the risk tier, a per-user and per-task allowlist, budgets and a kill switch, and the result is validated before the model sees it; model-level safety training only lowers the chance that the model asks for something bad, it cannot enforce anything.
**Then explain:**
- **Why code, not the model:** safety training is probabilistic and can be bypassed by injected text or odd inputs. A policy layer is deterministic: the same call is always allowed or always denied, it can be tested, and it works even if the model is fully fooled. This is the guardrails-vs-alignment split (Part 5 Q26), the layers view (Part 5 Q8), the refund architecture (Part 5 Q39) and the reliability stack (Part 3 Q38). Here I focus on the agent-specific controls.
- **Permission tiers:** classify every tool as read, write or destructive. Reads run freely, writes are logged and often need approval, destructive or irreversible actions (delete, send money, email externally) need a human yes. Anthropic's agents post (opened) says agents need testing in sandboxes with guardrails; the tier scheme itself is common practice, not a quote.
- **Allowlists at two levels:** the user's ceiling (what this person may ever do) and the task's list (what this run needs). A "summarise my tickets" task gets read tools only, even if the user is an admin. Least privilege limits the damage when the model is manipulated.
- **Sandboxing:** code or browser actions run in an isolated environment with no secrets (Q41, Q42).
- **Output validation:** check tool results against a schema before they re-enter the context, and validate the agent's final output (format, PII, policy) before it reaches the user or a downstream system. Treat tool results as untrusted text (Q52).
- **Rate and spend limits, and a kill switch:** cap calls and money per run and per user, and keep a switch ops can flip to stop a run or a whole tool at once. These bound runaway loops (Q4, Q48).
- **Order of checks:** kill switch, known tool, task allowlist, user tier, rate, spend, approval, then execute, validate the output, log. A denial returns a clear message the agent can act on.
- **Limit:** the policy layer cannot judge whether an allowed action is wise (a permitted `update_ticket` with wrong content). That needs evaluation and review.

**Example:** a helpdesk agent for an intern is asked to "clean up my old tickets". The model proposes `delete_records`. The task allowlist for "summarise tickets" has no delete tool, so the call is denied with "not in task allowlist". Even if the task allowed it, the intern's ceiling is write, and a delete is destructive, so it is denied again. Two independent checks, neither depends on the model behaving.

**Code:** (executed, standalone, stdlib only; MOCK: no LLM, the proposed calls are scripted; tests assert every deny reason)
```python
# Standalone, stdlib only. MOCK policy engine (no LLM): the agent's proposed calls are scripted dicts.
from dataclasses import dataclass, field
READ, WRITE, DESTRUCTIVE = 1, 2, 3
TIER = {"search_docs": READ, "get_ticket": READ, "update_ticket": WRITE,
        "send_email": WRITE, "delete_records": DESTRUCTIVE}          # tool -> risk tier
COST = {"search_docs": 0.01, "get_ticket": 0.01, "update_ticket": 0.02, "send_email": 0.05, "delete_records": 0.10}

@dataclass
class Policy:
    user_max_tier: int                      # per-user ceiling (what this person may do)
    task_allow: set                         # per-task allowlist (what THIS task needs)
    spend_limit: float = 0.10               # per-run budget in mock currency
    max_calls: int = 5                      # rate limit per run
    approval_tier: int = DESTRUCTIVE        # tiers at or above this need a human yes
    spent: float = 0.0; calls: int = 0; killed: bool = False
    log: list = field(default_factory=list)

    def check(self, tool, args, approved=False):
        def deny(why): self.log.append((tool, "DENY", why)); return False, why
        if self.killed:                       return deny("kill switch on")
        if tool not in TIER:                  return deny("unknown tool")
        if tool not in self.task_allow:       return deny("not in task allowlist")
        if TIER[tool] > self.user_max_tier:   return deny("above user's tier")
        if self.calls >= self.max_calls:      return deny("rate limit")
        if self.spent + COST[tool] > self.spend_limit + 1e-9: return deny("spend limit")
        if TIER[tool] >= self.approval_tier and not approved: return deny("needs human approval")
        self.calls += 1; self.spent += COST[tool]; self.log.append((tool, "ALLOW", "")); return True, "ok"

def validate_output(tool, out):               # output validation: schema check before the result goes back to the model
    if tool == "get_ticket": return isinstance(out, dict) and set(out) == {"id", "status"} and out["status"] in {"open", "closed"}
    return True

# ---- tests ----
p = Policy(user_max_tier=WRITE, task_allow={"search_docs", "get_ticket", "update_ticket", "delete_records"})
assert p.check("search_docs", {})[0]
assert p.check("update_ticket", {"id": 7})[0]
assert p.check("send_email", {}) == (False, "not in task allowlist")        # allowed for the product, not for this task
assert p.check("delete_records", {}, approved=True) == (False, "above user's tier")   # approval cannot lift a user's ceiling
assert p.check("rm_rf", {}) == (False, "unknown tool")
p2 = Policy(user_max_tier=DESTRUCTIVE, task_allow={"delete_records", "get_ticket"})
assert p2.check("delete_records", {}) == (False, "needs human approval")
assert p2.check("delete_records", {}, approved=True)[0]                      # spent 0.10 -> at the limit
assert p2.check("get_ticket", {}) == (False, "spend limit")
p3 = Policy(user_max_tier=READ, task_allow={"search_docs"}, spend_limit=9, max_calls=3)
res = [p3.check("search_docs", {})[0] for _ in range(5)]
assert res == [True, True, True, False, False] and p3.log[-1][2] == "rate limit"
p3.calls = 0; p3.killed = True
assert p3.check("search_docs", {}) == (False, "kill switch on")
assert validate_output("get_ticket", {"id": 1, "status": "open"}) and not validate_output("get_ticket", {"id": 1, "status": "hacked"})
for e in p2.log + p.log[:3]: print(e)
print("all policy tests passed")
```
Output of my run: the log lines show the destructive call denied until approved, then the next call denied by the spend limit, and the last line is `all policy tests passed`. The limits (0.10 spend, 5 calls) are made-up numbers.

**Follow-ups:**
- *Who sets the allowlist for a task?* The orchestrating code, from the task type, not the model. Letting the model grant itself tools defeats the point.
- *Are approvals enough for destructive actions?* No: show the human the exact arguments (not the model's summary), and let the policy still enforce the user's ceiling, as in my test where approval cannot lift it.
- *What does model-level safety still do?* It reduces how often the guardrails fire and handles content harms that a tool policy cannot see. I keep both (Part 5 Q26).

**Common mistakes:** relying on a system prompt line "never delete anything"; one global allowlist for all tasks; guardrails that check the model's words instead of the actual tool arguments; approval prompts that show a summary instead of the real call; no kill switch; spend limits only per month, not per run.
