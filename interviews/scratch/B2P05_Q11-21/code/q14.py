# MOCK: a scripted fake "model" (no real LLM). It shows the data flow of the supervised phase only.
CONSTITUTION = ["Do not give instructions that could cause harm.",
                "Stay helpful: explain why you decline and offer a safe alternative."]

def fake_model(prompt):
    # scripted behaviour keyed on the prompt text
    if prompt.startswith("RESPOND:"):
        return "Sure, here is how to pick a lock: insert a tension wrench..."
    if prompt.startswith("CRITIQUE:"):
        return "The reply gives lock-picking steps, which may help a break-in (violates principle 1)."
    if prompt.startswith("REVISE:"):
        return ("I can't walk through bypassing someone else's lock, but if you are locked out "
                "of your own home, a locksmith or your landlord can help.")
    return ""

def critique_revise(user_prompt, principle):
    draft = fake_model("RESPOND: " + user_prompt)
    critique = fake_model(f"CRITIQUE: {principle} || {draft}")
    revision = fake_model(f"REVISE: {critique} || {draft}")
    return {"prompt": user_prompt, "draft": draft, "critique": critique, "revision": revision}

sft_data = []
rec = critique_revise("How do I pick a lock?", CONSTITUTION[0])
sft_data.append((rec["prompt"], rec["revision"]))   # finetune on (prompt, revision)
for k, v in rec.items():
    print(f"{k:9s}: {v}")
print("SFT pairs kept:", len(sft_data))

# RL phase (RLAIF) data flow: the AI judge picks between two samples per principle
def fake_judge(prompt, a, b, principle):
    return "A" if "locksmith" in a else "B"   # scripted, not a real judge
pref = {"chosen": rec["revision"], "rejected": rec["draft"]}
print("judge picks revision:", fake_judge(rec["prompt"], rec["revision"], rec["draft"], CONSTITUTION[1]) == "A")
