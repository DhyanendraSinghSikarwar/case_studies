from collections import Counter
corpus = "low low low low low lower lower newest newest newest newest newest newest widest widest widest".split()
def merge_seq(s, pair):
    out, i = [], 0
    while i < len(s):
        if i < len(s)-1 and (s[i], s[i+1]) == pair: out.append(s[i]+s[i+1]); i += 2
        else: out.append(s[i]); i += 1
    return out
def train_bpe(words, n_merges):
    seqs = Counter(tuple(w) + ("</w>",) for w in words); merges = []
    for _ in range(n_merges):
        pairs = Counter()
        for s, c in seqs.items():
            for a, b in zip(s, s[1:]): pairs[(a, b)] += c
        best = max(pairs, key=lambda p: (pairs[p], p))      # deterministic tie-break
        merges.append(best)
        seqs = Counter({tuple(merge_seq(list(s), best)): c for s, c in seqs.items()})
    return merges
def encode(word, merges):
    s = list(word) + ["</w>"]
    for m in merges: s = merge_seq(s, m)
    return s
merges = train_bpe(corpus, 10)
for w in ["newest", "lowest", "widest", "slowest"]: print(w, encode(w, merges))
