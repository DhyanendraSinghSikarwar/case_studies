from collections import Counter
en = ("the cat sat on the mat and the dog ate the food while the bird sang in the tree "
      "we are going to the market to buy some fruit and vegetables for the week ") * 4
def merge(s, pair, new):
    out, i = [], 0
    while i < len(s):
        if i < len(s)-1 and (s[i], s[i+1]) == pair: out.append(new); i += 2
        else: out.append(s[i]); i += 1
    return out
seq = list(en.encode("utf-8")); merges = []
nid = 256
for _ in range(60):
    c = Counter(zip(seq, seq[1:])); best = max(c, key=lambda p: (c[p], p))
    merges.append((best, nid)); seq = merge(seq, best, nid); nid += 1
def enc(text):
    s = list(text.encode("utf-8"))
    for pair, new in merges: s = merge(s, pair, new)
    return s
e_txt = "the dog went to the market to buy fruit"
h_txt = "कुत्ता फल खरीदने बाज़ार गया"     # Hindi, similar meaning
for name, t in [("English", e_txt), ("Hindi", h_txt)]:
    print(name, "chars", len(t), "bytes", len(t.encode()), "toy tokens", len(enc(t)), "tokens/char", round(len(enc(t))/len(t), 2))
# API cost arithmetic (hypothetical price)
words = 1000; tpw = 1/0.75
print("rule of thumb tokens for 1000 words:", round(words*tpw))
price = 3.0  # hypothetical $ per 1M input tokens
print("cost per request at 1,333 tok:", round(1333*price/1e6, 5), " per 1M requests:", round(1333*price, 1))
print("with 40% cut:", round(1333*0.6*price, 1))
