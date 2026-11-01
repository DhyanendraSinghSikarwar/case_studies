import random
import sys
from bisect import bisect_left


def count_prefix_brute(words, p):
    return sum(1 for w in words if w.startswith(p))


class PrefixCounter:
    def __init__(self, words):
        self.sorted_words = sorted(words)          # O(n log n) once, comparisons cost up to L each

    def count(self, p):
        lo = bisect_left(self.sorted_words, p)             # first word >= p
        hi = bisect_left(self.sorted_words, p + "{")       # '{' is chr(ord('z') + 1)
        return hi - lo


words = ["apple", "app", "apt", "bat", "bath"]
pc = PrefixCounter(words)
for p in ["ap", "bat", "c", ""]:
    print(repr(p), pc.count(p))
assert pc.count("ap") == 3 and pc.count("bat") == 2 and pc.count("c") == 0 and pc.count("") == 5
assert chr(ord("z") + 1) == "{"
assert pc.count("apple") == 1 and pc.count("applez") == 0 and pc.count("zzz") == 0
assert PrefixCounter([]).count("a") == 0 and PrefixCounter([]).count("") == 0
assert PrefixCounter(["z", "zz", "zzz"]).count("z") == 3        # 'zzz{' still above 'zzz'
assert PrefixCounter(["a"]).count("a") == 1

# Why '{' and not a fixed sentinel: the bound must exceed every word starting with p.
# Every such word is p + (letters a..z)*, which is < p + '{'.
assert "zzzzzzzz" < "z{"

# a small trie sketch is NOT implemented here (Part 12); only the node-count estimate
rng = random.Random(36)
for _ in range(500):
    ws = list({"".join(rng.choice("abc") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(0, 12))})
    pc = PrefixCounter(ws)
    for _ in range(10):
        p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
        assert pc.count(p) == count_prefix_brute(ws, p), (ws, p)
print("random cross-check passed: 500 word sets x 10 prefixes")

# memory vs time sketch (sandbox-only numbers): strings in a sorted list vs trie node count
ws = list({"".join(rng.choice("abcdefghij") for _ in range(rng.randint(3, 8))) for _ in range(20000)})
nodes = len({w[:k] for w in ws for k in range(1, len(w) + 1)})      # distinct prefixes = trie nodes
chars = sum(len(w) for w in ws)
print("words", len(ws), "total chars", chars, "distinct prefixes (trie nodes, excluding root)", nodes)
