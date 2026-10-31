import itertools
import random
import sys

random.seed(3301)


def trie_numbers(words):
    """Returns [nodes, slots26, pairs, distinct] using a dict-of-dicts trie."""
    distinct = set(words)
    root = {}
    nodes = 0
    for w in distinct:                       # repeats change nothing, so insert each distinct word once
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                nodes += 1
            node = node[ch]
    pairs = sum(len(w) for w in distinct)    # every non-empty prefix of w pairs with w once
    return [nodes, 26 * (nodes + 1), pairs, len(distinct)]


def brute(words):
    distinct = set(words)
    prefixes = {w[:i] for w in distinct for i in range(1, len(w) + 1)}   # distinct non-empty prefixes
    return [len(prefixes), 26 * (len(prefixes) + 1), sum(len(w) for w in distinct), len(distinct)]


# dry run on the first example
words = ["car", "cart", "cat", "dog", "do", "car"]
seen = set()
for w in sorted(set(words)):
    new = [w[:i] for i in range(1, len(w) + 1) if w[:i] not in seen]
    seen.update(new)
    print(f"insert {w!r:7} new nodes: {new}")
print("nodes =", len(seen), "(the distinct non-empty prefixes)")

for ws, want in [(["car", "cart", "cat", "dog", "do", "car"], [8, 234, 15, 5]), (["a", "b", "c"], [3, 104, 3, 3]),
                 (["aaa"], [3, 104, 3, 1]), (["ab", "ac"], [3, 104, 4, 2])]:
    got = trie_numbers(ws)
    assert got == want == brute(ws), (ws, got)
    print(ws, "->", got)

# claim: dict of sets has exactly the trie's nodes as keys; nodes <= pairs; equality iff first letters all differ
for _ in range(1500):
    ws = ["".join(random.choice("abc") for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 6))]
    nodes, slots, pairs, distinct = trie_numbers(ws)
    assert [nodes, slots, pairs, distinct] == brute(ws)
    d = {}
    for w in set(ws):
        for i in range(1, len(w) + 1):
            d.setdefault(w[:i], set()).add(w)
    assert len(d) == nodes and sum(len(v) for v in d.values()) == pairs and nodes <= pairs
    firsts = {w[0] for w in set(ws)}
    assert (nodes == pairs) == (len(firsts) == distinct)
print("1500 seeded random word lists: nodes == keys of the dict of sets, nodes <= pairs, equal iff first letters all differ")

# exhaustive: every list of up to 3 words from {a, b, ab, ba, bb, aab}
pool = ["a", "b", "ab", "ba", "bb", "aab"]
for k in (1, 2, 3):
    for ws in itertools.product(pool, repeat=k):
        n, _, p, dct = trie_numbers(list(ws))
        assert n <= p and ((n == p) == (len({w[0] for w in set(ws)}) == dct))
print("exhaustive small lists ok")


# sandbox measurement (this machine and Python version only): shallow sys.getsizeof sums, NOT a proof of anything
def sizes(ws):
    distinct = set(ws)
    root = {}
    node_dicts = [root]
    for w in distinct:
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                node_dicts.append(node[ch])
            node = node[ch]
    trie_dict = sum(sys.getsizeof(d) for d in node_dicts)
    trie_arr = len(node_dicts) * sys.getsizeof([None] * 26)
    plain_set = sys.getsizeof(distinct) + sum(sys.getsizeof(w) for w in distinct)
    dos = {}
    for w in distinct:
        for i in range(1, len(w) + 1):
            dos.setdefault(w[:i], set()).add(w)
    dict_sets = sys.getsizeof(dos) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in dos.items()) \
        + sum(sys.getsizeof(w) for w in distinct)
    return trie_dict, trie_arr, plain_set, dict_sets


print("sandbox sizes, Python", sys.version.split()[0], "(bytes: trie of dicts, trie of 26-lists, plain set, dict of sets)")
for name, ws in [("5000 random words, len 1-20 over 'abcdefghij'",
                  ["".join(random.choice("abcdefghij") for _ in range(random.randint(1, 20))) for _ in range(5000)]),
                 ("5000 words 'internationalisation' + 4 letters over 'ab'",
                  ["internationalisation" + "".join(random.choice("ab") for _ in range(4)) for _ in range(5000)])]:
    r = trie_numbers(ws)
    print(" ", name, "-> [nodes, slots26, pairs, distinct] =", r, "| sizes", sizes(ws))

assert trie_numbers(["a" * 20] * 5000) == [20, 26 * 21, 20, 1]
print("edge asserts ok")
