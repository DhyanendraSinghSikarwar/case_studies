### Q31 ⭐ 🟡 Floating-point binary search: iterations versus epsilon. Return the square root of a real x with 0 <= x <= 10^6 so that |result - sqrt(x)| <= 10^-6, using binary search on reals with `hi = max(1.0, x)` (explain why hi = x is wrong for x < 1). Implement it twice: with a fixed number of iterations (100) and with `while hi - lo > eps`, then show with an iteration cap that `eps = 1e-15` never terminates for x = 10**6 (the interval cannot shrink below one float spacing), and say why a fixed iteration count is the safer default and how many halvings are needed to reach a given tolerance. Example: x=2 -> within 1e-6 of 1.41421356; x=0.25 -> within 1e-6 of 0.5; x=0 -> within 1e-6 of 0; x=10**6 -> within 1e-6 of 1000.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a real-valued answer. The predicate `mid * mid <= x` is True then False as mid grows, so I shrink an interval instead of an index range.

**Say this first (1 line):** "Square root by halving [0, max(1, x)]: keep lo where lo*lo <= x, move hi otherwise. I loop a fixed 100 times, because an epsilon loop can stall once the interval hits float spacing."

**Brute force:** Step r = 0, 1e-6, 2e-6, ... until r*r > x. For x = 10^6 that is about 10^9 steps. Too slow. A closer cousin is Newton's method, but the question asks for binary search.

**Optimal:**
- `lo = 0.0`, `hi = max(1.0, x)`. Loop: `mid = (lo + hi) / 2`; if `mid*mid <= x` then `lo = mid` else `hi = mid`.
- Why `hi = max(1.0, x)`: sqrt(x) <= x only when x >= 1. For x = 0.25 the root is 0.5, which is larger than x, so `hi = x` throws the answer out of the interval. The code run below shows `hi = x` returns 0.25.
- Invariant: `lo*lo <= x` and (`hi*hi > x` or hi is the initial bound). The root stays inside [lo, hi].
- Each halving halves the width. Halvings needed = smallest h with width / 2^h <= tol. For width 10^6 and tol 1e-6 that is 40. For width 1 it is 20. So 100 iterations is far more than enough.
- Epsilon loop trap: floats near 1000 are spaced about 1.1e-13 apart. With `eps = 1e-15`, lo and hi become neighbouring floats, `mid` equals one of them, the interval stops shrinking, and `hi - lo > eps` is True forever.
- A fixed count cannot hang. I would use an epsilon loop only when I know eps is comfortably above the float spacing at the answer.

**Complexity:** Time O(log(width / tol)), about 40 halvings for this tolerance, or exactly 100 with the fixed version. Space O(1).

**Dry run:** x = 2, lo = 0, hi = 2.
| step | mid | mid*mid vs 2 | new interval |
|---|---|---|---|
| 1 | 1 | 1 <= 2 | [1, 2] |
| 2 | 1.5 | 2.25 > 2 | [1, 1.5] |
| 3 | 1.25 | 1.5625 <= 2 | [1.25, 1.5] |
| 4 | 1.375 | 1.89 <= 2 | [1.375, 1.5] |
| 5 | 1.4375 | 2.07 > 2 | [1.375, 1.4375] |

The width halves every step: 2, 1, 0.5, 0.25, ... It heads to 1.41421356.

**Code:**
```python
import math
import random


def sqrt_fixed(x, iters=100):
    lo, hi = 0.0, max(1.0, x)            # sqrt(x) <= max(1, x) for every x >= 0
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sqrt_eps(x, eps=1e-9, cap=10**6):
    # returns (answer, loops used); cap stops a non-terminating loop for the demo
    lo, hi = 0.0, max(1.0, x)
    loops = 0
    while hi - lo > eps and loops < cap:
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
        loops += 1
    return (lo + hi) / 2, loops


def sqrt_bad_hi(x, iters=100):
    lo, hi = 0.0, x                      # WRONG for x < 1: sqrt(x) > x
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def halvings(width, tol):
    # smallest h with width / 2**h <= tol
    h = 0
    while width / 2 ** h > tol:
        h += 1
    return h


# examples from the prompt
for x, want in [(2, 1.41421356), (0.25, 0.5), (0, 0.0), (10**6, 1000.0)]:
    assert abs(sqrt_fixed(x) - want) <= 1e-6
    assert abs(sqrt_eps(x, 1e-9)[0] - want) <= 1e-6
    print("x =", x, "fixed:", sqrt_fixed(x), " eps loop:", sqrt_eps(x, 1e-9))

# hi = x is wrong below 1
print("hi = x with x=0.25 gives", sqrt_bad_hi(0.25), "(true 0.5)")
assert abs(sqrt_bad_hi(0.25) - 0.5) > 0.2

# eps below float spacing never terminates
ans, loops = sqrt_eps(10**6, 1e-15, cap=10**6)
print("eps=1e-15, x=10**6: loops =", loops, "(hit the 10**6 cap)", " spacing near 1000:", math.ulp(1000.0))
assert loops == 10**6
ans2, loops2 = sqrt_eps(10**6, 1e-9)
print("eps=1e-9, x=10**6: loops =", loops2)
assert loops2 < 100

# halvings needed
print("halvings for width 10**6 to tol 1e-6:", halvings(10**6, 1e-6))
print("halvings for width 1 to tol 1e-6:", halvings(1, 1e-6))
assert halvings(10**6, 1e-6) == 40 and halvings(1, 1e-6) == 20

# seeded cross-check against math.sqrt, including x < 1
rng = random.Random(31)
worst = 0.0
for _ in range(2000):
    x = rng.choice([rng.random(), rng.uniform(0, 10), rng.uniform(0, 10**6), float(rng.randint(0, 10**6))])
    err = abs(sqrt_fixed(x) - math.sqrt(x))
    worst = max(worst, err)
    assert err <= 1e-6
    assert abs(sqrt_eps(x, 1e-9)[0] - math.sqrt(x)) <= 1e-6
print("2000 random x: worst error of fixed-100 version =", worst)
print("all checks passed")
```

**Output (my run):**
```text
x = 2 fixed: 1.414213562373095  eps loop: (1.4142135619185865, 31)
x = 0.25 fixed: 0.5  eps loop: (0.5000000004656613, 30)
x = 0 fixed: 3.944304526105059e-31  eps loop: (4.656612873077393e-10, 30)
x = 1000000 fixed: 1000.0  eps loop: (999.99999999989, 50)
hi = x with x=0.25 gives 0.25 (true 0.5)
eps=1e-15, x=10**6: loops = 1000000 (hit the 10**6 cap)  spacing near 1000: 1.1368683772161603e-13
eps=1e-9, x=10**6: loops = 50
halvings for width 10**6 to tol 1e-6: 40
halvings for width 1 to tol 1e-6: 20
2000 random x: worst error of fixed-100 version = 1.1368683772161603e-13
all checks passed
```

All four prompt examples are right. The `eps = 1e-9` loop took about 30 to 50 loops. The `eps = 1e-15` loop for x = 10^6 hit my 10^6-loop cap, which proves it would never end. Timings were not needed; the loop counts are the evidence.

**Edge cases:**
- x = 0: the answer is 0 (the fixed version returns about 4e-31, inside tolerance).
- 0 < x < 1: needs `hi = 1`. x = 1: root is 1, fine.
- Large x = 10^6: root 1000, the float spacing near the answer is about 1.1e-13, so asking for less than that is impossible.
- Negative x: out of range; I would raise an error.

**Follow-ups:**
- "How many iterations for tolerance t?" ceil(log2(width / t)). Width 10^6, t = 1e-6 gives 40.
- "Why not `x ** 0.5`?" It is fine in real life. The question tests the search pattern.
- "Can I compare floats with ==?" No. Use the predicate with `<=` and a bounded loop.

**Common mistakes:**
- `hi = x` for x < 1.
- `while hi - lo > eps` with eps smaller than the float spacing (infinite loop).
- Stopping at `lo == hi` or checking `mid*mid == x` for equality on floats.
- Returning `lo` after a short loop; the midpoint `(lo + hi) / 2` is closer.

---

### Q32 ⭐ 🟡 Integer k-th root. Given integers x (0 <= x <= 10^18) and n (1 <= n <= 60), return floor(x^(1/n)) exactly. Binary search the integer r in [0, x] (hi = x is fine; Python integers are unbounded) with the predicate r**n <= x using Python's big integers. Show why `int(x ** (1 / n))` is unsafe (it rounds toward a wrong integer on exact roots) and why the predicate should be computed in integers. Example: x=27, n=3 -> 3; x=125, n=3 -> 5 (the float expression int(125 ** (1/3)) gives 4); x=80, n=4 -> 2; x=10**18, n=2 -> 10**9; x=0, n=5 -> 0; x=1, n=60 -> 1.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on an integer answer with an exact integer predicate. The answer is the last r with `r**n <= x`.

**Say this first (1 line):** "Binary search r in [0, x] for the largest r with r**n <= x, using Python big integers so the test is exact; the float `x ** (1/n)` rounds wrongly on exact roots."

**Brute force:** Increase r from 0 while `(r + 1)**n <= x`. That is about x^(1/n) steps, which is 10^9 for x = 10^18 and n = 2. Fine as a checker on small x only.

**Optimal:**
- `lo, hi = 0, x`. The predicate `r**n <= x` is True...True False...False, because r**n grows with r (n >= 1).
- I want the LAST True, so I use the upper middle: `mid = (lo + hi + 1) // 2`. If `mid**n <= x`, set `lo = mid`, else `hi = mid - 1`. With the lower middle the loop would not progress when `hi = lo + 1`.
- `hi = x` is safe in Python: no overflow, and r**n for r up to 10^18 and n = 60 is a number of about 1,000 digits, which is still cheap.
- Invariant: `lo**n <= x`, and every value above `hi` fails.
- Why floats fail: 125 ** (1/3) is 4.999999999999999 (the exponent 1/3 is not exact), so `int()` gives 4. My run found 888 exact roots r**n (n = 2..8, r < 300) where the float shortcut is wrong. It can also be wrong between roots: for x = 10^18 - 1 and n = 2, `x ** 0.5` becomes 1e9 but the exact answer is 999999999, because x itself rounds to 1e18 as a float.
- Speed-up (optional): start with `hi = 1 << (x.bit_length() // n + 1)`, which cuts the iterations from about 60 to about log2(root). Not needed here.

**Complexity:** About log2(x) <= 60 iterations; each computes `mid**n` on integers of up to ~n*60 bits. Time O(log x * M(n log x)), in plain words about 60 big-int powers. Space O(1) extra, aside from the big temporary.

**Dry run:** x = 80, n = 4, lo = 0, hi = 80.
| mid | mid**4 vs 80 | next |
|---|---|---|
| 40 | far above | hi = 39 |
| 20 | 160000 > 80 | hi = 19 |
| 10 | 10000 > 80 | hi = 9 |
| 5 | 625 > 80 | hi = 4 |
| 2 (lo=0, hi=4, mid=(0+4+1)//2) | 16 <= 80 | lo = 2 |
| 3 | 81 > 80 | hi = 2 |

lo == hi == 2, so the answer is 2.

**Code:**
```python
import random


def kth_root(x, n):
    lo, hi = 0, x                        # predicate r**n <= x is True...True False...False; find the last True
    while lo < hi:
        mid = (lo + hi + 1) // 2         # upper mid so the loop makes progress
        if mid ** n <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def kth_root_brute(x, n):
    r = 0
    while (r + 1) ** n <= x:
        r += 1
    return r


# prompt examples
for x, n, want in [(27, 3, 3), (125, 3, 5), (80, 4, 2), (10**18, 2, 10**9), (0, 5, 0), (1, 60, 1)]:
    assert kth_root(x, n) == want, (x, n)
    print("x =", x, "n =", n, "->", kth_root(x, n))
print("float 125 ** (1/3) =", 125 ** (1 / 3), "-> int() gives", int(125 ** (1 / 3)))
assert int(125 ** (1 / 3)) == 4

# how often is the float shortcut wrong on exact roots r**n?
bad = [(r, n) for n in range(2, 9) for r in range(1, 300) if int((r ** n) ** (1 / n)) != r]
print("exact roots r**n (n=2..8, r<300) where int(x ** (1/n)) is wrong:", len(bad), "e.g.", bad[:5])
assert (5, 3) in bad
# and it can be wrong off exact roots at large x
x = 10**18 - 1
print("float root of 10**18-1 (n=2):", int(x ** 0.5), "exact:", kth_root(x, 2))

# seeded cross-check
rng = random.Random(32)
for _ in range(600):
    n = rng.randint(1, 8)
    x = rng.randint(0, 5000)
    assert kth_root(x, n) == kth_root_brute(x, n), (x, n)
# exhaustive for small x and n
for n in range(1, 7):
    for x in range(0, 400):
        assert kth_root(x, n) == kth_root_brute(x, n)
# exact-boundary property on big values
for _ in range(300):
    n = rng.randint(1, 60)
    x = rng.randint(0, 10**18)
    r = kth_root(x, n)
    assert r ** n <= x < (r + 1) ** n
for n in range(1, 61):
    for r in (1, 2, 3, 7):
        assert kth_root(r ** n, n) == r and kth_root(r ** n - 1, n) == r - 1
# edge asserts
assert kth_root(0, 1) == 0 and kth_root(1, 1) == 1 and kth_root(10**18, 1) == 10**18
assert kth_root(10**18, 60) == 1      # 2**60 = 1.15e18 > 1e18, so only 1 fits
print("all checks passed")
```

**Output (my run):**
```text
x = 27 n = 3 -> 3
x = 125 n = 3 -> 5
x = 80 n = 4 -> 2
x = 1000000000000000000 n = 2 -> 1000000000
x = 0 n = 5 -> 0
x = 1 n = 60 -> 1
float 125 ** (1/3) = 4.999999999999999 -> int() gives 4
exact roots r**n (n=2..8, r<300) where int(x ** (1/n)) is wrong: 888 e.g. [(4, 3), (5, 3), (6, 3), (7, 3), (8, 3)]
float root of 10**18-1 (n=2): 1000000000 exact: 999999999
all checks passed
```

All six prompt examples match. The exhaustive check covers every x < 400 for n = 1..6. The boundary check shows `kth_root(r**n) == r` and `kth_root(r**n - 1) == r - 1` for n = 1..60.

**Edge cases:**
- x = 0: lo = hi = 0, returns 0. x = 1: returns 1 for any n.
- n = 1: the answer is x itself (the search still works).
- x < 2^n (such as 10^18 with n = 60): the root is 1.
- Perfect powers and their predecessors: tested above.

**Follow-ups:**
- "Can I use `round(x ** (1/n))` and correct it?" Yes: take that guess g, then fix it with `while g**n > x: g -= 1` and `while (g+1)**n <= x: g += 1`. It works, but the search is easier to prove.
- "What about floats x?" Then it is the real-valued search from Q31.
- "Is `**` exact on ints?" Yes, Python ints are unbounded.

**Common mistakes:**
- `int(x ** (1 / n))` with floats.
- Using the lower middle when searching for the last True (infinite loop).
- Restricting `hi` to something like `x // 2` and breaking x = 0 or x = 1.

---

### Q33 ⭐ 🟡 Designing and proving a monotone predicate. Binary search on the answer needs a predicate that is False...False True...True (or the reverse) over the whole search range. For each of two candidate predicates decide whether it is monotone and justify it, and for any that is not, give a concrete counterexample: (a) 'with capacity c the packages [1,2,3] take EXACTLY 2 days under greedy loading (False when a package exceeds c)', over c = 1..7; (b) 'some subarray of length L has sum >= 10' for arr=[5,-10,5,5] over L = 1..4, versus the same predicate on a list of non-negative numbers. Show how to restate (a) as 'at most 2 days' to make it monotone. Example: (a) with the rule that a capacity below the heaviest package is False, outputs for c=1..7 -> [False, False, True, True, True, False, False] (c=3..5 take 2 days, c>=6 take 1); (b) for arr=[5,-10,5,5] -> [False, True, False, False]. (For a monotone length predicate that does work, see Part 3 Q40.)
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Monotone predicate design for binary search on the answer. The search is only valid when the predicate flips once.

**Say this first (1 line):** "A predicate is searchable only if moving the parameter in one direction can never undo a True; 'exactly 2 days' fails that, 'at most 2 days' passes, and a subarray-sum test fails with negatives."

**Brute force:** Evaluate the predicate at every parameter value and check that the list has at most one flip. That is my monotonicity test, and I use it as a checker (exhaustive on small inputs).

**Optimal:** Decide by reasoning, then confirm by counterexample.
- (a) "Exactly 2 days" with greedy loading. Days by capacity for [1,2,3] are None, None, 2, 2, 2, 1, 1 for c = 1..7. Exactly-2 gives [F, F, T, T, T, F, F]: True then False, and the left False is the "too small" case. Not monotone. Counterexample: c = 5 is True, c = 6 is False, yet 6 > 5 means a looser limit.
- Why it breaks: more capacity can only lower the day count (never raise it), so the day count passes THROUGH 2 and keeps falling to 1. "Equal to" cannot be a threshold.
- Fix: "at most 2 days", i.e. `days(c) <= 2` with False for c below the heaviest package. That gives [F, F, T, T, T, T, T]. Reason: greedy days are non-increasing in c (a larger bin never needs more bins), and "non-increasing <= 2" is True from some point on. I checked this over 6,372 small (weights, d) cases.
- (b) "Some subarray of length L has sum >= 10" for [5, -10, 5, 5]: L = 1..4 gives [F, T, F, F]. Not monotone. Counterexample: L = 2 is True (the last two elements, 5 + 5 = 10) and L = 3 is False, because every length-3 window contains the -10.
- With non-negative numbers it IS monotone: a window of length L with sum >= T can be extended by one neighbour that adds >= 0, so L + 1 also works (when L < n). That is why the prefix-sum length search works in Part 3 Q40's setting.
- Rule: write the predicate as "answer <= p" or "answer >= p" (a threshold), not "answer == p".

**Complexity:** Each predicate evaluation here is O(n) (greedy loading pass, or window sums). Checking monotonicity by brute force costs the number of parameter values times that. For the search itself: O(n log range) once the predicate is monotone.

**Dry run:** Packages [1, 2, 3], c = 5: load 1, 2 (sum 3), adding 3 would give 6 > 5, so start day 2 with 3. Days = 2, so exactly-2 is True. c = 6: 1 + 2 + 3 = 6 fits, one day, so exactly-2 is False, but at-most-2 is True. For (b), L = 2 windows: [5, -10] = -5, [-10, 5] = -5, [5, 5] = 10, so True. L = 3: [5, -10, 5] = 0, [-10, 5, 5] = 0, so False.

**Code:**
```python
import random
from itertools import product


def days_needed(weights, c):
    # greedy loading in order; None when a package is heavier than c
    if any(w > c for w in weights):
        return None
    days, load = 1, 0
    for w in weights:
        if load + w > c:
            days += 1
            load = 0
        load += w
    return days


def pred_exact(weights, d, c):
    return days_needed(weights, c) == d


def pred_atmost(weights, d, c):
    t = days_needed(weights, c)
    return t is not None and t <= d


def has_sub_sum(arr, L, target):
    return any(sum(arr[i:i + L]) >= target for i in range(len(arr) - L + 1))


def is_monotone(seq):
    # True...True/False...False in either direction: at most one flip
    return sum(1 for a, b in zip(seq, seq[1:]) if a != b) <= 1


w = [1, 2, 3]
a = [pred_exact(w, 2, c) for c in range(1, 8)]
print("(a) exactly 2 days, c=1..7:", a, " monotone?", is_monotone(a))
assert a == [False, False, True, True, True, False, False]
print("    days by capacity:", [days_needed(w, c) for c in range(1, 8)])
a2 = [pred_atmost(w, 2, c) for c in range(1, 8)]
print("(a) at most 2 days, c=1..7:", a2, " monotone?", is_monotone(a2))
assert a2 == [False, False, True, True, True, True, True]

arr = [5, -10, 5, 5]
b = [has_sub_sum(arr, L, 10) for L in range(1, 5)]
print("(b) arr=[5,-10,5,5], L=1..4:", b, " monotone?", is_monotone(b))
assert b == [False, True, False, False]

# at-most-d predicate is monotone in c: exhaustive over small package lists
checked = 0
for n in range(1, 6):
    for ws in product(range(1, 5), repeat=n):
        for d in range(1, n + 1):
            seq = [pred_atmost(list(ws), d, c) for c in range(1, sum(ws) + 2)]
            assert is_monotone(seq) and (not seq or seq[-1]), (ws, d)
            checked += 1
print("at-most-d monotone in capacity: checked", checked, "(weights, d) cases")

# how often is the exact-d predicate NOT monotone? (random seeded)
rng = random.Random(33)
nonmono = 0
for _ in range(500):
    ws = [rng.randint(1, 6) for _ in range(rng.randint(2, 6))]
    d = rng.randint(1, len(ws))
    seq = [pred_exact(ws, d, c) for c in range(1, sum(ws) + 2)]
    nonmono += not is_monotone(seq)
print("exact-d predicate non-monotone in", nonmono, "of 500 random cases")
assert nonmono > 0

# (b) non-negative lists: 'some window of length L has sum >= T' is monotone in L (exhaustive small)
cnt = 0
for n in range(1, 6):
    for xs in product(range(0, 4), repeat=n):
        for T in range(0, 12):
            seq = [has_sub_sum(list(xs), L, T) for L in range(1, n + 1)]
            # larger L can only add non-negative amounts to a best window, so once True stays True
            assert all(not (a and not b) for a, b in zip(seq, seq[1:])), (xs, T)
            cnt += 1
print("non-negative: once True stays True for larger L, checked", cnt, "cases")
# with negatives it fails
neg_fail = 0
for _ in range(500):
    xs = [rng.randint(-5, 5) for _ in range(rng.randint(2, 6))]
    T = rng.randint(1, 6)
    seq = [has_sub_sum(xs, L, T) for L in range(1, len(xs) + 1)]
    neg_fail += any(a and not b for a, b in zip(seq, seq[1:]))
print("with negatives, True then False happened in", neg_fail, "of 500 random cases")
assert neg_fail > 0
print("all checks passed")
```

**Output (my run):**
```text
(a) exactly 2 days, c=1..7: [False, False, True, True, True, False, False]  monotone? False
    days by capacity: [None, None, 2, 2, 2, 1, 1]
(a) at most 2 days, c=1..7: [False, False, True, True, True, True, True]  monotone? True
(b) arr=[5,-10,5,5], L=1..4: [False, True, False, False]  monotone? False
at-most-d monotone in capacity: checked 6372 (weights, d) cases
exact-d predicate non-monotone in 279 of 500 random cases
non-negative: once True stays True for larger L, checked 16368 cases
with negatives, True then False happened in 172 of 500 random cases
all checks passed
```

Both prompt example lists are right as given: (a) [F, F, T, T, T, F, F] (with c < heaviest False) and (b) [F, T, F, F]. In 279 of 500 random package lists the exact-d predicate was not monotone, and with negatives, True-then-False appeared in 172 of 500 random lists.

**Edge cases:**
- Capacity below the heaviest package: define the predicate as False (no valid loading), so the False region starts at the left.
- d >= number of packages: at-most-d is True from c = heaviest.
- All-negative or zero-sum lists in (b): with target 10 everything is False, trivially monotone.
- A single flip may be True...False, so say which direction you search.

**Follow-ups:**
- "How do I prove monotone in an interview?" Give the exchange or extension argument: a solution for the stricter parameter also works for the looser one.
- "What if I need exactly k?" Search for the smallest c with at-most-k days; the exact count can then be adjusted separately.
- "Does the same trap appear elsewhere?" Yes: "is there a split with sum exactly S" is not a threshold; "largest part <= S" is.

**Common mistakes:**
- Using `==` in the predicate.
- Forgetting the infeasible region (c below the heaviest package).
- Assuming a sliding "length" predicate is monotone when values can be negative.
- Believing a True once found on a non-monotone predicate means every larger value works.

---

### Q34 ⭐ 🟡 K-th missing positive number: search on index versus on value. `arr` is a strictly increasing list of positive integers (1 <= len <= 1000) and k >= 1. Return the k-th positive integer that is not in arr. The count of missing positives before arr[i] is arr[i] - (i + 1), which is non-decreasing in i, so binary search the INDEX of the first i where that count >= k; the answer is then k + i (with i = len(arr) when none). Contrast this with searching over the VALUE range [1, arr[-1] + k] using the predicate 'missing positives <= v is >= k', and say which has fewer lines and which generalises. Example: [2,3,4,7,11], k=5 -> 9; [1,2,3,4], k=2 -> 6; [5,6], k=1 -> 1; [1,3], k=1 -> 2; [2], k=3 -> 4.
**Asked at:** Binary-search question roundups (igotanoffer.com binary-search list, which numbers Koko eating bananas and capacity to ship packages as listed questions and links rotated-array search and first/last position; snippet only, not opened); prep content, not company reports | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a derived non-decreasing array (missing count before each index), or on the value range with a counting predicate.

**Say this first (1 line):** "Before arr[i] there are arr[i] - (i + 1) missing positives, which never decreases, so I find the first index where that reaches k and the answer is k + i."

**Brute force:** Walk v = 1, 2, 3, ... using a set of arr, count the numbers not in the set, stop at the k-th. O(len + answer), where the answer can be up to arr[-1] + k.

**Optimal (index search):**
- `missing(i) = arr[i] - (i + 1)`. Strictly increasing arr means each step raises arr[i] by at least 1, so missing(i) is non-decreasing.
- Find the smallest i with `missing(i) >= k` (`lo = 0, hi = len(arr)`, `hi = len` meaning none). The k-th missing number is then before arr[i] and after arr[i-1].
- Answer is `k + i`. Why: among the numbers 1..answer there are exactly i array elements (those before index i), so answer - i of them are missing, and the k-th missing means answer - i = k.
- If no index qualifies, i = len(arr) and the answer is k + len(arr), past the end.

**Optimal (value search):** Search v in [1, arr[-1] + k] for the smallest v with `v - (count of arr <= v) >= k`. The counting uses an inner bisect, so it is O(log^2) unless you do it carefully.

**Which is better:** The index search is shorter (no inner count) and O(log n). The value search generalises: it works when the predicate is a count over values (multiplication table, pair distances) and there is no tidy per-index formula. Say both in an interview.

**Complexity:** Index search: time O(log n), space O(1). Value search: O(log(arr[-1] + k) * log n), space O(1).

**Dry run:** arr = [2, 3, 4, 7, 11], k = 5. missing(i) = 1, 1, 1, 3, 6.
| lo | hi | mid | missing(mid) | action |
|---|---|---|---|---|
| 0 | 5 | 2 | 1 < 5 | lo = 3 |
| 3 | 5 | 4 | 6 >= 5 | hi = 4 |
| 3 | 4 | 3 | 3 < 5 | lo = 4 |

i = 4, answer = 5 + 4 = 9. Check: the missing numbers are 1, 5, 6, 8, 9, so the 5th is 9.

**Code:**
```python
import random


def kth_missing_index(arr, k):
    # first index i with arr[i] - (i + 1) >= k; answer k + i
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) >= k:
            hi = mid
        else:
            lo = mid + 1
    return k + lo


def kth_missing_value(arr, k):
    # smallest v with (missing positives <= v) >= k; missing(v) = v - (count of arr <= v)
    def missing_upto(v):
        # count of arr elements <= v by binary search
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= v:
                lo = mid + 1
            else:
                hi = mid
        return v - lo
    lo, hi = 1, arr[-1] + k
    while lo < hi:
        mid = (lo + hi) // 2
        if missing_upto(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_missing_brute(arr, k):
    s, v = set(arr), 0
    while k:
        v += 1
        if v not in s:
            k -= 1
    return v


for arr, k, want in [([2, 3, 4, 7, 11], 5, 9), ([1, 2, 3, 4], 2, 6), ([5, 6], 1, 1), ([1, 3], 1, 2), ([2], 3, 4)]:
    got = (kth_missing_index(arr, k), kth_missing_value(arr, k), kth_missing_brute(arr, k))
    print(arr, "k =", k, "-> index search, value search, brute:", got)
    assert got == (want, want, want)

rng = random.Random(34)
for _ in range(1500):
    n = rng.randint(1, 12)
    arr = sorted(rng.sample(range(1, 30), n))
    k = rng.randint(1, 40)
    b = kth_missing_brute(arr, k)
    assert kth_missing_index(arr, k) == b == kth_missing_value(arr, k), (arr, k)
# exhaustive: every strictly increasing list from 1..8, k = 1..12
from itertools import combinations
cnt = 0
for n in range(1, 9):
    for arr in combinations(range(1, 9), n):
        for k in range(1, 13):
            assert kth_missing_index(list(arr), k) == kth_missing_brute(list(arr), k)
            cnt += 1
print("exhaustive cases checked:", cnt)
# edge asserts
assert kth_missing_index([1], 1) == 2          # nothing missing before arr[0]
assert kth_missing_index([1000], 1) == 1       # missing count before first element is 999
assert kth_missing_index([1000], 999) == 999
assert kth_missing_index([1000], 1000) == 1001 # past the end
print("all checks passed")
```

**Output (my run):**
```text
[2, 3, 4, 7, 11] k = 5 -> index search, value search, brute: (9, 9, 9)
[1, 2, 3, 4] k = 2 -> index search, value search, brute: (6, 6, 6)
[5, 6] k = 1 -> index search, value search, brute: (1, 1, 1)
[1, 3] k = 1 -> index search, value search, brute: (2, 2, 2)
[2] k = 3 -> index search, value search, brute: (4, 4, 4)
exhaustive cases checked: 3060
all checks passed
```

All five prompt examples are right and the three methods agree. I also ran every strictly increasing list drawn from 1..8 against k = 1..12 (3,060 cases).

**Edge cases:**
- arr[0] = 1: nothing missing before it (missing(0) = 0).
- arr[0] large: [1000] with k = 1 gives 1.
- k beyond the last element: [1000] with k = 1000 gives 1001.
- Length 1, k = 1: still correct.

**Follow-ups:**
- "What if arr may have duplicates?" The formula breaks. Deduplicate first, or use the value search with a count of distinct values.
- "What if the list is not sorted?" Sort it or use a set; no binary search then.
- "What if arr is huge and k small?" Index search stays O(log n).

**Common mistakes:**
- Using `arr[i] - i` instead of `arr[i] - (i + 1)`.
- Returning `arr[lo - 1] + (k - missing(lo - 1))` and mishandling lo = 0.
- Forgetting the past-the-end case.

---

### Q35 ⭐ 🔴 K-th smallest element of two sorted arrays in O(log(min(m, n))). `a` and `b` are sorted ascending (not both empty), and k is 1-based with 1 <= k <= len(a) + len(b); k counts duplicates. Binary search how many elements i come from `a` (and k - i from `b`) so that the cut is consistent: a[i-1] <= b[k-i] and b[k-i-1] <= a[i]. Say how this generalises the median-of-two-arrays cut and why the merge walk is only O(k). (The merge-walk baseline is Part 2 Q40.) Example: a=[1,3,8], b=[2,4,6,9], k=4 -> 4; a=[1,2], b=[1,2], k=3 -> 2; a=[], b=[3,5], k=2 -> 5; a=[7], b=[1,2,3], k=1 -> 1; a=[7], b=[1,2,3], k=4 -> 7.
**Asked at:** Median-of-two-sorted-arrays pages (techinterview.org 'binary search's nastiest cousin' page saying the O(m+n) merge is the usual first answer and O(log) is the expected follow-up, educative.io grokking page, a jointaro page with a company filter; snippets only, not opened; no company report verified) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports
**Pattern:** Binary search on a partition point (how many of the k smallest come from `a`). It is the median-of-two-arrays idea with a free k.

**Say this first (1 line):** "Pick i elements from a and k - i from b so everything on the left is <= everything on the right; binary search i, and the k-th is the larger of the two left boundaries."

**Brute force:** Merge both lists and take the k-th. Sorting the concatenation is O((m + n) log(m + n)); the merge walk stops after k steps, O(k) (Part 2 Q40 is the merge-walk baseline). With k near the middle of two million values that is a million steps.

**Optimal:**
- The k smallest form a prefix of `a` of length i and a prefix of `b` of length j = k - i.
- Valid i satisfies `a[i-1] <= b[j]` and `b[j-1] <= a[i]` (missing neighbours count as infinity or minus infinity).
- Range: `lo = max(0, k - n)` (we cannot take more than n from b), `hi = min(k, m)`.
- While lo < hi: `i = (lo + hi) // 2`, `j = k - i`. If `a[i] < b[j-1]`, then a[i] belongs among the k smallest, so take more from a: `lo = i + 1`. Else `hi = i`.
- Why indexes are safe: i < hi <= m so a[i] exists; i < hi <= k so j >= 1; j <= k - lo <= n so b[j-1] exists.
- Answer: `max(a[i-1] if i else -inf, b[j-1] if j else -inf)`.
- Invariant: the correct cut lies in [lo, hi]. Duplicates are fine because the tests use `<` on one side and `<=` implicitly on the other.
- It generalises the median: the median is k = (m + n + 1) // 2 (and for even totals, also k + 1).

**Complexity:** Time O(log(min(m, n, k))): the search range is at most min(k, m) - max(0, k - n), no bigger than min(m, n). Space O(1). The merge walk is O(k).

**Dry run:** a = [1, 3, 8], b = [2, 4, 6, 9], k = 4. lo = 0, hi = 3.
| lo | hi | i | j | test | action |
|---|---|---|---|---|---|
| 0 | 3 | 1 | 3 | a[1] = 3 < b[2] = 6 | lo = 2 |
| 2 | 3 | 2 | 2 | a[2] = 8 < b[1] = 4? no | hi = 2 |

i = 2, j = 2: left parts are [1, 3] and [2, 4]. The larger boundary is max(a[1], b[1]) = max(3, 4) = 4. The merged order 1, 2, 3, 4, ... agrees.

**Code:**
```python
import random


def kth_two(a, b, k):
    m, n = len(a), len(b)
    lo, hi = max(0, k - n), min(k, m)      # i = how many of the k smallest come from a
    while lo < hi:
        i = (lo + hi) // 2
        j = k - i
        # i < hi <= m so a[i] exists; i < hi <= k so j >= 1; j <= k - lo <= n so b[j-1] exists
        if a[i] < b[j - 1]:
            lo = i + 1                      # a[i] must be among the k smallest: take more from a
        else:
            hi = i
    i, j = lo, k - lo
    left = []
    if i > 0:
        left.append(a[i - 1])
    if j > 0:
        left.append(b[j - 1])
    return max(left)


def kth_merge(a, b, k):
    # O(k) merge walk (Part 2 Q40 style)
    i = j = 0
    for _ in range(k):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            v = a[i]; i += 1
        else:
            v = b[j]; j += 1
    return v


def kth_sorted(a, b, k):
    return sorted(a + b)[k - 1]


for a, b, k, want in [([1, 3, 8], [2, 4, 6, 9], 4, 4), ([1, 2], [1, 2], 3, 2), ([], [3, 5], 2, 5),
                      ([7], [1, 2, 3], 1, 1), ([7], [1, 2, 3], 4, 7)]:
    got = (kth_two(a, b, k), kth_merge(a, b, k), kth_sorted(a, b, k))
    print(a, b, "k =", k, "->", got)
    assert got == (want,) * 3

rng = random.Random(35)
cases = 0
for _ in range(4000):
    a = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 7)))
    b = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 7)))
    if not a and not b:
        continue
    for k in range(1, len(a) + len(b) + 1):
        assert kth_two(a, b, k) == kth_sorted(a, b, k), (a, b, k)
        cases += 1
print("random (a, b, k) cases checked:", cases)

# median from k-th (ties with duplicates included)
a, b = [1, 3], [2]
tot = len(a) + len(b)
assert kth_two(a, b, (tot + 1) // 2) == 2
# edges: one side empty, all equal, k = total, disjoint ranges
assert kth_two([], [5], 1) == 5 and kth_two([5], [], 1) == 5
assert kth_two([4, 4, 4], [4, 4], 5) == 4
assert kth_two([1, 2], [10, 11], 4) == 11 and kth_two([10, 11], [1, 2], 1) == 1
# big input: the search takes about 20 steps, not 10**6
big_a = list(range(0, 2 * 10**6, 2))
big_b = list(range(1, 2 * 10**6, 2))
assert kth_two(big_a, big_b, 10**6) == 10**6 - 1
print("all checks passed")
```

**Output (my run):**
```text
[1, 3, 8] [2, 4, 6, 9] k = 4 -> (4, 4, 4)
[1, 2] [1, 2] k = 3 -> (2, 2, 2)
[] [3, 5] k = 2 -> (5, 5, 5)
[7] [1, 2, 3] k = 1 -> (1, 1, 1)
[7] [1, 2, 3] k = 4 -> (7, 7, 7)
random (a, b, k) cases checked: 27983
all checks passed
```

All five prompt examples pass. The random check covers 27,983 (a, b, k) triples with duplicates and empty sides, each k from 1 to the total, against sorted concatenation.

**Edge cases:**
- One list empty: the range collapses (an empty `a` gives hi = 0, so i = 0), and the answer is the k-th of the other.
- k = 1: the minimum of the two heads. k = m + n: the overall maximum.
- All equal values: any cut works; the max of boundaries is the same value.
- Disjoint ranges: i is 0 or m.

**Follow-ups:**
- "How do I get the median?" k-th with k = (m + n + 1) // 2; for an even total average it with the (k + 1)-th.
- "Other approach?" Discard k/2 elements from one list each round (compare a[k/2 - 1] and b[k/2 - 1]), also O(log k).
- "Why search the shorter list?" It keeps the range small. Here the range is already clipped by `lo` and `hi`.

**Common mistakes:**
- Not clipping the range, so i or k - i falls outside a list.
- Off-by-one between 0-based indices and 1-based k.
- Treating missing neighbours as 0 instead of infinities (bad with negative numbers).

---

### Q36 ⭐ 🔴 Maximum average of a subarray with length at least k (binary search on a real answer). `nums` has 1 <= k <= len <= 10^4 integers (values may be negative). Return the largest average over all contiguous subarrays of length >= k, within 10^-5. Binary search the average t: a subarray of length >= k has average >= t iff after subtracting t from every element some such subarray has sum >= 0, checked with prefix sums and the minimum prefix seen so far at least k positions back. State the search range [min(nums), max(nums)], an iteration count that reaches 10^-5, and why 'some average >= t exists' is monotone in t. Example: [1,12,-5,-6,50,3], k=4 -> 12.75; [5], k=1 -> 5.0; [-3,-1,-2], k=2 -> -1.5; [0,4,0,3,2], k=1 -> 4.0.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a real answer with a feasibility check: "does some subarray of length >= k average at least t?"

**Say this first (1 line):** "Guess the average t, subtract it from every element, and ask whether some subarray of length >= k has sum >= 0; that test is monotone in t, so I search t between min and max."

**Brute force:** Try every subarray of length >= k with prefix sums, tracking the best sum / length. O(n^2) time. I use exact fractions to build my checker.

**Optimal:**
- Predicate `feasible(t)`: an average >= t exists iff some window of length >= k has `sum(x - t) >= 0`.
- Build prefix sums `P` of `x - t`. For each end index i >= k, the best start is the one with the smallest `P[j]` for j <= i - k. Keep `best_min` as a running minimum of `P[i - k]`. If `P[i] - best_min >= 0`, return True. That is O(n).
- Monotone in t: if a window has average >= t, it also has average >= any smaller t. So feasible is True for small t and False for large t. I checked this on 300 random lists over a grid of t.
- Range: `lo = min(nums)`, `hi = max(nums)`. Every average lies between them, so the answer does too.
- Move: if feasible(mid), `lo = mid` (try higher), else `hi = mid`.
- Iterations: if values are within +-10^4, the width is at most 2*10^4 and 31 halvings reach 1e-5. I use a fixed 50 (width up to about 10^10 at that tolerance).
- Note: the prompt gives no value bound, so state the assumption; a fixed 100 is a safe default.

**Complexity:** Time O(n log(range / tol)) (n per check, about 50 checks). Space O(n) for the prefix array (O(1) is possible by keeping two running prefix sums, one lagging k behind). Floating-point error is tiny at this scale (worst seen 3.6e-14).

**Dry run:** nums = [1, 12, -5, -6, 50, 3], k = 4.
- t = 12: x - t = -11, 0, -17, -18, 38, -9; prefix 0, -11, -11, -28, -46, -8, -17. At i = 5, best_min = min(P0, P1) = -11 and P5 - (-11) = 3 >= 0. Feasible.
- t = 13: prefix 0, -12, -13, -31, -50, -13, -23. At i = 5, best_min = -12 and P5 + 12 = -1. At i = 6, best_min = -13, P6 + 13 = -10. Not feasible.
So the answer is between 12 and 13. The exact value is 12.75 (window [12, -5, -6, 50], 51 / 4).

**Code:**
```python
import random
from fractions import Fraction


def feasible(nums, k, t):
    # some subarray of length >= k has average >= t  <=>  some such subarray has sum(x - t) >= 0
    pre = [0.0]
    for x in nums:
        pre.append(pre[-1] + (x - t))
    best_min = float("inf")
    for i in range(k, len(pre)):
        best_min = min(best_min, pre[i - k])     # smallest prefix at least k back
        if pre[i] - best_min >= 0:
            return True
    return False


def max_avg(nums, k, iters=50):
    lo, hi = float(min(nums)), float(max(nums))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if feasible(nums, k, mid):
            lo = mid                              # t is achievable, try higher
        else:
            hi = mid
    return lo


def max_avg_brute(nums, k):
    best = None
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if j - i + 1 >= k:
                v = Fraction(s, j - i + 1)
                if best is None or v > best:
                    best = v
    return best


for nums, k, want in [([1, 12, -5, -6, 50, 3], 4, 12.75), ([5], 1, 5.0), ([-3, -1, -2], 2, -1.5), ([0, 4, 0, 3, 2], 1, 4.0)]:
    got = max_avg(nums, k)
    print(nums, "k =", k, "->", round(got, 6), " brute:", float(max_avg_brute(nums, k)))
    assert abs(got - want) <= 1e-5 and float(max_avg_brute(nums, k)) == want

rng = random.Random(36)
worst = 0.0
for _ in range(1500):
    n = rng.randint(1, 10)
    nums = [rng.randint(-20, 20) for _ in range(n)]
    k = rng.randint(1, n)
    err = abs(max_avg(nums, k) - float(max_avg_brute(nums, k)))
    worst = max(worst, err)
    assert err <= 1e-5, (nums, k)
print("random cases: worst error =", worst)

# monotone in t: exhaustive over a grid of t for small lists
for _ in range(300):
    nums = [rng.randint(-9, 9) for _ in range(rng.randint(1, 8))]
    k = rng.randint(1, len(nums))
    seq = [feasible(nums, k, t / 4) for t in range(-40, 41)]
    assert all(not (not a and b) for a, b in zip(seq, seq[1:])), (nums, k)   # True then False only
# iterations needed: width 2*10**4 down to 1e-5
w, it = 2 * 10**4, 0
while w > 1e-5:
    w /= 2; it += 1
print("halvings from width 2*10**4 to 1e-5:", it)
assert it == 31
# edge asserts
assert abs(max_avg([7, 7, 7], 2) - 7.0) <= 1e-5            # all equal: lo == hi from the start
assert abs(max_avg([-5], 1) - (-5.0)) <= 1e-5
assert abs(max_avg([1, 2, 3, 4], 4) - 2.5) <= 1e-5          # k = n: only the whole array
print("all checks passed")
```

**Output (my run):**
```text
[1, 12, -5, -6, 50, 3] k = 4 -> 12.75  brute: 12.75
[5] k = 1 -> 5.0  brute: 5.0
[-3, -1, -2] k = 2 -> -1.5  brute: -1.5
[0, 4, 0, 3, 2] k = 1 -> 4.0  brute: 4.0
random cases: worst error = 3.552713678800501e-14
halvings from width 2*10**4 to 1e-5: 31
all checks passed
```

All four prompt examples match the exact-fraction brute force. The 1,500 seeded random lists had worst error 3.6e-14, well under 1e-5.

**Edge cases:**
- k = len(nums): only the whole array, answer is its mean.
- Single element: that element, even if negative.
- All equal: lo = hi after the search, answer is that value.
- Negative values: the range [min, max] still holds; the prefix test handles them.

**Follow-ups:**
- "Can the exact answer be found?" The optimum is always some integer ratio sum / length, so you can finish with an exact check, or compare Fractions.
- "What if k = 1?" The answer is simply max(nums), no search needed.
- "Why not sliding window?" The best window is not forced to have length k, and longer windows can win; a fixed-size window misses them.

**Common mistakes:**
- Using only windows of length exactly k.
- Using prefix `P[i - k + 1]` (off by one) or the global minimum prefix (allows windows shorter than k).
- Searching an integer range and returning an integer.
- Tolerance compare with == on floats.

---

### Q37 ⭐ 🔴 Median of a row-sorted matrix. `matrix` is r x c with r and c both odd positive integers (so r*c is odd), each row sorted ascending, no relation between rows, values up to 10^9, r*c <= 10^6. Return the median of all elements in O(r log c log(range)): binary search the VALUE v and count elements <= v per row with `bisect_right`, then return the smallest v with count >= (r*c + 1) // 2. Explain why that v is an actual entry and why the matrix cannot simply be flattened and bisected. Example: [[1,3,5],[2,6,9],[3,6,9]] -> 5; [[1]] -> 1; [[1,1,1],[2,2,2],[3,3,3]] -> 2.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the value range, with a monotone count: `count(<= v)` over rows, using `bisect_right` per row.

**Say this first (1 line):** "The matrix is not globally sorted, so I search the value v, count entries <= v row by row with bisect_right, and return the smallest v whose count reaches the middle rank."

**Brute force:** Flatten, sort, take element `len // 2`. O(rc log(rc)) time and O(rc) space. It is my checker.

**Optimal:**
- Middle rank `need = (r*c + 1) // 2`. With r*c odd, this is the 1-based position of the median.
- `lo = min(row[0])`, `hi = max(row[-1])`, since each row is sorted.
- `count(v) = sum(bisect_right(row, v) for row in matrix)`. It is non-decreasing in v, so find the smallest v with `count(v) >= need`.
- Why that v is an actual entry: for the smallest such v, `count(v - 1) < need <= count(v)`. So some entry equals v exactly (the count rose at v), and v is the need-th smallest value.
- Why not flatten-and-bisect: reading the rows one after another gives [1, 3, 5, 2, 6, 9, 3, 6, 9], which is not sorted, so there is no index to bisect. The rows are only sorted individually.
- Why r and c odd: r*c is odd, so there is one middle element and no averaging of two values.

**Complexity:** Time O(r * log c * log(range)): each value step does r bisects of O(log c). With range 10^9 that is about 30 steps (my run: 30 steps and 29,970 `bisect_right` calls for a 999 x 1001 matrix). Space O(1) extra.

**Dry run:** [[1,3,5],[2,6,9],[3,6,9]], need = 5, lo = 1, hi = 9.
| lo | hi | mid | count(<= mid) | action |
|---|---|---|---|---|
| 1 | 9 | 5 | 3 + 1 + 1 = 5 >= 5 | hi = 5 |
| 1 | 5 | 3 | 2 + 1 + 1 = 4 < 5 | lo = 4 |
| 4 | 5 | 4 | 2 + 1 + 1 = 4 < 5 | lo = 5 |

Answer 5, which is the 5th of 1, 2, 3, 3, 5, 6, 6, 9, 9.

**Code:**
```python
import random
from bisect import bisect_right

CALLS = 0


def count_le(matrix, v):
    global CALLS
    total = 0
    for row in matrix:
        CALLS += 1
        total += bisect_right(row, v)
    return total


def matrix_median(matrix):
    r, c = len(matrix), len(matrix[0])
    need = (r * c + 1) // 2                         # r*c odd, so this is the middle rank
    lo = min(row[0] for row in matrix)
    hi = max(row[-1] for row in matrix)
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(matrix, mid) >= need:
            hi = mid
        else:
            lo = mid + 1
    return lo


def matrix_median_brute(matrix):
    flat = sorted(x for row in matrix for x in row)
    return flat[len(flat) // 2]


for m, want in [([[1, 3, 5], [2, 6, 9], [3, 6, 9]], 5), ([[1]], 1), ([[1, 1, 1], [2, 2, 2], [3, 3, 3]], 2)]:
    print(m, "->", matrix_median(m), " brute:", matrix_median_brute(m))
    assert matrix_median(m) == matrix_median_brute(m) == want

rng = random.Random(37)
for _ in range(2000):
    r = rng.choice([1, 3, 5])
    c = rng.choice([1, 3, 5, 7])
    hi = rng.choice([3, 10, 100])
    m = [sorted(rng.randint(0, hi) for _ in range(c)) for _ in range(r)]
    v = matrix_median(m)
    assert v == matrix_median_brute(m), m
    assert any(v in row for row in m)               # the answer is an actual entry
print("2000 seeded random odd-by-odd matrices agree; answer was always an entry")

# why flattening-and-bisecting fails: flattening row by row is not sorted
m = [[1, 3, 5], [2, 6, 9], [3, 6, 9]]
flat = [x for row in m for x in row]
print("row-major flatten:", flat, "sorted?", flat == sorted(flat))
assert flat != sorted(flat)

# call count on a big case: r = 999, c = 1001 (about 10**6 entries), values up to 10**9
big = [sorted(rng.randint(0, 10**9) for _ in range(1001)) for _ in range(999)]
CALLS = 0
v = matrix_median(big)
steps = CALLS // 999
print("big matrix 999 x 1001: value-search steps =", steps, " bisect_right calls =", CALLS)
assert steps <= 30
assert v == matrix_median_brute(big)
# edge asserts
assert matrix_median([[7, 7, 7]]) == 7
assert matrix_median([[1], [2], [3]]) == 2
assert matrix_median([[5, 5, 5], [5, 5, 5], [5, 5, 5]]) == 5
assert matrix_median([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 5
print("all checks passed")
```

**Output (my run):**
```text
[[1, 3, 5], [2, 6, 9], [3, 6, 9]] -> 5  brute: 5
[[1]] -> 1  brute: 1
[[1, 1, 1], [2, 2, 2], [3, 3, 3]] -> 2  brute: 2
2000 seeded random odd-by-odd matrices agree; answer was always an entry
row-major flatten: [1, 3, 5, 2, 6, 9, 3, 6, 9] sorted? False
big matrix 999 x 1001: value-search steps = 30  bisect_right calls = 29970
all checks passed
```

The three prompt examples are correct. 2,000 seeded random odd-by-odd matrices with many duplicates agreed with the flatten-and-sort answer, and the result was always an entry.

**Edge cases:**
- 1 x 1: lo = hi, returns the value.
- Heavy duplicates: bisect_right counts all copies of mid, which is what the rank needs.
- Single row or single column: works the same.
- Negative values: fine, the range just starts lower.

**Follow-ups:**
- "Even r*c?" Take the average of the two middle ranks, found with two searches (need and need + 1).
- "Why bisect_right not bisect_left?" I need the count of entries <= v. bisect_left would count entries < v.
- "Heap alternative?" A k-way merge heap works but costs O(rc log r) time; Part 8 covers heaps.

**Common mistakes:**
- Using `bisect_left`.
- Using `need = r*c // 2` (zero-based index) against a count that is one-based.
- Using lo = 0 and hi = 10^9 blindly; fine, but the min/max of rows is tighter.

---

### Q38 ⭐ 🔴 K-th smallest pair distance. `nums` is a list of integers (2 <= len <= 10^4, values up to 10^6) and 1 <= k <= n*(n-1)/2. Consider the absolute difference |nums[i] - nums[j]| for every pair i < j; return the k-th smallest of these n*(n-1)/2 values (duplicates counted). Sort nums, binary search the distance d in [0, max - min], and count pairs with distance <= d in O(n) with two pointers; return the smallest d with count >= k. Give the O(n^2 log n) enumerate-and-sort reference and explain why the O(n^2) pair list is too big for n = 10^4. (A value-space binary search for a different counting problem is Part 1 Q28.) Example: [1,3,1], k=1 -> 0; [1,1,1], k=2 -> 0; [1,6,1], k=3 -> 5; [1,3,1], k=2 -> 2; [1,3,1], k=3 -> 2.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the answer (a distance), with an O(n) two-pointer count on the sorted array.

**Say this first (1 line):** "Sort, then binary search the distance d; for each d count pairs with difference <= d by two pointers in O(n); the answer is the smallest d with at least k pairs."

**Brute force:** Build all n(n-1)/2 absolute differences, sort, take index k - 1: O(n^2 log n) time, O(n^2) space. For n = 10^4 there are 49,995,000 pairs; at just 8 bytes per list slot that is about 399 MB before counting the int objects. Too big. It is my checker for small n.

**Optimal:**
- Sort `nums`. Distances between pairs are then differences of sorted values, and the set of pair distances is the same.
- `count_le(d)`: for each `right`, move `left` forward while `a[right] - a[left] > d`; add `right - left` (the partners to its left within d). Left never moves backward, so this is O(n).
- `count_le` is non-decreasing in d. Search d in [0, a[-1] - a[0]] for the smallest d with `count_le(d) >= k`.
- Why that d is an actual distance: count(d - 1) < k <= count(d), so at least one pair has distance exactly d.
- Duplicates count: [1, 1, 1] has three pairs of distance 0.

**Complexity:** Time O(n log n) for the sort plus O(n log(max - min)) for the search, about 20 to 30 counting passes. Space O(1) beyond the sorted copy.

**Dry run:** nums = [1, 3, 1], k = 2. Sorted [1, 1, 3], range [0, 2].
- mid = 1: right = 1 (value 1): left 0, adds 1. right = 2 (value 3): 3 - 1 > 1 and 3 - 1 > 1, left goes to 2, adds 0. Total 1 < 2, so lo = 2.
- lo = hi = 2. Answer 2. Check: distances 0, 2, 2; the second smallest is 2.

**Code:**
```python
import random
from itertools import combinations


def kth_pair_distance(nums, k):
    a = sorted(nums)
    n = len(a)

    def count_le(d):
        cnt, left = 0, 0
        for right in range(n):
            while a[right] - a[left] > d:
                left += 1
            cnt += right - left              # pairs (left..right-1, right) with distance <= d
        return cnt

    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_pair_distance_brute(nums, k):
    return sorted(abs(x - y) for x, y in combinations(nums, 2))[k - 1]


for nums, k, want in [([1, 3, 1], 1, 0), ([1, 1, 1], 2, 0), ([1, 6, 1], 3, 5), ([1, 3, 1], 2, 2), ([1, 3, 1], 3, 2)]:
    got = kth_pair_distance(nums, k)
    print(nums, "k =", k, "->", got, " brute:", kth_pair_distance_brute(nums, k))
    assert got == kth_pair_distance_brute(nums, k) == want

rng = random.Random(38)
cnt = 0
for _ in range(1500):
    n = rng.randint(2, 9)
    nums = [rng.randint(0, 12) for _ in range(n)]
    for k in range(1, n * (n - 1) // 2 + 1):
        assert kth_pair_distance(nums, k) == kth_pair_distance_brute(nums, k), (nums, k)
        cnt += 1
print("random (nums, k) cases checked:", cnt)

# size argument for n = 10**4
n = 10**4
pairs = n * (n - 1) // 2
print("pairs for n = 10**4:", pairs, " pointer slots alone at 8 bytes each: about", pairs * 8 // 10**6, "MB")
# runtime sanity on a big input (sandbox only): O(n log range), never builds pairs
big = [rng.randint(0, 10**6) for _ in range(n)]
v = kth_pair_distance(big, pairs // 2)
print("n = 10**4 median pair distance (sandbox run):", v)
# edge asserts
assert kth_pair_distance([5, 5], 1) == 0
assert kth_pair_distance([1, 100], 1) == 99
assert kth_pair_distance([0, 10**6], 1) == 10**6
assert kth_pair_distance([1, 2, 3, 4], 6) == 3
print("all checks passed")
```

**Output (my run):**
```text
[1, 3, 1] k = 1 -> 0  brute: 0
[1, 1, 1] k = 2 -> 0  brute: 0
[1, 6, 1] k = 3 -> 5  brute: 5
[1, 3, 1] k = 2 -> 2  brute: 2
[1, 3, 1] k = 3 -> 2  brute: 2
random (nums, k) cases checked: 22297
pairs for n = 10**4: 49995000  pointer slots alone at 8 bytes each: about 399 MB
n = 10**4 median pair distance (sandbox run): 293341
all checks passed
```

All five prompt examples match the brute force. The random check ran every k for 1,500 seeded small lists with many ties (22,297 cases). I also ran n = 10^4 in the sandbox: it finishes without building any pair list (sandbox-only, not a proof of big-O).

**Edge cases:**
- n = 2: one pair, distance |a - b|.
- All equal: every distance 0.
- k = 1: the minimum gap (often 0 with duplicates); k = n(n-1)/2: max - min.
- Unsorted input: sort a copy first.

**Follow-ups:**
- "Faster than O(n log range)?" Not easily; the heap approach (pop and push neighbours) is O(k log n), worse for big k.
- "Is the pair set the same after sorting?" Yes: the multiset of |x - y| does not depend on order.
- "Does the count use <= or <?" `<= d`; with `< d` the smallest-d rule changes.

**Common mistakes:**
- Forgetting to sort before the two-pointer count.
- Counting `right - left + 1` (includes the element itself).
- Resetting `left = 0` for every right (O(n^2)).
- Searching [1, max - min] and missing distance 0.

---

### Q39 ⭐ 🔴 K-th smallest number in a multiplication table. The table has m rows and n columns where the entry in row i and column j (1-indexed) is i * j (1 <= m, n <= 3*10^4); k is 1-based with 1 <= k <= m*n and counts duplicates. Return the k-th smallest entry without building the table. Binary search the VALUE v in [1, m*n] with count(v) = sum over rows i of min(n, v // i), and return the smallest v with count(v) >= k. Explain why that v is always an entry of the table, and why this is a search over values (the table is not a sorted list you can index). Example: m=3, n=3, k=5 -> 3; m=2, n=3, k=6 -> 6; m=1, n=5, k=4 -> 4; m=3, n=3, k=9 -> 9; m=3, n=3, k=1 -> 1.
**Asked at:** Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the value, with a counting predicate: how many table entries are <= v.

**Say this first (1 line):** "The table is not a list I can index, so I binary search the value v and count entries <= v as the sum over rows of min(n, v // i); the answer is the smallest v with count >= k."

**Brute force:** Build the m x n table, sort, take index k - 1: O(mn log(mn)) time, O(mn) space. With m = n = 3*10^4 that is 9*10^8 entries. My checker uses it on small tables only.

**Optimal:**
- Row i holds i, 2i, ..., ni. Entries <= v in that row: `min(n, v // i)`.
- `count(v) = sum for i in 1..m of min(n, v // i)`. Rows with i > v contribute 0, so I loop to `min(m, v)`.
- count is non-decreasing in v. Search [1, m*n] for the smallest v with `count(v) >= k`.
- Why v is an entry: count(v - 1) < k <= count(v), so the count increases at v, which only happens if some i * j equals v.
- Why a value search: the table in row-major order is [1, 2, 3, 2, 4, 6, 3, 6, 9] for 3 x 3, which is not sorted, and sorted values can repeat; there is no array to bisect. The values are ordered, though, so I search them.

**Complexity:** Time O(m log(mn)): each count is O(m), and the value search takes about log2(9*10^8), roughly 30 steps. Space O(1). (Swap the roles to loop over the smaller of m and n.)

**Dry run:** m = 3, n = 3, k = 5, lo = 1, hi = 9.
| lo | hi | mid | count | action |
|---|---|---|---|---|
| 1 | 9 | 5 | 3 + 2 + 1 = 6 >= 5 | hi = 5 |
| 1 | 5 | 3 | 3 + 1 + 1 = 5 >= 5 | hi = 3 |
| 1 | 3 | 2 | 2 + 1 + 0 = 3 < 5 | lo = 3 |

Answer 3. Sorted table: 1, 2, 2, 3, 3, 4, 6, 6, 9, so the 5th is 3.

**Code:**
```python
def kth_table(m, n, k):
    def count_le(v):
        return sum(min(n, v // i) for i in range(1, min(m, v) + 1))   # rows beyond v contribute 0
    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_table_brute(m, n, k):
    return sorted(i * j for i in range(1, m + 1) for j in range(1, n + 1))[k - 1]


for m, n, k, want in [(3, 3, 5, 3), (2, 3, 6, 6), (1, 5, 4, 4), (3, 3, 9, 9), (3, 3, 1, 1)]:
    got = kth_table(m, n, k)
    print("m =", m, "n =", n, "k =", k, "->", got, " brute:", kth_table_brute(m, n, k))
    assert got == kth_table_brute(m, n, k) == want

# exhaustive: all m, n up to 9 and every k
cnt = 0
for m in range(1, 10):
    for n in range(1, 10):
        table = {i * j for i in range(1, m + 1) for j in range(1, n + 1)}
        for k in range(1, m * n + 1):
            v = kth_table(m, n, k)
            assert v == kth_table_brute(m, n, k), (m, n, k)
            assert v in table                          # the answer is always an entry
            cnt += 1
print("exhaustive (m, n, k) cases checked:", cnt)

# the table is not a sorted list: row-major reading of the 3 x 3 table
print("row-major 3 x 3:", [i * j for i in range(1, 4) for j in range(1, 4)])
# big sizes: no table is built
v = kth_table(3 * 10**4, 3 * 10**4, 3 * 10**4 * 3 * 10**4)
assert v == 9 * 10**8
v = kth_table(3 * 10**4, 3 * 10**4, 4 * 10**8)
print("m = n = 3*10**4, k = 4*10**8 ->", v)
# edge asserts
assert kth_table(1, 1, 1) == 1
assert kth_table(1, 7, 7) == 7 and kth_table(7, 1, 1) == 1
assert kth_table(30000, 1, 30000) == 30000
print("all checks passed")
```

**Output (my run):**
```text
m = 3 n = 3 k = 5 -> 3  brute: 3
m = 2 n = 3 k = 6 -> 6  brute: 6
m = 1 n = 5 k = 4 -> 4  brute: 4
m = 3 n = 3 k = 9 -> 9  brute: 9
m = 3 n = 3 k = 1 -> 1  brute: 1
exhaustive (m, n, k) cases checked: 2025
row-major 3 x 3: [1, 2, 3, 2, 4, 6, 3, 6, 9]
m = n = 3*10**4, k = 4*10**8 -> 139742112
all checks passed
```

All five prompt examples are right. I tested every m, n in 1..9 and every k (2,025 cases): the result matched brute force and was always in the table. The m = n = 3*10^4 runs build no table.

**Edge cases:**
- m = 1 or n = 1: a single row or column, answer is k.
- k = 1: 1. k = m*n: m*n.
- Repeated values (6 appears twice in 3 x 3): handled since count includes duplicates.
- Large m and n: the count loop is the only cost.

**Follow-ups:**
- "Can I count faster?" Yes, group rows by v // i blocks in O(sqrt v), but O(m) is already fine here.
- "Same idea elsewhere?" Kth smallest in a sorted matrix (Part 8 for the heap version) and pair distance (Q38).
- "Why min(n, v // i)?" Row i stops at column n.

**Common mistakes:**
- Looping rows past v (harmless but wasteful) or forgetting the `min(n, ...)` cap.
- Returning `lo - 1` or `hi` wrongly with a mixed template.
- Building the table.

---

### Q40 ⭐ 🔴 Minimise the maximum gap after adding k gas stations (real-valued answer). `stations` is a sorted list of distinct integer positions along a line (2 <= len <= 2000) and k >= 0 new stations may be placed anywhere (real positions allowed). Return the smallest achievable value of the largest distance between adjacent stations, within 10^-6. Binary search the gap d with the predicate 'sum over gaps of ceil(gap / d) - 1 <= k'. Explain why the predicate is monotone in d, why a fixed iteration count beats an epsilon loop here, and how the exact answer relates to some gap / (c + 1) for an integer c. Example: [1,2,3,4,5,6,7,8,9,10], k=9 -> 0.5; [23,24,36,39,46,56,57,65,84,98], k=1 -> 14.0; [0,10], k=0 -> 10.0; [0,10], k=1 -> 5.0.
**Asked at:** Community binary-search master lists (a LeetCode discuss 'binary search master list' post, Coding Blocks forum thread grouping Allocate Books, Aggressive Cows and Painter's Partition as one pattern; snippets only, not opened; list content, not company reports) | Binary-search pattern guides (techinterview.org binary-search patterns, advanced patterns and rotated-array/search-on-answer pages, DEV Community binary-search patterns series; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on a real answer d with the predicate "stations needed with max gap <= d is at most k".

**Say this first (1 line):** "A gap of length g needs ceil(g / d) - 1 new stations to get every piece <= d; if the total is <= k, d is achievable, so I shrink d, with a fixed 100 halvings."

**Brute force:** Greedy with a heap: always put one more station into the gap with the largest current piece (gap / (c + 1)). That is O(k log n), which is slow for huge k but exact. For small k I also try every way to split k stations over the gaps with exact fractions, which is my checker.

**Optimal:**
- `need(d) = sum(ceil((b - a) / d) - 1 for each adjacent pair)`.
- Monotone: a larger d never needs more stations, since ceil(g / d) is non-increasing in d. I checked `need` on 200 seeded lists over d = 0.25..49.75.
- Range: `lo = 0`, `hi = largest gap` (with d = hi, `need = 0 <= k`). Loop 100 times: `mid`; if `need(mid) <= k` then `hi = mid` else `lo = mid`. Return `hi`.
- Why a fixed count: the epsilon loop works with a sane eps (eps = 1e-6 took 24 loops for [0, 10], k = 1), but with a too-small eps it can never end, like Q31. On the 14.0 example, eps = 1e-17 ran into my 10^6-loop cap. A fixed count never hangs. I would say it plainly: a fixed count does not make the answer more correct, it just guarantees termination.
- Exact answer: the optimum is always some gap / (c + 1) for an integer c (one gap is the bottleneck and holds c extra stations, split evenly). In 600 seeded cases the exact optimum was always of that form, so a final snap to the nearest such value is possible.
- Float risk: ceil of a float quotient near an integer can flip, but the effect is on the order of the tolerance, and my cross-check found the worst error about 1.1e-16.

**Complexity:** Time O(n * iterations) = O(100 n), about 2*10^5 operations for n = 2000. Space O(1). The heap version is O(k log n).

**Dry run:** stations [0, 10], k = 1. lo = 0, hi = 10.
| mid | need = ceil(10 / mid) - 1 | action |
|---|---|---|
| 5 | 1 <= 1 | hi = 5 |
| 2.5 | 3 > 1 | lo = 2.5 |
| 3.75 | 2 > 1 | lo = 3.75 |
| 4.375 | 2 > 1 | lo = 4.375 |

It converges to 5.0 from above, exactly 10 / (1 + 1).

**Code:**
```python
import math
import random
from fractions import Fraction
from itertools import product


def need(stations, d):
    return sum(math.ceil((b - a) / d) - 1 for a, b in zip(stations, stations[1:]))


def min_max_gap(stations, k, iters=100):
    lo, hi = 0.0, float(max(b - a for a, b in zip(stations, stations[1:])))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if need(stations, mid) <= k:
            hi = mid                        # mid is enough, try smaller
        else:
            lo = mid
    return hi


def min_max_gap_eps(stations, k, eps, cap=10**6):
    lo, hi = 0.0, float(max(b - a for a, b in zip(stations, stations[1:])))
    loops = 0
    while hi - lo > eps and loops < cap:
        mid = (lo + hi) / 2
        if need(stations, mid) <= k:
            hi = mid
        else:
            lo = mid
        loops += 1
    return hi, loops


def min_max_gap_exact(stations, k):
    # brute force: try every way to split k stations over the gaps (extra stations in a gap -> gap/(c+1)); exact Fractions
    gaps = [b - a for a, b in zip(stations, stations[1:])]
    best = None
    def go(i, left, cur):
        nonlocal best
        if i == len(gaps) - 1:
            v = max(cur, Fraction(gaps[i], left + 1))
            if best is None or v < best:
                best = v
            return
        for c in range(left + 1):
            go(i + 1, left - c, max(cur, Fraction(gaps[i], c + 1)))
    go(0, k, Fraction(0))
    return best


for st, k, want in [(list(range(1, 11)), 9, 0.5), ([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 14.0), ([0, 10], 0, 10.0), ([0, 10], 1, 5.0)]:
    got = min_max_gap(st, k)
    print(st, "k =", k, "->", round(got, 7))
    assert abs(got - want) <= 1e-6
print("eps=1e-6 loop on [0,10], k=1:", min_max_gap_eps([0, 10], 1, 1e-6))
print("eps=1e-17 loop on the 14.0 example, capped at 10**6:", min_max_gap_eps([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 1e-17)[1], "loops")
assert min_max_gap_eps([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1, 1e-17)[1] == 10**6

# seeded cross-check against exact brute force, and the 'gap/(c+1)' claim
rng = random.Random(40)
hit = 0
worst = 0.0
for _ in range(600):
    n = rng.randint(2, 5)
    st = sorted(rng.sample(range(0, 40), n))
    k = rng.randint(0, 5)
    ex = min_max_gap_exact(st, k)
    got = min_max_gap(st, k)
    worst = max(worst, abs(got - float(ex)))
    assert abs(got - float(ex)) <= 1e-6, (st, k)
    gaps = [b - a for a, b in zip(st, st[1:])]
    assert any(ex == Fraction(g, c + 1) for g in gaps for c in range(k + 1)), (st, k)
    hit += 1
print("600 seeded cases: worst |binary search - exact| =", worst, "; exact optimum was always some gap/(c+1)")

# monotone predicate: need() never increases as d grows
for _ in range(200):
    st = sorted(rng.sample(range(0, 60), rng.randint(2, 7)))
    seq = [need(st, d / 4) for d in range(1, 200)]
    assert all(x >= y for x, y in zip(seq, seq[1:]))
print("need(d) non-increasing in d on 200 seeded station lists")
# edge asserts
assert abs(min_max_gap([0, 1], 0) - 1.0) <= 1e-6
assert abs(min_max_gap([0, 1, 2], 100) - 1 / 51) <= 1e-6        # 100 stations over 2 equal gaps: 50 each, gap 1/51
assert abs(min_max_gap([0, 7], 3) - 1.75) <= 1e-6
assert abs(min_max_gap([0, 10, 11], 1) - 5.0) <= 1e-6
print("all checks passed")
```

**Output (my run):**
```text
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] k = 9 -> 0.5
[23, 24, 36, 39, 46, 56, 57, 65, 84, 98] k = 1 -> 14.0
[0, 10] k = 0 -> 10.0
[0, 10] k = 1 -> 5.0
eps=1e-6 loop on [0,10], k=1: (5.0, 24)
eps=1e-17 loop on the 14.0 example, capped at 10**6: 1000000 loops
600 seeded cases: worst |binary search - exact| = 1.1102230246251565e-16 ; exact optimum was always some gap/(c+1)
need(d) non-increasing in d on 200 seeded station lists
all checks passed
```

All four prompt examples are right (0.5, 14.0, 10.0, 5.0). For 600 seeded small cases the binary search agreed with exact-fraction brute force to within 1.1e-16.

**Edge cases:**
- k = 0: answer is the largest gap (`need(d) <= 0` only when d >= every gap).
- Two stations only: one gap g, answer g / (k + 1).
- Huge k: the answer approaches 0 (never negative or zero, since `mid > 0`).
- Equal gaps: stations are spread evenly across them.

**Follow-ups:**
- "Why not search integers?" New stations may sit at real positions, so the answer can be fractional (0.5 in the first example).
- "Can I get the exact value?" Candidates are gap / (c + 1); test the smallest feasible one with fractions.
- "How is this like Allocate Books / ship packages?" Same minimise-the-maximum shape, but the answer is real, so I loop a fixed number of times instead of stopping at lo == hi.

**Common mistakes:**
- `ceil(g / d)` instead of `ceil(g / d) - 1` (counts pieces, not stations).
- Initialising `lo` to the smallest gap (wrong: the answer can be below it).
- Looping `while hi - lo > 1e-6` with a smaller epsilon and hanging.
- Putting stations into only the largest gap.
