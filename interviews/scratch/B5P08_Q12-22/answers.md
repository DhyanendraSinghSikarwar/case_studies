### Q12 ⭐⭐⭐ 🟡 Jump game (can you reach the end). `nums` holds non-negative integers (1 <= len <= 10^4), where nums[i] is the maximum jump length from index i (any length from 0 to nums[i] is allowed). Starting at index 0, return True if you can reach the last index. Give the O(n) greedy that tracks the farthest reachable index and returns False when the scan reaches an index beyond it, state the invariant, and say why the DP and the BFS versions are O(n^2) in the worst case. Example: nums=[2, 3, 1, 1, 4] -> True; nums=[3, 2, 1, 0, 4] -> False; nums=[0] -> True; nums=[1, 0, 1] -> False.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with an invariant: track the farthest reachable index while scanning left to right.

**Say this first (1 line):** "I scan once and keep `far`, the farthest index I can reach from the indices I have already visited. If the scan hits an index bigger than `far`, I am stuck, so False. Otherwise True."

**Brute force:**
- DP or BFS: from every reachable index `i`, mark all of `i+1 .. i+nums[i]` reachable.
- Worst case is `nums = [n, n, ..., n]`. Every index is reachable and each one marks about n - i cells, so the total is n(n-1)/2 marks. That is O(n^2) time (the run below counts 1,999,000 marks for n = 2000).
- BFS has the same count: each index is queued once, but each pop scans its whole jump range, so the edge scans add up to the same O(n^2).

**Optimal:**
- One pass. `far = 0`. For each `i`: if `i > far`, return False. Else `far = max(far, i + nums[i])`.
- **Invariant:** before step `i`, every index in `0..far` is reachable, and nothing beyond `far` is. Reachable set is always a prefix, because from any reachable index you can take any shorter jump too (lengths 0 to `nums[i]`). That prefix property is why one number is enough.
- If the scan gets through the last index, it was reachable. Early exit when `far >= n - 1` is optional.
- Failure is exactly "some index `i` has `i > far`": a block of zeros (or small values) that no earlier jump clears.

**Complexity:** Time O(n), one pass. Space O(1). The DP and BFS are O(n) space and O(n^2) time.

**Dry run:** `[3, 2, 1, 0, 4]`.
| i | nums[i] | i > far? | far after |
|---|---|---|---|
| 0 | 3 | no (0 > 0 is false) | 3 |
| 1 | 2 | no | 3 |
| 2 | 1 | no | 3 |
| 3 | 0 | no (3 > 3 is false) | 3 |
| 4 | 4 | yes (4 > 3) | return False |

Every path lands on index 3, which has a 0, so index 4 is out of reach.

**Code:**
```python
import random
import itertools

random.seed(12)

def can_reach_greedy(nums):
    far = 0                                  # farthest index reachable so far
    for i, x in enumerate(nums):
        if i > far:                          # index i is out of reach: stuck
            return False
        far = max(far, i + x)
        if far >= len(nums) - 1:             # early exit, optional
            return True
    return True

def can_reach_dp(nums):                      # forward marking, O(n^2) worst case
    n = len(nums)
    ok = [False] * n
    ok[0] = True
    for i in range(n):
        if ok[i]:
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                ok[j] = True
    return ok[-1]

def can_reach_bfs(nums):                     # explicit queue, also O(n^2) worst case
    from collections import deque
    n = len(nums)
    seen = [False] * n
    seen[0] = True
    q = deque([0])
    while q:
        i = q.popleft()
        if i == n - 1:
            return True
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if not seen[j]:
                seen[j] = True
                q.append(j)
    return False

# --- the four examples in the prompt
for nums, exp in [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False), ([0], True), ([1, 0, 1], False)]:
    assert can_reach_greedy(nums) == can_reach_dp(nums) == can_reach_bfs(nums) == exp
    print(nums, '->', can_reach_greedy(nums))

# --- exhaustive: every list of length 1..6 with values 0..4 (5^1 + ... + 5^6 = 19530 lists)
cnt = 0
for n in range(1, 7):
    for nums in itertools.product(range(5), repeat=n):
        nums = list(nums)
        g = can_reach_greedy(nums)
        assert g == can_reach_dp(nums) == can_reach_bfs(nums), nums
        cnt += 1
print('exhaustive ok:', cnt, 'lists')

# --- seeded random
for _ in range(500):
    nums = [random.randint(0, 6) for _ in range(random.randint(1, 30))]
    assert can_reach_greedy(nums) == can_reach_dp(nums)
print('random ok: 500 lists')

# --- worst case for the DP: huge jumps, every index reachable, n inner steps each
n = 2000
big = [n] * n
ops = sum(min(n, i + big[i] + 1) - (i + 1) for i in range(n))
print('DP inner steps on n=2000 all-big jumps:', ops, '(about n^2 / 2); greedy scans', n)
assert ops == n * (n - 1) // 2

# --- edge cases
assert can_reach_greedy([0]) is True
assert can_reach_greedy([0, 1]) is False       # stuck at index 0
assert can_reach_greedy([1, 0]) is True        # a 0 on the last index is fine
assert can_reach_greedy([5, 0, 0, 0, 0, 0]) is True
assert can_reach_greedy([1, 1, 0, 1]) is False
assert can_reach_greedy([0] * 10000) is False
assert can_reach_greedy([1] * 10000) is True
print('edge cases ok')
```

**Output (my run):**
```
[2, 3, 1, 1, 4] -> True
[3, 2, 1, 0, 4] -> False
[0] -> True
[1, 0, 1] -> False
exhaustive ok: 19530 lists
random ok: 500 lists
DP inner steps on n=2000 all-big jumps: 1999000 (about n^2 / 2); greedy scans 2000
edge cases ok
```

**Edge cases:**
- `[0]`: one element, already at the end, True. `[0, 1]`: stuck at 0, False.
- A zero on the LAST index is fine (`[1, 0]` is True). A zero in the middle is only fatal if `far` equals that index.
- Ten thousand zeros: False at i = 1. Ten thousand ones: True.
- Large `nums[i]` just saturates `far`; Python ints cannot overflow, so `i + nums[i]` is safe.

**Follow-ups:**
- Minimum number of jumps? Q13 in this part: same `far`, but count level ends.
- Backward version? Keep `goal = n - 1`; for `i` from the end, if `i + nums[i] >= goal` then `goal = i`. True if `goal == 0`. Same O(n).
- Return the path? Store the parent of each index when `far` improves, or use the DP version.

**Common mistakes:**
- Using `<` instead of `<=` for the stuck test: `i > far` is the stuck condition, `i == far` is still reachable.
- Taking `nums[i]` as the exact jump length (it is the maximum).
- Greedy "always jump the maximum": fails on `[2, 3, 1, 1, 4]`-style inputs where a shorter jump lands on a bigger number.
- Calling it DP-with-memoised-recursion on n = 10^4: recursion depth hits the limit.

### Q13 ⭐⭐⭐ 🟡 Jump game II (minimum jumps). Same moves as the reachability version: nums[i] is the maximum jump length from index i, 1 <= len <= 10^4, and the last index is guaranteed reachable. Return the minimum number of jumps from index 0 to the last index (0 when len is 1). Give the O(n) greedy that treats the reachable indices as BFS levels (current level end, farthest next reach, count a jump when the scan hits the level end), and say why this is BFS without a queue and why the scan stops before the last index. Example: nums=[2, 3, 1, 1, 4] -> 2; nums=[2, 3, 0, 1, 4] -> 2; nums=[0] -> 0; nums=[1, 1, 1, 1] -> 3.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** BFS levels without a queue. The set of indices reachable in k jumps is always a contiguous prefix, so a level is just an index range.

**Say this first (1 line):** "It is BFS where level k is the range of indices reachable in exactly k jumps. I scan the level, track the farthest index the next level can reach, and when I finish the level I count a jump."

**Brute force:**
- BFS (queue) or DP: `d[j] = min(d[j], d[i] + 1)` for every `j` in `i+1 .. i+nums[i]`.
- Correct, but each index scans its whole jump range: O(n^2) on `[n, n, ..., n]`. I use both as oracles in the code.

**Optimal:**
- Three variables: `jumps`, `level_end` (last index of the current level), `far` (farthest index reachable from anything scanned so far).
- For each `i`: `far = max(far, i + nums[i])`. When `i == level_end` the level is finished, so `jumps += 1` and `level_end = far`.
- Why it is BFS: level k is `(end of level k-1, end of level k]`. Everything in it was first reached by jump k. `far` while scanning level k is the end of level k+1.
- Why the scan stops before the last index: once `level_end >= n - 1` the last index is already inside the next level and we have counted the jump that gets there. If we scanned index `n - 1` itself and it happened to equal `level_end`, we would count one phantom jump (`[0]` would give 1, `[2, 3, 1, 1, 4]` would give 3; the code prints both).
- Guaranteed reachable means `far` never gets stuck below `n - 1`, so `level_end` always advances.

**Complexity:** Time O(n), one pass. Space O(1).

**Dry run:** `[2, 3, 1, 1, 4]`, `jumps = end = far = 0`.
| i | far | i == end? | jumps | end |
|---|---|---|---|---|
| 0 | 2 | yes | 1 | 2 |
| 1 | 4 | no | 1 | 2 |
| 2 | 4 | yes | 2 | 4 |
| 3 | 4 | no | 2 | 4 |

The loop stops at i = 3 (before index 4). Answer 2: jump 0 -> 1 (length 1), then 1 -> 4 (length 3).

**Code:**
```python
import random
import itertools
from collections import deque

random.seed(13)

def min_jumps_greedy(nums):
    jumps = 0
    level_end = 0                            # last index of the current BFS level
    far = 0                                  # farthest index reachable from the current level
    for i in range(len(nums) - 1):           # stop BEFORE the last index
        far = max(far, i + nums[i])
        if i == level_end:                   # finished scanning this level: one more jump
            jumps += 1
            level_end = far
    return jumps

def min_jumps_bfs(nums):                     # real BFS, O(n^2) worst case
    n = len(nums)
    dist = [-1] * n
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if dist[j] < 0:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist[-1]

def min_jumps_dp(nums):                      # forward relaxation, O(n^2)
    n = len(nums)
    INF = 10 ** 9
    d = [INF] * n
    d[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            d[j] = min(d[j], d[i] + 1)
    return d[-1]

def reachable(nums):
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + x)
    return True

for nums, exp in [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([0], 0), ([1, 1, 1, 1], 3)]:
    assert min_jumps_greedy(nums) == min_jumps_bfs(nums) == min_jumps_dp(nums) == exp
    print(nums, '->', min_jumps_greedy(nums))

# exhaustive: every list of length 1..6 over 0..4 whose last index is reachable
cnt = 0
for n in range(1, 7):
    for t in itertools.product(range(5), repeat=n):
        nums = list(t)
        if not reachable(nums):
            continue
        assert min_jumps_greedy(nums) == min_jumps_bfs(nums) == min_jumps_dp(nums), nums
        cnt += 1
print('exhaustive ok:', cnt, 'reachable lists')

# seeded random, longer lists (force reachability by lifting zeros to 1)
for _ in range(500):
    nums = [random.randint(1, 6) if random.random() < 0.7 else 1 for _ in range(random.randint(1, 40))]
    assert min_jumps_greedy(nums) == min_jumps_bfs(nums)
print('random ok: 500 lists')

# why the scan stops before the last index: with range(len(nums)) a final level end would add a phantom jump
def min_jumps_no_stop(nums):                 # WRONG on purpose
    jumps = end = far = 0
    for i in range(len(nums)):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
print('no-stop variant on [2, 3, 1, 1, 4]:', min_jumps_no_stop([2, 3, 1, 1, 4]), '(wrong, answer is 2)')
print('no-stop variant on [0]:', min_jumps_no_stop([0]), '(wrong, answer is 0)')
assert min_jumps_no_stop([0]) == 1 and min_jumps_greedy([0]) == 0
assert min_jumps_no_stop([2, 3, 1, 1, 4]) == 3

# edge cases and a big input (iterative, no recursion)
assert min_jumps_greedy([7]) == 0
assert min_jumps_greedy([1] * 10000) == 9999
assert min_jumps_greedy([10000] + [1] * 9999) == 1
assert min_jumps_greedy([5, 4, 3, 2, 1, 1, 1]) == 2
print('edge cases ok')
```

**Output (my run):**
```
[2, 3, 1, 1, 4] -> 2
[2, 3, 0, 1, 4] -> 2
[0] -> 0
[1, 1, 1, 1] -> 3
exhaustive ok: 13635 reachable lists
random ok: 500 lists
no-stop variant on [2, 3, 1, 1, 4]: 3 (wrong, answer is 2)
no-stop variant on [0]: 1 (wrong, answer is 0)
edge cases ok
```

**Edge cases:**
- `[x]`: length 1 gives 0 jumps, because the loop body never runs.
- `[10000] + [1] * 9999`: one jump.
- `[1] * 10000`: 9999 jumps. Iterative, no recursion limit problem.
- Zeros in the middle are fine as long as an earlier jump clears them (`[2, 3, 0, 1, 4]` is 2).

**Follow-ups:**
- What if the end may be unreachable? Run the Q12 reachability check first, or return -1 when `far <= i` at `level_end`.
- Why not DP? Same answer, O(n^2). Say the greedy is BFS in disguise and the DP is the same BFS with a table.
- Why is "jump to the cell with the biggest `i + nums[i]`" also correct? It is the same greedy seen from the other side, but harder to prove.

**Common mistakes:**
- Looping to `len(nums)` and counting a phantom jump.
- Counting a jump every time `far` improves (that counts too many).
- Returning `jumps + 1` or starting `jumps` at 1 without handling length 1.
- Forgetting `max`: `far = i + nums[i]` loses a better earlier reach.

### Q14 ⭐⭐⭐ 🟡 Gas station on a circle. There are n stations in a circle (1 <= n <= 10^5); `gas[i]` is the fuel at station i and `cost[i]` the fuel needed to drive from i to i+1 (mod n); the tank is empty at the start and unlimited. Return the smallest starting index from which you can complete one full lap clockwise (arriving at a station with exactly 0 fuel is fine), or -1 if no start works. Give the O(n) one-pass greedy (if total gas < total cost return -1; otherwise reset the candidate to i + 1 whenever the running tank goes negative) and prove it with the two facts: a failure at j from start s means every station between s and j also fails, and total gas >= total cost implies a start exists. Note that some formulations promise a unique answer; for general input it is not unique (for example gas = [1, 1], cost = [1, 1] works from both stations), which is why this prompt asks for the smallest index. Example: gas=[1, 2, 3, 4, 5], cost=[3, 4, 5, 1, 2] -> 3; gas=[2, 3, 4], cost=[3, 4, 3] -> -1; gas=[1, 1], cost=[1, 1] -> 0; gas=[5], cost=[4] -> 0.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** One-pass greedy with a reset: the running tank decides when a start candidate is dead.

**Say this first (1 line):** "If total gas is less than total cost, answer -1. Otherwise I walk once keeping a tank; whenever the tank goes negative, the start was wrong, and everything up to here is wrong too, so the new candidate is the next station."

**Brute force:**
- Try every start, simulate the lap, stop at the first start that never goes negative.
- O(n^2): a lap costs n and there are n starts. With n up to 10^5 that is 10^10, too slow.

**Optimal:**
- `if sum(gas) < sum(cost): return -1`.
- `tank = 0; start = 0`. For `i` in `0..n-1`: `tank += gas[i] - cost[i]`. If `tank < 0`: `start = i + 1`, `tank = 0`.
- Return `start`.
- Proof, two facts (both checked by the code on thousands of random circuits):
  1. **Failure fact.** Say the trip from `s` first goes negative at `j`. Then every station `k` between `s` and `j` also fails. Reason: the tank on reaching `k` from `s` was >= 0, so starting fresh at `k` has no more fuel than coming from `s`, and it still goes negative at `j`. So after a reset we can skip all of `s..j` at once, not just `s`.
  2. **Existence fact.** If total gas >= total cost, some start works. Reason: take the final candidate `start`. The pass proved the stretch `start..n-1` never goes negative. The sum of all legs is >= 0, and the stretches before `start` summed to a negative amount (each reset segment ended negative), so the stretch `start..n-1` has a surplus that covers the whole wrap-around part `0..start-1`.
- Smallest index: the greedy result is the smallest valid start. By the failure fact every station before the final `start` fails, so nothing smaller works. The brute force (first valid start in order) agrees on all 69,904 exhaustive inputs below.
- Not unique in general: `gas = [1, 1]`, `cost = [1, 1]` works from 0 and 1. Of the 69,904 small inputs, 30,940 have two or more valid starts, which is why this prompt asks for the smallest. The prompt that promises a unique answer is a different, narrower problem.

**Complexity:** Time O(n), one pass plus the two sums. Space O(1).

**Dry run:** `gas=[1,2,3,4,5]`, `cost=[3,4,5,1,2]`. Total gas 15, total cost 15, so go on.
| i | gas-cost | tank | action |
|---|---|---|---|
| 0 | -2 | -2 | negative, start = 1, tank = 0 |
| 1 | -2 | -2 | negative, start = 2, tank = 0 |
| 2 | -2 | -2 | negative, start = 3, tank = 0 |
| 3 | +3 | 3 | ok |
| 4 | +3 | 6 | ok |

Return 3. Check by hand: from 3 the tank goes 4-1=3, 3+5-2=6, 6+1-3=4, 4+2-4=2, 2+3-5=0. Never negative, ends at exactly 0, which is allowed.

**Code:**
```python
import random
import itertools

random.seed(14)

def gas_greedy(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                         # cannot get from start to i + 1
            start = i + 1                    # so no station in start..i works
            tank = 0
    return start

def completes(gas, cost, s):
    t = 0
    n = len(gas)
    for k in range(n):
        i = (s + k) % n
        t += gas[i] - cost[i]
        if t < 0:
            return False
    return True

def gas_brute(gas, cost):                    # O(n^2): try every start in order
    for s in range(len(gas)):
        if completes(gas, cost, s):
            return s
    return -1

cases = [
    ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
    ([2, 3, 4], [3, 4, 3], -1),
    ([1, 1], [1, 1], 0),
    ([5], [4], 0),
]
for gas, cost, exp in cases:
    assert gas_greedy(gas, cost) == gas_brute(gas, cost) == exp
    print('gas =', gas, 'cost =', cost, '->', gas_greedy(gas, cost))

# exhaustive: every gas and cost list with n 1..4 and values 0..3
total = multi = 0
for n in range(1, 5):
    for gas in itertools.product(range(4), repeat=n):
        for cost in itertools.product(range(4), repeat=n):
            g = gas_greedy(gas, cost)
            assert g == gas_brute(gas, cost), (gas, cost)
            total += 1
            if sum(completes(gas, cost, s) for s in range(n)) > 1:
                multi += 1
print('exhaustive ok:', total, 'inputs; with 2 or more valid starts:', multi)

for _ in range(2000):
    n = random.randint(1, 12)
    gas = [random.randint(0, 6) for _ in range(n)]
    cost = [random.randint(0, 6) for _ in range(n)]
    assert gas_greedy(gas, cost) == gas_brute(gas, cost)
print('random ok: 2000 inputs')

# fact 1: if a trip from s first fails at j, every station k in s..j also fails
facts = 0
for _ in range(3000):
    n = random.randint(2, 8)
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    for s in range(n):
        t = 0
        for k in range(n):
            i = (s + k) % n
            t += gas[i] - cost[i]
            if t < 0:
                # failure at offset k: stations s, s+1, ..., s+k (mod n) all fail
                for m in range(k + 1):
                    assert not completes(gas, cost, (s + m) % n)
                facts += 1
                break
print('fact 1 checked on', facts, 'failing starts')

# fact 2: sum(gas) >= sum(cost) implies some start exists
for _ in range(3000):
    n = random.randint(1, 8)
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    if sum(gas) >= sum(cost):
        assert gas_brute(gas, cost) != -1
    else:
        assert gas_brute(gas, cost) == -1
print('fact 2 ok: total gas >= total cost iff a start exists')

# edge cases
assert gas_greedy([0], [0]) == 0
assert gas_greedy([0, 0, 5], [0, 0, 5]) == 0     # zero-cost legs
assert gas_greedy([3, 1, 1], [1, 2, 2]) == 0
assert gas_greedy([1, 1, 1, 10], [2, 2, 2, 2]) == 3
big_n = 10 ** 5
assert gas_greedy([1] * big_n, [1] * big_n) == 0
assert gas_greedy([0] * (big_n - 1) + [big_n], [1] * big_n) == big_n - 1
print('edge cases ok')
```

**Output (my run):**
```
gas = [1, 2, 3, 4, 5] cost = [3, 4, 5, 1, 2] -> 3
gas = [2, 3, 4] cost = [3, 4, 3] -> -1
gas = [1, 1] cost = [1, 1] -> 0
gas = [5] cost = [4] -> 0
exhaustive ok: 69904 inputs; with 2 or more valid starts: 30940
random ok: 2000 inputs
fact 1 checked on 10367 failing starts
fact 2 ok: total gas >= total cost iff a start exists
edge cases ok
```

**Edge cases:**
- One station: `gas=[5], cost=[4]` is 0; `gas=[3], cost=[4]` is -1 (total check).
- Zero-cost legs and zero gas: `[0], [0]` is 0.
- Arriving with exactly 0 fuel is allowed: the test is `tank < 0`, not `tank <= 0`.
- All equal (`[1]*n`, `[1]*n`): returns 0, the smallest of n valid starts.
- n = 10^5: iterative, one pass, fine.

**Follow-ups:**
- Why is the total check needed? Without it the loop returns a candidate that fails on the wrap-around part.
- Unique-answer wording? If the statement guarantees uniqueness, the same code returns it; do not rely on the guarantee for general input.
- Return all valid starts? Then use prefix sums on the doubled array with a sliding-window minimum (a monotonic deque, as in Part 2 Q16); the one-pass trick only finds one.

**Common mistakes:**
- Resetting `start = i` instead of `i + 1`.
- Forgetting the total check and returning `start` for an impossible circuit.
- Using `tank <= 0` to reset (rejects exact-zero arrivals).
- Resetting only the one failing start and re-simulating (quadratic again).

### Q15 ⭐⭐⭐ 🟡 Reorganize string. Given a string `s` of lowercase letters (1 <= len <= 500), rearrange its characters so that no two adjacent characters are equal, and return the result, or the empty string if that is impossible. Several answers can be valid, and the checker accepts any rearrangement that is a permutation of `s` with no equal neighbours (and requires '' exactly when none exists); the examples show one accepted answer. Give the max-heap solution (pop the most frequent letter, hold it back one step) and the closed condition for feasibility, max_count <= (len + 1) // 2, with a short proof of necessity (an arrangement of length L has at most ceil(L / 2) slots for any one letter). Example: s='aab' -> 'aba'; s='aaab' -> ''; s='vvvlo' -> 'vlvov'; s='a' -> 'a'; s='aabbcc' -> 'abcabc'.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Max-heap of counts with a one-step hold-back (always place the most frequent letter that is not the one just placed).

**Say this first (1 line):** "First the quick test: if the most frequent letter appears more than (len + 1) // 2 times, it is impossible. Otherwise I use a max-heap of (count, letter), pop the biggest, place it, hold it back for one step, and push it back after the next placement."

**Brute force:**
- Try all distinct permutations and keep one with no equal neighbours. That is up to n! permutations. I use it for strings of length up to 7 as the oracle (also to prove the feasibility test is exact).

**Optimal:**
- Count letters. If `max_count > (len + 1) // 2` return `''`.
- Heap of `(-count, letter)`. Loop: pop the top, append its letter, decrement its count. If a letter was held from the last step, push it back now. If the popped letter still has copies, hold it (do not push yet).
- The hold-back is what guarantees no equal neighbours: the letter just used is not in the heap on the next pop.
- Necessity: a letter with count c in a string of length L needs c positions with no two adjacent. At most ceil(L/2) = (L+1)//2 positions can be pairwise non-adjacent, so c <= (L+1)//2.
- Sufficiency (sketch): taking the most frequent letter keeps the invariant "max remaining count <= ceil(remaining / 2)". The code checks the claim exhaustively on every string of length <= 7 over 'abc' (the heap alone never fails when the condition holds).
- Several answers are valid. I wrote my own checker: any permutation of `s` with no equal neighbours, and `''` exactly when brute force says none exists. The heap happens to return the same strings the prompt shows.
- **heapq tie-breaking:** the heap holds tuples `(-count, letter)`. Equal counts fall through to the letter, so ties are broken alphabetically and never raise. If the payload were something unorderable (a dict), two equal counts would raise `TypeError`; the code shows it.

**Complexity:** Time O(n log k), k = distinct letters (at most 26), so O(n) in practice. Space O(k).

**Dry run:** `s = 'aab'`. Counts a:2, b:1. Test: 2 <= (3+1)//2 = 2, fine. Heap `[(-2,'a'), (-1,'b')]`.
- Pop `(-2,'a')`: out `a`; count becomes -1, held `(-1,'a')`.
- Pop `(-1,'b')`: out `ab`; count 0, nothing held; push back held `(-1,'a')`.
- Pop `(-1,'a')`: out `aba`; count 0.
Result `aba`.

**Code:**
```python
import heapq
import itertools
import random
from collections import Counter

random.seed(15)

def reorganize(s):
    cnt = Counter(s)
    if max(cnt.values()) > (len(s) + 1) // 2:         # closed feasibility test
        return ''
    heap = [(-c, ch) for ch, c in cnt.items()]         # (negated count, letter): ties on count compare letters
    heapq.heapify(heap)
    out = []
    held = None                                        # last letter used, held back one step
    while heap or held:
        if not heap:                                   # cannot happen when feasible
            return ''
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        neg += 1                                       # one copy used (counts are negative)
        if held:
            heapq.heappush(heap, held)                 # the letter held last step may be used again
            held = None
        if neg:
            held = (neg, ch)
    return ''.join(out)

def reorganize_heap_only(s):                           # same heap logic, without the closed test
    cnt = Counter(s)
    heap = [(-c, ch) for ch, c in cnt.items()]
    heapq.heapify(heap)
    out, held = [], None
    while heap:
        neg, ch = heapq.heappop(heap)
        out.append(ch)
        neg += 1
        if held:
            heapq.heappush(heap, held)
            held = None
        if neg:
            held = (neg, ch)
    return ''.join(out) if len(out) == len(s) else ''

def valid(s, got):
    """Own checker: any permutation of s with no equal neighbours; '' exactly when none exists."""
    if got == '':
        return not exists_arrangement(s)
    return sorted(got) == sorted(s) and all(a != b for a, b in zip(got, got[1:]))

def exists_arrangement(s):                             # brute force over distinct permutations (small s)
    return any(all(a != b for a, b in zip(p, p[1:])) for p in set(itertools.permutations(s)))

for s, accepted in [('aab', 'aba'), ('aaab', ''), ('vvvlo', None), ('a', 'a'), ('aabbcc', None)]:
    got = reorganize(s)
    assert valid(s, got), (s, got)
    if accepted is not None and accepted in ('', 'aba', 'a'):
        assert got == accepted
    print(repr(s), '->', repr(got))

# exhaustive: all strings over 'abc' of length 1..7 (3+9+...+2187 = 3279 strings), brute-force feasibility
checked = infeasible = 0
for n in range(1, 8):
    for t in itertools.product('abc', repeat=n):
        s = ''.join(t)
        got = reorganize(s)
        feasible = max(Counter(s).values()) <= (n + 1) // 2
        assert feasible == exists_arrangement(s), s     # the closed condition is exact
        assert (got != '') == feasible and valid(s, got), (s, got)
        assert reorganize_heap_only(s) == got           # the heap alone already finds it whenever feasible
        checked += 1
        infeasible += not feasible
print('exhaustive ok:', checked, 'strings; infeasible:', infeasible)

for _ in range(300):
    s = ''.join(random.choice('abcdefg') for _ in range(random.randint(1, 200)))
    got = reorganize(s)
    assert valid(s, got) if got else max(Counter(s).values()) > (len(s) + 1) // 2
print('random ok: 300 strings up to length 200')

# heapq tie-breaking: tuples compare element by element
h = [(-2, 'b'), (-2, 'a'), (-1, 'z')]
heapq.heapify(h)
print('ties on count break by letter:', heapq.heappop(h))       # (-2, 'a')
# a tuple whose second item cannot be ordered raises TypeError as soon as the counts tie
try:
    bad = []
    heapq.heappush(bad, (-2, {'x': 1}))
    heapq.heappush(bad, (-2, {'y': 2}))
    print('no error (unexpected)')
except TypeError as e:
    print('TypeError on tied count with dict payload:', e)
heapq.heappush(bad, (-3, {'z': 3}))                              # different counts never reach the payload
print('heap of 3 after a distinct count:', len(bad))

# edge cases
assert reorganize('a') == 'a'
assert reorganize('aa') == ''
assert reorganize('ab') in ('ab', 'ba')
assert reorganize('aaabb') == 'ababa'
assert reorganize('a' * 250 + 'b' * 250) != '' and valid('a' * 250 + 'b' * 250, reorganize('a' * 250 + 'b' * 250))
assert reorganize('a' * 251 + 'b' * 249) == ''
print('edge cases ok')
```

**Output (my run):**
```
'aab' -> 'aba'
'aaab' -> ''
'vvvlo' -> 'vlvov'
'a' -> 'a'
'aabbcc' -> 'abcabc'
exhaustive ok: 3279 strings; infeasible: 582
random ok: 300 strings up to length 200
ties on count break by letter: (-2, 'a')
TypeError on tied count with dict payload: '<' not supported between instances of 'dict' and 'dict'
heap of 3 after a distinct count: 3
edge cases ok
```

**Edge cases:**
- `'a'` gives `'a'`. `'aa'` gives `''`.
- Exactly at the limit: 250 a + 250 b is feasible; 251 a + 249 b is not (251 > 250).
- Odd length with one dominant letter: `'aaabb'` -> `'ababa'`, the only arrangement.
- All distinct letters: any order works.

**Follow-ups:**
- Same letters must be at least k apart? Hold each used letter for k steps with a queue (the cooldown pattern from Q11 in this part, and k-distance rearrange).
- O(n) without a heap? Sort letters by frequency and fill even indices first, then odd indices.
- Return the lexicographically smallest valid answer? The plain heap is not enough; you need a feasibility check at each step.

**Common mistakes:**
- Pushing the popped letter straight back (equal neighbours).
- Skipping the feasibility test and returning a short string.
- Using the count alone as the heap item with letters in a dict (ties then compare dicts: TypeError).
- Forgetting heapq is a min-heap: store negative counts.

### Q16 ⭐⭐⭐ 🟡 Non-overlapping intervals (fewest removals). Intervals are half-open [start, end) with start < end, so [1, 2) and [2, 3) do not overlap. Given `intervals` (1 <= len <= 10^5, values in [-5*10^4, 5*10^4]), return the minimum number of intervals to remove so that the rest are pairwise non-overlapping. Sort by END time and keep an interval whenever its start is >= the last kept end (the earliest-finish greedy); give the exchange argument in two lines, show a counter-example for sorting by start time, and say why the answer equals len minus the activity-selection maximum. Example: intervals=[[1, 2], [2, 3], [3, 4], [1, 3]] -> 1; intervals=[[1, 2], [1, 2], [1, 2]] -> 2; intervals=[[1, 2], [2, 3]] -> 0; intervals=[[1, 100], [11, 22], [1, 11], [2, 12]] -> 2.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval scheduling (activity selection): sort by end time, keep whatever fits. Greedy with an exchange argument.

**Say this first (1 line):** "Removals equal n minus the biggest set of non-overlapping intervals. I sort by END and keep an interval whenever its start is at least the last kept end; the one that finishes earliest leaves the most room."

**Brute force:**
- Try every subset, keep those with no overlapping pair, take the biggest. O(2^n * n^2). Fine as an oracle for n <= 10, useless beyond.

**Optimal:**
- Sort by end. `last_end = None`. For each `(s, e)`: if `last_end is None or s >= last_end`, keep it and set `last_end = e`. Otherwise count a removal.
- `s >= last_end` (not `>`) because intervals are half-open: `[1, 2)` and `[2, 3)` do not overlap.
- **Exchange argument (two lines):** take any optimal solution and swap its first interval for the one with the earliest end. It ends no later, so everything else in the solution still fits. So an optimal solution exists that starts with the earliest-ending interval; repeat on the rest.
- **Why the answer is n minus the activity-selection maximum:** a set can be kept without conflicts exactly when it is pairwise non-overlapping. Removing the fewest means keeping the most, so removals = n - max kept.
- **Counter-example for sorting by start:** `[[1, 10], [2, 3], [4, 5]]`. By start you keep `[1, 10]` first and must remove the other two (2 removals). The right answer is 1: drop `[1, 10]`, keep the two small ones. The code finds 8 such failing triples among small inputs (and the end-sorted greedy matches brute force on all of them).
- Ties in the end value do not matter (checked: reversing input order never changes the count).

**Complexity:** Time O(n log n) for the sort, O(n) for the scan. Space O(n) for the sorted copy (O(1) extra if sorted in place).

**Dry run:** `[[1, 100], [11, 22], [1, 11], [2, 12]]`. Sorted by end: `[1,11] [2,12] [11,22] [1,100]`.
- `[1,11]`: first, keep, `last_end = 11`.
- `[2,12]`: 2 < 11, remove (1).
- `[11,22]`: 11 >= 11, keep, `last_end = 22`.
- `[1,100]`: 1 < 22, remove (2).
Answer 2.

**Code:**
```python
import itertools
import random

random.seed(16)

def erase_overlap(intervals):                          # sort by END, keep when start >= last kept end
    kept = 0
    last_end = None
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if last_end is None or s >= last_end:          # half-open: touching is fine
            kept += 1
            last_end = e
    return len(intervals) - kept

def max_non_overlapping(intervals):                    # activity selection size
    return len(intervals) - erase_overlap(intervals)

def overlap(a, b):                                     # half-open [s, e)
    return a[0] < b[1] and b[0] < a[1]

def brute(intervals):                                  # try every subset (n <= 10)
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        sel = [intervals[i] for i in range(n) if mask >> i & 1]
        if all(not overlap(a, b) for a, b in itertools.combinations(sel, 2)):
            best = max(best, len(sel))
    return n - best

def by_start(intervals):                               # WRONG greedy: sort by start
    kept = 0
    last_end = None
    for s, e in sorted(intervals):
        if last_end is None or s >= last_end:
            kept += 1
            last_end = e
    return len(intervals) - kept

for iv, exp in [([[1, 2], [2, 3], [3, 4], [1, 3]], 1), ([[1, 2], [1, 2], [1, 2]], 2),
                ([[1, 2], [2, 3]], 0), ([[1, 100], [11, 22], [1, 11], [2, 12]], 2)]:
    assert erase_overlap(iv) == brute(iv) == exp
    print(iv, '->', erase_overlap(iv))

# exhaustive: all multisets of up to 4 intervals with endpoints in 0..4 (10 possible intervals)
pool = [[a, b] for a in range(5) for b in range(a + 1, 5)]
cnt = 0
for k in range(1, 5):
    for combo in itertools.combinations_with_replacement(pool, k):
        iv = [list(x) for x in combo]
        assert erase_overlap(iv) == brute(iv), iv
        assert erase_overlap(iv[::-1]) == erase_overlap(iv)          # input order does not matter
        cnt += 1
print('exhaustive ok:', cnt, 'multisets')

for _ in range(500):
    n = random.randint(1, 10)
    iv = []
    for _ in range(n):
        a = random.randint(-8, 8)
        iv.append([a, random.randint(a + 1, a + 6)])
    assert erase_overlap(iv) == brute(iv)
    assert max_non_overlapping(iv) == len(iv) - brute(iv)
print('random ok: 500 inputs')

# counter-example for sort-by-start
cx = [[1, 10], [2, 3], [4, 5]]
print('sort by start on', cx, '->', by_start(cx), '(wrong); by end ->', erase_overlap(cx), '; brute ->', brute(cx))
assert by_start(cx) == 2 and erase_overlap(cx) == 1 == brute(cx)
bad = 0
for combo in itertools.combinations_with_replacement(pool, 3):
    iv = [list(x) for x in combo]
    bad += by_start(iv) != erase_overlap(iv)
print('3-interval multisets where sort-by-start is wrong:', bad)
assert bad > 0

# edge cases and a large input
assert erase_overlap([[0, 1]]) == 0
assert erase_overlap([[-50000, 50000], [-50000, -49999]]) == 1
assert erase_overlap([[1, 2], [2, 3], [3, 4]]) == 0               # touching endpoints do not overlap
assert erase_overlap([[1, 3], [1, 3]]) == 1
big = [[i, i + 2] for i in range(-50000, 49998)]                  # chain of overlaps, n about 10^5
assert erase_overlap(big) == len(big) - ((len(big) + 1) // 2)
print('edge cases ok; big n =', len(big))
```

**Output (my run):**
```
[[1, 2], [2, 3], [3, 4], [1, 3]] -> 1
[[1, 2], [1, 2], [1, 2]] -> 2
[[1, 2], [2, 3]] -> 0
[[1, 100], [11, 22], [1, 11], [2, 12]] -> 2
exhaustive ok: 1000 multisets
random ok: 500 inputs
sort by start on [[1, 10], [2, 3], [4, 5]] -> 2 (wrong); by end -> 1 ; brute -> 1
3-interval multisets where sort-by-start is wrong: 8
edge cases ok; big n = 99998
```

**Edge cases:**
- One interval: 0 removals.
- Identical intervals: `[[1,2]] * 3` keeps one, removes 2.
- Touching intervals `[1,2),[2,3)`: 0 removals. If the statement made them closed, the test becomes `s > last_end`; always ask.
- Values at the extremes (-50000, 50000): no overflow in Python; a language with fixed ints needs care only if you subtract.
- A chain of ~10^5 overlapping intervals: the answer is len minus ceil(len / 2), checked in the code.

**Follow-ups:**
- Minimum rooms needed instead? That is meeting rooms II (heap of end times or a sweep).
- Weighted intervals (maximise total value)? Greedy fails; sort by end and use DP with binary search (Parts 10-11).
- Minimum arrows to burst balloons? Q21 in this part: same sort by end, closed intervals.

**Common mistakes:**
- Sorting by start (the counter-example above) or by length.
- `s > last_end` for half-open intervals (counts touching as overlapping).
- Counting kept intervals and forgetting to subtract from n.
- Mutating the caller's list with `intervals.sort()` when the caller still needs the order.

### Q17 ⭐⭐⭐ 🔴 Median of a data stream. Maintain a running median: process `adds` (1 <= len <= 10^5, integers in [-10^6, 10^6]) one value at a time and return the list of medians after each insertion as floats (the middle value when the count is odd, the mean of the two middle values when it is even, so [1, 2] gives 1.5). Use two heaps, a max-heap `lo` (negated values) for the smaller half and a min-heap `hi` for the larger half, keep the invariant len(lo) == len(hi) or len(lo) == len(hi) + 1, and describe the push-then-rebalance step that keeps every element of lo <= every element of hi. State the cost (O(log n) per add, O(1) per median query) and compare with keeping a sorted list and using bisect.insort (O(n) per insert because of the memmove, but fast for small n). Example: adds=[1, 2, 3] -> [1.0, 1.5, 2.0]; adds=[5, 15, 1, 3] -> [5.0, 10.0, 5.0, 4.0]; adds=[-1, -2, -3, -4, -5] -> [-1.0, -1.5, -2.0, -2.5, -3.0]; adds=[2, 2, 2, 2] -> [2.0, 2.0, 2.0, 2.0]; adds=[7] -> [7.0].
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two heaps split the data at the median: a max-heap for the lower half, a min-heap for the upper half.

**Say this first (1 line):** "I keep the smaller half in a max-heap `lo` (negated, since heapq is a min-heap) and the larger half in a min-heap `hi`, sized so `lo` has the same count as `hi` or one more. The median is the top of `lo` or the mean of the two tops."

**Brute force:**
- Re-sort the whole prefix after every add and read the middle: O(n^2 log n) over the stream. Used as the oracle.
- Better baseline: keep one sorted list and `bisect.insort`. Finding the spot is O(log n), but the insert shifts elements (a memmove), so each add is O(n). The memmove is fast in C, so this is fine for small n and often wins in practice up to a few tens of thousands, but it is O(n^2) overall.

**Optimal:**
- Invariants: (1) `len(lo) == len(hi)` or `len(lo) == len(hi) + 1`; (2) every element of `lo` <= every element of `hi`.
- **Push-then-rebalance step** for each `x`:
  1. push `-x` onto `lo`;
  2. pop the max of `lo` and push it onto `hi` (this guarantees invariant 2, whichever half `x` belonged to);
  3. if `hi` now has more than `lo`, move `hi`'s min back to `lo` (restores invariant 1).
- Median: odd count, `-lo[0]` as a float; even count, `(-lo[0] + hi[0]) / 2`, which Python makes a float (so `[1, 2]` gives 1.5).
- Why correct: after step 2 the smaller half plus the new element is split by the max, so no element of `hi` is smaller than any in `lo`. Step 3 only moves one boundary element across, which keeps the order between halves.
- Ties and heapq: the heaps hold plain ints, so equal values never raise. The negation trick on ints is exact (no precision issue).

**Complexity:** Each add is a constant number of heap operations: O(log n). Median query O(1). Total O(n log n) for n adds. Space O(n).

**Dry run:** `[5, 15, 1, 3]`.
| x | lo (real values) | hi | median |
|---|---|---|---|
| 5 | {5} | {} | 5.0 |
| 15 | {5} | {15} | (5 + 15) / 2 = 10.0 |
| 1 | {5, 1} | {15} | 5.0 |
| 3 | {3, 1} | {5, 15} | (3 + 5) / 2 = 4.0 |

For x = 3: push into `lo` giving {5, 3, 1}, move the max 5 to `hi` giving {5, 15}, sizes 2 and 2, so no rebalance.

**Code:**
```python
import bisect
import heapq
import random

random.seed(17)

def running_median(adds):
    lo = []                                  # max-heap of the smaller half, stored negated
    hi = []                                  # min-heap of the larger half
    out = []
    for x in adds:
        heapq.heappush(lo, -x)               # 1. push into lo
        heapq.heappush(hi, -heapq.heappop(lo))   # 2. move lo's max to hi so every lo <= every hi
        if len(hi) > len(lo):                # 3. rebalance: lo may have at most one extra
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append(float(-lo[0]))        # odd count: the top of lo
        else:
            out.append((-lo[0] + hi[0]) / 2) # even count: mean of the two tops
    return out

def median_insort(adds):                     # sorted list + bisect.insort: O(n) per insert (memmove)
    a = []
    out = []
    for x in adds:
        bisect.insort(a, x)
        m = len(a)
        out.append(float(a[m // 2]) if m % 2 else (a[m // 2 - 1] + a[m // 2]) / 2)
    return out

def median_brute(adds):                      # re-sort the whole prefix each time, O(n^2 log n)
    out = []
    for i in range(1, len(adds) + 1):
        s = sorted(adds[:i])
        m = len(s)
        out.append(float(s[m // 2]) if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2)
    return out

for adds, exp in [([1, 2, 3], [1.0, 1.5, 2.0]), ([5, 15, 1, 3], [5.0, 10.0, 5.0, 4.0]),
                  ([-1, -2, -3, -4, -5], [-1.0, -1.5, -2.0, -2.5, -3.0]),
                  ([2, 2, 2, 2], [2.0, 2.0, 2.0, 2.0]), ([7], [7.0])]:
    assert running_median(adds) == median_insort(adds) == median_brute(adds) == exp
    print(adds, '->', running_median(adds))

for _ in range(1000):
    adds = [random.randint(-9, 9) for _ in range(random.randint(1, 25))]
    assert running_median(adds) == median_brute(adds), adds
print('random ok: 1000 small streams (many duplicates)')

for _ in range(20):
    adds = [random.randint(-10 ** 6, 10 ** 6) for _ in range(random.randint(100, 400))]
    assert running_median(adds) == median_insort(adds) == median_brute(adds)
print('random ok: 20 streams of 100-400 values in [-10^6, 10^6]')

# invariant check after every step: len(lo) == len(hi) or len(lo) == len(hi) + 1, and max(lo) <= min(hi)
lo, hi = [], []
for x in [random.randint(-50, 50) for _ in range(2000)]:
    heapq.heappush(lo, -x)
    heapq.heappush(hi, -heapq.heappop(lo))
    if len(hi) > len(lo):
        heapq.heappush(lo, -heapq.heappop(hi))
    assert len(lo) in (len(hi), len(hi) + 1)
    assert not hi or -lo[0] <= hi[0]
print('invariant holds for 2000 steps')

# edge cases: sorted, reverse sorted, all equal, extremes, mean of two extremes
assert running_median([1, 2]) == [1.0, 1.5]
assert running_median([-10 ** 6, 10 ** 6]) == [-1000000.0, 0.0]
assert running_median([10 ** 6, 10 ** 6 - 1]) == [1000000.0, 999999.5]
n = 20000
up = list(range(n))
assert running_median(up) == median_insort(up)
assert running_median(up[::-1]) == median_insort(up[::-1])
assert running_median([3] * n) == [3.0] * n
big = [random.randint(-10 ** 6, 10 ** 6) for _ in range(10 ** 5)]       # max size, iterative
res = running_median(big)
assert len(res) == 10 ** 5 and res[-1] == median_insort(big)[-1]
print('edge cases ok; n = 10^5 done')
```

**Output (my run):**
```
[1, 2, 3] -> [1.0, 1.5, 2.0]
[5, 15, 1, 3] -> [5.0, 10.0, 5.0, 4.0]
[-1, -2, -3, -4, -5] -> [-1.0, -1.5, -2.0, -2.5, -3.0]
[2, 2, 2, 2] -> [2.0, 2.0, 2.0, 2.0]
[7] -> [7.0]
random ok: 1000 small streams (many duplicates)
random ok: 20 streams of 100-400 values in [-10^6, 10^6]
invariant holds for 2000 steps
edge cases ok; n = 10^5 done
```

**Edge cases:**
- One value: median is that value as a float. Two values: their mean (`[1, 2]` -> 1.5).
- Duplicates (`[2, 2, 2, 2]`): fine, comparisons use `<=` across halves.
- Negatives: negation works, and `-lo[0]` restores them.
- Mean of the extremes `-10^6` and `10^6` is 0.0; values up to 10^6 mean the float mean of two ints is exact.
- Sorted or reverse-sorted input of 20,000 values, and 10^5 random values: the heaps stay balanced; the code is iterative.

**Follow-ups:**
- Sliding-window median? Two heaps plus lazy deletion (or a sorted container); each removal is marked and cleaned when it surfaces at a top.
- Median of values in a small known range? A counting array and a pointer, O(1) per query.
- Percentile other than 50? Same idea with unequal target sizes.
- Memory too large for all values? Use a quantile sketch; two heaps need all n values.

**Common mistakes:**
- Forgetting to negate when popping from `lo` (returns the min of the lower half).
- Pushing to the "right" heap by comparing with the current median; the push-pop-rebalance version avoids that case analysis.
- Integer division for the even case (returns 1 for `[1, 2]`).
- Breaking invariant 1 by rebalancing in the wrong direction (the extra element must sit in `lo`).

### Q18 ⭐⭐ 🟢 Last stone weight. `stones` holds positive integers (1 <= len <= 30, each <= 1000). Repeatedly take the two heaviest stones; if they are equal both are destroyed, otherwise the lighter is destroyed and the heavier becomes the difference. Return the weight of the last stone, or 0 if none is left. Show the max-heap via negation (heapq has no max-heap), say what happens with a single stone, and state the cost (O(n log n)). Example: stones=[2, 7, 4, 1, 8, 1] -> 1; stones=[1] -> 1; stones=[3, 3] -> 0; stones=[10, 4, 2, 10] -> 2.
**Asked at:** Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Repeatedly take the largest items: a max-heap, which in Python means a min-heap of negated values.

**Say this first (1 line):** "heapq only has a min-heap, so I store negatives. Pop twice, push back the difference if it is not zero, and stop when one or zero stones remain."

**Brute force:**
- Sort, pop the two largest, put the difference back, sort again. Each re-sort is O(n log n), so O(n^2 log n) in total. Fine for n <= 30 and used here as the oracle.

**Optimal:**
- `heap = [-s for s in stones]`; `heapify` (O(n)).
- While two or more stones remain: `a = -heappop`, `b = -heappop` (so `a >= b`). If `a != b`, push `-(a - b)`.
- Return `-heap[0]` if anything is left, else 0.
- Single stone: the loop never runs, the answer is that stone.
- Each round removes at least one stone (two out, at most one in), so there are at most n - 1 rounds.
- Ties: equal weights are plain ints, so comparisons never fail. If stones carried labels, a `(-weight, label)` tuple breaks ties by label (the code shows it); an unorderable label would raise `TypeError` on a tie.

**Complexity:** Time O(n log n): heapify O(n), at most n - 1 rounds each with two pops and one push at O(log n). Space O(n) for the heap.

**Dry run:** `[2, 7, 4, 1, 8, 1]`.
| round | take | push | stones left |
|---|---|---|---|
| 1 | 8, 7 | 1 | 4, 2, 1, 1, 1 |
| 2 | 4, 2 | 2 | 2, 1, 1, 1 |
| 3 | 2, 1 | 1 | 1, 1, 1 |
| 4 | 1, 1 | nothing | 1 |

Answer 1.

**Code:**
```python
import heapq
import random

random.seed(18)

def last_stone(stones):
    heap = [-s for s in stones]              # heapq is a min-heap: store negatives to get a max-heap
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)             # heaviest
        b = -heapq.heappop(heap)             # second heaviest, a >= b
        if a != b:
            heapq.heappush(heap, -(a - b))   # the remainder goes back
    return -heap[0] if heap else 0

def last_stone_sorted(stones):               # oracle: re-sort after each smash, O(n^2 log n)
    a = sorted(stones)
    while len(a) > 1:
        x = a.pop()
        y = a.pop()
        if x != y:
            a.append(x - y)
            a.sort()
    return a[0] if a else 0

for st, exp in [([2, 7, 4, 1, 8, 1], 1), ([1], 1), ([3, 3], 0), ([10, 4, 2, 10], 2)]:
    assert last_stone(st) == last_stone_sorted(st) == exp
    print(st, '->', last_stone(st))

for _ in range(2000):
    st = [random.randint(1, 20) for _ in range(random.randint(1, 12))]
    assert last_stone(st) == last_stone_sorted(st), st
print('random ok: 2000 inputs')

# negation trap: popping the heap without negating gives the LIGHTEST stones
h = [2, 7, 4, 1, 8, 1]
heapq.heapify(h)
print('raw min-heap pops first:', heapq.heappop(h), heapq.heappop(h), '(the two lightest, not heaviest)')

# a different, ordered-tuple view: ties between equal weights never raise, because ints are comparable
tie = [(-5, 'a'), (-5, 'b')]
heapq.heapify(tie)
print('tuple tie on weight breaks by label:', heapq.heappop(tie))

# edge cases
assert last_stone([5]) == 5
assert last_stone([1000] * 30) == 0                # 30 equal stones cancel in pairs
assert last_stone([1000] * 29) == 1000
assert last_stone([1, 1, 1]) == 1
assert last_stone([1000, 1]) == 999
assert last_stone([1, 2, 3]) == 0
print('edge cases ok')
```

**Output (my run):**
```
[2, 7, 4, 1, 8, 1] -> 1
[1] -> 1
[3, 3] -> 0
[10, 4, 2, 10] -> 2
random ok: 2000 inputs
raw min-heap pops first: 1 1 (the two lightest, not heaviest)
tuple tie on weight breaks by label: (-5, 'a')
edge cases ok
```

**Edge cases:**
- One stone: returned unchanged. Two equal stones: 0.
- An even number of equal stones cancels to 0 (30 of them), an odd number leaves one (29 give 1000).
- Remainder pushed back may be the new heaviest: `[1000, 1]` gives 999 straight away, then one stone.
- Empty result: the `else 0` branch.

**Follow-ups:**
- Stones up to 10^9 and n up to 10^5? Same heap, still O(n log n).
- Smallest two instead of largest two? Plain min-heap without negation (that is Q20's rule).
- Why not bucket sort? With weights <= 1000 a counting array works too, but the heap is simpler to explain.

**Common mistakes:**
- Using the raw min-heap and getting the lightest stones (the code prints it).
- Forgetting to negate the pushed difference.
- Pushing `0` when the stones are equal (it would later be treated as a stone).
- Returning `heap[0]` without negating it, or indexing an empty heap.

### Q19 ⭐⭐ 🟢 Assign cookies. `g[i]` is the minimum cookie size child i will accept and `s[j]` is the size of cookie j (0 <= len(g), len(s) <= 3*10^4, sizes in [1, 2^31 - 1]). Each child gets at most one cookie and each cookie goes to at most one child; a child is content when the cookie size is >= g[i]. Return the maximum number of content children. Sort both lists and walk the cookies with a pointer over the children (smallest cookie that satisfies the least greedy unmatched child), and give the exchange argument for why using the smallest sufficient cookie never hurts. Example: g=[1, 2, 3], s=[1, 1] -> 1; g=[1, 2], s=[1, 2, 3] -> 2; g=[], s=[4] -> 0; g=[5, 6], s=[1, 2] -> 0.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy matching after sorting: give each child the smallest cookie that satisfies them.

**Say this first (1 line):** "Sort both lists. Walk the cookies from smallest to largest, and keep a pointer on the least greedy unmatched child; if the cookie is big enough, that child is content and the pointer moves on."

**Brute force:**
- Try, for every child, either no cookie or each unused cookie (bitmask over cookies with memoisation). Exponential in the number of cookies; used as the oracle for lists of up to 7.

**Optimal:**
- Sort `g` and `s`. `i = 0`. For each cookie in ascending order: `if i < len(g) and g[i] <= cookie: i += 1`.
- Return `i`.
- Exchange argument: take an optimal assignment. If the least greedy child is matched with a cookie bigger than the smallest sufficient cookie (or is unmatched while that cookie is used elsewhere), swap; the cookie that was used is at least as big as needed by whoever had it, and the child needs no more than anyone else. So using the smallest sufficient cookie on the least greedy child never reduces the count.
- Cookies that are too small for the current child are useless for every other child too (they are at least as greedy), so skipping them is safe.
- Wasteful rule (biggest cookie to the least greedy child) is wrong: `g=[1,2]`, `s=[1,2]` gives 1 instead of 2. The code counts how many tiny cases differ.

**Complexity:** Time O(g log g + s log s) for the sorts plus O(s) for the walk. Space O(1) extra apart from sorted copies.

**Dry run:** `g=[1,2,3]`, `s=[1,1]`. Sorted already. Cookie 1: `g[0]=1 <= 1`, `i=1`. Cookie 1: `g[1]=2 <= 1`? No, skip. End: `i = 1`. Answer 1.

**Code:**
```python
import itertools
import random
from functools import lru_cache

random.seed(19)

def assign_cookies(g, s):
    g = sorted(g)
    s = sorted(s)
    i = 0                                    # next unmatched child (least greedy)
    for cookie in s:                         # smallest cookie first
        if i < len(g) and g[i] <= cookie:    # smallest cookie that satisfies the least greedy child
            i += 1
    return i

def brute(g, s):                             # try every cookie for every child, bitmask of used cookies
    @lru_cache(None)
    def f(i, used):
        if i == len(g):
            return 0
        best = f(i + 1, used)                # leave child i unhappy
        for j in range(len(s)):
            if not used >> j & 1 and s[j] >= g[i]:
                best = max(best, 1 + f(i + 1, used | 1 << j))
        return best
    return f(0, 0)

for g, s, exp in [([1, 2, 3], [1, 1], 1), ([1, 2], [1, 2, 3], 2), ([], [4], 0), ([5, 6], [1, 2], 0)]:
    assert assign_cookies(g, s) == brute(tuple(g), tuple(s)) == exp
    print('g =', g, 's =', s, '->', assign_cookies(g, s))

# exhaustive: lists of length 0..4 over sizes 1..4 (sizes form a tiny alphabet)
cnt = 0
for lg in range(0, 5):
    for ls in range(0, 5):
        for g in itertools.product(range(1, 5), repeat=lg):
            for s in itertools.product(range(1, 5), repeat=ls):
                assert assign_cookies(list(g), list(s)) == brute(g, s), (g, s)
                cnt += 1
print('exhaustive ok:', cnt, 'pairs')

for _ in range(1000):
    g = [random.randint(1, 8) for _ in range(random.randint(0, 7))]
    s = [random.randint(1, 8) for _ in range(random.randint(0, 7))]
    assert assign_cookies(g, s) == brute(tuple(g), tuple(s))
print('random ok: 1000 pairs')

# a wasteful rule (biggest cookie to the least greedy child) is wrong:
def wrong_biggest_cookie_to_first_child(g, s):      # gives each child (sorted ascending) the BIGGEST cookie left
    g = sorted(g)
    s = sorted(s)
    done = 0
    for c in g:
        if s and s[-1] >= c:
            s.pop()
            done += 1
    return done
bad = []
for g in itertools.product(range(1, 4), repeat=2):
    for s in itertools.product(range(1, 4), repeat=2):
        if wrong_biggest_cookie_to_first_child(list(g), list(s)) != assign_cookies(list(g), list(s)):
            bad.append((g, s))
print('wasteful rule differs from greedy on', len(bad), 'tiny cases, e.g.', bad[0] if bad else None)
assert wrong_biggest_cookie_to_first_child([1, 3], [1, 3]) == 1 and assign_cookies([1, 3], [1, 3]) == 2

# edge cases and max size
assert assign_cookies([], []) == 0
assert assign_cookies([1], []) == 0
assert assign_cookies([2 ** 31 - 1], [2 ** 31 - 1]) == 1
assert assign_cookies([1] * 30000, [1] * 30000) == 30000
assert assign_cookies([1] * 30000, [1] * 29999) == 29999
assert assign_cookies([2, 2, 2], [1, 1, 1]) == 0
print('edge cases ok')
```

**Output (my run):**
```
g = [1, 2, 3] s = [1, 1] -> 1
g = [1, 2] s = [1, 2, 3] -> 2
g = [] s = [4] -> 0
g = [5, 6] s = [1, 2] -> 0
exhaustive ok: 116281 pairs
random ok: 1000 pairs
wasteful rule differs from greedy on 20 tiny cases, e.g. ((1, 2), (1, 2))
edge cases ok
```

**Edge cases:**
- No children or no cookies: 0.
- Sizes up to 2^31 - 1: Python ints, no overflow.
- Equal sizes: a cookie equal to the greed is enough (`<=`).
- 30,000 children and 29,999 cookies of size 1: 29,999.
- Everyone too greedy: 0.

**Follow-ups:**
- Each cookie can serve several children? Different problem; think capacity.
- Minimum cookies needed to satisfy everyone? Count by sorted greed with a heap or two pointers.
- Two-pointer view from the other end (biggest cookie to the greediest child) also works, but reasoning from the least greedy side is simpler to state.

**Common mistakes:**
- Using `<` instead of `<=`.
- Not sorting one of the lists.
- Advancing the child pointer on every cookie (lets unsatisfied cookies "use up" children).
- Handing out the biggest cookie first and wasting it on a small greed.

### Q20 ⭐⭐ 🟢 Minimum cost to connect sticks. `sticks` holds positive integers (1 <= len <= 10^4, each <= 10^4). Joining two sticks of lengths a and b costs a + b and produces one stick of length a + b; repeat until one stick remains. Return the minimum total cost (0 for a single stick). Always join the two shortest sticks with a min-heap (O(n log n)); say why this is Huffman's merge rule and why joining the longest sticks first is worse (give a three-stick counter-example). Example: sticks=[2, 4, 3] -> 14; sticks=[1, 8, 3, 5] -> 30; sticks=[5] -> 0; sticks=[1, 1, 1, 1] -> 8.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Heap pattern guides and lists (igotanoffer heap interview questions, the LeetCode discuss post 'Master HEAP' on four heap patterns, the techinterview.org heap and priority-queue patterns page, a DesignGurus heap guide; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Huffman merging: always combine the two smallest with a min-heap.

**Say this first (1 line):** "Every time a stick is inside a join, its length is paid again, so short sticks should be joined early (they get paid many times, but they are small) and long sticks late. A min-heap gives me the two shortest each time."

**Brute force:**
- Try every pair at every step and take the cheapest total (memoised on the sorted multiset of lengths). Exponential; used as the oracle for up to 6 sticks.

**Optimal:**
- `heapify(sticks)`; `total = 0`. While more than one stick: pop `a`, pop `b`, `total += a + b`, push `a + b`. Return `total`.
- One stick: loop never runs, 0.
- Why it is Huffman's merge rule: the joins form a binary tree whose leaves are the original sticks. A stick of length w at depth d is included in d joins, so the total cost is the sum over leaves of `w * d`. Minimising that for fixed weights is exactly the Huffman coding problem, and merging the two lightest nodes is Huffman's greedy rule. The code builds the actual merge tree and confirms the weighted depth sum equals the heap total.
- Exchange idea: in an optimal tree the two lightest leaves can be made siblings at the deepest level; merging them is then a smaller instance of the same problem.
- Longest first is worse. Counter-example `[1, 2, 3]`: shortest first costs (1+2) + (3+3) = 9; longest first costs (3+2) + (5+1) = 11. Over all 125 triples with values 1..5, longest-first loses on 120 of them.
- Heap items are plain ints here, so ties never raise. Where a tuple carries a payload, ties on the weight compare the payload; the code shows the `TypeError` for dict payloads and uses `(weight, unique_id)` in the tree builder to avoid it.

**Complexity:** Time O(n log n): heapify O(n), n - 1 rounds with two pops and one push. Space O(n).

**Dry run:** `[2, 4, 3]`.
- Pop 2 and 3, cost 5, push 5. Heap `[4, 5]`.
- Pop 4 and 5, cost 9, push 9. Heap `[9]`.
- Total 5 + 9 = 14.

**Code:**
```python
import heapq
import itertools
import random
from functools import lru_cache

random.seed(20)

def connect_sticks(sticks):
    heap = list(sticks)
    heapq.heapify(heap)                      # min-heap of lengths
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)              # two shortest
        b = heapq.heappop(heap)
        total += a + b
        heapq.heappush(heap, a + b)
    return total

def connect_longest_first(sticks):           # WRONG on purpose: join the two LONGEST
    a = sorted(sticks)
    total = 0
    while len(a) > 1:
        x = a.pop()
        y = a.pop()
        total += x + y
        a.append(x + y)
        a.sort()
    return total

def brute(sticks):                           # try every pair at every step, memoised on the sorted multiset
    @lru_cache(None)
    def f(t):
        if len(t) == 1:
            return 0
        best = 10 ** 18
        for i, j in itertools.combinations(range(len(t)), 2):
            rest = [t[k] for k in range(len(t)) if k not in (i, j)] + [t[i] + t[j]]
            best = min(best, t[i] + t[j] + f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(sticks)))

def weighted_depth(sticks):                  # build the merge tree, then sum leaf weight * leaf depth
    heap = [(w, i) for i, w in enumerate(sticks)]        # (weight, unique id): ties never reach a non-orderable item
    heapq.heapify(heap)
    kids = {}
    nxt = len(sticks)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        kids[nxt] = (a[1], b[1])
        heapq.heappush(heap, (a[0] + b[0], nxt))
        nxt += 1
    total = 0
    stack = [(heap[0][1], 0)]                            # iterative walk from the root
    while stack:
        node, d = stack.pop()
        if node in kids:
            stack.append((kids[node][0], d + 1))
            stack.append((kids[node][1], d + 1))
        else:
            total += sticks[node] * d
    return total

for st, exp in [([2, 4, 3], 14), ([1, 8, 3, 5], 30), ([5], 0), ([1, 1, 1, 1], 8)]:
    assert connect_sticks(st) == brute(st) == weighted_depth(st) == exp
    print(st, '->', connect_sticks(st))

for _ in range(1000):
    st = [random.randint(1, 9) for _ in range(random.randint(1, 6))]
    assert connect_sticks(st) == brute(st) == weighted_depth(st), st
print('random ok: 1000 inputs')

# three-stick counter-example for longest-first
cx = [1, 2, 3]
print('longest first on', cx, '->', connect_longest_first(cx), '; shortest first ->', connect_sticks(cx), '; brute ->', brute(cx))
assert connect_longest_first(cx) == 11 and connect_sticks(cx) == 9 == brute(cx)
worse = sum(connect_longest_first(list(c)) > connect_sticks(list(c)) for c in itertools.product(range(1, 6), repeat=3))
print('triples over 1..5 where longest-first costs more:', worse, 'of 125')

# the heap of tuples: equal weights tie, so the tuple needs a unique tiebreak if the payload is not orderable
try:
    h = []
    heapq.heappush(h, (3, {'name': 'x'}))
    heapq.heappush(h, (3, {'name': 'y'}))
except TypeError as e:
    print('TypeError on tied weights with dict payload:', e)

# edge cases and max size
assert connect_sticks([7]) == 0
assert connect_sticks([1, 1]) == 2
assert connect_sticks([10 ** 4] * 4) == 80000
big = [random.randint(1, 10 ** 4) for _ in range(10 ** 4)]
assert connect_sticks(big) == weighted_depth(big)
print('edge cases ok; cost for n = 10^4 random sticks:', connect_sticks(big))
```

**Output (my run):**
```
[2, 4, 3] -> 14
[1, 8, 3, 5] -> 30
[5] -> 0
[1, 1, 1, 1] -> 8
random ok: 1000 inputs
longest first on [1, 2, 3] -> 11 ; shortest first -> 9 ; brute -> 9
triples over 1..5 where longest-first costs more: 120 of 125
TypeError on tied weights with dict payload: '<' not supported between instances of 'dict' and 'dict'
edge cases ok; cost for n = 10^4 random sticks: 645453002
```

**Edge cases:**
- Single stick: 0. Two sticks: their sum.
- All equal (`[1, 1, 1, 1]`): 8 (two joins of 2, one join of 4). `[10^4] * 4` gives 80,000.
- The total can be large: n = 10^4 random sticks gives hundreds of millions; Python ints do not overflow, a 32-bit language might.
- Duplicates are fine; the heap holds ints.

**Follow-ups:**
- Print the Huffman codes? Keep a tree of nodes, add a unique id to break ties, and walk the tree iteratively.
- Why must the heap hold the merged stick again? The merged stick can be shorter than other sticks, and it must compete for the next two shortest.
- Sort once and use two queues (originals and merged, both already sorted) for O(n) after the sort.

**Common mistakes:**
- Joining the largest sticks first.
- Adding only the new stick length rather than `a + b` to the total (same value, but people sometimes add the wrong variable).
- Forgetting to push the merged stick back.
- Not heapifying (popping from an unsorted list with `min`, O(n^2)).

### Q21 ⭐⭐ 🟡 Minimum arrows to burst balloons. Each balloon is a horizontal segment [x_start, x_end] on the x axis (closed, x_start <= x_end, integers in [-2^31, 2^31 - 1], 1 <= len <= 10^5, segments may touch). An arrow shot straight up at integer x bursts every balloon with x_start <= x <= x_end. Return the minimum number of arrows. Sort by x_end and shoot at the end of the first unburst balloon; say why sorting by x_start fails, and why comparing with a subtraction such as `a[1] - b[1]` as a sort key is an overflow trap in fixed-width languages although harmless in Python. Example: points=[[10, 16], [2, 8], [1, 6], [7, 12]] -> 2; points=[[1, 2], [3, 4], [5, 6], [7, 8]] -> 4; points=[[1, 2], [2, 3], [3, 4], [4, 5]] -> 2; points=[[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]] -> 2.
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Interval pattern guides on techinterview.org (merge, insert, meeting rooms, employee free time, interval scheduling; search snippets only, not opened; the site's own 'asked at' lists were not verified) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Interval greedy, same family as non-overlapping intervals (Q16): sort by end, act at the end.

**Say this first (1 line):** "Sort balloons by right end. Shoot an arrow at the end of the first unburst balloon: that is as far right as it can go while still hitting it, so it hits the most following balloons. Skip every balloon that arrow already hits."

**Brute force:**
- Try sets of integer x positions of growing size until every balloon contains one. Exponential in the coordinate range; used as the oracle for small coordinates.

**Optimal:**
- Sort by end. `shot = None`, `arrows = 0`. For each `(s, e)`: if `shot is None or s > shot`, the arrow at `shot` misses it, so `arrows += 1` and `shot = e`.
- Closed segments, so `s == shot` is a hit (`[1,5]` and `[5,9]` share one arrow at 5). That is why the test is `s > shot`, not `>=`.
- Why shooting at the first balloon's END is safe: any arrow that bursts that balloon sits at some x <= e; moving it right to e keeps it inside that balloon and cannot lose any balloon whose end is >= e (all later balloons have end >= e, and they need `x >= s`, which a larger x only helps).
- Why sorting by START fails as usually written: with `[[1, 10], [2, 3], [4, 5]]` the naive start-sorted scan sets the group end to 10 and says one arrow, but 3 < 4 so no single x hits both small balloons and the big one: the answer is 2. The code shows the naive version wrong on 332 small inputs. Sorting by start only works if you also shrink the group's end to the minimum end seen (the code includes that variant and it matches), which is more state to get wrong. Sorting by end needs none of it.
- Overflow trap: a comparator written as `a[1] - b[1]` is fine in Python, where ints never overflow and sorting should use `key=lambda p: p[1]` anyway. In a language with 32-bit ints, `2**31 - 1 - (-2**31)` wraps to -1, so the comparator says the larger value is smaller and sorts wrongly. The code emulates the wrap and prints the wrong order. Compare with `<` or `Integer.compare`, never subtract.

**Complexity:** Time O(n log n) for the sort, O(n) for the scan. Space O(n) for the sorted copy.

**Dry run:** `[[10,16],[2,8],[1,6],[7,12]]`. Sorted by end: `[1,6] [2,8] [7,12] [10,16]`.
- `[1,6]`: no arrow yet, arrows 1, `shot = 6`.
- `[2,8]`: 2 <= 6, hit.
- `[7,12]`: 7 > 6, arrows 2, `shot = 12`.
- `[10,16]`: 10 <= 12, hit.
Answer 2.

**Code:**
```python
import itertools
import random
from functools import cmp_to_key

random.seed(21)

def min_arrows(points):
    arrows = 0
    shot = None                              # x of the last arrow
    for s, e in sorted(points, key=lambda p: p[1]):      # sort by END
        if shot is None or s > shot:         # the arrow at `shot` misses this balloon (touching is a hit)
            arrows += 1
            shot = e                         # new arrow at this balloon's end
    return arrows

def by_start_naive(points):                  # WRONG: sort by start, never shrink the group's end
    arrows = 0
    end = None
    for s, e in sorted(points):
        if end is None or s > end:
            arrows += 1
            end = e
    return arrows

def by_start_shrinking(points):              # correct variant: sort by start AND shrink end to the min
    arrows = 0
    end = None
    for s, e in sorted(points):
        if end is None or s > end:
            arrows += 1
            end = e
        else:
            end = min(end, e)
    return arrows

def brute(points):                           # smallest set of integer x that hits every balloon (small coordinates)
    lo = min(p[0] for p in points)
    hi = max(p[1] for p in points)
    for r in range(1, len(points) + 1):
        for xs in itertools.combinations(range(lo, hi + 1), r):
            if all(any(s <= x <= e for x in xs) for s, e in points):
                return r

for pts, exp in [([[10, 16], [2, 8], [1, 6], [7, 12]], 2), ([[1, 2], [3, 4], [5, 6], [7, 8]], 4),
                 ([[1, 2], [2, 3], [3, 4], [4, 5]], 2),
                 ([[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]], 2)]:
    assert min_arrows(pts) == brute(pts) == exp
    print(pts, '->', min_arrows(pts))

# exhaustive: every multiset of up to 4 balloons with endpoints in 0..4 (15 possible balloons)
pool = [[a, b] for a in range(5) for b in range(a, 5)]
cnt = naive_bad = 0
for k in range(1, 5):
    for combo in itertools.combinations_with_replacement(pool, k):
        pts = [list(x) for x in combo]
        assert min_arrows(pts) == brute(pts), pts
        assert by_start_shrinking(pts) == min_arrows(pts), pts
        naive_bad += by_start_naive(pts) != min_arrows(pts)
        cnt += 1
print('exhaustive ok:', cnt, 'multisets; naive sort-by-start wrong on', naive_bad)

for _ in range(300):
    pts = []
    for _ in range(random.randint(1, 7)):
        a = random.randint(-6, 6)
        pts.append([a, random.randint(a, a + 5)])
    assert min_arrows(pts) == brute(pts)
print('random ok: 300 inputs')

cx = [[1, 10], [2, 3], [4, 5]]
print('naive sort-by-start on', cx, '->', by_start_naive(cx), '(wrong); correct ->', min_arrows(cx), '; brute ->', brute(cx))
assert by_start_naive(cx) == 1 and min_arrows(cx) == 2 == brute(cx)

# overflow trap: emulate a 32-bit signed subtraction comparator
def wrap32(x):
    return (x + 2 ** 31) % 2 ** 32 - 2 ** 31
def cmp32(a, b):
    return wrap32(a[1] - b[1])               # what a C or Java comparator `a[1] - b[1]` would compute
lo_b, hi_b = [-2 ** 31, -2 ** 31], [2 ** 31 - 1, 2 ** 31 - 1]
print('true a-b:', hi_b[1] - lo_b[1], '| 32-bit a-b:', cmp32(hi_b, lo_b), '(negative: says hi < lo, wrong order)')
bad_order = sorted([hi_b, lo_b], key=cmp_to_key(cmp32))
print('order from 32-bit subtraction comparator:', bad_order, '| correct:', sorted([hi_b, lo_b], key=lambda p: p[1]))
assert cmp32(hi_b, lo_b) < 0 and hi_b[1] - lo_b[1] > 0
big = [[-2 ** 31, 2 ** 31 - 1], [-2 ** 31, -2 ** 31], [2 ** 31 - 1, 2 ** 31 - 1]]
assert min_arrows(big) == 2                  # Python ints: no overflow; sort by key, no subtraction

# edge cases
assert min_arrows([[5, 5]]) == 1
assert min_arrows([[1, 1], [1, 1]]) == 1
assert min_arrows([[1, 5], [5, 9]]) == 1     # touching balloons share the arrow at x = 5
assert min_arrows([[i, i] for i in range(10 ** 5)]) == 10 ** 5
assert min_arrows([[0, 10 ** 9]] * 10 ** 5) == 1
print('edge cases ok')
```

**Output (my run):**
```
[[10, 16], [2, 8], [1, 6], [7, 12]] -> 2
[[1, 2], [3, 4], [5, 6], [7, 8]] -> 4
[[1, 2], [2, 3], [3, 4], [4, 5]] -> 2
[[3, 9], [7, 12], [3, 8], [6, 8], [9, 10], [2, 9], [0, 9], [3, 9], [0, 6], [2, 8]] -> 2
exhaustive ok: 3875 multisets; naive sort-by-start wrong on 332
random ok: 300 inputs
naive sort-by-start on [[1, 10], [2, 3], [4, 5]] -> 1 (wrong); correct -> 2 ; brute -> 2
true a-b: 4294967295 | 32-bit a-b: -1 (negative: says hi < lo, wrong order)
order from 32-bit subtraction comparator: [[2147483647, 2147483647], [-2147483648, -2147483648]] | correct: [[-2147483648, -2147483648], [2147483647, 2147483647]]
edge cases ok
```

**Edge cases:**
- One balloon: 1 arrow. A zero-width balloon `[5, 5]` still needs an arrow at 5.
- Touching balloons share an arrow (`[[1,2],[2,3],[3,4],[4,5]]` needs 2, not 4).
- All identical: 1. All disjoint: n (10^5 zero-width balloons gives 10^5).
- Extreme coordinates `-2^31` and `2^31 - 1`: Python handles them; the comparator subtraction is the only danger.

**Follow-ups:**
- Same as erase-overlap? Closely related: the arrows needed equal the maximum number of pairwise-disjoint balloons (for closed segments), but the code here counts groups directly.
- Arrows may only be shot at given endpoints? Same greedy (it already shoots at ends).
- Weighted or limited arrows? No longer greedy.

**Common mistakes:**
- `s >= shot` (counts touching balloons as missed).
- Sorting by start and not shrinking the group's end.
- Subtracting in the comparator (overflow in fixed-width languages).
- Setting `shot` to the start or to the previous balloon's end instead of the current balloon's end.

### Q22 ⭐⭐ 🟡 Partition labels. Given a lowercase string `s` (1 <= len <= 500), cut it into as many contiguous parts as possible so that each letter appears in at most one part, and return the list of part lengths in order. The answer is unique (the finest valid partition is unique). Record the last index of each letter, then scan keeping the farthest last index seen in the current part and cut when the scan index reaches it; say why this is greedy (each cut is made at the earliest legal place) and why it is O(n). Example: s='ababcbacadefegdehijhklij' -> [9, 7, 8]; s='eccbbbbdec' -> [10]; s='a' -> [1]; s='abc' -> [1, 1, 1].
**Asked at:** Greedy pattern guides on techinterview.org (activity selection, jump game, gas station, candy, task scheduling, Huffman coding; search snippets only, not opened; the snippets did not cover partition labels or exchange arguments) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Greedy with last occurrences: a part must stretch to the last copy of every letter it contains.

**Say this first (1 line):** "I record the last index of each letter. Then I scan, keep the farthest last index of anything in the current part, and cut when my index reaches that farthest point, because nothing inside still needs anything further right."

**Brute force:**
- Try every subset of the n - 1 cut positions, keep the partitions where no letter appears in two parts, take the one with most parts. O(2^n * n), fine for n <= 8 as the oracle.

**Optimal:**
- `last = {ch: i}` for the final occurrence of each letter.
- `start = end = 0`. For each `i, ch`: `end = max(end, last[ch])`. If `i == end`, the part `start..i` is closed: record `i - start + 1`, set `start = i + 1`.
- **Why it is greedy:** each cut is made at the earliest index where it is legal (no letter seen so far reappears later). Cutting earlier is impossible; cutting later can only merge parts and lower the count.
- **Why the answer is unique:** every legal cut position is forced. A cut is legal exactly when no letter spans it, and the set of legal cut positions does not depend on any choice, so the finest partition uses all of them. The code lists all valid partitions of every string over 'abc' up to length 8 (9,840 strings) and over 'abcd' up to length 7 (21,844 strings) and confirms exactly one has the most parts, and that it equals the greedy output.
- Why `i == end` is a valid test: by then the scan has seen every letter in the part, and the farthest last occurrence is `i` itself, so no letter reaches past `i`.

**Complexity:** Time O(n): one pass to build `last`, one pass to scan. Space O(1) (at most 26 letters in the dict) plus the output list.

**Dry run:** `'ababcbacadefegdehijhklij'`. Last indices: a 8, b 5, c 7, d 14, e 15, f 11, g 13, h 19, i 22, j 23, k 20, l 21.
- Indices 0 to 8: `end` reaches 8 (from 'a'), cut at i = 8, size 9.
- Indices 9 to 15: 'd' pushes `end` to 14, 'e' pushes it to 15, cut at i = 15, size 7.
- Indices 16 to 23: 'h' 19, 'i' 22, 'j' 23, cut at i = 23, size 8.
Result `[9, 7, 8]`.

**Code:**
```python
import itertools
import random

random.seed(22)

def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}   # last index of each letter
    sizes = []
    start = end = 0                            # current part is s[start..], end = farthest last index so far
    for i, ch in enumerate(s):
        end = max(end, last[ch])               # the part must reach the last copy of every letter seen
        if i == end:                           # nothing in the part needs anything further: cut here
            sizes.append(end - start + 1)
            start = i + 1
    return sizes

def valid_cuts(s, cuts):                       # parts: cut positions strictly inside 1..n-1
    n = len(s)
    parts = [s[a:b] for a, b in zip([0] + list(cuts), list(cuts) + [n])]
    seen = set()
    for p in parts:
        letters = set(p)
        if letters & seen:
            return None
        seen |= letters
    return parts

def brute_all(s):                              # every valid partition, as a list of part-length lists
    n = len(s)
    out = []
    for r in range(n):
        for cuts in itertools.combinations(range(1, n), r):
            parts = valid_cuts(s, cuts)
            if parts is not None:
                out.append([len(p) for p in parts])
    return out

def brute_best(s):
    allp = brute_all(s)
    m = max(len(p) for p in allp)
    best = [p for p in allp if len(p) == m]
    return best

for s, exp in [('ababcbacadefegdehijhklij', [9, 7, 8]), ('eccbbbbdec', [10]), ('a', [1]), ('abc', [1, 1, 1])]:
    assert partition_labels(s) == exp
    if len(s) <= 12:
        assert brute_best(s) == [exp]
    print(repr(s), '->', partition_labels(s))

# exhaustive: all strings over 'abc' of length 1..8 (9840 strings): the finest partition is UNIQUE and equals the greedy
cnt = 0
for n in range(1, 9):
    for t in itertools.product('abc', repeat=n):
        s = ''.join(t)
        best = brute_best(s)
        assert len(best) == 1, (s, best)                  # uniqueness claim from the prompt
        assert best[0] == partition_labels(s), s
        assert sum(best[0]) == n
        cnt += 1
print('exhaustive ok:', cnt, 'strings over abc; finest partition unique every time')

# also 4 letters, length up to 7
cnt = 0
for n in range(1, 8):
    for t in itertools.product('abcd', repeat=n):
        s = ''.join(t)
        assert brute_best(s) == [partition_labels(s)], s
        cnt += 1
print('exhaustive ok:', cnt, 'strings over abcd (length <= 7)')

for _ in range(300):
    s = ''.join(random.choice('abcdefghij') for _ in range(random.randint(1, 500)))
    sizes = partition_labels(s)
    assert sum(sizes) == len(s)
    pos = 0
    seen = set()
    for z in sizes:                                         # each letter appears in exactly one part
        part = set(s[pos:pos + z])
        assert not (part & seen)
        seen |= part
        pos += z
print('random ok: 300 strings up to length 500')

# greedy meaning: every cut is made at the EARLIEST legal index; moving any cut later only merges parts
s = 'ababcbacadefegdehijhklij'
cuts = list(itertools.accumulate(partition_labels(s)))[:-1]
print('cut positions for the long example:', cuts)

# edge cases
assert partition_labels('aaaa') == [4]
assert partition_labels('abab') == [4]
assert partition_labels('abcabc') == [6]
assert partition_labels('aabbcc') == [2, 2, 2]
assert partition_labels('abcdefghijklmnopqrstuvwxyz' * 1) == [1] * 26
assert partition_labels('a' + 'b' * 498 + 'a') == [500]
print('edge cases ok')
```

**Output (my run):**
```
'ababcbacadefegdehijhklij' -> [9, 7, 8]
'eccbbbbdec' -> [10]
'a' -> [1]
'abc' -> [1, 1, 1]
exhaustive ok: 9840 strings over abc; finest partition unique every time
exhaustive ok: 21844 strings over abcd (length <= 7)
random ok: 300 strings up to length 500
cut positions for the long example: [9, 16]
edge cases ok
```

**Edge cases:**
- One character: `[1]`. All distinct letters: all ones.
- All the same letter: one part (`'aaaa'` gives `[4]`).
- A letter at both ends (`'a' + 'b' * 498 + 'a'`) forces one part of length 500.
- Letters that interleave (`'abab'`, `'abcabc'`) cannot be separated.
- Sizes always sum to the string length.

**Follow-ups:**
- Return the parts, not the lengths? Slice with the same cut positions.
- Uppercase, digits, Unicode? Use a dict, not a 26-slot array.
- Merge-intervals view? Each letter spans `[first, last]`; the parts are the merged intervals of those spans (Part 8 merge intervals).
- Fewest parts instead? Trivial: one part.

**Common mistakes:**
- Cutting when the count of the current letter reaches zero (ignores other letters in the part).
- Resetting `end` to `last[ch]` instead of taking the max.
- Starting a new part at `i` instead of `i + 1`.
- Using `first` occurrences instead of `last`.
