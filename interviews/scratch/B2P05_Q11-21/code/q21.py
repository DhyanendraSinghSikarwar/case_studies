import re
# MOCK verifiers on scripted outputs (no real model). Question: 17 * 3 = ?  (true answer 51)
outputs = {
  "correct, reasoned":   "17*3 = 10*3 + 7*3 = 30 + 21 = 51. Answer: 51",
  "wrong, reasoned":     "17*3 = 41. Answer: 41",
  "hack: lists many":    "Possible answers: 41, 45, 51, 60. Answer: 41 51",
  "hack: no reasoning":  "Answer: 51",
  "correct, bad format": "The result is 51.",
}
def weak_verifier(text):          # 'contains the number 51 anywhere'
    return float("51" in text)
def strict_verifier(text):        # requires exactly one 'Answer: N' at the end and N == 51
    m = re.fullmatch(r".*Answer: (\d+)", text, flags=re.S)
    return float(bool(m) and m.group(1) == "51")
print(f"{'output':22s} weak  strict")
for k, v in outputs.items():
    print(f"{k:22s} {weak_verifier(v):.0f}     {strict_verifier(v):.0f}")
