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
