import itertools
import random
from bisect import bisect_right


def next_letter(letters, target):
    return letters[bisect_right(letters, target) % len(letters)]


def next_letter_manual(letters, target):
    lo, hi = 0, len(letters)
    while lo < hi:                       # upper bound: first index with letters[i] > target
        mid = (lo + hi) // 2
        if letters[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return letters[lo % len(letters)]    # lo == len -> wrap to index 0


def next_letter_brute(letters, target):
    for c in letters:
        if c > target:
            return c
    return letters[0]


examples = [(['c', 'f', 'j'], 'a', 'c'), (['c', 'f', 'j'], 'c', 'f'), (['c', 'f', 'j'], 'j', 'c'),
            (list("xxyy"), 'z', 'x'), (list("xxyy"), 'x', 'y')]
for letters, t, exp in examples:
    got = next_letter(letters, t)
    assert got == next_letter_manual(letters, t) == next_letter_brute(letters, t) == exp
    print("".join(letters), t, "->", got)

# exhaustive over alphabet a..f: every sorted list of length 2..7 with >= 2 distinct letters, every target a..g
alpha = "abcdef"
n_lists = n_pairs = 0
for L in range(2, 8):
    for combo in itertools.combinations_with_replacement(alpha, L):
        if len(set(combo)) < 2:
            continue
        letters = list(combo)
        n_lists += 1
        for t in "abcdefg":
            assert next_letter(letters, t) == next_letter_manual(letters, t) == next_letter_brute(letters, t), (letters, t)
            n_pairs += 1
print("exhaustive: %d lists x 7 targets = %d cases agree" % (n_lists, n_pairs))

random.seed(16)
for _ in range(500):
    letters = sorted(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(random.randint(2, 30)))
    if len(set(letters)) < 2:
        continue
    t = random.choice("abcdefghijklmnopqrstuvwxyz")
    assert next_letter(letters, t) == next_letter_brute(letters, t)
print("seeded random check passed")

# edge cases
assert next_letter(['a', 'b'], 'z') == 'a'          # target after everything
assert next_letter(['a', 'b'], 'a') == 'b'
assert next_letter(['a', 'z'], 'a') == 'z'
assert next_letter(['a', 'z'], 'z') == 'a'          # target equals the largest letter: wrap
assert next_letter(['b', 'b', 'c'], 'a') == 'b'
print("edge asserts passed")
