# Multi-query retrieval: MOCK variant generator (canned, no LLM), TOY BM25 corpus, RRF fusion with dedupe.
import re, math
def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
docs = {
 "leave1": "Employees accrue paid leave at 1.5 days per month of service",
 "leave2": "Unused vacation days can be carried forward up to 10 days",
 "sick":   "Sick leave requires a medical certificate after three consecutive absences",
 "wfh":    "Remote work is allowed two days per week with manager approval",
 "travel": "Business travel must be booked through the company portal",
 "exp":    "Expense claims are reimbursed within 15 working days",
 "it":     "Laptops are replaced every 3 years by the IT desk",
 "perf":   "Performance reviews happen twice a year in June and December",
}
ids = list(docs); D = {i: toks(t) for i, t in docs.items()}
N = len(D); avg = sum(map(len, D.values())) / N
df = {}
for d in D.values():
    for w in set(d): df[w] = df.get(w, 0) + 1
def bm25(q, k=3, k1=1.5, b=0.75):
    sc = {}
    for i, d in D.items():
        s = 0.0
        for w in toks(q):
            if w in df:
                tf = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        sc[i] = s
    return [i for i in sorted(ids, key=lambda i: -sc[i]) if sc[i] > 0][:k]
def rrf(lists, k=60):
    s = {}
    for l in lists:
        for r, d in enumerate(l, 1): s[d] = s.get(d, 0) + 1 / (k + r)
    return sorted(s, key=lambda d: -s[d])           # a dict key is unique, so this also dedupes
q = "how many days off do I get"
gold = {"leave1", "leave2"}
VARIANTS = [q,                                       # always keep the original
            "paid leave accrual days per month",     # mock LLM variant 1 (good)
            "annual leave carried forward unused vacation",         # mock LLM variant 2 (good)
            "sick leave medical certificate"]     # mock LLM variant 3 (DRIFT: leaves the question's intent)
def recall(l): return len(gold & set(l)) / len(gold)
print("single query top3      :", bm25(q), "recall@3 =", recall(bm25(q)[:3]))
lists = [bm25(v) for v in VARIANTS]
for v, l in zip(VARIANTS, lists): print(f"  {v[:36]!r:40} -> {l}")
f = rrf(lists)
print("fused (4 variants) top3:", f[:3], "recall@3 =", recall(f[:3]), "| searches run:", len(VARIANTS), "| unique docs:", len(f))
f2 = rrf(lists[:3])
print("fused w/o drifting variant:", f2[:3], "recall@3 =", recall(f2[:3]))
f3 = rrf(lists[:1] + lists[3:])
print("original + ONLY the drifting variant:", f3[:3], "recall@3 =", recall(f3[:3]))
