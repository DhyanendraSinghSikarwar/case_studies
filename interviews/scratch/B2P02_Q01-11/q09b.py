import hashlib, re
docs = ["The quick brown fox jumps over the lazy dog near the river bank today and everyone watched it happen.",
        "The quick brown fox jumps over the lazy dog near the river bank today and everyone watched it happen!!",
        "The quick brown fox jumps over the lazy dog near the river bank today and everybody watched it happen.",
        "buy now buy now buy now buy now buy now buy now",
        "Contact me at john.doe@example.com or call 9876543210 for the report details.",
        "Gradient descent updates parameters in the direction that reduces the loss function.", "hi"]
norm = lambda t: re.sub(r"\W+", " ", t.lower()).strip()
def quality(t): w = t.split(); return len(w) >= 5 and len(set(w)) / len(w) > 0.5
seen, kept = set(), []
for d in docs:
    h = hashlib.md5(norm(d).encode()).hexdigest()
    if quality(d) and h not in seen: seen.add(h); kept.append(d)
print(len(kept))                                                   # 4
def shingles(t, k=3): w = norm(t).split(); return {" ".join(w[i:i+k]) for i in range(len(w)-k+1)}
S = [shingles(d) for d in kept]
def minhash(sh, n=128): return [min(int(hashlib.md5(f"{i}|{s}".encode()).hexdigest()[:8], 16) for s in sh) for i in range(n)]
M = [minhash(s) for s in S]
print(len(S[0] & S[1]) / len(S[0] | S[1]), sum(a == b for a, b in zip(M[0], M[1])) / 128)
