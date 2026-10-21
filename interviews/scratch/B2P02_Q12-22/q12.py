from collections import Counter

def count_pairs(seq, overlap=True):
    c, i = Counter(), 0
    while i < len(seq) - 1:
        p = (seq[i], seq[i + 1])
        c[p] += 1
        if overlap or seq[i] != seq[i + 1]:
            i += 1
        else:                      # same-symbol pair, non-overlapping: skip past it
            i += 2
    return c

def merge(seq, pair, new):
    out, i = [], 0
    while i < len(seq):
        if i < len(seq) - 1 and (seq[i], seq[i + 1]) == pair:
            out.append(new); i += 2
        else:
            out.append(seq[i]); i += 1
    return out

def train(text, threshold=2, overlap=True):
    seq, merges = list(text), []
    while True:
        counts = count_pairs(seq, overlap)
        if not counts: break
        # highest count, then lexicographically smallest pair
        pair, n = min(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if n < threshold: break
        merges.append(pair)
        seq = merge(seq, pair, pair[0] + pair[1])
    return merges, seq

def encode(text, merges):
    seq = list(text)
    for pair in merges:            # apply merges in learned (rank) order
        seq = merge(seq, pair, pair[0] + pair[1])
    return seq

def decode(tokens):
    return "".join(tokens)

for ov in (True, False):
    merges, seq = train("abababa", 2, ov)
    print("overlap" if ov else "non-overlap", merges, seq)
text = "low lower lowest low low newer newest"
merges, seq = train(text, 2)
print(merges); print(seq)
ids = encode(text, merges)
assert decode(ids) == text and ids == seq
new = "lowest newlow"
assert decode(encode(new, merges)) == new
print(encode(new, merges))
assert train(text, 2)[0] == merges   # deterministic
print("round trip ok")
