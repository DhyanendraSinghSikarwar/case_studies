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
