# Standalone. The model is a MOCK (scripted closures); no real API is called.
# Message shapes are generic (provider-neutral): assistant turns carry tool_calls with ids,
# and every call id needs exactly one tool result. Check your provider's current docs.
import json

ORDERS = {"A1": {"status": "shipped", "total": 120.0}, "B2": {"status": "packed", "total": 80.0}}
LEDGER = []

def get_order(order_id):  return ORDERS[order_id]                     # KeyError if unknown
def refund(order_id, amount): LEDGER.append((order_id, amount)); return {"refunded": amount}
TOOLS = {"get_order": get_order, "refund": refund}

class ApiError(Exception): pass

def check_ids(messages):                       # what real APIs enforce (mock version)
    pending = set()
    for m in messages:
        if m["role"] == "assistant": pending = {c["id"] for c in m["tool_calls"]}
        elif m["role"] == "tool":
            if m["tool_call_id"] not in pending: raise ApiError(f"tool result id {m['tool_call_id']!r} matches no tool call")
            pending.discard(m["tool_call_id"])

# ---------------- BUGGY loop (as an LLM might write it) ----------------
def buggy_loop(model, user):
    messages = [{"role": "user", "content": user}]
    while True:                                                    # BUG 1: no max_steps guard
        resp = model(messages)
        messages.append({"role": "assistant", "text": resp["text"], "tool_calls": resp["tool_calls"]})
        if not resp["tool_calls"]:                                 # BUG 6: stop_reason never checked
            return resp["text"]
        call = resp["tool_calls"][0]                               # BUG 4: only first parallel call
        try:
            result = TOOLS[call["name"]](**call["args"])           # BUG 3: args not validated
        except Exception:
            result = ""                                            # BUG 5: error swallowed
        messages.append({"role": "tool", "tool_call_id": resp["id"],   # BUG 2: message id, not call id
                         "content": json.dumps(result)})

# ---------------- FIXED loop ----------------
class StepLimit(Exception): pass
class Truncated(Exception): pass

def validate(name, args):
    if name not in TOOLS: raise ValueError(f"unknown tool {name}")
    if name == "get_order":
        if set(args) != {"order_id"} or args["order_id"] not in ORDERS: raise ValueError("order_id must be an existing order, e.g. 'A1'")
    if name == "refund":
        if set(args) != {"order_id", "amount"}: raise ValueError("need order_id and amount")
        a = args["amount"]
        if not isinstance(a, (int, float)) or not (0 < a <= ORDERS.get(args["order_id"], {"total": 0})["total"]):
            raise ValueError("amount must be > 0 and <= order total")

def fixed_loop(model, user, max_steps=6):
    messages = [{"role": "user", "content": user}]
    for _ in range(max_steps):                                     # 1: hard step cap
        resp = model(messages)
        messages.append({"role": "assistant", "text": resp["text"], "tool_calls": resp["tool_calls"]})
        if resp["stop_reason"] == "end_turn": return resp["text"]  # 6: branch on stop reason
        if resp["stop_reason"] != "tool_use": raise Truncated(resp["stop_reason"])
        for call in resp["tool_calls"]:                            # 4: answer EVERY call
            try:
                validate(call["name"], call["args"])               # 3: validate before executing
                out, err = json.dumps(TOOLS[call["name"]](**call["args"])), False
            except Exception as e:                                 # 5: tell the model what went wrong
                out, err = f"ERROR: {type(e).__name__}: {e}", True
            messages.append({"role": "tool", "tool_call_id": call["id"],   # 2: the call's own id
                             "content": out, "is_error": err})
    raise StepLimit(f"no final answer after {max_steps} steps")

# ---------------- mock models ----------------
def R(stop, text="", calls=(), mid="msg_1"): return {"stop_reason": stop, "text": text, "tool_calls": list(calls), "id": mid}
def call(i, name, **args): return {"id": i, "name": name, "args": args}

def stuck_model(counter):
    def m(messages):
        counter[0] += 1
        if counter[0] > 100: raise RuntimeError("model called 100 times, demo aborted: loop never ends")
        return R("tool_use", calls=[call(f"c{counter[0]}", "get_order", order_id="A1")])
    return m

def negative_refund_model(messages):
    last = messages[-1]
    if last["role"] == "user": return R("tool_use", calls=[call("c1", "refund", order_id="A1", amount=-500.0)])
    if str(last["content"]).startswith("ERROR"): return R("tool_use", calls=[call("c2", "refund", order_id="A1", amount=50.0)])
    return R("end_turn", "Refund done.")

def parallel_model(messages):
    if messages[-1]["role"] == "user":
        return R("tool_use", calls=[call("c1", "get_order", order_id="A1"), call("c2", "get_order", order_id="B2")])
    return R("end_turn", f"Saw {sum(m['role']=='tool' for m in messages)} order result(s).")

def lowercase_model(messages):          # mock that papers over a missing result, then recovers on an error
    last = messages[-1]
    if last["role"] == "user": return R("tool_use", calls=[call("c1", "get_order", order_id="a1")])
    if str(last["content"]).startswith("ERROR"): return R("tool_use", calls=[call("c2", "get_order", order_id="A1")])
    if last["content"] in ('""', ""): return R("end_turn", "Your order is on its way.")   # invented
    return R("end_turn", "Order A1 is " + json.loads(last["content"])["status"] + ".")

def truncated_model(messages): return R("max_tokens", "Your refund of 50 has been")

def strict(model):
    def m(messages): check_ids(messages); return model(messages)
    return m

print("Scenarios trigger one bug each; the mock enforces tool-call ids only in scenario 2.")
print("S1 no step limit:    ", end="")
try: buggy_loop(stuck_model([0]), "status?")
except RuntimeError as e: print("buggy ->", e)
try: fixed_loop(stuck_model([0]), "status?")
except StepLimit as e: print("                     fixed ->", type(e).__name__, e)

print("S2 wrong call id:    ", end="")
class OneCall:  # model that calls once, then finishes
    def __call__(self, messages): return R("tool_use", calls=[call("c1", "get_order", order_id="A1")]) if messages[-1]["role"] == "user" else R("end_turn", "ok")
try: buggy_loop(strict(OneCall()), "status?")
except ApiError as e: print("buggy ->", "ApiError:", e)
print("                     fixed ->", fixed_loop(strict(OneCall()), "status?"))

print("S3 unvalidated args: ", end="")
LEDGER.clear(); buggy_loop(negative_refund_model, "refund me"); print("buggy -> ledger", LEDGER)
LEDGER.clear(); fixed_loop(negative_refund_model, "refund me"); print("                     fixed -> ledger", LEDGER)

print("S4 parallel calls:   ", end="")
print("buggy ->", buggy_loop(parallel_model, "orders A1 and B2?"))
print("                     fixed ->", fixed_loop(parallel_model, "orders A1 and B2?"))

print("S5 swallowed error:  ", end="")
print("buggy ->", buggy_loop(lowercase_model, "status of a1?"))
print("                     fixed ->", fixed_loop(lowercase_model, "status of a1?"))

print("S6 stop reason:      ", end="")
print("buggy ->", repr(buggy_loop(truncated_model, "refund?")))
try: fixed_loop(truncated_model, "refund?")
except Truncated as e: print("                     fixed -> Truncated:", e)
