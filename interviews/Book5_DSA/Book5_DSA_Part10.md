# Book 5 — Part 10: Dynamic Programming I (1D DP and Knapsack)

**Topic:** Python DSA for product-company interviews: how to define a DP state and derive the transition, base cases, counting versus optimising DPs, memoisation versus tabulation versus space optimisation, climbing stairs and Fibonacci (call counts of plain recursion, a cache and a bottom-up loop), min cost climbing stairs, house robber (linear and circular), maximum subarray (Kadane, with indices and a tie rule, and the circular variant), maximum product subarray, best time to buy and sell stock as a state machine (one transaction, cooldown, at most k transactions), decode ways, coin change (minimum coins, number of combinations, and recovering the coins), perfect squares, word break, longest increasing subsequence (O(n^2) table, O(n log n) with bisect and the patience-sorting argument, recovering one, the non-decreasing variant with bisect_right, counting all of them, Russian doll envelopes), 0/1 knapsack (1D table and why the capacity loop runs downward, recovering the items), subset sum with a table and a big-int bitset, partition equal subset sum, target sum, last stone weight II, unbounded knapsack, combination sum IV (order matters versus not), ones and zeroes (a two-capacity knapsack at the edge of 2D DP), delete and earn, jump game as DP versus greedy, paint fence and dice-roll counting with a modulus, minimum cost for tickets, and Python specifics (recursion limit versus bottom-up, `functools.cache` and `lru_cache` with mutable arguments and `cache_clear`, the `[[0]*n]*m` aliasing trap)

**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 13, ⭐⭐ 17, ⭐ 10)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns one-dimensional DP and knapsack-style tables. Part 5 owns binary search (the bisect semantics used by the patience-sorting LIS are cross-referenced as 'Part 5 Q11'), Part 7 owns trees (tree DP stays there: House Robber III is 'Part 7 Q45' and binary tree cameras 'Part 7 Q50'; the deep-recursion limit on skewed trees is 'Part 7 Q35'; nothing from them is duplicated here, and Q5 only points to Part 7 Q45), Part 8 owns greedy (jump game and jump game II are 'Part 8 Q12' and 'Part 8 Q13', the greedy-fails-for-coins counter-example is 'Part 8 Q33' and the heaviest-two stone smashing is 'Part 8 Q18'; here the same problems are the DP side of the greedy-versus-DP contrast), Part 4 owns monotonic stacks and deques (a DP over jumps of at most k with a monotonic deque is 'Part 4 Q35'), Part 9 owns graphs (shortest paths on a DAG as a DP are handed off by part number only), Part 11 owns DP II (two-dimensional grids, string DPs such as edit distance and longest common subsequence, interval DP and palindromic subsequences; this part has only the two-capacity knapsack of Q39, 'ones and zeroes', at the concept edge, and the aliasing trap of Q31, whose 2D table appears everywhere in Part 11), Part 12 owns backtracking (enumerating the combinations, orderings or paths instead of counting them: the counting questions here, Q10, Q19, Q21 and Q28, return counts only), and Part 13 owns math and prefix sums. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each Part N Qn reference was checked against its heading by build.py, and every within-part reference (Q6, Q10 and so on) was checked by build.py against the final question numbers. Conventions: every question states its constraints, whether an answer is returned exactly (Python integers do not overflow) or modulo 10^9 + 7, and its return value for degenerate input (an empty list, a zero target or amount, an impossible case returns -1 or null as the prompt says). Every prompt asks the answer to include a table walk-through on the first example and a seeded random cross-check of the optimal solution against a brute-force or plain-recursion oracle on small inputs. Recursion: every prompt whose size passes 1000 for a natural top-down recursion says a bottom-up solution is required, because a memoised recursion nests about n deep and CPython's default recursion limit is 1000 (demonstrated by running code: memoised recursions at the quoted sizes for climbing stairs, house robber, coin change, perfect squares, combination sum IV, coin change II, paint fence and the cooldown stock problem each raise RecursionError at the default limit, and a 3-step stair recursion succeeds at n = 500 and fails at n = 2000), while no prompt relies on raising the limit and no claim is made about the C stack. Questions whose answer would not be unique say exactly what is accepted: reconstruction questions fix an explicit tie rule (maximum subarray position: smallest start, then smallest end; coin change recovery: the lexicographically smallest list among minimum-size multisets; LIS recovery and knapsack item recovery: the lexicographically smallest list of indices), and the reachable set in the jump game, the `tails` array of patience sorting and the call counts of Q14 are defined step by step so their outputs are unique. Each question is a frozen, self-contained prompt with a precise statement, constraints, input format and at least one input/output example; every example below is rendered from the same data that scratch/B5P10_wavea/check_examples.py executes (python3 -I) against reference solutions, so no example can differ from what was run. Cross-checks: each reference against an independent brute force or plain recursion on 400 seeded random small inputs per question (15612 in all), for example subset enumeration for house robber, partition, knapsack, subset sum, ones and zeroes and delete and earn; all 2^n sign assignments for target sum; plain recursion without a memo for climbing stairs, coin change, perfect squares, unbounded knapsack and tickets; all subsequences for the LIS family (length, smallest last value per length, count, lexicographic recovery, non-decreasing variant); all colourings for paint fence; all outcomes for dice rolls; all multisets for coin recovery; every smash order for last stone weight II; and counted-call and dict-memo models for the cache questions. Claims tested by running code: the maximum subarray tie rule agrees with the O(n^2) enumeration on every list of length up to 6 with values in -2..2 (19530 lists); the reachable set in the jump game is a prefix of the indices on all 5460 lists of length up to 6 with values 0..3; the circular-array maximum equals the circular enumeration on every list of length up to 5 with values -3..3 and the naive formula max(Kadane, total - minimum subarray) is wrong on some of them; the upward-loop 0/1 knapsack equals the unbounded knapsack on 1000 random inputs and differs from the true 0/1 answer on some of them; the bitset and the boolean table agree for subset sum; target sum with z zeros is 2^z times the count without them; in combination sum IV the swapped loop order yields the unordered count and the ordered count is never smaller; the plain parent-pointer rebuild of coin change differs from the lexicographic tie rule on some inputs; bisect_left used for the non-decreasing LIS computes the strict length and is wrong on some inputs, the number of greedy patience piles equals the LIS length and `tails` is not itself an LIS; sorting equal widths by ascending height is wrong for Russian dolls on some inputs; the at-most-k stock table with k capped at n // 2 equals the full table; the fence count modulo 10^9 + 7 equals the exact big-integer count modulo; `[[0]*n]*m` has exactly one distinct row object while the comprehension has m; a list argument to a `functools.cache` function raises TypeError (unhashable type: 'list'); naive Fibonacci calls equal 2 fib(n + 1) - 1 and memoised calls equal 2n - 1 for n >= 1. Both branches of every boolean or sentinel answer occurred in the random tests, and all solutions run at the stated maximum sizes (10^5-element lists, 10^4 amounts, 200 items with 10^4 targets) in a fraction of a second to a few seconds in this sandbox (sandbox timing, not a proof of big-O). Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part10_sources.md). Searches returned DP pattern guides (techinterview.org, DesignGurus, IGotAnOffer, labuladong, system.design), candidate-reported Flipkart rounds that mention coin change, a longest decreasing subsequence assessment, a 0-1 knapsack with a space-optimisation follow-up and an unbounded-knapsack-like question (LeetCode Discuss, Naukri Code360, GeeksforGeeks and Taro, self-reported, spanning 2017 to 2025 and mixing intern and SDE-1 roles), and stock state-machine write-ups; nothing was found tying the other items to a named company, so 'Asked at' tags name source types, not verified company reports. Items such as delete and earn, last stone weight II, ones and zeroes, Russian doll envelopes, minimum cost for tickets and number of longest increasing subsequences come from editor knowledge of standard lists. The bounds and uniqueness claims above were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

### Q1 ⭐⭐⭐ 🟢 Climbing stairs, with a modulus. You climb a staircase of `n` steps (0 <= n <= 10^5) taking 1 or 2 steps at a time. Return the number of distinct ways to reach the top, modulo 10^9 + 7 (n = 0 has exactly 1 way: do nothing). State the recurrence, the base cases and why it is the Fibonacci sequence shifted by one. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). Show the O(1)-space version. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without memo (exponential, n <= 20) on small inputs. Example: n=0 -> 1; n=1 -> 1; n=5 -> 8; n=45 -> 836311896; n=100000 -> 967618232.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D counting DP. The state is one number (the step), the transition looks back a fixed distance. It is Fibonacci in disguise.

**Say this first (1 line):** "Let dp[i] be the number of ways to stand on step i; the last move was a 1 or a 2, so dp[i] = dp[i-1] + dp[i-2] with dp[0] = dp[1] = 1, bottom-up in O(n) time and O(1) space, mod 10^9 + 7."

**Brute force:** Plain recursion `ways(n) = ways(n-1) + ways(n-2)` with no memo. It makes exactly 2 * F(n+1) - 1 calls (177 for n = 10, 21,891 for n = 20), so it is exponential, about 1.6^n. Used in the code as the oracle for n <= 20.

**Optimal:**
- State: `dp[i]` = number of distinct move sequences that land exactly on step i.
- Transition: the final move was a 1-step (from i-1) or a 2-step (from i-2). These cases are disjoint and cover everything, so `dp[i] = dp[i-1] + dp[i-2]` (i >= 2).
- Base cases: `dp[0] = 1` (the empty sequence, "do nothing") and `dp[1] = 1`. Treating dp[0] = 1 is what makes n = 0 return 1 and makes dp[2] = 2 come out right.
- Why Fibonacci shifted by one: with F(1) = F(2) = 1, we have dp[0] = F(1), dp[1] = F(2), and the same recurrence, so `dp[n] = F(n+1)`. Checked in the code for n in 0..299.
- Take the modulus on every addition so numbers stay small. (Python ints would not overflow, but a 10^5-step Fibonacci has about 21,000 digits, so the loop would slow down.)
- Space: dp[i] reads only the previous two values, so keep two variables.
- Top-down version: `@cache def f(i): return 1 if i <= 1 else f(i-1) + f(i-2)`. It is correct, but the first call `f(n)` nests n frames deep. CPython's default recursion limit is 1000, so n = 5000 and n = 10^5 raise `RecursionError`. The fix is bottom-up (a loop), not `sys.setrecursionlimit`.

**Complexity:** Time O(n), space O(1) (the table version is O(n)). Bonus: fast doubling gives O(log n) arithmetic steps, with recursion depth only log2(n), so it needs no loop; it is in the code and checked against the loop.

**Dry run:** `n = 5`, table filled left to right.

| i | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| dp[i] | 1 | 1 | 2 | 3 | 5 | 8 |
| from | base | base | 1+1 | 2+1 | 3+2 | 5+3 |

Answer dp[5] = 8, matching the prompt. Each step reads only the two cells to its left, which is why two variables are enough.

**Code:**
```python
import random
from functools import cache

random.seed(101)
MOD = 10**9 + 7

def ways_bottom_up(n):
    """dp[i] = ways to reach step i. dp[0]=1, dp[1]=1, dp[i]=dp[i-1]+dp[i-2]. O(1) space: two variables."""
    a, b = 1, 1                      # a = dp[i-1], b = dp[i] starting at i = 1  (dp[0], dp[1])
    if n == 0:
        return 1
    for _ in range(n - 1):           # advance from dp[1] to dp[n]
        a, b = b, (a + b) % MOD
    return b

def ways_table(n):
    """Same recurrence with the full table (for the walk-through)."""
    dp = [0] * (n + 1)
    dp[0] = 1
    if n >= 1:
        dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = (dp[i - 1] + dp[i - 2]) % MOD
    return dp

def ways_memo(n):
    """Top-down with a cache: correct, but depth n."""
    @cache
    def f(i):
        if i <= 1:
            return 1
        return (f(i - 1) + f(i - 2)) % MOD
    return f(n)

def ways_plain(n):
    """Oracle: plain recursion, no memo, exponential. Returns the exact (unreduced) count."""
    if n <= 1:
        return 1
    return ways_plain(n - 1) + ways_plain(n - 2)

def fib(n):                          # F(1)=F(2)=1, exact, iterative
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def ways_doubling(n):
    """Extra: fast doubling, O(log n). ways(n) = F(n+1)."""
    def fd(k):                       # returns (F(k), F(k+1)) mod MOD
        if k == 0:
            return 0, 1
        a, b = fd(k >> 1)
        c = a * ((2 * b - a) % MOD) % MOD
        d = (a * a + b * b) % MOD
        return (d, (c + d) % MOD) if k & 1 else (c, d)
    return fd(n + 1)[0]              # recursion depth is only log2(n)

# --- prompt examples
for n, want in [(0, 1), (1, 1), (5, 8), (45, 836311896), (100000, 967618232)]:
    assert ways_bottom_up(n) == want, (n, ways_bottom_up(n))
    assert ways_doubling(n) == want
print('5 prompt examples ok (n = 0, 1, 5, 45, 100000)')

# --- table walk-through for n = 5
print('table n=5: i  ', list(range(6)))
print('           dp ', ways_table(5))

# --- oracle cross-check: every n in 0..20, plus seeded random draws
for n in range(21):
    assert ways_bottom_up(n) == ways_plain(n) % MOD == ways_memo(n) == ways_table(n)[n]
for _ in range(300):
    n = random.randint(0, 20)
    assert ways_bottom_up(n) == ways_plain(n) % MOD
print('cross-check vs plain recursion: all n in 0..20 and 300 seeded draws agree')

# --- shifted Fibonacci claim, exact integers
for n in range(0, 300):
    assert ways_bottom_up(n) == fib(n + 1) % MOD
assert fib(46) == 1836311903 and 1836311903 % MOD == 836311896   # n=45 example, reduced
print('ways(n) == Fibonacci(n+1) for n in 0..299 (F(1)=F(2)=1); n=45: F(46) = 1836311903 -> mod = 836311896')

# --- fast doubling agrees with the loop on seeded large n
for _ in range(50):
    n = random.randint(0, 10**5)
    assert ways_doubling(n) == ways_bottom_up(n)
print('fast doubling == linear loop on 50 seeded n up to 10^5')

# --- number of calls made by the plain recursion (why it is exponential)
calls = [0]
def counted(n):
    calls[0] += 1
    return 1 if n <= 1 else counted(n - 1) + counted(n - 2)
for n in (10, 20, 25):
    calls[0] = 0; counted(n)
    print(f'plain recursion n={n}: {calls[0]} calls (2*F(n+1) - 1 = {2 * fib(n + 1) - 1})')
    assert calls[0] == 2 * fib(n + 1) - 1

# --- recursion limit: memoised recursion at large n fails under the default limit (1000)
import sys
print('default recursion limit:', sys.getrecursionlimit())
for n in (500, 5000, 100000):
    try:
        ways_memo(n)
        print(f'memoised n={n}: ok')
    except RecursionError:
        print(f'memoised n={n}: RecursionError')
print('bottom-up n=100000 ->', ways_bottom_up(100000))
```

**Output (my run):**
```
5 prompt examples ok (n = 0, 1, 5, 45, 100000)
table n=5: i   [0, 1, 2, 3, 4, 5]
           dp  [1, 1, 2, 3, 5, 8]
cross-check vs plain recursion: all n in 0..20 and 300 seeded draws agree
ways(n) == Fibonacci(n+1) for n in 0..299 (F(1)=F(2)=1); n=45: F(46) = 1836311903 -> mod = 836311896
fast doubling == linear loop on 50 seeded n up to 10^5
plain recursion n=10: 177 calls (2*F(n+1) - 1 = 177)
plain recursion n=20: 21891 calls (2*F(n+1) - 1 = 21891)
plain recursion n=25: 242785 calls (2*F(n+1) - 1 = 242785)
default recursion limit: 1000
memoised n=500: ok
memoised n=5000: RecursionError
memoised n=100000: RecursionError
bottom-up n=100000 -> 967618232
```

**Edge cases:**
- `n = 0` returns 1 (the empty move sequence), `n = 1` returns 1.
- The loop `range(n - 1)` runs zero times for n = 1; n = 0 is handled before it.
- n = 10^5: bottom-up takes about 10^5 additions; the memoised version dies with RecursionError at default settings.
- The mod is applied inside the loop; applying it only at the end would give the same answer but with huge integers.

**Follow-ups:**
- Steps of size 1, 2 or 3? `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`; same loop, three variables.
- Very large n (10^18)? Matrix power or fast doubling, O(log n).
- Some steps broken? Set `dp[i] = 0` for broken steps and keep the same recurrence.

**Common mistakes:**
- `dp[0] = 0`, which makes everything come out as zero or shifted.
- Forgetting the modulus, or taking it only at the end.
- Memoised recursion for n = 10^5 and getting RecursionError; or "fixing" it with `setrecursionlimit` and risking a C-stack crash.
- Off by one in the loop count, returning dp[n-1] or dp[n+1].

### Q2 ⭐⭐⭐ 🟢 Min cost climbing stairs. `cost[i]` is the price of standing on step i; `cost` has 2 <= len <= 10^5 entries with 0 <= cost[i] <= 999. You may start on step 0 or step 1 for free, pay `cost[i]` each time you leave step i, and move up 1 or 2 steps per move. The top is the position len(cost), one past the last step. Return the minimum total price to reach the top. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a top-down recursion that asks 'cheapest cost to finish from step i' (a different direction from your table; n <= 15) on small inputs. Example: cost=[10, 15, 20] -> 15; cost=[1, 100, 1, 1, 1, 100, 1, 1, 100, 1] -> 6; cost=[0, 0] -> 0; cost=[5, 1] -> 1.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D optimising DP (min), look back one or two cells. Same skeleton as climbing stairs (Q1) with `min` and a cost instead of `+` and a count.

**Say this first (1 line):** "dp[i] is the cheapest price to be standing at position i; I arrive from i-1 or i-2 and pay the cost of the step I left, so dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]) with dp[0] = dp[1] = 0, answer dp[n]. O(n) time, O(1) space."

**Brute force:** Recursion from the other direction: `f(i)` = cheapest cost to finish from step i, `f(i) = cost[i] + min(f(i+1), f(i+2))`, `f(i) = 0` for i >= n, answer `min(f(0), f(1))`. No memo it is exponential; the cached version is O(n) but recurses n deep.

**Optimal:**
- State: `dp[i]` = minimum total price paid to reach position i, for i = 0..n. Position n is the top, one past the last step.
- Why the cost index shifts: you pay `cost[i]` when you leave step i. So reaching i from i-1 costs `cost[i-1]` and from i-2 costs `cost[i-2]`.
- Base cases: `dp[0] = dp[1] = 0` because you may start on either step for free.
- Transition: `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])` for i = 2..n. Answer `dp[n]`.
- Invariant: after iteration i, `dp[i]` is the true minimum, because any path to i has a last move from i-1 or i-2, and the best prefix to each is already stored.
- Space: two variables. The bottom-up loop has no recursion, so n = 10^5 is fine; a memoised recursion nests n frames and raises `RecursionError` at the default limit of 1000 (shown in the code for the forward version).

**Complexity:** Time O(n), space O(1) (O(n) for the table). The forward recursion with no memo is O(2^n).

**Dry run:** `cost = [10, 15, 20]`, positions 0..3.

| i | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| dp[i] | 0 | 0 | 10 | 15 |
| how | free start | free start | min(0 + 15, 0 + 10) = 10 | min(10 + 20, 0 + 15) = 15 |

Answer 15: start on step 1, pay 15, jump over step 2 to the top.

**Code:**
```python
import random
import sys
from functools import cache

random.seed(102)

def min_cost(cost):
    """dp[i] = cheapest price to stand on position i (0..n). dp[0] = dp[1] = 0 (free start).
    dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]). Two variables."""
    a, b = 0, 0                                  # dp[i-2], dp[i-1] for i = 2
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b                                     # dp[n]  (n >= 2 guaranteed)

def min_cost_table(cost):
    n = len(cost)
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    return dp

def min_cost_forward_memo(cost):
    """Top-down, other direction: f(i) = cheapest cost to finish from step i (about to pay cost[i])."""
    n = len(cost)
    @cache
    def f(i):
        if i >= n:
            return 0
        return cost[i] + min(f(i + 1), f(i + 2))
    return min(f(0), f(1))

def min_cost_oracle(cost):
    """Same as above, no memo, n <= 15."""
    n = len(cost)
    def f(i):
        if i >= n:
            return 0
        return cost[i] + min(f(i + 1), f(i + 2))
    return min(f(0), f(1))

for c, want in [([10, 15, 20], 15), ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6), ([0, 0], 0), ([5, 1], 1)]:
    assert min_cost(c) == min_cost_oracle(c) == min_cost_forward_memo(c) == want
print('4 prompt examples ok')

c = [10, 15, 20]
print('walk-through cost =', c, ' positions 0..3')
print('dp =', min_cost_table(c))

for _ in range(500):
    n = random.randint(2, 15)
    c = [random.randint(0, 999) for _ in range(n)]
    assert min_cost(c) == min_cost_oracle(c) == min_cost_table(c)[-1], c
print('500 seeded random lists (len 2..15, values 0..999): bottom-up == forward recursion')
# exhaustive over small lists
import itertools
cnt = 0
for n in range(2, 7):
    for c in itertools.product(range(4), repeat=n):
        assert min_cost(list(c)) == min_cost_oracle(list(c)); cnt += 1
print('exhaustive, len 2..6 values 0..3:', cnt, 'lists ok')

# the claim "start on step 0 or 1 for free": dp[0]=dp[1]=0, answer dp[n]; equals min over the two forward starts
big = [random.randint(0, 999) for _ in range(10**5)]
print('n = 10^5 bottom-up ->', min_cost(big))
try:
    min_cost_forward_memo(big)
    print('forward memo at 10^5: ok')
except RecursionError:
    print('forward memo at 10^5: RecursionError (default limit', sys.getrecursionlimit(), ')')
```

**Output (my run):**
```
4 prompt examples ok
walk-through cost = [10, 15, 20]  positions 0..3
dp = [0, 0, 10, 15]
500 seeded random lists (len 2..15, values 0..999): bottom-up == forward recursion
exhaustive, len 2..6 values 0..3: 5456 lists ok
n = 10^5 bottom-up -> 20600098
forward memo at 10^5: RecursionError (default limit 1000 )
```

**Edge cases:**
- `[0, 0]` returns 0; `[5, 1]` returns 1 (start on step 1, pay 1).
- len = 2 means the loop runs once: the answer is `min(cost[1], cost[0])`.
- All costs zero returns 0.
- Returning `dp[n-1]` (the last step) instead of `dp[n]` (the top) is the classic off by one.

**Follow-ups:**
- Print the path? Store the parent of each i (which of the two moves won) and walk back from n.
- Allow jumps of 1, 2 or 3? Add a third term; the loop is unchanged in shape.
- Why not greedy "always the cheaper next step"? It can pay a cheap step now and be forced into a big one; `[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]` needs the skips planned (answer 6).

**Common mistakes:**
- Adding `cost[i]` instead of `cost[i-1]` and `cost[i-2]` (pay on leaving, not on arriving).
- Starting with `dp[0] = cost[0]`, which charges for a step you may start on for free.
- Answering `min(dp[n-1], dp[n-2])` on a table that already includes the cost of leaving, double counting.
- Deep memoised recursion at n = 10^5.

### Q3 ⭐⭐⭐ 🟢 Maximum subarray (Kadane). `nums` has 1 <= len <= 10^5 integers (negatives allowed, |value| <= 10^4). Return the largest sum of a non-empty contiguous subarray (so an all-negative list returns its largest element, not 0). Define the state as 'best sum of a subarray that ends exactly at index i', give the transition, and say why the answer is the maximum over all i, not the last state. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every subarray on small inputs. Example: nums=[-2, 1, -3, 4, -1, 2, 1, -5, 4] -> 6; nums=[-3, -1, -2] -> -1; nums=[7] -> 7; nums=[5, -9, 6] -> 6.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D DP with a "must end here" state (Kadane). The trick is the state, not the loop.

**Say this first (1 line):** "Let best_here(i) be the best sum of a subarray that ends exactly at i; it is either nums[i] alone or nums[i] plus best_here(i-1), and the answer is the maximum of best_here over all i. O(n) time, O(1) space."

**Brute force:** Enumerate every (i, j), take the max of the sums. With prefix sums each subarray sum is O(1), so O(n^2) time; recomputing each sum is O(n^3). Used as the checker.

**Optimal:**
- State: `E[i]` = max sum over subarrays that end exactly at index i (non-empty).
- Transition: such a subarray is either just `nums[i]` or a subarray ending at i-1 extended by `nums[i]`. So `E[i] = max(nums[i], E[i-1] + nums[i]) = nums[i] + max(0, E[i-1])`.
- Base: `E[0] = nums[0]`.
- Answer: `max(E[i])` over all i, not `E[n-1]`. The best subarray can end anywhere, and the last state only covers subarrays that end at the last index (the code counts 10,427 of 19,607 small lists where `E[n-1]` is not the answer).
- Start `best` at `nums[0]`, not 0, so all-negative input returns the largest element (non-empty rule).
- Space: only `E[i-1]` is needed, so keep one variable plus the running maximum.

**Complexity:** Time O(n), space O(1). A bottom-up loop, so n = 10^5 has no recursion concern. (A top-down recursion for `E(i)` would nest n deep and fail at the default limit; the loop avoids that.)

**Dry run:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`.

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| nums[i] | -2 | 1 | -3 | 4 | -1 | 2 | 1 | -5 | 4 |
| E[i] | -2 | 1 | -2 | 4 | 3 | 5 | 6 | 1 | 5 |

Max over i is 6 (subarray `[4, -1, 2, 1]`, ending at i = 6). The last state is 5, which is why you take the max.

**Code:**
```python
import itertools
import random

random.seed(103)

def kadane(nums):
    """best_here = best sum of a subarray ENDING exactly at i: max(x, best_here_prev + x). Answer = max over all i."""
    best_here = best = nums[0]
    for x in nums[1:]:
        best_here = max(x, best_here + x)      # extend the previous subarray, or restart at x
        best = max(best, best_here)
    return best

def kadane_table(nums):
    ends, cur = [], 0
    for i, x in enumerate(nums):
        cur = x if i == 0 else max(x, cur + x)
        ends.append(cur)
    return ends

def brute(nums):
    n = len(nums)
    return max(sum(nums[i:j + 1]) for i in range(n) for j in range(i, n))   # O(n^2) subarrays (sum is O(n): O(n^3) overall)

def brute_prefix(nums):
    """True O(n^2): prefix sums."""
    n = len(nums); pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    return max(pre[j] - pre[i] for i in range(n) for j in range(i + 1, n + 1))

for a, want in [([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), ([-3, -1, -2], -1), ([7], 7), ([5, -9, 6], 6)]:
    assert kadane(a) == brute(a) == brute_prefix(a) == want
print('4 prompt examples ok')

a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print('nums      ', a)
print('ends at i ', kadane_table(a))
print('answer = max over i =', max(kadane_table(a)), ' (last state is', kadane_table(a)[-1], ')')

for _ in range(1000):
    n = random.randint(1, 12)
    a = [random.randint(-10, 10) for _ in range(n)]
    assert kadane(a) == brute(a) == brute_prefix(a) == max(kadane_table(a)), a
print('1000 seeded random lists (len 1..12, values -10..10): Kadane == enumeration')

cnt = 0
for n in range(1, 7):
    for a in itertools.product(range(-3, 3), repeat=n):
        assert kadane(list(a)) == brute(list(a)); cnt += 1
print('exhaustive len 1..6 values -3..2:', cnt, 'lists ok')

# why max over all i: count lists where the last state is NOT the answer
last_wrong = 0; total = 0
for n in range(1, 6):
    for a in itertools.product(range(-3, 4), repeat=n):
        total += 1
        if kadane_table(list(a))[-1] != brute(list(a)):
            last_wrong += 1
print(f'last state != answer on {last_wrong} of {total} lists (len 1..5, values -3..3)')

# all-negative: answer is the largest element, never 0
for _ in range(200):
    a = [random.randint(-9, -1) for _ in range(random.randint(1, 8))]
    assert kadane(a) == max(a) < 0
print('all-negative lists: answer = max element (200 seeded lists)')

big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
print('n = 10^5 ->', kadane(big), end=' ')
pre = 0; mn = 0; best = -10**9
for x in big:
    pre += x; best = max(best, pre - mn); mn = min(mn, pre)
assert best == kadane(big); print('(agrees with the prefix-sum minus smallest earlier prefix method)')
```

**Output (my run):**
```
4 prompt examples ok
nums       [-2, 1, -3, 4, -1, 2, 1, -5, 4]
ends at i  [-2, 1, -2, 4, 3, 5, 6, 1, 5]
answer = max over i = 6  (last state is 5 )
1000 seeded random lists (len 1..12, values -10..10): Kadane == enumeration
exhaustive len 1..6 values -3..2: 55986 lists ok
last state != answer on 10427 of 19607 lists (len 1..5, values -3..3)
all-negative lists: answer = max element (200 seeded lists)
n = 10^5 -> 781145 (agrees with the prefix-sum minus smallest earlier prefix method)
```

**Edge cases:**
- Single element returns itself; `[-3, -1, -2]` returns -1, not 0.
- All positives returns the total; mixed with a huge negative in the middle restarts after it.
- Zeros: ties between subarrays do not matter for the sum.
- Initialising `best = 0` is wrong for all-negative input.

**Follow-ups:**
- Return the indices? Track the start when you restart (`E[i-1] <= 0` means restart at i) and record the best end. Tie rules must be stated.
- Circular array? Max of Kadane and (total - min subarray), with the all-negative special case.
- Maximum product subarray? Track both the max and the min ending here, since a negative flips them.

**Common mistakes:**
- Returning the last state instead of the max over all i.
- Starting `best` at 0 and losing the all-negative case.
- Resetting to 0 instead of to `nums[i]` when restarting (that silently allows an empty subarray).
- Treating Kadane as "greedy": it is a DP with an O(1) state; the proof is the transition above.

### Q4 ⭐⭐⭐ 🟢 Best time to buy and sell stock, one transaction, as a two-state DP. `prices` has 0 <= len <= 10^5 non-negative integers (price on each day). You may buy once and sell once later; return the maximum profit, or 0 if no profitable trade exists or the list is empty. Define the two states 'best cash while holding' and 'best cash while not holding', give the transition per day and the O(1)-space loop, and say how it relates to the one-pass minimum-so-far method. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) check of every buy/sell pair on small inputs. Example: prices=[7, 1, 5, 3, 6, 4] -> 5; prices=[7, 6, 4, 3, 1] -> 0; prices=[] -> 0; prices=[3] -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Stock-trading state-machine write-ups (techinterview.org DP state machine patterns, labuladong stock guide, system.design state-machine notes, a LeetCode Discuss single-template post; search snippets only, not opened)

**Pattern:** State-machine DP. Two states (holding, not holding), one pass, one transition per day. It is the seed of the cooldown and at-most-k versions.

**Say this first (1 line):** "Two states per day: hold = best cash while holding a share, free = best cash while not holding; hold = max(hold, -price), free = max(free, hold + price); answer is free. O(n) time, O(1) space, and it is the min-so-far method in other words."

**Brute force:** Try every buy day i and later sell day j, profit `prices[j] - prices[i]`, keep the max (and 0). O(n^2) time, O(1) space.

**Optimal:**
- States after day d: `hold[d]` = max cash you can have while owning a share; `free[d]` = max cash while owning none. Cash starts at 0.
- Transitions for price p:
  - `hold = max(hold, -p)`: keep the share, or buy today. Only one transaction is allowed, so the cash before the buy is 0, which gives `-p`.
  - `free = max(free, hold_old + p)`: stay out, or sell the share held since yesterday. Use the old `hold`; Python's tuple assignment does this for free.
- Base: `hold = -infinity` (cannot hold before day 0), `free = 0`. An empty list never enters the loop and returns 0.
- Answer: `free` at the end (never negative because staying out is always available).
- Link to min-so-far: unrolling `hold` gives `hold_d = -(minimum price up to day d)` (the code asserts this), and `free_d = max(free_{d-1}, p - min_so_far)`. So the "track the lowest price, keep the best gap" method is exactly this DP with the hold state collapsed into one variable.
- No recursion and no table, so n = 10^5 is no concern.

**Complexity:** Time O(n), space O(1).

**Dry run:** `prices = [7, 1, 5, 3, 6, 4]`.

| day | price | hold | free |
|---|---|---|---|
| 0 | 7 | -7 | 0 |
| 1 | 1 | -1 | 0 |
| 2 | 5 | -1 | 4 |
| 3 | 3 | -1 | 4 |
| 4 | 6 | -1 | 5 |
| 5 | 4 | -1 | 5 |

Answer 5 (buy at 1, sell at 6). `hold` tracks minus the lowest price; `free` is the best sell so far.

**Code:**
```python
import itertools
import random

random.seed(104)
NEG = float('-inf')

def stock_two_state(prices):
    """hold = best cash while holding a share, free = best cash while not holding (never bought, or sold).
    hold' = max(hold, -p)        (keep holding, or buy today: only ONE buy, so cash before it is 0)
    free' = max(free, hold + p)  (stay out, or sell today)"""
    hold, free = NEG, 0
    for p in prices:
        hold, free = max(hold, -p), max(free, hold + p)    # tuple assignment uses the OLD hold on the right
    return free

def stock_min_so_far(prices):
    best, low = 0, float('inf')
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best

def brute(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best

def table(prices):
    hold, free, rows = NEG, 0, []
    for p in prices:
        hold, free = max(hold, -p), max(free, hold + p)
        rows.append((p, hold, free))
    return rows

for pr, want in [([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0), ([], 0), ([3], 0)]:
    assert stock_two_state(pr) == stock_min_so_far(pr) == brute(pr) == want
print('4 prompt examples ok')

print('day price hold free   (prices [7, 1, 5, 3, 6, 4])')
for d, (p, h, f) in enumerate(table([7, 1, 5, 3, 6, 4])):
    print(f'{d:>3} {p:>5} {h:>4} {f:>4}')

for _ in range(1000):
    n = random.randint(0, 12)
    pr = [random.randint(0, 20) for _ in range(n)]
    assert stock_two_state(pr) == brute(pr) == stock_min_so_far(pr), pr
print('1000 seeded random lists (len 0..12, values 0..20): two-state == all-pairs == min-so-far')

cnt = 0
for n in range(0, 7):
    for pr in itertools.product(range(5), repeat=n):
        pr = list(pr)
        assert stock_two_state(pr) == brute(pr); cnt += 1
print('exhaustive len 0..6 values 0..4:', cnt, 'lists ok')

# the link: hold_i == -(min price so far), and free_i == best profit so far
for _ in range(300):
    pr = [random.randint(0, 20) for _ in range(random.randint(1, 12))]
    rows = table(pr)
    for i, (p, h, f) in enumerate(rows):
        assert h == -min(pr[:i + 1])
        assert f == brute(pr[:i + 1])
print('hold_i == -(min price so far) and free_i == best profit on the prefix: verified on 300 seeded lists')

big = [random.randint(0, 10**4) for _ in range(10**5)]
assert stock_two_state(big) == stock_min_so_far(big)
print('n = 10^5 ->', stock_two_state(big))
assert stock_two_state([]) == 0 and stock_two_state([5, 5, 5]) == 0 and stock_two_state([1, 2, 3, 4, 5]) == 4
print('edge asserts ok: empty, flat, strictly rising')
```

**Output (my run):**
```
4 prompt examples ok
day price hold free   (prices [7, 1, 5, 3, 6, 4])
  0     7   -7    0
  1     1   -1    0
  2     5   -1    4
  3     3   -1    4
  4     6   -1    5
  5     4   -1    5
1000 seeded random lists (len 0..12, values 0..20): two-state == all-pairs == min-so-far
exhaustive len 0..6 values 0..4: 19531 lists ok
hold_i == -(min price so far) and free_i == best profit on the prefix: verified on 300 seeded lists
n = 10^5 -> 10000
edge asserts ok: empty, flat, strictly rising
```

**Edge cases:**
- `[]` and `[3]` return 0; strictly falling prices return 0 (the "do nothing" option).
- Flat prices return 0.
- A sell on the same day as the buy is profit 0 and is harmless.
- `hold = -inf` is a float; `-inf + p` stays `-inf` so no special first-day branch is needed.

**Follow-ups:**
- Unlimited transactions: `hold = max(hold, free - p)` (re-use cash); equals the sum of positive day-to-day gaps.
- Cooldown or at most k transactions: add a state or a transaction index (Part 10, later questions).
- Why does min-so-far work? Because the best sell on day d pairs with the lowest earlier price; the DP shows that as `hold = -min`.

**Common mistakes:**
- Updating `free` with the already-updated `hold` (that lets you buy and sell on the same day, harmless here but wrong in the cooldown and k-transaction variants).
- `hold = max(hold, free - p)` for the one-transaction version, which allows multiple trades.
- Starting `hold` at 0 (which pretends you can hold for free).
- Returning `hold` or the final price gap instead of `free`.

### Q5 ⭐⭐⭐ 🟡 House robber (linear street). `nums` has 0 <= len <= 10^5 non-negative integers (cash in each house, <= 400). You cannot take two adjacent houses; return the maximum total (0 for an empty street). Give the state, the transition `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`, the base cases, and the two-variable version. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). The same take-or-skip idea on a tree is Part 7 Q45 (House Robber III); do not solve the tree version here. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a subset enumeration with the no-two-adjacent rule (n <= 12) on small inputs. Example: nums=[1, 2, 3, 1] -> 4; nums=[2, 7, 9, 3, 1] -> 12; nums=[] -> 0; nums=[5] -> 5; nums=[4, 1, 1, 4] -> 8.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D take-or-skip DP with a look-back of two. The "no two neighbours" rule turns into `dp[i-2]` on the take branch.

**Say this first (1 line):** "dp[i] is the best total from houses 0..i; either I skip house i and keep dp[i-1], or I take it and add dp[i-2]; so dp[i] = max(dp[i-1], dp[i-2] + nums[i]), O(n) time and two variables."

**Brute force:** Enumerate every subset of houses, discard those with two adjacent picks (`mask & (mask >> 1)`), keep the largest sum. 2^n subsets, so only for n <= 12. Used as the checker.

**Optimal:**
- State: `dp[i]` = maximum cash from houses `0..i` under the no-adjacent rule.
- Transition: house i is either skipped (best is `dp[i-1]`) or taken (house i-1 is then forbidden, so `dp[i-2] + nums[i]`). Take the max.
- Base cases: `dp[-1] = dp[-2] = 0` (no houses), so `dp[0] = nums[0]` and `dp[1] = max(nums[0], nums[1])`. An empty street returns 0.
- Two variables: `skip` = dp[i-2], `take` = dp[i-1]; each step does `skip, take = take, max(take, skip + x)`.
- Greedy does not work: on `[2, 3, 2]`, grabbing the biggest house gives 3 but the optimum is 4.
- Top-down is `f(i) = max(f(i-1), f(i-2) + nums[i])` with `@cache`. It is correct but nests n frames; at n = 10^5 it raises `RecursionError` under the default limit of 1000 (shown in the code; it still works at n = 300). Use the loop.
- The same take-or-skip idea on a tree is Part 7 Q45 (House Robber III). That is not solved here.

**Complexity:** Time O(n), space O(1) (the table version O(n)). Brute force is O(2^n * n).

**Dry run:** `nums = [2, 7, 9, 3, 1]`.

| i | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| nums[i] | 2 | 7 | 9 | 3 | 1 |
| skip i: dp[i-1] | 0 | 2 | 7 | 11 | 11 |
| take i: dp[i-2] + nums[i] | 2 | 7 | 11 | 10 | 12 |
| dp[i] | 2 | 7 | 11 | 11 | 12 |

Answer 12 (houses with 2, 9, 1).

**Code:**
```python
import itertools
import random
import sys
from functools import cache

random.seed(105)

def rob(nums):
    """dp[i] = best total using houses 0..i, dp[i] = max(dp[i-1] (skip i), dp[i-2] + nums[i] (take i)),
    with dp[-1] = dp[-2] = 0 (no houses). Two variables."""
    skip, take = 0, 0          # dp[i-2], dp[i-1]
    for x in nums:
        skip, take = take, max(take, skip + x)
    return take

def rob_table(nums):
    dp = []                       # dp[i] = best using houses 0..i
    for i, x in enumerate(nums):
        dp.append(max(dp[i - 1] if i >= 1 else 0, (dp[i - 2] if i >= 2 else 0) + x))
    return dp

def rob_memo(nums):
    @cache
    def f(i):                      # best using houses 0..i
        if i < 0:
            return 0
        return max(f(i - 1), f(i - 2) + nums[i])
    return f(len(nums) - 1)

def brute(nums):
    """All subsets with no two adjacent houses (n <= 12): 4096 masks."""
    n = len(nums); best = 0
    for mask in range(1 << n):
        if mask & (mask >> 1):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best

for a, want in [([1, 2, 3, 1], 4), ([2, 7, 9, 3, 1], 12), ([], 0), ([5], 5), ([4, 1, 1, 4], 8)]:
    assert rob(a) == rob_memo(a) == brute(a) == want
print('5 prompt examples ok')

print('nums =', [2, 7, 9, 3, 1])
print('dp   =', rob_table([2, 7, 9, 3, 1]), ' (dp[i] = best using houses 0..i)')

for _ in range(1000):
    n = random.randint(0, 12)
    a = [random.randint(0, 400) for _ in range(n)]
    assert rob(a) == brute(a) == (rob_table(a) or [0])[-1] == rob_memo(a), a
print('1000 seeded random streets (len 0..12, cash 0..400): DP == subset enumeration')

cnt = 0
for n in range(0, 8):
    for a in itertools.product(range(4), repeat=n):
        assert rob(list(a)) == brute(list(a)); cnt += 1
print('exhaustive len 0..7 values 0..3:', cnt, 'streets ok')

# greedy "take the biggest house first" is wrong: 4 1 1 4 style
a = [2, 3, 2]
print('greedy-by-largest on [2, 3, 2] takes 3 -> 3, optimum is', rob(a))
assert rob(a) == 4

big = [random.randint(0, 400) for _ in range(10**5)]
print('n = 10^5 bottom-up ->', rob(big))
try:
    rob_memo(big)
    print('memoised: ok')
except RecursionError:
    print('memoised n = 10^5: RecursionError (default limit', sys.getrecursionlimit(), ')')
print('memoised n = 300 ->', rob_memo(big[:300]), '== bottom-up', rob(big[:300]))
```

**Output (my run):**
```
5 prompt examples ok
nums = [2, 7, 9, 3, 1]
dp   = [2, 7, 11, 11, 12]  (dp[i] = best using houses 0..i)
1000 seeded random streets (len 0..12, cash 0..400): DP == subset enumeration
exhaustive len 0..7 values 0..3: 21845 streets ok
greedy-by-largest on [2, 3, 2] takes 3 -> 3, optimum is 4
n = 10^5 bottom-up -> 11793642
memoised n = 10^5: RecursionError (default limit 1000 )
memoised n = 300 -> 35899 == bottom-up 35899
```

**Edge cases:**
- `[]` returns 0; `[5]` returns 5.
- `[4, 1, 1, 4]` returns 8 (both ends), not 5; a "take every other house" rule that fixes the parity fails here.
- All zeros returns 0.
- Two houses: the max of the two, never the sum.

**Follow-ups:**
- Circular street (first and last are neighbours)? Run the linear solution twice, on `nums[:-1]` and `nums[1:]`, take the max (handle length 1 separately).
- Return which houses? Keep the table and walk back: if `dp[i] == dp[i-1]` skip, else take and jump to i-2.
- Tree version? Return a pair (rob, skip) from each node (Part 7 Q45).

**Common mistakes:**
- `dp[i] = dp[i-1] + nums[i]` (ignores the adjacency rule) or `dp[i-2] + nums[i]` without the max with `dp[i-1]`.
- Wrong base for `dp[1]`: it is `max(nums[0], nums[1])`, not `nums[1]`.
- Crashing on empty input by reading `nums[0]` first.
- Memoised recursion at 10^5 houses.

### Q6 ⭐⭐⭐ 🟡 Coin change, minimum number of coins. `coins` is a list of 1 <= len <= 12 distinct positive integers (each <= 10^4), `amount` is an integer 0 <= amount <= 10^4, and each coin can be used any number of times. Return the fewest coins that sum to `amount`, 0 for amount 0, and -1 if it is impossible. Define the state `dp[a]`, the transition, and the base cases. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). Explain with the counter-example in Part 8 Q33 (When greedy fails: coins) why taking the largest coin first is not enough. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the amount with no memo (amount <= 12) on small inputs. Example: coins=[1, 2, 5], amount=11 -> 3; coins=[2], amount=3 -> -1; coins=[7], amount=0 -> 0; coins=[1, 3, 4], amount=6 -> 2.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Unbounded knapsack, optimising version. 1D DP over the amount; each cell asks "which coin did I use last?".

**Say this first (1 line):** "dp[a] is the fewest coins for exactly a; dp[0] = 0, dp[a] = 1 + min over coins c <= a of dp[a - c], infinity means impossible; bottom-up over a = 1..amount, O(amount * k) time, O(amount) space. Greedy fails."

**Brute force:** Plain recursion `f(a) = 1 + min(f(a - c))` over coins with no memo. The same sub-amount is recomputed over and over, so it is exponential; fine for amount <= 12 and used as the checker.

**Optimal:**
- State: `dp[a]` = minimum number of coins whose values sum to exactly a, for a = 0..amount.
- Transition: the last coin is some c <= a, so `dp[a] = 1 + min(dp[a - c])` over all coins; if every `dp[a - c]` is infinity, `dp[a]` stays infinity.
- Base: `dp[0] = 0` (no coins make zero). Every other cell starts at infinity. The answer is `dp[amount]`, or -1 if it is still infinity.
- Why order of loops does not matter here: min is symmetric, so coin-outer or amount-outer both give the same value (compare with Q10, where order matters because we count).
- Why greedy is not enough: with `[1, 3, 4]` and amount 6, largest-first takes 4+1+1 = 3 coins but 3+3 = 2. With `[2, 5]` and amount 6 greedy takes 5, is stuck with 1, and answers -1 although 2+2+2 works. The full counter-example discussion is Part 8 Q33 (When greedy fails: coins). In the exhaustive check below, greedy is wrong on 231 of 1,905 small cases.
- Recursion limit: the memoised version `f(a)` follows coin 1 down `a, a-1, a-2, ...`, so it nests about `amount` deep. At amount 10^4 it raises `RecursionError` under the default limit of 1000 (shown in the code; at amount 500 it works). The bottom-up loop has no such problem.
- Space: the table is O(amount). It cannot shrink to O(1) because the look-back distances are the coin values.

**Complexity:** Time O(amount * k) for k coins (at most 10^4 * 12 steps), space O(amount).

**Dry run:** `coins = [1, 2, 5]`, amount 11.

| a | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dp[a] | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 3 | 2 | 3 |

Example cell: `dp[11] = 1 + min(dp[10], dp[9], dp[6]) = 1 + min(2, 3, 2) = 3` (5 + 5 + 1). For `[1, 3, 4]` the table is `[0, 1, 2, 1, 1, 2, 2]`, so `dp[6] = 2`.

**Code:**
```python
import itertools
import random
import sys
from functools import cache

random.seed(106)
INF = float('inf')

def coin_min(coins, amount):
    """dp[a] = fewest coins to make exactly a. dp[0] = 0, dp[a] = 1 + min(dp[a - c]) over coins c <= a. INF = impossible."""
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1

def dp_table(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp

def coin_memo(coins, amount):
    @cache
    def f(a):
        if a == 0:
            return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    r = f(amount)
    return r if r != INF else -1

def brute(coins, amount):
    """Plain recursion over the amount, no memo (amount <= 12)."""
    def f(a):
        if a == 0:
            return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    r = f(amount)
    return r if r != INF else -1

def greedy(coins, amount):
    """Largest coin first. Shown wrong."""
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c
        amount %= c
    return n if amount == 0 else -1

for cs, am, want in [([1, 2, 5], 11, 3), ([2], 3, -1), ([7], 0, 0), ([1, 3, 4], 6, 2)]:
    assert coin_min(cs, am) == brute(cs, am) == coin_memo(cs, am) == want
print('4 prompt examples ok')

print('coins [1, 2, 5], dp[0..11] =', dp_table([1, 2, 5], 11))
print('coins [1, 3, 4], dp[0..6]  =', dp_table([1, 3, 4], 6))
print('greedy on coins [1, 3, 4], amount 6 ->', greedy([1, 3, 4], 6), '(4+1+1) but optimum is', coin_min([1, 3, 4], 6), '(3+3)')
print('greedy on coins [2, 5], amount 6 ->', greedy([2, 5], 6), 'but optimum is', coin_min([2, 5], 6), '(2+2+2)')

for _ in range(1000):
    k = random.randint(1, 5)
    cs = random.sample(range(1, 13), k)
    am = random.randint(0, 12)
    assert coin_min(cs, am) == brute(cs, am), (cs, am)
print('1000 seeded random (<= 5 coins in 1..12, amount 0..12): DP == plain recursion')

# exhaustive: every non-empty coin subset of 1..7, every amount 0..14; count where greedy fails
tot = bad_val = bad_imp = 0
for mask in range(1, 1 << 7):
    cs = [i + 1 for i in range(7) if mask >> i & 1]
    for am in range(15):
        d = coin_min(cs, am); g = greedy(cs, am); tot += 1
        assert d == brute(cs, am)
        if g != d:
            if g == -1: bad_imp += 1
            else: bad_val += 1
print(f'exhaustive coin sets in 1..7 x amounts 0..14 = {tot} cases: DP == recursion; greedy wrong on {bad_val + bad_imp} ({bad_imp} of them says -1 when a solution exists)')

assert greedy([1, 2, 5], 11) == 3
for cs in ([1, 5, 10, 25],):                              # canonical systems: greedy happens to work
    assert all(greedy(cs, a) == coin_min(cs, a) for a in range(200))

# large sizes
cs = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 5000, 7]
print('amount 10^4, 12 coins, bottom-up ->', coin_min(cs, 10**4))
print('coins [2], amount 9999 ->', coin_min([2], 9999), '; coins [2], amount 10^4 ->', coin_min([2], 10**4))
try:
    coin_memo([1, 2, 5], 10**4)
    print('memoised amount 10^4: ok')
except RecursionError:
    print('memoised amount 10^4: RecursionError (default limit', sys.getrecursionlimit(), ')')
print('memoised amount 500 ->', coin_memo([1, 2, 5], 500), '== bottom-up', coin_min([1, 2, 5], 500))
```

**Output (my run):**
```
4 prompt examples ok
coins [1, 2, 5], dp[0..11] = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]
coins [1, 3, 4], dp[0..6]  = [0, 1, 2, 1, 1, 2, 2]
greedy on coins [1, 3, 4], amount 6 -> 3 (4+1+1) but optimum is 2 (3+3)
greedy on coins [2, 5], amount 6 -> -1 but optimum is 3 (2+2+2)
1000 seeded random (<= 5 coins in 1..12, amount 0..12): DP == plain recursion
exhaustive coin sets in 1..7 x amounts 0..14 = 1905 cases: DP == recursion; greedy wrong on 231 (169 of them says -1 when a solution exists)
amount 10^4, 12 coins, bottom-up -> 2
coins [2], amount 9999 -> -1 ; coins [2], amount 10^4 -> 5000
memoised amount 10^4: RecursionError (default limit 1000 )
memoised amount 500 -> 100 == bottom-up 100
```

**Edge cases:**
- `amount = 0` returns 0 even if every coin is large (`[7]`, 0 -> 0).
- Impossible: `[2]` and 3 returns -1; the infinity must not be returned as a number.
- A coin larger than the amount is skipped (`c <= a`).
- `[1]` with amount 10^4 returns 10^4.

**Follow-ups:**
- Number of ways instead of fewest coins? That is Q10; the loop order changes meaning.
- Recover which coins? Store the last coin per cell and walk back (tie rules must be stated).
- Faster? BFS over amounts gives the same O(amount * k); no better in the worst case.

**Common mistakes:**
- Greedy largest-first, which is wrong for non-canonical coin sets.
- Using `amount + 1` as infinity and forgetting to map it to -1 (fine if you map it, a bug if you return it).
- `dp[0] = 1` (that counts the empty set as a coin).
- Memoised recursion at amount 10^4 hitting RecursionError.

### Q7 ⭐⭐⭐ 🟡 Longest increasing subsequence, O(n^2) and O(n log n). `nums` has 0 <= len <= 10^5 integers (|value| <= 10^9, repeats allowed). A subsequence keeps the original order but may skip elements; it is strictly increasing. Return `[length, tails]` where `tails` is the final array of the patience-sorting method: `tails[k]` is the smallest possible last value of any strictly increasing subsequence of length k + 1, maintained by replacing the first entry that is >= x using `bisect_left` (see Part 5 Q11 for bisect semantics). Return `[0, []]` for an empty list. Give the O(n^2) DP only for len <= 2500 as a cross-check, explain why `tails` stays sorted (the patience-sorting argument: why the number of piles equals the length), and note that `tails` itself is generally NOT an LIS. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against all subsequences enumerated for len <= 12 (length, and the smallest last value for each length) on small inputs. Example: nums=[10, 9, 2, 5, 3, 7, 101, 18] -> [4, [2, 3, 7, 18]]; nums=[0, 1, 0, 3, 2, 3] -> [4, [0, 1, 2, 3]]; nums=[7, 7, 7] -> [1, [7]]; nums=[] -> [0, []]; nums=[4, 10, 4, 3, 8, 9] -> [3, [3, 8, 9]].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** LIS as a 1D DP (O(n^2)), then the patience-sorting speed-up: keep, for each length, the smallest possible tail, and find the slot by binary search (Part 5 Q11 for `bisect_left`).

**Say this first (1 line):** "O(n^2): dp[i] is the longest increasing subsequence ending at i. O(n log n): tails[k] is the smallest last value of any increasing subsequence of length k+1; for each x, bisect_left on tails and overwrite or append; the length is len(tails)."

**Brute force:** Enumerate all 2^n subsequences, keep the strictly increasing ones, and record for each length the smallest last value (n <= 12). The O(n^2) DP is the mid-level reference (used for n up to 2500).

**Optimal:**
- O(n^2) state: `dp[i]` = length of the longest strictly increasing subsequence ending exactly at i. `dp[i] = 1 + max(dp[j])` over j < i with `nums[j] < nums[i]` (or 1). Answer: the max of all dp[i], not the last one. Base: every `dp[i] >= 1`.
- Faster state: `tails[k]` = smallest possible last value of a strictly increasing subsequence of length k+1.
- Why `tails` is strictly increasing: if a subsequence of length k+2 ends at value v, drop its last element to get one of length k+1 ending at something smaller than v. So `tails[k] < tails[k+1]`. Sorted means we can binary search.
- Update for x: find the first index i with `tails[i] >= x` using `bisect_left`.
  - If none, x extends the longest subsequence: append.
  - Else x is a smaller (or equal) ending for length i+1: overwrite `tails[i] = x`.
  - `bisect_left` (not `bisect_right`) is what makes equal values replace instead of extend, so the result is strictly increasing.
- Patience sorting argument: deal cards left to right, each onto the leftmost pile whose top is >= x, else start a new pile. Pile tops are exactly `tails` (the code checks this). If a comes before b and a < b, then when b arrives the top of a's pile is <= a < b (tops only decrease), so b lands on a strictly later pile. Hence an increasing subsequence uses strictly increasing pile numbers: length <= piles. Conversely, linking each card to the top of the previous pile at the time it was placed gives an increasing subsequence through every pile, of length = piles. So piles = LIS length.
- Warning: `tails` is generally NOT an LIS. It mixes values from different times. On `[2, 5, 3, 1]` it ends as `[1, 3]`, but 1 comes after 3 in the input. The code counts 441 of 2000 seeded lists where `tails` is not even a subsequence. Only `len(tails)` is trusted as an answer; the oracle confirms each `tails[k]` is the smallest last value for length k+1.
- Recursion: a memoised "LIS ending at i" recursion can nest n deep; on an increasing list of 1500 it raises `RecursionError` at the default limit of 1000 (fine at 300). The recursion depth depends on the call order, so do not rely on it; the loop versions have no such risk.

**Complexity:** O(n^2) time and O(n) space for the DP. The tails method is O(n log n) time (one `bisect_left` per element) and O(n) space.

**Dry run:** `nums = [10, 9, 2, 5, 3, 7, 101, 18]`.

| x | 10 | 9 | 2 | 5 | 3 | 7 | 101 | 18 |
|---|---|---|---|---|---|---|---|---|
| tails after x | [10] | [9] | [2] | [2, 5] | [2, 3] | [2, 3, 7] | [2, 3, 7, 101] | [2, 3, 7, 18] |

The O(n^2) table of "LIS ending at i" is `[1, 1, 1, 2, 2, 3, 4, 4]`, max 4. Answer `[4, [2, 3, 7, 18]]`; here 2, 3, 7, 18 is a real subsequence by luck, in general not (see above).

**Code:**
```python
import random
import sys
from bisect import bisect_left
from functools import cache

random.seed(107)

def lis_tails(nums):
    """Patience sorting. tails[k] = smallest last value of a strictly increasing subsequence of length k+1.
    Replace the first entry >= x (bisect_left), or append when x is bigger than all."""
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return [len(tails), tails]

def lis_n2(nums):
    """O(n^2) DP: dp[i] = length of the longest strictly increasing subsequence ENDING at i."""
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp, default=0), dp

def lis_memo(nums):
    n = len(nums)
    @cache
    def f(i):                                   # LIS ending at i
        best = 1
        for j in range(i - 1, -1, -1):
            if nums[j] < nums[i]:
                best = max(best, f(j) + 1)
        return best
    return max((f(i) for i in range(n - 1, -1, -1)), default=0)   # start from the end: deepest chain first

def brute(nums):
    """Enumerate every subsequence (len <= 12). For each strictly increasing one, record the smallest last value per length."""
    n = len(nums)
    best_last = {}                              # length -> smallest last value
    for mask in range(1, 1 << n):
        sub = [nums[i] for i in range(n) if mask >> i & 1]
        if all(sub[k] < sub[k + 1] for k in range(len(sub) - 1)):
            L = len(sub)
            if L not in best_last or sub[-1] < best_last[L]:
                best_last[L] = sub[-1]
    if not best_last:
        return [0, []]
    L = max(best_last)
    return [L, [best_last[k] for k in range(1, L + 1)]]

def piles(nums):
    """Patience sorting as cards: put x on the leftmost pile whose top is >= x, else open a new pile."""
    tops = []
    for x in nums:
        for k, t in enumerate(tops):
            if t >= x:
                tops[k] = x; break
        else:
            tops.append(x)
    return tops

def is_subseq(sub, nums):
    it = iter(nums)
    return all(any(x == y for y in it) for x in sub)

for a, want in [([10, 9, 2, 5, 3, 7, 101, 18], [4, [2, 3, 7, 18]]), ([0, 1, 0, 3, 2, 3], [4, [0, 1, 2, 3]]),
                ([7, 7, 7], [1, [7]]), ([], [0, []]), ([4, 10, 4, 3, 8, 9], [3, [3, 8, 9]])]:
    assert lis_tails(a) == brute(a) == want, a
    assert lis_n2(a)[0] == want[0] == lis_memo(a)
print('5 prompt examples ok')

a = [10, 9, 2, 5, 3, 7, 101, 18]
t = []
print('x     tails after x   (nums =', a, ')')
for x in a:
    i = bisect_left(t, x)
    if i == len(t): t.append(x)
    else: t[i] = x
    print(f'{x:<5} {t}')
print('O(n^2) table (LIS ending at i):', lis_n2(a)[1])

for _ in range(500):
    n = random.randint(0, 12)
    a = [random.randint(-6, 6) for _ in range(n)]
    got = lis_tails(a)
    assert got == brute(a), a
    assert lis_n2(a)[0] == got[0] == lis_memo(a)
    assert all(got[1][k] < got[1][k + 1] for k in range(len(got[1]) - 1))      # tails strictly increasing
    assert piles(a) == got[1]                                                   # piles == tails
    # prefix property: tails after every prefix equals the brute force on that prefix
    for p in range(0, n + 1, 4):
        assert lis_tails(a[:p]) == brute(a[:p])
print('500 seeded random lists (len 0..12, values -6..6): tails, length, piles, O(n^2) DP, memo all agree with subsequence enumeration')

# tails itself is generally NOT a subsequence of nums, hence not an LIS
cnt = 0; tot = 0; ex = None
for _ in range(2000):
    a = [random.randint(0, 9) for _ in range(random.randint(1, 8))]
    tot += 1
    tl = lis_tails(a)[1]
    if not is_subseq(tl, a):
        cnt += 1
        ex = ex or a
print(f'tails is not a subsequence of nums in {cnt} of {tot} seeded lists; first example {ex} -> tails {lis_tails(ex)[1]}')
assert lis_tails([2, 5, 3, 1]) == [2, [1, 3]]       # 1 comes after 3 in nums, so [1, 3] is not a subsequence

# larger: O(n^2) vs O(n log n) lengths
for _ in range(5):
    a = [random.randint(-10**9, 10**9) for _ in range(2500)]
    assert lis_tails(a)[0] == lis_n2(a)[0]
print('5 seeded lists of length 2500 (O(n^2) DP vs O(n log n) length): equal')

# sorted input is the O(n) piles / worst depth case
for n_ in (10**5,):
    inc = list(range(n_)); dec = list(range(n_, 0, -1))
    assert lis_tails(inc)[0] == n_ and lis_tails(dec)[0] == 1 and lis_tails(dec)[1] == [1]
big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
print('n = 10^5 random: LIS length', lis_tails(big)[0], ', strictly increasing 0..99999 -> 100000, strictly decreasing -> 1')

# recursion limit for the memoised O(n^2) version
print('default recursion limit:', sys.getrecursionlimit())
for n_ in (300, 1500):
    try:
        lis_memo(list(range(n_)))
        print(f'memoised LIS on increasing list n={n_}: ok')
    except RecursionError:
        print(f'memoised LIS on increasing list n={n_}: RecursionError')
```

**Output (my run):**
```
5 prompt examples ok
x     tails after x   (nums = [10, 9, 2, 5, 3, 7, 101, 18] )
10    [10]
9     [9]
2     [2]
5     [2, 5]
3     [2, 3]
7     [2, 3, 7]
101   [2, 3, 7, 101]
18    [2, 3, 7, 18]
O(n^2) table (LIS ending at i): [1, 1, 1, 2, 2, 3, 4, 4]
500 seeded random lists (len 0..12, values -6..6): tails, length, piles, O(n^2) DP, memo all agree with subsequence enumeration
tails is not a subsequence of nums in 441 of 2000 seeded lists; first example [7, 7, 2, 5, 4, 3, 0] -> tails [0, 3]
5 seeded lists of length 2500 (O(n^2) DP vs O(n log n) length): equal
n = 10^5 random: LIS length 624 , strictly increasing 0..99999 -> 100000, strictly decreasing -> 1
default recursion limit: 1000
memoised LIS on increasing list n=300: ok
memoised LIS on increasing list n=1500: RecursionError
```

**Edge cases:**
- `[]` returns `[0, []]`; `[7, 7, 7]` returns `[1, [7]]` (strict increase, equals replace).
- Strictly increasing 0..99999 gives 100000; strictly decreasing gives 1.
- Negatives and values up to 10^9 are fine: only comparisons are used.
- n = 10^5 with the tails method is about 10^5 binary searches; the O(n^2) DP would be 5 * 10^9 steps, hence the 2500 cap.

**Follow-ups:**
- Non-decreasing variant? Use `bisect_right` so equal values extend (`bisect_left` would give the strict length; wrong here).
- Recover one actual LIS? Also record, per element, the index of the tail it replaced's predecessor, and walk back.
- Count all LIS? Needs the O(n^2) DP with counts (or a Fenwick tree), not the tails method.

**Common mistakes:**
- `bisect_right` for the strict version, which lets equal values extend.
- Returning `tails` as the subsequence.
- Answering `dp[-1]` instead of `max(dp)` in the O(n^2) DP.
- Using the O(n^2) DP at n = 10^5.

### Q8 ⭐⭐⭐ 🟡 Word break. `s` is a non-empty lowercase string (1 <= len <= 200) and `word_dict` a list of 1 to 100 distinct non-empty lowercase words (each of length <= 20). Return True if `s` can be split into a sequence of dictionary words (words may be reused), else False. Define `dp[i]` = 'the first i characters can be segmented', give the transition, and state the number of substring checks (at most n times the number of distinct word lengths), noting that each check also slices and hashes up to 20 characters. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over prefixes with no memo on small inputs. Example: s='leetcode', word_dict=['leet', 'code'] -> True; s='catsandog', word_dict=['cats', 'dog', 'sand', 'and', 'cat'] -> False; s='aaaa', word_dict=['a', 'aa'] -> True; s='x', word_dict=['y'] -> False.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D DP over prefixes: "can the first i characters be built?" Each cell looks back by the length of a dictionary word.

**Say this first (1 line):** "dp[i] means the first i characters can be segmented; dp[0] is True; dp[i] is True if for some word length L, dp[i-L] is True and s[i-L:i] is in the set. At most n times the number of distinct word lengths checks."

**Brute force:** Recursion over prefixes with no memo: `f(rest)` is True if some word is a prefix of `rest` and `f(rest[len(word):])` is True. Without a cache this is exponential: on `'a' * 22 + 'b'` with words `[a, aa, aaa]` it makes 900,140 calls (the code prints this).

**Optimal:**
- State: `dp[i]` = True iff `s[:i]` is a concatenation of dictionary words (words reusable).
- Base: `dp[0] = True` (the empty prefix is a valid, empty segmentation).
- Transition: the last word has some length L <= i, so `dp[i] = OR over L of (dp[i - L] and s[i - L:i] in words)`. Only L values that equal some word's length matter, so loop over the sorted distinct lengths and stop when `L > i`.
- Answer: `dp[n]`.
- Use a `set` for words: membership is O(1) on average after hashing the slice.
- Substring-check count: for each of the n positions we try at most D distinct word lengths, so at most `n * D` checks (the code asserts this on 300 seeded cases, and in a worst case with nothing matching, n = 200 and 20 lengths gives 3,810 against the bound 4,000). Each check also builds a slice and hashes up to 20 characters, so the work is O(n * D * maxlen) character operations, here at most 200 * 20 * 20.
- Early `break` once `dp[i]` is True saves work but does not change the bound.
- Recursion: the memoised top-down version `f(i)` (can `s[i:]` be segmented) nests at most `len(s)` frames, so at the stated n <= 200 it stays far below the default limit of 1000 and works. It would raise `RecursionError` only for sizes outside this prompt (n = 5000 in the code). The bottom-up loop is still the safer default.

**Complexity:** Time O(n * D * m) where D = distinct word lengths (<= 20) and m = max word length (<= 20); space O(n + total word size).

**Dry run:** `s = 'leetcode'`, words `leet`, `code`.

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| prefix | "" | l | le | lee | leet | leetc | leetco | leetcod | leetcode |
| dp[i] | T | F | F | F | T | F | F | F | T |

dp[4] is True because dp[0] is True and `s[0:4] = 'leet'` is a word. dp[8] is True because dp[4] is True and `s[4:8] = 'code'` is a word. For `catsandog` the table is T F F T T F F T F F: dp[9] is False because the only way to cover `og` is missing, so the answer is False.

**Code:**
```python
import random
import string
import sys
from functools import cache

random.seed(108)

def word_break(s, word_dict, counter=None):
    """dp[i] = True if s[:i] can be segmented. dp[0] = True (empty prefix).
    dp[i] = any(dp[i - L] and s[i-L:i] in words) over the DISTINCT word lengths L <= i."""
    words = set(word_dict)
    lengths = sorted({len(w) for w in words})
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for L in lengths:
            if L > i:
                break
            if counter is not None:
                counter[0] += 1
            if dp[i - L] and s[i - L:i] in words:
                dp[i] = True
                break
    return dp[n]

def dp_row(s, word_dict):
    words = set(word_dict); dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(i >= len(w) and dp[i - len(w)] and s[i - len(w):i] == w for w in words)
    return dp

def memo(s, word_dict):
    words = set(word_dict)
    @cache
    def f(i):                      # can s[i:] be segmented?
        if i == len(s):
            return True
        return any(s.startswith(w, i) and f(i + len(w)) for w in words)
    return f(0)

def brute(s, word_dict):
    """Plain recursion over prefixes, no memo."""
    words = set(word_dict)
    def f(rest):
        if rest == '':
            return True
        return any(rest.startswith(w) and f(rest[len(w):]) for w in words)
    return f(s)

for s, wd, want in [('leetcode', ['leet', 'code'], True), ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], False),
                    ('aaaa', ['a', 'aa'], True), ('x', ['y'], False)]:
    assert word_break(s, wd) == brute(s, wd) == memo(s, wd) == want
print('4 prompt examples ok')

print('s = leetcode, words = [leet, code]; dp[0..8] =', dp_row('leetcode', ['leet', 'code']))
print('s = catsandog, words = [cats, dog, sand, and, cat]; dp[0..9] =', dp_row('catsandog', ['cats', 'dog', 'sand', 'and', 'cat']))

yes = 0
for _ in range(1500):
    alpha = 'ab' if random.random() < 0.7 else 'abc'
    words = sorted({''.join(random.choice(alpha) for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 5))})
    if random.random() < 0.5:                          # build a segmentable string half of the time
        s = ''.join(random.choice(words) for _ in range(random.randint(1, 5)))
        if random.random() < 0.4:
            s = s[:-1] + random.choice(alpha) if len(s) else s
    else:
        s = ''.join(random.choice(alpha) for _ in range(random.randint(1, 12)))
    s = s[:14] or 'a'
    a = word_break(s, words)
    assert a == brute(s, words) == memo(s, words) == dp_row(s, words)[-1], (s, words)
    yes += a
print(f'1500 seeded random cases: DP == plain recursion == memo ({yes} True, {1500 - yes} False)')

# check-count claim: at most n * (#distinct word lengths); count them, worst case = all false so no early break
for _ in range(300):
    n = random.randint(1, 200)
    words = sorted({''.join(random.choice('ab') for _ in range(random.randint(1, 20))) for _ in range(random.randint(1, 100))})
    s = ''.join(random.choice('ab') for _ in range(n))
    c = [0]; word_break(s, words, c)
    dl = len({len(w) for w in words})
    assert c[0] <= n * dl
print('substring checks <= n * (distinct word lengths) on 300 seeded cases with n up to 200, 100 words')

# worst case: nothing ever matches (early break never fires), 20 distinct word lengths: every position tries every length
n = 200; words = ['a' * k for k in range(1, 21)]; s = 'b' * n
c = [0]; r = word_break(s, words, c)
print('worst case n=200, 20 word lengths: result', r, ', checks =', c[0], ', bound n * 20 =', n * 20)
assert r is False and c[0] <= n * 20
# plain recursion blows up on the same input family (count calls on a smaller one)
calls = [0]
def counted(rest, words):
    calls[0] += 1
    return rest == '' or any(rest.startswith(w) and counted(rest[len(w):], words) for w in words)
counted('a' * 22 + 'b', ['a', 'aa', 'aaa']); print('plain recursion on a^22 b with [a, aa, aaa]:', calls[0], 'calls')

# recursion depth: memo depth <= len(s) <= 200, below the limit of 1000, so no RecursionError here
print('memoised depth is at most len(s) = 200; limit', sys.getrecursionlimit(), '->', memo('a' * 200, ['a']))
try:
    memo('a' * 5000, ['a']); print('memo n=5000: ok')
except RecursionError:
    print('memo n=5000 (outside the stated limits): RecursionError')
assert word_break('a' * 200, ['a']) is True
```

**Output (my run):**
```
4 prompt examples ok
s = leetcode, words = [leet, code]; dp[0..8] = [True, False, False, False, True, False, False, False, True]
s = catsandog, words = [cats, dog, sand, and, cat]; dp[0..9] = [True, False, False, True, True, False, False, True, False, False]
1500 seeded random cases: DP == plain recursion == memo (729 True, 771 False)
substring checks <= n * (distinct word lengths) on 300 seeded cases with n up to 200, 100 words
worst case n=200, 20 word lengths: result False , checks = 3810 , bound n * 20 = 4000
plain recursion on a^22 b with [a, aa, aaa]: 900140 calls
memoised depth is at most len(s) = 200; limit 1000 -> True
memo n=5000 (outside the stated limits): RecursionError
```

**Edge cases:**
- `s = 'x'`, words `['y']` returns False; `'aaaa'` with `['a', 'aa']` returns True.
- Word longer than the string is skipped (`L > i`).
- A string that can be segmented only by not taking the first matching word (`'aaaab'`-style traps) shows greedy longest-match is wrong; the DP tries all.
- Duplicate words are absent by the prompt, but a `set` makes them harmless anyway.

**Follow-ups:**
- Return one segmentation or all? Keep parent pointers (one) or backtrack with the dp table as a filter (all; the count of answers can be exponential).
- A trie instead of a set? Walk the trie forward from each True position; avoids slicing and hashing.
- Count the segmentations? Replace the boolean with a sum: `dp[i] += dp[i - L]`.

**Common mistakes:**
- Forgetting `dp[0] = True`, so nothing is ever True.
- Looping over every word per position and slicing with no length filter (works, but slower), or allowing `L > i` and indexing out of range.
- Plain recursion with no memo (exponential).
- Claiming the check count is O(n^2) when word lengths are bounded; with a set it is bounded by n * D.

### Q9 ⭐⭐⭐ 🟡 Decode ways. A string `s` of digits (1 <= len <= 100) encodes letters with 1 -> A, 2 -> B, ..., 26 -> Z; a code has no leading zero, so '0' alone and '06' are invalid. Return the number of ways to split `s` into valid codes, or 0 if there are none. Python integers are unbounded, so no modulus is needed at this size. Give `dp[i]`, the two conditions (the last one digit is 1..9, the last two digits are 10..26), the base cases dp[0] = 1, and the handling of zeros. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion that tries one or two digits on small inputs. Example: s='12' -> 2; s='226' -> 3; s='06' -> 0; s='10' -> 1; s='2101' -> 1; s='11111111111111111111111111111111111111111111111111' -> 20365011074.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D counting DP over prefixes with two look-back options (one digit or two digits). Same shape as climbing stairs, but each option is gated by a validity test.

**Say this first (1 line):** "dp[i] is the number of ways to decode the first i digits; add dp[i-1] if the last digit is 1..9, add dp[i-2] if the last two digits are 10..26; dp[0] = 1; zeros only survive inside 10 or 20."

**Brute force:** Recursion: at each position, if the digit is '0' return 0; otherwise take one digit, and also two digits when they form 10..26. No memo, so it re-solves suffixes: exponential. Used as the checker for len <= 14.

**Optimal:**
- State: `dp[i]` = number of ways to decode the prefix `s[:i]`.
- Base: `dp[0] = 1` (the empty prefix has one empty decoding). This is what makes `dp[1]` and `dp[2]` come out right.
- Transition: the last code is either one digit `s[i-1]` or two digits `s[i-2:i]`.
  - One digit counts only if it is `'1'..'9'` (a lone '0' is invalid): `dp[i] += dp[i-1]`.
  - Two digits count only if the number is 10..26 (this also rules out leading zeros like '06'): `dp[i] += dp[i-2]`.
- Zeros: a '0' cannot stand alone, so it must pair with the digit before it as 10 or 20. `'30'`, `'00'` and a leading '0' give 0 (the code checks these).
- Answer: `dp[n]`. Two variables are enough.
- No modulus: Python ints are exact, and the largest value at length 100 is the all-ones string, 573147844013817084101 (Fibonacci(101)); the code confirms all-ones is the maximum for every length up to 7 over the digits that matter, and the 50-ones prompt example gives 20365011074 = Fibonacci(51).
- Recursion: top-down depth is at most `len(s) <= 100`, far below the default limit of 1000, so memoisation is fine here (the code runs it at 100). It would hit `RecursionError` only at sizes outside this prompt (5000 in the code).

**Complexity:** Time O(n), space O(1) (O(n) with the table). The recursion without memo is O(2^n) in the worst case.

**Dry run:** `s = '226'`.

| i | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| prefix | "" | 2 | 22 | 226 |
| one digit valid? | | 2: yes (+dp[0]) | 2: yes (+dp[1]) | 6: yes (+dp[2]) |
| two digits valid? | | | 22: yes (+dp[0]) | 26: yes (+dp[1]) |
| dp[i] | 1 | 1 | 2 | 3 |

Answer 3 (2-2-6, 22-6, 2-26). For `'2101'` the table is `[1, 1, 2, 1, 1]`: at i = 2 ('21' and '1') gives 2; at i = 3 the digit is 0, so only '10' counts, dp[3] = dp[1] = 1; at i = 4 only the single '1' counts, since '01' is invalid, so dp[4] = dp[3] = 1. For `'06'` it is `[1, 0, 0]`.

**Code:**
```python
import random
import sys
from functools import cache

random.seed(109)

def decode_ways(s):
    """dp[i] = ways to decode s[:i]. dp[0] = 1.
    + dp[i-1] if s[i-1] is '1'..'9' ; + dp[i-2] if s[i-2:i] is '10'..'26'. Two variables."""
    prev, cur = 0, 1                      # dp[i-2] (placeholder), dp[i-1] = dp[0]
    for i in range(1, len(s) + 1):
        new = 0
        if s[i - 1] != '0':
            new += cur
        if i >= 2 and '10' <= s[i - 2:i] <= '26':
            new += prev
        prev, cur = cur, new
    return cur

def table(s):
    dp = [1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]
    return dp

def memo(s):
    @cache
    def f(i):
        if i == len(s):
            return 1
        if s[i] == '0':
            return 0
        r = f(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i:i + 2]) <= 26:
            r += f(i + 2)
        return r
    return f(0)

def brute(s):
    """Plain recursion: take one digit or two digits."""
    def f(rest):
        if rest == '':
            return 1
        if rest[0] == '0':
            return 0
        r = f(rest[1:])
        if len(rest) >= 2 and 10 <= int(rest[:2]) <= 26:
            r += f(rest[2:])
        return r
    return f(s)

ex = [('12', 2), ('226', 3), ('06', 0), ('10', 1), ('2101', 1), ('1' * 50, 20365011074)]
for s, want in ex:
    assert decode_ways(s) == memo(s) == table(s)[-1] == want, (s, decode_ways(s))
    if len(s) <= 25:
        assert brute(s) == want
print('6 prompt examples ok (the 50-digit one: 20365011074 = Fibonacci(51))')

print('s = 226  dp[0..3] =', table('226'))
print('s = 2101 dp[0..4] =', table('2101'))
print('s = 06   dp[0..2] =', table('06'))

for _ in range(1500):
    n = random.randint(1, 14)
    s = ''.join(random.choice('0123456789' if random.random() < 0.5 else '0126') for _ in range(n))
    assert decode_ways(s) == brute(s) == memo(s) == table(s)[-1], s
print('1500 seeded random digit strings (len 1..14): DP == plain recursion == memo == table')

# exhaustive: every digit string over {0,1,2,3,6,7} up to length 7 (the digits that matter for 10..26 boundaries)
import itertools
cnt = 0
for n in range(1, 8):
    top = 0
    for t in itertools.product('012367', repeat=n):
        s = ''.join(t)
        d = decode_ways(s)
        assert d == brute(s); cnt += 1
        top = max(top, d)
    assert top == decode_ways('1' * n)          # the all-ones string has the most decodings
print('exhaustive over alphabet 0,1,2,3,6,7 up to length 7:', cnt, 'strings ok; the all-ones string is the maximum at every length')

# claim: no modulus needed up to len 100: max is F(101) (all ones), about 5.7e20, python ints are exact
mx = decode_ways('1' * 100)
print('len 100 all ones ->', mx, '(exact big integer; no modulus needed)')
assert mx == 573147844013817084101
assert max(decode_ways(''.join(random.choice('12') for _ in range(100))) for _ in range(200)) <= mx

# zero handling
assert decode_ways('0') == 0 and decode_ways('00') == 0 and decode_ways('100') == 0 and decode_ways('30') == 0
assert decode_ways('27') == 1 and decode_ways('20') == 1 and decode_ways('1') == 1 and decode_ways('101') == 1
print('zero cases ok: 0, 00, 100, 30 -> 0;  20, 27, 101 -> 1')

# memoised depth <= len(s) <= 100, far below the limit; outside the limits it fails
print('memo on len 100 ->', memo('1' * 100) == mx, '; default limit', sys.getrecursionlimit())
try:
    memo('1' * 5000); print('memo len 5000: ok')
except RecursionError:
    print('memo len 5000 (outside the stated limit): RecursionError')
```

**Output (my run):**
```
6 prompt examples ok (the 50-digit one: 20365011074 = Fibonacci(51))
s = 226  dp[0..3] = [1, 1, 2, 3]
s = 2101 dp[0..4] = [1, 1, 2, 1, 1]
s = 06   dp[0..2] = [1, 0, 0]
1500 seeded random digit strings (len 1..14): DP == plain recursion == memo == table
exhaustive over alphabet 0,1,2,3,6,7 up to length 7: 335922 strings ok; the all-ones string is the maximum at every length
len 100 all ones -> 573147844013817084101 (exact big integer; no modulus needed)
zero cases ok: 0, 00, 100, 30 -> 0;  20, 27, 101 -> 1
memo on len 100 -> True ; default limit 1000
memo len 5000 (outside the stated limit): RecursionError
```

**Edge cases:**
- `'0'`, `'00'`, `'06'`, `'30'`, `'100'` all return 0.
- `'10'` and `'20'` return 1; `'27'` returns 1 (27 is not a code).
- A single digit `'1'` returns 1.
- Comparing the two digits as strings (`'10' <= t <= '26'`) is safe for exactly two characters, because equal-length digit strings order like numbers.

**Follow-ups:**
- Decode ways II (with `*` wildcards)? Same DP with multipliers and a modulus.
- Print all decodings? Backtracking guided by the dp table; the count can be exponential.
- Why does a '0' only allow the two-digit branch? Because no letter maps to 0 and no code has a leading zero.

**Common mistakes:**
- Treating '0' as valid on its own, or '06' as 6.
- Allowing 27..99 or 0X in the two-digit test.
- `dp[0] = 0`.
- Reading `s[i-2]` at i = 1 (negative index wraps around in Python and silently gives a wrong answer).

### Q10 ⭐⭐⭐ 🟡 Coin change II, number of combinations. `coins` has 1 <= len <= 12 distinct positive integers (each <= 5000) and `amount` is 0 <= amount <= 5000. Count the multisets of coins (order does not matter, each coin reusable) that sum to `amount`; amount 0 has exactly 1 (the empty multiset). Return the exact integer. Explain why the coin loop must be the OUTER loop to count combinations, and why this is a counting DP where the optimising version (Q6) uses min instead of +. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a recursion by coin index (take another copy or move to the next coin) on small inputs. Example: coins=[1, 2, 5], amount=5 -> 4; coins=[2], amount=3 -> 0; coins=[10], amount=0 -> 1; coins=[1, 2, 3], amount=4 -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Unbounded knapsack, counting version. Same table as Q6 (coin change, minimum coins), but the cell holds a count, so the update is `+=` and the loop order decides what is counted.

**Say this first (1 line):** "dp[a] is the number of multisets summing to a, dp[0] = 1; for each coin in the OUTER loop, for a from c up to amount do dp[a] += dp[a - c]; coin-outer counts combinations, amount-outer would count ordered sequences. O(amount * k) time, O(amount) space."

**Brute force:** Recursion by coin index: `f(i, rem)` = ways using coins `i..` to make `rem`; take another copy of coin i (`f(i, rem - coin)`) or move on (`f(i+1, rem)`). With no memo it is exponential. As a second, independent oracle the code also enumerates every count vector of the coins with `itertools.product`.

**Optimal:**
- State: after processing the first j coins, `dp[a]` = number of multisets of those coins summing to a.
- Base: `dp[0] = 1`, the empty multiset; all other cells start at 0.
- Transition when coin c is introduced: `dp[a] += dp[a - c]` for a = c..amount, amounts going UP. A multiset using c has a last copy of c removed, leaving a multiset (of the first j coins) that sums to `a - c`. Going upward lets `dp[a - c]` already include copies of c, which is what unbounded reuse means.
- Why the coin loop must be OUTER: each coin is introduced once and only extends combinations built from earlier coins, so every multiset is built in exactly one canonical order (all coin-1 copies, then coin-2 copies, ...). Putting the amount loop outside lets any coin come last at every amount, so 1+2 and 2+1 are both counted: you count ordered sequences. For `[1, 2, 5]` and amount 5 that gives 9, against 4 correct; over 600 seeded random cases the swapped loop differs on 219, and it equals the number of ordered sequences on all 300 checked.
- Counting versus optimising: Q6 uses `min(dp[a - c] + 1)` and infinity as the "impossible" value; here the combine is `+` and the "impossible" value is 0. With min, loop order does not matter; with a sum it does.
- Space: one array of amount + 1 big ints. Counts grow large (12 coins and amount 5000 gives 23303034594533, still exact in Python), no modulus is requested.
- Recursion: the memoised index recursion nests about `amount` deep (taking copies of coin 1), so at amount 5000 it raises `RecursionError` under the default limit of 1000 (shown in the code; it works at amount 300). A bottom-up loop is required.

**Complexity:** Time O(amount * k), space O(amount). Plain recursion: exponential.

**Dry run:** `coins = [1, 2, 5]`, amount 5, `dp[0..5]` after each coin is processed.

| after | dp[0] | dp[1] | dp[2] | dp[3] | dp[4] | dp[5] |
|---|---|---|---|---|---|---|
| start | 1 | 0 | 0 | 0 | 0 | 0 |
| coin 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| coin 2 | 1 | 1 | 2 | 2 | 3 | 3 |
| coin 5 | 1 | 1 | 2 | 2 | 3 | 4 |

Example: with coin 2, `dp[4] = old dp[4] + dp[2] = 1 + 2 = 3` (1111, 112, 22). Answer `dp[5] = 4`: 11111, 1112, 122, 5.

**Code:**
```python
import itertools
import random
import sys
from functools import cache

random.seed(110)

def ways_combinations(coins, amount):
    """dp[a] = number of multisets summing to a. Coin loop OUTER: each coin is introduced once, so a multiset
    is built in one fixed coin order (all 1s, then 2s, ...) and counted once."""
    dp = [1] + [0] * amount
    for c in coins:                       # outer: coins
        for a in range(c, amount + 1):    # inner: amounts upward (a coin may repeat)
            dp[a] += dp[a - c]
    return dp[amount]

def ways_ordered(coins, amount):
    """Amount OUTER, coin inner: counts ORDERED sequences (compositions). Wrong for this question."""
    dp = [1] + [0] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[amount]

def table_after_each_coin(coins, amount):
    dp = [1] + [0] * amount; rows = []
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
        rows.append((c, dp[:]))
    return rows

def by_index(coins, amount):
    """Oracle: ways(i, rem) = take another copy of coin i, or move to coin i+1. No memo."""
    def f(i, rem):
        if rem == 0:
            return 1
        if i == len(coins) or rem < 0:
            return 0
        return f(i, rem - coins[i]) + f(i + 1, rem)
    return f(0, amount)

def by_index_memo(coins, amount):
    @cache
    def f(i, rem):
        if rem == 0:
            return 1
        if i == len(coins) or rem < 0:
            return 0
        return f(i, rem - coins[i]) + f(i + 1, rem)
    return f(0, amount)

def enumerate_multisets(coins, amount):
    """Independent oracle: enumerate counts of each coin with itertools."""
    ranges = [range(amount // c + 1) for c in coins]
    return sum(1 for ks in itertools.product(*ranges) if sum(k * c for k, c in zip(ks, coins)) == amount)

for cs, am, want in [([1, 2, 5], 5, 4), ([2], 3, 0), ([10], 0, 1), ([1, 2, 3], 4, 4)]:
    assert ways_combinations(cs, am) == by_index(cs, am) == enumerate_multisets(cs, am) == want
print('4 prompt examples ok')

print('coins [1, 2, 5], amount 5: dp[0..5] after each coin')
print('  start       ', [1, 0, 0, 0, 0, 0])
for c, row in table_after_each_coin([1, 2, 5], 5):
    print(f'  after coin {c}:', row)
print('  ordered (amount-outer) answer for the same input:', ways_ordered([1, 2, 5], 5), '(compositions, not multisets)')

for _ in range(1000):
    k = random.randint(1, 4)
    cs = random.sample(range(1, 9), k)
    am = random.randint(0, 14)
    a = ways_combinations(cs, am)
    assert a == by_index(cs, am) == by_index_memo(cs, am) == enumerate_multisets(cs, am), (cs, am)
    # coin order must not matter for the count
    sh = cs[:]; random.shuffle(sh)
    assert ways_combinations(sh, am) == a
print('1000 seeded random (<= 4 coins in 1..8, amount 0..14): DP == index recursion == itertools enumeration; coin order irrelevant')

# the loop-order claim, measured
diff = same = 0
for _ in range(600):
    cs = random.sample(range(1, 9), random.randint(1, 4)); am = random.randint(0, 14)
    if ways_combinations(cs, am) != ways_ordered(cs, am): diff += 1
    else: same += 1
print(f'swapped loop order (amount outer) differs from the combination count on {diff} of 600 seeded cases')
# the swapped version counts ordered sequences: verify against a direct composition count
def compositions(cs, am):
    @cache
    def g(r):
        return 1 if r == 0 else sum(g(r - c) for c in cs if c <= r)
    return g(am)
for _ in range(300):
    cs = random.sample(range(1, 9), random.randint(1, 4)); am = random.randint(0, 14)
    assert ways_ordered(cs, am) == compositions(cs, am)
print('amount-outer version == number of ORDERED sequences (checked on 300 seeded cases)')

print('coins [1, 2, 5], amount 11: combinations =', ways_combinations([1, 2, 5], 11), '(Q6 asks the min coins, 3, for the same input)')

# edge and large cases
assert ways_combinations([10], 0) == 1 and ways_combinations([7], 5) == 0 and ways_combinations([1], 5000) == 1
big_coins = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
big = ways_combinations(big_coins, 5000)
print('12 coins, amount 5000 ->', big, '(an exact big integer, no modulus)')
try:
    by_index_memo([1, 2, 5], 5000)
    print('memoised by-index amount 5000: ok')
except RecursionError:
    print('memoised by-index amount 5000: RecursionError (default limit', sys.getrecursionlimit(), ')')
print('memoised by-index amount 300 ->', by_index_memo([1, 2, 5], 300), '== bottom-up', ways_combinations([1, 2, 5], 300))
```

**Output (my run):**
```
4 prompt examples ok
coins [1, 2, 5], amount 5: dp[0..5] after each coin
  start        [1, 0, 0, 0, 0, 0]
  after coin 1: [1, 1, 1, 1, 1, 1]
  after coin 2: [1, 1, 2, 2, 3, 3]
  after coin 5: [1, 1, 2, 2, 3, 4]
  ordered (amount-outer) answer for the same input: 9 (compositions, not multisets)
1000 seeded random (<= 4 coins in 1..8, amount 0..14): DP == index recursion == itertools enumeration; coin order irrelevant
swapped loop order (amount outer) differs from the combination count on 219 of 600 seeded cases
amount-outer version == number of ORDERED sequences (checked on 300 seeded cases)
coins [1, 2, 5], amount 11: combinations = 11 (Q6 asks the min coins, 3, for the same input)
12 coins, amount 5000 -> 23303034594533 (an exact big integer, no modulus)
memoised by-index amount 5000: RecursionError (default limit 1000 )
memoised by-index amount 300 -> 4621 == bottom-up 4621
```

**Edge cases:**
- `amount = 0` returns 1 for any coins (`[10]`, 0 -> 1).
- Impossible amount (`[2]`, 3) returns 0, not -1.
- A coin larger than the amount never enters the inner loop (its range is empty).
- Coin order in the list does not change the count (checked by shuffling).

**Follow-ups:**
- Count ordered sequences (combination sum IV)? Swap the loops: amount outer, coin inner.
- Each coin used at most once (0/1 version)? Iterate amounts downward, as in the 0/1 knapsack.
- Need an answer modulo 10^9 + 7? Reduce at each addition.

**Common mistakes:**
- Amount as the outer loop, which counts ordered sequences (9 instead of 4 on the first example).
- `dp[0] = 0`, which makes everything 0.
- Inner loop running downward, which allows each coin only once.
- Memoised recursion at amount 5000 hitting RecursionError.

### Q11 ⭐⭐⭐ 🟡 Partition equal subset sum. `nums` has 1 <= len <= 200 positive integers (each <= 100). Return True if the list can be split into two groups with equal sums, else False. Reduce it to subset sum with target total/2 (False at once if the total is odd) and give both the boolean table and the Python big-int bitset trick `bits |= bits << x`. Say why iterating the capacity downward matters in the 1D table. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12) on small inputs. Example: nums=[1, 5, 11, 5] -> True; nums=[1, 2, 3, 5] -> False; nums=[2] -> False; nums=[3, 3] -> True.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Subset sum on a 1D boolean table (0/1 knapsack, decision form). Two equal halves means one half sums to total/2.

**Say this first (1 line):** "If the total is odd, answer False. Otherwise I ask: can some subset reach total/2? That is a boolean 0/1 knapsack, and the capacity loop must go downward."

**Brute force:** Try all 2^n subsets and test 2 * sum == total. Fine for n <= 12 (the oracle), hopeless for n = 200.

**Optimal:**
- State: `dp[t]` = True if some subset of the items seen so far sums to exactly t. Size total/2 + 1.
- Base: `dp[0] = True` (the empty subset).
- Transition for item x: `dp[t] = dp[t] or dp[t - x]`, for t from target down to x.
- Why downward: `dp[t - x]` must still mean "before this item". Going upward, `dp[t - x]` may already have used x, so one item is counted many times. Example `[1, 5]`: total 6, target 3. Upward says True (1+1+1). Truth is False.
- Bitset: bit t of a Python int means "sum t reachable". `bits |= bits << x` does the whole row in one big-int operation, and the shift reads the old `bits` first, so it is naturally "downward". Answer is bit total/2.
- Top-down (memoised): `go(i, rem)`; depth is len(nums) <= 200, so the default recursion limit of 1000 is safe here. (At large n, memoised recursion raises RecursionError; see Q12.)
- Space: 1D table is O(total/2); the 2D table (item x sum) is not needed.

**Complexity:** Table: O(n * total/2) time, O(total/2) space. Max size: 200 items, total <= 20000, so about 2 million cell updates. Bitset: n shift-or operations on an integer of up to total bits, so about n * total / 64 word operations in theory.

**Dry run:** `[1, 5, 11, 5]`, total 22, target 11 (T = reachable, columns t = 0..11).
| after | row |
|---|---|
| start | `T...........` |
| item 1 | `TT..........` |
| item 5 | `TT...TT.....` |
| item 11 | `TT...TT....T` |
| item 5 | `TT...TT...TT` |
- dp[11] is True after item 11 (0 + 11). The other split is 1 + 5 + 5 = 11.

**Code:**
```python
import random
from functools import lru_cache

random.seed(11)

def can_partition(nums):
    """Optimal: boolean 1D table, capacity looped DOWNWARD. O(n * total/2) time, O(total/2) space."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target            # dp[t]: some subset of the items seen so far sums to t
    for x in nums:
        for t in range(target, x - 1, -1):     # downward: dp[t - x] is still the value from BEFORE this item
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def can_partition_bits(nums):
    """Bitset: bit t of `bits` is set when sum t is reachable. One shift-or per item."""
    total = sum(nums)
    if total % 2:
        return False
    bits = 1
    for x in nums:
        bits |= bits << x
    return bool(bits >> (total // 2) & 1)

def can_partition_memo(nums):
    """Top-down: depth is len(nums) (<= 200 here), so the default recursion limit is fine for this one."""
    total = sum(nums)
    if total % 2:
        return False
    @lru_cache(maxsize=None)
    def go(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return go(i + 1, rem - nums[i]) or go(i + 1, rem)
    return go(0, total // 2)

def can_partition_upward_bug(nums):
    """Same table, capacity loop UPWARD: an item can be reused, so it answers a different question."""
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for t in range(x, target + 1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def brute(nums):
    """Oracle: enumerate every subset, test 2 * sum == total."""
    n, total = len(nums), sum(nums)
    return any(2 * sum(nums[i] for i in range(n) if m >> i & 1) == total for m in range(1 << n))

# prompt examples
for nums, want in [([1, 5, 11, 5], True), ([1, 2, 3, 5], False), ([2], False), ([3, 3], True)]:
    assert can_partition(nums) is want and can_partition_bits(nums) is want and can_partition_memo(nums) is want and brute(nums) is want
print('4 prompt examples ok')

# table walk-through on the first example: total 22, target 11
nums = [1, 5, 11, 5]
target = sum(nums) // 2
dp = [True] + [False] * target
print('target =', target, '  columns t = 0..%d' % target)
print('start    ', ''.join('T' if v else '.' for v in dp))
for x in nums:
    for t in range(target, x - 1, -1):
        if dp[t - x]:
            dp[t] = True
    print('item %-4d' % x, ''.join('T' if v else '.' for v in dp))
bits = 1
for x in [1, 5, 11, 5]:
    bits |= bits << x
    print('bitset after item %-3d (bit 0 on the right): %s' % (x, bin(bits)[2:]))

# why DOWNWARD: [1, 5] has total 6, target 3, and no subset sums to 3
print('nums=[1, 5]: correct', can_partition([1, 5]), ' upward-loop', can_partition_upward_bug([1, 5]), ' (the upward loop used the 1 three times)')

# seeded cross-check against subset enumeration (len <= 12)
trues = 0
wrong_upward = 0
for _ in range(600):
    nums = [random.randint(1, 12) for _ in range(random.randint(1, 12))]
    b = brute(nums)
    assert can_partition(nums) == b == can_partition_bits(nums) == can_partition_memo(nums), nums
    trues += b
    wrong_upward += can_partition_upward_bug(nums) != b
print('600 random cases agree (table = bitset = memo = enumeration); True in', trues, 'of them; upward-loop bug wrong in', wrong_upward)

# edge cases
assert can_partition([1]) is False and can_partition([1, 1]) is True and can_partition([100] * 200) is True
assert can_partition([100] * 199 + [99]) is False          # odd total
assert can_partition_bits([100] * 200) is True
big = [random.randint(1, 100) for _ in range(200)]
assert can_partition(big) == can_partition_bits(big) == can_partition_memo(big)
print('edge cases ok; max-size random input ->', can_partition(big))
```

**Output (my run):**
```
4 prompt examples ok
target = 11   columns t = 0..11
start     T...........
item 1    TT..........
item 5    TT...TT.....
item 11   TT...TT....T
item 5    TT...TT...TT
bitset after item 1   (bit 0 on the right): 11
bitset after item 5   (bit 0 on the right): 1100011
bitset after item 11  (bit 0 on the right): 110001100001100011
bitset after item 5   (bit 0 on the right): 11000110001110001100011
nums=[1, 5]: correct False  upward-loop True  (the upward loop used the 1 three times)
600 random cases agree (table = bitset = memo = enumeration); True in 202 of them; upward-loop bug wrong in 46
edge cases ok; max-size random input -> True
```

**Edge cases:**
- Odd total: False at once.
- Single item: False (total/2 is not reachable), `[3, 3]` True.
- All items bigger than target: the inner loop does nothing; the answer comes from the initial state.
- 200 items of 100: target 10000, works, bitset has 20001 bits.

**Follow-ups:**
- Print the split? Keep the 2D table (or parent pointers) and walk back, or see the reconstruction in Q37.
- Faster? Bitset: Python's big-int shift is C-speed. Complexity in theory O(n * total / 64).
- Min difference of two groups? Same table; scan the reachable sums nearest to total/2 (Q30).

**Common mistakes:**
- Upward capacity loop (reuses an item).
- Forgetting the odd-total shortcut.
- Using `bits << x` into a new variable and then discarding it.
- Putting the whole total, not total/2, as the table size (wastes time, not wrong).

### Q12 ⭐⭐⭐ 🟡 House robber II (circular street). `nums` has 1 <= len <= 10^5 non-negative integers (each <= 400) arranged in a circle, so the first and last houses are adjacent (a single house is just itself). You cannot take two adjacent houses; return the maximum total. Reduce it to two linear problems and say which two ranges, and why every valid choice is covered. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a subset enumeration with the circular no-two-adjacent rule (len <= 12) on small inputs. Example: nums=[2, 3, 2] -> 3; nums=[1, 2, 3, 1] -> 4; nums=[7] -> 7; nums=[5, 1] -> 5; nums=[4, 1, 1, 4] -> 5.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Linear house robber (1D DP) run twice, because a circle breaks the problem into two lines.

**Say this first (1 line):** "In a circle, house 0 and house n-1 are neighbours, so I never take both. I solve two linear problems, houses 0..n-2 and houses 1..n-1, and take the max."

**Brute force:** Enumerate all 2^n subsets, reject any with two circular neighbours. Fine up to n = 12 (the oracle).

**Optimal:**
- Linear state: `best[i]` = best total using houses 0..i. Transition: `best[i] = max(best[i-1], best[i-2] + nums[i])` (skip i, or take i and skip i-1). Base: `best[-1] = best[-2] = 0`.
- Circular: answer = max(rob_line(nums[:-1]), rob_line(nums[1:])). Single house: return it (the two ranges would be empty).
- Why it covers everything: a valid circular selection cannot contain both house 0 and house n-1, so it lies inside one of the two ranges. Conversely, any linear-valid choice inside a range is circular-valid, because each range excludes one of the two end houses. So the max of the two is exactly the circular answer. I checked n = 2..12 exhaustively.
- Bottom-up with two variables: O(1) space.
- Recursion limit: the memoised top-down `best(i)` nests about n deep. At n = 10^5 it raises RecursionError under the default limit of 1000. Bottom-up is required.

**Complexity:** Time O(n) (two passes). Space O(1) for the bottom-up version (slices cost O(n), use index bounds to avoid them).

**Dry run:** `[2, 3, 2]`.
- Range A = houses 0..1 = `[2, 3]`: best = `[2, 3]`, so 3.
- Range B = houses 1..2 = `[3, 2]`: best = `[3, 3]`, so 3.
- Answer max(3, 3) = 3. The linear answer on all three would be 4 (2 + 2), which takes both ends: illegal on a circle.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(12)

def rob_line(nums):
    """Linear house robber, bottom-up, O(1) space: best[i] = max(best[i-1], best[i-2] + nums[i])."""
    prev2, prev1 = 0, 0                 # best for the prefixes of length i-2 and i-1
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def rob_circle(nums):
    """Circular: house 0 and house n-1 are neighbours, so one of them is skipped. Try both ranges."""
    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[:-1]), rob_line(nums[1:]))

def rob_circle_memo(nums):
    """Top-down version of the same thing. Fine for small n; nests ~n deep, so it breaks past the recursion limit."""
    def solve(arr):
        @lru_cache(maxsize=None)
        def best(i):                    # best total using houses 0..i of arr
            if i < 0:
                return 0
            return max(best(i - 1), best(i - 2) + arr[i])
        return best(len(arr) - 1)
    if len(nums) == 1:
        return nums[0]
    return max(solve(tuple(nums[:-1])), solve(tuple(nums[1:])))

def brute(nums):
    """Oracle: every subset, valid only if no two chosen houses are neighbours around the circle."""
    n, best = len(nums), 0
    for mask in range(1 << n):
        if n > 1 and any(mask >> i & 1 and mask >> ((i + 1) % n) & 1 for i in range(n) if (i + 1) % n != i):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best

for nums, want in [([2, 3, 2], 3), ([1, 2, 3, 1], 4), ([7], 7), ([5, 1], 5), ([4, 1, 1, 4], 5)]:
    assert rob_circle(nums) == rob_circle_memo(nums) == brute(nums) == want, nums
print('5 prompt examples ok')

# table walk-through on [2, 3, 2]: range A = houses 0..1 = [2, 3], range B = houses 1..2 = [3, 2]
def table(arr):
    best = []
    for i, x in enumerate(arr):
        best.append(max(best[i - 1] if i >= 1 else 0, (best[i - 2] if i >= 2 else 0) + x))
    return best
nums = [2, 3, 2]
print('range A nums[:-1] =', nums[:-1], 'best =', table(nums[:-1]))
print('range B nums[1:]  =', nums[1:], 'best =', table(nums[1:]))
print('answer = max(%d, %d) = %d' % (table(nums[:-1])[-1], table(nums[1:])[-1], rob_circle(nums)))
print('the (wrong) line answer 2+2 on [2,3,2] would be', rob_line(nums), '- it takes both ends, which are neighbours in a circle')

# claim: every valid circular choice skips house 0 or skips house n-1 (so the two ranges cover everything)
for n in range(2, 13):
    for mask in range(1 << n):
        valid = all(not (mask >> i & 1 and mask >> ((i + 1) % n) & 1) for i in range(n))
        if valid:
            assert not (mask & 1 and mask >> (n - 1) & 1)
print('claim checked for n = 2..12: no valid circular selection holds both house 0 and house n-1')

# exhaustive: every list of length 1..6 with values 0..3
count = 0
for n in range(1, 7):
    for nums in itertools.product(range(4), repeat=n):
        assert rob_circle(list(nums)) == brute(list(nums)), nums
        count += 1
print('exhaustive small inputs agree:', count)

# seeded random cross-check, len <= 12
for _ in range(500):
    nums = [random.randint(0, 400) for _ in range(random.randint(1, 12))]
    assert rob_circle(nums) == rob_circle_memo(nums) == brute(nums), nums
print('500 random cases agree (bottom-up = memo = subset enumeration)')

# recursion limit: memoised top-down at large n
big = [random.randint(0, 400) for _ in range(10**5)]
try:
    rob_circle_memo(big)
    print('memo at n=10^5: no error (unexpected)')
except RecursionError:
    print('memo at n=10^5: RecursionError under the default limit')
print('bottom-up at n=10^5 ->', rob_circle(big))

# edge cases
assert rob_circle([0]) == 0 and rob_circle([0, 0]) == 0 and rob_circle([9, 9, 9]) == 9
assert rob_circle([1, 2, 3, 4, 5, 6]) == brute([1, 2, 3, 4, 5, 6]) == 12
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
range A nums[:-1] = [2, 3] best = [2, 3]
range B nums[1:]  = [3, 2] best = [3, 3]
answer = max(3, 3) = 3
the (wrong) line answer 2+2 on [2,3,2] would be 4 - it takes both ends, which are neighbours in a circle
claim checked for n = 2..12: no valid circular selection holds both house 0 and house n-1
exhaustive small inputs agree: 5460
500 random cases agree (bottom-up = memo = subset enumeration)
memo at n=10^5: RecursionError under the default limit
bottom-up at n=10^5 -> 11717802
edge cases ok
```

**Edge cases:**
- One house: itself. Two houses: the larger one (each range is one house).
- All zeros: 0.
- n = 10^5: bottom-up is fine, memo raises RecursionError.

**Follow-ups:**
- Tree-shaped street? That is House Robber III, Part 7 Q45.
- Return which houses? Keep `best` as a list and walk back in the winning range.
- Why not "rob_line(nums) minus something"? You cannot patch a line answer; rerun on the two ranges.

**Common mistakes:**
- Forgetting the single-house case (both slices are empty, answer 0).
- Taking `max(nums[0], ...)` hacks instead of two clean ranges.
- Relying on `sys.setrecursionlimit` for n = 10^5 (can crash the interpreter).

### Q13 ⭐⭐⭐ 🟡 Maximum product subarray. `nums` has 1 <= len <= 2*10^4 integers (|value| <= 10, zeros and negatives allowed). Return the largest product of a non-empty contiguous subarray (Python integers do not overflow). Keep both the maximum and the minimum product ending at each index and say why the minimum is needed (a negative number flips them) and what a zero does. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every subarray on small inputs. Example: nums=[2, 3, -2, 4] -> 6; nums=[-2, 0, -1] -> 0; nums=[-3] -> -3; nums=[-2, 3, -4] -> 24; nums=[0, 2] -> 2.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Kadane-style 1D DP with two states (max and min product ending at i).

**Say this first (1 line):** "A negative number flips max and min, so I keep both the largest and smallest product of a subarray ending at i. A zero resets them."

**Brute force:** For every start, extend with a running product and track the best. O(n^2) time, O(1) space. It is the oracle.

**Optimal:**
- State: `hi[i]` / `lo[i]` = max / min product of a subarray that ends exactly at i.
- Transition: candidates are `x` (start fresh), `hi[i-1] * x`, `lo[i-1] * x`. Then `hi = max(cands)`, `lo = min(cands)`.
- Why the min: a big negative `lo` times a negative x becomes the new max. Max-only fails on `[-2, 3, -4]` (gives 3, truth 24); over all lists of length <= 6 with values -3..3 the max-only version was wrong on 76246 of 137256.
- Zero: candidates are 0, 0, 0 so hi = lo = 0, and the next element starts fresh via the candidate `x`.
- Base: `hi = lo = best = nums[0]` (non-empty subarray, so all-negative lists return the least negative number).
- Python ints do not overflow (the 2*10^4-element answer has 81 digits here).
- Memoised version: `ending(i)` nests n deep; at n = 2*10^4 it raises RecursionError under the default limit. Bottom-up is required.

**Complexity:** O(n) time, O(1) space.

**Dry run:** `[2, 3, -2, 4]`.
| i | x | max_end | min_end | best |
|---|---|---|---|---|
| 0 | 2 | 2 | 2 | 2 |
| 1 | 3 | 6 | 3 | 6 |
| 2 | -2 | -2 | -12 | 6 |
| 3 | 4 | 4 | -48 | 6 |
- At i=2 the old max 6 times -2 is -12, which becomes the min; the max is just -2 (fresh start).
- Zero trace `[-2, 0, -1]`: both states become 0 at the zero, best stays 0.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(13)

def max_product(nums):
    """Optimal: keep the max AND min product of a subarray ending here. O(n) time, O(1) space."""
    best = hi = lo = nums[0]
    for x in nums[1:]:
        cands = (x, hi * x, lo * x)      # start fresh at x, or extend the old max / old min
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best

def max_product_no_min(nums):
    """The tempting bug: track only the maximum."""
    best = hi = nums[0]
    for x in nums[1:]:
        hi = max(x, hi * x)
        best = max(best, hi)
    return best

def max_product_memo(nums):
    """Top-down: (max, min) ending at i. Nests n deep."""
    @lru_cache(maxsize=None)
    def ending(i):
        if i == 0:
            return nums[0], nums[0]
        hi, lo = ending(i - 1)
        c = (nums[i], hi * nums[i], lo * nums[i])
        return max(c), min(c)
    ending(len(nums) - 1)                # ask for the LAST index first: the recursion goes n deep
    return max(ending(i)[0] for i in range(len(nums)))

def brute(nums):
    """Oracle: every subarray, O(n^2) with a running product."""
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best

for nums, want in [([2, 3, -2, 4], 6), ([-2, 0, -1], 0), ([-3], -3), ([-2, 3, -4], 24), ([0, 2], 2)]:
    assert max_product(nums) == max_product_memo(nums) == brute(nums) == want, nums
print('5 prompt examples ok')

# table walk-through on [2, 3, -2, 4]
nums = [2, 3, -2, 4]
print('i  x   max_end  min_end  best')
best = hi = lo = nums[0]
print('0  %-3d %-8d %-8d %d' % (nums[0], hi, lo, best))
for i in range(1, len(nums)):
    x = nums[i]
    c = (x, hi * x, lo * x)
    hi, lo = max(c), min(c)
    best = max(best, hi)
    print('%d  %-3d %-8d %-8d %d' % (i, x, hi, lo, best))
print('zero resets both: trace on [-2, 0, -1]')
hi = lo = best = -2
print('  i=0 x=-2 max_end=-2 min_end=-2')
for i, x in enumerate([0, -1], start=1):
    c = (x, hi * x, lo * x)
    hi, lo = max(c), min(c)
    best = max(best, hi)
    print('  i=%d x=%-2d max_end=%d min_end=%d best=%d' % (i, x, hi, lo, best))
print('[-2, 3, -4]: with min ->', max_product([-2, 3, -4]), ' max-only ->', max_product_no_min([-2, 3, -4]))

# exhaustive: all lists of length 1..6 with values -3..3
count = bad_no_min = 0
for n in range(1, 7):
    for nums in itertools.product(range(-3, 4), repeat=n):
        nums = list(nums)
        assert max_product(nums) == brute(nums), nums
        bad_no_min += max_product_no_min(nums) != brute(nums)
        count += 1
print('exhaustive small inputs agree:', count, '; max-only variant wrong on', bad_no_min)

# seeded random cross-check
for _ in range(500):
    nums = [random.randint(-6, 6) for _ in range(random.randint(1, 12))]
    assert max_product(nums) == max_product_memo(nums) == brute(nums), nums
print('500 random cases agree (bottom-up = memo = O(n^2) enumeration)')

# recursion limit at large n
big = [random.randint(-10, 10) for _ in range(2 * 10**4)]
try:
    max_product_memo(big)
    print('memo at n=2*10^4: no error (unexpected)')
except RecursionError:
    print('memo at n=2*10^4: RecursionError under the default limit')
print('bottom-up at n=2*10^4 has', len(str(max_product(big))), 'digit answer (Python ints do not overflow)')
assert max_product([-1] * 3) == 1 and max_product([0]) == 0 and max_product([-2, -3]) == 6 and max_product([0, 0, -1]) == 0
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
i  x   max_end  min_end  best
0  2   2        2        2
1  3   6        3        6
2  -2  -2       -12      6
3  4   4        -48      6
zero resets both: trace on [-2, 0, -1]
  i=0 x=-2 max_end=-2 min_end=-2
  i=1 x=0  max_end=0 min_end=0 best=0
  i=2 x=-1 max_end=0 min_end=-1 best=0
[-2, 3, -4]: with min -> 24  max-only -> 3
exhaustive small inputs agree: 137256 ; max-only variant wrong on 76246
500 random cases agree (bottom-up = memo = O(n^2) enumeration)
memo at n=2*10^4: RecursionError under the default limit
bottom-up at n=2*10^4 has 81 digit answer (Python ints do not overflow)
edge cases ok
```

**Edge cases:**
- Single negative: itself. Single zero: 0.
- Two negatives: product positive (`[-2, -3]` -> 6).
- Zeros split the array into independent segments.

**Follow-ups:**
- Why not prefix products? Zeros and sign flips break division; the two-state DP avoids it.
- Max sum instead? That is Kadane (Q3).
- Circular? Not defined for products in the usual form; the sum version is Q26.

**Common mistakes:**
- Overwriting `hi` before computing `lo` from the old `hi` (use a tuple of candidates).
- Initialising `best = 0` (wrong for all-negative lists).
- Max-only tracking.

### Q14 ⭐⭐ 🟢 Fibonacci three ways: plain recursion, memoisation, bottom-up. Define fib(0) = 0, fib(1) = 1, fib(k) = fib(k-1) + fib(k-2), for 0 <= n <= 25. Return `[fib(n), naive_calls, memo_calls]` where `naive_calls` is the number of calls (counting the first) made by the plain recursive function, and `memo_calls` is the number of calls (counting the first and the ones answered from the cache) made by this memoised function: `def fib(k): count += 1; if k < 2: return k; if k in memo: return memo[k]; memo[k] = fib(k-1) + fib(k-2); return memo[k]` (the check of memo happens after the base case). Then explain the O(1)-space bottom-up loop and why naive calls grow exponentially while memo calls grow linearly. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against the counted recursive functions themselves (n <= 20) on small inputs. Example: n=0 -> [0, 1, 1]; n=1 -> [1, 1, 1]; n=2 -> [1, 3, 3]; n=10 -> [55, 177, 19]; n=25 -> [75025, 242785, 49].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Overlapping subproblems made visible: plain recursion versus memoisation versus bottom-up.

**Say this first (1 line):** "Plain recursion recomputes the same fib(k) exponentially often; a cache makes it linear; a two-variable loop makes it linear with O(1) space."

**Brute force:** The plain recursive function `fib(k-1) + fib(k-2)`. Calls: c(0) = c(1) = 1, c(k) = 1 + c(k-1) + c(k-2). This equals 2*fib(k+1) - 1 (checked for k = 0..25), and grows by the golden ratio 1.618 per step: exponential.

**Optimal:**
- Memoised function from the prompt (base case checked first, then the cache). Count: m(0) = m(1) = 1. For k >= 2 the call does one call chain for k-1 (which fills the cache down to the bottom) and then one call for k-2, which is answered from the cache or is a base case: m(k) = m(k-1) + 2, so m(n) = 2n - 1 for n >= 1.
- Bottom-up: `a, b = 0, 1; repeat n times: a, b = b, a + b`. O(n) time, O(1) space, no recursion.
- Recursion limit: the memoised version is O(n) calls but also n deep. At n = 5000 it raises RecursionError under the default limit; bottom-up does not.
- The answer is `[fib(n), naive_calls, memo_calls]`; I get naive_calls from its recurrence and memo_calls from 2n - 1, and the cross-check runs the actual counted functions.

**Complexity:** My function: O(n) time, O(1) space. The plain recursion is O(phi^n) time, O(n) stack. The memo is O(n) time and O(n) space (cache and stack).

**Dry run:** n = 0: one call, base case: `[0, 1, 1]`. n = 2: fib(2) calls fib(1) and fib(0), both base: 3 calls either way. n = 4: naive 9 calls (fib(2) is computed twice, fib(1) three times), memo 7. The table in the output shows k = 0..10, ending `55, 177, 19`.

**Code:**
```python
import random

random.seed(14)

def fib_three(n):
    """Optimal: bottom-up for the value (O(1) space) and recurrences for the two call counts."""
    a, b = 0, 1                       # fib(0), fib(1)
    for _ in range(n):
        a, b = b, a + b
    # naive calls: c(0) = c(1) = 1, c(k) = 1 + c(k-1) + c(k-2)
    c_prev, c_cur = 1, 1
    for _ in range(n - 1):
        c_prev, c_cur = c_cur, 1 + c_prev + c_cur
    naive = 1 if n < 2 else c_cur
    # memo calls: the first call is 1; each new k >= 2 makes two child calls; derived below, equals 2n - 1 for n >= 1
    memo = 1 if n == 0 else 2 * n - 1
    return [a, naive, memo]

def counted_recursions(n):
    """Oracle: run the two functions from the prompt and count their calls."""
    count = [0]
    def naive(k):
        count[0] += 1
        return k if k < 2 else naive(k - 1) + naive(k - 2)
    value = naive(n)
    naive_calls = count[0]
    count[0] = 0
    memo = {}
    def memoised(k):
        count[0] += 1
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = memoised(k - 1) + memoised(k - 2)
        return memo[k]
    assert memoised(n) == value
    return [value, naive_calls, count[0]]

for n, want in [(0, [0, 1, 1]), (1, [1, 1, 1]), (2, [1, 3, 3]), (10, [55, 177, 19]), (25, [75025, 242785, 49])]:
    assert fib_three(n) == want, n
    assert counted_recursions(n) == want, n
print('5 prompt examples ok')

# walk-through: n = 2 (first call fib(2) -> fib(1), fib(0))
print('n=2 naive: fib(2) -> fib(1) base, fib(0) base = 3 calls; memo: same 3 calls, nothing cached yet')
# and n = 5 call table
print('k   fib(k)  naive_calls  memo_calls')
for k in range(0, 11):
    v, nv, mm = fib_three(k)
    print('%-3d %-7d %-12d %d' % (k, v, nv, mm))

# growth: naive ratio tends to the golden ratio, memo grows by 2 per step
ratios = [fib_three(k)[1] / fib_three(k - 1)[1] for k in (10, 20, 25)]
print('naive_calls(k)/naive_calls(k-1) at k=10,20,25:', [round(r, 4) for r in ratios], '(golden ratio 1.6180)')
print('naive_calls(k) = 2*fib(k+1) - 1 ?', all(fib_three(k)[1] == 2 * fib_three(k + 1)[0] - 1 for k in range(0, 26)))

# seeded random cross-check, n <= 20, plus every n
for n in range(0, 21):
    assert fib_three(n) == counted_recursions(n), n
for _ in range(300):
    n = random.randint(0, 20)
    assert fib_three(n) == counted_recursions(n)
print('all n in 0..20 and 300 random draws agree with the counted recursive functions')

# recursion limit: the memoised function is O(n) calls but also O(n) DEEP
def deep_memo(n):
    memo = {}
    def f(k):
        if k < 2:
            return k
        if k in memo:
            return memo[k]
        memo[k] = f(k - 1) + f(k - 2)
        return memo[k]
    return f(n)
try:
    deep_memo(5000)
    print('memo fib(5000): no error (unexpected)')
except RecursionError:
    print('memo fib(5000): RecursionError under the default limit; bottom-up gives', len(str(fib_three(5000)[0])), 'digits')
assert fib_three(0)[0] == 0 and fib_three(1)[0] == 1
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
n=2 naive: fib(2) -> fib(1) base, fib(0) base = 3 calls; memo: same 3 calls, nothing cached yet
k   fib(k)  naive_calls  memo_calls
0   0       1            1
1   1       1            1
2   1       3            3
3   2       5            5
4   3       9            7
5   5       15           9
6   8       25           11
7   13      41           13
8   21      67           15
9   34      109          17
10  55      177          19
naive_calls(k)/naive_calls(k-1) at k=10,20,25: [1.6239, 1.6181, 1.618] (golden ratio 1.6180)
naive_calls(k) = 2*fib(k+1) - 1 ? True
all n in 0..20 and 300 random draws agree with the counted recursive functions
memo fib(5000): RecursionError under the default limit; bottom-up gives 1045 digits
edge cases ok
```

**Edge cases:**
- n = 0 and n = 1: one call each.
- n = 25: 242785 naive calls versus 49 memo calls.
- Large n: Python ints are exact (fib(5000) has 1045 digits).

**Follow-ups:**
- Faster than O(n)? Matrix power or fast doubling gives O(log n) big-int steps.
- Modulo? Reduce each addition.
- Climbing stairs (Q1) is the same recurrence shifted by one.

**Common mistakes:**
- Checking the cache before the base case (changes the call count by the prompt's definition).
- Forgetting the first call in the count.
- Claiming memoisation is O(1) space: it is O(n).

### Q15 ⭐⭐ 🟡 Paint fence (counting with a modulus). There are `n` posts (1 <= n <= 10^5) and `k` colours (1 <= k <= 10^9). Paint every post so that no three consecutive posts share a colour. Return the number of ways modulo 10^9 + 7. Use the two states 'last two posts the same' and 'last two posts different'. State the answer for k = 1 (1 for n = 1 or 2, else 0). Say where the modulus is applied (after every multiplication and addition) and why you may not take the modulus of the inputs mid-way in a comparison. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all colourings (n <= 7, k <= 4) on small inputs. Example: n=1, k=5 -> 5; n=3, k=2 -> 6; n=7, k=2 -> 42; n=3, k=1 -> 0; n=100000, k=1000000000 -> 910929812.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Counting DP with two states (same as previous, different from previous), modulus.

**Say this first (1 line):** "At each post the last two are either the same or different; same can only follow different, and different has k-1 choices after anything."

**Brute force:** Enumerate all k^n colourings and reject any with three equal in a row (n <= 7, k <= 4 here).

**Optimal:**
- State: `same[i]` = ways for posts 1..i where posts i and i-1 share a colour; `diff[i]` = ways where they differ.
- Base: post 1: `same = 0`, `diff = k`.
- Transition: `same[i] = diff[i-1]` (copy the previous colour; allowed only if i-1 and i-2 differed, else three in a row). `diff[i] = (same[i-1] + diff[i-1]) * (k - 1)`.
- Answer: `same[n] + diff[n]`, modulo 10^9+7.
- k = 1 falls out of the recurrence: n = 1 -> 1, n = 2 -> 1, n >= 3 -> 0.
- One-state form: `total[i] = (k-1) * (total[i-1] + total[i-2])`; I checked it agrees.
- Modulus: reduce after every multiplication and addition (the exact count has about 30 bits more per post: 59795 bits at n = 2000). Use reduced numbers only inside arithmetic. Never use a reduced value in a comparison or ordering (a count of M+5 reduces to 5).
- Recursion limit: top-down `go(i)` nests n deep; at n = 10^5 it raises RecursionError. Bottom-up is required.

**Complexity:** O(n) time, O(1) space.

**Dry run:** n = 3, k = 2.
| post | same | diff | total |
|---|---|---|---|
| 1 | 0 | 2 | 2 |
| 2 | 2 | 2 | 4 |
| 3 | 2 | 4 | 6 |
- Total 6 = 8 colourings minus AAA and BBB.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(15)
M = 10**9 + 7

def paint_fence(n, k):
    """Optimal: two states per post. O(n) time, O(1) space, modulus after every product/sum."""
    same, diff = 0, k                 # post 1: it cannot be 'same as previous'; k choices, all 'different'
    for _ in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1) % M
        # same[i] = diff[i-1]            (copy the colour of post i-1, allowed only if i-1 and i-2 differed)
        # diff[i] = total[i-1] * (k-1)   (pick any colour except the previous post's)
    return (same + diff) % M

def paint_fence_memo(n, k):
    """Top-down, same recurrence. Nests n deep."""
    @lru_cache(maxsize=None)
    def go(i):                        # returns (same, diff) for posts 1..i
        if i == 1:
            return 0, k % M
        same, diff = go(i - 1)
        return diff, (same + diff) * (k - 1) % M
    s, d = go(n)
    return (s + d) % M

def brute(n, k):
    """Oracle: enumerate all k^n colourings and reject three equal in a row."""
    c = 0
    for col in itertools.product(range(k), repeat=n):
        if all(not (col[i] == col[i + 1] == col[i + 2]) for i in range(n - 2)):
            c += 1
    return c % M

for (n, k), want in [((1, 5), 5), ((3, 2), 6), ((7, 2), 42), ((3, 1), 0), ((100000, 10**9), 910929812)]:
    assert paint_fence(n, k) == want, (n, k)
    if n <= 7:
        assert brute(n, k) == want
print('5 prompt examples ok')

# table walk-through on n=1,k=5 and n=3,k=2
def rows(n, k):
    same, diff = 0, k
    out = [(1, same, diff, same + diff)]
    for i in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
        out.append((i, same, diff, same + diff))
    return out
print('n=3, k=2 (no modulus needed at this size)')
print('post  same  diff  total')
for r in rows(3, 2):
    print('%-5d %-5d %-5d %d' % r)
print('n=1, k=5 -> total', rows(1, 5)[0][3], '(just k)')

# k = 1: 1 for n = 1 or 2, then 0
print('k=1, n=1..5 ->', [paint_fence(n, 1) for n in range(1, 6)])

# exhaustive over n <= 7, k <= 4, all three methods
count = 0
for n in range(1, 8):
    for k in range(1, 5):
        assert paint_fence(n, k) == paint_fence_memo(n, k) == brute(n, k), (n, k)
        count += 1
print('exhaustive n<=7, k<=4:', count, 'cases agree (bottom-up = memo = enumeration)')
for _ in range(200):
    n, k = random.randint(1, 7), random.randint(1, 4)
    assert paint_fence(n, k) == brute(n, k)

# alternative one-state recurrence: total[i] = (k-1) * (total[i-1] + total[i-2])
def alt(n, k):
    t1, t2 = k, k * k
    if n == 1:
        return t1 % M
    for _ in range(3, n + 1):
        t1, t2 = t2, (k - 1) * (t1 + t2) % M
    return t2 % M
assert all(alt(n, k) == paint_fence(n, k) for n in range(1, 40) for k in (1, 2, 3, 10**9))
print('one-state recurrence total[i] = (k-1)*(total[i-1] + total[i-2]) agrees')

# modulus: the exact big-int answer reduced once at the end equals the answer reduced after every step
def exact(n, k):
    same, diff = 0, k
    for _ in range(2, n + 1):
        same, diff = diff, (same + diff) * (k - 1)
    return same + diff
assert exact(2000, 10**9) % M == paint_fence(2000, 10**9)
print('n=2000, k=10^9: exact big int mod M equals the in-loop reduction:', exact(2000, 10**9) % M == paint_fence(2000, 10**9))
print('bits of the exact count at n=2000, k=10^9:', exact(2000, 10**9).bit_length(), '(why we reduce: it grows by about 30 bits per post)')
# the loop has no comparison on reduced values; a reduced number says nothing about order or equality of the true number
print('true value M+5 reduces to', (M + 5) % M, '-> a test like "if count_mod > other_mod" or "if count_mod == 5" would be wrong')

# recursion limit
try:
    paint_fence_memo(10**5, 10**9)
    print('memo at n=10^5: no error (unexpected)')
except RecursionError:
    print('memo at n=10^5: RecursionError under the default limit')
print('bottom-up n=10^5, k=10^9 ->', paint_fence(10**5, 10**9))
assert paint_fence(1, 1) == 1 and paint_fence(2, 1) == 1 and paint_fence(2, 3) == 9
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
n=3, k=2 (no modulus needed at this size)
post  same  diff  total
1     0     2     2
2     2     2     4
3     2     4     6
n=1, k=5 -> total 5 (just k)
k=1, n=1..5 -> [1, 1, 0, 0, 0]
exhaustive n<=7, k<=4: 28 cases agree (bottom-up = memo = enumeration)
one-state recurrence total[i] = (k-1)*(total[i-1] + total[i-2]) agrees
n=2000, k=10^9: exact big int mod M equals the in-loop reduction: True
bits of the exact count at n=2000, k=10^9: 59795 (why we reduce: it grows by about 30 bits per post)
true value M+5 reduces to 5 -> a test like "if count_mod > other_mod" or "if count_mod == 5" would be wrong
memo at n=10^5: RecursionError under the default limit
bottom-up n=10^5, k=10^9 -> 910929812
edge cases ok
```

**Edge cases:**
- n = 1: k. n = 2: k^2 (no rule applies yet).
- k = 1: 1, 1, 0, 0, ...
- n = 10^5, k = 10^9: 910929812.

**Follow-ups:**
- No two adjacent the same? `k * (k-1)^(n-1)`; no DP needed.
- O(log n)? Matrix power of the 2x2 transition.
- Why not three states? Runs of three are forbidden, so run length 1 or 2 is all you track.

**Common mistakes:**
- Starting the loop at post 1 instead of post 2 (n = 1 must return k).
- Missing the `% M` on one of the two operations.
- Letting `same[i]` copy `same[i-1]` too (that allows three equal in a row).

### Q16 ⭐⭐ 🟡 Perfect squares (fewest squares summing to n). Given 1 <= n <= 10^4, return the minimum number of perfect squares (1, 4, 9, ...) that add up to n. Define `dp[i]`, the transition over squares j*j <= i, and the base case. This is coin change (Q6) with the coins 1, 4, 9, ...; state the time (the double loop is about n * sqrt(n) steps). Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion with no memo (n <= 25) on small inputs. Example: n=12 -> 3; n=13 -> 2; n=1 -> 1; n=7 -> 4; n=9999 -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Unbounded min-count DP (coin change, Q6, with the coins 1, 4, 9, ...).

**Say this first (1 line):** "dp[i] is the fewest squares that sum to i; I try every square j*j <= i as the last piece."

**Brute force:** Plain recursion `1 + min(f(m - j*j))` with no cache. Exponential; used as the oracle for n <= 25.

**Optimal:**
- State: `dp[i]` = fewest squares summing to exactly i.
- Base: `dp[0] = 0`.
- Transition: `dp[i] = min(dp[i - j*j] + 1)` over all j with j*j <= i. Every i >= 1 has an answer (1 + 1 + ... uses dp[i-1]).
- Bottom-up in increasing i, so smaller states are done.
- Recursion limit: the memoised version tries j = 1 first, so the first descent is n deep. At n = 10^4 it raises RecursionError under the default limit. Bottom-up is required.
- Facts checked for every n in 1..10^4: the answer is at most 4 (Lagrange), and equals 4 exactly when n = 4^a * (8b + 7) (Legendre). That gives an O(sqrt n) solution but is not needed in an interview.

**Complexity:** About n * sqrt(n) steps: the inner loop runs floor(sqrt(i)) times at i; the exact count at n = 10^4 is 661750 (about (2/3) n^1.5). Space O(n).

**Dry run:** n = 12.
| i | dp[i] | choices |
|---|---|---|
| 4 | 1 | dp[0]+1 |
| 8 | 2 | dp[4]+1 |
| 11 | 3 | dp[10]+1 = 3, dp[2]+1 = 3 |
| 12 | 3 | dp[11]+1 = 4, dp[8]+1 = 3, dp[3]+1 = 4 |
- Answer 3 = 4 + 4 + 4. The full table is in the output.

**Code:**
```python
import random
from functools import lru_cache

random.seed(16)
INF = float('inf')

def perfect_squares(n):
    """Optimal: dp[i] = fewest squares summing to i. Bottom-up, O(n sqrt n) time, O(n) space."""
    dp = [0] + [INF] * n              # dp[0] = 0: the empty sum
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            if dp[i - j * j] + 1 < dp[i]:
                dp[i] = dp[i - j * j] + 1
            j += 1
    return dp[n]

def perfect_squares_memo(n):
    """Top-down: tries j = 1 first, so the first descent goes n deep."""
    @lru_cache(maxsize=None)
    def f(m):
        if m == 0:
            return 0
        return 1 + min(f(m - j * j) for j in range(1, int(m ** 0.5) + 1))
    return f(n)

def brute(n):
    """Oracle: plain recursion, no cache."""
    if n == 0:
        return 0
    return 1 + min(brute(n - j * j) for j in range(1, int(n ** 0.5) + 1))

for n, want in [(12, 3), (13, 2), (1, 1), (7, 4), (9999, 4)]:
    assert perfect_squares(n) == want, n
    if n < 900:
        assert perfect_squares_memo(n) == want
    if n <= 25:
        assert brute(n) == want
print('5 prompt examples ok')

# walk-through, n = 12
dp = [0] + [INF] * 12
print('i   dp[i]  best choice (j*j subtracted)')
print('0   0      base')
for i in range(1, 13):
    cands = [(dp[i - j * j] + 1, j * j) for j in range(1, int(i ** 0.5) + 1)]
    dp[i] = min(c[0] for c in cands)
    print('%-3d %-6d %s' % (i, dp[i], ', '.join('dp[%d]+1=%d' % (i - s, v) for v, s in cands)))
print('dp[12] = 3 : 4 + 4 + 4')

# step count of the double loop at n = 10^4 versus n^2/2 for a plain 1..n coin loop
steps = sum(int(i ** 0.5) for i in range(1, 10**4 + 1))
print('inner-loop steps at n=10^4:', steps, '(about n * sqrt(n) * 2/3 = 666667)')

# seeded cross-check against the plain recursion
for n in range(1, 26):
    assert perfect_squares(n) == brute(n) == perfect_squares_memo(n), n
for _ in range(300):
    n = random.randint(1, 25)
    assert perfect_squares(n) == brute(n)
print('all n in 1..25 and 300 random draws agree with the plain recursion')

# claims: answer never exceeds 4 (Lagrange); 4 exactly when n = 4^a (8b + 7) (Legendre)
def legendre4(n):
    while n % 4 == 0:
        n //= 4
    return n % 8 == 7
dp_all = [0] + [INF] * 10**4
for i in range(1, 10**4 + 1):
    j = 1
    while j * j <= i:
        dp_all[i] = min(dp_all[i], dp_all[i - j * j] + 1)
        j += 1
assert max(dp_all[1:]) == 4
assert all((dp_all[i] == 4) == legendre4(i) for i in range(1, 10**4 + 1))
print('for every n in 1..10^4 the answer is <= 4, and equals 4 exactly when n = 4^a * (8b + 7)')

# recursion limit
try:
    perfect_squares_memo(10**4)
    print('memo at n=10^4: no error (unexpected)')
except RecursionError:
    print('memo at n=10^4: RecursionError under the default limit')
print('bottom-up n=10^4 ->', perfect_squares(10**4))
assert perfect_squares(1) == 1 and perfect_squares(4) == 1 and perfect_squares(2) == 2
print('edge cases ok')
```

**Output (my run):**
```
5 prompt examples ok
i   dp[i]  best choice (j*j subtracted)
0   0      base
1   1      dp[0]+1=1
2   2      dp[1]+1=2
3   3      dp[2]+1=3
4   1      dp[3]+1=4, dp[0]+1=1
5   2      dp[4]+1=2, dp[1]+1=2
6   3      dp[5]+1=3, dp[2]+1=3
7   4      dp[6]+1=4, dp[3]+1=4
8   2      dp[7]+1=5, dp[4]+1=2
9   1      dp[8]+1=3, dp[5]+1=3, dp[0]+1=1
10  2      dp[9]+1=2, dp[6]+1=4, dp[1]+1=2
11  3      dp[10]+1=3, dp[7]+1=5, dp[2]+1=3
12  3      dp[11]+1=4, dp[8]+1=3, dp[3]+1=4
dp[12] = 3 : 4 + 4 + 4
inner-loop steps at n=10^4: 661750 (about n * sqrt(n) * 2/3 = 666667)
all n in 1..25 and 300 random draws agree with the plain recursion
for every n in 1..10^4 the answer is <= 4, and equals 4 exactly when n = 4^a * (8b + 7)
memo at n=10^4: RecursionError under the default limit
bottom-up n=10^4 -> 1
edge cases ok
```

**Edge cases:**
- n = 1: 1. n a perfect square: 1.
- n = 7: 4 (4+1+1+1). n = 9999: 4.
- Greedy "largest square first" fails (n = 12 gives 9+1+1+1 = 4, answer 3).

**Follow-ups:**
- Faster? Four-square theorem plus the three-square test: O(sqrt n).
- BFS version? Levels = number of squares; same answer, O(n sqrt n).
- Coin change? Q6.

**Common mistakes:**
- `dp[0] = INF` or forgetting `dp[0] = 0`.
- Looping j up to `n` instead of `sqrt(i)`.
- Using floats for sqrt with large n (`int(i ** 0.5)` is fine here; `isqrt` is safer).

### Q17 ⭐⭐ 🟡 0/1 knapsack (maximum value). `weights` and `values` are lists of equal length 1 <= len <= 100 (1 <= weight <= 100, 1 <= value <= 1000) and `cap` is the capacity 0 <= cap <= 1000. Each item is used at most once. Return the maximum total value with total weight <= cap (0 if nothing fits). Give the 2D table, then the 1D table that iterates the capacity DOWNWARD, and explain what the upward loop computes instead (it lets an item be reused, so it answers the unbounded problem of Q20). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12) on small inputs. Example: weights=[1, 3, 4, 5], values=[1, 4, 5, 7], cap=7 -> 9; weights=[5], values=[10], cap=4 -> 0; weights=[2, 2, 3], values=[3, 3, 5], cap=4 -> 6; weights=[3, 4], values=[5, 6], cap=0 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** 0/1 knapsack: each item once, maximise value under a weight cap.

**Say this first (1 line):** "dp[c] is the best value with capacity c; for each item I go through capacities from high to low so the item is used at most once."

**Brute force:** Try all 2^n subsets (the oracle, n <= 12); O(2^n * n).

**Optimal:**
- 2D state: `dp[i][c]` = best value from the first i items with capacity c. Base: row 0 all zeros.
- Transition: `dp[i][c] = max(dp[i-1][c], dp[i-1][c - w] + v)` (the second only if c >= w). Skip item i, or take it once on top of the row above.
- 1D: only row i-1 is needed, so keep one row and loop c from cap down to w. Downward, `dp[c - w]` is still the previous row.
- Upward loop: `dp[c - w]` may already contain this item, so it can be taken again. It computes the unbounded knapsack (Q20). Checked on 500 random cases: it equalled the unbounded answer every time and differed from the 0/1 answer in 438 of them. (`weights=[2], values=[5], cap=6`: 0/1 gives 5, upward gives 15.)
- Memoised top-down `go(i, rem)`: depth len(weights) <= 100, safe under the default recursion limit. At large depth it would raise RecursionError.

**Complexity:** Time O(n * cap), space O(n * cap) for 2D, O(cap) for 1D. (Pseudo-polynomial: polynomial in the value of cap, not its bit length.)

**Dry run:** weights `[1, 3, 4, 5]`, values `[1, 4, 5, 7]`, cap 7 (columns 0..7).
| row | values |
|---|---|
| none | 0 0 0 0 0 0 0 0 |
| w1 v1 | 0 1 1 1 1 1 1 1 |
| w3 v4 | 0 1 1 4 5 5 5 5 |
| w4 v5 | 0 1 1 4 5 6 6 9 |
| w5 v7 | 0 1 1 4 5 7 8 9 |
- Answer dp[7] = 9 (weights 3 + 4, values 4 + 5). The 1D row after each item is identical to the matching 2D row.

**Code:**
```python
import random
from functools import lru_cache

random.seed(17)

def knapsack_2d(weights, values, cap):
    """2D table: dp[i][c] = best value using the first i items with capacity c. O(n * cap) time and space."""
    n = len(weights)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]          # row 0: no items, value 0 for every capacity
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(cap + 1):
            dp[i][c] = dp[i - 1][c]                        # skip item i
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)   # take item i once
    return dp

def knapsack_1d(weights, values, cap):
    """Optimal: one row, capacity looped DOWNWARD. O(n * cap) time, O(cap) space."""
    dp = [0] * (cap + 1)                                   # dp[c] = best value with weight <= c
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack_upward(weights, values, cap):
    """The classic bug: capacity looped UPWARD. dp[c - w] may already include this item, so it can be taken again."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def unbounded(weights, values, cap):
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c:
                dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack_memo(weights, values, cap):
    """Top-down: state (i, remaining capacity); depth is len(weights) <= 100, safe under the default limit."""
    @lru_cache(maxsize=None)
    def go(i, rem):
        if i == len(weights):
            return 0
        best = go(i + 1, rem)
        if weights[i] <= rem:
            best = max(best, go(i + 1, rem - weights[i]) + values[i])
        return best
    return go(0, cap)

def brute(weights, values, cap):
    """Oracle: every subset."""
    n, best = len(weights), 0
    for m in range(1 << n):
        if sum(weights[i] for i in range(n) if m >> i & 1) <= cap:
            best = max(best, sum(values[i] for i in range(n) if m >> i & 1))
    return best

for (w, v, c), want in [(([1, 3, 4, 5], [1, 4, 5, 7], 7), 9), (([5], [10], 4), 0), (([2, 2, 3], [3, 3, 5], 4), 6), (([3, 4], [5, 6], 0), 0)]:
    assert knapsack_2d(w, v, c)[-1][c] == knapsack_1d(w, v, c) == knapsack_memo(w, v, c) == brute(w, v, c) == want
print('4 prompt examples ok')

# walk-through on weights=[1,3,4,5], values=[1,4,5,7], cap=7
w, v, cap = [1, 3, 4, 5], [1, 4, 5, 7], 7
print('2D table, columns c = 0..7')
print('no items ', knapsack_2d([], [], cap)[0])
dp2 = knapsack_2d(w, v, cap)
for i in range(1, 5):
    print('item %d (w=%d,v=%d)' % (i, w[i - 1], v[i - 1]), dp2[i])
print('1D table, same final row; each line is the single row after one item (downward loop)')
dp = [0] * (cap + 1)
for wi, vi in zip(w, v):
    for c in range(cap, wi - 1, -1):
        dp[c] = max(dp[c], dp[c - wi] + vi)
    print('after w=%d' % wi, dp)
assert dp == dp2[-1]
print('answer', dp[cap], '= items weight 3 + 4 (values 4 + 5)')

# what the upward loop computes: a different problem
print('upward loop on the same input:', knapsack_upward(w, v, cap), '; unbounded answer:', unbounded(w, v, cap), '; true 0/1 answer:', knapsack_1d(w, v, cap))
print('example where it breaks: one item weight 2, value 5, cap 6 -> 0/1', knapsack_1d([2], [5], 6), 'upward', knapsack_upward([2], [5], 6))

# seeded cross-check against subset enumeration (len <= 12)
diff = 0
for _ in range(500):
    n = random.randint(1, 12)
    w = [random.randint(1, 9) for _ in range(n)]
    v = [random.randint(1, 30) for _ in range(n)]
    cap = random.randint(0, 40)
    b = brute(w, v, cap)
    assert knapsack_1d(w, v, cap) == knapsack_2d(w, v, cap)[-1][cap] == knapsack_memo(w, v, cap) == b, (w, v, cap)
    assert knapsack_upward(w, v, cap) == unbounded(w, v, cap)
    diff += knapsack_upward(w, v, cap) != b
print('500 random cases agree (1D = 2D = memo = enumeration); upward loop equals the unbounded answer every time and differs from 0/1 in', diff)

# edge cases and max size
assert knapsack_1d([100], [1000], 99) == 0 and knapsack_1d([100], [1000], 100) == 1000
big_w = [random.randint(1, 100) for _ in range(100)]
big_v = [random.randint(1, 1000) for _ in range(100)]
assert knapsack_1d(big_w, big_v, 1000) == knapsack_memo(big_w, big_v, 1000) == knapsack_2d(big_w, big_v, 1000)[-1][1000]
print('edge cases ok; max-size random input ->', knapsack_1d(big_w, big_v, 1000))
```

**Output (my run):**
```
4 prompt examples ok
2D table, columns c = 0..7
no items  [0, 0, 0, 0, 0, 0, 0, 0]
item 1 (w=1,v=1) [0, 1, 1, 1, 1, 1, 1, 1]
item 2 (w=3,v=4) [0, 1, 1, 4, 5, 5, 5, 5]
item 3 (w=4,v=5) [0, 1, 1, 4, 5, 6, 6, 9]
item 4 (w=5,v=7) [0, 1, 1, 4, 5, 7, 8, 9]
1D table, same final row; each line is the single row after one item (downward loop)
after w=1 [0, 1, 1, 1, 1, 1, 1, 1]
after w=3 [0, 1, 1, 4, 5, 5, 5, 5]
after w=4 [0, 1, 1, 4, 5, 6, 6, 9]
after w=5 [0, 1, 1, 4, 5, 7, 8, 9]
answer 9 = items weight 3 + 4 (values 4 + 5)
upward loop on the same input: 9 ; unbounded answer: 9 ; true 0/1 answer: 9
example where it breaks: one item weight 2, value 5, cap 6 -> 0/1 5 upward 15
500 random cases agree (1D = 2D = memo = enumeration); upward loop equals the unbounded answer every time and differs from 0/1 in 438
edge cases ok; max-size random input -> 23637
```

**Edge cases:**
- cap = 0 or every item too heavy: 0.
- Item exactly equal to cap: allowed (`c >= w`).
- Max size 100 items, cap 1000: 100,000 updates.

**Follow-ups:**
- Which items? Q37 (reconstruction with a tie rule).
- Exactly cap? Initialise dp[0] = 0 and others -inf.
- Unbounded? Q20: flip the loop direction.

**Common mistakes:**
- Upward capacity loop.
- Loop bound `range(cap, w, -1)` (misses `c == w`).
- Defining dp as "exactly c" but initialising to zeros.

### Q18 ⭐⭐ 🟡 Subset sum (decision). `nums` has 1 <= len <= 200 positive integers (each <= 500) and `target` is 0 <= target <= 10^4. Return True if some subset (possibly empty, so target 0 is True) sums to `target`. Give the boolean 1D table with the downward capacity loop and the big-int bitset version; state the time O(n * target) for the table and O(n * target / 64) word operations for the bitset in theory (not a measured claim). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12), and your two methods against each other on small inputs. Example: nums=[3, 34, 4, 12, 5, 2], target=9 -> True; nums=[3, 34, 4, 12, 5, 2], target=30 -> False; nums=[7], target=0 -> True; nums=[5, 5], target=5 -> True.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Subset sum, decision form of 0/1 knapsack (boolean table or bitset).

**Say this first (1 line):** "dp[t] says whether sum t is reachable; for each number I update t from high to low. In Python the same thing is `bits |= bits << x`."

**Brute force:** Enumerate all 2^n subsets (n <= 12, the oracle).

**Optimal:**
- State: `dp[t]` = True if some subset of the items so far sums to exactly t. Base: `dp[0] = True`, so target 0 is True via the empty subset.
- Transition: for x in nums, for t from target down to x: `dp[t] |= dp[t - x]`. Downward so x is used once.
- Bitset: `bits |= (bits << x) & mask`, with `mask = (1 << (target + 1)) - 1` so the integer never grows beyond target + 1 bits. The answer is bit `target`.
- Memoised top-down `go(i, rem)`: depth <= len(nums) + 1, safe under the default limit.
- Table time O(n * target), space O(target). Bitset: n shift-or operations on an integer of target + 1 bits, so O(n * target / 64) word operations in theory (a statement about word size, not a measured claim).

**Complexity:** Table: O(n * target) time, O(target) space. At the maximum (n = 200, target = 10^4) that is at most 2,000,000 cell updates; the bitset does 200 shift-or operations on a 10001-bit integer (about 157 64-bit words).

**Dry run:** `[3, 34, 4, 12, 5, 2]`, target 9 (T = reachable, t = 0..9).
| after | row |
|---|---|
| start | `T.........` |
| 3 | `T..T......` |
| 34 | `T..T......` (too big) |
| 4 | `T..TT..T..` |
| 12 | `T..TT..T..` (too big) |
| 5 | `T..TTT.TTT` |
| 2 | `T.TTTTTTTT` |
- dp[9] True (4 + 5). The bitset rows in the output show the same bits.

**Code:**
```python
import random
from functools import lru_cache

random.seed(18)

def subset_sum(nums, target):
    """Boolean 1D table, capacity DOWNWARD. O(n * target) time, O(target) space."""
    dp = [True] + [False] * target                  # dp[t]: some subset of the items so far sums to exactly t
    for x in nums:
        for t in range(target, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]

def subset_sum_bits(nums, target):
    """Big-int bitset: bit t set means sum t reachable. Mask to target+1 bits so the int never grows past the target."""
    mask = (1 << (target + 1)) - 1
    bits = 1
    for x in nums:
        bits |= (bits << x) & mask
    return bool(bits >> target & 1)

def subset_sum_memo(nums, target):
    """Top-down over (i, remaining). Depth <= len(nums) + 1, safe under the default limit."""
    @lru_cache(maxsize=None)
    def go(i, rem):
        if rem == 0:
            return True
        if i == len(nums) or rem < 0:
            return False
        return go(i + 1, rem - nums[i]) or go(i + 1, rem)
    return go(0, target)

def brute(nums, target):
    n = len(nums)
    return any(sum(nums[i] for i in range(n) if m >> i & 1) == target for m in range(1 << n))

for (nums, t), want in [(([3, 34, 4, 12, 5, 2], 9), True), (([3, 34, 4, 12, 5, 2], 30), False), (([7], 0), True), (([5, 5], 5), True)]:
    assert subset_sum(nums, t) is want and subset_sum_bits(nums, t) is want and subset_sum_memo(nums, t) is want and brute(nums, t) is want
print('4 prompt examples ok')

# walk-through: nums=[3,34,4,12,5,2], target=9; items bigger than the target do nothing (34, 12)
nums, target = [3, 34, 4, 12, 5, 2], 9
dp = [True] + [False] * target
print('columns t = 0..9')
print('start   ', ''.join('T' if x else '.' for x in dp))
for x in nums:
    for t in range(target, x - 1, -1):
        if dp[t - x]:
            dp[t] = True
    print('item %-3d' % x, ''.join('T' if y else '.' for y in dp))
print('dp[9] =', dp[9], '(4 + 5, or 4 + 3 + 2)')

bits = 1
mask = (1 << 10) - 1
print('bitset after each item (bit 0 on the right, masked to 10 bits):')
for x in nums:
    bits |= (bits << x) & mask
    print('  item %-3d %s' % (x, format(bits, '010b')))

# seeded cross-check: table vs bitset vs memo vs enumeration (len <= 12)
t_true = 0
for _ in range(600):
    nums = [random.randint(1, 15) for _ in range(random.randint(1, 12))]
    target = random.randint(0, sum(nums) + 3)
    b = brute(nums, target)
    assert subset_sum(nums, target) == subset_sum_bits(nums, target) == subset_sum_memo(nums, target) == b, (nums, target)
    t_true += b
print('600 random cases agree (table = bitset = memo = enumeration); True in', t_true)

# edge cases and max size, table against bitset
assert subset_sum([7], 0) and not subset_sum([7], 3) and subset_sum([1] * 200, 200) and not subset_sum([2] * 200, 399)
for _ in range(5):
    nums = [random.randint(1, 500) for _ in range(200)]
    target = random.randint(0, 10**4)
    assert subset_sum(nums, target) == subset_sum_bits(nums, target) == subset_sum_memo(nums, target)
print('edge cases ok; five max-size random inputs: table = bitset = memo')
print('table cell updates at max size (n=200, target=10^4): at most', 200 * 10**4, '; bitset: 200 shift-or operations on a', 10**4 + 1, 'bit integer (about', (10**4 + 1 + 63) // 64, '64-bit words each)')
```

**Output (my run):**
```
4 prompt examples ok
columns t = 0..9
start    T.........
item 3   T..T......
item 34  T..T......
item 4   T..TT..T..
item 12  T..TT..T..
item 5   T..TTT.TTT
item 2   T.TTTTTTTT
dp[9] = True (4 + 5, or 4 + 3 + 2)
bitset after each item (bit 0 on the right, masked to 10 bits):
  item 3   0000001001
  item 34  0000001001
  item 4   0010011001
  item 12  0010011001
  item 5   1110111001
  item 2   1111111101
600 random cases agree (table = bitset = memo = enumeration); True in 391
edge cases ok; five max-size random inputs: table = bitset = memo
table cell updates at max size (n=200, target=10^4): at most 2000000 ; bitset: 200 shift-or operations on a 10001 bit integer (about 157 64-bit words each)
```

**Edge cases:**
- target = 0: True. target above the sum: False.
- Items larger than target are skipped.
- Duplicates are fine (`[5, 5]`, target 5: True).

**Follow-ups:**
- Count the subsets? Replace `|=` with `+=` (Q19).
- Which subset? Keep a 2D table or parent pointers.
- Large values, few items? Meet in the middle, O(2^(n/2)).

**Common mistakes:**
- Upward loop (reuses an item).
- Not masking the bitset (the int grows to the total sum; harmless but wasteful).
- Treating target 0 as False.

### Q19 ⭐⭐ 🟡 Target sum (count sign assignments). `nums` has 1 <= len <= 20 non-negative integers with sum <= 1000 (zeros allowed). Put a + or a - in front of every number and count the assignments whose total equals `target` (-1000 <= target <= 1000). Return the count. Reduce it to counting subsets with sum (S + target) / 2, where S is the total; say when the answer is 0 at once (|target| > S or S + target odd), and explain what each zero in the list does to the count (it doubles it). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all 2^n sign assignments (len <= 12) on small inputs. Example: nums=[1, 1, 1, 1, 1], target=3 -> 5; nums=[1], target=1 -> 1; nums=[0, 0, 1], target=1 -> 4; nums=[1, 2], target=4 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Count subsets with a given sum (counting 0/1 knapsack), after an algebra reduction.

**Say this first (1 line):** "Plus-group P and minus-group N: P - N = target and P + N = S, so P = (S + target) / 2. I count subsets with sum P."

**Brute force:** All 2^n sign assignments (n <= 12 as the oracle). A direct DP over signed running totals (a dict) also works and is the version I give first if I do not see the trick.

**Optimal:**
- Reduction: need = (S + target) / 2. The answer is 0 at once if |target| > S or S + target is odd.
- State: `dp[w]` = number of subsets (by index) with sum w. Base: `dp[0] = 1`.
- Transition: for x in nums, for w from need down to x: `dp[w] += dp[w - x]`. Downward, each item once.
- Zeros: for x = 0 the loop runs w = need..0 and does `dp[w] += dp[w]`, doubling every cell. So each zero doubles the count (a zero can take + or - without changing the total). Verified exhaustively for all lists of length <= 6 with values 0..3: `count(with z zeros) = 2^z * count(without)` and the DP equals the 2^n enumeration.
- Memoised top-down over (i, running total): depth len(nums) <= 20.

**Complexity:** O(n * need) time, O(need) space, with need <= (S + |target|)/2 <= 1000.

**Dry run:** `[1,1,1,1,1]`, target 3: S = 5, need = 4. Row after each item (w = 0..4):
`[1,0,0,0,0]` -> `[1,1,0,0,0]` -> `[1,2,1,0,0]` -> `[1,3,3,1,0]` -> `[1,4,6,4,1]` -> `[1,5,10,10,5]`.
- dp[4] = 5 = C(5, 4): choose which four numbers get a plus.
- With `[0, 0, 1]`, target 1 (need 1): `[1,0]` -> `[2,0]` -> `[4,0]` -> `[4,4]`: answer 4.

**Code:**
```python
import random
import itertools
from functools import lru_cache

random.seed(19)

def target_sum(nums, target):
    """Optimal: signs = split into P (plus) and N (minus). P - N = target, P + N = S, so P = (S + target) / 2.
    Count subsets with sum P. O(n * P) time, O(P) space."""
    s = sum(nums)
    if abs(target) > s or (s + target) % 2:
        return 0
    need = (s + target) // 2
    dp = [1] + [0] * need                           # dp[w]: number of subsets (by index) with sum w
    for x in nums:
        for w in range(need, x - 1, -1):            # downward; for x = 0 this runs w = need..0 and doubles every cell
            dp[w] += dp[w - x]
    return dp[need]

def target_sum_memo(nums, target):
    """Top-down over (i, running signed total). Depth = len(nums) <= 20."""
    @lru_cache(maxsize=None)
    def go(i, total):
        if i == len(nums):
            return 1 if total == target else 0
        return go(i + 1, total + nums[i]) + go(i + 1, total - nums[i])
    return go(0, 0)

def target_sum_dict(nums, target):
    """Direct DP over signed totals (no reduction), the version you give first if you do not see the trick."""
    ways = {0: 1}
    for x in nums:
        nxt = {}
        for t, c in ways.items():
            nxt[t + x] = nxt.get(t + x, 0) + c
            nxt[t - x] = nxt.get(t - x, 0) + c
        ways = nxt
    return ways.get(target, 0)

def brute(nums, target):
    """Oracle: all 2^n sign assignments."""
    return sum(1 for signs in itertools.product((1, -1), repeat=len(nums)) if sum(a * b for a, b in zip(signs, nums)) == target)

for (nums, t), want in [(([1, 1, 1, 1, 1], 3), 5), (([1], 1), 1), (([0, 0, 1], 1), 4), (([1, 2], 4), 0)]:
    assert target_sum(nums, t) == target_sum_memo(nums, t) == target_sum_dict(nums, t) == brute(nums, t) == want
print('4 prompt examples ok')

# walk-through on [1,1,1,1,1], target 3: S = 5, P = (5 + 3) / 2 = 4
nums, target = [1, 1, 1, 1, 1], 3
s = sum(nums); need = (s + target) // 2
dp = [1] + [0] * need
print('S =', s, ' need P =', need, ' columns w = 0..%d' % need)
print('start   ', dp)
for x in nums:
    for w in range(need, x - 1, -1):
        dp[w] += dp[w - x]
    print('item %d  ' % x, dp)
print('dp[4] =', dp[need], '= C(5,4) ways to pick which four numbers get a plus')

# zero check on [0,0,1], target 1: S=1, need=1
dp = [1, 0]
print('[0,0,1] target 1: need = 1')
print('start   ', dp)
for x in [0, 0, 1]:
    for w in range(1, x - 1, -1):
        dp[w] += dp[w - x]
    print('item %d  ' % x, dp)

# immediate zeros
print('|target| > S  ->', target_sum([1, 2], 4), ';  S + target odd ->', target_sum([1, 2], 2), ' (S=3, 5 is odd)')

# claim: every zero doubles the count (exhaustive)
count = 0
for n in range(1, 7):
    for nums in itertools.product(range(0, 4), repeat=n):
        nums = list(nums)
        for target in range(-sum(nums) - 1, sum(nums) + 2):
            got = target_sum(nums, target)
            assert got == brute(nums, target), (nums, target)
            nz = [x for x in nums if x]
            z = n - len(nz)
            if nz:
                assert got == 2 ** z * target_sum(nz, target)
            count += 1
print('exhaustive (all lists len<=6, values 0..3, every target in range):', count, 'checks; each zero doubles the count, and the DP matches the 2^n enumeration')

# seeded random cross-check, len <= 12
for _ in range(500):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    target = random.randint(-sum(nums) - 2, sum(nums) + 2)
    b = brute(nums, target)
    assert target_sum(nums, target) == target_sum_memo(nums, target) == target_sum_dict(nums, target) == b, (nums, target)
print('500 random cases agree (reduction = memo = signed-total dict = enumeration)')

# edge cases / max size
assert target_sum([0], 0) == 2 and target_sum([0] * 20, 0) == 2**20 and target_sum([0] * 20, 1) == 0
assert target_sum([50] * 20, 0) == target_sum_dict([50] * 20, 0) == 184756
assert target_sum([1000], -1000) == 1 and target_sum([1000], 0) == 0
print('edge cases ok: twenty zeros -> 2^20 =', target_sum([0] * 20, 0), '; twenty 50s, target 0 ->', target_sum([50] * 20, 0))
```

**Output (my run):**
```
4 prompt examples ok
S = 5  need P = 4  columns w = 0..4
start    [1, 0, 0, 0, 0]
item 1   [1, 1, 0, 0, 0]
item 1   [1, 2, 1, 0, 0]
item 1   [1, 3, 3, 1, 0]
item 1   [1, 4, 6, 4, 1]
item 1   [1, 5, 10, 10, 5]
dp[4] = 5 = C(5,4) ways to pick which four numbers get a plus
[0,0,1] target 1: need = 1
start    [1, 0]
item 0   [2, 0]
item 0   [4, 0]
item 1   [4, 4]
|target| > S  -> 0 ;  S + target odd -> 0  (S=3, 5 is odd)
exhaustive (all lists len<=6, values 0..3, every target in range): 109224 checks; each zero doubles the count, and the DP matches the 2^n enumeration
500 random cases agree (reduction = memo = signed-total dict = enumeration)
edge cases ok: twenty zeros -> 2^20 = 1048576 ; twenty 50s, target 0 -> 184756
```

**Edge cases:**
- `[0]`, target 0: 2. Twenty zeros, target 0: 2^20.
- |target| > S: 0. S + target odd: 0.
- Negative target: symmetric to its absolute value.

**Follow-ups:**
- Why not a dict DP? It works (target range is small); the reduction is faster and 1D.
- Large values? Same table, still bounded by the sum limit.
- Min number of sign flips? Different DP; keep counts of items too.

**Common mistakes:**
- Skipping the parity check (non-integer need).
- Looping `w` down to `x` with `range(need, x, -1)` and missing `w == x`.
- Treating zeros as ignorable (the answer is off by a factor 2 per zero).

### Q20 ⭐⭐ 🟡 Unbounded knapsack (maximum value). `weights` and `values` have equal length 1 <= len <= 50 (1 <= weight <= 100, 1 <= value <= 1000) and each item can be used any number of times; `cap` is 0 <= cap <= 10^4. Return the maximum total value with total weight <= cap (0 if nothing fits). Give the 1D table (capacity upward) and say how it differs from the 0/1 version (Q17) by one loop direction only. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the remaining capacity (cap <= 10) on small inputs. Example: weights=[2, 3, 4], values=[3, 5, 7], cap=8 -> 14; weights=[5], values=[10], cap=4 -> 0; weights=[1, 5], values=[1, 8], cap=11 -> 17; weights=[3], values=[7], cap=9 -> 21.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Unbounded knapsack (items reusable), 1D table, capacity upward.

**Say this first (1 line):** "dp[c] is the best value with weight at most c; for each c I try every item as the last one added. It is the 0/1 knapsack with the capacity loop flipped to upward."

**Brute force:** Plain recursion over the remaining capacity: `f(c) = max(0, f(c - w) + v)` over items that fit. Exponential; the oracle for cap <= 10.

**Optimal:**
- State: `dp[c]` = best value with total weight <= c. Base: `dp[0] = 0`, and all zeros means "capacity left over is fine".
- Transition: `dp[c] = max(dp[c - w] + v)` over items with w <= c (or leave it at 0).
- Loop order: capacity outer, items inner; or items outer, capacity upward. Both give the same answer (checked in 500 cases) because for max the order of use does not matter.
- Versus 0/1 (Q17): the only difference is the capacity direction. Upward lets `dp[c - w]` already contain the item, which is exactly "reuse". Example `weights=[3], values=[7], cap=9`: 0/1 gives 7, unbounded gives 21.
- Recursion limit: the memoised top-down `f(c)` descends up to cap deep (a weight-1 item gives depth 10^4). It raises RecursionError under the default limit of 1000. Bottom-up is required.

**Complexity:** O(n * cap) time, O(cap) space. Max: 50 * 10^4 = 500,000 updates.

**Dry run:** weights `[2,3,4]`, values `[3,5,7]`, cap 8.
| c | dp[c] | best candidate |
|---|---|---|
| 1 | 0 | nothing fits |
| 2 | 3 | w2: dp[0]+3 |
| 3 | 5 | w3: dp[0]+5 |
| 4 | 7 | w4: dp[0]+7 |
| 5 | 8 | w2: dp[3]+3 = 8 |
| 6 | 10 | dp[4]+3 = 10 |
| 7 | 12 | w3: dp[4]+5 = 12 |
| 8 | 14 | w4: dp[4]+7 = 14 |
- Answer 14 (two weight-4 items).

**Code:**
```python
import random
from functools import lru_cache

random.seed(20)

def unbounded_knapsack(weights, values, cap):
    """Optimal: dp[c] = best value with total weight <= c, items reusable. O(n * cap) time, O(cap) space."""
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c and dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[cap]

def unbounded_item_outer(weights, values, cap):
    """Same answer, items outer and capacity UPWARD: the 0/1 code with one loop direction flipped."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack01(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def unbounded_memo(weights, values, cap):
    """Top-down over the remaining capacity. Depth can reach cap (weight-1 items), so it breaks past ~1000."""
    @lru_cache(maxsize=None)
    def f(c):
        return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)

def brute(weights, values, cap):
    """Oracle: plain recursion over the remaining capacity, no cache."""
    def f(c):
        return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)

for (w, v, c), want in [(([2, 3, 4], [3, 5, 7], 8), 14), (([5], [10], 4), 0), (([1, 5], [1, 8], 11), 17), (([3], [7], 9), 21)]:
    assert unbounded_knapsack(w, v, c) == unbounded_item_outer(w, v, c) == brute(w, v, c) == unbounded_memo(tuple(w), tuple(v), c) == want
print('4 prompt examples ok')

# walk-through on weights=[2,3,4], values=[3,5,7], cap=8
w, v, cap = [2, 3, 4], [3, 5, 7], 8
dp = [0] * (cap + 1)
print('c   dp[c]  candidates dp[c-w]+v for each item that fits')
print('0   0      base: nothing fits in capacity 0')
for c in range(1, cap + 1):
    cands = ['w=%d:dp[%d]+%d=%d' % (wi, c - wi, vi, dp[c - wi] + vi) for wi, vi in zip(w, v) if wi <= c]
    dp[c] = max([0] + [dp[c - wi] + vi for wi, vi in zip(w, v) if wi <= c])
    print('%-3d %-6d %s' % (c, dp[c], ', '.join(cands) if cands else 'nothing fits'))
print('dp[8] =', dp[8], '= 7 + 7 (two weight-4 items)')

# 0/1 versus unbounded: one loop direction
print('weights=[3], values=[7], cap=9 -> 0/1', knapsack01([3], [7], 9), ' unbounded', unbounded_knapsack([3], [7], 9))

# seeded cross-check against the plain recursion (cap <= 10)
for _ in range(500):
    n = random.randint(1, 4)
    w = [random.randint(1, 7) for _ in range(n)]
    v = [random.randint(1, 20) for _ in range(n)]
    cap = random.randint(0, 10)
    b = brute(w, v, cap)
    assert unbounded_knapsack(w, v, cap) == unbounded_item_outer(w, v, cap) == unbounded_memo(tuple(w), tuple(v), cap) == b, (w, v, cap)
print('500 random cases agree (capacity-outer = item-outer = memo = plain recursion)')

# recursion limit
try:
    unbounded_memo((1,), (1,), 10**4)
    print('memo at cap=10^4 with a weight-1 item: no error (unexpected)')
except RecursionError:
    print('memo at cap=10^4 with a weight-1 item: RecursionError under the default limit')
print('bottom-up cap=10^4, weights=[1] ->', unbounded_knapsack([1], [1], 10**4))

# edge cases and max size
assert unbounded_knapsack([5], [10], 0) == 0 and unbounded_knapsack([100], [1000], 99) == 0
big_w = [random.randint(1, 100) for _ in range(50)]
big_v = [random.randint(1, 1000) for _ in range(50)]
assert unbounded_knapsack(big_w, big_v, 10**4) == unbounded_item_outer(big_w, big_v, 10**4)
print('edge cases ok; max-size random input ->', unbounded_knapsack(big_w, big_v, 10**4))
```

**Output (my run):**
```
4 prompt examples ok
c   dp[c]  candidates dp[c-w]+v for each item that fits
0   0      base: nothing fits in capacity 0
1   0      nothing fits
2   3      w=2:dp[0]+3=3
3   5      w=2:dp[1]+3=3, w=3:dp[0]+5=5
4   7      w=2:dp[2]+3=6, w=3:dp[1]+5=5, w=4:dp[0]+7=7
5   8      w=2:dp[3]+3=8, w=3:dp[2]+5=8, w=4:dp[1]+7=7
6   10     w=2:dp[4]+3=10, w=3:dp[3]+5=10, w=4:dp[2]+7=10
7   12     w=2:dp[5]+3=11, w=3:dp[4]+5=12, w=4:dp[3]+7=12
8   14     w=2:dp[6]+3=13, w=3:dp[5]+5=13, w=4:dp[4]+7=14
dp[8] = 14 = 7 + 7 (two weight-4 items)
weights=[3], values=[7], cap=9 -> 0/1 7  unbounded 21
500 random cases agree (capacity-outer = item-outer = memo = plain recursion)
memo at cap=10^4 with a weight-1 item: RecursionError under the default limit
bottom-up cap=10^4, weights=[1] -> 10000
edge cases ok; max-size random input -> 8640000
```

**Edge cases:**
- cap = 0 or all items heavier than cap: 0.
- One item of weight 3, cap 9: three copies, 21.
- cap = 10^4: bottom-up is instant; memo raises RecursionError.

**Follow-ups:**
- Exactly cap? Initialise others to -inf.
- Count ways? Coin change II (Q10); combinations versus sequences is a loop-order choice.
- Bounded copies? Binary splitting of the counts into 0/1 items.

**Common mistakes:**
- Using the downward loop (gives the 0/1 answer).
- Raising the recursion limit instead of going bottom-up.
- Initialising `dp` with -inf and then reading dp[cap] when it should be "at most".

### Q21 ⭐⭐ 🟡 Combination sum IV: order matters versus order does not matter. `nums` is a list of 1 <= len <= 10 distinct positive integers (each <= 100) and `target` is 0 <= target <= 2000. Return `[ordered, unordered]`: `ordered` is the number of sequences (so [1, 2] and [2, 1] are different) of numbers from `nums`, reuse allowed, that sum to `target`; `unordered` is the number of multisets with that sum (Q10). Target 0 gives [1, 1]. Python integers are unbounded, so return exact values. Explain how swapping the two loops turns one count into the other, and which loop is outer in each. Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a recursion that enumerates every sequence (ordered) and every multiset (unordered), target <= 10 on small inputs. Example: nums=[1, 2, 3], target=4 -> [7, 4]; nums=[9], target=3 -> [0, 0]; nums=[2, 5], target=0 -> [1, 1]; nums=[1, 2], target=6 -> [13, 4].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D counting DP, unbounded knapsack flavour. `dp[t]` counts ways to reach sum `t`. The only thing that changes between "ordered" and "unordered" is which loop is outer.

**Say this first (1 line):** "Same recurrence, two loop orders: target outside and coins inside counts sequences; coins outside and target inside counts multisets."

**Brute force:** Recurse on the remaining sum and enumerate. For sequences: try every coin at every step, record the whole sequence. For multisets: decide per coin how many copies to take (or keep only sorted sequences). Exponential: the ordered count for `[1,2,3]` grows like the tribonacci numbers (it has 530 digits at target 2000), so enumeration only works for target <= 10 or so. That is the oracle, not the answer.

**Optimal:**
- State, ordered: `o[t]` = number of sequences from `nums` (reuse allowed) with sum `t`. Condition on the LAST element: `o[t] = sum(o[t - x] for x in nums if x <= t)`. Base `o[0] = 1` (the empty sequence). Different last elements give different sequences, and the same multiset in a different order is a different sequence, so nothing is merged.
- State, unordered: `u[t]` = number of multisets with sum `t`, using only the coins processed so far. Process coins one at a time: `u[t] += u[t - x]` for `t` from `x` up. Base `u[0] = 1`.
- Why the loop order matters: with the coin loop OUTER, each coin gets a "turn" and is never revisited, so a multiset is built in one fixed order of coin types (all 1s, then all 2s, ...) and counted once. With the target loop OUTER, at every `t` every coin is allowed as the last element, so `1,2` and `2,1` are both reached, and counted twice.
- Which loop is outer: ordered = target outer, coins inner. Unordered = coins outer, target inner.
- Target 0: both are 1 (the empty sequence). Check: `[2, 5]`, target 0 gives `[1, 1]`.
- Exact integers: Python ints are unbounded, so there is no modulo. The ordered count for `[1,2,3]`, target 2000 has 530 digits (printed below). Cost: O(target * len(nums)) big-int additions.

**Complexity:** Time O(target * len(nums)) additions for each count (big ints make each add O(digits), which grows with target; say that if asked). Space O(target). Both can be done in one pass each, no 2D table needed.

**Dry run:** `nums=[1,2,3]`, target 4.
- Ordered, `t=1..4`: `o[1]=o[0]=1`; `o[2]=o[1]+o[0]=2`; `o[3]=o[2]+o[1]+o[0]=4`; `o[4]=o[3]+o[2]+o[1]=7`. Table `[1,1,2,4,7]`.
- Unordered: after coin 1 every cell is 1 (`1+1+1+1`). After coin 2: `[1,1,2,2,3]` (e.g. `u[4] = u[4] + u[2] = 1 + 2`). After coin 3: `[1,1,2,3,4]`. Answer 4: `{1111, 112, 22, 13}`.
- Answer `[7, 4]`. The 7 sequences: 1111, 112, 121, 211, 22, 13, 31. The 3 extra are the re-orderings of `112` (2 more) and `13` (1 more).

**Code:**
```python
import random, sys
from functools import cache

random.seed(21)

def count_both(nums, target):
    """Bottom-up. ordered: target loop OUTER, coin loop inner. unordered: coin loop OUTER, target inner."""
    ordered = [1] + [0] * target
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                ordered[t] += ordered[t - x]
    unordered = [1] + [0] * target
    for x in nums:
        for t in range(x, target + 1):
            unordered[t] += unordered[t - x]
    return [ordered[target], unordered[target]]

def swapped(nums, target):
    """The classic swap: each loop order with the other count's name."""
    a = [1] + [0] * target            # coin outer, target inner -> this is the UNORDERED count
    for x in nums:
        for t in range(x, target + 1):
            a[t] += a[t - x]
    b = [1] + [0] * target            # target outer, coin inner -> this is the ORDERED count
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                b[t] += b[t - x]
    return a[target], b[target]

def memo_ordered(nums, target):
    @cache
    def f(rem):
        if rem == 0:
            return 1
        return sum(f(rem - x) for x in nums if x <= rem)
    return f(target)

def brute(nums, target):
    """Enumerate every sequence (ordered) and every non-decreasing sequence = multiset (unordered)."""
    seqs = []
    def rec(rem, cur):
        if rem == 0:
            seqs.append(tuple(cur)); return
        for x in nums:
            if x <= rem:
                cur.append(x); rec(rem - x, cur); cur.pop()
    rec(target, [])
    ms = set()
    for s in seqs:
        ms.add(tuple(sorted(s)))        # a multiset is a sorted sequence
    sets2 = []
    sn = sorted(nums)
    def rec2(i, rem, cur):
        if rem == 0:
            sets2.append(tuple(cur)); return
        if i == len(sn): return
        k = 0
        while k * sn[i] <= rem:
            rec2(i + 1, rem - k * sn[i], cur + [sn[i]] * k); k += 1
    rec2(0, target, [])
    assert set(sets2) == ms and len(sets2) == len(ms)   # two independent ways to enumerate multisets agree
    return [len(seqs), len(sets2)]

# examples
for nums, t, exp in [([1, 2, 3], 4, [7, 4]), ([9], 3, [0, 0]), ([2, 5], 0, [1, 1]), ([1, 2], 6, [13, 4])]:
    got = count_both(nums, t); assert got == exp == brute(nums, t), (nums, t, got)
    print('example', nums, t, '->', got)

# hand table for the first example
nums, t = [1, 2, 3], 4
o = [1] + [0] * t
for tt in range(1, t + 1):
    o[tt] = sum(o[tt - x] for x in nums if x <= tt)
print('ordered   t=0..4:', o)
u = [1] + [0] * t
for x in nums:
    for tt in range(x, t + 1):
        u[tt] += u[tt - x]
    print('unordered after coin', x, ':', u)

# seeded cross-check
n_cases = diff = swap_ok = 0
for _ in range(600):
    k = random.randint(1, 4)
    nums = random.sample(range(1, 7), k)
    target = random.randint(0, 10)
    got = count_both(nums, target)
    assert got == brute(nums, target), (nums, target)
    a, b = swapped(nums, target)
    assert (a, b) == (got[1], got[0])     # coin-outer gives unordered, target-outer gives ordered, always
    n_cases += 1; diff += got[0] != got[1]
    swap_ok += got[0] >= got[1]  # ordered count >= unordered count always
print('cross-check cases', n_cases, '| ordered != unordered on', diff, '| ordered >= unordered on', swap_ok)
for _ in range(100):
    nums = random.sample(range(1, 30), random.randint(1, 6)); target = random.randint(0, 120)
    assert count_both(nums, target)[0] == memo_ordered(nums, target)
print('memo (depth <= 120) equals bottom-up on 100 random cases')

# big sizes: bottom-up is fine, memo recursion is not
big = count_both([1, 2, 3], 2000)
print('target 2000, nums [1,2,3]: ordered has', len(str(big[0])), 'digits, unordered =', big[1])
print('limit =', sys.getrecursionlimit())
for n in (500, 2000):
    try:
        v = memo_ordered([1, 2, 3], n); print('memo target', n, 'ok', v == count_both([1, 2, 3], n)[0])
    except RecursionError:
        print('memo target', n, 'RecursionError')
def memo_ok(n):
    try:
        memo_ordered([1, 2, 3], n); return True
    except RecursionError:
        return False
lo, hi = 1, 2000          # largest n that works in a fresh cache (the sum(...) generator costs a second frame per level)
while lo < hi:
    mid = (lo + hi + 1) // 2
    if memo_ok(mid): lo = mid
    else: hi = mid - 1
print('largest target the memo handles at limit 1000 (this layout, called from module level):', lo)
assert count_both([1], 2000) == [1, 1]
assert count_both([100] * 1, 2000) == [1, 1] and count_both([100, 99], 1) == [0, 0]
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 2, 3] 4 -> [7, 4]
example [9] 3 -> [0, 0]
example [2, 5] 0 -> [1, 1]
example [1, 2] 6 -> [13, 4]
ordered   t=0..4: [1, 1, 2, 4, 7]
unordered after coin 1 : [1, 1, 1, 1, 1]
unordered after coin 2 : [1, 1, 2, 2, 3]
unordered after coin 3 : [1, 1, 2, 3, 4]
cross-check cases 600 | ordered != unordered on 220 | ordered >= unordered on 600
memo (depth <= 120) equals bottom-up on 100 random cases
target 2000, nums [1,2,3]: ordered has 530 digits, unordered = 334334
limit = 1000
memo target 500 RecursionError
memo target 2000 RecursionError
largest target the memo handles at limit 1000 (this layout, called from module level): 498
edge asserts passed
```

Reading the output:
- All four examples match both the DP and the enumeration. Ordered count is >= unordered on all 600 cases and strictly larger on 220 of them.
- The swapped loop order gave the other count on all 600 cases: target-outer always equals the ordered count and coin-outer the unordered count.
- The recursion limit result is the honest surprise. At the default limit of 1000, the memoised top-down function failed already at target 500, not only at 2000. The reason: `sum(f(rem - x) for x ...)` runs inside a generator frame, so each level costs two Python frames. The largest target that worked here was 498 (sandbox figure, depends on how deep the caller already is). Moral: the limit hits earlier than the "depth = n" rule of thumb suggests.

**Edge cases:**
- Target 0: `[1, 1]` (empty sequence).
- Target below the smallest coin, or no coin divides into it: `[0, 0]`.
- `nums=[1]`: always `[1, 1]` (one way, any order).
- Large target: exact big ints, no modulo. Do not convert to float.
- Coins larger than `t` must be skipped (`if x <= t`), or `dp[t - x]` indexes negative and silently wraps around in Python. That is a real Python-specific bug.

**Follow-ups:**
- "Return the answer modulo 10^9+7?" Reduce each addition: `o[t] = (o[t] + o[t-x]) % M`. Same loops.
- "How do you count sequences if negatives are allowed?" Infinite counts are possible (a cycle of +1, -1), so you need a bound on length. Then add a length dimension.
- "Why not top-down?" It is correct but needs depth about target (two frames per level here); at target 2000 it raises `RecursionError` at the default limit. Raising the limit is fragile; use the loop.

**Common mistakes:**
- Putting the coin loop outer for the "number of sequences" count. It silently returns the multiset count. Example `[1,2,3]`, 4 gives 4 instead of 7.
- Forgetting `o[0] = 1`, so every count is 0.
- No `x <= t` guard (negative index wraps around).
- Memoising with a `sum(generator)` and assuming the recursion depth is just `target`.

### Q22 ⭐⭐ 🟡 Maximum subarray with its position (reconstruction with a tie rule). `nums` has 1 <= len <= 10^5 integers (|value| <= 10^4). Return `[best, l, r]` where `best` is the largest sum of a non-empty contiguous subarray and nums[l..r] (inclusive, 0-indexed) is the subarray achieving it; when several subarrays reach the maximum, return the one with the smallest l, and among those the smallest r. Say how you carry the start index through Kadane, and why 'restart when the running sum is negative' needs care on ties (a running sum of exactly 0). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every subarray with the same tie rule, plus an exhaustive check over every list of length <= 6 with values in -2..2 on small inputs. Example: nums=[-2, 1, -3, 4, -1, 2, 1, -5, 4] -> [6, 3, 6]; nums=[0, 0, 0] -> [0, 0, 0]; nums=[3, -3, 3] -> [3, 0, 0]; nums=[-5, -2, -9] -> [-2, 1, 1]; nums=[2, -2, 2, -2, 5] -> [5, 0, 4].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D DP, "best subarray ending at i" (Kadane), plus reconstruction by carrying the start index.

**Say this first (1 line):** "`run` is the best sum of a subarray ending here; I extend it unless it is strictly negative, and I carry its start index so I can report `[best, l, r]`."

**Brute force:** Try every `(l, r)` with a running sum, keep the best by key `(-sum, l, r)`. O(n^2) time, O(1) space. Fine at n = 10^4, too slow at 10^5. This is the oracle.

**Optimal:**
- State: `run[i]` = largest sum of a non-empty subarray that ends exactly at `i`. Transition: `run[i] = max(nums[i], run[i-1] + nums[i])`. Base: `run[0] = nums[0]`. Answer: `max(run)`.
- Why only the previous value matters: any subarray ending at `i` is either just `nums[i]` or a subarray ending at `i-1` plus `nums[i]`. The best of the second kind uses the best `run[i-1]`.
- Space: only the last `run` is needed, so O(1).
- Carrying the start: keep `start[i]`. If we restart, `start = i`; if we extend, `start` stays. Keep `(best, l, r)` and update whenever `run > best`.
- The tie care, exactly: when `run[i-1] == 0`, extending and restarting give the same sum, but extending keeps the SMALLER start. The rule wants the smallest `l`, so restart only when `run[i-1] < 0` (strictly). Restarting on `<= 0` is wrong.
- Why updating only on a strictly greater sum then also gives the smallest `r` for the chosen `l`: the first time the best is reached we freeze `r`.
- Do we also need an "equal sum but smaller l" update? Argue it is never needed: suppose an earlier candidate `(l', r')` ties the global maximum with `l' > L` and `r' < R`, where `(L, R)` is the answer. Then `S(L..r') = S(L..l'-1) + best <= best`, and `S(l'..R) = best - S(L..l'-1) <= best`, so `S(L..l'-1) = 0` and `(L, r')` is also optimal with `r' < R`, contradicting the smallest `r` for `L`. My code has the extra check as a flag and the exhaustive test shows the plain `>` rule alone gives the same answers (count 0 wrong), so the claim holds on the tested range.
- All-negative lists: `run` restarts every time, so the answer is the largest single element (examples: `[-5,-2,-9] -> [-2,1,1]`). Do not initialise `best = 0`; that would allow an empty subarray.

**Complexity:** Time O(n), space O(1). It is already a loop, so there is no recursion limit issue at n = 10^5. (A memoised "best ending at i" recursion would nest n deep and raise `RecursionError` at the default limit of 1000, so loop.)

**Dry run:** `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` (table printed below).
- i=0: restart, run -2, start 0, best -2 at [0,0].
- i=1: previous run -2 < 0 so restart: run 1, start 1, best 1 [1,1].
- i=2: run 1-3 = -2, start 1; best stays.
- i=3: previous -2 < 0 so restart: run 4, start 3, best 4 [3,3].
- i=4..6: run 3, 5, 6, start 3; best 6 [3,6].
- i=7,8: run 1, 5; no improvement. Answer `[6, 3, 6]`.

**Code:**
```python
import random, itertools

random.seed(22)

def kadane_pos(nums, restart_on_zero=False, update_on_smaller_l=True):
    """Kadane with the start index carried. Returns [best, l, r] with the tie rule smallest l, then smallest r.
    run = best sum of a subarray ENDING at i, start = its leftmost start."""
    best, bl, br = None, 0, 0
    run, start = 0, 0
    for i, x in enumerate(nums):
        if i == 0 or run < 0 or (restart_on_zero and run == 0):
            run, start = x, i            # restart: the old prefix cannot help (strictly hurts)
        else:
            run += x                     # run == 0 keeps the older start: same sum, smaller l
        if best is None or run > best or (update_on_smaller_l and run == best and start < bl):
            best, bl, br = run, start, i
    return [best, bl, br]

def brute(nums):
    """O(n^2): every subarray, key = (-sum, l, r)."""
    n = len(nums); cand = []
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += nums[r]; cand.append((-s, l, r))
    s, l, r = min(cand)
    return [-s, l, r]

for nums, exp in [([-2, 1, -3, 4, -1, 2, 1, -5, 4], [6, 3, 6]), ([0, 0, 0], [0, 0, 0]), ([3, -3, 3], [3, 0, 0]),
                  ([-5, -2, -9], [-2, 1, 1]), ([2, -2, 2, -2, 5], [5, 0, 4])]:
    assert kadane_pos(nums) == brute(nums) == exp, nums
    print('example', nums, '->', exp)

# hand table, first example
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
run, start, best = 0, 0, None
print('i  x  run start best[l,r]')
bl = br = 0
for i, x in enumerate(nums):
    if i == 0 or run < 0: run, start = x, i
    else: run += x
    if best is None or run > best or (run == best and start < bl): best, bl, br = run, start, i
    print(f'{i}  {x:2d}  {run:3d}  {start:3d}   {best} [{bl},{br}]')

# exhaustive: all lists of length 1..6 over -2..2
total = bad_zero = bad_strict = bad_main = 0
for n in range(1, 7):
    for t in itertools.product(range(-2, 3), repeat=n):
        l = list(t); want = brute(l); total += 1
        bad_main += kadane_pos(l) != want
        bad_zero += kadane_pos(l, restart_on_zero=True) != want
        bad_strict += kadane_pos(l, update_on_smaller_l=False) != want
print('exhaustive lists checked:', total)
print('main version wrong on', bad_main)
print('restart when run <= 0 wrong on', bad_zero)
print('update only on strictly greater sum (no smaller-l check) wrong on', bad_strict)
assert bad_main == 0 and total == 19530

# seeded random cross-check, longer lists
for _ in range(500):
    n = random.randint(1, 40); l = [random.randint(-6, 6) for _ in range(n)]
    assert kadane_pos(l) == brute(l)
print('500 random lists (len <= 40) agree with the O(n^2) enumeration')

# max size, runs in one pass
big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
b = kadane_pos(big)
P = 0; s = sum(big[b[1]:b[2] + 1]); assert s == b[0]
print('n = 10^5 result', b)
assert kadane_pos([7]) == [7, 0, 0] and kadane_pos([-3]) == [-3, 0, 0]
print('edge asserts passed')
```

**Output (my run):**
```
example [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> [6, 3, 6]
example [0, 0, 0] -> [0, 0, 0]
example [3, -3, 3] -> [3, 0, 0]
example [-5, -2, -9] -> [-2, 1, 1]
example [2, -2, 2, -2, 5] -> [5, 0, 4]
i  x  run start best[l,r]
0  -2   -2    0   -2 [0,0]
1   1    1    1   1 [1,1]
2  -3   -2    1   1 [1,1]
3   4    4    3   4 [3,3]
4  -1    3    3   4 [3,3]
5   2    5    3   5 [3,5]
6   1    6    3   6 [3,6]
7  -5    1    3   6 [3,6]
8   4    5    3   6 [3,6]
exhaustive lists checked: 19530
main version wrong on 0
restart when run <= 0 wrong on 4503
update only on strictly greater sum (no smaller-l check) wrong on 0
500 random lists (len <= 40) agree with the O(n^2) enumeration
n = 10^5 result [2992853, 12608, 74008]
edge asserts passed
```

Reading the output:
- The "restart when run <= 0" variant is wrong on 4503 of the 19530 lists (it gives a larger `l`); the claim in the prompt is correct.
- The plain `>` rule without the smaller-`l` check is also right on all 19530 lists, matching the argument above.

**Edge cases:**
- All negative: single largest element, `l == r`.
- All zeros: `[0, 0, 0]` (first position wins both ties).
- Zero running sum in the middle (`[3,-3,3] -> [3,0,0]`): extending to index 2 ties at 3, but `r` stays 0 because we update only on strictly greater.
- Single element.
- n = 10^5: values up to 10^4 give sums up to 10^9, no overflow in Python.

**Follow-ups:**
- "Return all optimal subarrays?" Keep a list and reset it when a strictly larger sum appears; with ties you need the prefix-min formulation (`best ending at r = P[r+1] - min P[l]`), tracking every minimising index.
- "Maximum product subarray?" Track both max and min ending here, because a negative flips them.
- "Circular?" See Q26.

**Common mistakes:**
- `best = 0` initial value (empty subarray) on all-negative input.
- Restarting when `run <= 0`, which moves `l` to the right on ties.
- Updating `(l, r)` on `>=`, which moves `r` to the right on ties.
- Resetting `start` on every step instead of only on restart.

### Q23 ⭐⭐ 🟡 Coin change with the coins themselves (reconstruction with a tie rule). `coins` has 1 <= len <= 8 distinct positive integers (each <= 100) and `amount` is 0 <= amount <= 1000. Return the list of coins (in non-decreasing order, repeats listed) of a minimum-size multiset summing to `amount`; if several minimum-size multisets exist return the lexicographically smallest list; return [] for amount 0 and null (None) if the amount cannot be made. Explain how to rebuild the answer from the `dp` table (which coin was used last) and how to follow the tie rule, and why storing a parent pointer per amount gives some optimal answer but not necessarily this one unless you choose carefully. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all multisets with the same tie rule (amount <= 15) on small inputs. Example: coins=[1, 2, 5], amount=11 -> [1, 5, 5]; coins=[2], amount=3 -> null; coins=[3, 5], amount=0 -> []; coins=[1, 3, 4], amount=6 -> [3, 3]; coins=[2, 3], amount=7 -> [2, 2, 3].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** 1D DP, unbounded knapsack (minimise count), with reconstruction under a tie rule.

**Say this first (1 line):** "`dp[a]` is the fewest coins for amount `a`; to get the coins I walk back from `amount` and, at each step, take the smallest coin `c` with `dp[a-c] == dp[a]-1`."

**Brute force:** Enumerate every multiset: for each coin (in sorted order) choose how many copies, keep those with sum `amount`, then take the minimum size and, among those, the lexicographically smallest list. Exponential, fine for amount <= 15. This is the oracle.

**Optimal:**
- State: `dp[a]` = minimum number of coins summing to `a`, or infinity. Base: `dp[0] = 0`. Transition on the last coin: `dp[a] = min(dp[a - c] + 1)` over coins `c <= a`.
- Answer exists iff `dp[amount]` is finite; otherwise return `None`. Amount 0 gives `[]`.
- Rebuild: from `a = amount`, scan coins in ascending order and take the first `c <= a` with `dp[a - c] == dp[a] - 1`. Append it, set `a -= c`, repeat.
- Why this follows the tie rule: the output list is sorted, so its first element is the smallest coin in the multiset. If the smallest coin of some optimal multiset is `m`, then `dp[a - m] == dp[a] - 1`, so `m` is a candidate; the smallest candidate `c` therefore satisfies `c <= m`. And `c` is actually usable as the smallest member: if the optimal rest for `a - c` contained a coin `d < c`, then removing `d` from `{c} + rest` leaves a multiset for `a - d` of size `dp[a] - 1`, so `d` is a smaller candidate, contradicting that `c` was the smallest candidate. So `c` is the smallest possible first element, and the argument repeats on `a - c` (coins taken later are always >= `c`, so the list comes out non-decreasing). Check: the code asserts the output is sorted.
- Why a parent pointer is not enough by itself: `par[a]` stores the coin that first achieved `dp[a]` in the loop order. If you loop coins in the INPUT order, you get some optimal answer but not necessarily the lexicographically smallest. In the run below that differs from the rule on 38 of 2000 cases (e.g. coins `[4,6,5,3]`, amount 9: parent pointer gives `[4,5]`, the rule gives `[3,6]`). Looping coins in ascending order with strict `<` is the same as the rebuild above and matched on all 2000 cases (it picks the smallest coin attaining the minimum). Looping descending differed on 3 of 2000.

**Complexity:** Time O(amount * len(coins)) for the table, O(amount) for the rebuild (each step removes at least 1). Space O(amount). Top-down memoised recursion needs depth up to `amount / min(coin)`; with coin 1 and amount 1000 that is about 1000 frames and it raises `RecursionError` at the default limit (shown below). Bottom-up avoids that.

**Dry run:** `coins=[1,2,5]`, amount 11.
- `dp[0..11] = [0,1,1,2,2,1,2,2,3,3,2,3]` (e.g. `dp[7] = dp[2]+1 = 2` via coin 5).
- Rebuild: `a=11`, `dp=3`: coin 1: `dp[10]=2 == 2`, take 1. `a=10`, `dp=2`: coin 1: `dp[9]=3` no; coin 2: `dp[8]=3` no; coin 5: `dp[5]=1` yes, take 5. `a=5`: coin 1: `dp[4]=2` no; coin 2: `dp[3]=2` no; coin 5: `dp[0]=0` yes, take 5. Result `[1,5,5]`.

**Code:**
```python
import random, sys
from functools import cache

random.seed(23)
INF = float('inf')

def min_table(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp

def coin_list(coins, amount):
    """Bottom-up table, then rebuild: at each amount take the SMALLEST coin c with dp[a-c] == dp[a]-1."""
    dp = min_table(coins, amount)
    if dp[amount] == INF:
        return None
    out, a = [], amount
    cs = sorted(coins)
    while a:
        for c in cs:
            if c <= a and dp[a - c] == dp[a] - 1:
                out.append(c); a -= c
                break
    return out                      # already non-decreasing (argued in the text, asserted below)

def naive_parent(coins, amount, order='input'):
    """Plain parent pointer: remember the first coin (in the given loop order) that achieves dp[a], rebuild, sort."""
    dp = [0] + [INF] * amount
    par = [0] * (amount + 1)
    cs = {'input': list(coins), 'asc': sorted(coins), 'desc': sorted(coins, reverse=True)}[order]
    for a in range(1, amount + 1):
        for c in cs:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1; par[a] = c
    if dp[amount] == INF:
        return None
    out, a = [], amount
    while a:
        out.append(par[a]); a -= par[a]
    return sorted(out)

def memo_len(coins, amount):
    @cache
    def f(a):
        if a == 0: return 0
        best = INF
        for c in coins:
            if c <= a:
                best = min(best, f(a - c) + 1)
        return best
    return f(amount)

def brute(coins, amount):
    """Enumerate every multiset with sum amount (k copies of each coin), pick min size then lexicographically smallest."""
    cs = sorted(coins); found = []
    def rec(i, rem, cur):
        if rem == 0:
            found.append(list(cur)); return
        if i == len(cs): return
        k = 0
        while k * cs[i] <= rem:
            rec(i + 1, rem - k * cs[i], cur + [cs[i]] * k); k += 1
    rec(0, amount, [])
    if not found: return None
    m = min(map(len, found))
    return min(f for f in found if len(f) == m)

for coins, amt, exp in [([1, 2, 5], 11, [1, 5, 5]), ([2], 3, None), ([3, 5], 0, []), ([1, 3, 4], 6, [3, 3]), ([2, 3], 7, [2, 2, 3])]:
    got = coin_list(coins, amt); assert got == brute(coins, amt) == exp, (coins, amt, got)
    print('example', coins, amt, '->', got)

# hand table for the first example
dp = min_table([1, 2, 5], 11)
print('dp[0..11] =', dp)
a, steps = 11, []
while a:
    for c in [1, 2, 5]:
        if c <= a and dp[a - c] == dp[a] - 1:
            steps.append((a, c)); a -= c; break
print('rebuild (amount, coin taken):', steps)

# seeded cross-check, amount <= 15
n = mism_in = mism_asc = mism_desc = none_cnt = 0
ex = None
for _ in range(2000):
    coins = random.sample(range(1, 10), random.randint(2, 4)); amt = random.randint(0, 15)
    got = coin_list(coins, amt); want = brute(coins, amt)
    assert got == want, (coins, amt, got, want)
    if got is not None: assert got == sorted(got)
    n += 1; none_cnt += got is None
    for key in ('input', 'asc', 'desc'):
        bad = naive_parent(coins, amt, key) != want
        if key == 'input':
            mism_in += bad
            if bad and ex is None: ex = (coins, amt)
        elif key == 'asc': mism_asc += bad
        else: mism_desc += bad
print('cross-check cases', n, '(of which unreachable:', none_cnt, ')')
print('naive parent pointer, coins looped in INPUT order, differs from the tie rule on', mism_in)
print('naive parent pointer, coins looped ascending, differs on', mism_asc)
print('naive parent pointer, coins looped descending, differs on', mism_desc)
print('example of a miss (input order):', ex, 'naive', naive_parent(ex[0], ex[1]), 'rule', brute(*ex))

# memo version agrees on small, recursion limit at large
for _ in range(100):
    coins = random.sample(range(1, 20), random.randint(1, 5)); amt = random.randint(0, 60)
    d = min_table(coins, amt)[amt]
    assert memo_len(coins, amt) == d
big = coin_list([1, 5, 10, 25, 100], 1000)
print('amount 1000, coins [1,5,10,25,100] ->', big, 'size', len(big))
assert sum(big) == 1000
print('limit =', sys.getrecursionlimit())
try:
    memo_len([1, 7], 1000); print('memo amount 1000 ok')
except RecursionError:
    print('memo amount 1000 with coin 1: RecursionError')
assert coin_list([1], 1000) == [1] * 1000
assert coin_list([7, 3], 2) is None and coin_list([4, 6], 0) == []
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 2, 5] 11 -> [1, 5, 5]
example [2] 3 -> None
example [3, 5] 0 -> []
example [1, 3, 4] 6 -> [3, 3]
example [2, 3] 7 -> [2, 2, 3]
dp[0..11] = [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3]
rebuild (amount, coin taken): [(11, 1), (10, 5), (5, 5)]
cross-check cases 2000 (of which unreachable: 471 )
naive parent pointer, coins looped in INPUT order, differs from the tie rule on 38
naive parent pointer, coins looped ascending, differs on 0
naive parent pointer, coins looped descending, differs on 3
example of a miss (input order): ([4, 6, 5, 3], 9) naive [4, 5] rule [3, 6]
amount 1000, coins [1,5,10,25,100] -> [100, 100, 100, 100, 100, 100, 100, 100, 100, 100] size 10
limit = 1000
memo amount 1000 with coin 1: RecursionError
edge asserts passed
```

**Edge cases:**
- Amount 0: `[]` (not `None`). Unreachable (e.g. `[2]`, 3): `None`.
- Compare to infinity before using `dp[amount]`; a float `inf` or a large sentinel both work, but do not return `-1` here, the prompt says `None`.
- A coin of 1 makes everything reachable.
- Amount 1000 with coin 1 and nothing else: a list of 1000 ones.
- Coins arrive unsorted: sort them before rebuilding (the table does not care).

**Follow-ups:**
- "Count the ways instead?" Coins outer, amount inner (Q10).
- "Why does greedy fail?" Coins `[1,3,4]`, amount 6: greedy takes 4+1+1 (three coins) but 3+3 uses two (Part 8 Q33).
- "Memory for reconstruction?" Storing a coin per amount (`par`) is O(amount) too; the rebuild from `dp` alone costs a coin scan per step but no extra array.

**Common mistakes:**
- Taking the last-found coin (`<=` instead of `<`, or input order) and getting a different optimal multiset.
- Forgetting to sort the output or the coin order, so the list is not non-decreasing.
- `dp` initialised to 0 instead of infinity, so unreachable amounts look free.
- Returning `[]` for unreachable and `None` for 0: swapped.

### Q24 ⭐⭐ 🟡 Jump game as DP versus greedy. `nums` has 1 <= len <= 10^4 non-negative integers; from index i you may jump to any index in i+1..i+nums[i] (clipped at the last index). Return `[can_reach_end, reachable_count]`: whether index len-1 is reachable from index 0, and how many indices (index 0 included) are reachable from 0. Write the DP first (`reach[j]` is True if some reachable i < j has i + nums[i] >= j; O(n^2)), then show the O(n) furthest-reach version and the fact that the reachable set is always a prefix of the indices, which is why the greedy works; the greedy O(n) solution itself is Part 8 Q12 and the minimum-jumps version Part 8 Q13. A DP over jumps of at most k with a monotonic deque is Part 4 Q35. Your submitted solution must be O(n). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a graph search over indices (a stack of reachable indices) and your own O(n^2) DP on small inputs. Example: nums=[2, 3, 1, 1, 4] -> [True, 5]; nums=[3, 2, 1, 0, 4] -> [False, 4]; nums=[0] -> [True, 1]; nums=[1, 0, 5] -> [False, 2]; nums=[2, 0, 0] -> [True, 3].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D reachability DP that collapses to a greedy "furthest reach" scan.

**Say this first (1 line):** "`reach[j]` is true if some reachable `i < j` can hop that far; because everything between a reachable index and its furthest hop is also reachable, I only need to track the single furthest reachable index `R`."

**Brute force:** Graph search over indices: an edge from `i` to every `j` in `i+1..i+nums[i]`; DFS with a stack and a `seen` set from index 0. O(n^2) worst case (each node scans up to `nums[i]` neighbours). That is one oracle; the O(n^2) DP below is the second.

**Optimal:**
- DP definition: `reach[j]` = True if index `j` can be reached from 0. Base `reach[0] = True`. Transition: `reach[j] = any(reach[i] and i + nums[i] >= j for i < j)`. That is O(n^2) time, O(n) space. Answers: `reach[n-1]` and `sum(reach)`.
- Key fact: the reachable set is always a prefix `0..R`. Proof: if `i` is reachable and `nums[i] = k`, every index in `i+1..i+k` is reachable, so there is no gap between a reachable index and the furthest hop taken from it. By induction the set is `{0..R}` where `R` is the largest `i + nums[i]` over reachable `i` (clipped to `n-1`). I tested this on every list of length <= 6 with values 0..3 (5460 lists): the prefix property held on all of them.
- Therefore replace the whole table with one number: scan `i = 0, 1, ...` while `i <= R`; update `R = max(R, i + nums[i])`. Stuck when `i > R`.
- Answers: `can_reach_end = R >= n-1`, `reachable_count = min(R, n-1) + 1`.
- This is the DP with its inner loop collapsed by the prefix property. The greedy solution on its own is Part 8 Q12, the minimum number of jumps is Part 8 Q13, and a DP over jumps of at most `k` with a monotonic deque is Part 4 Q35.

**Complexity:** Time O(n), space O(1). The O(n^2) DP is only used as an oracle. A memoised `can_reach(i)` recursion could nest n = 10^4 deep and raise `RecursionError` at the default limit of 1000, but the loop never recurses.

**Dry run:** `[2,3,1,1,4]`.
- DP table `reach = [T,T,T,T,T]`: `reach[1]` from index 0 (0+2 >= 1), `reach[2]` from 0, `reach[3]` from 1 (1+3 >= 3), `reach[4]` from 1 (1+3 >= 4).
- Greedy: i=0: `R = 2`; i=1: `R = 4`; i=2,3: no change; i=4: `R = 8`, loop ends. `R >= 4` so True, count `min(8, 4) + 1 = 5`.
- `[3,2,1,0,4]`: `R` becomes 3 at i=0 and stays 3. At i=4, `i > R`, stuck: `[False, 4]` (indices 0..3 reachable, the zero at index 3 is the trap).

**Code:**
```python
import random, itertools, sys

random.seed(24)

def dp_reach(nums):
    """O(n^2) DP: reach[j] is True if some reachable i < j has i + nums[i] >= j."""
    n = len(nums); reach = [False] * n; reach[0] = True
    for j in range(1, n):
        reach[j] = any(reach[i] and i + nums[i] >= j for i in range(j))
    return reach

def solve(nums):
    """O(n): furthest reach R. Everything up to R is reachable (prefix), so count = min(R, n-1) + 1."""
    n = len(nums); R = 0; i = 0
    while i <= R and i < n:
        R = max(R, i + nums[i]); i += 1
    return [R >= n - 1, min(R, n - 1) + 1]

def graph_search(nums):
    n = len(nums); seen = {0}; stack = [0]
    while stack:
        i = stack.pop()
        for j in range(i + 1, min(n - 1, i + nums[i]) + 1):
            if j not in seen:
                seen.add(j); stack.append(j)
    return [n - 1 in seen, len(seen)]

def from_dp(nums):
    r = dp_reach(nums); return [r[-1], sum(r)]

for nums, exp in [([2, 3, 1, 1, 4], [True, 5]), ([3, 2, 1, 0, 4], [False, 4]), ([0], [True, 1]), ([1, 0, 5], [False, 2]), ([2, 0, 0], [True, 3])]:
    assert solve(nums) == graph_search(nums) == from_dp(nums) == exp, nums
    print('example', nums, '->', exp)

# walk-through on the first example
nums = [2, 3, 1, 1, 4]
print('DP table reach[j] for', nums, '=', dp_reach(nums))
R = 0
for i, x in enumerate(nums):
    if i > R: break
    R = max(R, i + x); print(f'greedy i={i} nums[i]={x} -> furthest R={R}')
print('answer', solve(nums))
nums = [3, 2, 1, 0, 4]; R = 0
for i, x in enumerate(nums):
    if i > R: print(f'greedy i={i}: i > R={R}, stuck'); break
    R = max(R, i + x); print(f'greedy i={i} nums[i]={x} -> furthest R={R}')

# claim: the reachable set is a prefix of the indices; exhaustive, length <= 6, values 0..3
cnt = 0
for n in range(1, 7):
    for t in itertools.product(range(4), repeat=n):
        l = list(t); r = dp_reach(l)
        k = sum(r)
        assert r == [True] * k + [False] * (n - k), l           # prefix
        assert solve(l) == graph_search(l) == [r[-1], k], l
        cnt += 1
print('exhaustive lists (len <= 6, values 0..3):', cnt, '- reachable set is a prefix on all, greedy = DP = graph search on all')

# seeded random cross-check
for _ in range(600):
    n = random.randint(1, 14); l = [random.choice([0, 0, 1, 1, 2, 3, 5]) for _ in range(n)]
    assert solve(l) == graph_search(l) == from_dp(l), l
print('600 seeded random lists: O(n) == graph search == O(n^2) DP')

# max size (O(n) only)
big = [random.randint(1, 3) for _ in range(10**4)]
print('n = 10^4 result', solve(big))
assert solve([0]) == [True, 1] and solve([1]) == [True, 1] and solve([0, 5]) == [False, 1] and solve([100, 0, 0]) == [True, 3]
print('limit', sys.getrecursionlimit(), '- top-down reach(j) recursion would be up to n = 10^4 deep, so loop')
print('edge asserts passed')
```

**Output (my run):**
```
example [2, 3, 1, 1, 4] -> [True, 5]
example [3, 2, 1, 0, 4] -> [False, 4]
example [0] -> [True, 1]
example [1, 0, 5] -> [False, 2]
example [2, 0, 0] -> [True, 3]
DP table reach[j] for [2, 3, 1, 1, 4] = [True, True, True, True, True]
greedy i=0 nums[i]=2 -> furthest R=2
greedy i=1 nums[i]=3 -> furthest R=4
greedy i=2 nums[i]=1 -> furthest R=4
greedy i=3 nums[i]=1 -> furthest R=4
greedy i=4 nums[i]=4 -> furthest R=8
answer [True, 5]
greedy i=0 nums[i]=3 -> furthest R=3
greedy i=1 nums[i]=2 -> furthest R=3
greedy i=2 nums[i]=1 -> furthest R=3
greedy i=3 nums[i]=0 -> furthest R=3
greedy i=4: i > R=3, stuck
exhaustive lists (len <= 6, values 0..3): 5460 - reachable set is a prefix on all, greedy = DP = graph search on all
600 seeded random lists: O(n) == graph search == O(n^2) DP
n = 10^4 result [True, 10000]
limit 1000 - top-down reach(j) recursion would be up to n = 10^4 deep, so loop
edge asserts passed
```

**Edge cases:**
- `[0]`: already at the end, `[True, 1]`.
- Zero at the start with `n > 1`: `[False, 1]`.
- A huge `nums[i]` is clipped by `min(R, n-1)`; count is not `R + 1`.
- `[1, 0, 5]`: reaches index 1 and stops at the zero: `[False, 2]` (the 5 is unreachable, it does not help).
- Loop condition is `i <= R and i < n`: stop when stuck (`i > R`) or off the end. Do not stop early when `R >= n-1` and then forget that `R` may exceed `n-1` (clip it).

**Follow-ups:**
- "Minimum jumps?" BFS by levels or greedy window (Part 8 Q13).
- "Jumps of at most k with weights/maximise score?" DP plus a monotonic deque (Part 4 Q35).
- "Why can the prefix property fail in other problems?" If you may only jump exactly `nums[i]`, reachable indices have gaps, and the greedy no longer works; use DP or BFS.

**Common mistakes:**
- Treating `nums[i]` as an exact jump length.
- Counting reachable indices as `R + 1` without clipping to `n`.
- Running the O(n^2) DP at n = 10^4 as the submission (the prompt requires O(n)).

### Q25 ⭐⭐ 🟡 Best time to buy and sell stock with a cooldown. `prices` has 0 <= len <= 5000 non-negative integers (price on each day, <= 1000). You may make as many transactions as you like (hold at most one share, buy again only after selling), but after you sell you cannot buy the next day. Return the maximum profit (0 for an empty list). Define the three states holding, just-sold and free-to-buy, give the transitions per day, and say what changes if you drop the cooldown (the three states collapse to two, and the problem becomes unlimited transactions, a variant of the one-transaction problem of Q4). Sizes go well past 1000, so a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and fail with RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the day and a holding flag (len <= 10) on small inputs. Example: prices=[1, 2, 3, 0, 2] -> 3; prices=[1] -> 0; prices=[] -> 0; prices=[6, 1, 3, 2, 4, 7] -> 6.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Stock-trading state-machine write-ups (techinterview.org DP state machine patterns, labuladong stock guide, system.design state-machine notes, a LeetCode Discuss single-template post; search snippets only, not opened)

**Pattern:** State-machine DP over days (three states), O(1) rolling space.

**Say this first (1 line):** "Each day I am in one of three states: holding, just sold today, or free to buy; the cooldown is just that 'sold' cannot go straight to 'hold'."

**Brute force:** Plain recursion `f(day, holding)`: do nothing; or if holding, sell and jump to `day + 2` (the next day is the cooldown); or if not holding, buy and go to `day + 1`. Exponential without a cache, fine for len <= 10. It is the oracle.

**Optimal:**
- States at the end of day `i`: `hold[i]` = best profit ending the day holding a share; `sold[i]` = best profit if I sold today; `free[i]` = best profit ending the day with no share and allowed to buy tomorrow.
- Transitions with price `p`: `hold = max(hold, free - p)` (keep holding, or buy today from the free state); `sold = hold_prev + p` (sell the share I held yesterday); `free = max(free, sold_prev)` (stay free, or the cooldown day just ended).
- Why buying only from `free`: a share bought the day after selling would come from `sold`, which is exactly the cooldown. `sold` must pass through `free` first.
- Base: `hold = -inf`, `sold = -inf`, `free = 0` before day 1. Answer `max(sold, free)` at the end (ending while holding is never better). Empty list: 0.
- Rolling variables: the three new values depend only on the three old ones, so update them in one tuple assignment (the right-hand side uses the old values). Space O(1).
- Dropping the cooldown: `sold` and `free` merge into one state "not holding" (`cash = max(cash, hold + p)`), so two states, and the problem is unlimited transactions. The answer is then the sum of positive day-to-day rises, which is the unlimited-transactions variant of the one-transaction problem in Q4. I checked on all 800 random cases that the two-state value equals that sum, and that it was strictly larger than the cooldown answer on 254 of them (never smaller).

**Complexity:** Time O(n), space O(1). The memoised `f(day, holding)` has about 2n states but nests up to n deep. At 5000 days it raises `RecursionError` at the default limit of 1000 (shown in the run), so bottom-up is required.

**Dry run:** `[1, 2, 3, 0, 2]` (table printed below).
- Day 1 (p=1): hold -1 (buy), free 0.
- Day 2 (p=2): sold = -1 + 2 = 1; hold stays -1; free 0.
- Day 3 (p=3): sold = -1 + 3 = 2; free = max(0, sold_prev 1) = 1.
- Day 4 (p=0): hold = max(-1, free_prev 1 - 0) = 1; sold = -1 + 0 = -1; free = max(1, 2) = 2.
- Day 5 (p=2): sold = 1 + 2 = 3; free = max(2, -1) = 2. Answer `max(3, 2) = 3`: buy 1, sell 2, cooldown, buy 0, sell 2.

**Code:**
```python
import random, sys
from functools import cache

random.seed(25)
NEG = float('-inf')

def cooldown(prices):
    """Bottom-up, O(1) space. States at the END of each day:
    hold = best profit while holding a share; sold = best profit if I sold today; free = best profit, no share, free to buy."""
    hold, sold, free = NEG, NEG, 0
    for p in prices:
        hold, sold, free = max(hold, free - p), hold + p, max(free, sold)
    return max(sold, free)

def cooldown_table(prices):
    """Same thing with full arrays, to print the walk-through."""
    hold, sold, free = [NEG], [NEG], [0]
    for p in prices:
        hold.append(max(hold[-1], free[-1] - p)); sold.append(hold[-2] + p); free.append(max(free[-1], sold[-2]))
    return hold, sold, free

def no_cooldown(prices):
    """Drop the cooldown: sold and free merge into one 'not holding' state."""
    hold, cash = NEG, 0
    for p in prices:
        hold, cash = max(hold, cash - p), max(cash, hold + p)
    return cash

def rises(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))

def memo(prices):
    n = len(prices)
    @cache
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)                                 # do nothing today
        if holding: best = max(best, prices[i] + f(i + 2, False))   # sell today; day i+1 is the cooldown day
        else: best = max(best, -prices[i] + f(i + 1, True))        # buy today
        return best
    return f(0, False)

def brute(prices):
    """Plain recursion over (day, holding), no cache."""
    n = len(prices)
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)
        if holding: best = max(best, prices[i] + f(i + 2, False))
        else: best = max(best, -prices[i] + f(i + 1, True))
        return best
    return f(0, False)

for pr, exp in [([1, 2, 3, 0, 2], 3), ([1], 0), ([], 0), ([6, 1, 3, 2, 4, 7], 6)]:
    assert cooldown(pr) == brute(pr) == memo(pr) == exp, pr
    print('example', pr, '->', exp)

h, s, f = cooldown_table([1, 2, 3, 0, 2])
print('day  price  hold  sold  free')
print('  0      -    ', h[0], s[0], f[0])
for i, p in enumerate([1, 2, 3, 0, 2], 1):
    print(f'  {i}    {p:3d}   {h[i]:4}  {s[i]:4}  {f[i]:4}')
print('answer = max(sold, free) at the end =', max(s[-1], f[-1]))

n_cases = 0; cd_lt = 0
for _ in range(800):
    n = random.randint(0, 10); pr = [random.randint(0, 9) for _ in range(n)]
    want = brute(pr)
    assert cooldown(pr) == want == memo(pr), pr
    nc = no_cooldown(pr)
    assert nc == rises(pr) and nc >= want       # without the cooldown it is the sum of positive daily rises
    n_cases += 1; cd_lt += nc > want
print('cross-check cases', n_cases, '| no-cooldown value strictly larger on', cd_lt, '| no-cooldown == sum of positive rises on all')

# max size: bottom-up fine, memo recursion not
big = [random.randint(0, 1000) for _ in range(5000)]
print('n = 5000 profit', cooldown(big))
print('limit =', sys.getrecursionlimit())
try:
    memo(big); print('memo n=5000 ok')
except RecursionError:
    print('memo n=5000: RecursionError')
assert cooldown([5, 4, 3]) == 0 and cooldown([1, 5]) == 4 and cooldown([2, 2, 2]) == 0
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 2, 3, 0, 2] -> 3
example [1] -> 0
example [] -> 0
example [6, 1, 3, 2, 4, 7] -> 6
day  price  hold  sold  free
  0      -     -inf -inf 0
  1      1     -1  -inf     0
  2      2     -1     1     0
  3      3     -1     2     1
  4      0      1    -1     2
  5      2      1     3     2
answer = max(sold, free) at the end = 3
cross-check cases 800 | no-cooldown value strictly larger on 254 | no-cooldown == sum of positive rises on all
n = 5000 profit 665818
limit = 1000
memo n=5000: RecursionError
edge asserts passed
```

**Edge cases:**
- Empty list or one price: 0.
- Strictly decreasing prices: 0.
- Prices equal: 0.
- Two days `[1, 5]`: 4.
- Do not allow ending with a negative: `max(sold, free)` handles it, `hold` is never the answer.

**Follow-ups:**
- "Add a transaction fee?" Subtract the fee when selling (or buying); the states stay the same.
- "At most k transactions?" See Q29.
- "Cooldown of c days?" Track the last c days of `sold` (or add c rest states).

**Common mistakes:**
- Letting `buy` read `sold` of the previous day (no cooldown at all).
- Using already-updated values inside the same day (writing the three updates as separate statements).
- Starting `hold` at 0 instead of -infinity (a free share).
- Returning `hold` at the end.

### Q26 ⭐⭐ 🟡 Maximum sum circular subarray. `nums` has 1 <= len <= 10^5 integers (|value| <= 10^4) arranged in a circle. A subarray is non-empty and contiguous around the circle; it may wrap from the end to the start but may use each element at most once (it can be the whole list). Return its maximum sum. Explain the two cases (a normal subarray, or a wrapping one equal to the total minus a minimum middle subarray) and the all-negative edge case where the wrapping formula would wrongly allow an empty subarray. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) enumeration of every circular subarray on small inputs. Example: nums=[1, -2, 3, -2] -> 3; nums=[5, -3, 5] -> 10; nums=[-3, -2, -3] -> -2; nums=[3, -1, 2, -1] -> 4; nums=[4] -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Kadane twice (max and min), the circular case as "total minus the minimum middle".

**Say this first (1 line):** "Either the best subarray does not wrap, which is plain Kadane, or it wraps, and then what is left out is a contiguous middle block, so the wrapped sum is the total minus the minimum subarray."

**Brute force:** Every start `s` and every length `L` from 1 to `n`, summing `nums[(s+k) % n]`. O(n^2) with a running sum. It is the oracle.

**Optimal:**
- Case 1 (no wrap): the best subarray lies inside the list, so it is the ordinary Kadane maximum `mx`. State: `cur[i]` = best sum ending at `i`, `cur[i] = max(x, cur[i-1] + x)`.
- Case 2 (wrap): the chosen arc uses a suffix and a prefix. What it leaves out is a contiguous block in the middle. Its sum is `total - leftover`, so to maximise it, minimise the leftover: `total - mn` where `mn` is the minimum-sum subarray (second Kadane with `min`).
- Answer: `max(mx, total - mn)`.
- The all-negative trap: if every element is negative, the minimum subarray is the whole list, so `total - mn = 0`, which corresponds to taking NOTHING, an empty subarray that is not allowed. The formula would then return 0, higher than every legal answer. Fix: if `mx < 0` (all elements negative), return `mx`. (If `mx >= 0`, the value `total - mn` is at most the total of a non-empty arc whenever the minimum block is not the whole list, and when it is the whole list the term is 0 which does not beat `mx >= 0`.)
- I checked exactly this: on all 19607 lists of length 1..5 with values -3..3, the fixed version matches the circular enumeration; the naive formula `max(mx, total - mn)` is wrong on 363 of them and every one of those is an all-negative list.
- Space O(1), single pass possible.

**Complexity:** Time O(n), space O(1). Loops only; no recursion.

**Dry run:** `[5, -3, 5]`: total 7. Normal Kadane gives 7 (the whole list, which is a legal arc). Minimum subarray is `[-3]` with sum -3. Wrap value: `7 - (-3) = 10`, which is the arc `5, 5` going around the end back to the start. Answer 10. For `[-3, -2, -3]`: `mx = -2`, `mn = -8`, `total - mn = 0` would be empty, so return `-2`.

**Code:**
```python
import random, itertools

random.seed(26)

def kadane_max_min(nums):
    mx = cur = mn = curm = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x); mx = max(mx, cur)
        curm = min(x, curm + x); mn = min(mn, curm)
    return mx, mn

def circular(nums):
    """max(best normal subarray, total - min subarray), except when every element is negative (then the
    minimum subarray is the whole list and total - mn = 0 would be an EMPTY subarray)."""
    mx, mn = kadane_max_min(nums)
    if mx < 0:
        return mx
    return max(mx, sum(nums) - mn)

def naive(nums):
    mx, mn = kadane_max_min(nums)
    return max(mx, sum(nums) - mn)

def brute(nums):
    n = len(nums); best = None
    for s in range(n):
        tot = 0
        for L in range(1, n + 1):
            tot += nums[(s + L - 1) % n]
            if best is None or tot > best: best = tot
    return best

for nums, exp in [([1, -2, 3, -2], 3), ([5, -3, 5], 10), ([-3, -2, -3], -2), ([3, -1, 2, -1], 4), ([4], 4)]:
    assert circular(nums) == brute(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [5, -3, 5]
mx, mn = kadane_max_min(nums)
print('walk-through', nums, ': total', sum(nums), '| best normal', mx, '| min middle', mn, '| wrap =', sum(nums), '-', mn, '=', sum(nums) - mn, '| answer', circular(nums))
nums = [-3, -2, -3]
mx, mn = kadane_max_min(nums)
print('all-negative', nums, ': best normal', mx, '| min', mn, '| total - min =', sum(nums) - mn, '(empty subarray!) | answer', circular(nums))

# exhaustive: every list of length 1..5 with values -3..3, plus seeded random
cnt = bad_naive = 0
for n in range(1, 6):
    for t in itertools.product(range(-3, 4), repeat=n):
        l = list(t); assert circular(l) == brute(l), l
        cnt += 1; bad_naive += naive(l) != brute(l)
print('exhaustive lists', cnt, '| naive formula wrong on', bad_naive)
allneg_bad = 0
for n in range(1, 6):
    for t in itertools.product(range(-3, 4), repeat=n):
        l = list(t)
        if naive(l) != brute(l):
            assert max(l) < 0; allneg_bad += 1
print('every naive failure is an all-negative list:', allneg_bad == bad_naive)
for _ in range(500):
    n = random.randint(1, 12); l = [random.randint(-9, 9) for _ in range(n)]
    assert circular(l) == brute(l), l
print('500 seeded random lists agree with the O(n^2) circular enumeration')

big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
print('n = 10^5 answer', circular(big))
assert circular([4]) == 4 and circular([-1]) == -1 and circular([2, 2]) == 4 and circular([-1, 5, -1]) == 5
print('edge asserts passed')
```

**Output (my run):**
```
example [1, -2, 3, -2] -> 3
example [5, -3, 5] -> 10
example [-3, -2, -3] -> -2
example [3, -1, 2, -1] -> 4
example [4] -> 4
walk-through [5, -3, 5] : total 7 | best normal 7 | min middle -3 | wrap = 7 - -3 = 10 | answer 10
all-negative [-3, -2, -3] : best normal -2 | min -8 | total - min = 0 (empty subarray!) | answer -2
exhaustive lists 19607 | naive formula wrong on 363
every naive failure is an all-negative list: True
500 seeded random lists agree with the O(n^2) circular enumeration
n = 10^5 answer 2416709
edge asserts passed
```

**Edge cases:**
- Single element: itself (`[4] -> 4`, `[-1] -> -1`).
- All negative: the largest element.
- Mixed with total negative: the answer is a normal subarray; the wrap term is smaller.
- The whole list is allowed (each element at most once), so Kadane's whole-list case is legal.
- Zeros: no special handling.

**Follow-ups:**
- "Do it without a second Kadane?" Use prefix sums and a deque for sliding-window minimum on a doubled array (O(n), more code).
- "Maximum product circular?" Not the same trick; negatives flip.
- "Return the arc too?" Carry start indexes (Q22) and, for the wrap case, the complement of the min block.

**Common mistakes:**
- Forgetting the all-negative case and returning 0.
- Checking `total == mn` instead of `mx < 0` (the `mx < 0` test is the clean one).
- Letting the wrapped arc use an element twice (doubled array with window length > n).
- Initialising `mx = 0` or `mn = 0` instead of `nums[0]`.

### Q27 ⭐⭐ 🟡 Delete and earn. `nums` has 0 <= len <= 2*10^4 integers in 1..10^4. In one move pick a value x present in the list: you earn x points for EVERY copy of x, and then every copy of x - 1 and x + 1 is deleted (the other copies of x are consumed by the move). Moves repeat until nothing is left that you want. Return the maximum points (0 for an empty list). Show the reduction to house robber (Q5) over a table indexed by value and why copies of the same value always go together. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all sets of distinct values with no two consecutive integers on small inputs. Example: nums=[3, 4, 2] -> 6; nums=[2, 2, 3, 3, 3, 4] -> 9; nums=[] -> 0; nums=[1, 1, 1, 2, 4, 5, 5, 5, 6] -> 18.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Reduction to House Robber (Q5) on a table indexed by value.

**Say this first (1 line):** "Pick value `x` and you take all copies and lose `x-1` and `x+1`, so build `tot[v] = v * count(v)` and the question becomes: choose values with no two adjacent, maximise the sum. That is House Robber."

**Brute force:** Enumerate every subset of the distinct values with no two consecutive integers, score `sum(v * count(v))`. O(2^d) for d distinct values. A second oracle simulates the game itself on small lists (pick a value, remove it and its neighbours, recurse).

**Optimal:**
- Why copies go together: choosing `x` once earns `x` for every copy, and the rule consumes all other copies of `x` in the same move. So there is no case where taking only some copies is possible or better, and after taking `x` the same neighbours `x-1`, `x+1` are gone either way. Each distinct value is a take-all or skip decision.
- Table: `tot[v] = v * count(v)` for `v = 0..max(nums)`; missing values have 0.
- State: `best[v]` = best total using values `<= v`. Transition: `best[v] = max(best[v-1], best[v-2] + tot[v])` (skip v, or take v and so skip v-1). Base `best[0] = 0` (and `best[-1] = 0`).
- Rolling form: `take, skip = skip + tot[v], max(take, skip)`. Answer `max(take, skip)`. Space O(max value) for the table, O(1) beyond it.
- Gaps are harmless: a value with `tot = 0` is simply never needed, and two values differing by 2 or more do not conflict, which the recurrence reflects since it only links `v` to `v-1`.
- Empty list: 0.

**Complexity:** Time O(n + M) where M = max value (10^4 here), space O(M). Memoised recursion `f(v)` nests M = 10^4 deep: it raises `RecursionError` at the default limit of 1000 (shown in the run), so use the loop.

**Dry run:** `[2, 2, 3, 3, 3, 4]`: `tot = [0, 0, 4, 9, 4]`.
- v=2: take 4, skip 0.
- v=3: take = skip_prev + 9 = 9; skip = max(4, 0) = 4.
- v=4: take = skip_prev 4 + 4 = 8; skip = max(9, 4) = 9.
- Answer 9: take all three 3s, losing the 2s and the 4.

**Code:**
```python
import random, sys
from collections import Counter
from functools import cache

random.seed(27)

def delete_and_earn(nums):
    """Reduce to house robber over values: tot[v] = v * count(v); picking v forbids v-1 and v+1."""
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    take, skip = 0, 0                    # take = best with the previous value taken, skip = best with it not taken
    for v in range(len(tot)):
        take, skip = skip + tot[v], max(take, skip)
    return max(take, skip)

def rob(a):
    """House robber, rolling: prev2, prev1."""
    p2 = p1 = 0
    for v in a: p2, p1 = p1, max(p1, p2 + v)
    return p1

def via_robber(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    return rob(tot)

def memo(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    @cache
    def f(i):
        if i < 0: return 0
        return max(f(i - 1), f(i - 2) + tot[i])
    return f(len(tot) - 1)

def brute(nums):
    """All sets of distinct values with no two consecutive integers."""
    c = Counter(nums); vals = sorted(c); best = 0
    for m in range(1 << len(vals)):
        ch = [vals[i] for i in range(len(vals)) if m >> i & 1]
        if all(ch[i + 1] - ch[i] > 1 for i in range(len(ch) - 1)):
            best = max(best, sum(v * c[v] for v in ch))
    return best

def simulate(nums):
    """Direct simulation of the game on small lists (picks one value at a time), to justify the reduction."""
    @cache
    def g(state):
        best = 0
        for v in set(state):
            rest = tuple(sorted(y for y in state if y != v and y != v - 1 and y != v + 1))
            best = max(best, v * state.count(v) + g(rest))
        return best
    return g(tuple(sorted(nums)))

for nums, exp in [([3, 4, 2], 6), ([2, 2, 3, 3, 3, 4], 9), ([], 0), ([1, 1, 1, 2, 4, 5, 5, 5, 6], 18)]:
    assert delete_and_earn(nums) == brute(nums) == via_robber(nums) == memo(nums) == simulate(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [2, 2, 3, 3, 3, 4]
tot = [0] * (max(nums) + 1)
for x in nums: tot[x] += x
print('tot by value 0..4 =', tot)
take, skip = 0, 0
for v in range(len(tot)):
    take, skip = skip + tot[v], max(take, skip)
    print(f'value {v}: tot={tot[v]:2d}  best if value {v} taken={take:2d}  best if not taken={skip:2d}')
print('answer', max(take, skip))

for _ in range(800):
    n = random.randint(0, 9); l = [random.randint(1, 8) for _ in range(n)]
    want = brute(l)
    assert delete_and_earn(l) == want == via_robber(l) == memo(l), l
    assert simulate(l) == want, l
print('800 seeded random lists: DP == subset enumeration == game simulation == memo')

big = [random.randint(1, 10**4) for _ in range(2 * 10**4)]
print('n = 2*10^4, values <= 10^4 answer', delete_and_earn(big))
print('limit =', sys.getrecursionlimit())
try:
    memo([10**4]); print('memo ok')
except RecursionError:
    print('memo over a value table of 10^4 slots: RecursionError')
assert delete_and_earn([1]) == 1 and delete_and_earn([5, 5, 5]) == 15 and delete_and_earn([1, 2]) == 2
print('edge asserts passed')
```

**Output (my run):**
```
example [3, 4, 2] -> 6
example [2, 2, 3, 3, 3, 4] -> 9
example [] -> 0
example [1, 1, 1, 2, 4, 5, 5, 5, 6] -> 18
tot by value 0..4 = [0, 0, 4, 9, 4]
value 0: tot= 0  best if value 0 taken= 0  best if not taken= 0
value 1: tot= 0  best if value 1 taken= 0  best if not taken= 0
value 2: tot= 4  best if value 2 taken= 4  best if not taken= 0
value 3: tot= 9  best if value 3 taken= 9  best if not taken= 4
value 4: tot= 4  best if value 4 taken= 8  best if not taken= 9
answer 9
800 seeded random lists: DP == subset enumeration == game simulation == memo
n = 2*10^4, values <= 10^4 answer 60911434
limit = 1000
memo over a value table of 10^4 slots: RecursionError
edge asserts passed
```

**Edge cases:**
- Empty list: 0 (guard `max(nums)`; `max([])` raises `ValueError`).
- One distinct value with many copies: `v * count`.
- All values consecutive (`[1,2]`): 2, not 3.
- Large gaps: the table is mostly zeros; fine at M = 10^4. If values were up to 10^9, sort the distinct values and compare only with the previous distinct value (check `v - prev == 1`).

**Follow-ups:**
- "Values up to 10^9?" Work over sorted distinct values and keep the two previous states, resetting when the gap is > 1.
- "House Robber on a circle?" Run twice, excluding the first or the last (Part 7 Q45 is the tree version).
- "Why not greedy (take the largest value first)?" On `[2,2,3,3,3,4]` it takes the 4 (4 points), loses the 3s, then takes the 2s (4): 8, but the best is 9 (all the 3s).

**Common mistakes:**
- Counting `v` once instead of `v * count(v)`.
- Linking `v` to `v-1` in the list index of the sorted array instead of the value table (gaps then break adjacency).
- Calling `max(nums)` on an empty list.
- Memoised recursion over a 10^4-slot table.

### Q28 ⭐⭐ 🔴 Number of longest increasing subsequences. `nums` has 0 <= len <= 2000 integers (|value| <= 10^6, repeats allowed). Return `[L, count]`: L is the length of the longest strictly increasing subsequence and `count` the number of index sets (subsequences chosen by position, so equal values at different positions count separately) that achieve it; return [0, 0] for an empty list. Keep two arrays per index (best length ending here, how many ways) and explain the update when a longer length is found and when an equal one is found. State the time (O(n^2)) and how the O(n log n) bisect method (Q7) differs: it gives the length but not the count without extra bookkeeping. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsequences (len <= 12) on small inputs. Example: nums=[1, 3, 5, 4, 7] -> [4, 2]; nums=[2, 2, 2, 2, 2] -> [1, 5]; nums=[] -> [0, 0]; nums=[1, 2, 4, 3, 5, 4, 7, 2] -> [5, 3]; nums=[5, 4, 3] -> [1, 3].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** O(n^2) LIS DP carrying a second array (counts), the "count the optimal solutions" DP.

**Say this first (1 line):** "For each index I store the longest increasing run ending there and how many runs achieve it; a longer predecessor replaces the count, an equally long one adds to it."

**Brute force:** Enumerate all 2^n subsets by position, keep the strictly increasing ones, track the longest length and how many reach it. O(2^n * n); fine for n <= 12. It is the oracle.

**Optimal:**
- State: `length[i]` = length of the longest strictly increasing subsequence ending at index `i`; `ways[i]` = number of such subsequences of that length ending at `i` (counted by position, so equal values at different positions are different).
- Base: `length[i] = 1`, `ways[i] = 1` (the element alone).
- Transition: for each `j < i` with `nums[j] < nums[i]`, the candidate length is `length[j] + 1`.
  - If it is strictly greater than `length[i]`: set `length[i] = length[j] + 1` and `ways[i] = ways[j]` (the old count described shorter runs and is thrown away).
  - If it equals `length[i]`: `ways[i] += ways[j]` (a second family of equally long runs).
  - If smaller: ignore.
- Answer: `L = max(length)`, `count = sum(ways[i] for i with length[i] == L)`. A run of length `L` ends somewhere, and the ends are distinct positions, so we add over all of them. Empty list: `[0, 0]`.
- Why the counts are right: a longest run ending at `i` has a unique predecessor position `j`, and its first `length-1` elements form a longest run ending at `j`. So the runs ending at `i` split by predecessor, and each class has `ways[j]` members.
- Equal values: `nums[j] < nums[i]` is strict, so equal values never chain; `[2,2,2,2,2]` gives `[1, 5]`.
- Versus the O(n log n) bisect method (Q7): `tails` only keeps the smallest tail per length, so it throws away how many ways there were. It gives `L` (my run shows it equals `L` on all 700 cases) but not the count unless you extend each pile with counts (more bookkeeping).

**Complexity:** Time O(n^2) (n = 2000 means about 2 million inner steps), space O(n). Recursion limit: the top-down memo over `(index)` nests as deep as the dependency chain. In the run, on the increasing list `0..1999` the version whose inner loop runs `j` descending raised `RecursionError` at the default limit of 1000, while the ascending-`j` version computed the small indices first and did not (a fragile accident of loop order). The prompt does not force bottom-up, but I use the loops because their depth is always 1.

**Dry run:** `[1, 3, 5, 4, 7]` (table printed below).
- 1: length 1, ways 1.
- 3: from 1: length 2, ways 1.
- 5: from 1 (length 2, replace), from 3 (length 3 > 2, replace): length 3, ways 1.
- 4: from 1: 2; from 3: 3 (replace): length 3, ways 1.
- 7: from 1: 2; from 3: 3; from 5: 4 (replace, ways 1); from 4: 4 equals, add ways 1: length 4, ways 2.
- `L = 4`, count 2 (`1,3,5,7` and `1,3,4,7`).

**Code:**
```python
import random, sys, bisect
from functools import cache

random.seed(28)

def count_lis(nums):
    """O(n^2). length[i] = longest strictly increasing subsequence ENDING at i, ways[i] = how many (by position)."""
    n = len(nums)
    if n == 0: return [0, 0]
    length = [1] * n; ways = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i], ways[i] = length[j] + 1, ways[j]      # strictly longer: replace the count
                elif length[j] + 1 == length[i]:
                    ways[i] += ways[j]                               # equally long: add the counts
    L = max(length)
    return [L, sum(w for l, w in zip(length, ways) if l == L)]

def tables(nums):
    n = len(nums); length = [1] * n; ways = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]: length[i], ways[i] = length[j] + 1, ways[j]
                elif length[j] + 1 == length[i]: ways[i] += ways[j]
    return length, ways

def lis_len_bisect(nums):
    tails = []
    for x in nums:
        k = bisect.bisect_left(tails, x)
        if k == len(tails): tails.append(x)
        else: tails[k] = x
    return len(tails)

def memo(nums):
    n = len(nums)
    @cache
    def f(i):                       # (length ending at i, ways)
        best, w = 1, 1
        for j in range(i):
            if nums[j] < nums[i]:
                l, c = f(j)
                if l + 1 > best: best, w = l + 1, c
                elif l + 1 == best: w += c
        return best, w
    if n == 0: return [0, 0]
    res = [f(i) for i in range(n)]       # forward order keeps the recursion shallow in this test; see text
    L = max(l for l, _ in res)
    return [L, sum(c for l, c in res if l == L)]

def brute(nums):
    n = len(nums); best = 0; cnt = 0
    for m in range(1, 1 << n):
        v = [nums[i] for i in range(n) if m >> i & 1]
        if all(v[i] < v[i + 1] for i in range(len(v) - 1)):
            if len(v) > best: best, cnt = len(v), 1
            elif len(v) == best: cnt += 1
    return [best, cnt] if n else [0, 0]

for nums, exp in [([1, 3, 5, 4, 7], [4, 2]), ([2, 2, 2, 2, 2], [1, 5]), ([], [0, 0]),
                  ([1, 2, 4, 3, 5, 4, 7, 2], [5, 3]), ([5, 4, 3], [1, 3])]:
    assert count_lis(nums) == brute(nums) == memo(nums) == exp, nums
    print('example', nums, '->', exp)

nums = [1, 3, 5, 4, 7]
ln, wy = tables(nums)
print('i   x  length ways')
for i, x in enumerate(nums): print(f'{i}  {x:2d}  {ln[i]:5d} {wy[i]:4d}')
print('L =', max(ln), '| count = sum of ways where length == L =', sum(w for l, w in zip(ln, wy) if l == max(ln)))

cases = 0; bisect_agree = 0
for _ in range(700):
    n = random.randint(0, 12); l = [random.randint(-4, 6) for _ in range(n)]
    assert count_lis(l) == brute(l) == memo(l), l
    assert lis_len_bisect(l) == count_lis(l)[0]
    cases += 1
print('cross-check cases', cases, '| bisect_left length equals L on all (it gives the length, not the count)')

big = [random.randint(-10**6, 10**6) for _ in range(2000)]
print('n = 2000 random:', count_lis(big))
inc = list(range(2000))
print('n = 2000 increasing:', count_lis(inc))
print('n = 2000 all equal:', count_lis([7] * 2000))
print('limit =', sys.getrecursionlimit())
def top_down(seq, order):
    @cache
    def g(i):
        best, w = 1, 1
        for j in order(i):
            if seq[j] < seq[i]:
                l, c = g(j)
                if l + 1 > best: best, w = l + 1, c
                elif l + 1 == best: w += c
        return best, w
    return g
for name, order in (('j ascending', lambda i: range(i)), ('j descending', lambda i: reversed(range(i)))):
    try:
        top_down(inc, order)(1999); print('top-down, inner loop', name, ': ok on 0..1999 increasing')
    except RecursionError:
        print('top-down, inner loop', name, ': RecursionError on 0..1999 increasing')
assert count_lis([9]) == [1, 1] and count_lis([1, 2]) == [2, 1]
print('edge asserts passed')
```

**Output (my run):**
```
example [1, 3, 5, 4, 7] -> [4, 2]
example [2, 2, 2, 2, 2] -> [1, 5]
example [] -> [0, 0]
example [1, 2, 4, 3, 5, 4, 7, 2] -> [5, 3]
example [5, 4, 3] -> [1, 3]
i   x  length ways
0   1      1    1
1   3      2    1
2   5      3    1
3   4      3    1
4   7      4    2
L = 4 | count = sum of ways where length == L = 2
cross-check cases 700 | bisect_left length equals L on all (it gives the length, not the count)
n = 2000 random: [87, 9256960]
n = 2000 increasing: [2000, 1]
n = 2000 all equal: [1, 2000]
limit = 1000
top-down, inner loop j ascending : ok on 0..1999 increasing
top-down, inner loop j descending : RecursionError on 0..1999 increasing
edge asserts passed
```

**Edge cases:**
- Empty list: `[0, 0]` (not `[0, 1]`).
- All equal: `[1, n]`.
- Strictly decreasing: `[1, n]`.
- Strictly increasing: `[n, 1]`.
- Counts can be huge in other variants; here Python integers are exact (a random 2000-list gave 9256960).

**Follow-ups:**
- "Count in O(n log n)?" Use a Fenwick tree or segment tree over values storing `(length, count)` pairs and merge by max length (adding counts on ties).
- "Non-decreasing?" Change `<` to `<=`; equal values then chain.
- "Return one LIS?" Q34 (tie rule and rebuild).

**Common mistakes:**
- Setting `ways[i] += ways[j]` when the length is greater instead of replacing.
- Summing `ways` over all `i` instead of only those with `length == L`.
- Counting distinct value sequences instead of index sets.
- Returning `[0, 1]` for the empty list.

### Q29 ⭐⭐ 🔴 Best time to buy and sell stock with at most k transactions. `prices` has 0 <= len <= 1000 non-negative integers (<= 1000) and `k` is 0 <= k <= 10^9; a transaction is one buy and the later sell of that share, and you hold at most one share at a time. Return the maximum profit. Define the states (buy[j], sell[j] for j transactions), give the O(n * k) table with O(k) space, and say why k >= len // 2 can be treated as 'unlimited transactions' (sum of positive day-to-day rises), which also keeps the table small when k is huge. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over day, transactions left and holding flag (len <= 8) on small inputs. Example: k=2, prices=[3, 2, 6, 5, 0, 3] -> 7; k=1, prices=[7, 6, 4, 3, 1] -> 0; k=1000000000, prices=[1, 5, 2, 8, 3, 9] -> 16; k=0, prices=[1, 9] -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Stock-trading state-machine write-ups (techinterview.org DP state machine patterns, labuladong stock guide, system.design state-machine notes, a LeetCode Discuss single-template post; search snippets only, not opened)

**Pattern:** State-machine DP with a transaction counter (buy[j], sell[j]), plus a cap on useful `k`.

**Say this first (1 line):** "`buy[j]` is the best profit while holding the share of my j-th transaction, `sell[j]` after finishing j transactions; each day updates both, and if `k >= n // 2` the limit never binds, so it is just the sum of positive rises."

**Brute force:** Recursion over `(day, transactions left, holding)`: skip, sell if holding, buy if not holding and a transaction is left. Exponential without a cache; I use it for len <= 8. A memoised version has `n * k * 2` states.

**Optimal:**
- State: `buy[j]` = max profit so far if I currently hold a share bought as my j-th transaction; `sell[j]` = max profit so far having completed j transactions and holding nothing. Counting a transaction at the buy keeps the bookkeeping simple.
- Base: `sell[0] = 0`, `buy[j] = -inf` and `sell[j] = 0` for `j >= 1` (doing fewer transactions is always allowed, so 0 is right).
- Transition, for each price `p` and `j = 1..k`: `buy[j] = max(buy[j], sell[j-1] - p)`; `sell[j] = max(sell[j], buy[j] + p)`. Answer `sell[k]`.
- Space: only the previous day's values are needed, and the arrays are indexed by `j`, so O(k) (the code overwrites in place; updating `buy[j]` before `sell[j]` on the same day can only allow a buy and a sell at the same price, which adds 0 profit and is harmless).
- Why `k >= n // 2` means unlimited: a transaction needs a buy day and a later sell day, so at most `n // 2` disjoint transactions fit in `n` days. With `k >= n // 2` the limit never binds, so the answer equals the unlimited answer, the sum of positive day-to-day rises. Exhaustively checked: on all 21845 lists of length <= 7 with values 0..3, `table(k) == unlimited` for every k from `n // 2` up. The bound is also tight: for `[0, 1, 0, 1]`, `k = 1` gives 1 but unlimited gives 2.
- Why it keeps the table small when `k = 10^9`: without the cap the `buy`/`sell` arrays would have 10^9 entries. With the cap `k` is replaced by the shortcut, and when `k < n // 2` the arrays have at most 500 entries here.
- Degenerate cases: `k = 0` or fewer than 2 days: 0.

**Complexity:** Time O(n * min(k, n // 2)) = at most 1000 * 500 here, space O(min(k, n // 2)). Memoised recursion over days nests n = 1000 deep and raises `RecursionError` at the default limit of 1000 (shown in the run), so bottom-up is the answer.

**Dry run:** `k=2`, `[3, 2, 6, 5, 0, 3]` (table printed below).
- Best first trade: buy 2, sell 6 (+4); second: buy 0, sell 3 (+3). Total 7.
- In the table `buy1` ends at 0 (the share bought at price 0 costs `-0`), `sell1 = 4`, `buy2 = sell1 - 0 = 4`, `sell2 = 4 + 3 = 7`.

**Code:**
```python
import random, sys
from functools import cache

random.seed(29)
NEG = float('-inf')

def table_k(k, prices):
    """O(n*k) time, O(k) space. buy[j] = best profit holding a share during the j-th transaction,
    sell[j] = best profit after completing j transactions."""
    buy = [NEG] * (k + 1); sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]

def unlimited(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))

def solve(k, prices):
    n = len(prices)
    if n < 2 or k == 0: return 0
    if k >= n // 2: return unlimited(prices)     # at most n // 2 transactions can ever be useful
    return table_k(k, prices)

def memo(k, prices):
    n = len(prices)
    @cache
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)

def brute(k, prices):
    n = len(prices)
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)

for k, pr, exp in [(2, [3, 2, 6, 5, 0, 3], 7), (1, [7, 6, 4, 3, 1], 0), (10**9, [1, 5, 2, 8, 3, 9], 16), (0, [1, 9], 0)]:
    assert solve(k, pr) == brute(k, pr) == exp, (k, pr)
    print('example k =', k, pr, '->', exp)

# walk-through for the first example
k, pr = 2, [3, 2, 6, 5, 0, 3]
buy = [NEG] * (k + 1); sell = [0] * (k + 1)
print('day price | buy1 sell1 buy2 sell2')
for d, p in enumerate(pr):
    for j in range(1, k + 1):
        buy[j] = max(buy[j], sell[j - 1] - p); sell[j] = max(sell[j], buy[j] + p)
    print(f' {d}   {p}   | {buy[1]:4} {sell[1]:4} {buy[2]:4} {sell[2]:4}')
print('answer sell[2] =', sell[2])

# the k >= n // 2 claim: full table vs unlimited, exhaustive over small price lists
cnt = 0; first_k_needed = {}
import itertools
for n in range(0, 8):
    for t in itertools.product(range(0, 4), repeat=n):
        pr = list(t); u = unlimited(pr)
        for kk in range(0, n + 3):
            full = table_k(kk, pr) if kk else 0
            if kk >= n // 2: assert full == u, (kk, pr)
            if kk < n // 2: assert full <= u
        cnt += 1
print('exhaustive price lists (len <= 7, values 0..3):', cnt, '- table(k) == unlimited for every k >= n // 2')
# is n // 2 tight? find a list where k = n // 2 - 1 is strictly worse
ex = None
for n in (4, 6):
    for t in itertools.product(range(0, 3), repeat=n):
        pr = list(t)
        if table_k(n // 2 - 1, pr) < unlimited(pr): ex = pr; break
    if ex: break
print('k = n // 2 - 1 is not enough on e.g.', ex, ':', table_k(len(ex) // 2 - 1, ex), '<', unlimited(ex))

# seeded cross-check against the recursion over (day, transactions left, holding)
n_cases = 0
for _ in range(600):
    n = random.randint(0, 8); pr = [random.randint(0, 9) for _ in range(n)]; kk = random.randint(0, 5)
    want = brute(kk, pr)
    assert solve(kk, pr) == want == memo(kk, pr) == (table_k(kk, pr) if kk else 0), (kk, pr)
    n_cases += 1
print('cross-check cases', n_cases, '(table, shortcut and memo all equal the recursion)')

big = [random.randint(0, 1000) for _ in range(1000)]
print('n = 1000, k = 10^9 ->', solve(10**9, big), '| k = 50 ->', solve(50, big))
print('limit =', sys.getrecursionlimit())
try:
    memo(3, big); print('memo n=1000 ok')
except RecursionError:
    print('memo n=1000: RecursionError')
assert solve(0, [1, 2]) == 0 and solve(5, []) == 0 and solve(5, [4]) == 0 and solve(1, [1, 2]) == 1
print('edge asserts passed')
```

**Output (my run):**
```
example k = 2 [3, 2, 6, 5, 0, 3] -> 7
example k = 1 [7, 6, 4, 3, 1] -> 0
example k = 1000000000 [1, 5, 2, 8, 3, 9] -> 16
example k = 0 [1, 9] -> 0
day price | buy1 sell1 buy2 sell2
 0   3   |   -3    0   -3    0
 1   2   |   -2    0   -2    0
 2   6   |   -2    4   -2    4
 3   5   |   -2    4   -1    4
 4   0   |    0    4    4    4
 5   3   |    0    4    4    7
answer sell[2] = 7
exhaustive price lists (len <= 7, values 0..3): 21845 - table(k) == unlimited for every k >= n // 2
k = n // 2 - 1 is not enough on e.g. [0, 1, 0, 1] : 1 < 2
cross-check cases 600 (table, shortcut and memo all equal the recursion)
n = 1000, k = 10^9 -> 166382 | k = 50 -> 46152
limit = 1000
memo n=1000: RecursionError
edge asserts passed
```

**Edge cases:**
- `k = 0`: 0. Empty or single price: 0.
- `k = 10^9`: take the shortcut, never allocate `k + 1` slots.
- Always falling prices: 0.
- `k >= n // 2` with `n` odd (e.g. n = 5, k = 2): shortcut applies, `n // 2 = 2`.

**Follow-ups:**
- "k = 2 exactly?" Four scalar variables (the table with k = 2 unrolled).
- "Cooldown instead of a limit?" Q25.
- "Fee per transaction?" Subtract it at the sell; the shortcut changes to a greedy-with-fee form.

**Common mistakes:**
- Allocating arrays of size `k + 1` for huge `k` (memory error).
- Using `k >= n` as the cap and wasting time, or `k > n // 2` and missing the `==` case.
- Initialising `buy` to 0 (free share) instead of `-inf`.
- Starting the `sell[j]` array at `-inf`, which wrongly forbids doing fewer than `j` trades.

### Q30 ⭐⭐ 🔴 Last stone weight II (any smash order). `stones` has 1 <= len <= 30 integers in 1..100. Repeatedly choose ANY two stones x <= y and smash them: both vanish if equal, otherwise a stone of weight y - x remains. At most one stone is left at the end (or none). Return the smallest possible weight of the last stone (0 if none is left). Part 8 Q18 smashes the two heaviest and answers a different question (that order is fixed); here you choose the order. Show the reduction to splitting the stones into two groups with the smallest difference of sums, then subset sums up to total // 2. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an exhaustive search over every sequence of smashes (len <= 7) and over all sign assignments on small inputs. Example: stones=[2, 7, 4, 1, 8, 1] -> 1; stones=[31, 26, 33, 21, 40] -> 5; stones=[5] -> 5; stones=[3, 3] -> 0; stones=[1, 2, 5] -> 2.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 0/1 knapsack as subset sum ("split into two groups with the smallest difference"). Any smash order is free, so this is not the greedy of Part 8 Q18.

**Say this first (1 line):** "Whatever order I smash in, the last stone is the absolute value of some plus/minus sum of the stones, so I want the two-group split with the smallest difference, which is subset sums up to `total // 2`."

**Brute force:** Try every sequence of smashes: pick any two stones, replace them by their difference (drop it if 0), recurse on the sorted tuple with a cache. Exponential; I use it for len <= 7. Also all `2^n` sign assignments, taking the minimum of `|sum|`.

**Optimal:**
- Reduction, direction 1: after any smash, the new stone `y - x` is a signed combination of the two original groups of stones. By induction, every stone in the pile is `+/-` a signed sum of original stones, and the last stone is `|sum of s_i * stone_i|` for some signs `s_i`. So the answer is at least `min |signed sum|`.
- Direction 2: take signs with minimum `d = |signed sum|`, plus-group P and minus-group N. Smash a plus stone against a minus stone repeatedly (the difference joins the heavier side); each step keeps the signed sum the same. This ends when one side is empty, leaving stones that sum to `d` on one side. If two or more were left, smashing two of them `u <= v` would make a smash order whose result has signed sum `d - 2u < d`, contradicting minimality of `d` (`d >= u + v >= 2u`). So exactly one stone (or none) remains with weight `d`. So the answer equals `min |signed sum|`. All checked by brute force: the smash search, the sign enumeration and the DP agree on 500 seeded lists of length <= 7.
- Signed sum = `sum(P) - sum(N) = total - 2 * sum(N)`. Minimise `|total - 2a|` over subset sums `a`; the best is the largest achievable `a <= total // 2`. Answer `total - 2a`.
- State: `can[s]` = True if some subset of the stones seen so far sums to `s`, for `s = 0..total // 2`. Base `can[0] = True`. Transition per stone `x`: for `s` from `half` DOWN to `x`: `can[s] |= can[s - x]`. Downward so each stone is used once (an upward loop would be the unbounded version, Q20).
- Bitset alternative: `bits |= bits << x`, then walk down from `total // 2` to the first set bit. Same answers on every test.
- Space: O(total // 2), at most 30 * 100 / 2 = 1500 slots.

**Complexity:** Time O(n * total / 2) = about 30 * 1500 = 45,000 steps; space O(total / 2). Memoised recursion over `(i, cap)` nests at most `n = 30` deep, far below the recursion limit of 1000, so the limit is not a problem here; I still prefer the table (and a memo has up to n * half = 45,000 states, so the table is cheaper).

**Dry run:** `[2, 7, 4, 1, 8, 1]`, total 23, half 11 (the printed table lists the reachable sums after each stone).
- After 2: {0, 2}. After 7: {0, 2, 7, 9}. After 4: {0, 2, 4, 6, 7, 9, 11}. After 1: every sum 0..11.
- Largest `a <= 11` is 11. Last stone `23 - 22 = 1`. (Total is odd, so 0 is impossible.)

**Code:**
```python
import random, itertools, sys
from functools import cache

random.seed(30)
INF = float('inf')

def last_stone_ii(stones):
    """Split into two groups with sums a <= b: last stone = b - a = total - 2a. Maximise a <= total // 2 by subset sums."""
    total = sum(stones); half = total // 2
    can = [True] + [False] * half               # can[s]: some subset sums to s
    for x in stones:
        for s in range(half, x - 1, -1):         # downward: each stone used at most once
            if can[s - x]: can[s] = True
    a = max(s for s in range(half + 1) if can[s])
    return total - 2 * a

def bitset(stones):
    total = sum(stones); bits = 1
    for x in stones: bits |= bits << x
    h = total // 2
    while not bits >> h & 1: h -= 1
    return total - 2 * h

def memo_subset(stones):
    total = sum(stones); half = total // 2; n = len(stones)
    @cache
    def best(i, cap):                            # largest subset sum <= cap using stones[i:]
        if i == n: return 0
        r = best(i + 1, cap)
        if stones[i] <= cap: r = max(r, stones[i] + best(i + 1, cap - stones[i]))
        return r
    return total - 2 * best(0, half)

def signs(stones):
    n = len(stones); best = INF
    for mask in range(1 << n):
        s = sum(x if mask >> i & 1 else -x for i, x in enumerate(stones))
        best = min(best, abs(s))
    return best

def smashes(stones):
    """Every sequence of smashes (choose any two stones each time)."""
    @cache
    def f(state):
        if len(state) <= 1: return state[0] if state else 0
        best = INF
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                rest = list(state[:i] + state[i + 1:j] + state[j + 1:])
                d = state[j] - state[i]
                if d: rest.append(d)
                best = min(best, f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(stones)))

for st, exp in [([2, 7, 4, 1, 8, 1], 1), ([31, 26, 33, 21, 40], 5), ([5], 5), ([3, 3], 0), ([1, 2, 5], 2)]:
    assert last_stone_ii(st) == bitset(st) == memo_subset(st) == signs(st) == smashes(st) == exp, st
    print('example', st, '->', exp)

st = [2, 7, 4, 1, 8, 1]; total = sum(st); half = total // 2
can = [True] + [False] * half
print('total', total, 'half', half, '; reachable subset sums 0..', half, 'after each stone:')
for x in st:
    for s in range(half, x - 1, -1):
        if can[s - x]: can[s] = True
    print(f'  after {x}:', [s for s in range(half + 1) if can[s]])
a = max(s for s in range(half + 1) if can[s])
print('best group sum a =', a, '-> last stone =', total, '-', 2 * a, '=', total - 2 * a)

n_cases = 0
for _ in range(500):
    n = random.randint(1, 7); st = [random.randint(1, 12) for _ in range(n)]
    want = smashes(st)
    assert last_stone_ii(st) == bitset(st) == memo_subset(st) == want == signs(st), st
    n_cases += 1
print('cross-check cases (len <= 7)', n_cases, ': subset-sum DP == bitset == memo == every smash order == all sign assignments')
for _ in range(200):
    st = [random.randint(1, 30) for _ in range(random.randint(1, 14))]
    assert last_stone_ii(st) == signs(st) == bitset(st)
print('200 more (len <= 14) against all sign assignments')

big = [random.randint(1, 100) for _ in range(30)]
print('n = 30, values <= 100 ->', last_stone_ii(big), '(total', sum(big), ')')
print('limit', sys.getrecursionlimit(), '- memo recursion depth is len(stones) <= 30, far below it')
assert last_stone_ii([100] * 30) == 0 and last_stone_ii([1]) == 1 and last_stone_ii([1, 100]) == 99
print('edge asserts passed')
```

**Output (my run):**
```
example [2, 7, 4, 1, 8, 1] -> 1
example [31, 26, 33, 21, 40] -> 5
example [5] -> 5
example [3, 3] -> 0
example [1, 2, 5] -> 2
total 23 half 11 ; reachable subset sums 0.. 11 after each stone:
  after 2: [0, 2]
  after 7: [0, 2, 7, 9]
  after 4: [0, 2, 4, 6, 7, 9, 11]
  after 1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  after 8: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
  after 1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
best group sum a = 11 -> last stone = 23 - 22 = 1
cross-check cases (len <= 7) 500 : subset-sum DP == bitset == memo == every smash order == all sign assignments
200 more (len <= 14) against all sign assignments
n = 30, values <= 100 -> 1 (total 1779 )
limit 1000 - memo recursion depth is len(stones) <= 30, far below it
edge asserts passed
```

**Edge cases:**
- One stone: itself (`[5] -> 5`).
- Two equal stones: 0.
- One huge stone and small ones: the small ones cannot cancel it (`[1, 100] -> 99`).
- Total odd: answer is at least 1.
- Loop direction: `range(half, x - 1, -1)`; forgetting `x - 1` lower bound would index negative.

**Follow-ups:**
- "Return the groups?" Keep a parent array or a 2D boolean table and walk back.
- "Why not smash the two heaviest?" That is a fixed order (Part 8 Q18), and it can give a larger last stone than the best order.
- "Values up to 10^9?" Subset sums no longer fit in a table; meet in the middle for n <= 40.

**Common mistakes:**
- Using the upward loop (items reusable).
- Searching up to `total` instead of `total // 2` and picking the wrong `a`.
- Answering `total % 2` (parity only), which ignores whether the sum is reachable.
- Simulating greedy smashes of the two largest stones.

### Q31 ⭐ 🟢 The `[[0]*n]*m` aliasing trap. For 1 <= m, n <= 6 build two tables: `bug = [[0]*n]*m` and `ok = [[0 for _ in range(n)] for _ in range(m)]`, apply the assignments `ops` (a list of [r, c, v]; 0 <= r < m, 0 <= c < n) to both with `table[r][c] = v` in order, and return `[bug, ok, distinct_rows_bug, distinct_rows_ok]`, where the last two are the numbers of distinct row objects (by `id`) in each table. Explain, from what `*` does to a list, why one write shows up in every row of `bug`, why `[0]*n` itself is safe (the elements are immutable ints) and what DP bug this creates (all rows alias, so a DP table gives wrong answers whenever a cell reads a value from a row it did not just write, such as a diagonal neighbour; a table whose cells read only the cell above and the cell to the left can look right by accident, because the single shared row then acts like a rolling array). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a hand-written model of the aliasing on small inputs. Example: m=2, n=3, ops=[[0, 1, 5]] -> [[[0, 5, 0], [0, 5, 0]], [[0, 5, 0], [0, 0, 0]], 1, 2]; m=3, n=2, ops=[[0, 0, 1], [2, 1, 7], [1, 0, 9]] -> [[[9, 7], [9, 7], [9, 7]], [[1, 0], [9, 0], [0, 7]], 1, 3]; m=1, n=1, ops=[] -> [[[0]], [[0]], 1, 1].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; a function-caching tutorial seen as a search snippet only; behaviour verified by running Python 3.13) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Python object identity, not an algorithm. It is the first DP bug people hit, because every 2D DP table starts with an allocation line.

**Say this first (1 line):** "`[[0]*n]*m` makes m references to one row list, so a write to any row is a write to all of them; `[0]*n` is fine because the ints are immutable, and the fix is a comprehension that builds a fresh row per iteration."

**Brute force:** There is nothing to optimise. The "brute force" is to build both tables, apply the writes, and compare them with a hand model of what aliasing should do. That is the cross-check below.

**Optimal:** The mechanism, step by step.
- `[0]*n` builds a list of n slots that all point to the one int object `0`. That is safe: `row[c] = v` rebinds one slot to a new object. It never changes the int `0` (ints cannot be mutated).
- `x * m` for a list `x` copies the element REFERENCES, not the elements. So `[row]*m` is a list of m slots pointing to the same list object `row`. No row is copied.
- `bug[r][c] = v` first fetches `bug[r]` (the one shared row), then rebinds slot `c` of that row. Every `bug[i]` is that row, so column `c` changes in all m rows at once.
- `ok = [[0 for _ in range(n)] for _ in range(m)]` runs the inner expression m times, so there are m separate lists.
- `distinct_rows_bug` is 1 for every m >= 1, because all m slots hold the same `id`. `distinct_rows_ok` is m.
- The DP consequence: a table filled row by row has only ONE row of storage when aliased. Whatever you write for row r overwrites row r-1 at the same time. Reads of the previous row then return the new values, which are wrong.
- Honest nuance (I tested it): the bug does not always change the final answer. For unique paths with right/down moves, each cell reads `dp[r-1][c]` and `dp[r][c-1]`. In the shared row those are exactly the old value and the new value, so the aliased table accidentally acts like the rolling 1D array and gives the right answer. It breaks as soon as a cell reads `dp[r-1][c-1]` (diagonal move, LCS, edit distance): that slot was already overwritten. The code shows 17 versus the correct 13. So "silently wrong" is true in general but not for every DP; never rely on luck.
- Safe patterns: `[[0]*n for _ in range(m)]` (inner `*` is fine, outer must be a comprehension), or `[[0 for _ in range(n)] for _ in range(m)]`. Do NOT use `copy.copy` on the outer list (shallow, same problem).

**Complexity:** Time O(m*n) to build and O(len(ops)) to apply writes. Space O(m*n) for `ok`, O(n) for `bug` (which is the whole problem: it has far less storage than you think).

**Dry run (first example):** `m=2, n=3, ops=[[0,1,5]]`.
- Start: `bug` is `[R, R]` where `R = [0,0,0]`. `ok` is `[A, B]` with `A = [0,0,0]`, `B = [0,0,0]` (separate lists).
- Apply `table[0][1] = 5`.

| step | table | `table[0]` | `table[1]` |
|---|---|---|---|
| before | bug | `[0,0,0]` (R) | `[0,0,0]` (the same R) |
| before | ok | `[0,0,0]` (A) | `[0,0,0]` (B) |
| after | bug | `[0,5,0]` (R) | `[0,5,0]` (the same R) |
| after | ok | `[0,5,0]` (A) | `[0,0,0]` (B) |

- Distinct rows: bug 1 (`id(R)`), ok 2. Result `[[[0,5,0],[0,5,0]], [[0,5,0],[0,0,0]], 1, 2]`. This matches the prompt.
- Second example: writes to column 0 (values 1, then 9) and column 1 (value 7). In `bug` the last write per column wins everywhere: `[9,7]` in all three rows. In `ok` each row keeps its own write: `[1,0]`, `[9,0]`, `[0,7]`.

**Code:**
```python
import random

random.seed(31)

def alias_trap(m, n, ops):
    bug = [[0] * n] * m                                   # m references to ONE row list
    ok = [[0 for _ in range(n)] for _ in range(m)]        # m separate row lists
    for r, c, v in ops:
        bug[r][c] = v
        ok[r][c] = v
    return [bug, ok, len({id(row) for row in bug}), len({id(row) for row in ok})]

def model(m, n, ops):
    """Hand model: bug has ONE row, so a write at (r, c) changes column c everywhere."""
    one_row = [0] * n
    real = [[0] * n for _ in range(m)]
    for r, c, v in ops:
        one_row[c] = v          # the single shared row
        real[r][c] = v          # a real, independent cell
    return [[one_row[:] for _ in range(m)], real, 1, m]

# ---- examples from the prompt
assert alias_trap(2, 3, [[0, 1, 5]]) == [[[0, 5, 0], [0, 5, 0]], [[0, 5, 0], [0, 0, 0]], 1, 2]
assert alias_trap(3, 2, [[0, 0, 1], [2, 1, 7], [1, 0, 9]]) == [[[9, 7], [9, 7], [9, 7]], [[1, 0], [9, 0], [0, 7]], 1, 3]
assert alias_trap(1, 1, []) == [[[0]], [[0]], 1, 1]
print('examples ok')

# ---- show the mechanism: * copies the reference, not the list
row = [0] * 3
t = [row] * 2
print('t[0] is t[1]:', t[0] is t[1], '| [0]*3 elements share one int object:', row[0] is row[1])
row[0] = 5   # rebinding a slot never mutates the int 0, so [0]*n is safe
print('after row[0] = 5:', row)

# ---- DPs filled row by row on the aliased table. The shared row acts like a rolling array.
def grid(m, n, diagonal, aliased):
    dp = [[0] * n] * m if aliased else [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1] + (dp[r - 1][c - 1] if diagonal else 0)
    return dp[m - 1][n - 1]
print('unique paths 3x3 (right/down moves): aliased =', grid(3, 3, False, True), ' correct =', grid(3, 3, False, False))
print('paths with a diagonal move 3x3:      aliased =', grid(3, 3, True, True), ' correct =', grid(3, 3, True, False))
assert grid(3, 3, False, True) == grid(3, 3, False, False) == 6      # the bug hides: reads of row r-1 see the old value
assert grid(3, 3, True, False) == 13 and grid(3, 3, True, True) != 13  # dp[r-1][c-1] was already overwritten

# ---- seeded cross-check: solution vs the hand model (and an exhaustive sweep of tiny shapes)
cases = 0
for _ in range(1000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    ops = [[random.randrange(m), random.randrange(n), random.randint(-9, 9)] for _ in range(random.randint(0, 8))]
    assert alias_trap(m, n, ops) == model(m, n, ops), (m, n, ops)
    cases += 1
for m in range(1, 4):
    for n in range(1, 4):
        for r in range(m):
            for c in range(n):
                assert alias_trap(m, n, [[r, c, 7]]) == model(m, n, [[r, c, 7]])
                cases += 1
print('cross-check passed on', cases, 'cases')

# ---- edge cases
assert alias_trap(1, 3, [[0, 2, 4]])[0] == alias_trap(1, 3, [[0, 2, 4]])[1]   # m = 1: no visible bug
assert alias_trap(4, 1, [[3, 0, 8]])[0] == [[8]] * 4
print('edge cases ok')
```

**Output (my run):**
```
examples ok
t[0] is t[1]: True | [0]*3 elements share one int object: True
after row[0] = 5: [5, 0, 0]
unique paths 3x3 (right/down moves): aliased = 6  correct = 6
paths with a diagonal move 3x3:      aliased = 17  correct = 13
cross-check passed on 1036 cases
edge cases ok
```

**Edge cases:**
- m = 1: the aliased table has one row either way, so the bug is invisible. Do not conclude that it is safe; it breaks at m = 2.
- n = 1: still aliased (the rows are lists of length 1 pointing to one list).
- Empty `ops`: both tables are all zeros and equal, but the id counts still differ (1 versus m).
- Writing the same cell twice in `bug`: the last write wins in every row.

**Follow-ups:**
- *Same trap with other types?* `[[]]*m` for adjacency lists, `[{}]*m` for dicts, `[set()]*m`. Any mutable element. Use comprehensions.
- *Same trap with default arguments?* `def f(x, memo={})` shares one dict across calls. Related idea: one object, many names.
- *Why does `[0]*n` not bite?* Slot assignment rebinds, and ints have no in-place mutation. `[x]*n` with a mutable `x` bites only when you MUTATE `x` (`row.append`, `row[i] = ...`), not when you rebind the outer slot.

**Common mistakes:**
- Fixing it with `copy.copy` or `list(...)` on the outer list: still shallow.
- Using `deepcopy` of the aliased table after the fact; the damage is done when the writes happen before the copy.
- Believing a passing test proves the table is fine: unique paths passes by accident.
- Testing only m = 1 (no visible bug).

### Q32 ⭐ 🟡 `functools.cache`, mutable arguments and `cache_clear`. `nums` is a list of 0 <= len <= 15 integers (|value| <= 20) and `target` an integer (|target| <= 100). Write a memoised recursive function `f(i, rem)` that counts the subsets (chosen by position) of `nums` with sum `target`: `f(i, rem)` returns 1 if i == len(nums) and rem == 0, 0 if i == len(nums) otherwise, and else `f(i + 1, rem) + f(i + 1, rem - nums[i])` (no pruning of negative `rem`); decorate it with `@functools.cache`, keep `nums` as a tuple captured from the enclosing scope (a list passed as an argument would raise `TypeError: unhashable type: 'list'`). Call f(0, target) once and return `[answer, hits, misses, currsize_after_clear]` from `f.cache_info()` taken right after that call and after `f.cache_clear()`. Explain why misses equals the number of cached entries, why a list argument cannot be used as a cache key, and the options (convert to a tuple, use indices). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a hand-written dict memo that counts hits and misses itself on small inputs. Example: nums=[1, 2, 3], target=3 -> [2, 1, 14, 0]; nums=[], target=0 -> [1, 0, 1, 0]; nums=[0, 0], target=0 -> [4, 2, 3, 0]; nums=[2, 2, 2, 2], target=4 -> [6, 6, 15, 0].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; a function-caching tutorial seen as a search snippet only; behaviour verified by running Python 3.13) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Top-down memoisation with `functools.cache`. The state is `(i, rem)`: positions decided so far and the sum still needed. Cache keys must be hashable.

**Say this first (1 line):** "`cache` keys on the call arguments, so arguments must be hashable; I keep `nums` as a tuple in the closure and pass only the ints `i` and `rem`, and the cache then holds one entry per distinct state, which is exactly the miss count."

**Brute force:** Enumerate all 2^n subsets and test the sum: O(2^n * n). With n <= 15 that is 32768 subsets and fine. It is one of the cross-checks (the other is a hand-written dict memo that counts hits and misses itself).

**Optimal:**
- State: `f(i, rem)` = the number of ways to choose from `nums[i:]` (by position) so that the chosen sum is `rem`.
- Base: `i == len(nums)`: 1 if `rem == 0`, else 0 (the empty choice is the only one left).
- Transition: `f(i, rem) = f(i+1, rem)` (skip `nums[i]`) `+ f(i+1, rem - nums[i])` (take it). There is no pruning, so `rem` may go negative and zeros and negatives are counted correctly (two zeros give 4 subsets for target 0).
- `@functools.cache` is `lru_cache(maxsize=None)`. The key is built from the arguments `(i, rem)`. Each distinct key is computed once (a miss); each repeat is a hit.
- Misses equal the number of cached entries: every miss stores exactly one new entry, there is no size limit so nothing is evicted, and a recursion that raises would store nothing. (With a `maxsize` limit this would stop being true.) I checked `misses == currsize == len(dict memo)` on all 500 random cases.
- Hits plus misses equals the number of calls to `f`, including the first call.
- Why a list cannot be a key: the key is hashed, and lists are mutable so `list.__hash__` is `None`; `f([1,2])` raises `TypeError: unhashable type: 'list'`. A mutable key could also change after being stored, which would corrupt the cache.
- Options: (1) pass a tuple (`tuple(nums)`), O(len) to hash on every call so only OK for small tuples; (2) pass indices and keep the data in a closure, as here (best); (3) your own `dict` memo with `(i, rem)` tuple keys.
- `cache_clear()` empties the cache and resets hits, misses and currsize to 0. Use it between tests when the function is module-level, because a stale cache is shared state; here `f` is rebuilt per call so it matters less, and the clear makes the last item of the answer 0.
- Recursion depth is len(nums) + 1 <= 16 here, so no recursion-limit issue (see Q33 for that).

**Complexity:** Time O(S) where S = the number of distinct states visited, at most (n+1) * (number of reachable sums) and at most 2^(n+1) - 1 without any collisions; each state costs O(1). Space O(S) for the cache plus O(n) stack. Here n <= 15 and |value| <= 20 so rem stays in a small range.

**Dry run (first example):** `nums=[1,2,3], target=3`. Calls in depth-first order, M = miss, H = hit.

| call | result | note |
|---|---|---|
| f(0,3) M | 2 | root |
| f(1,3) M | 1 | skip 1 |
| f(2,3) M | 1 | skip 2 |
| f(3,3) M | 0 | end, rem != 0 |
| f(3,0) M | 1 | end, take 3, rem 0 |
| f(2,1) M | 0 | take 2 |
| f(3,1) M, f(3,-2) M | 0, 0 | |
| f(1,2) M | 1 | take 1 |
| f(2,2) M | 0 | skip 2 |
| f(3,2) M, f(3,-1) M | 0, 0 | |
| f(2,0) M | 1 | take 2 |
| f(3,0) **H** | 1 | already stored |
| f(3,-3) M | 0 | |

- Total: 14 misses, 1 hit, answer 2 (subsets {3} and {1,2}), cache size 14 before the clear and 0 after: `[2, 1, 14, 0]`.

**Code:**
```python
import functools
import random

random.seed(32)

def solve(nums, target):
    ns = tuple(nums)          # hashable, captured by the closure (not a cache key)
    n = len(ns)

    @functools.cache
    def f(i, rem):
        if i == n:
            return 1 if rem == 0 else 0
        return f(i + 1, rem) + f(i + 1, rem - ns[i])

    ans = f(0, target)
    info = f.cache_info()
    entries = info.currsize          # entries held right before the clear
    f.cache_clear()
    return [ans, info.hits, info.misses, f.cache_info().currsize], entries

def oracle(nums, target):
    """Hand-written dict memo that counts hits and misses itself."""
    n = len(nums)
    memo, hits, misses = {}, 0, 0
    def f(i, rem):
        nonlocal hits, misses
        if (i, rem) in memo:
            hits += 1
            return memo[(i, rem)]
        misses += 1
        v = (1 if rem == 0 else 0) if i == n else f(i + 1, rem) + f(i + 1, rem - nums[i])
        memo[(i, rem)] = v
        return v
    a = f(0, target)
    return [a, hits, misses, 0], len(memo)

def brute_count(nums, target):
    n = len(nums)
    return sum(1 for mask in range(1 << n) if sum(nums[i] for i in range(n) if mask >> i & 1) == target)

# ---- examples from the prompt
assert solve([1, 2, 3], 3)[0] == [2, 1, 14, 0]
assert solve([], 0)[0] == [1, 0, 1, 0]
assert solve([0, 0], 0)[0] == [4, 2, 3, 0]
assert solve([2, 2, 2, 2], 4)[0] == [6, 6, 15, 0]
print('examples ok')

# ---- why a list argument cannot be a cache key
@functools.cache
def g(lst):
    return sum(lst)
try:
    g([1, 2])
except TypeError as e:
    print('TypeError:', e)
print('tuple key works:', g((1, 2)))

# ---- misses == entries stored; hits + misses == number of calls
ex, entries = solve([1, 2, 3], 3)
print('example 1: misses', ex[2], 'entries before clear', entries, 'currsize after clear', ex[3])

# ---- seeded cross-check against the dict memo and a plain subset enumeration
cases = 0
for _ in range(500):
    nums = [random.randint(-20, 20) for _ in range(random.randint(0, 9))]
    target = random.randint(-100, 100) if random.random() < 0.3 else sum(random.sample(nums, random.randint(0, len(nums))))
    got, entries = solve(nums, target)
    exp, entries2 = oracle(nums, target)
    assert got == exp, (nums, target, got, exp)
    assert got[2] == entries == entries2          # misses == cached entries
    assert got[0] == brute_count(nums, target)
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- cache_clear matters: a closure cache is rebuilt per call here, but a module-level one grows across tests
@functools.cache
def h(i):
    return i * 2
h(1); h(2); h(1)
print('module-level cache:', h.cache_info())
h.cache_clear()
print('after cache_clear:', h.cache_info())
assert h.cache_info().currsize == 0

# ---- edge cases
assert solve([], 5)[0] == [0, 0, 1, 0]
assert solve([20] * 15, 100)[0][0] == 3003          # C(15, 5)
print('edge cases ok')
```

**Output (my run):**
```
examples ok
TypeError: unhashable type: 'list'
tuple key works: 3
example 1: misses 14 entries before clear 14 currsize after clear 0
cross-check passed on 500 cases
module-level cache: CacheInfo(hits=1, misses=2, maxsize=None, currsize=2)
after cache_clear: CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
edge cases ok
```

**Edge cases:**
- `nums = []`: one miss, answer 1 if `target == 0` else 0.
- Zeros and negatives: no pruning on `rem`, otherwise `[0, 0]` target 0 would count 1 instead of 4.
- Duplicate values count as different positions (2,2,2,2 target 4 gives 6).
- Calling `info = f.cache_info()` after `cache_clear()` shows zeros; take it BEFORE the clear.

**Follow-ups:**
- *Why not decorate a function that takes `nums` as an argument?* Lists are unhashable; passing a tuple works but hashes the whole tuple per call.
- *`cache` versus `lru_cache(maxsize=128)`?* The default `lru_cache` evicts, so misses no longer equal entries and a DP can become exponential again. Use `maxsize=None` or `cache` for DP.
- *Memory leak?* A module-level cache keeps arguments alive (and every state) until `cache_clear()`. Methods on instances also keep `self` alive.

**Common mistakes:**
- Putting a list or dict in the signature of a cached function.
- Reading `cache_info()` after `cache_clear()` and wondering why everything is 0.
- Forgetting that a decorated function defined inside a loop or per-call has a fresh cache each time.
- Pruning `rem < 0` when negatives exist.

### Q33 ⭐ 🟡 Memoised recursion versus bottom-up: the recursion limit. Count the ways to climb `n` stairs with steps 1, 2 or 3 modulo 10^9 + 7 (f(0) = 1, f(k) = f(k-1) + f(k-2) + f(k-3), f(negative) = 0), for n in 0..500 or 2000..10^5. Return `[ways, memo_outcome]` where `ways` is the correct answer from your bottom-up loop and `memo_outcome` is the string 'ok' if a `@functools.cache` top-down version `f(n)` called in a fresh Python 3.13 interpreter at the default recursion limit returns normally, or 'RecursionError' if it raises. Explain why the depth is about n, why raising `sys.setrecursionlimit` is not a fix to rely on in an interview, and how bottom-up avoids it. (Part 7 Q35 shows the same limit on deep trees.) In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against the memoised top-down function itself, run in try/except (the oracle returns the outcome and, when it succeeds, the value) on small inputs. Example: n=0 -> [1, 'ok']; n=10 -> [274, 'ok']; n=500 -> [283701821, 'ok']; n=2000 -> [78591238, 'RecursionError']; n=100000 -> [111787461, 'RecursionError'].
**Asked at:** Python caching and recursion notes (functools documentation: fetch failed, not opened; a function-caching tutorial seen as a search snippet only; behaviour verified by running Python 3.13) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Tabulation (bottom-up) versus memoisation (top-down) for a linear counting DP, and what the Python recursion limit does to the top-down one.

**Say this first (1 line):** "The recurrence is f(k) = f(k-1) + f(k-2) + f(k-3); top-down recursion goes about n frames deep and dies at n of about 1000 under the default limit, so I write it bottom-up with three rolling variables."

**Brute force:** Plain recursion with no cache: T(n) = T(n-1) + T(n-2) + T(n-3), which grows like 1.84^n. Hopeless past n of about 35. The memoised version fixes the time but not the depth.

**Optimal:**
- State: `f(k)` = number of ordered step sequences (steps 1, 2 or 3) that sum to exactly k, modulo 10^9 + 7.
- Base: `f(0) = 1` (the empty sequence), `f(negative) = 0`. So `f(1) = 1`, `f(2) = 2`, `f(3) = 4`.
- Transition: the LAST step is 1, 2 or 3, so `f(k) = f(k-1) + f(k-2) + f(k-3)`. Apply the modulus at every addition so numbers stay small (Python ints would not overflow, but they would become huge and slow).
- Bottom-up: keep `(f(k-3), f(k-2), f(k-1))` in three variables and roll them n times. O(n) time, O(1) space, no recursion.
- Top-down with `@functools.cache`: `f(n)` calls `f(n-1)` first, which calls `f(n-2)`... down to `f(0)` before anything returns. The chain is about n frames deep (one frame per level; the cache wrapper is C code and adds no Python frame, but the calls still nest).
- Default limit: `sys.getrecursionlimit()` is 1000. The oracle run says the largest working n at module level here is 997 (the script's own frames take a few). So n in 0..500 is `'ok'` and n >= 1000 raises `RecursionError`. That matches the prompt: n = 2000 and 10^5 both raise.
- Why not `sys.setrecursionlimit(10**6)`: the limit is a guard, not extra stack. Python frames for pure-Python calls are cheap in 3.13, but this function reaches through the C `lru_cache` wrapper, and I measured that even with the limit at 10^6 it still raises at n = 5000 in Python 3.13.17 here (n = 3000 passed). In an older CPython or a different build the same code can crash the interpreter with a segfault instead of raising. Behaviour depends on the build, so it is unsafe to rely on in an interview or in production. Bottom-up has no such failure.
- Other fixes: an explicit stack (iterative DFS), or just bottom-up. For this recurrence bottom-up is simplest.
- Cross-reference: Part 7 Q35 shows the same limit on deep trees.

**Complexity:** Bottom-up: time O(n), space O(1). Top-down memoised: time O(n) but space O(n) for the cache plus an O(n) call stack, and it fails for n above about 1000 at the default limit. Plain recursion: exponential (about 1.84^n).

**Dry run (first example family, n = 10):** `f(0)=1`, `f(-1)=f(-2)=0`.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| f(k) | 1 | 1 | 2 | 4 | 7 | 13 | 24 | 44 | 81 | 149 | 274 |

- Check one cell: `f(4) = f(3) + f(2) + f(1) = 4 + 2 + 1 = 7`. `f(10) = f(9) + f(8) + f(7) = 149 + 81 + 44 = 274`. Matches the prompt.
- The three rolling variables hold `(f(k-3), f(k-2), f(k-1))`: start `(0, 0, 1)` for k = 1, then `(0, 1, 1)`, `(1, 1, 2)`, `(1, 2, 4)`, `(2, 4, 7)`... the last value is the answer.
- Top-down trace for n = 3: `f(3)` calls `f(2)` calls `f(1)` calls `f(0)` (depth 4); the values then return upward, and `f(-1)`, `f(-2)` return 0 immediately.

**Code:**
```python
import functools
import random
import sys

random.seed(33)
MOD = 10**9 + 7
assert sys.getrecursionlimit() == 1000          # the default; the claims below are about this limit

def bottom_up(n):
    """f(0)=1, f(k)=f(k-1)+f(k-2)+f(k-3), f(negative)=0, three rolling variables, no recursion."""
    if n == 0:
        return 1
    a, b, c = 0, 0, 1                           # f(-2), f(-1), f(0)
    for _ in range(n):
        a, b, c = b, c, (a + b + c) % MOD
    return c

@functools.cache
def top_down(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return (top_down(n - 1) + top_down(n - 2) + top_down(n - 3)) % MOD

def memo_outcome(n):
    """The oracle: run the memoised recursion in try/except. Returns (outcome, value or None)."""
    top_down.cache_clear()
    try:
        return 'ok', top_down(n)
    except RecursionError:
        return 'RecursionError', None

def solve(n):
    # 'ways' from the loop; 'memo_outcome' is reported by running top_down in this interpreter
    return [bottom_up(n), memo_outcome(n)[0]]

# ---- examples from the prompt
assert solve(0) == [1, 'ok']
assert solve(10) == [274, 'ok']
assert solve(500) == [283701821, 'ok']
assert solve(2000) == [78591238, 'RecursionError']
assert solve(100000) == [111787461, 'RecursionError']
print('examples ok')

# ---- where exactly does the default limit bite? (the depth is about n, one frame per level)
top = 0
for n in range(1, 1000):
    if memo_outcome(n)[0] == 'ok':
        top = n
    else:
        break
print('largest n that works at limit 1000 (this interpreter, called from module level):', top)

# ---- every n in 0..500 is fine, so the prompt's 'ok' range is correct
assert all(memo_outcome(n)[0] == 'ok' for n in range(0, 501))
print('n = 0..500 all ok')

# ---- seeded cross-check: bottom-up value against the memoised oracle, outcome as well
cases = 0
for _ in range(300):
    n = random.randint(0, 500)
    out, val = memo_outcome(n)
    assert out == 'ok' and val == bottom_up(n)
    cases += 1
for n in (1000, 1500, 2000, 5000, 10**5):
    out, val = memo_outcome(n)
    assert out == 'RecursionError' and val is None and solve(n)[1] == out
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- raising the limit: a stopgap, not a plan
old = sys.getrecursionlimit()
sys.setrecursionlimit(10**6)
for n in (2000, 3000, 5000):
    out, val = memo_outcome(n)
    print('limit raised, n =', n, '->', out, '| bottom-up agrees:', val is None or val == bottom_up(n))
sys.setrecursionlimit(old)
print('limit restored to', sys.getrecursionlimit())

# ---- bottom-up at the full size, and the space-optimised form is O(1)
print('bottom-up n = 10**5:', bottom_up(10**5))
assert bottom_up(1) == 1 and bottom_up(2) == 2 and bottom_up(3) == 4
```

**Output (my run):**
```
examples ok
largest n that works at limit 1000 (this interpreter, called from module level): 997
n = 0..500 all ok
cross-check passed on 305 cases
limit raised, n = 2000 -> ok | bottom-up agrees: True
limit raised, n = 3000 -> ok | bottom-up agrees: True
limit raised, n = 5000 -> RecursionError | bottom-up agrees: True
limit restored to 1000
bottom-up n = 10**5: 111787461
```

**Edge cases:**
- n = 0: one way (do nothing); n = 1: 1; n = 2: 2.
- The modulus comes after the SUM of three terms, not on each term separately only; either is correct as long as every stored value is reduced.
- The first top-down call is the deepest; calling `f(500)` first and then `f(900)` works for that reason (the cache holds the lower values), but a fresh `f(2000)` still fails. Warm-up loops (`for k in range(n): f(k)`) are a hack to dodge the limit; bottom-up is the honest version.
- `RecursionError` is raised, not a wrong answer, so it is loud. Mention it in a code review.

**Follow-ups:**
- *Can you do n = 10^18?* Yes: matrix exponentiation of the 3x3 companion matrix, O(27 log n).
- *Why is the cache wrapper not adding frames?* `lru_cache` is implemented in C; the Python function frame is the only one per level. Still, I will not rely on that.
- *Climbing stairs with steps 1 and 2?* The same code with two variables (Fibonacci).

**Common mistakes:**
- Raising the recursion limit and calling it fixed.
- Forgetting `cache_clear()` between tests, so a warm cache hides the error for large n.
- Leaving out the modulus (answers become enormous big ints) or applying it only at the end.
- Off-by-one in the base: `f(0) = 1`, not 0.

### Q34 ⭐ 🟡 Longest increasing subsequence: recover one (with a tie rule). `nums` has 0 <= len <= 2000 integers (|value| <= 10^6). Among all strictly increasing subsequences of maximum length, return the VALUES of the one whose index list is lexicographically smallest (compare the position lists element by element); return [] for an empty list. Explain why the `tails` array of the bisect method (Q7) is not the answer, how to rebuild from the O(n^2) table, and how the patience-sorting method can recover a subsequence with predecessor pointers (which may return a different optimal subsequence unless you follow the tie rule). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsequences with the same tie rule (len <= 12) on small inputs. Example: nums=[10, 9, 2, 5, 3, 7, 101, 18] -> [2, 5, 7, 101]; nums=[0, 1, 0, 3, 2, 3] -> [0, 1, 2, 3]; nums=[3, 3, 3] -> [3]; nums=[] -> []; nums=[1, 3, 2, 4] -> [1, 3, 4].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** LIS with reconstruction. Compute the table from the right, then walk it left to right picking the smallest valid index each time.

**Say this first (1 line):** "`tails` only gives the length, not a subsequence; for the answer I take the O(n^2) table `f[i]` = longest increasing subsequence starting at i, then scan left to right picking the first index with the needed `f` and a larger value than the last pick, which gives the lexicographically smallest index list."

**Brute force:** Enumerate all subsets by index, keep the strictly increasing ones, take the longest, and among those the smallest index tuple. O(2^n * n); fine for n <= 12. It is the oracle.

**Optimal:**
- State: `f[i]` = length of the longest strictly increasing subsequence that STARTS at index i.
- Base: `f[i] = 1` (just `nums[i]`).
- Transition, filled for i from n-1 down to 0: `f[i] = 1 + max(f[j])` over `j > i` with `nums[j] > nums[i]` (default 1).
- Why from the right: then "starts at i" lets me read forward. The first element of the answer is the smallest index i with `f[i] = L` (L = max f). The next element is the smallest `j > i` with `nums[j] > nums[i]` and `f[j] = L - 1`, and one exists by the definition of `f[i]`. Repeat.
- Why this is the lexicographically smallest INDEX list: at every step I take the smallest index that can still be extended to full length L, and every shorter prefix choice is forced by that. The scan keeps going to the right, so indices are increasing automatically; the check `nums[i] > last` enforces the strictness.
- Ties: equal values are distinct positions. `[3,3,3]` has L = 1 and the answer `[3]` is index 0.
- Why `tails` is not the answer: `tails[k]` is the smallest possible LAST value of an increasing subsequence of length k + 1, taken over different subsequences. Entries come from different subsequences and may even sit in the wrong order of positions. Example: `[3, 4, 1]` gives `tails = [1, 4]`, but 1 comes after 4, so `[1, 4]` is not a subsequence.
- Patience sorting with predecessor pointers: when `x` lands at pile p, remember `pred[i]` = the index on top of pile p - 1 at that moment. Follow pred from the top of the last pile. It always yields a valid optimal subsequence in O(n log n), but not the tie-rule one. On the first example it returns `[2, 3, 7, 18]` (indices 2, 4, 5, 7) while the tie rule gives `[2, 5, 7, 101]` (indices 2, 3, 5, 6). Both have length 4. On 600 seeded small lists the two index lists differed on 368. If the question says "any one", patience is enough; with a tie rule use the table.
- Space: the O(n^2) approach needs only the 1D table `f` (O(n)); no 2D table.

**Complexity:** Table: time O(n^2) (n = 2000 gives 2 million pair checks), space O(n). Walk: O(n). Patience with pred: O(n log n) time, O(n) space (tails, tails_idx, pred).

**Dry run (first example):** `nums = [10, 9, 2, 5, 3, 7, 101, 18]`, fill `f` from the right.

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| nums | 10 | 9 | 2 | 5 | 3 | 7 | 101 | 18 |
| f (starts here) | 2 | 2 | 4 | 3 | 3 | 2 | 1 | 1 |

- Check: `f[5]` (value 7): later larger values 101 and 18 both have f = 1, so f = 2. `f[3]` (value 5): larger later values are 7 (f 2), 101, 18, so f = 3. `f[2]` (value 2): best is `f[3] = 3`, so 4.
- L = 4. Walk: the first index with f = 4 is index 2 (value 2). Need 3: first index after it with f = 3 and value > 2 is index 3 (value 5). Need 2: index 4 has f = 3, not 2; index 5 has f = 2 and 7 > 5, take it. Need 1: index 6 (value 101), f = 1 and 101 > 7. Result `[2, 5, 7, 101]`.

**Code:**
```python
import bisect
import itertools
import random

random.seed(34)

def lis_table(nums):
    """f[i] = length of the longest strictly increasing subsequence that STARTS at index i. O(n^2)."""
    n = len(nums)
    f = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] > nums[i] and f[j] + 1 > f[i]:
                f[i] = f[j] + 1
    return f

def lis_lex_min(nums):
    """Values of the max-length strictly increasing subsequence with the lexicographically smallest index list."""
    n = len(nums)
    if n == 0:
        return []
    f = lis_table(nums)
    need, last, out = max(f), None, []
    for i in range(n):                       # scanning left to right = smallest next index first
        if f[i] == need and (last is None or nums[i] > last):
            out.append(nums[i])
            last = nums[i]
            need -= 1
            if need == 0:
                break
    return out

def lis_patience(nums):
    """O(n log n) with predecessor pointers. A valid LIS, but NOT necessarily the lexicographically smallest."""
    tails_val, tails_idx, pred = [], [], [-1] * len(nums)
    for i, x in enumerate(nums):
        p = bisect.bisect_left(tails_val, x)
        if p == len(tails_val):
            tails_val.append(x); tails_idx.append(i)
        else:
            tails_val[p] = x; tails_idx[p] = i
        pred[i] = tails_idx[p - 1] if p else -1
    out, k = [], tails_idx[-1] if tails_idx else -1
    while k != -1:
        out.append(k)
        k = pred[k]
    out.reverse()
    return out, tails_val                    # index list, tails

def lis_brute(nums):
    n = len(nums)
    for L in range(n, 0, -1):
        cands = [c for c in itertools.combinations(range(n), L)
                 if all(nums[c[t]] < nums[c[t + 1]] for t in range(L - 1))]
        if cands:
            return [nums[i] for i in min(cands)]       # tuples compare lexicographically
    return []

# ---- examples from the prompt
assert lis_lex_min([10, 9, 2, 5, 3, 7, 101, 18]) == [2, 5, 7, 101]
assert lis_lex_min([0, 1, 0, 3, 2, 3]) == [0, 1, 2, 3]
assert lis_lex_min([3, 3, 3]) == [3]
assert lis_lex_min([]) == []
assert lis_lex_min([1, 3, 2, 4]) == [1, 3, 4]
print('examples ok')

# ---- the tables for the first example
ex = [10, 9, 2, 5, 3, 7, 101, 18]
print('nums     :', ex)
print('f (start):', lis_table(ex))
idx, tails = lis_patience(ex)
print('tails    :', tails, '(length 4 is right; here the content happens to be valid too)')
print('patience (pred pointers):', [ex[i] for i in idx], 'indices', idx, '| tie rule:', lis_lex_min(ex))
assert [ex[i] for i in idx] != lis_lex_min(ex)      # both are optimal, different answers
bad = [3, 4, 1]
print('tails for', bad, '=', lis_patience(bad)[1], 'but no increasing subsequence of nums reads 1 then 4: tails is not the answer')

# ---- seeded cross-check against the enumeration with the same tie rule
cases = diff_patience = 0
for _ in range(600):
    n = random.randint(0, 12)
    nums = [random.randint(-4, 8) for _ in range(n)]
    assert lis_lex_min(nums) == lis_brute(nums), nums
    pidx, _t = lis_patience(nums)
    pv = [nums[i] for i in pidx]
    assert len(pv) == len(lis_lex_min(nums))                          # same length
    assert all(pv[t] < pv[t + 1] for t in range(len(pv) - 1))         # a valid strictly increasing subsequence
    assert pidx == sorted(pidx)
    # indices of the tie-rule answer, for comparison of INDEX lists
    f = lis_table(nums); need = max(f, default=0); last = None; li = []
    for i in range(n):
        if need and f[i] == need and (last is None or nums[i] > last):
            li.append(i); last = nums[i]; need -= 1
    if pidx != li:
        diff_patience += 1
    cases += 1
print('cross-check passed on', cases, 'cases; patience index list differs from the tie rule on', diff_patience)

# ---- edge cases
assert lis_lex_min([5]) == [5]
assert lis_lex_min([5, 4, 3, 2, 1]) == [5]                  # all equal length 1: smallest index
assert lis_lex_min([1, 2, 3, 4]) == [1, 2, 3, 4]
assert lis_lex_min([2, 2, 3, 3]) == [2, 3]
assert len(lis_lex_min(list(range(2000)))) == 2000
print('edge cases ok')
```

**Output (my run):**
```
examples ok
nums     : [10, 9, 2, 5, 3, 7, 101, 18]
f (start): [2, 2, 4, 3, 3, 2, 1, 1]
tails    : [2, 3, 7, 18] (length 4 is right; here the content happens to be valid too)
patience (pred pointers): [2, 3, 7, 18] indices [2, 4, 5, 7] | tie rule: [2, 5, 7, 101]
tails for [3, 4, 1] = [1, 4] but no increasing subsequence of nums reads 1 then 4: tails is not the answer
cross-check passed on 600 cases; patience index list differs from the tie rule on 368
edge cases ok
```

**Edge cases:**
- Empty list: return `[]` (L would be undefined).
- All equal: length 1, the first element.
- Strictly decreasing: length 1, the first element (index 0).
- Already increasing: the whole list.
- Duplicates in the middle (`[2,2,3,3]` gives `[2,3]` using the first 2 and the first 3).

**Follow-ups:**
- *Count them?* Keep a parallel count table (Part 10 Q28).
- *Any one LIS is enough?* Then patience sorting with predecessor pointers is O(n log n) and valid. The tie rule is what forces the table walk in this question.
- *Why from the right?* So `f[i]` means "starts at i" and the answer can be read forward, smallest index first.

**Common mistakes:**
- Returning `tails`.
- Building `f` ending at i and then scanning backwards, which yields the lexicographically LARGEST index list.
- Using `>=` and returning a non-decreasing subsequence.
- Forgetting the empty input.

### Q35 ⭐ 🟡 Longest non-decreasing subsequence and the bisect_left versus bisect_right choice. `nums` has 0 <= len <= 10^5 integers (|value| <= 10^9). Return `[nondecreasing_length, tails, strict_length]`: the length of the longest non-decreasing subsequence, the final patience-sorting `tails` array for that variant, and the length of the longest strictly increasing subsequence. Explain which of `bisect_left` and `bisect_right` each variant uses (see Part 5 Q11), and what answer you get if you use `bisect_left` for the non-decreasing variant (it silently computes the strict length). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsequences (len <= 12) on small inputs. Example: nums=[1, 3, 3, 2, 3] -> [4, [1, 2, 3, 3], 3]; nums=[5, 5, 5] -> [3, [5, 5, 5], 1]; nums=[2, 1] -> [1, [1], 1]; nums=[] -> [0, [], 0]; nums=[4, 4, 2, 9, 9, 1] -> [4, [1, 4, 9, 9], 2].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** LIS in O(n log n) by patience sorting: `tails[k]` is the smallest possible last value of a valid subsequence of length k + 1. The only change between strict and non-decreasing is which bisect you call.

**Say this first (1 line):** "Strict increasing uses `bisect_left` (an equal value replaces the equal one), non-decreasing uses `bisect_right` (an equal value goes after the equals); using `bisect_left` for non-decreasing silently returns the strict length."

**Brute force:** Enumerate all 2^n subsequences, test sortedness, and for each length keep the smallest last value. O(2^n * n), n <= 12 only. It gives the lengths and also the `tails` array, so the cross-check compares all three outputs.

**Optimal:**
- Invariant: after processing a prefix, `tails` is sorted (non-decreasing for the variant, strictly increasing for strict), and `tails[k]` is the minimum last value over all valid subsequences of length k + 1 in that prefix. The length of `tails` is the answer.
- For each `x`: find the position `p` where `x` belongs; if `p == len(tails)` append, else overwrite `tails[p] = x` (a smaller or equal tail of the same length is never worse).
- Non-decreasing: `p = bisect_right(tails, x)` = first index with `tails[p] > x`. An equal tail does NOT block `x`, so `x` extends the equal run. For `[5,5,5]`: every 5 goes to the end, `tails = [5,5,5]`.
- Strict: `p = bisect_left(tails, x)` = first index with `tails[p] >= x`. An equal tail blocks (x cannot follow an equal value), so `x` replaces it. For `[5,5,5]`: `tails = [5]`.
- Using `bisect_left` for non-decreasing gives exactly the strict length (I checked on 600 random lists: equal always; it was wrong for non-decreasing on 284 of them). Silent, no error. See Part 5 Q11 for `bisect_left` versus `bisect_right` semantics.
- The `tails` for the non-decreasing variant is not itself an answer subsequence either; only its length is. It is the same idea as Q34.
- Return value: `[len(nd_tails), nd_tails, len(strict_tails)]`, two passes of the same loop with different bisects.

**Complexity:** Time O(n log n): n elements, one binary search each (an overwrite or an append is O(1)). Space O(n) for `tails`. For n = 10^5 that is about 1.7 million comparisons.

**Dry run (first example):** `nums = [1, 3, 3, 2, 3]`.

| x | non-decreasing tails (`bisect_right`) | strict tails (`bisect_left`) |
|---|---|---|
| 1 | [1] | [1] |
| 3 | [1, 3] | [1, 3] |
| 3 | [1, 3, 3] (right of the equal 3) | [1, 3] (replaces the 3) |
| 2 | [1, 2, 3] (`bisect_right` at 2 is 1, replace the first 3) | [1, 2] (replace 3) |
| 3 | [1, 2, 3, 3] (append) | [1, 2, 3] (append) |

- Answer `[4, [1, 2, 3, 3], 3]`. A real non-decreasing subsequence of length 4 is `[1, 3, 3, 3]` (indices 0, 1, 2, 4); note `tails` ends in `[1,2,3,3]`, which is NOT a subsequence of `nums` in that order, because 2 sits after the first 3. That is normal: tails is not the subsequence.

**Code:**
```python
import bisect
import itertools
import random

random.seed(35)

def patience(nums, strict):
    """tails[k] = smallest possible last value of a valid subsequence of length k + 1."""
    find = bisect.bisect_left if strict else bisect.bisect_right
    tails = []
    for x in nums:
        p = find(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
    return tails

def solve(nums):
    nd = patience(nums, strict=False)      # bisect_right: an equal value goes AFTER the equals
    st = patience(nums, strict=True)       # bisect_left: an equal value REPLACES the equal
    return [len(nd), nd, len(st)]

def brute(nums):
    """Enumerate every subsequence; for each length keep the smallest last value."""
    n = len(nums)
    best_nd, best_st = {}, {}
    for L in range(1, n + 1):
        for c in itertools.combinations(range(n), L):
            v = [nums[i] for i in c]
            if all(v[t] <= v[t + 1] for t in range(L - 1)):
                best_nd[L] = min(best_nd.get(L, v[-1]), v[-1])
            if all(v[t] < v[t + 1] for t in range(L - 1)):
                best_st[L] = min(best_st.get(L, v[-1]), v[-1])
    return [len(best_nd), [best_nd[k] for k in sorted(best_nd)], len(best_st)]

def nondecreasing_with_bisect_left(nums):
    return len(patience(nums, strict=True))          # the classic slip

# ---- examples from the prompt
assert solve([1, 3, 3, 2, 3]) == [4, [1, 2, 3, 3], 3]
assert solve([5, 5, 5]) == [3, [5, 5, 5], 1]
assert solve([2, 1]) == [1, [1], 1]
assert solve([]) == [0, [], 0]
assert solve([4, 4, 2, 9, 9, 1]) == [4, [1, 4, 9, 9], 2]
print('examples ok')

# ---- step trace of the first example
nums = [1, 3, 3, 2, 3]
tr, tl = [], []
for x in nums:
    tr.append(x)
    tl.append((x, patience(tr, False), patience(tr, True)))
for x, a, b in tl:
    print(f'x={x}: non-decreasing tails (bisect_right) {a} | strict tails (bisect_left) {b}')

# ---- seeded random cross-check against the enumeration, plus an exhaustive sweep
cases = 0
for _ in range(500):
    nums = [random.randint(-5, 5) for _ in range(random.randint(0, 12))]
    assert solve(nums) == brute(nums), nums
    cases += 1
for n in range(0, 7):
    for nums in itertools.product(range(4), repeat=n):
        assert solve(list(nums)) == brute(list(nums)), nums
        cases += 1
print('cross-check passed on', cases, 'cases')

# ---- what bisect_left gives for the non-decreasing variant: the strict length, always
wrong = same = 0
for _ in range(600):
    nums = [random.randint(0, 5) for _ in range(random.randint(0, 10))]
    assert nondecreasing_with_bisect_left(nums) == solve(nums)[2]
    if nondecreasing_with_bisect_left(nums) != solve(nums)[0]:
        wrong += 1
print('bisect_left for non-decreasing equals the strict length on all 600; it is wrong for non-decreasing on', wrong)
print('example [5, 5, 5]: bisect_left gives', nondecreasing_with_bisect_left([5, 5, 5]), 'instead of 3')

# ---- edge cases and size
assert solve([7]) == [1, [7], 1]
assert solve([3, 2, 1]) == [1, [1], 1]
assert solve([1, 1, 2, 2]) == [4, [1, 1, 2, 2], 2]
big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
r = solve(big)
assert 1 <= r[2] <= r[0] <= len(big)
print('n = 10**5 random lengths (non-decreasing, strict):', r[0], r[2])
```

**Output (my run):**
```
examples ok
x=1: non-decreasing tails (bisect_right) [1] | strict tails (bisect_left) [1]
x=3: non-decreasing tails (bisect_right) [1, 3] | strict tails (bisect_left) [1, 3]
x=3: non-decreasing tails (bisect_right) [1, 3, 3] | strict tails (bisect_left) [1, 3]
x=2: non-decreasing tails (bisect_right) [1, 2, 3] | strict tails (bisect_left) [1, 2]
x=3: non-decreasing tails (bisect_right) [1, 2, 3, 3] | strict tails (bisect_left) [1, 2, 3]
cross-check passed on 5961 cases
bisect_left for non-decreasing equals the strict length on all 600; it is wrong for non-decreasing on 284
example [5, 5, 5]: bisect_left gives 1 instead of 3
n = 10**5 random lengths (non-decreasing, strict): 628 628
```

**Edge cases:**
- Empty list: `[0, [], 0]`.
- All equal: non-decreasing is n, strict is 1.
- Strictly decreasing: 1 and 1.
- Large values (10^9) and negatives are fine; only comparisons are used.
- If the problem says "non-increasing", negate the values (or reverse the list) and reuse the same routine.

**Follow-ups:**
- *Longest non-increasing subsequence?* Negate every value and run the non-decreasing version.
- *Why does overwriting with an equal value not matter in strict mode?* Same value, same position, nothing changes; replacing the equal is a no-op for the length and keeps the strict invariant.
- *Russian dolls?* A sort trick plus the strict version (Q40).

**Common mistakes:**
- `bisect_left` for the non-decreasing variant (the classic bug).
- `bisect_right` for strict, which counts equal values as extending.
- Returning `tails` as if it were the subsequence.
- Starting with `tails = [nums[0]]` and crashing on the empty list.

### Q36 ⭐ 🟡 Number of dice rolls with a target sum (counting with a modulus). You roll `n` dice, each with faces 1..k (1 <= n, k <= 30), and `target` is 0 <= target <= 1000. Return the number of ordered outcomes (sequences of n faces) whose sum is exactly `target`, modulo 10^9 + 7; 0 if impossible. Roll the table over dice with a single 1D array (a new array per die, no in-place hazards), say what the state is and why the answer is 0 outside n..n*k, and where the modulus is applied. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all k^n outcomes (k^n <= 10^5) on small inputs. Example: n=1, k=6, target=3 -> 1; n=2, k=6, target=7 -> 6; n=30, k=30, target=500 -> 222616187; n=2, k=5, target=1 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Counting DP over a rolling 1D array. The state is "dice thrown so far, sum so far", and one die is one layer.

**Say this first (1 line):** "`dp[s]` is the number of ordered outcomes of the dice thrown so far with sum s; each die builds a new array by adding faces 1..k, and I take the modulus on every addition."

**Brute force:** Enumerate all k^n sequences of faces and count those with the right sum. Exponential; fine only when k^n <= 10^5. It is the oracle.

**Optimal:**
- State: after j dice, `dp_j[s]` = the number of ordered sequences of j faces (each 1..k) that add to s.
- Base: `dp_0[0] = 1` (the empty sequence), every other `dp_0[s] = 0`.
- Transition: `dp_j[s] = sum over f = 1..k of dp_{j-1}[s - f]` (the last die shows f). Written "forward": for each s with `dp[s] != 0`, for each f, add `dp[s]` into `new[s + f]`.
- Answer: `dp_n[target]`, modulo 10^9 + 7.
- Rolling: only `dp_{j-1}` is needed for `dp_j`, so two 1D arrays of length `target + 1`. A NEW array per die is the safe form: updating one array in place would let a die's contribution be read again by the same die (the same hazard that breaks the upward 0/1 knapsack loop in Q37; here it would let one die show several faces).
- Why 0 outside n..n*k: each die contributes at least 1 and at most k, so n dice give a sum in `[n, n*k]`. Nothing can reach a target below n or above n*k, and the table never gets a nonzero entry there. I checked this for 4 dice with 6 faces: zero outside 4..24, positive inside. Target 0 gives 0 because n >= 1.
- Where the modulus goes: on every addition into `new[s + f]`, so every stored value stays below 10^9 + 7. Reducing only at the end also gives the right value in Python (big ints), but the numbers grow to about 43 digits for n = k = 30 (I measured) and larger for bigger inputs. In a fixed-width language the per-step reduction is mandatory.
- Faster: the sum over f is a sliding window of width k over `dp_{j-1}`, so one die costs O(target) instead of O(target * k). The code has that version and it matches on every case.
- Why no `dp[s]` for `s > target`: a partial sum above target can never come back down (faces are positive), so I do not store them.

**Complexity:** Time O(n * target * k) for the plain version, up to 30 * 1000 * 30 = 900000 steps (about 10^6); O(n * target) with the sliding window. Space O(target) for two arrays.

**Dry run (n = 1, k = 6, target = 3, then the table for n = 2):**
- One die: `dp_0 = [1,0,0,0]`; the die adds 1..6 but only sums up to 3 matter: `dp_1 = [0,1,1,1]`. `dp_1[3] = 1`. Matches the prompt.
- n = 2, k = 6, target = 7 (columns are sums 0..7):

| dice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 2 | 0 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |

- Row 2, sum 7: `dp_2[7] = dp_1[1] + ... + dp_1[6] = 6` (the six pairs (1,6) ... (6,1)). Row 1, sum 7 is 0 because one six-sided die cannot show 7.
- n = 2, k = 5, target = 1: row 2, sum 1 is 0 (two dice sum to at least 2).

**Code:**
```python
import itertools
import random

random.seed(36)
MOD = 10**9 + 7

def dice(n, k, target):
    """dp[s] = number of ordered outcomes of the dice thrown so far with sum s (s <= target)."""
    dp = [0] * (target + 1)
    dp[0] = 1                                   # zero dice: the empty sequence has sum 0
    for _ in range(n):
        nd = [0] * (target + 1)                 # a NEW array per die: no in-place hazard
        for s in range(target + 1):
            if dp[s]:
                for f in range(1, min(k, target - s) + 1):
                    nd[s + f] = (nd[s + f] + dp[s]) % MOD
        dp = nd
    return dp[target]

def dice_prefix(n, k, target):
    """Same answer in O(n * target) with a sliding window sum instead of the inner loop over faces."""
    dp = [1] + [0] * target
    for _ in range(n):
        nd = [0] * (target + 1)
        window = 0
        for s in range(1, target + 1):
            window += dp[s - 1]
            if s - 1 - k >= 0:
                window -= dp[s - 1 - k]
            nd[s] = window % MOD
            window %= MOD
        dp = nd
    return dp[target]

def brute(n, k, target):
    return sum(1 for r in itertools.product(range(1, k + 1), repeat=n) if sum(r) == target) % MOD

# ---- examples from the prompt
assert dice(1, 6, 3) == 1
assert dice(2, 6, 7) == 6
assert dice(30, 30, 500) == 222616187
assert dice(2, 5, 1) == 0
print('examples ok')

# ---- table for n = 2, k = 6, target = 7 (rows = dice thrown, columns = sums 0..7)
dp = [1] + [0] * 7
print('sum:      ', list(range(8)))
print('0 dice:   ', dp)
for d in (1, 2):
    nd = [0] * 8
    for s in range(8):
        for f in range(1, 7):
            if s + f <= 7:
                nd[s + f] += dp[s]
    dp = nd
    print(f'{d} dice:   ', dp)
assert dp[7] == 6

# ---- seeded cross-check against the enumeration of all k^n outcomes (k^n <= 10^5)
cases = 0
for _ in range(400):
    k = random.randint(1, 8)
    n = random.randint(1, 30)
    while k ** n > 10**5:
        n -= 1
    n = max(n, 1)
    t = random.randint(0, n * k + 3)
    exp = brute(n, k, t)
    assert dice(n, k, t) == exp == dice_prefix(n, k, t), (n, k, t)
    cases += 1
for n in range(1, 6):                      # exhaustive tiny sweep
    for k in range(1, 6):
        for t in range(0, n * k + 3):
            assert dice(n, k, t) == brute(n, k, t) == dice_prefix(n, k, t)
            cases += 1
print('cross-check passed on', cases, 'cases')

# ---- 0 outside n..n*k, and the modulus matters at the full size
assert all(dice(4, 6, t) == 0 for t in list(range(0, 4)) + list(range(25, 40)))
assert all(dice(4, 6, t) > 0 for t in range(4, 25))
assert dice(30, 30, 1000) == 0 and dice(30, 30, 30) == 1 and dice(30, 30, 900) == 1
big = dice(30, 30, 465)
exact = [1] + [0] * 465
for _ in range(30):                          # same DP with Python big ints and no modulus
    nd = [0] * 466
    for t in range(466):
        for f in range(1, 31):
            if t - f >= 0:
                nd[t] += exact[t - f]
    exact = nd
print('n=30, k=30, target=465: mod answer', big, '| exact count has', len(str(exact[465])), 'digits')
assert exact[465] % MOD == big and exact[465] > MOD
assert dice_prefix(30, 30, 465) == big
print('edge cases ok')
```

**Output (my run):**
```
examples ok
sum:       [0, 1, 2, 3, 4, 5, 6, 7]
0 dice:    [1, 0, 0, 0, 0, 0, 0, 0]
1 dice:    [0, 1, 1, 1, 1, 1, 1, 0]
2 dice:    [0, 0, 1, 2, 3, 4, 5, 6]
cross-check passed on 700 cases
n=30, k=30, target=465: mod answer 252370474 | exact count has 43 digits
edge cases ok
```

**Edge cases:**
- `target < n` or `target > n*k`: 0, with no special-case code needed.
- `k = 1`: exactly one outcome, the sum n.
- `target = 0`: 0 (n >= 1).
- Large n, k with the modulus: the exact count has 43 digits for n = k = 30, target 465, so the modulus really does bite.
- Use `[0] * (target + 1)` per die, not `[[0]*...]*...` aliasing (Q31).

**Follow-ups:**
- *Remove the factor k?* Sliding-window or prefix sums, as in the code, O(n * target).
- *Probability instead of a count?* Divide by k^n (use floats, or modular inverse for a modulus).
- *n up to 10^9?* Use the generating function `(x + ... + x^k)^n` with polynomial exponentiation (outside this part).

**Common mistakes:**
- Updating one array in place.
- Forgetting the modulus inside the inner loop (correct in Python but slow and unsafe elsewhere).
- Indexing `new[s + f]` past `target` (IndexError) without a bound.
- Using `dp[0] = 0` as the base, which makes everything 0.

### Q37 ⭐ 🟡 0/1 knapsack: which items (reconstruction with a tie rule). `weights` and `values` have equal length 1 <= len <= 100 (1 <= weight <= 100, 1 <= value <= 1000) and `cap` is 0 <= cap <= 1000. Return `[best, items]`: the maximum value and the list of chosen item indices in ascending order. If several subsets reach the maximum, return the one whose ascending index list is lexicographically smallest (a list that is a prefix of another is smaller). Explain why a 1D table cannot rebuild the items (you need the 2D table, or a bit per item and capacity) and how the table is read backwards. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets with the same tie rule (len <= 12) on small inputs. Example: weights=[1, 3, 4, 5], values=[1, 4, 5, 7], cap=7 -> [9, [1, 2]]; weights=[5], values=[10], cap=4 -> [0, []]; weights=[2, 2, 3], values=[3, 3, 5], cap=4 -> [6, [0, 1]]; weights=[1, 1, 1], values=[4, 4, 4], cap=2 -> [8, [0, 1]].
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2024 on-campus LeetCode Discuss post with a coin change discussion, a Naukri Code360 2020 report with a longest-decreasing-subsequence assessment, a GeeksforGeeks 2017 intern report with a 0-1 knapsack and a space-optimisation follow-up, a 2021 report with an unbounded-knapsack-like question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** 0/1 knapsack with reconstruction. Value-only needs a 1D array; recovering the items needs the full 2D table (or a bit per item and capacity).

**Say this first (1 line):** "I build `f[i][c]` = best value from items i..n-1 with capacity c, from the right, then walk it left to right taking item i whenever taking it still reaches `f[i][c]`; that gives the lexicographically smallest index list."

**Brute force:** Try all 2^n subsets, keep those within capacity, take the highest value and, among ties, the smallest index list (Python list comparison, where a prefix is smaller). O(2^n * n), n <= 12. It is the oracle.

**Optimal:**
- State: `f[i][c]` = maximum value using only items `i..n-1` with capacity c.
- Base: `f[n][c] = 0` for all c (no items left).
- Transition: `f[i][c] = max(f[i+1][c], values[i] + f[i+1][c - weights[i]])` where the second option exists only if `weights[i] <= c`. Skip or take.
- Answer value: `f[0][cap]`.
- Why from the right: so the walk goes forward through the items, and "the smallest index first" is just "decide item 0 first".
- Reconstruction walk: with `c = cap`, for i from 0: if `f[i][c] == 0` stop (all values are at least 1, so nothing more is worth taking, and stopping gives the shorter prefix); else if `weights[i] <= c` and `values[i] + f[i+1][c - weights[i]] == f[i][c]`, take i and reduce c. Otherwise skip.
- Why the tie rule works: among optimal subsets, the one with the smallest first index takes the first item that can start an optimal set. Taking i when it is feasible for the optimum gives a list starting with i, which beats every list starting with a larger index; the skip branch can only produce lists starting with larger indices. Same argument at every later step.
- Why a 1D table cannot rebuild: `dp[c]` after the last item says only the best value for capacity c. Each cell was overwritten by earlier items, so which item caused it is lost. Choices: keep the 2D table (O(n*cap) memory, here 100 * 1000 = 10^5 cells, fine), or store one bit per (item, capacity) saying whether item i was taken at c (the same size in bits).
- The 1D value-only version has the capacity loop DOWNWARD (`for c in range(cap, w-1, -1)`): `dp[c]` reads `dp[c - w]`, which must still hold the value from before this item. Going upward would reuse the item (unbounded knapsack). The code uses it only to cross-check the value.

**Complexity:** Time O(n * cap) (100 * 1001 about 10^5). Space O(n * cap) for the 2D table; the value alone needs O(cap). The enumeration oracle is O(2^n).

**Dry run (first example):** weights `[1,3,4,5]`, values `[1,4,5,7]`, cap 7. Row i uses items i..3.

| from item \ cap | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 1 | 4 | 5 | 7 | 8 | 9 |
| 1 | 0 | 0 | 0 | 4 | 5 | 7 | 7 | 9 |
| 2 | 0 | 0 | 0 | 0 | 5 | 7 | 7 | 7 |
| 3 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 7 |
| 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

- Value `f[0][7] = 9`.
- Walk: c = 7. i = 0: take it? `1 + f[1][6] = 1 + 7 = 8`, not 9: skip. i = 1: `4 + f[2][4] = 4 + 5 = 9`, equals `f[1][7] = 9`: take, c = 4. i = 2: `5 + f[3][0] = 5`, equals `f[2][4] = 5`: take, c = 0. i = 3: `f[3][0] = 0`, stop. Items `[1, 2]`, value 9.
- Tie check, third example `[2,2,3]` values `[3,3,5]`, cap 4: items 0 and 1 give 6 and item 2 alone gives 5, so `[0, 1]`.

**Code:**
```python
import itertools
import random

random.seed(37)

def best_1d(weights, values, cap):
    """Value only, O(cap) space. Capacity loop goes DOWNWARD so each item is used at most once."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]

def knapsack(weights, values, cap):
    """f[i][c] = best value using items i..n-1 with capacity c. Built from the right so the walk reads left to right."""
    n = len(weights)
    f = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for c in range(cap + 1):
            f[i][c] = f[i + 1][c]                                   # skip item i
            if weights[i] <= c:
                f[i][c] = max(f[i][c], values[i] + f[i + 1][c - weights[i]])   # take item i
    items, c = [], cap
    for i in range(n):
        if f[i][c] == 0:                      # values >= 1: nothing more is worth taking; stop (shorter prefix wins)
            break
        if weights[i] <= c and values[i] + f[i + 1][c - weights[i]] == f[i][c]:
            items.append(i)                   # taking i can still reach the optimum; i is the smallest such index
            c -= weights[i]
    return [f[0][cap], items], f

def brute(weights, values, cap):
    n = len(weights)
    cands = []
    for L in range(n + 1):
        for comb in itertools.combinations(range(n), L):
            if sum(weights[i] for i in comb) <= cap:
                cands.append((sum(values[i] for i in comb), list(comb)))
    mv = max(v for v, _ in cands)
    return [mv, min(c for v, c in cands if v == mv)]       # list comparison: prefix is smaller

def solve(weights, values, cap):
    return knapsack(weights, values, cap)[0]

# ---- examples from the prompt
assert solve([1, 3, 4, 5], [1, 4, 5, 7], 7) == [9, [1, 2]]
assert solve([5], [10], 4) == [0, []]
assert solve([2, 2, 3], [3, 3, 5], 4) == [6, [0, 1]]
assert solve([1, 1, 1], [4, 4, 4], 2) == [8, [0, 1]]
print('examples ok')

# ---- the table of the first example (rows i = items i..n-1 allowed, columns = capacity 0..7)
res, f = knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
print('cap       ', list(range(8)))
for i in range(5):
    print(f'from item {i}', f[i])
print('result', res)

# ---- seeded cross-check against the subset enumeration with the same tie rule
cases = 0
for _ in range(600):
    n = random.randint(1, 10)
    ws = [random.randint(1, 6) for _ in range(n)]
    vs = [random.randint(1, 9) for _ in range(n)]
    cap = random.randint(0, 20)
    got = solve(ws, vs, cap)
    assert got == brute(ws, vs, cap), (ws, vs, cap, got)
    assert best_1d(ws, vs, cap) == got[0]
    assert sum(ws[i] for i in got[1]) <= cap and sum(vs[i] for i in got[1]) == got[0]
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- why the 1D table cannot rebuild the items: dp[c] forgets which items made it
dp = [0] * 8
for w, v in zip([1, 3, 4, 5], [1, 4, 5, 7]):
    for c in range(7, w - 1, -1):
        dp[c] = max(dp[c], dp[c - w] + v)
print('1D table after all items:', dp, '-> value', dp[7], 'but nothing says WHICH items')

# ---- edge cases and full size
assert solve([3], [5], 3) == [5, [0]]
assert solve([1, 1], [1, 1], 0) == [0, []]
assert solve([2, 2], [3, 3], 2) == [3, [0]]                  # tie: smallest index list
W = [random.randint(1, 100) for _ in range(100)]
V = [random.randint(1, 1000) for _ in range(100)]
r = solve(W, V, 1000)
assert r[0] == best_1d(W, V, 1000) and sum(W[i] for i in r[1]) <= 1000
print('n = 100, cap = 1000 ok: value', r[0], 'with', len(r[1]), 'items')
```

**Output (my run):**
```
examples ok
cap        [0, 1, 2, 3, 4, 5, 6, 7]
from item 0 [0, 1, 1, 4, 5, 7, 8, 9]
from item 1 [0, 0, 0, 4, 5, 7, 7, 9]
from item 2 [0, 0, 0, 0, 5, 7, 7, 7]
from item 3 [0, 0, 0, 0, 0, 7, 7, 7]
from item 4 [0, 0, 0, 0, 0, 0, 0, 0]
result [9, [1, 2]]
cross-check passed on 600 cases
1D table after all items: [0, 1, 1, 4, 5, 7, 8, 9] -> value 9 but nothing says WHICH items
n = 100, cap = 1000 ok: value 27115 with 42 items
```

**Edge cases:**
- `cap = 0` or every weight above cap: `[0, []]`.
- Ties between equal-value subsets (`[1,1,1]` values 4, cap 2): `[0, 1]`, not `[1, 2]`.
- Exact fit (`weight == cap`) must be allowed (`<=`, not `<`).
- All items fit: every index in ascending order.
- Zero value does not occur (values >= 1); if it could, the stop-at-zero rule would need changing.

**Follow-ups:**
- *Memory-lean reconstruction?* Store one bitmask per capacity (the same information as the 2D table, packed).
- *Unbounded version?* Loop capacity upward, one 1D array (Q20 in this part).
- *Space for value only?* One array with a downward loop, as in `best_1d`.

**Common mistakes:**
- Looping capacity upward in the 1D table (reuses items).
- Building the table from item 0 and walking back, where the tie rule is awkward to get right; building from the right makes it a simple left-to-right scan.
- Not stopping at `f == 0`, then adding useless items that happen to fit.
- Returning item values instead of indices.

### Q38 ⭐ 🟡 Minimum cost for tickets. You will travel on the days listed in `days` (1 <= len <= 365, strictly increasing integers in 1..365). A 1-day pass costs `costs[0]`, a 7-day pass `costs[1]` and a 30-day pass `costs[2]` (1 <= each <= 1000); a d-day pass bought on day t covers days t..t+d-1. Return the minimum total cost to cover every travel day. Define `dp[d]` over calendar days (cost to cover all travel days up to d) and give the transition for travel and non-travel days. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion over the next uncovered travel day on small inputs. Example: days=[1, 4, 6, 7, 8, 20], costs=[2, 7, 15] -> 11; days=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], costs=[2, 7, 15] -> 17; days=[5], costs=[3, 2, 1] -> 1; days=[1, 30], costs=[5, 6, 7] -> 7.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 1D DP over calendar days with "buy a pass that ends today" choices. Think of it as a small unbounded-style cover problem on a line.

**Say this first (1 line):** "`dp[d]` is the cheapest cost to cover every travel day up to day d; a non-travel day copies `dp[d-1]`, and a travel day takes the best of a 1-day, 7-day or 30-day pass ending today, looking back 1, 7 or 30 days (clamped at 0)."

**Brute force:** Recursion over the next uncovered travel day: from travel day `days[i]`, try each pass, skip to the first travel day it does not cover, add its cost. Without a cache it is up to 3^n. With n <= 9 in the cross-check it is fine; with a cache on `i` it becomes O(n) states times 3 choices, the second DP form.

**Optimal:**
- State: `dp[d]` = minimum cost to cover all travel days that are `<= d`, for calendar day d in 0..last travel day.
- Base: `dp[0] = 0`.
- Non-travel day d: `dp[d] = dp[d-1]` (nothing needs covering on d, and any pass that covered up to d-1 is enough).
- Travel day d: `dp[d] = min(dp[d-1] + costs[0], dp[max(0, d-7)] + costs[1], dp[max(0, d-30)] + costs[2])`.
- Why the look-back is right: a pass that covers day d and is bought as late as possible covers `d-d_len+1 .. d`. Everything before that window must be covered by something else, and `dp[d - d_len]` is exactly the cost for everything up to `d - d_len`. The `max(0, ...)` clamp handles windows that start before day 1.
- Why "the pass ends today" is enough: when the pass covering day d is chosen, the days it can usefully cover are those up to d (anything later is handled by later states). Among the passes that cover d, the one that covers the most earlier days is the one ending on d. A pass that really ends later covers the same earlier days, so the DP loses nothing by pretending it ends on d.
- Answer: `dp[last]` where `last = days[-1]`.
- Costs need not be monotone (a 7-day pass may cost more than a 30-day pass). The min over the three options handles that; I tested random costs in 1..12 without forcing order.
- Space: `dp` is O(last) = O(365). A sliding window of 30 values would also do, but 365 is tiny.
- Variant on the days list: the same DP indexed by travel day (`dp[i]` and a pointer for each pass length) is O(n); the calendar form is simpler to explain.

**Complexity:** Time O(last) = O(365) steps, each with three lookups. Space O(last). The recursion oracle is up to O(3^n).

**Dry run (first example):** `days = [1,4,6,7,8,20]`, costs `[2,7,15]`.

| day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9..19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| travel? | | yes | | | yes | | yes | yes | yes | | yes |
| dp | 0 | 2 | 2 | 2 | 4 | 4 | 6 | 7 | 9 | 9 | 11 |

- Day 1: `min(0+2, 0+7, 0+15) = 2`. Days 2, 3: copy 2. Day 4: `min(2+2, dp[0]+7, dp[0]+15) = 4`. Day 5: copy 4. Day 6: `min(4+2, 0+7, 0+15) = 6`.
- Day 7: `min(6+2 = 8, dp[0]+7 = 7, ...) = 7`: one 7-day pass bought on day 1 covers days 1, 4, 6, 7.
- Day 8: `min(7+2 = 9, dp[1]+7 = 9, dp[0]+15 = 15) = 9`. Days 9..19 copy 9.
- Day 20: `min(9+2 = 11, dp[13]+7 = 16, dp[0]+15 = 15) = 11`. Answer 11.

**Code:**
```python
import random
import sys

random.seed(38)

def min_cost(days, costs):
    """dp[d] = minimum cost to cover every travel day <= d. Calendar days 0..last."""
    travel = set(days)
    last = days[-1]
    dp = [0] * (last + 1)                       # dp[0] = 0: nothing to cover yet
    for d in range(1, last + 1):
        if d not in travel:
            dp[d] = dp[d - 1]                   # a non-travel day costs nothing extra
        else:
            dp[d] = min(dp[d - 1] + costs[0],              # 1-day pass covers d only
                        dp[max(0, d - 7)] + costs[1],      # 7-day pass covers d-6..d
                        dp[max(0, d - 30)] + costs[2])     # 30-day pass covers d-29..d
    return dp[last], dp

def rec(days, costs):
    """Plain recursion over the next uncovered travel day (index into days)."""
    n = len(days)
    def f(i):
        if i >= n:
            return 0
        best = float('inf')
        for span, c in zip((1, 7, 30), costs):
            j = i
            while j < n and days[j] < days[i] + span:    # the pass bought on days[i] covers these
                j += 1
            best = min(best, c + f(j))
        return best
    return f(0)

# ---- examples from the prompt
assert min_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])[0] == 11
assert min_cost([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])[0] == 17
assert min_cost([5], [3, 2, 1])[0] == 1
assert min_cost([1, 30], [5, 6, 7])[0] == 7
print('examples ok')

# ---- table for the first example
ans, dp = min_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])
print('day :', list(range(len(dp))))
print('dp  :', dp)
print('answer', ans)

# ---- seeded cross-check against the plain recursion
cases = 0
for _ in range(600):
    n = random.randint(1, 9)
    days = sorted(random.sample(range(1, random.choice([10, 40, 80]) + 1), n))
    costs = [random.randint(1, 12) for _ in range(3)]          # not forced to be monotone
    assert min_cost(days, costs)[0] == rec(days, costs), (days, costs)
    cases += 1
print('cross-check passed on', cases, 'cases')

# ---- edge cases and full size
assert min_cost([1], [1, 1, 1])[0] == 1
assert min_cost([365], [1000, 1000, 1000])[0] == 1000
full = min_cost(list(range(1, 366)), [2, 7, 15])[0]
print('every day of the year with costs [2, 7, 15]:', full)
assert full == 12 * 15 + 7                                  # twelve 30-day passes (360 days) + one 7-day pass for 5 days
assert min_cost([1, 8, 15], [10, 1, 1])[0] == 1              # one cheap 30-day pass covers all three
assert min_cost([1, 8, 15], [10, 5, 1])[0] == 1
print('edge cases ok')
```

**Output (my run):**
```
examples ok
day : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
dp  : [0, 2, 2, 2, 4, 4, 6, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11]
answer 11
cross-check passed on 600 cases
every day of the year with costs [2, 7, 15]: 187
edge cases ok
```

**Edge cases:**
- One travel day: the cheapest of the three costs (`days=[5]`, costs `[3,2,1]` gives 1: a 30-day pass is the cheapest ticket).
- Look-back below day 1: clamp with `max(0, ...)`, otherwise a negative index silently reads the END of the list.
- Day 365 with the longest pass: no day beyond 365 is needed; the pass just covers extra days.
- Costs not monotone: take the min over all three, do not assume the longer pass is cheaper per day.
- Every day of the year with costs [2,7,15]: twelve 30-day passes (360 days) plus a 7-day pass for the last 5 days, 187 (checked in the code).

**Follow-ups:**
- *Why not greedy (always the cheapest per day)?* The pass cost per day is not enough: partial coverage and gaps matter, and the DP shows 7 beating 2+2+2+2 at day 7.
- *More pass types?* Add another term to the min; time O(last * types).
- *Very large day range?* Index by travel day and use pointers, O(n).

**Common mistakes:**
- `dp[d-7]` with d < 7 (negative index) instead of the clamp.
- Forgetting the non-travel copy case, which makes the min apply to every day and overcounts.
- Reading "7-day pass bought on day t covers t..t+6" and looking back 6 or 8 days; the window ending at d is `d-6..d`, so the look-back is `dp[d-7]`.

### Q39 ⭐ 🔴 Ones and zeroes (a knapsack with two capacities). `strs` is a list of 1 <= len <= 100 non-empty binary strings (each of length <= 100), and `m`, `n` are 0 <= m, n <= 100. Return the size of the largest subset of strings that uses at most m zeros and at most n ones in total. The table has two capacity axes and each string is an item taken at most once, so both loops run downward. This is the concept edge of 2D DP (grids and strings are Part 11); say what the state is, the transition, and the time O(len * m * n). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an enumeration of all subsets (len <= 12) on small inputs. Example: strs=['10', '0001', '111001', '1', '0'], m=5, n=3 -> 4; strs=['10', '0', '1'], m=1, n=1 -> 2; strs=['0'], m=0, n=5 -> 0.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** 0/1 knapsack with TWO capacities (zeros and ones), each string an item of weight `(zeros, ones)` and value 1. This is the concept edge of 2D DP; grids and string DPs are Part 11.

**Say this first (1 line):** "`dp[a][b]` is the most strings I can take using at most a zeros and b ones; for each string I update the table with both loops going downward, so a string is used at most once; time is O(len * m * n)."

**Brute force:** Try all 2^len subsets, keep those whose total zeros are at most m and total ones at most n, return the largest size. O(2^len * total length). len <= 12 in the cross-check.

**Optimal:**
- State: after processing some strings, `dp[a][b]` = the maximum number of those strings that can be chosen with total zeros `<= a` and total ones `<= b`. The table has `(m + 1) x (n + 1)` cells and it is "at most", so `dp[a][b]` is non-decreasing in both a and b.
- Base: all zeros (the empty subset is always allowed).
- Transition for a string with `z` zeros and `o` ones: `dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)` for `a >= z` and `b >= o`. Skip (keep the old value) or take (one more string, paying `z` and `o`).
- Why both loops go downward: `dp[a - z][b - o]` must still be the value from BEFORE this string. In the downward order, cell `(a - z, b - o)` is smaller in both coordinates, so it has not been updated yet for this string. In the upward order it has, and the string is counted again. A string with `z = 0` or `o = 0` makes it obvious: the code shows `['0']`, m = 3, n = 0 gives 3 with the upward loops, but the true answer is 1. The upward version was wrong on 329 of 500 random cases.
- Order of the two loops among themselves does not matter (any order where each inner index goes down is fine), as long as both are downward and the item loop is outermost.
- Same idea as the 1D 0/1 knapsack (Q37 value-only form), one dimension more.
- The state cannot be a single number because two budgets can bind independently; both must be tracked.

**Complexity:** Time O(len * m * n) = up to 100 * 100 * 100 = 10^6 updates. Space O(m * n) = 10^4 cells (the item dimension is rolled away by the downward loops). Counting zeros per string is O(total length).

**Dry run (first example):** strings `10, 0001, 111001, 1, 0`, m = 5 zeros, n = 3 ones. Items as `(zeros, ones)`: `(1,1)`, `(3,1)`, `(2,4)`, `(0,1)`, `(1,0)`.
- `111001` has 4 ones, more than n = 3, so it can never be taken: the table does not change for it (the loop range for b is empty).
- After `10` (1,1): every cell with `a >= 1`, `b >= 1` is 1.
- After `0001` (3,1): cells with `a >= 4`, `b >= 2` become 2 (take both): for example `dp[4][2] = dp[1][1] + 1 = 2`.
- After `1` (0,1): `dp[4][3]` becomes `dp[4][2] + 1 = 3`.
- After `0` (1,0): `dp[5][3] = dp[4][3] + 1 = 4`.
- Answer `dp[5][3] = 4`: take `10`, `0001`, `1`, `0` (zeros 1 + 3 + 0 + 1 = 5, ones 1 + 1 + 1 + 0 = 3). The printed table after each string is in the output below (rows are zeros allowed 0..5, columns ones allowed 0..3).

**Code:**
```python
import itertools
import random

random.seed(39)

def ones_zeroes(strs, m, n):
    """dp[a][b] = largest subset of the strings seen so far using at most a zeros and b ones."""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0')
        o = len(s) - z
        for a in range(m, z - 1, -1):              # both loops DOWNWARD: each string is used at most once
            for b in range(n, o - 1, -1):
                dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]

def upward_bug(strs, m, n):
    """WRONG: upward loops let a string be reused (it behaves like an unbounded item)."""
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0')
        o = len(s) - z
        for a in range(z, m + 1):
            for b in range(o, n + 1):
                dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]

def brute(strs, m, n):
    k, best = len(strs), 0
    for mask in range(1 << k):
        ch = [strs[i] for i in range(k) if mask >> i & 1]
        if sum(s.count('0') for s in ch) <= m and sum(s.count('1') for s in ch) <= n:
            best = max(best, len(ch))
    return best

# ---- examples from the prompt
assert ones_zeroes(['10', '0001', '111001', '1', '0'], 5, 3) == 4
assert ones_zeroes(['10', '0', '1'], 1, 1) == 2
assert ones_zeroes(['0'], 0, 5) == 0
print('examples ok')

# ---- table for the first example: dp after each string (rows a = zeros allowed 0..5, columns b = ones allowed 0..3)
strs = ['10', '0001', '111001', '1', '0']
m, n = 5, 3
dp = [[0] * (n + 1) for _ in range(m + 1)]
for s in strs:
    z = s.count('0'); o = len(s) - z
    for a in range(m, z - 1, -1):
        for b in range(n, o - 1, -1):
            dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    print(f'after {s!r} (zeros {z}, ones {o}):', dp)
assert dp[m][n] == 4

# ---- seeded cross-check against the enumeration of all subsets (len <= 12)
cases = diff_upward = 0
for _ in range(500):
    k = random.randint(1, 12)
    strs = [''.join(random.choice('01') for _ in range(random.randint(1, 5))) for _ in range(k)]
    m, n = random.randint(0, 8), random.randint(0, 8)
    assert ones_zeroes(strs, m, n) == brute(strs, m, n), (strs, m, n)
    if upward_bug(strs, m, n) != ones_zeroes(strs, m, n):
        diff_upward += 1
    cases += 1
print('cross-check passed on', cases, 'cases; the upward-loop version was wrong on', diff_upward)
print("upward on ['0'], m=3, n=0:", upward_bug(['0'], 3, 0), '(true answer', ones_zeroes(['0'], 3, 0), ')')

# ---- edge cases and full size
assert ones_zeroes(['0'], 0, 5) == 0 and ones_zeroes(['1'], 5, 0) == 0 and ones_zeroes(['01'], 1, 1) == 1
assert ones_zeroes(['0', '0', '0'], 2, 0) == 2
big = [''.join(random.choice('01') for _ in range(random.randint(1, 100))) for _ in range(100)]
print('len = 100, m = n = 100:', ones_zeroes(big, 100, 100))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
after '10' (zeros 1, ones 1): [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1]]
after '0001' (zeros 3, ones 1): [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2]]
after '111001' (zeros 2, ones 4): [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2]]
after '1' (zeros 0, ones 1): [[0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 3], [0, 1, 2, 3]]
after '0' (zeros 1, ones 0): [[0, 1, 1, 1], [1, 2, 2, 2], [1, 2, 3, 3], [1, 2, 3, 3], [1, 2, 3, 3], [1, 2, 3, 4]]
cross-check passed on 500 cases; the upward-loop version was wrong on 329
upward on ['0'], m=3, n=0: 3 (true answer 1 )
len = 100, m = n = 100: 20
edge cases ok
```

**Edge cases:**
- A string with more ones than n or more zeros than m can never be taken; the loop range is empty and the table is untouched.
- `m = 0` or `n = 0`: only strings made entirely of the other digit can be taken (`['0']`, m = 0, n = 5 gives 0; with m = 1 it gives 1).
- Identical strings are separate items (`['0','0','0']`, m = 2 gives 2).

**Follow-ups:**
- *Memory?* Already O(m * n); the item dimension is gone.
- *Maximise total length instead of count?* Use value `len(s)` instead of 1.
- *Why is this a Part 11 concept?* Two capacity axes make the table 2D; Part 11 covers grids, strings and intervals, where the table axes are positions rather than budgets.

**Common mistakes:**
- Upward loops on either axis (reuses strings).
- Putting the item loop inside the capacity loops (the table then mixes items; the item loop must be outermost).
- Counting ones as `s.count('1')` and zeros as `len(s) - ones` is fine; mixing the two up swaps m and n.
- Forgetting that `dp` is "at most", so the answer is `dp[m][n]`, not a max over cells.

### Q40 ⭐ 🔴 Russian doll envelopes (LIS with a sort trick). `envelopes` is a list of 0 <= len <= 10^5 pairs [w, h] (1 <= w, h <= 10^9). One envelope fits inside another only if BOTH its width and its height are strictly smaller. Return the maximum number of envelopes in a nesting chain (0 for an empty list). Sort by width ascending and, for equal widths, height DESCENDING, then take the strict LIS of the heights with `bisect_left` (Part 5 Q11); explain why the descending tie-break stops two envelopes of equal width from chaining. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against an O(n^2) DP over pairs that checks both dimensions strictly on small inputs. Example: envelopes=[[5, 4], [6, 4], [6, 7], [2, 3]] -> 3; envelopes=[[1, 1], [1, 1], [1, 1]] -> 1; envelopes=[] -> 0; envelopes=[[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]] -> 4.
**Asked at:** DP pattern guides and lists (techinterview.org 1D dynamic-programming interview patterns and DP recurrence guides, DesignGurus common DP questions, IGotAnOffer DP interview questions; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** A two-dimensional "both strictly smaller" chain reduced to a 1D strict LIS by sorting one dimension. The tie-break on the sorted dimension is the whole trick.

**Say this first (1 line):** "Sort by width ascending and, for equal widths, height DESCENDING, then take the strict LIS of the heights with `bisect_left`; the descending tie-break makes it impossible to pick two envelopes of the same width in one increasing run."

**Brute force:** Sort, then `dp[i]` = longest chain ending at envelope i = 1 + the best `dp[j]` over earlier `j` with BOTH width and height strictly smaller. O(n^2) time, O(n) space. Correct, but 10^10 pair checks at n = 10^5. It is the oracle.

**Optimal:**
- After sorting by width, widths never decrease along the list, so the width condition holds automatically between envelopes with different widths (earlier is smaller or equal). What remains is the height condition and the equal-width exception.
- Take the heights in sorted order and compute the strictly increasing LIS with the patience method (Q7): `tails[k]` is the smallest possible last height of a chain of length k + 1; `bisect_left` finds the position, so an equal height replaces rather than extends.
- Why heights DESCENDING on equal width: two envelopes with the same width cannot nest (width must be strictly smaller). If the equal-width group were sorted ascending by height, say `(4,5)` then `(4,6)`, the heights `5, 6` would form an increasing step and the LIS could use both. Sorted descending, `6` comes before `5`, and no strictly increasing run can take two heights from one descending group, so at most one envelope per width is picked.
- Why that loses nothing: if a chain uses one envelope of width w, any envelope of width w with the same or better height works equally; the LIS picks the best one on its own.
- Counterexample (verified): `[[4,5],[4,6],[6,7],[2,3],[1,1]]`. Ascending tie-break gives heights `1,3,5,6,7` and LIS 5, which is wrong. The true answer is 4 (for example `(1,1),(2,3),(4,5),(6,7)`). Descending gives heights `1,3,6,5,7`, strict LIS 4. On 600 random small inputs the ascending tie-break was wrong 282 times (the exact count varies with the seed).
- Equal envelopes `[[1,1],[1,1],[1,1]]`: same width, so they are in one group and a chain of 1 results. And with `bisect_left`, equal heights from different widths do not chain either (height must be strictly smaller): `[[1,5],[2,5],[3,5]]` gives 1.

**Complexity:** Time O(n log n): the sort is O(n log n) and each of the n heights does one binary search. Space O(n) for the sorted copy and `tails`. For n = 10^5 that is about 1.7 million binary-search steps plus the sort.

**Dry run (first example):** `[[5,4],[6,4],[6,7],[2,3]]`.
- Sort by (width asc, height desc): `[2,3], [5,4], [6,7], [6,4]`. Heights: `3, 4, 7, 4`.

| h | `bisect_left(tails, h)` | action | tails |
|---|---|---|---|
| 3 | 0 | append | [3] |
| 4 | 1 | append | [3, 4] |
| 7 | 2 | append | [3, 4, 7] |
| 4 | 1 | replace the 4 | [3, 4, 7] |

- Answer 3: `[2,3] -> [5,4] -> [6,7]`. The last 4 (width 6) could not extend anything, and it cannot follow `[5,4]` because the height 4 is not strictly larger than 4.

**Code:**
```python
import bisect
import random

random.seed(40)

def lis_strict(heights):
    tails = []
    for h in heights:
        p = bisect.bisect_left(tails, h)       # strict: an equal height replaces, never extends
        if p == len(tails):
            tails.append(h)
        else:
            tails[p] = h
    return len(tails)

def russian_doll(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], -e[1]))     # width up, height DOWN on equal width
    return lis_strict([h for _, h in order])

def ascending_tiebreak_bug(envelopes):
    order = sorted(envelopes, key=lambda e: (e[0], e[1]))      # WRONG tie-break
    return lis_strict([h for _, h in order])

def brute(envelopes):
    """O(n^2) DP over pairs, checking BOTH dimensions strictly."""
    es = sorted(envelopes)
    n = len(es)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if es[j][0] < es[i][0] and es[j][1] < es[i][1]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)

# ---- examples from the prompt
assert russian_doll([[5, 4], [6, 4], [6, 7], [2, 3]]) == 3
assert russian_doll([[1, 1], [1, 1], [1, 1]]) == 1
assert russian_doll([]) == 0
assert russian_doll([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]) == 4
print('examples ok')

# ---- walk-through of the first example
env = [[5, 4], [6, 4], [6, 7], [2, 3]]
order = sorted(env, key=lambda e: (e[0], -e[1]))
print('sorted (w asc, h desc):', order)
tails = []
for _, h in order:
    p = bisect.bisect_left(tails, h)
    tails[p:p + 1] = [h]
    print(f'  h={h}: position {p}, tails = {tails}')
print('answer', len(tails))

# ---- why descending: with an ascending tie-break equal widths chain
E2 = [[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]]
print('ascending tie-break on', E2, '->', ascending_tiebreak_bug(E2), '| correct', russian_doll(E2))
assert ascending_tiebreak_bug(E2) == 5 and brute(E2) == 4

# ---- seeded cross-check against the O(n^2) pair DP
cases = bad_asc = 0
for _ in range(600):
    n = random.randint(0, 14)
    es = [[random.randint(1, 6), random.randint(1, 6)] for _ in range(n)]
    got = russian_doll(es)
    assert got == brute(es), es
    if ascending_tiebreak_bug(es) != got:
        bad_asc += 1
    cases += 1
print('cross-check passed on', cases, 'cases; the ascending tie-break was wrong on', bad_asc)

# ---- edge cases and full size
assert russian_doll([[3, 3]]) == 1
assert russian_doll([[1, 5], [1, 6], [1, 7]]) == 1             # same width never nests
assert russian_doll([[1, 5], [2, 5], [3, 5]]) == 1             # same height never nests
assert russian_doll([[i, i] for i in range(1, 101)]) == 100
big = [[random.randint(1, 10**9), random.randint(1, 10**9)] for _ in range(10**5)]
print('n = 10**5 random envelopes, chain length:', russian_doll(big))
print('edge cases ok')
```

**Output (my run):**
```
examples ok
sorted (w asc, h desc): [[2, 3], [5, 4], [6, 7], [6, 4]]
  h=3: position 0, tails = [3]
  h=4: position 1, tails = [3, 4]
  h=7: position 2, tails = [3, 4, 7]
  h=4: position 1, tails = [3, 4, 7]
answer 3
ascending tie-break on [[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]] -> 5 | correct 4
cross-check passed on 600 cases; the ascending tie-break was wrong on 282
n = 10**5 random envelopes, chain length: 611
edge cases ok
```

**Edge cases:**
- Empty list: 0.
- All identical envelopes: 1.
- Same width, many heights: 1 (descending tie-break).
- Same height, many widths: 1 (`bisect_left` replaces equal heights).
- A perfect chain `(i, i)`: n.
- Widths and heights up to 10^9: only comparisons are used.

**Follow-ups:**
- *Recover the actual chain?* Keep predecessor pointers as in Q34; the descending tie-break does not change that.
- *Three dimensions (boxes)?* This sort trick does not extend directly; the usual answer is the O(n^2) DP over sorted triples or a CDQ divide and conquer (beyond this part).
- *Can the sort be by height instead?* Yes, by symmetry.

**Common mistakes:**
- Ascending tie-break on height (counts equal-width envelopes as nesting).
- `bisect_right` for the LIS (counts equal heights as nesting).
- Sorting by width only, leaving the order of equal widths arbitrary.
- Applying the O(n^2) DP at n = 10^5 and timing out.

