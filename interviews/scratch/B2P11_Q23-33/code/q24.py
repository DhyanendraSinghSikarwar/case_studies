# TOY: tool gateway for an agent: scopes, per-user credentials, allowlist, caps, approval, tamper-evident audit.
import hashlib, json, time

TOOLS = {"search_orders": {"kind": "read"}, "get_invoice": {"kind": "read"},
         "issue_refund": {"kind": "write", "needs_approval_over": 50.0, "max_amount": 500.0},
         "delete_account": {"kind": "write", "needs_approval_over": 0.0}}
POLICY = {"alice": {"allowed": {"search_orders", "get_invoice", "issue_refund"}, "daily_spend_cap": 120.0, "max_calls": 7}}

class Gateway:
    def __init__(self):
        self.log, self.spent, self.calls, self.prev = [], {}, {}, "0" * 8
    def _audit(self, rec):
        rec["prev"] = self.prev
        h = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:8]
        rec["hash"] = h; self.prev = h; self.log.append(rec)
    def call(self, user, tool, args, approved_by=None):
        pol = POLICY[user]; t = TOOLS.get(tool); amt = float(args.get("amount", 0))
        self.calls[user] = self.calls.get(user, 0) + 1
        if t is None or tool not in pol["allowed"]: d = "deny:not-allowlisted"
        elif self.calls[user] > pol["max_calls"]: d = "deny:rate-cap"
        elif t["kind"] == "write" and amt > t.get("max_amount", 0): d = "deny:over-hard-limit"
        elif t["kind"] == "write" and self.spent.get(user, 0) + amt > pol["daily_spend_cap"]: d = "deny:spend-cap"
        elif t["kind"] == "write" and amt > t["needs_approval_over"] and not approved_by: d = "pending:human-approval"
        else:
            d = "allow"
            if t["kind"] == "write": self.spent[user] = self.spent.get(user, 0) + amt
        self._audit({"user": user, "tool": tool, "args": args, "decision": d, "approved_by": approved_by})
        return d
    def verify(self):
        prev = "0" * 8
        for r in self.log:
            body = {k: v for k, v in r.items() if k != "hash"}
            if body["prev"] != prev or hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:8] != r["hash"]: return False
            prev = r["hash"]
        return True

g = Gateway()
plan = [("search_orders", {"q": "order 17"}, None), ("issue_refund", {"amount": 20}, None),
        ("issue_refund", {"amount": 80}, None), ("issue_refund", {"amount": 80}, "carol"),
        ("issue_refund", {"amount": 80}, "carol"), ("delete_account", {"id": 9}, None),
        ("issue_refund", {"amount": 900}, "carol"), ("get_invoice", {"id": 3}, None)]
for tool, args, appr in plan:
    print(f"{tool:15} {str(args):22} approver={str(appr):5} -> {g.call('alice', tool, args, appr)}")
print("spent by alice:", g.spent["alice"], "| audit entries:", len(g.log), "| chain valid:", g.verify())
g.log[2]["args"]["amount"] = 8        # attacker edits history
print("after editing entry 2, chain valid:", g.verify())
