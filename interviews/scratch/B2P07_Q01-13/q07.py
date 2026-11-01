# Query rewriting with a MOCK rewriter (a lookup table, no LLM). TOY BM25 corpus.
import re, math
def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
docs = {
 "price_pro":   "The Pro plan costs 49 dollars per month billed annually",
 "price_basic": "The Basic plan costs 9 dollars per month",
 "refund":      "Refund requests are accepted within 30 days of purchase",
 "e4021":       "Error E4021 means the payment gateway timed out",
 "pay_help":    "Payment problems troubleshooting guide for failed card transactions",
 "pay_faq":     "Frequently asked payment questions about cards and invoices",
}
ids = list(docs); D = {i: toks(t) for i, t in docs.items()}
N = len(D); avg = sum(map(len, D.values())) / N
df = {}
for d in D.values():
    for w in set(d): df[w] = df.get(w, 0) + 1
def bm25(q, k1=1.5, b=0.75):
    sc = {}
    for i, d in D.items():
        s = 0.0
        for w in toks(q):
            if w in df:
                tf = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        sc[i] = s
    return [i for i in sorted(ids, key=lambda i: -sc[i]) if sc[i] > 0]
def rrf(lists, k=60):
    s = {}
    for l in lists:
        for r, d in enumerate(l, 1): s[d] = s.get(d, 0) + 1 / (k + r)
    return sorted(s, key=lambda d: -s[d])

# MOCK rewriter: canned outputs. Case 2 shows a drifting rewriter on an already-precise query.
MOCK = {
 "and how much is that one?": "Pro plan price per month",                 # ellipsis resolved with chat history
 "i paid and nothing happened, money gone, help": "refund payment failed",     # messy long query condensed
 "E4021": "payment problems troubleshooting guide",                           # drift: precise code dropped
}
cases = [("and how much is that one?", "price_pro"),
         ("i paid and nothing happened, money gone, help", "refund"),
         ("E4021", "e4021")]
def rr(lst, g): return 1 / (lst.index(g) + 1) if g in lst else 0.0
tot = {"original": 0, "rewritten": 0, "fused (RRF)": 0}
for q, g in cases:
    o = bm25(q); w = bm25(MOCK[q]); f = rrf([o, w])
    for name, l in (("original", o), ("rewritten", w), ("fused (RRF)", f)): tot[name] += rr(l, g)
    print(f"{q[:34]!r:38} RR original={rr(o,g):.2f} rewritten={rr(w,g):.2f} fused={rr(f,g):.2f}")
print("MRR over 3 cases:", {k: round(v / 3, 3) for k, v in tot.items()})
