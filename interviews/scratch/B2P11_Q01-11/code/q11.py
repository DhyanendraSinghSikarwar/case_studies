# TOY PII redactor on SYNTHETIC text (fake names, test card number). Regex + Luhn only; real systems add NER and review.
import re, hashlib
def luhn(num):
    d = [int(c) for c in num][::-1]
    return (sum(d[0::2]) + sum(sum(divmod(2 * x, 10)) for x in d[1::2])) % 10 == 0
assert luhn("4111111111111111") and not luhn("4111111111111112")     # known test card number passes, off-by-one fails
PATTERNS = [("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
            ("CARD", re.compile(r"\b(?:\d[ -]?){13,16}\b")),
            ("PHONE", re.compile(r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{9}(?!\d)"))]   # 10-digit mobile-like pattern; a generic example
class Vault:                                                                   # placeholder <-> value map, kept OUTSIDE the prompt and the trace store
    def __init__(self): self.map = {}
    def put(self, kind, val):
        tok = f"<{kind}_{len([k for k in self.map if k.startswith('<' + kind)]) + 1}>"; self.map[tok] = val; return tok
def redact(text, vault):
    for kind, rx in PATTERNS:
        def sub(m):
            raw = m.group(0)
            if kind == "CARD" and not luhn(re.sub(r"\D", "", raw)): return raw        # 16 digits that fail Luhn are probably an order id
            return vault.put(kind, raw)
        text = rx.sub(sub, text)
    return text
msgs = [("Hi, I am Priya Nair. Card 4111 1111 1111 1111, mail priya.n@example.test", {"EMAIL": 1, "CARD": 1, "NAME": 1}),
        ("Call me on 9876543210 about order 1234567890123456", {"PHONE": 1}),
        ("Ravi Kumar here, my number is 98765 43210", {"PHONE": 1, "NAME": 1}),
        ("Refund to a.b@example.test and c@example.test please", {"EMAIL": 2})]
v = Vault(); found = {}; truth = {}
for text, gt in msgs:
    out = redact(text, v)
    print("IN :", text); print("OUT:", out)
    for k, n in gt.items(): truth[k] = truth.get(k, 0) + n
for tok in v.map: found[tok.split("_")[0][1:]] = found.get(tok.split("_")[0][1:], 0) + 1
print("recall per type (found / planted):", {k: f"{found.get(k, 0)}/{n}" for k, n in sorted(truth.items())})
print("what the trace store keeps for message 1: redacted text + sha256_12 of the raw text =", hashlib.sha256(msgs[0][0].encode()).hexdigest()[:12])
