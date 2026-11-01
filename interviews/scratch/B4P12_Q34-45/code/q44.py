# Q44: agent role denied a write it was not granted, using a COPY of iam_eval_sketch.py (unmodified).
import sys; sys.path.insert(0, "."); from iam_eval_sketch import evaluate
A = lambda a, r="*", e="Allow": {"Version": "2012-10-17", "Statement": [{"Effect": e, "Action": a, "Resource": r}]}
tickets = "arn:aws:dynamodb:ap-south-1:111122223333:table/tickets"
agent_role = [A(["dynamodb:GetItem", "dynamodb:Query"], tickets)]          # read-only agent
approver_role = [A(["dynamodb:GetItem", "dynamodb:PutItem"], tickets)]     # used only after human approval
boundary = A(["dynamodb:GetItem", "dynamodb:Query", "dynamodb:PutItem"], tickets)
for who, pol in [("agent (read grant)", agent_role), ("approval-flow role", approver_role)]:
    for act in ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:DeleteItem"]:
        print(f"{who:20s} {act:22s} ->", evaluate(act, tickets, identity=pol, boundary=boundary))
assert evaluate("dynamodb:PutItem", tickets, identity=agent_role)[0] == "Deny"
# explicit deny guardrail beats any later allow
guard = A("dynamodb:DeleteItem", "*", "Deny")
print("with explicit deny guard, even an admin-ish allow:", evaluate("dynamodb:DeleteItem", tickets, identity=[A("dynamodb:*"), guard]))
# rate/spend limit and secret-in-context check (platform-level, toy)
import re
ctx = "summarise ticket 42. key=AKIAIOSFODNN7EXAMPLE"
print("secret in context?", bool(re.search(r"AKIA[0-9A-Z]{16}", ctx)), "-> block call")
