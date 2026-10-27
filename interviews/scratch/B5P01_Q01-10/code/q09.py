import random
import string
from collections import defaultdict


def group_brute(words):
    # O(n^2 * L log L): compare each word against each existing group's first word
    groups = []
    for w in words:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return groups


def group_sorted_key(words):
    d = defaultdict(list)
    for w in words:
        d["".join(sorted(w))].append(w)  # O(L log L) per word
    return list(d.values())


def group_count_key(words):
    d = defaultdict(list)
    for w in words:
        cnt = [0] * 26
        for ch in w:  # O(L) per word to build, O(26) to hash the tuple
            cnt[ord(ch) - 97] += 1
        d[tuple(cnt)].append(w)  # a list is unhashable, a tuple is fine
    return list(d.values())


def norm(groups):
    return sorted(sorted(g) for g in groups)


ex = ["eat", "tea", "tan", "ate", "nat", "bat"]
print("sorted key:", group_sorted_key(ex))
print("count key :", group_count_key(ex))
print("example ok (any order):", norm(group_sorted_key(ex)) == norm([["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]))

random.seed(9)
for _ in range(1000):
    ws = ["".join(random.choice("abc") for _ in range(random.randint(0, 4))) for _ in range(random.randint(0, 8))]
    e = norm(group_brute(ws))
    assert norm(group_sorted_key(ws)) == e == norm(group_count_key(ws)), ws
print("cross-check: 1000 seeded cases agree")

assert group_sorted_key([]) == []
assert norm(group_sorted_key([""])) == [[""]]
assert norm(group_count_key(["a"])) == [["a"]]
assert norm(group_sorted_key(["", ""])) == [["", ""]]
assert norm(group_count_key(["ab", "ba", "ab"])) == [["ab", "ab", "ba"]]
assert norm(group_sorted_key(["abc", "def"])) == [["abc"], ["def"]]
# duplicates kept, not merged
assert sum(len(g) for g in group_sorted_key(["x", "x", "x"])) == 3
print("edge asserts passed")

# sandbox-only timing, long words (big-O comes from the code, not from this)
import time
L = 20000
words = ["".join(random.choice(string.ascii_lowercase) for _ in range(L)) for _ in range(50)]
for f in (group_sorted_key, group_count_key):
    t = time.perf_counter()
    f(words)
    print(f.__name__, "50 words of length 20000 (sandbox only): %.3fs" % (time.perf_counter() - t))
