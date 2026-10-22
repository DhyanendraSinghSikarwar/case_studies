# Standalone policy gate for a refunds agent. No model involved: this is the deterministic
# layer that sits AFTER the model proposes a refund and BEFORE any money moves.
from dataclasses import dataclass, field
import hashlib, json, copy

ORDERS0 = {"A1": {"total": 120.0, "refunded": 0.0, "customer": "u1"},
          "B2": {"total": 80.0,  "refunded": 80.0, "customer": "u2"}}
APPROVAL_ABOVE = 50.0          # human approval above this amount (assumed policy)
DAILY_LIMIT = 200.0            # agent-wide spend limit per day (assumed policy)

@dataclass
class State:
    spent_today: float = 0.0
    seen_keys: dict = field(default_factory=dict)
    audit: list = field(default_factory=list)
    orders: dict = field(default_factory=lambda: copy.deepcopy(ORDERS0))

def idem_key(order_id, amount):
    return hashlib.sha256(json.dumps([order_id, round(amount, 2)]).encode()).hexdigest()[:12]

def check_refund(req, st):
    """Returns (decision, reason). decision in {'allow','needs_approval','deny'}. Fails closed."""
    try:
        oid, amt = req["order_id"], req["amount"]                # layer 1: schema-ish validation
        if not isinstance(oid, str) or isinstance(amt, bool) or not isinstance(amt, (int, float)):
            return "deny", "bad types"
        if set(req) - {"order_id", "amount", "idempotency_key"}: return "deny", "unknown fields"
        order = st.orders.get(oid)
        if order is None: return "deny", "unknown order"
        key = req.get("idempotency_key") or idem_key(oid, amt)   # layer 3: idempotency
        if key in st.seen_keys: return "deny", f"duplicate of earlier request {key}"
        if amt <= 0: return "deny", "amount must be positive"     # layer 2: business rules
        if order["refunded"] > 0: return "deny", "order already refunded"
        if amt > order["total"] - order["refunded"]: return "deny", "amount exceeds order total"
        if st.spent_today + amt > DAILY_LIMIT: return "deny", "daily spend limit"   # layer 4
        if amt > APPROVAL_ABOVE: return "needs_approval", "above approval threshold"  # layer 5
        return "allow", "ok"
    except Exception as e:                                       # fail closed
        return "deny", f"error: {type(e).__name__}"

def process(req, st, approved=False):
    d, why = check_refund(req, st)
    if d == "needs_approval" and approved: d, why = "allow", "human approved"
    if d == "allow":
        key = req.get("idempotency_key") or idem_key(req["order_id"], req["amount"])
        st.seen_keys[key] = req["amount"]; st.spent_today += req["amount"]
        st.orders[req["order_id"]]["refunded"] += req["amount"]   # one refund per order
    st.audit.append({"req": req, "decision": d, "reason": why})   # layer 6: audit every decision
    return d, why

# ---- tests ----
def fresh(): return State()
assert process({"order_id": "A1", "amount": 30.0}, fresh())[0] == "allow"
assert process({"order_id": "A1", "amount": 90.0}, fresh())[0] == "needs_approval"
assert process({"order_id": "A1", "amount": 90.0}, fresh(), approved=True)[0] == "allow"
assert process({"order_id": "A1", "amount": 500.0}, fresh()) == ("deny", "amount exceeds order total")
assert process({"order_id": "A1", "amount": -5}, fresh())[0] == "deny"
assert process({"order_id": "B2", "amount": 10.0}, fresh()) == ("deny", "order already refunded")
assert process({"order_id": "ZZ", "amount": 10.0}, fresh())[0] == "deny"
assert process({"order_id": "A1", "amount": "30"}, fresh())[0] == "deny"
assert process({"order_id": "A1", "amount": True}, fresh())[0] == "deny"
assert process({"order_id": "A1", "amount": 10.0, "note": "x"}, fresh())[0] == "deny"
assert process({}, fresh())[0] == "deny"                                   # fails closed
s = fresh(); process({"order_id": "A1", "amount": 30.0}, s)
assert process({"order_id": "A1", "amount": 30.0}, s)[0] == "deny"        # retry = duplicate, not 2nd refund
s = fresh(); s.spent_today = 190.0
assert process({"order_id": "A1", "amount": 30.0}, s) == ("deny", "daily spend limit")
assert len(s.audit) == 1
print("all policy tests passed")
s = fresh()
for r in [{"order_id": "A1", "amount": 30.0}, {"order_id": "A1", "amount": 30.0}, {"order_id": "A1", "amount": 90.0}]:
    print(r, "->", process(r, s))
