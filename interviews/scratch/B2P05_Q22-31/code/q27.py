import re
# ILLUSTRATIVE, incomplete patterns. Tiny hand-made labelled set (placeholder data only).
PATTERNS = {
 "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"),
 "phone_in": re.compile(r"(?<!\d)(?:\+91[- ]?)?[6-9]\d{9}(?!\d)"),
 "secret": re.compile(r"\b(?:sk|key)[-_][A-Za-z0-9]{16,}\b"),
}
# (text, set of true PII/secret items present)
data = [
 ("mail me at asha.rao@example.com", {"asha.rao@example.com"}),
 ("call +91 9876543210 tomorrow", {"+91 9876543210"}),
 ("token is sk-AAAABBBBCCCCDDDD1234", {"sk-AAAABBBBCCCCDDDD1234"}),
 ("Ravi Kumar lives at 12 Park Street", {"Ravi Kumar", "12 Park Street"}),
 ("order id 9876543210 shipped", set()),               # 10 digits, not a phone: false positive risk
 ("contact: priya (at) example (dot) com", {"priya (at) example (dot) com"}),
 ("the weather is nice", set()),
 ("reach me on 98765 43210", {"98765 43210"}),          # spaced phone: regex misses
]
tp = fp = fn = 0
for text, truth in data:
    found = set()
    for pat in PATTERNS.values():
        found |= {m.group(0) for m in pat.finditer(text)}
    # match found items to truth loosely by substring overlap
    matched = {t for t in truth if any(f in t or t in f for f in found)}
    tp += len(matched); fn += len(truth - matched)
    fp += len([f for f in found if not any(f in t or t in f for t in truth)])
    print(f"{text[:38]:40s} found={sorted(found)}")
print(f"TP={tp} FP={fp} FN={fn} precision={tp/(tp+fp):.2f} recall={tp/(tp+fn):.2f}")
def shannon(s):
    from math import log2
    return 0.0 - sum(s.count(c)/len(s)*log2(s.count(c)/len(s)) for c in set(s))
for s in ["aaaaaaaaaaaaaaaaaaaa", "hello_world_variable", "q8Zr3KpL0vXw9TnB2yHd"]:
    print(f"entropy {shannon(s):.2f} bits/char  {s}")
def redact(text):
    for name, p in PATTERNS.items(): text = p.sub(f"[{name.upper()}]", text)
    return text
print(redact("mail asha.rao@example.com or call 9876543210"))
