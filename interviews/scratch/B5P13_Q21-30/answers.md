# Book 5 Part 13, answers Q21-Q30 (Wave B)

### Q21 ⭐⭐ 🟢 Running sum and pivot index. `nums` has 1 <= len <= 10^4 integers (|value| <= 1000). Return `[pivot, running]`: `running` is the list of running sums (`running[i] = nums[0] + ... + nums[i]`, what `itertools.accumulate` gives), and `pivot` is the smallest index i such that the sum of the items strictly to its left equals the sum of the items strictly to its right (an empty side sums to 0), or -1 if there is no such index. Do it in O(n) time with the total and the running sum: the left sum is `running[i] - nums[i]` and the right sum is `total - running[i]`. Explain why negative values do not break this (unlike a sliding window) and why you must return the leftmost index when several qualify. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n^2) rescanning of each side on small inputs. Example: nums=[1, 7, 3, 6, 5, 6] -> [3, [1, 8, 11, 17, 22, 28]]; nums=[1, 2, 3] -> [-1, [1, 3, 6]]; nums=[2, 1, -1] -> [0, [2, 3, 2]]; nums=[0] -> [0, [0]].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Prefix sums. One running total turns "sum of everything on one side" into an O(1) subtraction.

**Say this first (1 line):** "Left sum is `running[i] - nums[i]`, right sum is `total - running[i]`; scan once and return the first index where they are equal, else -1."

**Brute force:** For each index i, add up `nums[:i]` and `nums[i+1:]` and compare. O(n) per index, O(n^2) overall. With n = 10^4 that is about 10^8 additions in the worst case. It is the oracle in the cross-check.

**Optimal:**
- Build `running` with `itertools.accumulate`. `total = running[-1]`.
- For each i: `left = running[i] - nums[i]` (everything before i), `right = total - running[i]` (everything after i). Compare.
- Scan left to right and return at the first match. That gives the leftmost pivot for free.
- Invariant: `left + nums[i] + right == total` for every i. So the test `left == right` is the same as `2 * left + nums[i] == total`.
- Negatives are fine because we only test equality at each index. We never move a window and never assume the sum only grows. A sliding window needs the sum to change monotonically when you shrink or grow it. With negatives that breaks. A prefix sum does not care about signs.
- Leftmost matters because several indexes can qualify. In `[0, 0]` index 0 (left 0, right 0) and index 1 (left 0, right 0) both work. The answer must be 0. The exhaustive check below finds 2795 such lists out of 19530.

**Complexity:** Time O(n): one accumulate pass plus one scan. Space O(n) for `running`, which the question asks us to return anyway. If you only needed the pivot, keep a single integer `left` and use O(1) space.

**Dry run:** `[1, 7, 3, 6, 5, 6]`, total 28. At i=3, x=6: `running[3] = 17`, left = 17 - 6 = 11, right = 28 - 17 = 11. Equal, so the pivot is 3. Indexes 0 to 2 fail (left 0, 1, 8 against right 27, 20, 17). The program prints each step.

**Code:**
```python
import itertools
import random

random.seed(2101)

def pivot_index(nums):
    """O(n): returns [leftmost pivot or -1, running sums]."""
    running = list(itertools.accumulate(nums))
    total = running[-1]
    for i, x in enumerate(nums):
        left = running[i] - x            # sum of nums[:i]
        right = total - running[i]       # sum of nums[i+1:]
        if left == right:
            return [i, running]          # first hit = leftmost
    return [-1, running]

def brute(nums):
    run, s = [], 0
    for v in nums:
        s += v
        run.append(s)
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]):   # rescan both sides: O(n^2)
            return [i, run]
    return [-1, run]

examples = [([1, 7, 3, 6, 5, 6], [3, [1, 8, 11, 17, 22, 28]]),
            ([1, 2, 3], [-1, [1, 3, 6]]),
            ([2, 1, -1], [0, [2, 3, 2]]),
            ([0], [0, [0]])]
for nums, want in examples:
    assert pivot_index(nums) == want == brute(nums)
    print(nums, '->', pivot_index(nums))

# dry run on the first example
nums = [1, 7, 3, 6, 5, 6]
run = list(itertools.accumulate(nums)); total = run[-1]
for i, x in enumerate(nums):
    print(f'  i={i} x={x} left={run[i] - x} right={total - run[i]}')

# seeded random cross-check
for _ in range(3000):
    nums = [random.randint(-4, 4) for _ in range(random.randint(1, 9))]
    assert pivot_index(nums) == brute(nums)
print('random cross-check ok: 3000 cases')

# exhaustive: every list of length 1..6 over -2..2
total_lists = several = 0
for n in range(1, 7):
    for nums in itertools.product(range(-2, 3), repeat=n):
        nums = list(nums)
        assert pivot_index(nums) == brute(nums)
        total_lists += 1
        all_piv = [i for i in range(n) if sum(nums[:i]) == sum(nums[i + 1:])]
        if len(all_piv) > 1:
            several += 1
            assert pivot_index(nums)[0] == all_piv[0]     # leftmost wins
print('exhaustive ok:', total_lists, 'lists; with 2+ valid pivots:', several)
print('example with 2 pivots:', [0, 0], '->', pivot_index([0, 0])[0], '(index 1 also qualifies)')

# edge asserts
assert pivot_index([5])[0] == 0                      # both sides empty
assert pivot_index([-1, 3, -1])[0] == 1             # negatives are fine: -1 on both sides
assert pivot_index([1, -1])[0] == -1
big = [1000] * 10**4
assert pivot_index(big)[0] == -1 and pivot_index(big)[1][-1] == 10**7
print('edge asserts ok')
```

**Output (my run):**
```
[1, 7, 3, 6, 5, 6] -> [3, [1, 8, 11, 17, 22, 28]]
[1, 2, 3] -> [-1, [1, 3, 6]]
[2, 1, -1] -> [0, [2, 3, 2]]
[0] -> [0, [0]]
  i=0 x=1 left=0 right=27
  i=1 x=7 left=1 right=20
  i=2 x=3 left=8 right=17
  i=3 x=6 left=11 right=11
  i=4 x=5 left=17 right=6
  i=5 x=6 left=22 right=0
random cross-check ok: 3000 cases
exhaustive ok: 19530 lists; with 2+ valid pivots: 2795
example with 2 pivots: [0, 0] -> 0 (index 1 also qualifies)
edge asserts ok
```

**Edge cases:**
- One element: both sides are empty, so the pivot is 0 (`[0]` and `[5]`).
- Pivot at the first index: `[2, 1, -1]` gives 0 because left is 0 and right is 1 - 1 = 0.
- Pivot at the last index: needs the whole left side to sum to 0.
- No pivot: `[1, 2, 3]` and `[1, -1]` give -1.
- All 1000s with n = 10^4: total is 10^7, no pivot. Python ints cannot overflow, but in a 32-bit language the sums still fit (at most 10^7).

**Follow-ups:**
- *Return all pivots?* Collect instead of returning at the first match. Same O(n).
- *Many range-sum queries?* The same `running` array answers any `sum(l..r)` as `running[r] - running[l-1]`.
- *Why not two pointers here?* There is no monotone rule that says which pointer to move once negatives are allowed.

**Common mistakes:**
- Including `nums[i]` in the left sum (off by one). `running[i]` already contains it, so subtract it.
- Forgetting that an empty side is 0 (first and last index).
- Returning the last match, or the one nearest the middle, instead of the leftmost.
- Using a window or early `break` when the running sum passes half the total. That only works for non-negative numbers.

### Q22 ⭐⭐ 🟢 Rounding half to even and why floats surprise you. `values` is a list of 1 to 30 decimal strings such as '2.5' or '-1.005' with at most 3 digits after the point (a negative value has absolute value at least 0.01). For each string s return `[a, b, c, d]`: `a = round(float(s))` (Python 3 rounds ties to the nearest EVEN integer, so 2.5 gives 2 and 3.5 gives 4); `b` = the integer obtained by rounding the exact decimal value half away from zero (`Decimal(s)` with `ROUND_HALF_UP`, so 2.5 gives 3 and -2.5 gives -3); `c = repr(round(float(s), 2))`; `d = str(Decimal(s).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))` (always two decimals). Explain why `round(2.675, 2)` gives 2.67 (the stored binary double is slightly below 2.675, so it is not a tie at all), why `a` is a true tie rule only because .5 is exactly representable, why banks and statisticians prefer half-even (no systematic upward bias) and when to use Decimal instead of float (money). In the answer include a dry run on the first example and a seeded random cross-check of your solution against exact Fraction arithmetic on small inputs. Example: values=['2.5', '0.5', '-1.5', '2.675', '1.005', '3.5', '-0.5'] -> [[2, 3, '2.5', '2.50'], [0, 1, '0.5', '0.50'], [-2, -2, '-1.5', '-1.50'], [3, 3, '2.67', '2.68'], [1, 1, '1.0', '1.00'], [4, 4, '3.5', '3.50'], [0, -1, '-0.5', '-0.50']]; values=['10'] -> [[10, 10, '10.0', '10.00']].
**Asked at:** Python documentation for int, float, Decimal and Fraction (docs.python.org fetch failed with ENOTFOUND, not opened; behaviour verified by running Python 3.13)

**Pattern:** Number representation. Python's `round` works on the stored binary double. `Decimal` works on the written decimal. Know which one you are rounding.

**Say this first (1 line):** "round() on a float rounds the exact binary value, ties go to even; money is a Decimal job, because 2.675 is not stored as 2.675."

**Brute force:** Convert each string to an exact `Fraction`, do the rounding rules with integer arithmetic (floor, compare the remainder with 1/2, tie goes to the even neighbour), and format the result by hand. Exact but slow to write. It is the oracle here.

**Optimal:** Four one-liners per value:
- `a = round(float(s))`: ties to even. 2.5 gives 2, 3.5 gives 4, -1.5 gives -2, 0.5 gives 0.
- `b = int(Decimal(s).to_integral_value(ROUND_HALF_UP))`: exact decimal, ties away from zero. 2.5 gives 3, -2.5 gives -3, 0.5 gives 1.
- `c = repr(round(float(s), 2))`: the float is rounded, then printed with the shortest repr that round-trips.
- `d = str(Decimal(s).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))`: exact decimal, two places, tie to even, always two decimals.

Why `round(2.675, 2)` is 2.67: the double nearest 2.675 is 2.67499999999999982236431605997495353221893310546875. It is below the tie, so it is not a tie at all and it rounds down. `Decimal('2.675')` is exactly 2.675, a real tie, and half-even gives 2.68 (7 is odd, so go up to 8).

Why `a` is a true tie rule: x.5 is a sum of powers of two, so the double holds it exactly. Of all decimals with at most 3 digits, only the x.5 ones are exactly representable ties at integer rounding. At two places, a tie like x.xx5 is almost never exact. The program counts it: of the 10000 strings x.xx5 from 0.005 to 99.995, `round(f, 2)` differs from the exact half-even answer in 4800.

Why banks and statisticians use half-even: each tie goes up half the time and down half the time, so the rounding error averages to 0. Half-up always pushes ties the same way. For the ties 0.5, 1.5, ..., 9.5 the mean error is +0.5 for half-up and 0.0 for half-even (printed).

Use `Decimal` (or integer cents) for money. Use float for measurements.

**Complexity:** O(1) per value, O(len(values)) in total (the strings have at most a handful of digits).

**Dry run:** `'2.675'`. a: `float` is 2.67499..., `round` gives 3. b: Decimal 2.675 rounds half up to 3. c: `round(2.67499.., 2)` is 2.67, printed `'2.67'`. d: exact 2.675, tie, neighbours 2.67 (odd last digit) and 2.68 (even), so `'2.68'`. Result `[3, 3, '2.67', '2.68']`. The program prints the exact doubles behind 2.675 and 1.005.

**Code:**
```python
import math
import random
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from fractions import Fraction

random.seed(2201)

def solve(values):
    out = []
    for s in values:
        f, d = float(s), Decimal(s)
        a = round(f)                                              # ties to even
        b = int(d.to_integral_value(rounding=ROUND_HALF_UP))      # exact decimal, half away from 0
        c = repr(round(f, 2))                                     # rounds the BINARY double
        q = str(d.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))
        out.append([a, b, c, q])
    return out

def half_even(x):                      # Fraction -> int, ties to even
    fl = math.floor(x)
    r = x - fl
    return fl if r < Fraction(1, 2) else fl + 1 if r > Fraction(1, 2) else (fl if fl % 2 == 0 else fl + 1)

def brute(values):
    """Independent oracle: exact Fraction arithmetic only."""
    out = []
    for s in values:
        q, ex = Fraction(s), Fraction(float(s))              # ex = the exact value of the stored double
        hu = (1 if q >= 0 else -1) * math.floor(abs(q) + Fraction(1, 2))
        r2 = float(half_even(ex * 100) / Fraction(100))
        h2 = half_even(q * 100)
        sign, mag = ('-' if h2 < 0 else ''), abs(h2)
        out.append([half_even(ex), hu, repr(r2), f'{sign}{mag // 100}.{mag % 100:02d}'])
    return out

ex1 = ['2.5', '0.5', '-1.5', '2.675', '1.005', '3.5', '-0.5']
want1 = [[2, 3, '2.5', '2.50'], [0, 1, '0.5', '0.50'], [-2, -2, '-1.5', '-1.50'], [3, 3, '2.67', '2.68'],
         [1, 1, '1.0', '1.00'], [4, 4, '3.5', '3.50'], [0, -1, '-0.5', '-0.50']]
assert solve(ex1) == want1 == brute(ex1)
assert solve(['10']) == [[10, 10, '10.0', '10.00']] == brute(['10'])
for s, r in zip(ex1, solve(ex1)):
    print(f'{s:>6} -> {r}')

# why 2.675 surprises: the stored double is just below the tie
print('exact value of the double 2.675  :', Decimal(2.675))
print('exact value of the double 1.005  :', Decimal(1.005))
print('exact value of the double 2.5    :', Decimal(2.5), '(exact, a true tie)')
assert Decimal(2.675) < Decimal('2.675') and Decimal(1.005) < Decimal('1.005')

# which decimals with <=3 digits are exactly representable ties? only x.5 (a dyadic fraction)
assert all(Fraction(k, 1000) == Fraction(k / 1000) for k in range(500, 10001, 1000))
print('x.5 values 0.5..10.5 all exact doubles: True')

# how often do float rounding (c) and exact half-even decimal (d) disagree on x.xx5 strings?
bad = 0; total = 0
for k in range(0, 100000):
    s = f'{k // 1000}.{k % 1000:03d}'
    if s.endswith('5'):
        total += 1
        r = solve([s])[0]
        if float(r[2]) != float(r[3]):
            bad += 1
print(f'x.xx5 strings 0.005..99.995: {total}; float round(.,2) differs from exact half-even in {bad}')

# half-even removes the upward bias: average error over the ties 0.5, 1.5, ..., 9.5
ties = [k + 0.5 for k in range(10)]
up = sum(math.floor(t + 0.5) - t for t in ties) / 10
even = sum(round(t) - t for t in ties) / 10
print('mean error half-up:', up, ' half-even:', even)
assert up == 0.5 and even == 0.0

# seeded random cross-check against exact Fractions
def rand_dec():
    k = random.randint(0, 3); v = random.randint(-2000, 2000)
    if v == 0 or (v < 0 and abs(v) < 10 ** (k - 2 if k > 2 else 0)): v = 1
    sign = '-' if v < 0 else ''; v = abs(v)
    s = f'{sign}{v // 10 ** k}' + (f'.{v % 10 ** k:0{k}d}' if k else '')
    return s if abs(Fraction(s)) >= Fraction(1, 100) else '0.01'
for _ in range(3000):
    vals = [rand_dec() for _ in range(random.randint(1, 8))]
    assert solve(vals) == brute(vals), vals
print('random cross-check ok: 3000 lists')
assert solve(['-0.01'])[0] == [0, 0, '-0.01', '-0.01']
assert solve(['0.125', '0.135']) == [[0, 0, '0.12', '0.12'], [0, 0, '0.14', '0.14']]
print('edge asserts ok')
```

**Output (my run):**
```
   2.5 -> [2, 3, '2.5', '2.50']
   0.5 -> [0, 1, '0.5', '0.50']
  -1.5 -> [-2, -2, '-1.5', '-1.50']
 2.675 -> [3, 3, '2.67', '2.68']
 1.005 -> [1, 1, '1.0', '1.00']
   3.5 -> [4, 4, '3.5', '3.50']
  -0.5 -> [0, -1, '-0.5', '-0.50']
exact value of the double 2.675  : 2.67499999999999982236431605997495353221893310546875
exact value of the double 1.005  : 1.00499999999999989341858963598497211933135986328125
exact value of the double 2.5    : 2.5 (exact, a true tie)
x.5 values 0.5..10.5 all exact doubles: True
x.xx5 strings 0.005..99.995: 10000; float round(.,2) differs from exact half-even in 4800
mean error half-up: 0.5  half-even: 0.0
random cross-check ok: 3000 lists
edge asserts ok
```

**Edge cases:**
- Ties on both signs: -1.5 gives -2 in both `a` and `b`, but -0.5 gives 0 for `a` (even) and -1 for `b` (half away from zero).
- `'10'`: no fraction, `c = '10.0'`, `d = '10.00'`.
- `'-0.01'` gives `d = '-0.01'`. `a` is 0 (an int, so no negative zero is shown).
- `'1.005'`: float side gives `'1.0'` (the double is below 1.005), decimal side gives `'1.00'` (exact tie, 0 is even).
- `'0.125'` is exact in binary, so `round(0.125, 2)` really is a tie and gives 0.12. `'0.135'` is not exact and the program shows 0.14.

**Follow-ups:**
- *`math.isclose` vs `==`?* Floats are compared with a tolerance; `0.1 + 0.2 != 0.3`.
- *Why is `round(x)` an int but `round(x, 2)` a float?* With no digit argument `round` returns an int. With a digit argument it returns the same type as the input.
- *When is `Decimal` not enough?* If you need exact thirds or similar, use `Fraction`.

**Common mistakes:**
- Believing `round(2.675, 2)` is a bug in Python. The decimal you typed is simply not the number stored.
- Assuming Python rounds half up like school. It rounds half to even.
- Building a Decimal from a float: `Decimal(2.675)` gives the long binary expansion. Build it from the string.
- Using `ROUND_HALF_UP` and calling it "banker's rounding".

### Q23 ⭐⭐ 🟡 Car pooling with a difference array. `capacity` is the number of seats (1 <= capacity <= 10^5) and `trips` has 1 to 1000 items [passengers, start, end] with 1 <= passengers <= 100 and 0 <= start < end <= 1000: those passengers board at stop `start` and leave at stop `end`; at a stop, people leaving get off before people boarding get on, so the load at stop x counts trips with start <= x < end. Return `[ok, peak, first_stop]`: `ok` is True if the load never exceeds `capacity`; `peak` is the largest load over all stops 0..1000; `first_stop` is the smallest stop at which that largest load occurs. Do it in O(len(trips) + 1001) with a difference array (`d[start] += p`, `d[end] -= p`) and a running sum, and explain why this beats checking every trip at every stop (O(trips * stops)). The Corporate Flight Bookings problem is the same trick with 1-indexed inclusive ranges. In the answer include a dry run on the first example and a seeded random cross-check of your solution against counting, for every stop, the trips that cover it on small inputs. Example: capacity=4, trips=[[2, 1, 5], [3, 3, 7]] -> [False, 5, 3]; capacity=5, trips=[[2, 1, 5], [3, 3, 7]] -> [True, 5, 3]; capacity=3, trips=[[2, 1, 5], [3, 5, 7]] -> [True, 3, 5].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Difference array plus a running sum. Do range updates in O(1) each and read the result with one prefix pass.

**Say this first (1 line):** "Add p at the start stop, subtract p at the end stop, take a running sum over stops 0 to 1000: that is the load at each stop."

**Brute force:** For every stop x in 0..1000 and every trip, add the passengers if `start <= x < end`. O(trips * stops), up to 1000 * 1001 = 1,001,000 checks. It is the oracle in the cross-check.

**Optimal:**
- `d[start] += p` and `d[end] -= p`.
- `load += d[x]` for x = 0..1000; `load` is the number of passengers on board at x.
- Why it works: the running sum of `d` at x is the sum of all `+p` placed at or before x minus all `-p` placed at or before x. That is exactly the trips with `start <= x` that have not yet ended (`end > x`). This is the "leaving before boarding" rule: the `-p` at `end` is already applied when we read stop `end`.
- Track the peak with a strict `>`. Then `first_stop` stays at the smallest stop where the peak first appears. `ok` is `peak <= capacity`.
- `d` needs index up to 1000 (an `end` of 1000), so allocate 1001 or 1002 slots.

**Complexity:** Time O(T + S) with T trips and S = 1001 stops, at most 2001 steps. Space O(S). The brute force is O(T * S), about 10^6 checks for the maximum input. The difference array wins because each trip is touched twice instead of once per stop.

**Dry run:** capacity 4, trips `[2,1,5]` and `[3,3,7]`. `d` after both trips: `[0, 2, 0, 3, 0, -2, 0, -3]`. Running sum: `[0, 2, 2, 5, 5, 3, 3, 0]`. The peak is 5, first reached at stop 3. 5 > 4, so `ok` is False. Result `[False, 5, 3]`. The program prints both arrays.

**Code:**
```python
import random

random.seed(2301)
STOPS = 1001   # stops 0..1000

def car_pool(capacity, trips, stops=STOPS):
    d = [0] * (stops + 1)
    for p, a, b in trips:
        d[a] += p            # board at a
        d[b] -= p            # alight at b (not counted at b)
    load = peak = first = 0
    for x in range(stops):
        load += d[x]
        if load > peak:      # strict: keeps the SMALLEST stop of the max
            peak, first = load, x
    return [peak <= capacity, peak, first]

def brute(capacity, trips, stops=STOPS):
    loads = [sum(p for p, a, b in trips if a <= x < b) for x in range(stops)]
    peak = max(loads)
    return [all(l <= capacity for l in loads), peak, loads.index(peak)]

examples = [(4, [[2, 1, 5], [3, 3, 7]], [False, 5, 3]),
            (5, [[2, 1, 5], [3, 3, 7]], [True, 5, 3]),
            (3, [[2, 1, 5], [3, 5, 7]], [True, 3, 5])]
for cap, trips, want in examples:
    assert car_pool(cap, trips) == want == brute(cap, trips)
    print(cap, trips, '->', car_pool(cap, trips))

# dry run: difference array and running sum for example 1 (stops 0..7)
d = [0] * 8
for p, a, b in [[2, 1, 5], [3, 3, 7]]:
    d[a] += p; d[b] -= p
load, row = 0, []
for x in range(8):
    load += d[x]; row.append(load)
print('diff array :', d)
print('load by stop:', row)

# seeded random cross-check
for _ in range(3000):
    trips = []
    for _ in range(random.randint(1, 8)):
        a = random.randint(0, 999); b = random.randint(a + 1, min(1000, a + random.randint(1, 30)))
        trips.append([random.randint(1, 100), a, b])
    cap = random.randint(1, 400)
    assert car_pool(cap, trips) == brute(cap, trips)
print('random cross-check ok: 3000 cases (stops 0..1000)')

# exhaustive on a tiny world: 4 stops, every multiset of up to 3 trips with 1..2 passengers
import itertools
all_trips = [[p, a, b] for p in (1, 2) for a in range(4) for b in range(a + 1, 4)]
count = 0
for r in (1, 2, 3):
    for trips in itertools.combinations_with_replacement(all_trips, r):
        for cap in (1, 2, 3, 5):
            assert car_pool(cap, list(trips), 4) == brute(cap, list(trips), 4)
            count += 1
print('exhaustive tiny-world ok:', count, 'cases')

# boundary: a trip ending at x and one starting at x never overlap at x
assert car_pool(2, [[2, 0, 5], [2, 5, 9]]) == [True, 2, 0]
# max end 1000 uses d[1000]; the last stop counted is 999 (end is exclusive)
assert car_pool(1, [[1, 0, 1000]]) == [True, 1, 0]
# max load: 1000 trips of 100 passengers all over 0..1000 -> 100000 = capacity bound
trips = [[100, 0, 1000]] * 1000
assert car_pool(10**5, trips) == [True, 100000, 0] and car_pool(99999, trips)[0] is False
# work: difference array does len(trips) + 1001 steps, the direct method len(trips) * 1001 checks
print('work: diff array', 1000 + 1001, 'steps vs direct', 1000 * 1001, 'trip-stop checks (counted from the formula)')
print('edge asserts ok')
```

**Output (my run):**
```
4 [[2, 1, 5], [3, 3, 7]] -> [False, 5, 3]
5 [[2, 1, 5], [3, 3, 7]] -> [True, 5, 3]
3 [[2, 1, 5], [3, 5, 7]] -> [True, 3, 5]
diff array : [0, 2, 0, 3, 0, -2, 0, -3]
load by stop: [0, 2, 2, 5, 5, 3, 3, 0]
random cross-check ok: 3000 cases (stops 0..1000)
exhaustive tiny-world ok: 1816 cases
work: diff array 2001 steps vs direct 1001000 trip-stop checks (counted from the formula)
edge asserts ok
```

**Edge cases:**
- A trip ending at x and another starting at x never overlap: `[[2,0,5],[2,5,9]]` gives peak 2, not 4.
- The last valid stop is 999 for a trip with end 1000 (end is exclusive), and `d[1000]` must exist.
- Ties for the peak: report the smallest stop, which the strict `>` gives.
- Peak equal to capacity is fine (`<=`): example 2 returns True.
- Largest input: 1000 trips of 100 passengers over 0..1000 gives 100000, equal to the largest capacity.

**Follow-ups:**
- *Corporate Flight Bookings?* The same, but the ranges are 1-indexed and inclusive, so subtract at `last + 1` instead of at `end`.
- *Huge coordinates?* Sort the events (start, +p) and (end, -p) and sweep; O(T log T). Part 8 covers the interval version.
- *Many point queries after many updates?* Interleaved updates and queries need a Fenwick tree (Part 14).

**Common mistakes:**
- Subtracting at `end + 1`, which counts the passengers at the stop where they should already have left.
- Using `>=` for the peak and reporting the last stop of the peak instead of the first.
- Allocating only 1000 slots and crashing on `end = 1000`.
- Sorting or merging trips first. The difference array does not need sorted input.

### Q24 ⭐⭐ 🟡 Matrix block sum. `mat` is an m x n list of lists of integers (1 <= m, n <= 100, |value| <= 100) and `k` is an integer with 0 <= k <= 100. Return an m x n matrix `ans` where `ans[i][j]` is the sum of `mat[r][c]` over all cells with i - k <= r <= i + k and j - k <= c <= j + k that lie inside the matrix (the square is clipped at the borders). Use a 2D prefix-sum table so each cell costs O(1) after an O(m * n) build, clamping the four corners with `max(0, i - k)` and `min(m - 1, i + k)` (and the same for columns). Explain why the clamping is correct, and compare with the O(m * n * k^2) direct method. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the direct double loop over the clipped square on small inputs. Example: mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], k=1 -> [[12, 21, 16], [27, 45, 33], [24, 39, 28]]; mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], k=2 -> [[45, 45, 45], [45, 45, 45], [45, 45, 45]]; mat=[[5]], k=3 -> [[5]]; mat=[[1, 2], [3, 4]], k=0 -> [[1, 2], [3, 4]].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** 2D prefix sums. One table lets you read any rectangle sum with four lookups.

**Say this first (1 line):** "Build `P` where `P[i][j]` is the sum of the top-left i x j block; each answer cell is a rectangle with clamped corners, read with inclusion-exclusion in O(1)."

**Brute force:** For each cell, loop over the clipped (2k+1) x (2k+1) square and add. O(m * n * k^2) in the worst case. For a 100 x 100 matrix with k = 100 the clipped squares are the whole matrix: 100,000,000 reads (computed from the formula in the program, not run).

**Optimal:**
- `P` has size (m+1) x (n+1), with a zero first row and column. `P[i+1][j+1] = mat[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]`. The last term removes the overlap that was added twice.
- For cell (i, j): `r1 = max(0, i-k)`, `r2 = min(m-1, i+k)`, `c1 = max(0, j-k)`, `c2 = min(n-1, j+k)`.
- Sum = `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`.
- Why clamping is right: the problem says cells outside the matrix do not exist, so the sum over the square equals the sum over the square intersected with the matrix. That intersection is still a rectangle, whose corners are exactly the clamped values. Without clamping you would index outside the table, or, with negative indexes, silently read from the other end in Python.

**Complexity:** Build O(m * n), queries O(m * n) (4 lookups each). Total O(m * n), space O(m * n) for `P` and for the answer. For the 100 x 100 case with k = 10 the direct method reads 3,960,100 cells, the table 40,000 (the program prints these).

**Dry run:** `[[1,2,3],[4,5,6],[7,8,9]]`, k = 1. Prefix table: `[[0,0,0,0],[0,1,3,6],[0,5,12,21],[0,12,27,45]]`. Cell (0,0): rows 0..1, columns 0..1, so `P[2][2] - P[0][2] - P[2][0] + P[0][0] = 12 - 0 - 0 + 0 = 12`. That is 1 + 2 + 4 + 5. Center cell (1,1): rows 0..2, columns 0..2, so `45 - 0 - 0 + 0 = 45`.

**Code:**
```python
import itertools
import random

random.seed(2401)

def block_sum(mat, k):
    m, n = len(mat), len(mat[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]        # P[i][j] = sum of mat[:i][:j]
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = mat[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            r1, r2 = max(0, i - k), min(m - 1, i + k)      # clip to the matrix
            c1, c2 = max(0, j - k), min(n - 1, j + k)
            row.append(P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1])
        out.append(row)
    return out

def brute(mat, k, count=None):
    m, n = len(mat), len(mat[0])
    visits = 0
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            s = 0
            for r in range(max(0, i - k), min(m - 1, i + k) + 1):
                for c in range(max(0, j - k), min(n - 1, j + k) + 1):
                    s += mat[r][c]; visits += 1
            row.append(s)
        out.append(row)
    if count is not None:
        count.append(visits)
    return out

G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
examples = [(G, 1, [[12, 21, 16], [27, 45, 33], [24, 39, 28]]),
            (G, 2, [[45] * 3] * 3), ([[5]], 3, [[5]]), ([[1, 2], [3, 4]], 0, [[1, 2], [3, 4]])]
for mat, k, want in examples:
    assert block_sum(mat, k) == want == brute(mat, k)
    print('k =', k, mat, '->', block_sum(mat, k))

# dry run: the prefix table of G and the cell (0, 0) with k = 1
P = [[0] * 4 for _ in range(4)]
for i in range(3):
    for j in range(3):
        P[i + 1][j + 1] = G[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
print('prefix table:', P)
print('cell (0,0), k=1: rows 0..1, cols 0..1 ->', P[2][2], '-', P[0][2], '-', P[2][0], '+', P[0][0], '=', P[2][2] - P[0][2] - P[2][0] + P[0][0])

# seeded random cross-check
for _ in range(2000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    k = random.randint(0, 7)
    assert block_sum(mat, k) == brute(mat, k)
print('random cross-check ok: 2000 cases')

# exhaustive: every 2 x 3 matrix over {-1,0,1} and k = 0..3
cnt = 0
for cells in itertools.product((-1, 0, 1), repeat=6):
    mat = [list(cells[:3]), list(cells[3:])]
    for k in range(4):
        assert block_sum(mat, k) == brute(mat, k); cnt += 1
print('exhaustive 2x3 ok:', cnt, 'cases')

# cost: cell reads of the direct method (from the clipped square sizes) versus 4 table reads per cell
def clipped_cells(m, n, k):          # number of cell reads the direct method makes
    rows = sum(min(m - 1, i + k) - max(0, i - k) + 1 for i in range(m))
    cols = sum(min(n - 1, j + k) - max(0, j - k) + 1 for j in range(n))
    return rows * cols
for m, n, k in [(100, 100, 1), (100, 100, 10), (100, 100, 100)]:
    print(f'{m}x{n}, k={k}: direct reads {clipped_cells(m, n, k)} cells; prefix table: 4 reads per cell = {4 * m * n}')
mat = [[random.randint(-5, 5) for _ in range(7)] for _ in range(6)]
v = []
brute(mat, 2, v)
assert v[0] == clipped_cells(6, 7, 2)
big = [[random.randint(-100, 100) for _ in range(100)] for _ in range(100)]
assert block_sum(big, 100) == [[sum(map(sum, big))] * 100] * 100          # whole-matrix sum everywhere
assert block_sum([[7]], 100) == [[7]]
print('edge asserts ok')
```

**Output (my run):**
```
k = 1 [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[12, 21, 16], [27, 45, 33], [24, 39, 28]]
k = 2 [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[45, 45, 45], [45, 45, 45], [45, 45, 45]]
k = 3 [[5]] -> [[5]]
k = 0 [[1, 2], [3, 4]] -> [[1, 2], [3, 4]]
prefix table: [[0, 0, 0, 0], [0, 1, 3, 6], [0, 5, 12, 21], [0, 12, 27, 45]]
cell (0,0), k=1: rows 0..1, cols 0..1 -> 12 - 0 - 0 + 0 = 12
random cross-check ok: 2000 cases
exhaustive 2x3 ok: 2916 cases
100x100, k=1: direct reads 88804 cells; prefix table: 4 reads per cell = 40000
100x100, k=10: direct reads 3960100 cells; prefix table: 4 reads per cell = 40000
100x100, k=100: direct reads 100000000 cells; prefix table: 4 reads per cell = 40000
edge asserts ok
```

**Edge cases:**
- k = 0: each cell equals itself.
- k larger than the matrix: every answer is the total sum (checked at 100 x 100, k = 100).
- 1 x 1, 1 x n and m x 1 matrices: clamping handles them.
- Negative values: nothing assumes the sums are non-negative.
- Values up to 100 over 10^4 cells: at most 10^6 in magnitude, no overflow in Python (and fits int32 in other languages).

**Follow-ups:**
- *Region queries on a fixed matrix?* Same table; each query is 4 lookups (matrix region sum).
- *Point updates between queries?* Rebuild is O(m * n); use a 2D Fenwick tree (Part 14) or per-row prefix sums (Q40).
- *Add a value over a rectangle many times?* Use a 2D difference array and one 2D prefix pass at the end.

**Common mistakes:**
- Forgetting to add back `P[r1][c1]` (the corner subtracted twice).
- Mixing inclusive and exclusive bounds: with the (m+1) x (n+1) table the upper indexes are `r2+1`, `c2+1`.
- Clamping only one side (`max` but not `min`).
- Building `P` without the zero padding row and column, which forces special cases for the first row and column.

### Q25 ⭐⭐ 🟡 Set matrix zeroes in O(1) extra space. `matrix` is an m x n list of lists of integers (1 <= m, n <= 200). If a cell is 0, set its whole row and whole column to 0. Modify the matrix in place and also return it, using O(1) extra space beyond the matrix: first remember in two booleans whether row 0 and column 0 contain a zero, then use row 0 and column 0 as the marker arrays for the other rows and columns, then zero the inner cells from the markers, and finally zero row 0 and column 0 from the two booleans. Part 1 Q31 states this problem at concept level; here you must write it fully and explain the trap: a version that marks `matrix[i][0] = 0` and `matrix[0][j] = 0` for every zero at (i, j) and later zeroes row 0 and column 0 whenever `matrix[0][0] == 0` (instead of using two saved booleans) gives a wrong result for 42 of the 512 binary 3 x 3 matrices (it cannot tell whether row 0 and column 0 held a zero themselves or were only marked). Give one failing 3 x 3 input of that version and say what it returns. Compare with the O(m + n) extra-space version that keeps two sets. In the answer include a dry run on the first example and a seeded random cross-check of your solution against two sets of zero rows and zero columns on small inputs. Example: matrix=[[1, 1, 1], [1, 0, 1], [1, 1, 1]] -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]]; matrix=[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]] -> [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]; matrix=[[1, 2], [3, 4]] -> [[1, 2], [3, 4]]; matrix=[[1, 0]] -> [[0, 0]].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** In-place matrix with the first row and first column reused as marker arrays. This trades the O(m + n) sets for O(1) extra space.

**Say this first (1 line):** "Save two booleans first (does row 0 or column 0 hold a zero?), then use row 0 and column 0 as flags for the rest, zero the inner cells, and last fix row 0 and column 0 from the booleans."

**Brute force:** Two sets: rows that contain a zero and columns that contain a zero. A second pass sets a cell to 0 if its row or column is in a set. O(m * n) time, O(m + n) space. Even simpler: copy the matrix. O(m * n) space. The two-set version is the oracle here.

**Optimal:**
1. `row0 = any zero in matrix[0]`, `col0 = any zero in matrix[i][0]`. Do this before touching anything.
2. For i, j from 1: if `matrix[i][j] == 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`.
3. For i, j from 1: if `matrix[i][0] == 0` or `matrix[0][j] == 0`, set `matrix[i][j] = 0`.
4. If `row0`, zero all of row 0. If `col0`, zero all of column 0.

Invariant: after step 2 each marker cell `matrix[i][0]` or `matrix[0][j]` is 0 if and only if row i or column j needs clearing, as far as the inner cells are concerned. The original zeros in row 0 and column 0 are not lost because step 1 saved them in two booleans.

The trap: if you mark for every zero (including zeros that were in row 0 or column 0 already) and later look at `matrix[0][0] == 0` to decide about row 0 and column 0, you cannot tell "row 0 had a zero" from "I wrote a marker into row 0". That version is wrong on 42 of the 512 binary 3 x 3 matrices (counted exhaustively below). One failing input: `[[1,1,1],[0,1,1],[1,0,1]]`. Zeros are at (1,0) and (2,1). The correct result is `[[0,0,1],[0,0,0],[0,0,0]]`. The naive code marks `matrix[0][0] = 0` while handling the zero at (1,0), and then wipes the whole of row 0 and returns all zeros.

**Complexity:** Time O(m * n): a constant number of passes. Extra space O(1): two booleans. The two-set version takes O(m + n) extra space.

**Dry run:** `[[1,1,1],[1,0,1],[1,1,1]]`. Row 0 has no zero, column 0 has no zero. The only inner zero is at (1,1), so mark `matrix[1][0] = 0` and `matrix[0][1] = 0`: `[[1,0,1],[0,0,1],[1,1,1]]`. Inner pass: (1,2) has marker `matrix[1][0] = 0` so it becomes 0, (2,1) has marker `matrix[0][1] = 0` so it becomes 0. Result `[[1,0,1],[0,0,0],[1,0,1]]`. Both flags are False, so nothing else changes. The program prints the stages.

**Code:**
```python
import itertools
import random

random.seed(2501)

def set_zeroes(matrix):
    """O(1) extra space: row 0 and column 0 are the marker arrays."""
    m, n = len(matrix), len(matrix[0])
    row0 = any(matrix[0][j] == 0 for j in range(n))      # saved BEFORE markers overwrite row 0
    col0 = any(matrix[i][0] == 0 for i in range(m))      # saved BEFORE markers overwrite col 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:
        for j in range(n): matrix[0][j] = 0
    if col0:
        for i in range(m): matrix[i][0] = 0
    return matrix

def naive_markers(matrix):
    """The TRAP: marks for every zero (including row 0 / col 0 ones), then decides row 0 and col 0 from matrix[0][0]."""
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if matrix[0][0] == 0:
        for j in range(n): matrix[0][j] = 0
        for i in range(m): matrix[i][0] = 0
    return matrix

def two_sets(matrix):
    """O(m + n) extra space oracle: collect zero rows and columns, then write."""
    rows = {i for i, r in enumerate(matrix) if 0 in r}
    cols = {j for r in matrix for j, v in enumerate(r) if v == 0}
    return [[0 if i in rows or j in cols else v for j, v in enumerate(r)] for i, r in enumerate(matrix)]

def cp(x): return [r[:] for r in x]

examples = [([[1, 1, 1], [1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
            ([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
            ([[1, 2], [3, 4]], [[1, 2], [3, 4]]), ([[1, 0]], [[0, 0]])]
for mat, want in examples:
    a = cp(mat); r = set_zeroes(a)
    assert r is a and a == want == two_sets(mat)           # in place AND returned
    print(mat, '->', a)

# dry run: example 1, stage by stage
mat = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print('row0 has zero:', any(v == 0 for v in mat[0]), ' col0 has zero:', any(r[0] == 0 for r in mat))
mark = cp(mat)
mark[1][0] = mark[0][1] = 0                  # the only inner zero is (1,1): mark its row and column
print('after marking :', mark)
for i in range(1, 3):
    for j in range(1, 3):
        if mark[i][0] == 0 or mark[0][j] == 0: mark[i][j] = 0
print('after inner pass:', mark, '(row 0 and col 0 hold the zeros their markers made; both saved flags are False, so nothing more to do)')

# seeded random cross-check against the two-set version (values 0..3, zeros common)
for _ in range(3000):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.choice([0, 0, 1, 2, 3]) for _ in range(n)] for _ in range(m)]
    a = cp(mat)
    assert set_zeroes(a) == two_sets(mat)
print('random cross-check ok: 3000 cases')

# exhaustive over every binary matrix of shapes up to 3 x 3 (and 1 x n, m x 1 up to 6)
shapes = [(m, n) for m in range(1, 4) for n in range(1, 4)] + [(1, 6), (6, 1), (2, 5), (5, 2)]
total = 0
wrong = 0
first_bad = None
for m, n in shapes:
    for cells in itertools.product((0, 1), repeat=m * n):
        mat = [list(cells[i * n:(i + 1) * n]) for i in range(m)]
        want = two_sets(mat)
        assert set_zeroes(cp(mat)) == want
        total += 1
        if (m, n) == (3, 3):
            if naive_markers(cp(mat)) != want:
                wrong += 1
                if first_bad is None or sum(map(sum, mat)) > sum(map(sum, first_bad)):
                    first_bad = mat
print('correct version exhaustive ok:', total, 'binary matrices over', len(shapes), 'shapes')
print('naive marker version wrong on', wrong, 'of 512 binary 3x3 matrices')
bad = [[1, 1, 1], [0, 1, 1], [1, 0, 1]]
print('failing input :', bad)
print('naive returns :', naive_markers(cp(bad)))
print('correct       :', two_sets(bad))
assert wrong == 42 and naive_markers(cp(bad)) != two_sets(bad)

# edge asserts: zero at the corner, whole zero matrix, single cell, non-binary values stay
assert set_zeroes([[0]]) == [[0]] and set_zeroes([[7]]) == [[7]]
assert set_zeroes([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
assert set_zeroes([[5, 6, 7], [8, 0, 9]]) == [[5, 0, 7], [0, 0, 0]]
big = [[1] * 200 for _ in range(200)]; big[199][199] = 0
r = set_zeroes(big)
assert sum(map(sum, r)) == 199 * 199
print('edge asserts ok')
```

**Output (my run):**
```
[[1, 1, 1], [1, 0, 1], [1, 1, 1]] -> [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]] -> [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
[[1, 2], [3, 4]] -> [[1, 2], [3, 4]]
[[1, 0]] -> [[0, 0]]
row0 has zero: False  col0 has zero: False
after marking : [[1, 0, 1], [0, 0, 1], [1, 1, 1]]
after inner pass: [[1, 0, 1], [0, 0, 0], [1, 0, 1]] (row 0 and col 0 hold the zeros their markers made; both saved flags are False, so nothing more to do)
random cross-check ok: 3000 cases
correct version exhaustive ok: 2858 binary matrices over 13 shapes
naive marker version wrong on 42 of 512 binary 3x3 matrices
failing input : [[1, 1, 1], [0, 1, 1], [1, 0, 1]]
naive returns : [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
correct       : [[0, 0, 1], [0, 0, 0], [0, 0, 0]]
edge asserts ok
```

**Edge cases:**
- 1 x n and m x 1: the inner loops are empty and only the flags work (`[[1,0]]` gives `[[0,0]]`).
- A zero at (0,0): both flags become True.
- Zero only in row 0: only the columns of those zeros are cleared, and row 0 itself.
- All zeros and non-binary values (the real test uses any integers): only the zero test matters.
- Return the same list object (the program asserts `r is a`).
- 200 x 200 with one zero in the corner: result keeps 199 x 199 cells.

**Follow-ups:**
- *Why not use a sentinel like None or -1?* It works for simple values but needs a value that cannot appear; the marker trick has no such assumption.
- *Time cost compared with the two sets?* Same O(m * n); you save only the memory.
- *Part 1 Q31 is the concept version; why does the order of steps matter here?* Because the markers live inside the data, anything that reads them before the saved booleans are applied sees a polluted state.

**Common mistakes:**
- Clearing row 0 or column 0 before the inner cells are processed (the markers disappear).
- Starting the inner loops at 0 instead of 1.
- Using `matrix[0][0]` for both row 0 and column 0 (the 42-of-512 bug above).
- Returning a new matrix when the problem says modify in place.

### Q26 ⭐⭐ 🟡 Conway's Game of Life in place. `board` is an m x n list of lists of 0 (dead) and 1 (live), 1 <= m, n <= 30, and `generations` is an integer with 1 <= generations <= 10. Advance the board that many generations simultaneously (all cells change at once) and return the final board; modify `board` in place and return it. Each cell has up to 8 neighbours (cells beyond the border count as dead); a live cell with 2 or 3 live neighbours survives, a dead cell with exactly 3 live neighbours becomes live, every other cell is dead in the next generation. Use O(1) extra space per generation by encoding each cell in two bits (bit 0 = current state, bit 1 = next state, so you can still read the old state of cells you already updated), then shift every cell right by one. Explain why overwriting cells in a single pass without such an encoding gives wrong answers (later cells would see updated neighbours), and say what changes on an unbounded board (the live region can grow, so you would store live cells in a set). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a copy-based version that counts neighbours of live cells in a Counter on small inputs. Example: board=[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]], generations=1 -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]; board=[[1, 1], [1, 0]], generations=1 -> [[1, 1], [1, 1]]; board=[[0, 0, 0], [1, 1, 1], [0, 0, 0]], generations=2 -> [[0, 0, 0], [1, 1, 1], [0, 0, 0]].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** Simultaneous in-place update by encoding old and new state in one cell (two bits).

**Say this first (1 line):** "Bit 0 is the old state, bit 1 is the new state; count neighbours with `& 1`, write the new state with `|= 2`, and shift everything right by one at the end."

**Brute force:** Copy the board, compute the next board from the copy. O(m * n) time and O(m * n) space per generation. A second oracle keeps only the live cells and counts neighbours of live cells in a `Counter`: O(live cells) per generation, and it is easy to extend to an unbounded board.

**Optimal:**
- A cell holds 0 to 3. `value & 1` is the state in the current generation, `value >> 1` the state in the next.
- For each cell count live neighbours with `board[x][y] & 1` (the old state, even for cells already marked). If `live == 3`, or the cell is alive and `live == 2`, do `board[i][j] |= 2`.
- After the whole board is marked, do `board[i][j] >>= 1` for every cell. Dead-to-dead (0) and live-to-dead (1) both become 0, dead-to-live (2) and live-to-live (3) become 1.
- Repeat for each generation.
- Why a single pass without encoding fails: when you write the new value of a cell, the cells after it (to the right and below) read that new value as a neighbour. Those cells then count the wrong number of live neighbours. The program counts it: the plain overwrite is wrong on 417 of the 512 3 x 3 boards, for example `[[0,0,0],[0,0,0],[1,1,1]]` (it returns `[[0,0,0],[0,1,1],[1,0,1]]`, right is `[[0,0,0],[0,1,0],[0,1,0]]`).
- Unbounded board: the live region can grow, so a fixed array does not work. Store the live cells in a set and count neighbours in a `Counter`, as the oracle does. A glider moves one cell diagonally every 4 generations (checked in the program); on the bounded 4 x 4 board it crashes into the wall and ends as a 2 x 2 block.

**Complexity:** Per generation O(m * n * 8) = O(m * n) time, O(1) extra space. For `g` generations O(g * m * n); the maximum is 10 * 30 * 30 = 9000 cell updates, each looking at 8 neighbours.

**Dry run:** First example, 4 x 3. Encoded after marking: `[[0,1,0],[2,0,3],[1,3,3],[0,2,0]]`. Cell (1,2): old 1 with three live neighbours ((0,1), (2,1), (2,2)), so it survives, and the `3` is old 1 plus new 1. Cell (0,1): old 1, only one live neighbour, so it dies (stays `1`, new bit 0). After `>> 1`: `[[0,0,0],[1,0,1],[0,1,1],[0,1,0]]`, which matches.

**Code:**
```python
import collections
import itertools
import random

random.seed(2601)

def life(board, generations):
    m, n = len(board), len(board[0])
    for _ in range(generations):
        for i in range(m):
            for j in range(n):
                live = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n:
                            live += board[i + di][j + dj] & 1          # bit 0 = OLD state
                if live == 3 or (board[i][j] & 1 and live == 2):
                    board[i][j] |= 2                                   # bit 1 = NEW state
        for i in range(m):
            for j in range(n):
                board[i][j] >>= 1                                      # new becomes current
    return board

def counter_version(board, generations):
    m, n = len(board), len(board[0])
    cells = {(i, j) for i in range(m) for j in range(n) if board[i][j]}
    for _ in range(generations):
        cnt = collections.Counter((i + di, j + dj) for i, j in cells
                                  for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj)
        cells = {p for p, c in cnt.items() if 0 <= p[0] < m and 0 <= p[1] < n and (c == 3 or (c == 2 and p in cells))}
    return [[1 if (i, j) in cells else 0 for j in range(n)] for i in range(m)]

def buggy_single_pass(board):
    """Overwrite in place with no encoding: later cells see already-updated neighbours."""
    m, n = len(board), len(board[0])
    for i in range(m):
        for j in range(n):
            live = sum(board[i + di][j + dj] for di in (-1, 0, 1) for dj in (-1, 0, 1)
                       if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n)
            board[i][j] = 1 if live == 3 or (board[i][j] and live == 2) else 0
    return board

def cp(x): return [r[:] for r in x]

examples = [([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]], 1, [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]),
            ([[1, 1], [1, 0]], 1, [[1, 1], [1, 1]]),
            ([[0, 0, 0], [1, 1, 1], [0, 0, 0]], 2, [[0, 0, 0], [1, 1, 1], [0, 0, 0]])]
for b, g, want in examples:
    a = cp(b); r = life(a, g)
    assert r is a and a == want == counter_version(b, g)
    print(b, 'x', g, '->', a)

# dry run on the first example: encoded board after the marking pass of generation 1
b = cp(examples[0][0]); m, n = 4, 3
for i in range(m):
    for j in range(n):
        live = sum(b[i + di][j + dj] & 1 for di in (-1, 0, 1) for dj in (-1, 0, 1)
                   if (di or dj) and 0 <= i + di < m and 0 <= j + dj < n)
        if live == 3 or (b[i][j] & 1 and live == 2): b[i][j] |= 2
print('encoded (value = old + 2*new):', b)
print('after >> 1                   :', [[v >> 1 for v in r] for r in b])

# seeded random cross-check
for _ in range(1500):
    m, n = random.randint(1, 7), random.randint(1, 7)
    b = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
    g = random.randint(1, 6)
    assert life(cp(b), g) == counter_version(b, g)
print('random cross-check ok: 1500 cases')

# exhaustive: every 3 x 3 board, 1 and 2 generations; every 2 x 4 board, 1 generation
count = 0
for cells in itertools.product((0, 1), repeat=9):
    b = [list(cells[:3]), list(cells[3:6]), list(cells[6:])]
    for g in (1, 2):
        assert life(cp(b), g) == counter_version(b, g); count += 1
for cells in itertools.product((0, 1), repeat=8):
    b = [list(cells[:4]), list(cells[4:])]
    assert life(cp(b), 1) == counter_version(b, 1); count += 1
print('exhaustive ok:', count, 'cases')

# the single-pass bug: how many of the 512 3x3 boards go wrong, and one example
wrong = 0; ex = None
for cells in itertools.product((0, 1), repeat=9):
    b = [list(cells[:3]), list(cells[3:6]), list(cells[6:])]
    if buggy_single_pass(cp(b)) != counter_version(b, 1):
        wrong += 1
        ex = ex or b
print('single-pass overwrite wrong on', wrong, 'of 512 3x3 boards; first:', ex)
print('  buggy:', buggy_single_pass(cp(ex)), ' right:', counter_version(ex, 1))
assert wrong > 0

# unbounded board: the live region grows. A glider on an infinite plane moves (1,1) every 4 generations.
def step_inf(cells):
    cnt = collections.Counter((i + di, j + dj) for i, j in cells for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj)
    return {p for p, c in cnt.items() if c == 3 or (c == 2 and p in cells)}
glider = {(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
g = glider
for _ in range(4): g = step_inf(g)
assert g == {(i + 1, j + 1) for i, j in glider}
print('glider after 4 generations on an unbounded board is shifted by (1, 1): True')
# on a bounded 4x4 board the same glider hits the wall instead
b = [[0] * 4 for _ in range(4)]
for i, j in glider: b[i][j] = 1
print('bounded 4x4 glider after 8 generations:', life(b, 8))

# edge asserts and max size
assert life([[1]], 1) == [[0]] and life([[0]], 3) == [[0]]
assert life([[1, 1], [1, 1]], 10) == [[1, 1], [1, 1]]          # block is stable
big = [[random.randint(0, 1) for _ in range(30)] for _ in range(30)]
assert life(cp(big), 10) == counter_version(big, 10)
print('edge asserts ok')
```

**Output (my run):**
```
[[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]] x 1 -> [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
[[1, 1], [1, 0]] x 1 -> [[1, 1], [1, 1]]
[[0, 0, 0], [1, 1, 1], [0, 0, 0]] x 2 -> [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
encoded (value = old + 2*new): [[0, 1, 0], [2, 0, 3], [1, 3, 3], [0, 2, 0]]
after >> 1                   : [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
random cross-check ok: 1500 cases
exhaustive ok: 1280 cases
single-pass overwrite wrong on 417 of 512 3x3 boards; first: [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
  buggy: [[0, 0, 0], [0, 1, 1], [1, 0, 1]]  right: [[0, 0, 0], [0, 1, 0], [0, 1, 0]]
glider after 4 generations on an unbounded board is shifted by (1, 1): True
bounded 4x4 glider after 8 generations: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
edge asserts ok
```

**Edge cases:**
- Border cells have fewer than 8 neighbours; cells beyond the border count as dead.
- 1 x 1 board: a live cell has 0 neighbours and dies.
- A 2 x 2 block of live cells is stable (10 generations leave it unchanged).
- Oscillators like the blinker return to start after 2 generations (example 3).
- 30 x 30 random board with 10 generations matches the Counter version.

**Follow-ups:**
- *Other encodings?* Use `-1` for live-to-dead and `2` for dead-to-live, then convert at the end. Same idea.
- *Very sparse infinite board?* The set-based version, O(live cells) per generation.
- *Toroidal board?* Use modulo indexes for the neighbours.

**Common mistakes:**
- Reading `board[x][y]` instead of `board[x][y] & 1` for neighbours (the new bit makes the count wrong).
- Shifting inside the cell loop instead of after the whole board is marked.
- Applying the rule to dead cells as "survive with 2 or 3".
- Forgetting that the shift must happen once per generation, not once in total.

### Q27 ⭐⭐ 🟡 Diagonal traverse of a matrix. `mat` is an m x n list of lists of integers (1 <= m, n <= 100). Return all elements by anti-diagonals (cells with equal i + j) alternating direction, starting with the diagonal of the top-left cell going up-right: that diagonal has one cell; the next goes down-left; the next goes up-right again, and so on, finishing at the bottom-right cell. For a 3 x 3 matrix [[1,2,3],[4,5,6],[7,8,9]] the order is 1, 2, 4, 7, 5, 3, 6, 8, 9. Explain that there are m + n - 1 anti-diagonals, that i + j is constant on each, and give two O(m * n) ways: a pointer walk with direction flips at the borders (the tricky part is the order of the border checks in the corners) and grouping by i + j then reversing every second group (O(m * n) extra space). Say what changes if you want the diagonals with constant i - j instead. In the answer include a dry run on the first example and a seeded random cross-check of your solution against grouping by i + j and reversing alternate groups on small inputs. Example: mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 4, 7, 5, 3, 6, 8, 9]; mat=[[1, 2], [3, 4]] -> [1, 2, 3, 4]; mat=[[1, 2, 3, 4]] -> [1, 2, 3, 4]; mat=[[1], [2], [3]] -> [1, 2, 3].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** Matrix traversal by anti-diagonals. All cells on one diagonal share `i + j`.

**Say this first (1 line):** "There are m + n - 1 diagonals; walk them with a direction flag and check the right and bottom borders before the top and left ones."

**Brute force / second method:** Put every cell into a bucket `groups[i + j]` (rows are visited top to bottom, so each bucket is in down-left order), then reverse the buckets with an even index (they go up-right). O(m * n) time and O(m * n) extra space. It is the oracle.

**Optimal (pointer walk):**
- Start at (0,0) going up. Emit `mat[i][j]`, then move:
  - Going up: if `j == n-1` move down one row (`i += 1`) and flip; else if `i == 0` move right (`j += 1`) and flip; else `i -= 1, j += 1`.
  - Going down: if `i == m-1` move right and flip; else if `j == 0` move down and flip; else `i += 1, j -= 1`.
- The order of the checks matters in the corners. At the top-right corner both `i == 0` and `j == n-1` are true while going up. The right border must win and move down, because moving right would leave the matrix. The same holds at the bottom-left corner going down: the bottom border (`i == m-1`) must come first. The program tests the swapped order and it walks off the grid (or returns nothing valid) on 33 of the 49 shapes up to 7 x 7.
- Total steps: exactly m * n.

**Complexity:** Time O(m * n), each cell is emitted once and each step is O(1). Space O(1) extra for the walk (the output is O(m * n)). The grouping method uses O(m * n) extra.

**Dry run:** 3 x 3. (0,0)=1 up, hits top border so go right: (0,1)=2 going down, left border not reached so (1,0)=4, then left border, go down: (2,0)=7 going up. (1,1)=5, (0,2)=3. At (0,2) the right border wins: go down to (1,2)=6 going down. (2,1)=8, then the bottom border: (2,2)=9. Order 1, 2, 4, 7, 5, 3, 6, 8, 9. The program prints the position and direction at every step.

**Code:**
```python
import itertools
import random

random.seed(2701)

def diag_walk(mat):
    m, n = len(mat), len(mat[0])
    i = j = 0
    up = True
    out = []
    for _ in range(m * n):
        out.append(mat[i][j])
        if up:
            if j == n - 1:   i += 1; up = False       # right border FIRST (this also covers the top-right corner)
            elif i == 0:     j += 1; up = False
            else:            i -= 1; j += 1
        else:
            if i == m - 1:   j += 1; up = True        # bottom border FIRST (covers the bottom-left corner)
            elif j == 0:     i += 1; up = True
            else:            i += 1; j -= 1
    return out

def group_by_sum(mat):
    m, n = len(mat), len(mat[0])
    groups = [[] for _ in range(m + n - 1)]
    for i in range(m):
        for j in range(n):
            groups[i + j].append(mat[i][j])          # row order: top to bottom = down-left direction
    out = []
    for s, g in enumerate(groups):
        out.extend(g[::-1] if s % 2 == 0 else g)     # even sums go up-right: reverse
    return out

def wrong_order(mat):
    """Same walk but checks the top/left border BEFORE the right/bottom border."""
    m, n = len(mat), len(mat[0])
    i = j = 0; up = True; out = []
    for _ in range(m * n):
        if not (0 <= i < m and 0 <= j < n):
            return None                              # walked off the grid
        out.append(mat[i][j])
        if up:
            if i == 0:       j += 1; up = False
            elif j == n - 1: i += 1; up = False
            else:            i -= 1; j += 1
        else:
            if j == 0:       i += 1; up = True
            elif i == m - 1: j += 1; up = True
            else:            i += 1; j -= 1
    return out

G = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
examples = [(G, [1, 2, 4, 7, 5, 3, 6, 8, 9]), ([[1, 2], [3, 4]], [1, 2, 3, 4]),
            ([[1, 2, 3, 4]], [1, 2, 3, 4]), ([[1], [2], [3]], [1, 2, 3])]
for mat, want in examples:
    assert diag_walk(mat) == want == group_by_sum(mat)
    print(mat, '->', diag_walk(mat))

# dry run on the 3 x 3: position, direction, and which rule fired
i = j = 0; up = True; trace = []
for _ in range(9):
    trace.append(f'({i},{j})={G[i][j]}{"^" if up else "v"}')
    if up:
        if j == 2: i += 1; up = False
        elif i == 0: j += 1; up = False
        else: i -= 1; j += 1
    else:
        if i == 2: j += 1; up = True
        elif j == 0: i += 1; up = True
        else: i += 1; j -= 1
print(' '.join(trace))

# seeded random cross-check
for _ in range(2000):
    m, n = random.randint(1, 8), random.randint(1, 8)
    mat = [[random.randint(-50, 50) for _ in range(n)] for _ in range(m)]
    assert diag_walk(mat) == group_by_sum(mat)
print('random cross-check ok: 2000 cases')

# exhaustive over all shapes up to 7 x 7 using distinct labels (so any wrong order shows)
for m in range(1, 8):
    for n in range(1, 8):
        mat = [[i * n + j for j in range(n)] for i in range(m)]
        out = diag_walk(mat)
        assert out == group_by_sum(mat) and sorted(out) == list(range(m * n))
        assert out[0] == mat[0][0] and out[-1] == mat[m - 1][n - 1]
print('all shapes 1..7 x 1..7: permutation, starts top-left, ends bottom-right')

# the corner-order trap: how many shapes break when the border checks are in the wrong order
broken = [(m, n) for m in range(1, 8) for n in range(1, 8)
          if wrong_order([[i * n + j for j in range(n)] for i in range(m)]) != diag_walk([[i * n + j for j in range(n)] for i in range(m)])]
print('wrong check order breaks', len(broken), 'of 49 shapes, e.g.', broken[:4])
print('  wrong_order on the 3x3 ->', wrong_order(G))

# variant: constant i - j (main-direction diagonals), top-right start going down-right
def by_difference(mat):
    m, n = len(mat), len(mat[0])
    groups = {}
    for i in range(m):
        for j in range(n):
            groups.setdefault(j - i, []).append(mat[i][j])      # j - i from n-1 down to -(m-1)
    return [groups[k] for k in range(n - 1, -m, -1)]
print('i - j diagonals of the 3x3:', by_difference(G), '(count m + n - 1 =', 3 + 3 - 1, ')')
assert [len(g) for g in by_difference(G)] == [1, 2, 3, 2, 1]
assert diag_walk([[9]]) == [9]
big = [[i * 100 + j for j in range(100)] for i in range(100)]
assert len(diag_walk(big)) == 10000 and diag_walk(big) == group_by_sum(big)
print('edge asserts ok')
```

**Output (my run):**
```
[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 4, 7, 5, 3, 6, 8, 9]
[[1, 2], [3, 4]] -> [1, 2, 3, 4]
[[1, 2, 3, 4]] -> [1, 2, 3, 4]
[[1], [2], [3]] -> [1, 2, 3]
(0,0)=1^ (0,1)=2v (1,0)=4v (2,0)=7^ (1,1)=5^ (0,2)=3^ (1,2)=6v (2,1)=8v (2,2)=9^
random cross-check ok: 2000 cases
all shapes 1..7 x 1..7: permutation, starts top-left, ends bottom-right
wrong check order breaks 33 of 49 shapes, e.g. [(2, 1), (2, 2), (2, 3), (2, 4)]
  wrong_order on the 3x3 -> None
i - j diagonals of the 3x3: [[3], [2, 6], [1, 5, 9], [4, 8], [7]] (count m + n - 1 = 5 )
edge asserts ok
```

**Edge cases:**
- 1 x n: every step hits the top border going up, so the walk goes right one cell at a time: `[1,2,3,4]`.
- m x 1: the right border (`j == n-1 == 0`) fires first and moves down: `[1,2,3]`.
- 1 x 1: one emit, the final move is ignored.
- Non-square shapes: the diagonals grow, stay flat, then shrink; `m + n - 1` diagonals either way.

**Follow-ups:**
- *Diagonals with constant `i - j`?* Group by `j - i`, which runs from `n-1` down to `-(m-1)`. For the 3 x 3 you get `[3], [2, 6], [1, 5, 9], [4, 8], [7]` (printed). The count is the same, `m + n - 1`.
- *Zig-zag only the main-direction diagonals?* No direction flips are needed.
- *Spiral order?* Layer by layer with four bounds (the same border-check care).

**Common mistakes:**
- Checking `i == 0` before `j == n-1` when going up (or `j == 0` before `i == m-1` when going down).
- Moving after the last cell and indexing out of range (guard with a count of m * n, not a bounds check).
- Reversing the wrong parity of groups in the bucket method: even `i + j` goes up-right and is reversed.

### Q28 ⭐⭐ 🟡 Prime factorisation by trial division. `nums` has 1 to 200 integers with 2 <= value <= 10^12. For each value n return `[factors, divisors, steps]`: `factors` is the list of [prime, exponent] pairs in increasing prime order; `divisors` is the number of positive divisors of n (the product of (exponent + 1)); `steps` is the number of iterations of this loop: `m = n; d = 2`, then `while d * d <= m:` count one step, divide out d completely if it divides m, and do `d += 1`; after the loop, if m > 1 it is a prime factor with exponent 1. Explain why the loop may stop at d * d <= m (the leftover m is then prime), why the worst case is a prime n near 10^12 with about 10^6 steps, why d never needs to skip composites for correctness, and how a smallest-prime-factor sieve answers many queries below 10^6 in O(log n) each after one O(n log log n) build. In the answer include a dry run on the first example and a seeded random cross-check of your solution against reconstructing n from the factors and an independent divisor count on small inputs. Example: nums=[12, 97, 360, 1024] -> [[[[2, 2], [3, 1]], 6, 1], [[[97, 1]], 2, 8], [[[2, 3], [3, 2], [5, 1]], 24, 2], [[[2, 10]], 11, 1]]; nums=[2] -> [[[[2, 1]], 2, 0]]; nums=[999999999989] -> [[[[999999999989, 1]], 2, 999998]]; nums=[600851475143] -> [[[[71, 1], [839, 1], [1471, 1], [6857, 1]], 16, 1470]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Number theory: trial division up to the square root, shrinking `m` as factors are removed.

**Say this first (1 line):** "Try d = 2, 3, 4, ... while d*d <= m, divide each d out fully, and whatever is left above 1 is a prime."

**Brute force:** Try every d from 2 to n. O(n), which is 10^12 steps for the largest input. The oracle here rebuilds n from the factors and counts the divisors independently (by listing all of 1..n when n is small).

**Optimal:**
- Exactly the loop in the question. `steps` counts each time the `while d * d <= m` test passes.
- Why stopping at `d * d <= m` is enough: if m is composite it has a divisor at most `sqrt(m)`. If no d up to `sqrt(m)` divides m, then m is prime. The leftover is prime with exponent 1.
- Why composites never divide: before d is tried, all smaller primes have been divided out of m completely. A composite d would need a prime factor smaller than itself, which is already gone. The program asserts that every d that divides m is prime for all n up to 30000. So skipping composites would not change the answer, only the step count.
- Divisor count: the product of `(exponent + 1)`.
- Worst case: a prime n near 10^12 never shrinks m, so d runs to `isqrt(n)`. `999999999989` takes 999,998 steps (equal to `isqrt(n) - 1`). The program checks `steps <= isqrt(n) - 1` for all n up to 20000, with equality for every prime. A square of a prime like (10^6 + 3)^2 also costs about 10^6 steps.
- Many queries below 10^6: build the smallest-prime-factor array with a sieve in O(n log log n). Then factorising n takes one array lookup per prime factor, at most about log2(n) = 19 for n up to 10^6, so O(log n) per query. The program builds it and compares with trial division.

**Complexity:** Time O(sqrt(n)) per number, so at most about 10^6 iterations for n up to 10^12, and 200 numbers is roughly 2 * 10^8 loop iterations in the worst case (do not give 200 large primes to a Python loop without thinking). Space O(number of distinct primes). The sandbox ran the single worst number in well under a second (a sandbox timing, not a proof).

**Dry run:** `n = 360`. d = 2: 4 <= 360, step 1, divide out 2^3, m = 45. d = 3: 9 <= 45, step 2, divide out 3^2, m = 5. d = 4: 16 > 5, stop. Leftover m = 5 is prime. Factors `[[2,3],[3,2],[5,1]]`, divisors (3+1)(2+1)(1+1) = 24, steps 2. The program prints this.

**Code:**
```python
import math
import random
import time

random.seed(2801)

def factorise(n):
    """Returns [factors, divisor_count, steps] with the exact loop from the question."""
    m, d, steps = n, 2, 0
    f = []
    while d * d <= m:
        steps += 1
        if m % d == 0:
            e = 0
            while m % d == 0:          # divide out d completely
                m //= d
                e += 1
            f.append([d, e])
        d += 1
    if m > 1:
        f.append([m, 1])               # leftover is prime (exponent 1)
    div = 1
    for p, e in f:
        div *= e + 1
    return [f, div, steps]

def solve(nums):
    return [factorise(n) for n in nums]

def is_prime(n):                       # independent: plain trial division on all d, no tricks
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))

def brute(nums):
    """Oracle: rebuild n from the factors, count divisors by direct enumeration (small n) or from exponents."""
    out = []
    for n in nums:
        f, div, steps = factorise(n)
        prod = 1
        for p, e in f:
            assert is_prime(p) if p < 10**7 else True
            prod *= p ** e
        assert prod == n and [p for p, _ in f] == sorted(p for p, _ in f)
        if n <= 30000:
            assert div == sum(1 for k in range(1, n + 1) if n % k == 0)
        out.append([f, div, steps])
    return out

examples = [([12, 97, 360, 1024], [[[[2, 2], [3, 1]], 6, 1], [[[97, 1]], 2, 8], [[[2, 3], [3, 2], [5, 1]], 24, 2], [[[2, 10]], 11, 1]]),
            ([2], [[[[2, 1]], 2, 0]]),
            ([999999999989], [[[[999999999989, 1]], 2, 999998]]),
            ([600851475143], [[[[71, 1], [839, 1], [1471, 1], [6857, 1]], 16, 1470]])]
for nums, want in examples:
    assert solve(nums) == want == brute(nums)
    print(nums, '->', solve(nums))

# dry run: n = 360 step by step
m, d = 360, 2
while d * d <= m:
    note = ''
    if m % d == 0:
        e = 0
        while m % d == 0: m //= d; e += 1
        note = f'divide out {d}^{e}, m = {m}'
    print(f'  d={d}: d*d={d * d} <= m -> step; {note}')
    d += 1
print(f'  d={d}: d*d={d * d} > m={m} -> stop; leftover m={m}', '(prime, add it)' if m > 1 else '')

# seeded random cross-check, plus every n from 2 to 20000
for _ in range(500):
    nums = [random.randint(2, 10**6) for _ in range(5)]
    assert solve(nums) == brute(nums)
for n in range(2, 20001):
    assert brute([n]) == [factorise(n)]
print('random cross-check ok: 500 lists; every n in 2..20000 ok')

# why composites never divide m: every d that divides m in the loop is prime (checked for all n <= 30000)
for n in range(2, 30001):
    m, d = n, 2
    while d * d <= m:
        if m % d == 0:
            assert is_prime(d), (n, d)
            while m % d == 0: m //= d
        d += 1
print('every divisor d met by the loop is prime for all n <= 30000: True')

# steps bound: steps <= isqrt(n) - 1 (d runs 2..isqrt(m)), reached only when n is prime
for n in range(2, 20001):
    st = factorise(n)[2]
    assert st <= max(0, math.isqrt(n) - 1)
    assert (st == max(0, math.isqrt(n) - 1)) or not is_prime(n)
print('steps <= isqrt(n) - 1 for n <= 20000, with equality for every prime: True')

# worst case near 10^12: prime
big = 999999999989
assert is_prime(big)
t = time.perf_counter(); r = factorise(big); dt = time.perf_counter() - t
print('prime near 10^12 steps:', r[2], '(sandbox time %.2f s, not a proof)' % dt)
print('10^12 =', factorise(10**12)[:2], 'steps', factorise(10**12)[2])
print('(10^6 + 3)^2 =', factorise((10**6 + 3) ** 2))

# smallest-prime-factor sieve below 10^6: O(n log log n) build, O(log n) per query
LIM = 10**6
spf = list(range(LIM + 1))
for p in range(2, math.isqrt(LIM) + 1):
    if spf[p] == p:
        for q in range(p * p, LIM + 1, p):
            if spf[q] == q:
                spf[q] = p
def spf_factor(n):
    f = []
    while n > 1:
        p = spf[n]; e = 0
        while n % p == 0: n //= p; e += 1
        f.append([p, e])
    return f
for n in [2, 360, 1024, 999983, 720720, 10**6]:
    assert spf_factor(n) == factorise(n)[0]
for _ in range(300):
    n = random.randint(2, LIM)
    assert spf_factor(n) == factorise(n)[0]
print('SPF sieve to 10^6 agrees with trial division on 306 values; 720720 ->', spf_factor(720720))
print('max query length: log2(10^6) =', math.floor(math.log2(LIM)), 'prime-factor pulls at most')

# edge asserts
assert factorise(2) == [[[2, 1]], 2, 0] and factorise(4) == [[[2, 2]], 3, 1] and factorise(9)[0] == [[3, 2]]
assert factorise(2**39)[0] == [[2, 39]] and factorise(2**39)[2] == 1
assert solve([10**12])[0][1] == 169          # (12 + 1) * (12 + 1)
print('edge asserts ok')
```

**Output (my run):**
```
[12, 97, 360, 1024] -> [[[[2, 2], [3, 1]], 6, 1], [[[97, 1]], 2, 8], [[[2, 3], [3, 2], [5, 1]], 24, 2], [[[2, 10]], 11, 1]]
[2] -> [[[[2, 1]], 2, 0]]
[999999999989] -> [[[[999999999989, 1]], 2, 999998]]
[600851475143] -> [[[[71, 1], [839, 1], [1471, 1], [6857, 1]], 16, 1470]]
  d=2: d*d=4 <= m -> step; divide out 2^3, m = 45
  d=3: d*d=9 <= m -> step; divide out 3^2, m = 5
  d=4: d*d=16 > m=5 -> stop; leftover m=5 (prime, add it)
random cross-check ok: 500 lists; every n in 2..20000 ok
every divisor d met by the loop is prime for all n <= 30000: True
steps <= isqrt(n) - 1 for n <= 20000, with equality for every prime: True
prime near 10^12 steps: 999998 (sandbox time 0.08 s, not a proof)
10^12 = [[[2, 12], [5, 12]], 169] steps 4
(10^6 + 3)^2 = [[[1000003, 2]], 3, 1000002]
SPF sieve to 10^6 agrees with trial division on 306 values; 720720 -> [[2, 4], [3, 2], [5, 1], [7, 1], [11, 1], [13, 1]]
max query length: log2(10^6) = 19 prime-factor pulls at most
edge asserts ok
```

**Edge cases:**
- n = 2: the loop does not run (4 > 2), steps 0, leftover 2.
- Powers of a prime: `1024` is `2^10` and costs 1 step (m drops to 1 immediately).
- n = 10^12 = 2^12 * 5^12: 4 steps, 169 divisors.
- Prime near 10^12 and a square of a large prime: about 10^6 steps.
- Perfect squares like 36: d = 6 is never needed because 2 and 3 are removed first.

**Follow-ups:**
- *Speed up the loop?* Handle 2 once and then try only odd d, or only 6k +- 1. It halves or thirds the steps; the big-O stays.
- *Primality of a single 64-bit number?* Miller-Rabin (not covered here).
- *Many big numbers?* Pollard's rho. Mention only.

**Common mistakes:**
- Looping `d <= n` instead of `d * d <= m`; or testing `d * d <= n` with the original n so the loop does not shrink.
- Forgetting the leftover prime above 1.
- Dividing `m` only once per d (so 12 becomes `[2,1],[3,1]` plus a leftover 2).
- Using float `sqrt` for 10^12-sized values; use `d * d <= m` or `math.isqrt`.

### Q29 ⭐⭐ 🟡 Modular inverse and n choose r modulo a prime. `a` is an integer with 1 <= a <= 10^9, `m` is an integer with 2 <= m <= 10^9, and `queries` has up to 1000 pairs [n, r] with 0 <= r <= n <= 10^5. Return `[inverse, answers]`: `inverse` is the integer x in [0, m - 1] with (a * x) % m == 1, or None if no such x exists; `answers[t]` is C(n, r) modulo 1000000007 for query t. Use `pow(a, -1, m)` (negative exponents with a modulus work from Python 3.8, a version note from editor knowledge; verified here on 3.13; it raises ValueError when gcd(a, m) > 1) and state when the inverse exists (exactly when gcd(a, m) = 1). Build the factorial table once and an inverse-factorial table from a single modular inverse of the largest factorial, so each query is O(1). Explain Fermat's little theorem a^(p-2) mod p as the inverse for PRIME p only (it is wrong for composite m) and the extended Euclidean algorithm as the general method, and why you cannot divide by r! (the exact quotient is not available after reducing modulo p). For modular powers without an inverse, `pow(x, n, m)` from Part 13's fast-power question is the tool (Q9). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a scan for the inverse and math.comb reduced modulo p on small inputs. Example: a=3, m=7, queries=[[5, 2], [10, 3]] -> [5, [10, 120]]; a=4, m=8, queries=[[0, 0]] -> [null, [1]]; a=10, m=1000000007, queries=[[100000, 50000]] -> [700000005, [149033233]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Modular arithmetic: modular inverse, and binomial coefficients from factorial and inverse-factorial tables.

**Say this first (1 line):** "The inverse of a modulo m exists exactly when gcd(a, m) = 1; for C(n, r) mod a prime p, precompute factorials and inverse factorials once and answer each query with two multiplications."

**Brute force:** For the inverse, try every x in [0, m-1] and test `a * x % m == 1` (O(m)). For C(n, r), call `math.comb(n, r) % p`, which builds a huge integer (for n = 10^5 that is a number with tens of thousands of digits). Both are the oracle.

**Optimal:**
- Inverse: `pow(a, -1, m)`. Negative exponents with a modulus need Python 3.8 or later (that is editor knowledge; the behaviour was run here on 3.13). It raises `ValueError` ("base is not invertible for the given modulus") when gcd(a, m) > 1, so catch it and return `None`. The result is already in [0, m-1].
- The inverse exists exactly when gcd(a, m) = 1. If gcd = g > 1, then `a * x` and `m` are both multiples of g, so `a * x % m` is also a multiple of g and can never be 1. If gcd = 1, Bezout gives `a*x + m*y = 1`, so x is the inverse. The program checks all a, m up to 80 (6320 pairs).
- Extended Euclid is the general method: `ext_gcd(a, b)` returns `(g, x, y)` with `a*x + b*y = g`; if g = 1 then `x % m` is the inverse. For `(3, 7)` it returns `(1, -2, 1)`, meaning `3*(-2) + 7*1 = 1`, and `-2 mod 7 = 5`, the inverse.
- Fermat: for a PRIME modulus p and gcd(a, p) = 1, `a^(p-2) mod p` is the inverse. For a composite modulus it fails: the program finds it wrong for 7436 coprime (a, m) pairs with composite m below 200, for example a = 3, m = 4 gives 1 but the true inverse is 3. It was right for every prime modulus.
- nCr: `fact[i]` mod p for i up to the largest n. One inverse: `inv_fact[mx] = pow(fact[mx], -1, p)`. Then `inv_fact[i-1] = inv_fact[i] * i % p` going down. Each query is `fact[n] * inv_fact[r] % p * inv_fact[n-r] % p`.
- Why you cannot divide by r!: after reducing the product modulo p the exact quotient is gone. The program shows C(10, 3): `(10*9*8 mod 11) // 3!` gives 0 but the real answer mod 11 is 10. You must multiply by the modular inverse of r!, which exists because n < p means r! shares no factor with p.
- The tables need n < p (10^5 < 10^9 + 7 here). For n >= p you would need Lucas' theorem.

**Complexity:** Tables O(N) with N the largest n (at most 10^5), one `pow` of O(log p) multiplications, each query O(1). Total O(N + Q + log p). The inverse of a by `pow` is O(log m); the scan is O(m). Space O(N).

**Dry run:** `a=3, m=7`: `3 * 5 = 15 = 1 (mod 7)`, so the inverse is 5. Fermat gives `3^5 mod 7 = 5` too, because 7 is prime. For C(5, 2) = 120 / (2 * 6) = 10: `fact[5] * inv_fact[2] * inv_fact[3]` mod p gives 10. The program prints these.

**Code:**
```python
import math
import random

random.seed(2901)
MOD = 1_000_000_007

def ext_gcd(a, b):
    """Returns (g, x, y) with a*x + b*y = g."""
    if b == 0:
        return a, 1, 0
    g, x, y = ext_gcd(b, a % b)
    return g, y, x - (a // b) * y

def inverse(a, m):
    try:
        return pow(a, -1, m)               # Python 3.8+ (editor knowledge); ValueError if gcd > 1
    except ValueError:
        return None

def inverse_ext(a, m):
    g, x, _ = ext_gcd(a % m, m)
    return x % m if g == 1 else None

def solve(a, m, queries):
    mx = max([n for n, _ in queries], default=0)
    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (mx + 1)
    inv_fact[mx] = pow(fact[mx], -1, MOD)           # ONE modular inverse
    for i in range(mx, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD     # (i-1)!^-1 = i! ^-1 * i
    return [inverse(a, m), [fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD for n, r in queries]]

def brute(a, m, queries):
    inv = next((x for x in range(m) if a * x % m == 1), None)
    return [inv, [math.comb(n, r) % MOD for n, r in queries]]

examples = [((3, 7, [[5, 2], [10, 3]]), [5, [10, 120]]),
            ((4, 8, [[0, 0]]), [None, [1]]),
            ((10, MOD, [[100000, 50000]]), [700000005, [149033233]])]
for args, want in examples[:2]:
    assert solve(*args) == want == brute(*args)
a, m, q = examples[2][0]
assert solve(a, m, q) == examples[2][1]
assert math.comb(100000, 50000) % MOD == 149033233 and 10 * 700000005 % MOD == 1
for args, want in examples:
    print(args if len(str(args)) < 60 else (args[0], args[1], args[2]), '->', solve(*args))

# dry run: 3 mod 7 by hand (search), by Fermat, by extended Euclid; C(5,2) from tables mod 7-free formula
print('3 * 5 =', 3 * 5, '=', 15 % 7, '(mod 7)  -> inverse of 3 is 5')
print('Fermat 3^(7-2) mod 7 =', pow(3, 5, 7), '; ext_gcd(3, 7) =', ext_gcd(3, 7), '(3*(-2) + 7*1 = 1, and -2 % 7 = 5)')
print('C(5,2) = 5! * inv(2!) * inv(3!) =', 120, '*', pow(2, -1, MOD), '*', pow(6, -1, MOD), 'mod p =', 120 * pow(2, -1, MOD) * pow(6, -1, MOD) % MOD)

# seeded random cross-check on small values against a scan and math.comb
for _ in range(3000):
    m = random.randint(2, 60); a = random.randint(1, 200)
    qs = [[n, random.randint(0, n)] for n in (random.randint(0, 40) for _ in range(5))]
    assert solve(a, m, qs) == brute(a, m, qs), (a, m)
print('random cross-check ok: 3000 cases')

# exhaustive: inverse exists exactly when gcd = 1, for every a, m <= 80; result in [0, m-1]; ext Euclid agrees
cnt = 0
for m in range(2, 81):
    for a in range(1, 81):
        inv = inverse(a, m)
        assert (inv is not None) == (math.gcd(a, m) == 1)
        assert inv == inverse_ext(a, m) == next((x for x in range(m) if a * x % m == 1), None)
        if inv is not None:
            assert 0 <= inv < m and a * inv % m == 1
        cnt += 1
print('exhaustive a, m <= 80:', cnt, 'pairs: inverse exists iff gcd = 1')

# Fermat's a^(m-2) is the inverse only for PRIME m
def is_prime(n): return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))
bad_comp = bad_prime = 0; ex = None
for m in range(3, 200):
    for a in range(1, m):
        if math.gcd(a, m) == 1:
            ok = pow(a, m - 2, m) == pow(a, -1, m)
            if is_prime(m): bad_prime += (not ok)
            elif not ok:
                bad_comp += 1; ex = ex or (a, m, pow(a, m - 2, m), pow(a, -1, m))
print('Fermat wrong for a prime modulus:', bad_prime, '; for a composite modulus (coprime a):', bad_comp, '; first (a, m, fermat, true) =', ex)
assert bad_prime == 0 and bad_comp > 0
print('pow(4, -1, 8) raises:', end=' ')
try: pow(4, -1, 8)
except ValueError as e: print(repr(str(e)))

# nCr: all n <= 120 vs math.comb, some large queries
qs = [[n, r] for n in range(0, 121) for r in range(0, n + 1)]
res = solve(1, 2, qs)[1]
assert res == [math.comb(n, r) % MOD for n, r in qs]
print('nCr table n <= 120 (', len(qs), 'queries) matches math.comb')
big = [[random.randint(0, 10**5), 0] for _ in range(1000)]
big = [[n, random.randint(0, n)] for n, _ in big]
res = solve(7, 10**9, big)[1]
for (n, r), v in list(zip(big, res))[:15]:
    assert v == math.comb(n, r) % MOD
print('1000 queries with n up to 10^5 built from one table; 15 spot-checked against math.comb')

# why you cannot divide by r!: floor-dividing the reduced products is wrong
n, r = 10, 3
reduced = 1
for i in range(n - r + 1, n + 1): reduced = reduced * i % 11
print('C(10,3) = 120; (10*9*8 mod 11) // 3! =', reduced, '// 6 =', reduced // 6, '(wrong; true 120 mod 11 =', 120 % 11, ')')

# edge asserts
assert solve(1, 2, [])[0] == 1 and solve(2, 2, [])[0] is None
assert solve(10**9, 10**9, [])[0] is None and solve(10**9, 10**9 - 1, [])[0] == 1
assert solve(5, 7, [[0, 0], [100000, 0], [100000, 100000]])[1] == [1, 1, 1]
print('edge asserts ok')
```

**Output (my run):**
```
(3, 7, [[5, 2], [10, 3]]) -> [5, [10, 120]]
(4, 8, [[0, 0]]) -> [None, [1]]
(10, 1000000007, [[100000, 50000]]) -> [700000005, [149033233]]
3 * 5 = 15 = 1 (mod 7)  -> inverse of 3 is 5
Fermat 3^(7-2) mod 7 = 5 ; ext_gcd(3, 7) = (1, -2, 1) (3*(-2) + 7*1 = 1, and -2 % 7 = 5)
C(5,2) = 5! * inv(2!) * inv(3!) = 120 * 500000004 * 166666668 mod p = 10
random cross-check ok: 3000 cases
exhaustive a, m <= 80: 6320 pairs: inverse exists iff gcd = 1
Fermat wrong for a prime modulus: 0 ; for a composite modulus (coprime a): 7436 ; first (a, m, fermat, true) = (3, 4, 1, 3)
pow(4, -1, 8) raises: 'base is not invertible for the given modulus'
nCr table n <= 120 ( 7381 queries) matches math.comb
1000 queries with n up to 10^5 built from one table; 15 spot-checked against math.comb
C(10,3) = 120; (10*9*8 mod 11) // 3! = 5 // 6 = 0 (wrong; true 120 mod 11 = 10 )
edge asserts ok
```

**Edge cases:**
- `a = 4, m = 8`: gcd 2, no inverse, answer `None` (the question's `null`).
- `a` larger than `m` or a multiple of `m`: reduce implicitly; `pow` handles it. `a = m` gives `None`.
- `m = 2`, `a = 1`: the inverse is 1.
- `r = 0` or `r = n`: both give 1.
- `n = 10^5`, `r = 50000`: the table has 100001 entries; the answer is 149033233.
- No queries: tables of size 1.

**Follow-ups:**
- *Modular power when there is no inverse?* `pow(x, n, m)` (the fast power in Q9) works for any m.
- *Inverse of all numbers 1..N in O(N)?* `inv[i] = -(p // i) * inv[p % i] % p`, for prime p.
- *Why mod 10^9 + 7?* It is a prime a bit below 2^30, so products of two residues fit in a 64-bit integer in other languages. Python does not care.

**Common mistakes:**
- Using Fermat for a composite modulus.
- Dividing with `//` after taking the modulus.
- Computing the inverse of `r!` and `(n-r)!` separately for each query with `pow` (works, but costs a log factor per query).
- Forgetting that `pow(a, -1, m)` raises when the inverse does not exist.

### Q30 ⭐⭐ 🟡 Fraction to recurring decimal. `numerator` and `denominator` are integers with |numerator| <= 2^31, 1 <= |denominator| <= 10^5 (the denominator is nonzero and may be negative). Return the decimal expansion of numerator / denominator as a string: an optional '-' (only if the value is negative), the integer part, and, if the fraction part is not zero, a '.' followed by the digits, with the repeating block wrapped in parentheses, e.g. '0.5', '0.(6)', '2', '-0.58(3)', '0.0(012)'. The value 0 is '0'. Do long division, remembering for every remainder the position in the digit string where it first appeared; when a remainder repeats, the digits from there on are the repeating block. Explain why the remainders must repeat (fewer than |denominator| distinct nonzero remainders), why the repeating block has at most |denominator| - 1 digits, and why the sign must be decided before taking absolute values. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the multiplicative order of 10 modulo the denominator with its 2s and 5s removed on small inputs. Example: numerator=1, denominator=2 -> '0.5'; numerator=2, denominator=3 -> '0.(6)'; numerator=-7, denominator=12 -> '-0.58(3)'; numerator=1, denominator=81 -> '0.(012345679)'; numerator=0, denominator=-5 -> '0'; numerator=22, denominator=7 -> '3.(142857)'.
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Long division with a remainder map. A repeated remainder means a repeated digit block.

**Say this first (1 line):** "Do long division, store each remainder's position in the digit string, and when a remainder shows up again wrap the digits from that position in parentheses."

**Brute force:** Compute the pre-period and period lengths from number theory: remove the factors 2 and 5 from the denominator; the pre-period is the larger of the two exponents and the period is the multiplicative order of 10 modulo what is left. Then take `rem * 10^total // d` as one big integer and cut it. That is the oracle; it is exact but builds a long integer.

**Optimal:**
- Decide the sign first: negative if exactly one of numerator and denominator is negative. `0` gives `'0'` (no sign, no point).
- Work with absolute values: `ip, rem = divmod(n, d)`. If `rem == 0` return `sign + str(ip)`.
- Loop: while `rem` is nonzero and not seen, record `seen[rem] = len(digits)`, then `rem *= 10`, append `rem // d`, `rem %= d`.
- If `rem == 0` the decimal terminates. Otherwise `k = seen[rem]` and the digits from index k repeat.
- Why the remainders must repeat: each new remainder is one of 1..d-1 (zero ends the division), so there are fewer than d distinct nonzero remainders. After at most d - 1 steps a remainder repeats. The next digits are then fully determined, so they repeat too.
- Why the block has at most d - 1 digits: a block longer than the number of distinct remainders would need a repeated remainder inside it. The program shows, for numerator 1 and every d up to 3000, that the block length equals the multiplicative order of 10 (after removing 2s and 5s) and is at most d - 1 (a full-reptend prime like 2971 hits d - 1; 99989 gives 99988 digits).
- Why the sign comes before the absolute values: `divmod(-7, 12)` is `(-1, 5)` in Python (floor division), which gives integer part -1 and remainder 5, not -0.58(3). Python also has no negative integer zero, so for `-1/3` the integer part 0 cannot carry the sign. Take `sign` from the original signs, then work with `abs`.

**Complexity:** Time O(|d|) digits at most (fewer than d - 1 + the digits before the repeat), each step O(1) with a dict. Space O(|d|) for the dict and the digits. Maximum about 10^5 digits.

**Dry run:** `-7/12`. One negative, so sign `-`. `7/12`: integer part 0, remainder 7. Remainder 7 at position 0: 70 / 12 = 5, new remainder 10. Remainder 10 at position 1: 100 / 12 = 8, new remainder 4. Remainder 4 at position 2: 40 / 12 = 3, new remainder 4. Remainder 4 is seen at position 2, so digits from 2 repeat: `-0.58(3)`.

**Code:**
```python
import math
import random
import sys
from fractions import Fraction

random.seed(3001)
sys.set_int_max_str_digits(0)   # the ORACLE builds a ~10^5-digit integer and prints it; the solution never does

def fraction_to_decimal(num, den):
    if num == 0:
        return '0'
    sign = '-' if (num < 0) != (den < 0) else ''      # decide the sign BEFORE abs
    n, d = abs(num), abs(den)
    ip, rem = divmod(n, d)
    if rem == 0:
        return sign + str(ip)
    digits, seen = [], {}
    while rem and rem not in seen:
        seen[rem] = len(digits)                        # position where this remainder first appeared
        rem *= 10
        digits.append(str(rem // d))
        rem %= d
    if rem == 0:
        return sign + str(ip) + '.' + ''.join(digits)
    k = seen[rem]
    return sign + str(ip) + '.' + ''.join(digits[:k]) + '(' + ''.join(digits[k:]) + ')'

def mult_order(d):
    """Oracle: lengths from the multiplicative order of 10 mod d with 2s and 5s removed."""
    a = b = 0
    while d % 2 == 0: d //= 2; a += 1
    while d % 5 == 0: d //= 5; b += 1
    pre = max(a, b)
    period = 0
    if d > 1:
        period, x = 1, 10 % d
        while x != 1:
            x = x * 10 % d
            period += 1
    return pre, period

def brute(num, den):
    """Oracle: exact digits from integer arithmetic using the predicted pre-period and period lengths."""
    if num == 0:
        return '0'
    sign = '-' if (num < 0) != (den < 0) else ''
    fr = Fraction(abs(num), abs(den))
    ip, rem, d = fr.numerator // fr.denominator, fr.numerator % fr.denominator, fr.denominator
    if rem == 0:
        return sign + str(ip)
    pre, per = mult_order(d)
    total = pre + per
    s = str(rem * 10 ** total // d).zfill(total)
    return sign + str(ip) + '.' + s[:pre] + ('(' + s[pre:] + ')' if per else '')

examples = [((1, 2), '0.5'), ((2, 3), '0.(6)'), ((-7, 12), '-0.58(3)'), ((1, 81), '0.(012345679)'),
            ((0, -5), '0'), ((22, 7), '3.(142857)')]
for (a, b), want in examples:
    assert fraction_to_decimal(a, b) == want == brute(a, b)
    print(f'{a}/{b} -> {fraction_to_decimal(a, b)}')

# dry run: -7/12
print('-7/12: sign "-" (one negative); |7|/12: integer part 0, remainder 7')
rem, seen, digits = 7, {}, []
while rem and rem not in seen:
    seen[rem] = len(digits)
    print(f'  remainder {rem}: first seen at digit position {len(digits)}; {rem}*10 = {rem * 10}, digit {rem * 10 // 12}, new remainder {rem * 10 % 12}')
    rem *= 10; digits.append(str(rem // 12)); rem %= 12
print(f'  remainder {rem} was seen at position {seen[rem]} -> repeat from digit {seen[rem]}: 0.{"".join(digits[:seen[rem]])}({"".join(digits[seen[rem]:])})')

# seeded random cross-check against the multiplicative-order construction
for _ in range(4000):
    a = random.randint(-2**31, 2**31); b = random.choice([-1, 1]) * random.randint(1, 10**5)
    assert fraction_to_decimal(a, b) == brute(a, b), (a, b)
print('random cross-check ok: 4000 cases')
for _ in range(3000):
    a = random.randint(-50, 50); b = random.choice([-1, 1]) * random.randint(1, 60)
    assert fraction_to_decimal(a, b) == brute(a, b)
print('random small cross-check ok: 3000 cases')

# exhaustive: every denominator up to 300 with numerators -2d..2d, and value check by exact reparse
cnt = 0
for d in range(1, 301):
    for a in range(-2 * d, 2 * d + 1):
        s = fraction_to_decimal(a, d)
        assert s == brute(a, d)
        cnt += 1
print('exhaustive |den| <= 300, |num| <= 2|den|:', cnt, 'fractions')

# period length <= den - 1 and equals the multiplicative order; pre-period = max(#2s, #5s)
worst = (0, 0)
for d in range(2, 3001):
    pre, per = mult_order(d)
    out = fraction_to_decimal(1, d)
    got = out.split('.')[1] if '.' in out else ''
    got_per = len(got.split('(')[1][:-1]) if '(' in got else 0
    assert got_per == per and per <= d - 1
    if per > worst[1]: worst = (d, per)
print('d <= 3000: period equals multiplicative order and is <= d - 1; longest', worst, '(a full-reptend prime has period d - 1)')
r = fraction_to_decimal(1, 99989)
assert r.endswith(')') and len(r.split('(')[1]) - 1 == mult_order(99989)[1]
print('1/99989 period length:', mult_order(99989)[1], 'of at most', 99988)
r2 = fraction_to_decimal(1, 99991)
print('1/99991 period length:', len(r2.split('(')[1]) - 1)
# distinct nonzero remainders < den, so a repeat must occur within den - 1 steps
for d in (7, 97, 1000, 99999):
    rem, k, seen = 1, 0, set()
    while rem and rem not in seen:
        seen.add(rem); rem = rem * 10 % d; k += 1
    assert k <= d - 1 + (d == 1)
print('digit loop runs at most den - 1 times for 7, 97, 1000, 99999: True')

# sign trap: floor division on a negative numerator breaks the integer part and the digits
def naive_sign(num, den):
    ip, rem = divmod(num, den)           # Python floors: -7 // 12 = -1, remainder 5
    return ip, rem
print('divmod(-7, 12) =', naive_sign(-7, 12), '-> integer part -1 and remainder 5, not -0.58(3)')
assert fraction_to_decimal(-7, 12) == '-0.58(3)'
# -1/3 and 1/-3 and -1/-3 agree in magnitude, sign decided first
assert [fraction_to_decimal(-1, 3), fraction_to_decimal(1, -3), fraction_to_decimal(-1, -3)] == ['-0.(3)', '-0.(3)', '0.(3)']

# edge asserts
assert fraction_to_decimal(-2**31, -1) == '2147483648' and fraction_to_decimal(-2**31, 1) == '-2147483648'
assert fraction_to_decimal(1, 3) == '0.(3)' and fraction_to_decimal(1, 6) == '0.1(6)' and fraction_to_decimal(1, 1) == '1'
assert fraction_to_decimal(1, 1000) == '0.001' and fraction_to_decimal(1, 90) == '0.0(1)' and fraction_to_decimal(1, 7) == '0.(142857)'
assert fraction_to_decimal(5, 4) == '1.25' and fraction_to_decimal(-1, 2**5) == '-0.03125'
print('edge asserts ok')
```

**Output (my run):**
```
1/2 -> 0.5
2/3 -> 0.(6)
-7/12 -> -0.58(3)
1/81 -> 0.(012345679)
0/-5 -> 0
22/7 -> 3.(142857)
-7/12: sign "-" (one negative); |7|/12: integer part 0, remainder 7
  remainder 7: first seen at digit position 0; 7*10 = 70, digit 5, new remainder 10
  remainder 10: first seen at digit position 1; 10*10 = 100, digit 8, new remainder 4
  remainder 4: first seen at digit position 2; 4*10 = 40, digit 3, new remainder 4
  remainder 4 was seen at position 2 -> repeat from digit 2: 0.58(3)
random cross-check ok: 4000 cases
random small cross-check ok: 3000 cases
exhaustive |den| <= 300, |num| <= 2|den|: 180900 fractions
d <= 3000: period equals multiplicative order and is <= d - 1; longest (2971, 2970) (a full-reptend prime has period d - 1)
1/99989 period length: 99988 of at most 99988
1/99991 period length: 49995
digit loop runs at most den - 1 times for 7, 97, 1000, 99999: True
divmod(-7, 12) = (-1, 5) -> integer part -1 and remainder 5, not -0.58(3)
edge asserts ok
```

**Edge cases:**
- Zero numerator with a negative denominator: `'0'`.
- Both negative: positive result (`-1 / -3` gives `0.(3)`).
- Integer result: no decimal point (`2`, `-2147483648`).
- `-2^31 / -1 = 2147483648`: overflows int32 in other languages, fine in Python.
- Terminating fractions such as `1/1000 = 0.001`, or a pre-period like `1/6 = 0.1(6)`.
- Large block: `1/99989` has 99988 repeating digits.

**Follow-ups:**
- *Why does the denominator's 2s and 5s decide termination?* The decimal terminates if and only if after reduction the denominator has no prime factor other than 2 and 5.
- *Convert a repeating decimal back to a fraction?* `0.58(3)`: shift and subtract.
- *Other bases?* Replace 10 with the base.

**Common mistakes:**
- Storing the digit position in the dict instead of the remainder (or storing the digit, which can repeat without the remainder repeating).
- Not reducing or skipping the check for `rem == 0` (infinite loop or `(0)` printed).
- Getting the sign wrong when the integer part is 0.
- Using floats.
