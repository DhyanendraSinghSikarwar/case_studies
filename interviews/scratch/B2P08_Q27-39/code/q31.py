# TOY A2A-style agent card + task state machine. Field names and states follow a guide's description
# (name, skills, endpoint, auth; Submitted/Working/Input Required/Completed/Failed/Canceled). Not the real spec: check it.
import json
CARD = {"name": "invoice-checker", "description": "Checks invoices against purchase orders",
        "endpoint": "https://agents.example.invalid/invoice", "auth": {"scheme": "bearer"},
        "skills": [{"id": "match_po", "description": "Match an invoice to a purchase order"}]}
REQUIRED = {"name": str, "endpoint": str, "skills": list, "auth": dict}
def validate_card(c):
    errs = [f"missing/invalid {k}" for k, t in REQUIRED.items() if not isinstance(c.get(k), t)]
    if isinstance(c.get("skills"), list) and not c["skills"]: errs.append("no skills")
    return errs

ALLOWED = {"submitted": {"working", "canceled", "failed"},
           "working": {"input_required", "completed", "failed", "canceled"},
           "input_required": {"working", "canceled", "failed"},
           "completed": set(), "failed": set(), "canceled": set()}      # last three are terminal
class Task:
    def __init__(self, tid, skill): self.id, self.skill, self.state, self.history = tid, skill, "submitted", ["submitted"]
    def move(self, new):
        if new not in ALLOWED[self.state]: raise ValueError(f"illegal transition {self.state} -> {new}")
        self.state = new; self.history.append(new); return self

assert validate_card(CARD) == [] and validate_card({"name": "x"}) != []
# a client picks an agent by matching the skill it needs against the card
need = "match_po"; assert any(s["id"] == need for s in CARD["skills"])
t = Task("t1", need)
t.move("working").move("input_required")      # agent asks the client for a missing PO number
t.move("working").move("completed")
print("happy path:", " -> ".join(t.history))
try: t.move("working")
except ValueError as e: print("blocked:", e)
t2 = Task("t2", need).move("working").move("canceled"); print("cancel path:", " -> ".join(t2.history))
try: Task("t3", need).move("completed")
except ValueError as e: print("blocked:", e)
print("card errors for a bad card:", validate_card({"name": "x", "skills": []}))
print("tests passed")
