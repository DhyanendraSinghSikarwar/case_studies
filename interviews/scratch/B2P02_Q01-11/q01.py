from collections import Counter
corpus = "low low low low low lower lower newest newest newest newest newest newest widest widest widest".split()
def train_bpe(words, n_merges):
    seqs = Counter(tuple(w) + ("</w>",) for w in words)
    merges = []
    for _ in range(n_merges):
        pairs = Counter()
        for s, c in seqs.items():
            for a, b in zip(s, s[1:]): pairs[(a, b)] += c
        if not pairs: break
        best = max(pairs, key=lambda p: (pairs[p], p))   # tie-break: larger pair string
        merges.append(best)
        new = Counter()
        for s, c in seqs.items():
            out, i = [], 0
            while i < len(s):
                if i < len(s)-1 and (s[i], s[i+1]) == best: out.append(s[i]+s[i+1]); i += 2
                else: out.append(s[i]); i += 1
            new[tuple(out)] += c
        seqs = new
    return merges
def encode(word, merges):
    s = list(word) + ["</w>"]
    for a, b in merges:
        out, i = [], 0
        while i < len(s):
            if i < len(s)-1 and (s[i], s[i+1]) == (a, b): out.append(a+b); i += 2
            else: out.append(s[i]); i += 1
        s = out
    return s
merges = train_bpe(corpus, 10)
print(merges)
for w in ["newest", "lowest", "widest", "slowest"]:
    print(w, encode(w, merges))
print("word vocab has 'lowest'?", "lowest" in set(corpus))
