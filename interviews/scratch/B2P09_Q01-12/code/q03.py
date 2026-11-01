# Reference-based metrics from scratch on toy strings. The "embedding" is a TOY synonym table
# (not a real model) that stands in for BERTScore-style soft matching.
import math
from collections import Counter

def toks(s): return s.lower().replace(".", "").replace(",", "").split()
def exact(p, r): return float(toks(p) == toks(r))
def f1(p, r):
    p, r = toks(p), toks(r); c = sum((Counter(p) & Counter(r)).values())
    if c == 0: return 0.0
    pr, rc = c / len(p), c / len(r); return 2 * pr * rc / (pr + rc)

def ngrams(t, n): return Counter(tuple(t[i:i+n]) for i in range(len(t) - n + 1))
def bleu2(p, r):                       # BLEU with n=1,2, uniform weights, brevity penalty, no smoothing
    p, r = toks(p), toks(r); logs = []
    for n in (1, 2):
        pg, rg = ngrams(p, n), ngrams(r, n)
        clip = sum((pg & rg).values()); tot = max(sum(pg.values()), 1)
        if clip == 0: return 0.0
        logs.append(math.log(clip / tot))
    bp = 1.0 if len(p) > len(r) else math.exp(1 - len(r) / max(len(p), 1))
    return bp * math.exp(sum(logs) / 2)

def lcs(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            d[i+1][j+1] = d[i][j] + 1 if a[i] == b[j] else max(d[i][j+1], d[i+1][j])
    return d[-1][-1]
def rougeL(p, r):
    p, r = toks(p), toks(r); l = lcs(p, r)
    if l == 0: return 0.0
    pr, rc = l / len(p), l / len(r); return 2 * pr * rc / (pr + rc)

SYN = {"purchase": "buy", "bought": "buy", "car": "auto", "automobile": "auto", "vehicle": "auto"}
def soft_f1(p, r):                    # toy BERTScore-like: greedy match, sim 1 for same/synonym, else 0
    canon = lambda w: SYN.get(w, w)
    p, r = [canon(w) for w in toks(p)], [canon(w) for w in toks(r)]
    prec = sum(w in r for w in p) / len(p); rec = sum(w in p for w in r) / len(r)
    return 0.0 if prec * rec == 0 else 2 * prec * rec / (prec + rec)

ref = "Maria bought a car in 2019."
cands = {
    "paraphrase (correct)":      "In 2019 Maria purchased an automobile.",
    "wrong year (incorrect)":    "Maria bought a car in 2021.",
    "exact copy":                "Maria bought a car in 2019.",
    "unrelated":                 "The weather was nice.",
}
print(f"{'candidate':26s} EM    F1    BLEU2 ROUGE-L softF1")
for name, c in cands.items():
    print(f"{name:26s} {exact(c,ref):.2f}  {f1(c,ref):.2f}  {bleu2(c,ref):.2f}  {rougeL(c,ref):.2f}   {soft_f1(c,ref):.2f}")
