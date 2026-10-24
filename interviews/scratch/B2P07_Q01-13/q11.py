# TOY contextual retrieval: invented filings, BM25 from scratch. The "context" is a template built from doc metadata
# (a stand-in for an LLM-written 50-100 token blurb). Shows the mechanism only, not real-world gains.
import re, math, random
random.seed(3)
def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
companies = ["Acme Corp", "Borealis Ltd", "Cinder Foods", "Delta Works", "Evergreen Bank", "Fathom Labs"]
quarters = ["Q1 2023", "Q2 2023"]
chunks = []                       # (text, context, company, quarter, kind)
for c in companies:
    for q in quarters:
        g = random.randint(1, 9)
        chunks.append((f"Revenue grew {g}% over the previous quarter.", f"This chunk is from the {c} {q} earnings report, financial results section.", c, q, "revenue"))
        chunks.append(("Operating costs remained stable and headcount was flat.", f"This chunk is from the {c} {q} earnings report, cost section.", c, q, "cost"))
        chunks.append(("Management expects continued demand next quarter.", f"This chunk is from the {c} {q} earnings report, outlook section.", c, q, "outlook"))
def build(with_ctx):
    docs = [toks((ctx + " " if with_ctx else "") + t) for t, ctx, *_ in chunks]
    N = len(docs); avg = sum(map(len, docs)) / N; df = {}
    for d in docs:
        for w in set(d): df[w] = df.get(w, 0) + 1
    def score(q, k1=1.5, b=0.75):
        out = []
        for d in docs:
            s = 0.0
            for w in toks(q):
                if w in df:
                    tf = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                    s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
            out.append(s)
        return out
    return score
def evaluate(with_ctx):
    score = build(with_ctx); rr, hit1 = [], 0
    for c in companies:
        for q in quarters:
            gold = [i for i, ch in enumerate(chunks) if ch[2:] == (c, q, "revenue")][0]
            sc = score(f"{c} {q} revenue growth")
            order = sorted(range(len(chunks)), key=lambda i: (-sc[i], i))   # ties broken by index (stable)
            r = order.index(gold) + 1; rr.append(1 / r); hit1 += r == 1
    return round(sum(rr) / len(rr), 3), hit1
print("chunks:", len(chunks), "| queries: 12 (company + quarter + 'revenue growth')")
print("context-free  : MRR, hit@1 =", evaluate(False))
print("with context  : MRR, hit@1 =", evaluate(True))
print("example chunk alone:", repr(chunks[0][0]), "-> which company? which quarter? unknowable")
