# ILLUSTRATIVE and INCOMPLETE PII scrubbing + dedup + split-before-dedup. Regex misses names, addresses, IDs in other formats.
# Use NER-based tools plus human review for real data. Data below is made up.
import re, hashlib, random
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)")   # Indian mobile-like only
def scrub(t):
    t = EMAIL.sub("<EMAIL>", t)
    return PHONE.sub("<PHONE>", t)

rows = [
 "Hi, I am Priya Sharma, mail me at priya.sharma@example.com or call +91 98765 43210.",
 "Refund for order 4471 please. Contact: rahul_k@mail.example.org, 9123456780",
 "Refund for order 4471 please. Contact: rahul_k@mail.example.org, 9123456780",       # exact dup
 "refund for order 4471 please, thanks!  contact: someone@else.example.net, 9000011111",   # near dup
 "I live at 12 MG Road, Pune 411001. Cancel my plan.",
]
for r in rows[:2] + rows[4:]:
    print("IN :", r); print("OUT:", scrub(r))
print("-> names ('Priya Sharma') and the street address survive: regex is not enough.\n")

def norm(t):                                    # normalise before comparing
    t = scrub(t).lower()
    return re.sub(r"[^a-z0-9 ]+", " ", re.sub(r"\s+", " ", t)).strip()
def shingles(t, n=3):
    w = norm(t).split(); return {" ".join(w[i:i+n]) for i in range(max(1, len(w)-n+1))}
def jaccard(a, b): return len(a & b) / len(a | b)

# 1) exact dedup on normalised hash; 2) near-dup via Jaccard of word 3-shingles
seen, uniq = {}, []
for r in rows:
    h = hashlib.md5(norm(r).encode()).hexdigest()
    if h in seen: continue
    seen[h] = r; uniq.append(r)
print("after exact dedup (normalised):", len(rows), "->", len(uniq))
print("Jaccard row1 vs row3:", round(jaccard(shingles(rows[1]), shingles(rows[3])), 2))

# Dedup ACROSS train and eval (not only inside each), and split by GROUP, so a near-duplicate never straddles the two sets.
random.seed(0)
pool = [f"ticket template {i%50} variant {i}" for i in range(200)]        # 50 templates x 4 variants
def leak(train, test):
    tk = {t.rsplit(" variant", 1)[0] for t in train}
    return sum(t.rsplit(" variant", 1)[0] in tk for t in test)
random.shuffle(pool); tr_rand, te_rand = pool[:160], pool[160:]
groups = sorted({p.rsplit(" variant", 1)[0] for p in pool})
te_g = set(groups[:10])
te_grp = [p for p in pool if p.rsplit(" variant", 1)[0] in te_g]
tr_grp = [p for p in pool if p.rsplit(" variant", 1)[0] not in te_g]
print("random row split: eval items whose template is also in train:", leak(tr_rand, te_rand), "of", len(te_rand))
print("group split     : eval items whose template is also in train:", leak(tr_grp, te_grp), "of", len(te_grp))
