from collections import Counter, defaultdict
from itertools import combinations
import random

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]

def key_sorted(w):   return "".join(sorted(w))                    # O(L log L), exact
def key_count(w):                                                  # O(L + 26), exact
    c = [0] * 26
    for ch in w: c[ord(ch) - 97] += 1
    return tuple(c)
def key_counter_items(w): return frozenset(Counter(w).items())    # O(L), exact, any alphabet
def key_primes(w):                                                 # exact (unique factorisation), big ints
    p = 1
    for ch in w: p *= PRIMES[ord(ch) - 97]
    return p
def key_frozenset(w): return frozenset(w)                          # WRONG: drops multiplicity
def key_sum(w):       return sum(map(ord, w))                      # WRONG: different multisets, same sum
def key_poly_mod(w, mod=101):                                      # sum of ord^2 mod small prime: collides
    return sum(ord(c) ** 2 for c in w) % mod

def group(words, key):
    d = defaultdict(list)
    for w in words: d[key(w)].append(w)
    return list(d.values())

def partition(groups):  # canonical form to compare groupings
    return sorted(sorted(g) for g in groups)

words = ['ab', 'ba', 'abb', 'bab']
truth = partition(group(words, key_sorted))
print("truth            :", truth)
for name, k in [("count tuple", key_count), ("counter items", key_counter_items),
                ("prime product", key_primes), ("frozenset(chars)", key_frozenset),
                ("sum of ords", key_sum)]:
    p = partition(group(words, k))
    print(f"{name:17}:", "OK " if p == truth else "WRONG", p)

# The prompt's example does NOT break the sum key, so find words that do:
print("sum('ad'), sum('bc'):", key_sum('ad'), key_sum('bc'), "-> merged although multisets differ")
print("frozenset('ab') == frozenset('abb'):", frozenset('ab') == frozenset('abb'))

# a deterministic collision for the small-modulus polynomial-style hash
col = next((a, b) for a, b in combinations(["".join(t) for t in
           [(x, y) for x in "abcdefgh" for y in "abcdefgh"]], 2)
           if sorted(a) != sorted(b) and key_poly_mod(a) == key_poly_mod(b))
print("mod-101 sum-of-squares collision:", col)

# unhashable keys
for bad in ([1, 2], {1, 2}):
    try: {bad: 1}
    except TypeError as e: print("TypeError:", e)
print("tuple/frozenset keys fine:", {(1, 2): 1, frozenset({1, 2}): 2})

# seeded cross-check: exact keys must equal truth partition, wrong keys must (often) not
rng = random.Random(41)
bad_counts = {"frozenset": 0, "sum": 0, "poly101": 0}
for _ in range(400):
    ws = ["".join(rng.choice("abcd") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(1, 8))]
    t = partition(group(ws, key_sorted))
    for k in (key_count, key_counter_items, key_primes):
        assert partition(group(ws, k)) == t
    bad_counts["frozenset"] += partition(group(ws, key_frozenset)) != t
    bad_counts["sum"] += partition(group(ws, key_sum)) != t
    bad_counts["poly101"] += partition(group(ws, key_poly_mod)) != t
print("exact keys matched on 400 seeded cases; wrong-key failures:", bad_counts)

# edge cases
assert group([], key_sorted) == []
assert partition(group(['', ''], key_count)) == [['', '']]
assert key_sorted('') == '' and key_primes('') == 1
assert key_count('a') != key_count('b')
print("edge asserts passed")
