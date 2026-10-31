import hashlib, re
docs = [
 "The quick brown fox jumps over the lazy dog near the river bank today and everyone watched it happen.",
 "The quick brown fox jumps over the lazy dog near the river bank today and everyone watched it happen!!",  # exact dup after normalising
 "The quick brown fox jumps over the lazy dog near the river bank today and everybody watched it happen.",  # near dup (1 word)
 "buy now buy now buy now buy now buy now buy now",                                                         # repetitive, low quality
 "Contact me at john.doe@example.com or call 9876543210 for the report details.",
 "Gradient descent updates parameters in the direction that reduces the loss function.",
 "hi",
]
def norm(t): return re.sub(r"\W+", " ", t.lower()).strip()
def quality(t):
    w = t.split(); return len(w) >= 5 and len(set(w)) / len(w) > 0.5
seen, kept = set(), []
for d in docs:
    if not quality(d): continue
    h = hashlib.md5(norm(d).encode()).hexdigest()
    if h in seen: continue
    seen.add(h); kept.append(d)
print("after quality filter + exact dedup:", len(kept), "of", len(docs))
def shingles(t, k=3):
    w = norm(t).split(); return {" ".join(w[i:i+k]) for i in range(len(w)-k+1)}
S = [shingles(d) for d in kept]
jac = len(S[0] & S[1]) / len(S[0] | S[1])
def minhash(sh, n=128):
    return [min(int(hashlib.md5(f"{i}|{s}".encode()).hexdigest()[:8], 16) for s in sh) for i in range(n)]
M = [minhash(s) for s in S]
est = sum(a == b for a, b in zip(M[0], M[1])) / 128
print("true Jaccard:", round(jac, 2), " MinHash estimate:", round(est, 2), " unrelated pair:", round(sum(a == b for a, b in zip(M[0], M[2])) / 128, 2))
pii = re.compile(r"[\w.]+@[\w.]+|\b\d{10}\b")
print([pii.sub("<PII>", d) for d in kept if pii.search(d)])
