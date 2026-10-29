# Book 5 — Part 13: Extra I (Prefix Sums, Matrices and 2D Grids, Math and Number Theory, Randomized Algorithms, Sorting Internals)

**Topic:** Python DSA for product-company interviews, the 'Extra I' part: prefix sums and difference arrays (immutable range sums, range addition, car pooling, running sums and the pivot index, counting range sums with merge sort), 2D prefix sums (region sums, matrix block sums, point updates at a basic level, adding to many rectangles with a 2D difference array), matrix manipulation (in-place rotation, spiral and diagonal traversal, set matrix zeroes in O(1) space, Game of Life in place, rotating every layer), math and number theory (Euclid's gcd and lcm, trailing zeroes of n factorial, the prime sieve, factorisation, fast power, modular inverse with pow(a, -1, m) and n choose r modulo a prime, Pascal's triangle, happy number, Excel column numbers, fractions to recurring decimals), fixed-width versus Python integers and floating-point pitfalls (reversing a 32-bit integer, round-half-even, float versus Fraction and Decimal, big-integer Fibonacci and the int-to-string digit limit), randomized algorithms checked exactly by enumerating every random-choice sequence (Fisher-Yates and the classic biased shuffle, reservoir sampling with one slot and k slots, weighted random pick with prefix sums and bisect, rejection sampling, random index of a target value), and sorting internals from scratch (merge sort with exact comparison counts, counting inversions, iterative Lomuto quicksort, Hoare partition, three-way partition on duplicates, heap sort, counting and radix sort, maximum gap in linear time, stability and Python's sort behaviour with key=, reverse=, cmp_to_key and mixed types, adaptive behaviour on nearly sorted input, Timsort's minrun and natural runs, the comparison-sort lower bound).

**Target:** 50  |  **Actual:** 50 (⭐⭐⭐ 17, ⭐⭐ 22, ⭐ 11)  |  **Date:** 2026-10-29  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns the prefix-sum and difference-array techniques, matrix manipulation, math and number theory, randomized algorithms and sorting from scratch. Part 1 owns hashing and the hashmap prefix-sum count 'Part 1 Q13' (subarray sum equals k), 'Part 1 Q11' (product of array except self), the set matrix zeroes statement at concept level 'Part 1 Q31' (Q25 here writes it fully in O(1) space and tests the marker trap), 'Part 1 Q50' (submatrices that sum to a target) and the randomised set 'Part 1 Q35' and its duplicate version 'Part 1 Q47' (not repeated; the reservoir questions here are about one-pass streams). Part 5 owns binary search ('Part 5 Q10' and 'Part 5 Q22' search sorted matrices; not repeated). Part 8 owns heaps and greedy ('Part 8 Q28' heap sift up and down, 'Part 8 Q36' quickselect rounds; heap sort here is the sorting-internals version and kth largest is not repeated). Part 6 owns linked-list merge sort ('Part 6 Q25'). Part 9 owns graph traversal on grids (BFS, DFS, flood fill), Part 12 owns bit manipulation, and Part 14 owns design problems and the Fenwick and segment trees (named here only as the answer for mutable range queries: Q4, Q40 and Q47).

Fixed-width integers: Python integers have no overflow, so only Q10 simulates a 32-bit signed integer (it returns both the checked result and what a wrapping machine would hold); Q2, Q9 and Q20 ask where a fixed-width language would overflow while the Python answers stay exact. Randomised questions never use a live random generator in the checker: each fixes the random choices as an input list (or enumerates ALL choice sequences for tiny sizes) and states exactly what is accepted (the output order, the draw convention and the exact counts). Every recursive question keeps its depth far below CPython's default recursion limit of 1000, and the two quicksort questions (Q16, Q42) require an explicit stack because sorted or all-equal input nests about n frames. Version notes for pow(a, -1, m), math.lcm and the int-to-str digit limit are editor knowledge (behaviour itself was verified by running Python 3.13); the Timsort description in Q44 is editor-level and labelled so.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet or result summary only (see research_notes/Book5_Part13_sources.md). Searches returned prefix-sum and difference-array guides (techinterview.org, a LeetCode Discuss study guide, talentd.in topic lists), matrix question lists (Educative, Techie Delight, talentd.in, labuladong), number-theory and math pattern guides (techinterview.org), sampling guides (Wikipedia reservoir sampling, techinterview.org, a Codemia rand7 page), sorting guides (techinterview.org, Techie Delight, GeeksforGeeks) and Python Sorting HOWTO snippets; nothing was found tying any single item to a named company, so 'Asked at' lines name source types only. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 Range sum queries on an immutable array. `nums` has 1 <= len <= 10^5 integers (|value| <= 10^9) that never change, and `queries` is a list of up to 10^5 pairs [l, r] with 0 <= l <= r < len(nums). Return the list of sums nums[l] + ... + nums[r] (both ends included), one per query, answering each query in O(1) after one O(n) pass. Build `pre` with `pre[0] = 0` and `pre[i + 1] = pre[i] + nums[i]`, explain why the leading 0 removes the special case for l = 0 and why the answer is `pre[r + 1] - pre[l]`, and mention `itertools.accumulate(nums, initial=0)` as the idiom. State why a C++ or Java version needs a 64-bit type here (a sum can reach 10^5 * 10^9 = 10^14, which is above 2^31 - 1) while Python integers need nothing. Counting subarrays whose sum equals k with a hashmap is Part 1 Q13 and the product of the array except self is Part 1 Q11; neither is repeated here. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a plain sum() over each slice on small inputs. Example: nums=[3, -1, 4, 1, -5], queries=[[0, 4], [1, 2], [3, 3], [0, 0]] -> [2, 3, 1, 3]; nums=[7], queries=[[0, 0]] -> [7]; nums=[-2, -2, -2], queries=[[0, 2], [1, 2]] -> [-6, -4].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Prefix sums. Many range queries on data that never changes. Pay O(n) once, then answer each query in O(1).

**Say this first (1 line):** "I build `pre` with a leading zero, so any range sum is `pre[r + 1] - pre[l]` in O(1)."

**Brute force:**
- For each query, `sum(nums[l:r+1])`.
- O(n) per query, so O(n * q) in total. With n = q = 10^5 that is about 10^10 additions. Too slow.

**Optimal:**
- `pre[0] = 0`, `pre[i + 1] = pre[i] + nums[i]`. So `pre[i]` is the sum of the first i numbers.
- Sum of `nums[l..r]` = (first r+1 numbers) minus (first l numbers) = `pre[r + 1] - pre[l]`.
- The leading 0 is why `l = 0` needs no special case: `pre[0] = 0` means "nothing to subtract". Without it you would write `pre[r] - pre[l-1]` and need an `if l == 0`.
- Idiom: `list(itertools.accumulate(nums, initial=0))` builds the same table.
- Invariant: `pre[i]` always equals the sum of `nums[:i]`.

**Complexity:**
- Build O(n), each query O(1), total O(n + q).
- Space O(n) for `pre`, plus the output.

**Dry run:** `nums = [3, -1, 4, 1, -5]`, so `pre = [0, 3, 2, 6, 7, 2]`.

| query | formula | answer |
|---|---|---|
| [0, 4] | pre[5] - pre[0] = 2 - 0 | 2 |
| [1, 2] | pre[3] - pre[1] = 6 - 3 | 3 |
| [3, 3] | pre[4] - pre[3] = 7 - 6 | 1 |
| [0, 0] | pre[1] - pre[0] = 3 - 0 | 3 |

**Code:**
```python
import random
from itertools import accumulate

def brute(nums, queries):
    return [sum(nums[l:r + 1]) for l, r in queries]            # O(n) per query

def optimal(nums, queries):
    pre = [0]                                                  # pre[i] = sum of nums[:i]
    for v in nums:
        pre.append(pre[-1] + v)
    return [pre[r + 1] - pre[l] for l, r in queries]           # O(1) per query

def optimal_accumulate(nums, queries):
    pre = list(accumulate(nums, initial=0))                    # same table, idiom form
    return [pre[r + 1] - pre[l] for l, r in queries]

# examples from the prompt
ex = [([3, -1, 4, 1, -5], [[0, 4], [1, 2], [3, 3], [0, 0]], [2, 3, 1, 3]),
      ([7], [[0, 0]], [7]),
      ([-2, -2, -2], [[0, 2], [1, 2]], [-6, -4])]
for nums, qs, want in ex:
    got = optimal(nums, qs)
    assert got == want == brute(nums, qs) == optimal_accumulate(nums, qs)
    print(nums, qs, '->', got)

# seeded random cross-check
random.seed(1)
cases = 0
for _ in range(500):
    n = random.randint(1, 12)
    nums = [random.randint(-9, 9) for _ in range(n)]
    qs = []
    for _ in range(random.randint(0, 8)):
        l = random.randint(0, n - 1)
        qs.append([l, random.randint(l, n - 1)])
    assert optimal(nums, qs) == brute(nums, qs) == optimal_accumulate(nums, qs)
    cases += 1
print('random cross-check ok:', cases, 'cases')

# exhaustive: every (l, r) on a fixed small array
a = [5, -3, 0, 8, -1, 2]
allq = [[l, r] for l in range(len(a)) for r in range(l, len(a))]
assert optimal(a, allq) == brute(a, allq)
print('all', len(allq), 'ranges of a 6-array ok')

# max size: the sum really exceeds a 32-bit int; Python needs nothing special
big = [10**9] * 10**5
total = optimal(big, [[0, len(big) - 1]])[0]
print('max total', total, '> 2**31-1 =', 2**31 - 1, ' fits int64:', total < 2**63)
assert total == 10**14 > 2**31 - 1
# edge: single element, negative-only
assert optimal([-5], [[0, 0]]) == [-5]
assert optimal([1, 2, 3], []) == []
print('edge asserts ok')
```

**Output (my run):**
```
[3, -1, 4, 1, -5] [[0, 4], [1, 2], [3, 3], [0, 0]] -> [2, 3, 1, 3]
[7] [[0, 0]] -> [7]
[-2, -2, -2] [[0, 2], [1, 2]] -> [-6, -4]
random cross-check ok: 500 cases
all 21 ranges of a 6-array ok
max total 100000000000000 > 2**31-1 = 2147483647  fits int64: True
edge asserts ok
```

**Edge cases:**
- One element, or `l == r`.
- `l == 0` (the leading zero handles it).
- Negative numbers: nothing changes, subtraction still works.
- Zero queries: return `[]`.
- Sums up to 10^14. A C++ or Java version needs `long long` / `long` (10^5 * 10^9 = 10^14 is above 2^31 - 1 = 2147483647 but below 2^63). Python ints just work. The run above printed the max total.

**Follow-ups:**
- *Values change between queries?* A prefix array costs O(n) per update. Use a Fenwick or segment tree (O(log n) both). That is Part 14, only named here.
- *Count subarrays with sum k?* Prefix sums plus a hashmap. That is Part 1 Q13.
- *Why not the product?* Division by zero breaks the prefix-product trick. See Part 1 Q11.

**Common mistakes:**
- Writing `pre[r] - pre[l]` (off by one: drops `nums[r]`).
- Building `pre` of length n and special-casing `l = 0`.
- Using `sum(nums[l:r+1])` inside the loop and calling it a prefix sum.
- Forgetting that C++/Java need 64-bit sums.

---

### Q2 ⭐⭐⭐ 🟢 GCD and LCM with Euclid's algorithm. `a` and `b` are integers with 1 <= a, b <= 10^18 and `nums` has 1 to 1000 integers with 1 <= value <= 10^12. Return `[gcd(a, b), lcm(a, b), steps, gcd_all, lcm_all]`: `steps` is the number of times the loop `while b: a, b = b, a % b` runs, started from the pair exactly as given (if a < b the first step swaps them); `gcd_all` and `lcm_all` are the GCD and the LCM of the whole list `nums`. Write the loop yourself (do not call `math.gcd`), compute the LCM as `a // g * b` and explain why dividing first keeps intermediates small even though Python never overflows (a fixed-width language would overflow on `a * b`). State why the worst case for Euclid is a pair of consecutive Fibonacci numbers (smaller first, which costs one extra swap step; for all 1 <= a, b <= 100 the largest step count, 10, is reached by (55, 89)) and why that gives O(log min(a, b)) steps, then say what `math.gcd` and `math.lcm` (the latter added in Python 3.9: version note from editor knowledge, not checked against a page) do for you, including `math.gcd(0, 0)`. `lcm_all` can be a very large integer; return it exactly. In the answer include a dry run on the first example and a seeded random cross-check of your solution against math.gcd, math.lcm and a recursive step counter on small inputs. Example: a=48, b=18, nums=[4, 6, 10] -> [6, 144, 3, 2, 60]; a=13, b=21, nums=[7] -> [1, 273, 7, 7, 7]; a=5, b=5, nums=[2, 3, 5, 7, 11] -> [5, 5, 1, 1, 2310]; a=8, b=12, nums=[1000000007, 998244353] -> [4, 24, 3, 1, 998244359987710471].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Number theory. Euclid: `gcd(a, b) = gcd(b, a % b)`. Then `lcm = a / gcd * b`. Fold both over a list.

**Say this first (1 line):** "gcd by the remainder loop, lcm as `a // g * b`, and fold over the list with gcd(0, x) = x and lcm identity 1."

**Brute force:**
- Try every d from min(a, b) down to 1 and take the first that divides both.
- O(min(a, b)). For 10^18 that never finishes.

**Optimal:**
- `while b: a, b = b, a % b`. The pair shrinks fast: after any two steps the larger number is at least halved (a % b is always less than half of a), so the loop is logarithmic.
- Why it is correct: any common divisor of a and b divides `a % b`, and the other way round. So the common divisors do not change, only the numbers shrink.
- lcm: `a // g * b`. Dividing first keeps the intermediate at most the lcm. In C++/Java `a * b` with a, b near 10^18 overflows 64 bits. Python would not overflow, but the product is just a needlessly big number.
- Fold: `gcd_all` starts at 0 (`gcd(0, x) = x`). `lcm_all` starts at 1 and does `la // gcd(la, v) * v`.
- Worst case for steps: consecutive Fibonacci numbers, smaller first. Each remainder is the next smaller Fibonacci number, so every step shrinks as slowly as possible. Fibonacci numbers grow by a factor of about 1.618, so the step count is O(log min(a, b)) (Lame's theorem: about 4.8 * log10(min) steps at most). Smaller first costs one extra step, the swap: (55, 89) takes 10 steps, (89, 55) takes 9.
- Library: `math.gcd` (accepts several arguments in 3.9+) and `math.lcm` (added in Python 3.9; editor knowledge, I only ran it on 3.13). `math.gcd(0, 0)` is 0.

**Complexity:**
- Steps: O(log min(a, b)). The Fibonacci pair just under 10^18 takes 86 steps (computed).
- Whole list: O(len(nums) * log(max)) gcd steps. `lcm_all` can grow to tens of thousands of bits, so the later multiplications and divisions are on big integers and cost more than O(1) each.
- Space O(1) beyond the result.

**Dry run:** `a=48, b=18`.
- (48, 18) -> (18, 12) -> (12, 6) -> (6, 0). 3 steps, gcd 6. lcm = 48 // 6 * 18 = 144.
- `nums = [4, 6, 10]`: gcd: 0 -> 4 -> 2 -> 2. lcm: 1 -> 4 -> 4 // 2 * 6 = 12 -> 12 // 2 * 10 = 60. Result `[6, 144, 3, 2, 60]`.

**Code:**
```python
import math, random

def euclid(a, b):
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return a, steps

def optimal(a, b, nums):
    g, steps = euclid(a, b)
    lcm = a // g * b                      # divide first: intermediate stays <= lcm
    ga, la = 0, 1                         # gcd(0, x) = x, lcm identity 1
    for v in nums:
        ga = euclid(ga, v)[0]
        la = la // euclid(la, v)[0] * v
    return [g, lcm, steps, ga, la]

def brute(a, b, nums):                    # library + recursive step counter
    def rsteps(x, y):
        return 0 if y == 0 else 1 + rsteps(y, x % y)
    return [math.gcd(a, b), math.lcm(a, b), rsteps(a, b), math.gcd(*nums), math.lcm(*nums)]

ex = [((48, 18, [4, 6, 10]), [6, 144, 3, 2, 60]),
      ((13, 21, [7]), [1, 273, 7, 7, 7]),
      ((5, 5, [2, 3, 5, 7, 11]), [5, 5, 1, 1, 2310]),
      ((8, 12, [1000000007, 998244353]), [4, 24, 3, 1, 998244359987710471])]
for args, want in ex:
    got = optimal(*args)
    assert got == want == brute(*args)
    print(args, '->', got)

random.seed(2)
for _ in range(500):
    a, b = random.randint(1, 200), random.randint(1, 200)
    nums = [random.randint(1, 200) for _ in range(random.randint(1, 5))]
    assert optimal(a, b, nums) == brute(a, b, nums)
print('random cross-check ok: 500 cases')

# claim: for all 1 <= a, b <= 100 the max step count is 10, reached by (55, 89)
best = max(euclid(a, b)[1] for a in range(1, 101) for b in range(1, 101))
arg = [(a, b) for a in range(1, 101) for b in range(1, 101) if euclid(a, b)[1] == best]
print('max steps for 1..100:', best, 'at', arg)
assert best == 10 and (55, 89) in arg
# (89, 55) takes one step less: smaller-first costs the extra swap
assert euclid(89, 55)[1] == 9 and euclid(55, 89)[1] == 10
# gcd * lcm == a * b exhaustively
assert all(math.gcd(a, b) * math.lcm(a, b) == a * b for a in range(1, 101) for b in range(1, 101))
print('gcd*lcm == a*b for all pairs up to 100; math.gcd(0, 0) =', math.gcd(0, 0))
# edge and size checks
assert optimal(1, 1, [1]) == [1, 1, 1, 1, 1]
big = optimal(10**18, 10**18 - 1, list(range(10**12 - 999, 10**12 + 1)))
print('max-size a,b: gcd', big[0], 'steps', big[2], 'lcm_all bits', big[4].bit_length())
assert big[0] == 1 and big[1] == 10**18 * (10**18 - 1)
```

**Output (my run):**
```
(48, 18, [4, 6, 10]) -> [6, 144, 3, 2, 60]
(13, 21, [7]) -> [1, 273, 7, 7, 7]
(5, 5, [2, 3, 5, 7, 11]) -> [5, 5, 1, 1, 2310]
(8, 12, [1000000007, 998244353]) -> [4, 24, 3, 1, 998244359987710471]
random cross-check ok: 500 cases
max steps for 1..100: 10 at [(55, 89)]
gcd*lcm == a*b for all pairs up to 100; math.gcd(0, 0) = 0
max-size a,b: gcd 1 steps 2 lcm_all bits 32174
```
The max-size line shows the last example of the prompt's limits: `lcm_all` of 1000 consecutive numbers near 10^12 is a 32,174-bit integer. I first tried to print its decimal digits and hit `ValueError: Exceeds the limit (4300 digits)` on Python 3.13. That is the int-to-str digit limit. That it arrived in 3.11 is editor knowledge; the error itself I saw on 3.13. So print `.bit_length()`, not `str()`, for such numbers.

**Edge cases:**
- a == b: one step.
- a < b: first step swaps.
- a divides b: gcd is a, 2 steps (or 1 if equal).
- Coprime: gcd 1, lcm = a * b.
- One-element list: gcd = lcm = the element.
- `math.gcd(0, 0) = 0`; never reached here since all values are at least 1.

**Follow-ups:**
- *Extended Euclid?* Track coefficients so that `a*x + b*y = g`. Gives modular inverses without Fermat.
- *Why gcd * lcm = a * b?* Exponent of each prime: min + max = sum. I asserted it for all pairs up to 100.
- *Binary GCD?* Uses shifts and subtraction. Same big-O in bits; rarely needed in Python.

**Common mistakes:**
- `a * b // g`: fine in Python, an overflow bug in C++/Java.
- Folding `lcm_all` from 0 (lcm(0, x) is 0).
- Claiming Fibonacci pairs are the worst case without saying smaller-first adds a step.
- Calling `math.gcd` when the interviewer asked for the loop.

---

### Q3 ⭐⭐⭐ 🟢 Trailing zeroes of n factorial. `n` is an integer with 0 <= n <= 10^18 and `base` is an integer with 2 <= base <= 100. Return `[z10, zb]`: the number of trailing zeroes of n! written in base 10, and in base `base`. Do not compute n!. For base 10 count the factors of 5 with `n // 5 + n // 25 + n // 125 + ...` and explain why factors of 2 never run out (there are at least as many); for a general base factor `base` into prime powers p^e and take the minimum over its primes of `floor(v_p(n!) / e)`, where `v_p(n!) = n // p + n // p^2 + ...`. Give the number of loop rounds for n = 10^18 in base 10 (the largest k with 5^k <= n) and say why the answer is the same for n and n + 1 unless n + 1 is a multiple of 5. In the answer include a dry run on the first example and a seeded random cross-check of your solution against computing n! with math.factorial and counting zeros by repeated division on small inputs. Example: n=25, base=10 -> [6, 6]; n=0, base=2 -> [0, 0]; n=100, base=12 -> [24, 48]; n=10, base=16 -> [2, 2].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Count prime factors of n! with Legendre's formula, never build n!.

**Say this first (1 line):** "A trailing zero is a factor of the base. For base 10 count 5s, because 2s never run out; for any base take the minimum over its primes of `v_p(n!) // e`."

**Brute force:**
- Compute `math.factorial(n)` and divide by the base while it divides.
- n = 10^18 has about 10^19 digits. Impossible. Used here only as the oracle for small n.

**Optimal:**
- `v_p(n!) = n//p + n//p^2 + n//p^3 + ...`. Each multiple of p contributes one factor, each multiple of p^2 one more, and so on.
- Base 10 = 2 * 5. Zeros = min(v_2, v_5) = v_5, because v_2 >= v_5 (checked for every n up to 10000; reason: every 5th number has a 5, every 2nd number has a 2).
- General base = product of p^e. You can strip the base k times when every prime has p^(e*k) available, so zeros = min over primes of `v_p // e`. Example: 12 = 2^2 * 3, so min(v_2 // 2, v_3 // 1).
- Number of rounds for n = 10^18 in base 10: the largest k with 5^k <= n is k = 25 (5^25 is about 2.98e17, 5^26 is about 1.49e18). The loop `while n: n //= 5` actually runs 26 times because the 26th division produces the 0 that ends the loop and adds 0. So 25 non-zero terms, 26 loop passes. The answer is 249999999999999995.
- Why n and n + 1 give the same count unless n + 1 is a multiple of 5: n! and (n+1)! differ by the factor n + 1, which brings new 5s only if 5 divides it. Verified for n up to 5000.

**Complexity:**
- Base 10: O(log_5 n) rounds.
- General base: factoring base by trial division is O(sqrt(base)) = at most 10 steps for base <= 100, then O(log_p n) per prime.
- Space O(1).

**Dry run:** `n=25, base=10`: 25 // 5 = 5, 25 // 25 = 1, then 25 // 125 = 0. Total 6. Twos: 12 + 6 + 3 + 1 = 22, more than 6, fine. Check: 25! = 15511210043330985984000000 ends in six zeros.
Second: `n=100, base=12 = 2^2 * 3`: v_2(100!) = 50+25+12+6+3+1 = 97, 97 // 2 = 48. v_3 = 33+11+3+1 = 48, 48 // 1 = 48. Minimum 48.

**Code:**
```python
import math, random

def factor(b):
    f, d = {}, 2
    while d * d <= b:
        while b % d == 0:
            f[d] = f.get(d, 0) + 1
            b //= d
        d += 1
    if b > 1:
        f[b] = f.get(b, 0) + 1
    return f

def vfact(n, p):                          # exponent of prime p in n! (Legendre)
    c = 0
    while n:
        n //= p
        c += n
    return c

def trailing(n, base):                    # zeros of n! in the given base
    return min(vfact(n, p) // e for p, e in factor(base).items())

def optimal(n, base):
    return [trailing(n, 10), trailing(n, base)]

def brute(n, base):
    f = math.factorial(n)
    def tz(x, b):
        c = 0
        while x % b == 0:
            x //= b
            c += 1
        return c
    return [tz(f, 10), tz(f, base)]

for (n, base), want in [((25, 10), [6, 6]), ((0, 2), [0, 0]), ((100, 12), [24, 48]), ((10, 16), [2, 2])]:
    got = optimal(n, base)
    assert got == want == brute(n, base)
    print(n, base, '->', got)

# exhaustive on small inputs: every n in 0..150 and every base in 2..100
for n in range(151):
    for base in range(2, 101):
        assert optimal(n, base) == brute(n, base)
print('exhaustive check ok: n in 0..150, base in 2..100')

# claim: factors of 2 never run out (n up to 10000)
assert all(vfact(n, 2) >= vfact(n, 5) for n in range(10001))
# claim: z10(n+1) != z10(n) exactly when n+1 is a multiple of 5
assert all((vfact(n + 1, 5) != vfact(n, 5)) == ((n + 1) % 5 == 0) for n in range(5000))
# 10**18: largest k with 5**k <= n, and loop rounds of `while n: n //= 5`
k = 0
while 5 ** (k + 1) <= 10**18:
    k += 1
n, rounds = 10**18, 0
while n:
    n //= 5
    rounds += 1
print('largest k with 5**k <= 10**18:', k, ' loop rounds (while n):', rounds,
      ' z10 =', vfact(10**18, 5))
assert k == 25 and rounds == 26
print('big base 97 :', optimal(10**18, 97), ' base 64:', optimal(10**18, 64))
```

**Output (my run):**
```
25 10 -> [6, 6]
0 2 -> [0, 0]
100 12 -> [24, 48]
10 16 -> [2, 2]
exhaustive check ok: n in 0..150, base in 2..100
largest k with 5**k <= 10**18: 25  loop rounds (while n): 26  z10 = 249999999999999995
big base 97 : [249999999999999995, 10416666666666661]  base 64: [249999999999999995, 166666666666666662]
```
The exhaustive line covers every n in 0..150 and every base in 2..100 against the factorial oracle (about 15,000 pairs), not a sample.

**Edge cases:**
- n = 0 or 1: 0! = 1! = 1, zero zeroes.
- Prime base larger than n: zero.
- Base that is a perfect power (4, 8, 16, 64): the `// e` matters. 10! in base 16: v_2 = 8, 8 // 4 = 2 (matches the example).
- Huge n: plain integer loop, no overflow in Python. In C++ use 64-bit and watch `p^k` overflowing; divide n repeatedly instead of multiplying p.

**Follow-ups:**
- *Smallest n whose n! has k trailing zeroes?* Binary search on n, since the count is monotone.
- *Last non-zero digit of n!?* Remove factors of 2 and 5 separately, work modulo 10. Harder.
- *Count of divisors in n!?* Product of (v_p + 1) over primes <= n.

**Common mistakes:**
- Using only `n // 5`, missing 25, 125.
- Computing 5^k in a loop with fixed-width ints that overflow.
- For base 12 saying "count 2s and 3s" without dividing by the exponent.
- Calling `math.factorial` on 10^18.

---

### Q4 ⭐⭐⭐ 🟡 Range addition with a difference array. `n` is the length of an array that starts as all zeros (1 <= n <= 10^5) and `updates` is a list of up to 10^5 triples [l, r, v] with 0 <= l <= r < n and |v| <= 10^4; update [l, r, v] adds v to every element from index l to index r inclusive. Return the final array after all updates in O(n + len(updates)) time: keep `d` of length n + 1, do `d[l] += v` and `d[r + 1] -= v`, then one running prefix sum over `d` gives the values. Explain why the final array is the prefix sum of `d`, why the updates can be applied in any order, and why `d` needs length n + 1 (or a guard) when r = n - 1. State what breaks if the updates are interleaved with queries for the current value (you would need a Fenwick or segment tree; those belong to Part 14, only name them here). In the answer include a dry run on the first example and a seeded random cross-check of your solution against applying each update with a plain loop over l..r on small inputs. Example: n=5, updates=[[1, 3, 2], [2, 4, 3], [0, 2, -2]] -> [-2, 0, 3, 5, 3]; n=1, updates=[[0, 0, 5]] -> [5]; n=4, updates=[] -> [0, 0, 0, 0].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Difference array. Many range additions, one read at the end. Store the changes at the boundaries, then prefix-sum once.

**Say this first (1 line):** "For `[l, r, v]` I add v at `d[l]` and subtract it at `d[r + 1]`; one running sum over `d` is the final array."

**Brute force:**
- Loop `l..r` for every update. O(n) per update, O(n * u) total. About 10^10 for the limits.

**Optimal:**
- `d` has length n + 1. `d[l] += v` says "from l onward, everything is v higher". `d[r + 1] -= v` says "from r + 1 onward, cancel it".
- Final value at i = `d[0] + ... + d[i]`, so the array is the prefix sum of `d`. Each update contributes exactly v to the positions l..r and 0 elsewhere.
- Addition commutes, so the order of updates does not matter (checked in the code by shuffling).
- Length n + 1: when `r = n - 1`, the write goes to `d[n]`. The code shows the IndexError you get otherwise. Alternative: skip the write when `r + 1 == n`.
- If reads are mixed with updates ("current value at i, now"), a difference array needs a prefix sum per read, O(n). Use a Fenwick or segment tree. Those are Part 14, only named here.

**Complexity:** O(n + u) time, O(n) space.

**Dry run:** `n = 5`, `d = [0, 0, 0, 0, 0, 0]`.
- `[1, 3, 2]`: `d[1] += 2`, `d[4] -= 2`.
- `[2, 4, 3]`: `d[2] += 3`, `d[5] -= 3`.
- `[0, 2, -2]`: `d[0] -= 2`, `d[3] += 2`.
- `d = [-2, 2, 3, 2, -2, -3]`. Running sums: -2, 0, 3, 5, 3. Matches the example.

**Code:**
```python
import random

def brute(n, updates):
    a = [0] * n
    for l, r, v in updates:
        for i in range(l, r + 1):
            a[i] += v
    return a

def optimal(n, updates):
    d = [0] * (n + 1)                     # length n + 1: r + 1 may equal n
    for l, r, v in updates:
        d[l] += v
        d[r + 1] -= v
    out, run = [], 0
    for i in range(n):
        run += d[i]                       # prefix sum of d = the array
        out.append(run)
    return out

for (n, ups), want in [((5, [[1, 3, 2], [2, 4, 3], [0, 2, -2]]), [-2, 0, 3, 5, 3]),
                       ((1, [[0, 0, 5]]), [5]), ((4, []), [0, 0, 0, 0])]:
    got = optimal(n, ups)
    assert got == want == brute(n, ups)
    print(n, ups, '->', got)

random.seed(4)
for _ in range(500):
    n = random.randint(1, 12)
    ups = []
    for _ in range(random.randint(0, 8)):
        l = random.randint(0, n - 1)
        ups.append([l, random.randint(l, n - 1), random.randint(-9, 9)])
    assert optimal(n, ups) == brute(n, ups)
    shuffled = ups[:]
    random.shuffle(shuffled)
    assert optimal(n, shuffled) == optimal(n, ups)       # order does not matter
print('random cross-check ok: 500 cases, order-independence ok')

# exhaustive: every single update on n = 6 (all l, r, v in -2..2)
n = 6
for l in range(n):
    for r in range(l, n):
        for v in range(-2, 3):
            assert optimal(n, [[l, r, v]]) == brute(n, [[l, r, v]])
print('every single update on n=6 ok (incl. r = n - 1, which writes d[n])')

# a version without the extra slot fails at r = n - 1
try:
    d = [0] * 3
    d[2 + 1] -= 1
except IndexError as e:
    print('d of length n raises:', e)
# max size
import time
n = 10**5
ups = [[l, random.randint(l, n - 1), random.randint(-10**4, 10**4)] for l in (random.randint(0, n - 1) for _ in range(10**5))]
t = time.perf_counter(); res = optimal(n, ups); dt = time.perf_counter() - t
assert len(res) == n
print('max size done (sandbox timing only, not a proof):', 'under 1s' if dt < 1 else 'over 1s')
```

**Output (my run):**
```
5 [[1, 3, 2], [2, 4, 3], [0, 2, -2]] -> [-2, 0, 3, 5, 3]
1 [[0, 0, 5]] -> [5]
4 [] -> [0, 0, 0, 0]
random cross-check ok: 500 cases, order-independence ok
every single update on n=6 ok (incl. r = n - 1, which writes d[n])
d of length n raises: list index out of range
max size done (sandbox timing only, not a proof): under 1s
```
The timing line is sandbox-only and says nothing about big-O; the big-O comes from the single pass over `d` and one pass over `updates`.

**Edge cases:**
- No updates: all zeros.
- `l == r`: a single cell.
- `r = n - 1`: needs `d[n]`.
- Negative v, and updates that cancel each other.
- n = 1.

**Follow-ups:**
- *2D version?* Four corner updates on a 2D difference array, then a 2D prefix sum. Same idea, one dimension up.
- *Car pooling / flight bookings?* The same pattern: +passengers at the start, -passengers at the end.
- *Need to know a value in the middle of the updates?* Fenwick tree with range update, point query.

**Common mistakes:**
- `d` of length n (crashes on `r = n - 1`).
- Subtracting at `d[r]` instead of `d[r + 1]` (the update would stop one cell early).
- Forgetting to prefix-sum at the end and returning `d`.
- Reading a value before the final pass.

---

### Q5 ⭐⭐⭐ 🟡 Region sum queries on an immutable matrix (2D prefix sums). `matrix` is an m x n list of lists of integers (1 <= m, n <= 200, |value| <= 10^4) that never changes and `queries` has up to 10^5 items [r1, c1, r2, c2] with 0 <= r1 <= r2 < m and 0 <= c1 <= c2 < n; return the sum of the sub-rectangle with corners (r1, c1) and (r2, c2), both included, for every query, in O(1) per query after an O(m * n) build. Use a table `P` of size (m + 1) x (n + 1) with `P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]` and the query `P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]`. Explain both formulas by inclusion-exclusion (which rectangle is subtracted twice and so added back) and why the extra zero row and column remove the edge cases. Part 1 Q50 reuses a row-pair collapse to count submatrices with a target sum; this question is the plain static region query. In the answer include a dry run on the first example and a seeded random cross-check of your solution against summing the rectangle cell by cell on small inputs. Example: matrix=[[3, 0, 1], [5, 6, 3], [1, 2, 0]], queries=[[0, 0, 2, 2], [1, 1, 2, 2], [1, 0, 1, 0]] -> [21, 11, 5]; matrix=[[-4]], queries=[[0, 0, 0, 0]] -> [-4]; matrix=[[1, 2], [3, 4]], queries=[[0, 1, 1, 1], [0, 0, 0, 1]] -> [6, 3].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** 2D prefix sums. Static matrix, many rectangle sums. Inclusion-exclusion on a table with a zero border.

**Say this first (1 line):** "`P[i][j]` is the sum of the top-left i-by-j block; a rectangle is big minus two strips plus the corner they both removed."

**Brute force:**
- Add up every cell in the rectangle for each query. O(m * n) per query, which is 40,000 cells times 10^5 queries.

**Optimal:**
- `P` is (m + 1) x (n + 1). `P[i][j]` = sum of `matrix[0..i-1][0..j-1]`.
- Build: `P[i+1][j+1] = matrix[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]`. The block above plus the block to the left both contain the block above-left, so that block was counted twice: subtract it once.
- Query: `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`. Take the big block from the origin. Remove the strip above the rectangle and the strip to its left. The top-left corner block was removed twice, so add it back once.
- The zero row 0 and zero column 0 make `r1 = 0` or `c1 = 0` just read zeros, so no `if` for the edges.
- Part 1 Q50 collapses row pairs to count submatrices with a target sum. This question is the plain static query.

**Complexity:** Build O(m * n). Each query O(1). Space O(m * n).

**Dry run:** matrix `[[3,0,1],[5,6,3],[1,2,0]]`.
- Row 1 of P: `[0, 3, 3, 4]`. Row 2: `[0, 8, 14, 18]`. Row 3: `[0, 9, 17, 21]`.
- Check `P[2][2]` = 6 + P[1][2] + P[2][1] - P[1][1] = 6 + 3 + 8 - 3 = 14.
- Query `[1, 1, 2, 2]`: `P[3][3] - P[1][3] - P[3][1] + P[1][1]` = 21 - 4 - 9 + 3 = 11.
- Query `[1, 0, 1, 0]`: `P[2][1] - P[1][1] - P[2][0] + P[1][0]` = 8 - 3 - 0 + 0 = 5.
- Query `[0, 0, 2, 2]`: `P[3][3]` = 21.

**Code:**
```python
import random

def brute(matrix, queries):
    return [sum(matrix[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
            for r1, c1, r2, c2 in queries]

def optimal(matrix, queries):
    m, n = len(matrix), len(matrix[0])
    P = [[0] * (n + 1) for _ in range(m + 1)]            # zero row 0 and zero column 0
    for i in range(m):
        for j in range(n):
            P[i + 1][j + 1] = matrix[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    return [P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
            for r1, c1, r2, c2 in queries]

ex = [([[3, 0, 1], [5, 6, 3], [1, 2, 0]], [[0, 0, 2, 2], [1, 1, 2, 2], [1, 0, 1, 0]], [21, 11, 5]),
      ([[-4]], [[0, 0, 0, 0]], [-4]),
      ([[1, 2], [3, 4]], [[0, 1, 1, 1], [0, 0, 0, 1]], [6, 3])]
for M, qs, want in ex:
    got = optimal(M, qs)
    assert got == want == brute(M, qs)
    print(M, qs, '->', got)

random.seed(5)
for _ in range(500):
    m, n = random.randint(1, 6), random.randint(1, 6)
    M = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    qs = []
    for _ in range(random.randint(0, 8)):
        r1 = random.randint(0, m - 1); r2 = random.randint(r1, m - 1)
        c1 = random.randint(0, n - 1); c2 = random.randint(c1, n - 1)
        qs.append([r1, c1, r2, c2])
    assert optimal(M, qs) == brute(M, qs)
print('random cross-check ok: 500 cases')

# exhaustive: every rectangle of a fixed 4 x 5 matrix
M = [[random.randint(-9, 9) for _ in range(5)] for _ in range(4)]
allq = [[a, b, c, d] for a in range(4) for c in range(a, 4) for b in range(5) for d in range(b, 5)]
assert optimal(M, allq) == brute(M, allq)
print('all', len(allq), 'rectangles of a 4x5 matrix ok')

# max-size: 200 x 200, whole-matrix query equals sum of everything; |value| <= 10^4
M = [[random.randint(-10**4, 10**4) for _ in range(200)] for _ in range(200)]
assert optimal(M, [[0, 0, 199, 199]]) == [sum(map(sum, M))]
assert optimal(M, [[0, 0, 0, 0], [199, 199, 199, 199]]) == [M[0][0], M[199][199]]
print('max size 200x200 ok')
```

**Output (my run):**
```
[[3, 0, 1], [5, 6, 3], [1, 2, 0]] [[0, 0, 2, 2], [1, 1, 2, 2], [1, 0, 1, 0]] -> [21, 11, 5]
[[-4]] [[0, 0, 0, 0]] -> [-4]
[[1, 2], [3, 4]] [[0, 1, 1, 1], [0, 0, 0, 1]] -> [6, 3]
random cross-check ok: 500 cases
all 150 rectangles of a 4x5 matrix ok
max size 200x200 ok
```
The exhaustive line checks all 150 rectangles of a 4x5 matrix, the seeded loop checks 500 random matrices.

**Edge cases:**
- 1x1 matrix.
- Query on the first row or first column (zeros in `P` handle it).
- Whole-matrix query (`P[m][n]`).
- Negative entries (no change to the algorithm).
- Zero queries.

**Follow-ups:**
- *Matrix values change?* Point update would need rebuilding O(m * n); use a 2D Fenwick tree (Part 14, named only). 
- *Add to many rectangles, read at the end?* 2D difference array: +v at (r1, c1), -v at (r1, c2+1) and (r2+1, c1), +v at (r2+1, c2+1).
- *Matrix block sum?* Same table; clamp the block to the borders.

**Common mistakes:**
- Forgetting to add back `P[r1][c1]`.
- Using `P` of size m x n and writing edge-case `if`s.
- Indexing the query with `r2` instead of `r2 + 1`.
- Building `P` by adding row prefix sums without the corner correction.

---

### Q6 ⭐⭐⭐ 🟡 Rotate an n x n matrix by 90 degrees clockwise in place. `matrix` is a list of n lists of n integers (1 <= n <= 200). Modify it in place using O(1) extra space and also return the same list object. Do it as a transpose (swap `matrix[i][j]` with `matrix[j][i]` for j > i) followed by reversing every row, and explain why that equals a clockwise quarter turn; say what you change for an anticlockwise turn (transpose, then reverse the order of the rows). Mention that `[list(r) for r in zip(*matrix[::-1])]` is correct but builds a new matrix with O(n^2) extra space, so it does not meet the in-place requirement. A cell at (i, j) moves to (j, n - 1 - i); state the 4-cell cycle this gives and why the starting cells with i < n // 2 and j < (n + 1) // 2 cover every 4-cell cycle exactly once if you rotate cycle by cycle (for odd n the centre cell stays where it is). In the answer include a dry run on the first example and a seeded random cross-check of your solution against the zip-based rotation on small inputs. Example: matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]; matrix=[[5]] -> [[5]]; matrix=[[1, 2], [3, 4]] -> [[3, 1], [4, 2]]; matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]] -> [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** In-place matrix transformation. Rotation = transpose + reverse each row.

**Say this first (1 line):** "Swap across the main diagonal, then reverse every row. That is a clockwise quarter turn in O(1) extra space."

**Brute force:**
- Build a new matrix: `[list(r) for r in zip(*matrix[::-1])]`. Correct, but O(n^2) extra space, so it breaks the in-place rule.

**Optimal:**
- Transpose: swap `matrix[i][j]` with `matrix[j][i]` for `j > i` (only the upper triangle, otherwise you swap everything back).
- Then reverse each row. Why: a cell at (i, j) goes to (j, i) after the transpose. Reversing row j sends column i to column n - 1 - i. So (i, j) ends at (j, n - 1 - i). That is exactly the clockwise turn (verified for n = 1..9 in the code).
- Anticlockwise: transpose, then reverse the order of the rows (verified as the same as three clockwise turns).
- Cycle form: (i, j) -> (j, n-1-i) -> (n-1-i, n-1-j) -> (n-1-j, i) -> (i, j). Four cells move in a loop. Start cells with `i < n // 2` and `j < (n + 1) // 2` cover every 4-cycle exactly once (I enumerated n = 1..9: the cycles are disjoint and cover n*n cells, minus the centre when n is odd). The centre of an odd matrix is a fixed point.
- Return the same list object.

**Complexity:** O(n^2) time (every cell is touched a constant number of times). O(1) extra space.

**Dry run:** `[[1,2,3],[4,5,6],[7,8,9]]`.
- Transpose: swap (0,1)<->(1,0), (0,2)<->(2,0), (1,2)<->(2,1): `[[1,4,7],[2,5,8],[3,6,9]]`.
- Reverse each row: `[[7,4,1],[8,5,2],[9,6,3]]`. Matches.
- Cycle form, start (0,0): the corners 1, 7, 9, 3 move one corner clockwise. Start (0,1): edges 2, 4, 8, 6 move. The centre 5 stays.

**Code:**
```python
import random, copy

def brute(matrix):                                       # new matrix, O(n^2) extra space
    return [list(r) for r in zip(*matrix[::-1])]

def optimal(matrix):                                     # transpose, then reverse each row
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix

def cycles(matrix):                                      # alternative: rotate 4-cell cycles
    n = len(matrix)
    for i in range(n // 2):
        for j in range((n + 1) // 2):
            tmp = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = matrix[i][j]
            matrix[i][j] = tmp
    return matrix

ex = [([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
      ([[5]], [[5]]), ([[1, 2], [3, 4]], [[3, 1], [4, 2]]),
      ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
       [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]])]
for M, want in ex:
    m = copy.deepcopy(M)
    got = optimal(m)
    assert got is m and got == want == brute(M) == cycles(copy.deepcopy(M))
    print(M, '->', got)

random.seed(6)
for _ in range(500):
    n = random.randint(1, 7)
    M = [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]
    a = copy.deepcopy(M)
    assert optimal(a) == brute(M) == cycles(copy.deepcopy(M))
print('random cross-check ok: 500 cases (transpose+reverse, cycles, zip all agree)')

# claims, exhaustive over n = 1..9 with distinct labels
for n in range(1, 10):
    M = [[i * n + j for j in range(n)] for i in range(n)]
    cw = optimal(copy.deepcopy(M))
    assert all(cw[j][n - 1 - i] == M[i][j] for i in range(n) for j in range(n))   # (i,j) -> (j, n-1-i)
    # anticlockwise = transpose, then reverse the order of the rows
    ccw = [list(r) for r in zip(*M)][::-1]
    assert optimal(optimal(optimal(copy.deepcopy(M)))) == ccw
    seen = set()
    for i in range(n // 2):
        for j in range((n + 1) // 2):
            cyc = {(i, j), (j, n - 1 - i), (n - 1 - i, n - 1 - j), (n - 1 - j, i)}
            assert len(cyc) == 4 and not (cyc & seen)
            seen |= cyc
    assert len(seen) == n * n - n % 2                     # centre cell of odd n is left out
    assert (n // 2) * ((n + 1) // 2) * 4 == n * n - n % 2
print('claims ok for n=1..9: destination (j, n-1-i), anticlockwise recipe, 4-cycles cover each cell once, centre stays')
# four turns = identity
M = [[random.randint(0, 99) for _ in range(5)] for _ in range(5)]
r = copy.deepcopy(M)
for _ in range(4):
    optimal(r)
assert r == M
# max size
M = [[random.randint(-9, 9) for _ in range(200)] for _ in range(200)]
assert optimal(copy.deepcopy(M)) == brute(M)
print('max size 200x200 ok; four turns restore the matrix')
```

**Output (my run):**
```
[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
[[5]] -> [[5]]
[[1, 2], [3, 4]] -> [[3, 1], [4, 2]]
[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]] -> [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
random cross-check ok: 500 cases (transpose+reverse, cycles, zip all agree)
claims ok for n=1..9: destination (j, n-1-i), anticlockwise recipe, 4-cycles cover each cell once, centre stays
max size 200x200 ok; four turns restore the matrix
```

**Edge cases:**
- n = 1: nothing moves.
- n = 2: one 4-cycle.
- Odd n: centre stays.
- Four rotations give the original (asserted).
- Non-square input: not in place; the result has different dimensions.

**Follow-ups:**
- *180 degrees?* Reverse the rows, then reverse each row.
- *Rotate by k * 90?* `k % 4` times, or compose the right mapping directly.
- *Rectangular matrix?* A new matrix is needed because the shape changes.

**Common mistakes:**
- Swapping all (i, j) in the transpose (undoes itself).
- Mixing up the two finishing steps: transpose then reverse each row is clockwise; transpose then reverse the order of the rows is anticlockwise.
- Using `matrix = zip(...)` inside a function and thinking the caller's list changed.
- Cycle loop bounds `range(n)` for both loops (rotates every cell four times).

---

### Q7 ⭐⭐⭐ 🟡 Spiral order of a matrix. `matrix` is an m x n list of lists of integers (1 <= m, n <= 100). Return all m * n elements in clockwise spiral order starting at the top-left cell: along the top row to the right, down the right column, back along the bottom row to the left, up the left column, then repeat on the inner layer. Use four shrinking boundaries `top, bottom, left, right`. The classic bug is on a layer that is a single row (2 or more cells) or a single column (3 or more cells), where the third and fourth loops would walk over cells that were already visited and the result has too many elements; show the guard that prevents it. A visited-set simulation with direction changes is the alternative; compare their space. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a visited-set direction-turning simulation on small inputs. Example: matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 3, 6, 9, 8, 7, 4, 5]; matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]] -> [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]; matrix=[[1], [2], [3]] -> [1, 2, 3]; matrix=[[1, 2, 3]] -> [1, 2, 3].
**Asked at:** Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)

**Pattern:** Boundary-shrinking traversal of a grid. Four pointers, one layer per round.

**Say this first (1 line):** "Walk top row, right column, bottom row, left column, shrink the four borders, and guard the last two walks when the layer is a single row or column."

**Brute force / alternative:**
- Simulate: start at (0, 0) heading right, mark cells in a visited set, turn right whenever the next cell is outside or already visited, stop after m * n cells.
- Correct and simple. O(m * n) time and O(m * n) extra space for the set.

**Optimal:**
- `top, bottom, left, right` start at the borders. Each round walks:
  1. top row, left to right;
  2. right column, top + 1 down to bottom;
  3. bottom row, right - 1 back to left;
  4. left column, bottom - 1 up to top + 1.
  Then `top += 1; bottom -= 1; left += 1; right -= 1`.
- The bug: if the layer is a single row (2 or more cells) step 3 walks the same row backwards, and if it is a single column (3 or more cells) step 4 walks it backwards. Cells are output twice.
- The guard: do steps 3 and 4 only when `top < bottom and left < right`.
- I enumerated every shape up to 9 x 9. The unguarded code returns the wrong length for exactly 36 of 81 shapes: those where `min(m, n)` is odd and either `n > m` or `m - n >= 2` (the innermost layer is a single row of 2+ cells or a single column of 3+ cells). A 2 x 1 and a 1 x 1 are fine unguarded.

**Complexity:** O(m * n) time, each cell visited once. Extra space O(1) beyond the output (the visited-set version uses O(m * n) more).

**Dry run:** 3 x 3.
- Round 1: top row 1, 2, 3. Right column rows 1..2: 6, 9. Guard true (top < bottom, left < right): bottom row from col 1 to 0: 8, 7. Left column rows 1..1: 4.
- Shrink: top = bottom = 1, left = right = 1. Round 2: top row: 5. Right column range(2, 2): empty. Guard false (top == bottom), so no backward walks.
- Result 1, 2, 3, 6, 9, 8, 7, 4, 5.

**Code:**
```python
import random

def brute(matrix):                                       # visited set + direction turning, O(mn) extra space
    m, n = len(matrix), len(matrix[0])
    seen, out, i, j, di, dj = set(), [], 0, 0, 0, 1
    for _ in range(m * n):
        out.append(matrix[i][j]); seen.add((i, j))
        ni, nj = i + di, j + dj
        if not (0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen):
            di, dj = dj, -di                             # turn right
            ni, nj = i + di, j + dj
        i, j = ni, nj
    return out

def optimal(matrix):                                     # four boundaries, O(1) extra space
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            out.append(matrix[top][j])
        for i in range(top + 1, bottom + 1):
            out.append(matrix[i][right])
        if top < bottom and left < right:                # guard: layer has 2+ rows AND 2+ columns
            for j in range(right - 1, left - 1, -1):
                out.append(matrix[bottom][j])
            for i in range(bottom - 1, top, -1):
                out.append(matrix[i][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out

def no_guard(matrix):                                    # the classic bug
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1): out.append(matrix[top][j])
        for i in range(top + 1, bottom + 1): out.append(matrix[i][right])
        for j in range(right - 1, left - 1, -1): out.append(matrix[bottom][j])
        for i in range(bottom - 1, top, -1): out.append(matrix[i][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out

ex = [([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 2, 3, 6, 9, 8, 7, 4, 5]),
      ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]),
      ([[1], [2], [3]], [1, 2, 3]), ([[1, 2, 3]], [1, 2, 3])]
for M, want in ex:
    got = optimal(M)
    assert got == want == brute(M)
    print(M, '->', got)

random.seed(7)
for _ in range(500):
    m, n = random.randint(1, 6), random.randint(1, 6)
    M = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    assert optimal(M) == brute(M)
print('random cross-check ok: 500 cases')

# exhaustive over every shape up to 9 x 9: each cell exactly once, and the guard matters
bad = []
for m in range(1, 10):
    for n in range(1, 10):
        M = [[i * n + j for j in range(n)] for i in range(m)]
        assert sorted(optimal(M)) == list(range(m * n)) and optimal(M) == brute(M)
        if len(no_guard(M)) != m * n:
            bad.append((m, n))
print('shapes where the unguarded version returns the wrong length:', bad[:6], '...', len(bad), 'of 81')
# exact rule: the innermost layer is a single row of 2+ cells or a single column of 3+ cells
# (min(m, n) odd, and n > m, or m - n >= 2)
rule = {(m, n) for m in range(1, 10) for n in range(1, 10) if min(m, n) % 2 == 1 and (n > m or m - n >= 2)}
assert set(bad) == rule
print('bad shapes match the rule exactly:', len(rule), 'shapes; 2 x 1 and 1 x 1 are fine:', (2, 1) not in bad and (1, 1) not in bad)
```

**Output (my run):**
```
[[1, 2, 3], [4, 5, 6], [7, 8, 9]] -> [1, 2, 3, 6, 9, 8, 7, 4, 5]
[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]] -> [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
[[1], [2], [3]] -> [1, 2, 3]
[[1, 2, 3]] -> [1, 2, 3]
random cross-check ok: 500 cases
shapes where the unguarded version returns the wrong length: [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)] ... 36 of 81
bad shapes match the rule exactly: 36 shapes; 2 x 1 and 1 x 1 are fine: True
```

**Edge cases:**
- 1 x 1.
- Single row (1 x n) and single column (m x 1): the guard.
- 2 x 2 and other even squares: the last layer is a 2 x 2.
- Odd squares: the last layer is one cell.
- Non-square shapes where the inner layer becomes a row or a column.

**Follow-ups:**
- *Spiral II: fill an n x n matrix with 1..n^2 in spiral order?* Same loop, write instead of read.
- *Counter-clockwise or start elsewhere?* Swap the direction order.
- *Why not a visited set?* It costs O(m * n) space and a set lookup per move; the boundaries need neither.

**Common mistakes:**
- No guard: duplicates on a single row or column.
- Using only the loop condition `top <= bottom and left <= right` and assuming it stops steps 3 and 4 (it does not; they need their own `top < bottom and left < right` test).
- Off-by-one in the ranges (right column starts at `top + 1`, bottom row starts at `right - 1`).
- Assuming m == n.

---

### Q8 ⭐⭐⭐ 🟡 Count primes below n with the sieve of Eratosthenes. `n` is an integer with 0 <= n <= 5*10^6. Return `[count, marks]`: `count` is the number of primes strictly less than n, and `marks` is the number of composite-marking steps of this exact sieve: a `bytearray` flags 0..n-1, and for every p = 2, 3, 4, ... while p * p < n whose flag is still set, the multiples p*p, p*p + p, ... (all below n) are marked, each one costing 1 even if it was marked before; `marks` is the total over all such p. For n < 3 return `[0, 0]`. Explain why you can start at p*p (every smaller multiple has a smaller prime factor and is already marked), why the outer loop can stop at p * p < n, the memory (one byte per number here) and why the total work is about n log log n. Say why trial division of each number up to its square root is much slower for n = 5*10^6. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trial division by every d with d * d <= x on small inputs. Example: n=10 -> [4, 4]; n=2 -> [0, 0]; n=30 -> [10, 21]; n=100 -> [25, 102]; n=0 -> [0, 0].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Sieve of Eratosthenes. Cross out multiples of each prime, starting at its square.

**Say this first (1 line):** "A `bytearray` of flags; for each p with p * p < n still marked prime, cross out p*p, p*p + p, ... below n."

**Brute force:**
- For each x, trial-divide by every d with d * d <= x. About sqrt(x) checks per number.
- For n = 5*10^6 the primes alone (about 350,000 of them, each needing up to about 2,200 divisions) cost hundreds of millions of modulo operations. The sieve does about n log log n.

**Optimal:**
- Flags 0..n-1, all 1 except 0 and 1.
- For p = 2, 3, 4, ... while `p * p < n`: if `flags[p]` is still set, mark `p*p, p*p+p, ...` (all below n). Every marking costs 1, even if already marked. `marks` counts them.
- Start at `p*p`: a smaller multiple `p*k` with `k < p` has a prime factor smaller than p, so an earlier prime already crossed it out. Verified: starting at `2p` gives the same primes but more marks (654 vs 715 for n = 499).
- Stop at `p * p < n`: a composite below n has a prime factor with square at most that composite, so it was crossed out by a p with `p * p < n`.
- Memory: one byte per number, 5 MB for n = 5*10^6 (a plain Python list holds an 8-byte pointer per slot, about 40 MB).
- In the code the marking is a C-speed slice assignment `flags[p*p::p] = bytes(cnt)`; the count of marks is computed from `len(range(...))`.
- Work is the sum over primes p <= sqrt(n) of n / p, about n log log n.

**Complexity:** O(n log log n) time, O(n) space.

**Dry run:** n = 10.
- Flags for 2..9 all set. p = 2 (4 < 10): mark 4, 6, 8 (3 marks). p = 3 (9 < 10): mark 9 (1 mark). p = 4: 16 >= 10, stop.
- Still set: 2, 3, 5, 7. Count 4, marks 4. Matches `[4, 4]`.
- n = 30: p = 2 marks 13 (4..28), p = 3 marks 7 (9..27), p = 4 is already crossed, p = 5 marks 1 (25). 21 marks, 10 primes.

**Code:**
```python
import random, math

def brute(n):                                            # trial division by every d with d*d <= x
    def is_prime(x):
        return x >= 2 and all(x % d for d in range(2, math.isqrt(x) + 1))
    count = sum(1 for x in range(n) if is_prime(x))
    marks = sum(len(range(p * p, n, p)) for p in range(2, n) if p * p < n and is_prime(p))
    return [count, marks]

def optimal(n):
    if n < 3:
        return [0, 0]
    flags = bytearray([1]) * n
    flags[0] = flags[1] = 0
    marks, p = 0, 2
    while p * p < n:
        if flags[p]:
            cnt = len(range(p * p, n, p))               # multiples p*p, p*p+p, ... below n
            marks += cnt
            flags[p * p::p] = bytes(cnt)                # slice assignment = C-speed marking
        p += 1
    return [sum(flags), marks]

def sieve_loop(n, start_sq=True):                       # plain loops, to compare start points
    flags = bytearray([1]) * n
    flags[:2] = b'\x00\x00'[:min(2, n)]
    marks, p = 0, 2
    while p * p < n:
        if flags[p]:
            for x in range(p * p if start_sq else 2 * p, n, p):
                flags[x] = 0
                marks += 1
        p += 1
    return sum(flags), marks

for n, want in [(10, [4, 4]), (2, [0, 0]), (30, [10, 21]), (100, [25, 102]), (0, [0, 0])]:
    got = optimal(n)
    assert got == want == brute(n)
    print('n =', n, '->', got)

# exhaustive over every n in 0..500 (not just seeded samples) plus a seeded random batch
for n in range(501):
    assert optimal(n) == brute(n)
random.seed(8)
for _ in range(300):
    n = random.randint(0, 3000)
    assert optimal(n) == brute(n)
print('cross-check ok: every n in 0..500 and 300 seeded n up to 3000')

# claims: starting at 2p instead of p*p gives the same primes but more marks; p*p < n bound enough
for n in range(3, 500):
    c1, k1 = sieve_loop(n, True)
    c2, k2 = sieve_loop(n, False)
    assert c1 == c2 == optimal(n)[0] and k1 == optimal(n)[1] and k2 >= k1
print('start at p*p vs 2p: same count; marks for n=499:', sieve_loop(499, True)[1], 'vs', sieve_loop(499, False)[1])
# known prime counts
assert [optimal(n)[0] for n in (10, 100, 1000, 10**6)] == [4, 25, 168, 78498]
# max size
res = optimal(5 * 10**6)
print('n = 5*10**6 ->', res)
assert res[0] == 348513
# memory: one byte per flag
print('flags bytes for n = 5*10**6:', len(bytearray(5 * 10**6)))
```

**Output (my run):**
```
n = 10 -> [4, 4]
n = 2 -> [0, 0]
n = 30 -> [10, 21]
n = 100 -> [25, 102]
n = 0 -> [0, 0]
cross-check ok: every n in 0..500 and 300 seeded n up to 3000
start at p*p vs 2p: same count; marks for n=499: 654 vs 715
n = 5*10**6 -> [348513, 11192868]
flags bytes for n = 5*10**6: 5000000
```
For n = 5*10^6 there are 348,513 primes (matches the known value) and 11,192,868 marks. Cross-check: every n in 0..500 against trial division (not a sample), plus 300 seeded larger ones.

**Edge cases:**
- n = 0, 1, 2: no primes below n; return `[0, 0]`.
- n = 3: the only prime below 3 is 2; the loop does not run (4 >= 3).
- n a perfect square, say 25: p = 5 has 25 < 25 false, so 5 does not mark; 25 itself is not below n anyway.
- Slicing `flags[p*p::p]` needs the exact length for the replacement `bytes(cnt)`.

**Follow-ups:**
- *Only odd numbers?* Halve the memory. Segmented sieve for a range [lo, hi] when n is huge.
- *Smallest prime factor sieve?* Store spf, factorise any number in O(log n).
- *Is one number prime?* Trial division up to sqrt(x), or Miller-Rabin for huge x.

**Common mistakes:**
- Starting at `2 * p`.
- Running the outer loop to n.
- A list of Python ints instead of a `bytearray`.
- Forgetting 0 and 1 are not prime.
- Off-by-one: "less than n" versus "up to n".

---

### Q9 ⭐⭐⭐ 🟡 Fast power for integers. `x` is a nonzero integer with |x| <= 10 and `n` is an integer with |n| <= 300 (negative allowed). Return `[numerator, denominator, multiplications]`: x ** n as a reduced fraction with a positive denominator (so for negative n it is 1 / x^|n|, and 0 < denominator), and the number of multiplications done by exponentiation by squaring written exactly like this: `e = abs(n); result = 1; base = x`, then `while e:` do `if e & 1: result *= base` (1 multiplication), `e >>= 1`, and `if e: base *= base` (1 multiplication). For n = 0 the count is 0. Explain why this takes O(log |n|) multiplications instead of |n|, give the closed form for the count (the number of 1 bits of |n| plus its bit length minus 1), and explain the recursive halving version x^n = (x^(n/2))^2 * x^(n mod 2). Say what goes wrong in C++ or Java when n = -2^31 (negating it overflows) and why Python does not have that problem, and why `pow(x, n, m)` with three arguments is the right tool when only the remainder is needed (modular exponentiation is Q29 territory). In the answer include a dry run on the first example and a seeded random cross-check of your solution against Fraction(x) ** n and a bit-count formula on small inputs. Example: x=2, n=10 -> [1024, 1, 5]; x=3, n=-2 -> [1, 9, 2]; x=-2, n=5 -> [-32, 1, 4]; x=7, n=0 -> [1, 1, 0]; x=10, n=1 -> [10, 1, 1].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Exponentiation by squaring. Halve the exponent, square the base.

**Say this first (1 line):** "I walk the bits of |n|: multiply into the result when the bit is 1, square the base for the next bit, then take the reciprocal if n is negative."

**Brute force:**
- Multiply x by itself |n| - 1 times. O(|n|) multiplications. For n = 300 that is 299.

**Optimal:**
- `e = abs(n); result = 1; base = x`. While e: if the low bit is set, `result *= base`; shift e right; if e remains, `base *= base`.
- Why: x^n = product of x^(2^k) over the set bits k of n. The base is squared each round, so it holds x^(2^k) in round k.
- Count = (number of 1 bits of |n|) multiplications into the result + (bit length - 1) squarings. The last square is skipped by the `if e` guard. The code asserts this closed form for every |n| up to 300.
- Recursive form: x^n = (x^(n/2))^2 * x^(n mod 2). Depth is log2(n), at most 9 here, far below the recursion limit.
- Negative n: compute with |n|, then answer 1 / x^|n| as a `Fraction`, reduced and with positive denominator (the sign sits in the numerator).
- C++/Java: negating n = -2^31 overflows (2^31 does not fit in 32 bits). Python has no such issue (the code prints `abs(-2**31)`). Here |n| <= 300 anyway.
- `pow(x, n, m)` with three arguments does modular exponentiation without building the huge number (modular exponentiation is Q29 territory). I show `pow(7, 10**18, 10**9+7)` finishing instantly.

**Complexity:** O(log |n|) multiplications (at most 2 * bit_length - 1). The numbers themselves grow, so each multiply costs more as the exponent grows; for these limits it does not matter.

**Dry run:** x = 2, n = 10 (binary 1010).
- e = 10: bit 0 is 0. e = 5. base = 4 (1 mult).
- e = 5: bit is 1, result = 4 (1 mult). e = 2. base = 16 (1 mult).
- e = 2: bit 0. e = 1. base = 256 (1 mult).
- e = 1: bit is 1, result = 4 * 256 = 1024 (1 mult). e = 0. No more squaring.
- Total 5 multiplications. Closed form: popcount(10) = 2, bit length 4, 2 + 4 - 1 = 5.

**Code:**
```python
import random
from fractions import Fraction

def brute(x, n):                                         # |n| multiplications by repeated product
    e, r = abs(n), 1
    for _ in range(e):
        r *= x
    f = Fraction(1, r) if n < 0 else Fraction(r)
    return [f.numerator, f.denominator, max(e - 1, 0)]

def optimal(x, n):
    e, result, base, mult = abs(n), 1, x, 0
    while e:
        if e & 1:
            result *= base; mult += 1
        e >>= 1
        if e:
            base *= base; mult += 1
    f = Fraction(1, result) if n < 0 else Fraction(result)   # reduced, denominator > 0
    return [f.numerator, f.denominator, mult]

def pow_rec(x, e):                                       # x^e = (x^(e//2))^2 * x^(e%2), depth ~ log2(e)
    if e == 0:
        return 1
    h = pow_rec(x, e // 2)
    return h * h * (x if e & 1 else 1)

def closed_form(n):
    e = abs(n)
    return bin(e).count('1') + e.bit_length() - 1 if e else 0

for (x, n), want in [((2, 10), [1024, 1, 5]), ((3, -2), [1, 9, 2]), ((-2, 5), [-32, 1, 4]),
                     ((7, 0), [1, 1, 0]), ((10, 1), [10, 1, 1])]:
    got = optimal(x, n)
    assert got == want
    print('x =', x, 'n =', n, '->', got)

# exhaustive over the whole input space: every nonzero |x| <= 10 and every |n| <= 300
for x in [v for v in range(-10, 11) if v]:
    for n in range(-300, 301):
        got = optimal(x, n)
        f = Fraction(x) ** n
        assert got[:2] == [f.numerator, f.denominator] and got[2] == closed_form(n)
        assert got[1] > 0 and Fraction(got[0], got[1]) == f
        assert pow_rec(abs(x), abs(n)) == abs(x) ** abs(n)
        if abs(n) <= 40:
            assert brute(x, n)[:2] == got[:2]
print('exhaustive check ok: 20 values of x times 601 values of n; count equals popcount + bit_length - 1')
random.seed(9)
for _ in range(300):
    x = random.choice([v for v in range(-10, 11) if v]); n = random.randint(-40, 40)
    assert optimal(x, n)[:2] == brute(x, n)[:2]
print('seeded random cross-check vs repeated multiplication ok')

# claim: n = -2**31 overflows when negated in 32-bit C/Java; Python has no such limit
n = -2**31
print('abs(-2**31) =', abs(n), '> 2**31 - 1 =', 2**31 - 1, '(a 32-bit int cannot hold it)')
# modular exponentiation: pow with three arguments never builds the huge number
assert pow(7, 10**18, 10**9 + 7) == pow(7, 10**18 % (10**9 + 6), 10**9 + 7)   # Fermat, p prime
print('pow(7, 10**18, 10**9+7) =', pow(7, 10**18, 10**9 + 7))
# max case: x = 10, n = -300
assert optimal(10, -300) == [1, 10**300, closed_form(300)] and closed_form(300) == 4 + 9 - 1
print('x=10, n=-300 -> denominator has', len(str(10**300)), 'digits; multiplications', closed_form(300))
```

**Output (my run):**
```
x = 2 n = 10 -> [1024, 1, 5]
x = 3 n = -2 -> [1, 9, 2]
x = -2 n = 5 -> [-32, 1, 4]
x = 7 n = 0 -> [1, 1, 0]
x = 10 n = 1 -> [10, 1, 1]
exhaustive check ok: 20 values of x times 601 values of n; count equals popcount + bit_length - 1
seeded random cross-check vs repeated multiplication ok
abs(-2**31) = 2147483648 > 2**31 - 1 = 2147483647 (a 32-bit int cannot hold it)
pow(7, 10**18, 10**9+7) = 259616729
x=10, n=-300 -> denominator has 301 digits; multiplications 12
```
The exhaustive check covers all 20 values of x (|x| <= 10, nonzero) times all 601 values of n from -300 to 300, which is the whole input space, against `Fraction(x) ** n`.

**Edge cases:**
- n = 0: result 1, 0 multiplications (also for x negative).
- n = 1: 1 multiplication.
- Negative x with odd or even n (sign of the numerator).
- Negative n: numerator is +1 or -1, denominator |x|^|n|.
- x = 1 or -1.

**Follow-ups:**
- *Modular power?* Reduce mod m after every multiply (or `pow(x, n, m)`).
- *Matrix power for Fibonacci?* Same loop with a matrix as the base.
- *Float power x ** n with negative n?* Gives a float; use `Fraction` when you need exactness.

**Common mistakes:**
- Squaring after the last bit (one wasted multiply, and a huge useless number).
- Negating n in a fixed-width language.
- Returning `-1 / x^n` as a negative denominator.
- Forgetting that `n = 0` gives 1, not 0.

---

### Q10 ⭐⭐⭐ 🟡 Reverse an integer under 32-bit signed rules (this question simulates a fixed-width integer). `x` is an integer with -2^31 <= x <= 2^31 - 1. Reverse its decimal digits keeping the sign (120 becomes 21, -120 becomes -21). Return `[result, wrapped]`: `result` is the reversed value, or 0 if it is outside the signed 32-bit range [-2^31, 2^31 - 1]; `wrapped` is the value a 32-bit two's-complement machine would hold if it simply wrapped the reversed number around without checking, computed as `((v + 2**31) % 2**32) - 2**31` for the reversed value v. Explain that Python integers never overflow, so you must test the range yourself after (or before) the last multiply, and show the digit loop `r = r * 10 + v % 10` that a C solution would guard with a pre-check against INT_MAX // 10. Say for which inputs the reversal can leave the range at all (only 10-digit values) and why a 9-digit input never can. In the answer include a dry run on the first example and a seeded random cross-check of your solution against string reversal with ctypes.c_int32 for the wraparound on small inputs. Example: x=123 -> [321, 321]; x=-120 -> [-21, -21]; x=1534236469 -> [0, 1056389759]; x=-2147483648 -> [0, 126087180]; x=0 -> [0, 0]; x=1463847412 -> [2147483641, 2147483641].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Digit loop with an explicit range check, simulating 32-bit integers.

**Say this first (1 line):** "Python never overflows, so I reverse with `r = r * 10 + v % 10` and then test the result against [-2^31, 2^31 - 1] myself."

**Brute force:**
- Convert to a string, reverse it, convert back, test the range. Used here as the oracle (with `ctypes.c_int32` to get the wraparound).

**Optimal:**
- Take the sign off, loop `r = r * 10 + v % 10; v //= 10`, put the sign back.
- Return `[r if -2^31 <= r <= 2^31 - 1 else 0, wrapped]` where `wrapped = ((r + 2**31) % 2**32) - 2**31` is what a machine would hold if it just wrapped.
- A C solution cannot test after the fact (the overflow already happened). It checks before the multiply: if `r > INT_MAX // 10`, or `r == INT_MAX // 10` and the next digit exceeds 7 (8 for negatives), it returns 0. I translated that into `checked()` in the code and it agrees with the simple version on all test inputs.
- Which inputs can leave the range: only 10-digit values. A 9-digit (or shorter) value reverses to at most 9 digits, below 10^9, which is below 2^31 - 1. The code checks the whole range -10^6..10^6 and 50,000 random 9-digit values, and it is also a one-line proof.
- For 10-digit inputs it depends on the last digit, which becomes the first: a last digit of 3 or more always overflows (3,000,000,000 > 2^31), 0 or 1 never does, 2 depends on the rest (checked on a 50,000-sample).

**Complexity:** O(number of digits), at most 10 loop passes. O(1) space.

**Dry run:**
- `x = 123`: r = 3, then 32, then 321. In range, wrapped is the same: `[321, 321]`.
- `x = -120`: sign -1, v = 120. r = 0, then 02 = 2, then 21. Result -21.
- `x = 1534236469`: reversed 9646324351, above 2147483647, so result 0. Wrapped: 9646324351 - 2 * 2^32 = 9646324351 - 8589934592 = 1056389759.
- `x = 1463847412`: reversed 2147483641, just inside the range, so result 2147483641.

**Code:**
```python
import random, ctypes

I32_MIN, I32_MAX = -2**31, 2**31 - 1

def to_int32(v):                                         # two's-complement wrap, as a machine would hold it
    return ((v + 2**31) % 2**32) - 2**31

def optimal(x):
    sign = -1 if x < 0 else 1
    v, r = abs(x), 0
    while v:
        r = r * 10 + v % 10                              # in C this line needs a pre-check against INT_MAX // 10
        v //= 10
    r *= sign
    return [r if I32_MIN <= r <= I32_MAX else 0, to_int32(r)]

def brute(x):                                            # string reversal + ctypes wraparound
    s = str(x)
    r = int('-' + s[:0:-1]) if x < 0 else int(s[::-1])
    w = ctypes.c_int32(r).value
    return [r if w == r else 0, w]

for x, want in [(123, [321, 321]), (-120, [-21, -21]), (1534236469, [0, 1056389759]),
                (-2147483648, [0, 126087180]), (0, [0, 0]), (1463847412, [2147483641, 2147483641])]:
    got = optimal(x)
    assert got == want == brute(x)
    print('x =', x, '->', got)

random.seed(10)
pool = [0, I32_MIN, I32_MAX, -I32_MAX, 10**9, 10**9 - 1, 2**31 - 10, 1000000003, 2000000003, 1147483647]
for _ in range(20000):
    pool.append(random.choice([random.randint(I32_MIN, I32_MAX), random.randint(-999, 999),
                               random.randint(10**9, I32_MAX), -random.randint(10**9, 2**31)]))
for x in pool:
    assert optimal(x) == brute(x)
print('random cross-check ok:', len(pool), 'inputs incl. boundaries')

# claim: a 9-digit (or shorter) input can never leave the range: its reversal has at most 9 digits < 10**9 < 2**31
assert 10**9 - 1 < I32_MAX
for x in range(-10**6, 10**6):                           # exhaustive on the small side
    assert optimal(x)[0] == int(str(abs(x))[::-1]) * (-1 if x < 0 else 1)
for x in [random.randint(-10**9 + 1, 10**9 - 1) for _ in range(50000)]:
    assert optimal(x)[0] == optimal(x)[1] and (optimal(x)[0] != 0 or x == 0)
# 10-digit inputs: some overflow, some do not
ten = [random.randint(10**9, I32_MAX) for _ in range(50000)]
bad = sum(optimal(x)[0] == 0 for x in ten)
print('10-digit sample: overflow in', bad, 'of', len(ten))
# reversed last digit >= 3 always overflows for a positive 10-digit input; last digit 0 or 1 never does
assert all((optimal(x)[0] == 0) for x in ten if x % 10 >= 3)
assert all((optimal(x)[0] != 0) for x in ten if x % 10 <= 1)
print('10-digit rule on the sample: last digit >= 3 always overflows, last digit 0 or 1 never does')
# the pre-check a C solution uses, translated: before r = r*10 + d, need r <= INT_MAX // 10 (with the last digit rule)
def checked(x):
    sign, v, r = (-1 if x < 0 else 1), abs(x), 0
    while v:
        d = v % 10
        if r > I32_MAX // 10 or (r == I32_MAX // 10 and d > 7 + (sign < 0)):
            return 0
        r = r * 10 + d; v //= 10
    return sign * r
assert all(checked(x) == optimal(x)[0] for x in pool)
print('pre-check form (r > INT_MAX // 10 test) agrees on all', len(pool), 'inputs')
```

**Output (my run):**
```
x = 123 -> [321, 321]
x = -120 -> [-21, -21]
x = 1534236469 -> [0, 1056389759]
x = -2147483648 -> [0, 126087180]
x = 0 -> [0, 0]
x = 1463847412 -> [2147483641, 2147483641]
random cross-check ok: 20010 inputs incl. boundaries
10-digit sample: overflow in 39201 of 50000
10-digit rule on the sample: last digit >= 3 always overflows, last digit 0 or 1 never does
pre-check form (r > INT_MAX // 10 test) agrees on all 20010 inputs
```

**Edge cases:**
- 0.
- Trailing zeros (120 -> 21, they become leading zeros and vanish).
- Negative numbers; `-2^31` itself (`abs` is 2^31, fine in Python, a trap in C).
- Palindromes.
- Reversal landing exactly on 2^31 - 1 or 2^31 (the last digit 7 versus 8 rule).

**Follow-ups:**
- *Why can't C test after the overflow?* Signed overflow is undefined behaviour in C/C++; in Java it silently wraps.
- *Reverse bits instead of digits?* Part 12.
- *Palindrome number without converting to a string?* Reverse half the digits.

**Common mistakes:**
- Assuming Python will wrap or raise on its own.
- Using `v % 10` on a negative number without taking the sign out first (Python's `%` is non-negative for positive modulus, which gives the wrong digits for negatives).
- Checking `abs(r) < 2**31` instead of the asymmetric range.
- Returning the wrapped value instead of 0.

### Q11 ⭐⭐⭐ 🟡 Fisher-Yates shuffle and its exact uniformity (exhaustive check). `n` is an integer with 1 <= n <= 5 and `choices` is a list of n - 1 integers. The shuffle starts from `a = [0, 1, ..., n - 1]` and, for i = n - 1 down to 1, takes the next value j from `choices` (the k-th value, counting from 0, is used at i = n - 1 - k and satisfies 0 <= j <= i) and swaps `a[i]` with `a[j]`. Return `[perm, sequences, distinct, min_count, max_count]`: `perm` is the final list for the given `choices`, and the other four numbers come from running the shuffle on EVERY possible sequence of choices (j ranging over 0..i at each step): the number of sequences, how many different permutations they produce, and the smallest and largest number of sequences that produce one particular permutation. Use that table to prove uniformity: when the table shows every permutation produced by exactly one sequence and each sequence has the same probability 1/(n * (n-1) * ... * 2) = 1/n!, every permutation has probability 1/n!. Explain why the loop must pick j from 0..i (the part not yet fixed) and not from 0..n-1 (the next question measures that bug), and say that CPython's `random.shuffle` runs this loop with `j = randbelow(i + 1)` going from i = len - 1 down to 1. In the answer include a dry run on the first example and a seeded random cross-check of your solution against recursive enumeration of the swap tree on small inputs. Example: n=3, choices=[2, 1] -> [[0, 1, 2], 6, 6, 1, 1]; n=1, choices=[] -> [[0], 1, 1, 1, 1]; n=4, choices=[0, 0, 0] -> [[1, 2, 3, 0], 24, 24, 1, 1]; n=5, choices=[4, 3, 2, 1] -> [[0, 1, 2, 3, 4], 120, 120, 1, 1].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened) | Python random module source (random.py of the installed Python 3.13 read to check the loop; docs not opened)

**Pattern:** Randomised algorithm, uniform permutation. Shrinking "unfixed prefix" plus swap: Fisher-Yates (Knuth shuffle). Proof by counting choice sequences.

**Say this first (1 line):** "Walk i from n-1 down to 1, pick j uniformly in 0..i, swap a[i] and a[j]. That gives n x (n-1) x ... x 2 = n! equally likely choice sequences, and each permutation comes from exactly one sequence, so each has probability 1/n!."

**Brute force:** Build the swap tree: at each i branch on every j in 0..i, recurse, and count the leaves per permutation. That is n! leaves, O(n * n!) work. Fine for n <= 5, and it is the proof, not the shuffle.

**Optimal:**
- The shuffle itself is one backward pass, O(n) time, O(1) extra space, in place.
- Invariant: after the step for i, `a[i]` is final and is a uniformly random pick among the items that were still unfixed. Positions i+1..n-1 never change again.
- Why j must be in 0..i: the part 0..i is the "not yet fixed" part. Choosing from 0..n-1 would swap into the finished suffix and move a fixed item again, which breaks the counting. The sequences then number n^n, and n^n is not divisible by n! in general, so the permutations cannot all get equal counts. (For n = 3 below: 27 sequences over 6 permutations, counts 4 and 5. The next question measures the bug properly.)
- The uniformity proof from the table: the sequence count is `(i+1)` choices at each step, so n! sequences, each of probability 1/(n * (n-1) * ... * 2) = 1/n!. The enumeration shows n! distinct permutations, each from exactly one sequence (min = max = 1). Different sequences give different permutations (the last step fixes a[i], so the permutation determines every j going back), so every permutation has probability exactly 1/n!.
- CPython's `random.shuffle` is this loop: I read the installed 3.13 source, and it runs `for i in reversed(range(1, len(x)))` with `j = randbelow(i + 1)`.

**Complexity:** Shuffle: O(n) time, O(1) extra space, n-1 random draws. The exhaustive table is for proof only: n! sequences, so about n * n! steps, trivial for n <= 5.

**Dry run:** n = 4, choices [0, 0, 0], start [0,1,2,3]. i=3, j=0: swap a[3] and a[0] -> [3,1,2,0]. i=2, j=0 -> [2,1,3,0]. i=1, j=0 -> [1,2,3,0]. Answer [1,2,3,0], matching the example. For n = 3, choices [2,1] every swap is a self-swap, so the result is [0,1,2]. The sequence count is 3 * 2 = 6.

**Code:**
```python
import itertools
import inspect
import math
import random
from collections import Counter

random.seed(1311)

def shuffle_with(n, choices):
    """Fisher-Yates driven by an explicit list of choices: the k-th choice is used at i = n-1-k, 0 <= j <= i."""
    a = list(range(n))
    for k, i in enumerate(range(n - 1, 0, -1)):
        j = choices[k]
        assert 0 <= j <= i
        a[i], a[j] = a[j], a[i]
    return a

def fisher_yates(n, choices):
    """Optimal: run once for the given choices, then run on EVERY choice sequence and tabulate."""
    counts = Counter(tuple(shuffle_with(n, cs))
                     for cs in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]))
    return [shuffle_with(n, choices), sum(counts.values()), len(counts),
            min(counts.values()), max(counts.values())]

def brute(n, choices):
    """Brute force: recursive walk of the swap tree (a branch for every j at every step)."""
    acc = Counter()
    def rec(a, i):
        if i == 0:
            acc[tuple(a)] += 1
            return
        for j in range(i + 1):
            b = a[:]
            b[i], b[j] = b[j], b[i]
            rec(b, i - 1)
    rec(list(range(n)), n - 1)
    a, i = list(range(n)), n - 1
    for c in choices:
        a[i], a[c] = a[c], a[i]
        i -= 1
    return [a, sum(acc.values()), len(acc), min(acc.values()), max(acc.values())]

examples = [
    (3, [2, 1], [[0, 1, 2], 6, 6, 1, 1]),
    (1, [], [[0], 1, 1, 1, 1]),
    (4, [0, 0, 0], [[1, 2, 3, 0], 24, 24, 1, 1]),
    (5, [4, 3, 2, 1], [[0, 1, 2, 3, 4], 120, 120, 1, 1]),
]
for n, ch, exp in examples:
    got = fisher_yates(n, ch)
    print(n, ch, '->', got)
    assert got == exp and brute(n, ch) == exp

# the exhaustive table for every n <= 5: n! sequences, n! distinct perms, each exactly once
for n in range(1, 6):
    r = fisher_yates(n, [0] * (n - 1))
    assert r[1:] == [math.factorial(n)] * 2 + [1, 1], r
    print('n =', n, 'sequences, distinct, min, max =', r[1:])

# seeded random cross-check against the recursive swap tree
for _ in range(300):
    n = random.randint(1, 5)
    ch = [random.randint(0, i) for i in range(n - 1, 0, -1)]
    assert fisher_yates(n, ch) == brute(n, ch)
print('random cross-check ok: 300 cases')

# the wrong loop (j from 0..n-1) on n = 3: 27 equally likely sequences, 6 permutations, NOT uniform
bad = Counter()
for js in itertools.product(range(3), repeat=3):
    a = [0, 1, 2]
    for i, j in enumerate(js):
        a[i], a[j] = a[j], a[i]
    bad[tuple(a)] += 1
print('naive swap-with-any, n=3:', sorted(bad.items()))
assert sum(bad.values()) == 27 and set(bad.values()) == {4, 5}

# does CPython's random.shuffle run this loop? (read from the installed 3.13 source)
src = inspect.getsource(random.Random.shuffle)
print('loop is reversed(range(1, len(x))):', 'reversed(range(1, len(x)))' in src,
      '| uses randbelow(i + 1):', 'randbelow(i + 1)' in src)
assert 'reversed(range(1, len(x)))' in src and 'randbelow(i + 1)' in src

# edge asserts
assert fisher_yates(1, []) == [[0], 1, 1, 1, 1]
assert fisher_yates(2, [0])[0] == [1, 0] and fisher_yates(2, [1])[0] == [0, 1]
print('edge asserts ok')
```

**Output (my run):**
```
3 [2, 1] -> [[0, 1, 2], 6, 6, 1, 1]
1 [] -> [[0], 1, 1, 1, 1]
4 [0, 0, 0] -> [[1, 2, 3, 0], 24, 24, 1, 1]
5 [4, 3, 2, 1] -> [[0, 1, 2, 3, 4], 120, 120, 1, 1]
n = 1 sequences, distinct, min, max = [1, 1, 1, 1]
n = 2 sequences, distinct, min, max = [2, 2, 1, 1]
n = 3 sequences, distinct, min, max = [6, 6, 1, 1]
n = 4 sequences, distinct, min, max = [24, 24, 1, 1]
n = 5 sequences, distinct, min, max = [120, 120, 1, 1]
random cross-check ok: 300 cases
naive swap-with-any, n=3: [((0, 1, 2), 4), ((0, 2, 1), 5), ((1, 0, 2), 5), ((1, 2, 0), 5), ((2, 0, 1), 4), ((2, 1, 0), 4)]
loop is reversed(range(1, len(x))): True | uses randbelow(i + 1): True
edge asserts ok
```

**Edge cases:**
- n = 1: no steps, one sequence, one permutation.
- j == i is a legal self-swap. Leaving it out (Sattolo's variant, j in 0..i-1) gives only cyclic permutations, (n-1)! of them.
- Duplicated values do not matter here: the shuffle moves positions.
- Empty list: the loop body never runs.

**Follow-ups:**
- Shuffle a list in place with the standard library? `random.shuffle(x)`. It is the same loop (read from the 3.13 source), and `random.sample` copies.
- The forward version (i from 0, j in i..n-1) is also uniform. Same proof, mirrored.
- Is `sorted(a, key=lambda _: random.random())` uniform? Only up to ties among the random keys, and it costs O(n log n). Prefer Fisher-Yates.

**Common mistakes:**
- j = randint(0, n-1) at every step: n^n outcomes, provably biased (27 outcomes over 6 permutations for n = 3, counts 4 and 5).
- Off by one: j in 0..i-1 (Sattolo), or an off-by-one on the range of i that skips index 1.
- Proving uniformity by "run it 10000 times and look". Count the sequences instead.

### Q12 ⭐⭐⭐ 🟡 Reservoir sampling with a reservoir of size one, checked exactly. A stream has n items (`stream` is a list of 1 <= n <= 6 integers; values may repeat, so identify items by position). Process them in order keeping one held item: the first item is held at once; for the i-th item (i = 2..n, counting from 1) take the next number d from `draws` (`draws[i - 2]`, with 0 <= d <= i - 1) and replace the held item by the i-th one exactly when d == 0. Return `[held, counts, sequences]`: `held` is the VALUE held at the end for the given `draws` (which has n - 1 numbers); `sequences` is the number of possible draw sequences (1 * 2 * ... * n = n!, counting every choice of every draw); and `counts[t]` is the number of those sequences after which the item at position t (0-indexed) is held. Use the exact counts to show every item is held in (n-1)! of the n! sequences, that is with probability 1/n, and explain it with the product (1/i) * (1 - 1/(i+1)) * ... * (1 - 1/n) = 1/n. State the memory used (one item plus a counter) and why this works when n is unknown in advance. Picking a random element of a set or list you can index is Part 1 Q35 and Part 1 Q47; this question is about a one-pass stream. In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating every draw sequence with itertools.product on small inputs. Example: stream=[10, 20, 30], draws=[0, 2] -> [20, [2, 2, 2], 6]; stream=[5], draws=[] -> [5, [1], 1]; stream=[4, 4, 9, 1], draws=[1, 0, 0] -> [1, [6, 6, 6, 6], 24].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Reservoir sampling (Algorithm R) with k = 1. One pass over a stream of unknown length, keep one item.

**Say this first (1 line):** "Keep the first item. For the i-th item, replace the held one with probability 1/i. Item t survives to the end with probability (1/t) x (1 - 1/(t+1)) x ... x (1 - 1/n) = 1/n. Memory is one item and a counter."

**Brute force:** Read the whole stream into a list, then `random.choice`. O(n) memory, and you need n (or the whole stream) first. Not possible for an unbounded stream.

**Optimal:**
- Keep `held` and the counter `i`. Item i is taken when a draw from 0..i-1 equals 0, which has probability 1/i. So item 1 is always taken, item 2 with 1/2, item 3 with 1/3.
- Invariant: after i items, each of the i items seen is held with probability 1/i. Step to i+1: the new item wins with 1/(i+1). An old item stays held with (1/i) x (i/(i+1)) = 1/(i+1). So the invariant holds.
- Exact proof by counting every draw sequence (n! of them: 1 x 2 x ... x n). Item t (counting from 1, t >= 2) must win its own draw (1 way), the earlier draws are free ((t-1)! ways) and every later draw i > t must not be 0 (i-1 ways each, (n-1)!/(t-1)! in all). That is (n-1)! sequences out of n!, so probability 1/n. The enumeration confirms it for every n <= 7.
- Works when n is unknown: nothing in the loop uses n. You can stop at any moment and the held item is uniform over what has been read.

**Complexity:** O(n) time, one pass. O(1) space: one held item and one counter (plus the random generator). The counting table is a proof aid.

**Dry run:** stream [10,20,30], draws [0,2]. Held 10. Item 2 (20): draw 0 equals 0, so held becomes 20. Item 3 (30): draw 2 is not 0, so held stays 20. Result 20. Counts: after item 2 the 2 sequences hold position 0 once and position 1 once. At item 3, old items survive in 2 of 3 draws: [1*2, 1*2] and the new item wins in 2 sequences (total before = 2): [2,2,2] of 6.

**Code:**
```python
import itertools
import math
import random
from fractions import Fraction

random.seed(1312)

def reservoir_one(stream, draws):
    """One pass, one held item plus a counter. i-th item (1-based) replaces the held one iff draw == 0, draw in 0..i-1."""
    held = stream[0]
    for i, x in enumerate(stream[1:], start=2):
        if draws[i - 2] == 0:
            held = x
    return held

def solve(stream, draws):
    n = len(stream)
    held = reservoir_one(stream, draws)
    # exact counts without enumeration: counts after item i; old items survive in (i-1) of i draws
    counts, total = [1], 1
    for i in range(2, n + 1):
        counts = [c * (i - 1) for c in counts] + [total]
        total *= i
    return [held, counts, total]

def brute(stream, draws):
    """Enumerate EVERY draw sequence with itertools.product and count which position is held."""
    n = len(stream)
    cnt, tot = [0] * n, 0
    for ds in itertools.product(*[range(i) for i in range(2, n + 1)]):
        pos = 0
        for i, d in enumerate(ds, start=2):
            if d == 0:
                pos = i - 1
        cnt[pos] += 1
        tot += 1
    pos = 0
    for i, d in enumerate(draws, start=2):
        if d == 0:
            pos = i - 1
    return [stream[pos], cnt, tot]

examples = [
    ([10, 20, 30], [0, 2], [20, [2, 2, 2], 6]),
    ([5], [], [5, [1], 1]),
    ([4, 4, 9, 1], [1, 0, 0], [1, [6, 6, 6, 6], 24]),
]
for s, d, exp in examples:
    got = solve(s, d)
    print(s, d, '->', got)
    assert got == exp and brute(s, d) == exp

# the exact table: every item held in (n-1)! of n! sequences, for every n <= 7 (enumeration, not sampling)
for n in range(1, 8):
    r = brute(list(range(n)), [1] * (n - 1))
    assert r[1] == [math.factorial(n - 1)] * n and r[2] == math.factorial(n), (n, r)
    assert solve(list(range(n)), [1] * (n - 1)) == r
    print('n =', n, 'counts =', r[1], 'of', r[2], '-> probability', Fraction(r[1][0], r[2]))

# the product: (1/i)(1-1/(i+1))...(1-1/n) = 1/n for item i, exactly
for n in range(1, 12):
    for i in range(1, n + 1):
        p = Fraction(1, i)
        for m in range(i + 1, n + 1):
            p *= 1 - Fraction(1, m)
        assert p == Fraction(1, n)
print('product telescopes to 1/n: checked exactly for n <= 11, every i')

# seeded random cross-check (values may repeat; items identified by position)
for _ in range(300):
    n = random.randint(1, 6)
    s = [random.randint(0, 3) for _ in range(n)]
    d = [random.randint(0, i - 1) for i in range(2, n + 1)]
    assert solve(s, d) == brute(s, d)
print('random cross-check ok: 300 cases')

# edge asserts
assert solve([7], []) == [7, [1], 1]
assert solve([1, 2], [0]) == [2, [1, 1], 2] and solve([1, 2], [1]) == [1, [1, 1], 2]
assert reservoir_one(list(range(6)), [1, 1, 1, 1, 1]) == 0      # no draw is 0: the first item stays
assert reservoir_one(list(range(6)), [0, 0, 0, 0, 0]) == 5      # every draw is 0: the last item wins
print('edge asserts ok')
```

**Output (my run):**
```
[10, 20, 30] [0, 2] -> [20, [2, 2, 2], 6]
[5] [] -> [5, [1], 1]
[4, 4, 9, 1] [1, 0, 0] -> [1, [6, 6, 6, 6], 24]
n = 1 counts = [1] of 1 -> probability 1
n = 2 counts = [1, 1] of 2 -> probability 1/2
n = 3 counts = [2, 2, 2] of 6 -> probability 1/3
n = 4 counts = [6, 6, 6, 6] of 24 -> probability 1/4
n = 5 counts = [24, 24, 24, 24, 24] of 120 -> probability 1/5
n = 6 counts = [120, 120, 120, 120, 120, 120] of 720 -> probability 1/6
n = 7 counts = [720, 720, 720, 720, 720, 720, 720] of 5040 -> probability 1/7
product telescopes to 1/n: checked exactly for n <= 11, every i
random cross-check ok: 300 cases
edge asserts ok
```

**Edge cases:**
- n = 1: nothing to draw, the only item is held (`draws` is empty).
- Repeated values: identify items by position. [4,4,9,1] still gives counts [6,6,6,6]; the held VALUE for a given `draws` can repeat, the probabilities are per position.
- All draws nonzero: first item is kept. All draws zero: last item wins.
- Empty stream: undefined (nothing to return); say so.

**Follow-ups:**
- Keep k items? Hold the first k, then for item i draw d in 0..i-1 and replace slot d if d < k (that is probability k/i). Every k-subset is then equally likely (stated here, not run in this answer).
- Stream is weighted? Use keys u^(1/w) and keep the largest (A-Res); out of scope here.
- Random element of a set or list you can index: Part 1 Q35 and Part 1 Q47. This question is the one-pass stream.

**Common mistakes:**
- Replacing with probability 1/n using the final n, which you do not know.
- Using `random.randint(0, i)` for the i-th item (i counted from 0 but 1-based range): off by one and biased.
- Replacing with a fixed probability like 1/2: later items would be over-weighted.

### Q13 ⭐⭐⭐ 🟡 Random pick with weights, using prefix sums and bisect. `w` is a list of 1 to 10^4 positive integers with sum(w) <= 10^6, and `rs` is a list of integers with 0 <= r < sum(w). The generator behind the picker produces an integer r uniformly from 0 to sum(w) - 1; the picker must return the index i whose block of numbers contains r, where index i owns the w[i] consecutive values after those owned by the earlier indices. Return `[picks, counts]`: `picks[t]` is the index for `rs[t]`, and `counts[i]` is the number of values r in 0..sum(w)-1 that your rule maps to index i (so a correct rule gives `counts == w`, which is what makes the pick probability w[i] / sum(w) exactly). Build the inclusive prefix sums once and answer each pick with a binary search in O(log n). State exactly which bisect function applies when r is in 0..total-1 (the first index whose prefix sum is strictly greater than r) and why the other one (`bisect_left`) assigns the boundary values to the wrong index, and what changes if r is drawn from 1..total instead. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a linear scan that subtracts weights one by one on small inputs. Example: w=[1, 3], rs=[0, 1, 2, 3] -> [[0, 1, 1, 1], [1, 3]]; w=[5], rs=[0, 4] -> [[0, 0], [5]]; w=[2, 1, 3], rs=[0, 1, 2, 3, 5] -> [[0, 0, 1, 2, 2], [2, 1, 3]].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Prefix sums plus binary search. Map a uniform integer to a weighted index (inverse CDF on integers).

**Say this first (1 line):** "Build inclusive prefix sums once. Draw r uniformly in 0..total-1 and return `bisect_right(prefix, r)`: the first index whose prefix sum is strictly greater than r. Index i then owns exactly w[i] values of r."

**Brute force:** For every pick, walk the weights and subtract: `for i, x in enumerate(w): if r < x: return i; r -= x`. O(n) per pick. Correct and the reference here.

**Optimal:**
- Block i covers the values from prefix[i-1] up to prefix[i]-1 (prefix[-1] taken as 0), which is w[i] numbers. Example w = [2,1,3]: prefix [2,3,6], blocks {0,1}, {2}, {3,4,5}.
- r lands in block i when prefix[i-1] <= r < prefix[i]. The first prefix strictly greater than r is prefix[i]. That is `bisect_right(prefix, r)`.
- Why not `bisect_left`: it returns the first prefix >= r. When r equals a prefix value (r = 2 or 3 above) it returns the previous index, so each boundary value is given to the wrong block. For w = [2,1,3] it counts [3,1,2] instead of [2,1,3].
- If r is drawn from 1..total instead, the blocks are (prefix[i-1], prefix[i]] and `bisect_left` is the right call. Match the function to the range.
- Correctness is shown by counts: for all r in 0..total-1, count how many map to each index; the result equals w, so P(i) = w[i]/total exactly.

**Complexity:** Build O(n). Each pick O(log n) by binary search. Space O(n) for the prefix list. (The counts loop in my code is a checker, O(total log n), not part of the picker.)

**Dry run:** w = [1,3], prefix [1,4], total 4. r=0: first prefix > 0 is 1, index 0. r=1: 1 is not > 1, next prefix 4 > 1, index 1. r=2 and r=3: index 1. Picks [0,1,1,1], counts [1,3] = w.

**Code:**
```python
import bisect
import itertools
import random

random.seed(1313)

def weighted_pick(w, rs):
    """Inclusive prefix sums once, then bisect_right per pick: first index whose prefix sum is > r."""
    pre = list(itertools.accumulate(w))
    total = pre[-1]
    picks = [bisect.bisect_right(pre, r) for r in rs]
    # counts[i] = how many r in 0..total-1 land on i (loop over r only for the check; real pick is O(log n))
    counts = [0] * len(w)
    for r in range(total):
        counts[bisect.bisect_right(pre, r)] += 1
    return [picks, counts]

def brute(w, rs):
    """Linear scan: subtract weights one by one until r falls inside a block."""
    def pick(r):
        for i, x in enumerate(w):
            if r < x:
                return i
            r -= x
    counts = [0] * len(w)
    for r in range(sum(w)):
        counts[pick(r)] += 1
    return [[pick(r) for r in rs], counts]

examples = [
    ([1, 3], [0, 1, 2, 3], [[0, 1, 1, 1], [1, 3]]),
    ([5], [0, 4], [[0, 0], [5]]),
    ([2, 1, 3], [0, 1, 2, 3, 5], [[0, 0, 1, 2, 2], [2, 1, 3]]),
]
for w, rs, exp in examples:
    got = weighted_pick(w, rs)
    print(w, rs, '->', got)
    assert got == exp and brute(w, rs) == exp

# why bisect_left is wrong for r in 0..total-1: boundary values go to the previous index
w = [2, 1, 3]
pre = list(itertools.accumulate(w))
left = [0] * 3
for r in range(sum(w)):
    left[bisect.bisect_left(pre, r)] += 1
print('prefix', pre, 'bisect_left counts', left, '(want', w, ')')
assert left != w and left == [3, 1, 2]

# if r is drawn from 1..total instead, bisect_left is the right one
alt = [0] * 3
for r in range(1, sum(w) + 1):
    alt[bisect.bisect_left(pre, r)] += 1
assert alt == w
print('r in 1..total with bisect_left gives', alt)

# seeded random cross-check against the linear scan
for _ in range(300):
    w = [random.randint(1, 6) for _ in range(random.randint(1, 6))]
    rs = [random.randrange(sum(w)) for _ in range(random.randint(0, 10))]
    assert weighted_pick(w, rs) == brute(w, rs) and weighted_pick(w, rs)[1] == w
print('random cross-check ok: 300 cases (counts == w every time)')

# maximum size: n = 10^4, sum <= 10^6; one prefix build, picks cost O(log n) each
w = [random.randint(1, 100) for _ in range(10 ** 4)]
assert sum(w) <= 10 ** 6
pre = list(itertools.accumulate(w))
assert bisect.bisect_right(pre, 0) == 0 and bisect.bisect_right(pre, sum(w) - 1) == len(w) - 1
print('max size ok: n =', len(w), 'total =', sum(w))

# edge asserts
assert weighted_pick([1], [0]) == [[0], [1]]
assert weighted_pick([1, 1, 1], [0, 1, 2])[0] == [0, 1, 2]
assert weighted_pick([4, 1], [3, 4])[0] == [0, 1]       # r = 3 is the last value of block 0, r = 4 the first of block 1
print('edge asserts ok')
```

**Output (my run):**
```
[1, 3] [0, 1, 2, 3] -> [[0, 1, 1, 1], [1, 3]]
[5] [0, 4] -> [[0, 0], [5]]
[2, 1, 3] [0, 1, 2, 3, 5] -> [[0, 0, 1, 2, 2], [2, 1, 3]]
prefix [2, 3, 6] bisect_left counts [3, 1, 2] (want [2, 1, 3] )
r in 1..total with bisect_left gives [2, 1, 3]
random cross-check ok: 300 cases (counts == w every time)
max size ok: n = 10000 total = 510843
edge asserts ok
```

**Edge cases:**
- Single weight: always index 0.
- r = 0 goes to index 0; r = total-1 goes to the last index (checked at the max size).
- Weights all equal: the picker is uniform.
- Zero weights are excluded by the prompt (positive integers).

**Follow-ups:**
- Update a weight between picks? The prefix list goes stale; a Fenwick tree (Part 14, named only) gives O(log n) update and pick.
- Faster than O(log n) per pick? The alias method gives O(1) per pick after O(n) setup; mention only.
- Float weights? Use `random.random() * total` with `bisect_right`, accept tiny rounding at boundaries, or `random.choices(w_cumulative)`.

**Common mistakes:**
- `bisect_left` with r in 0..total-1 (boundary values go to the previous index, shown above).
- Drawing r in 1..total with `bisect_right`: r = total would return n, out of range.
- Recomputing prefix sums on every pick, which makes it O(n) again.

### Q14 ⭐⭐⭐ 🟡 Python sort stability, key= and reverse=. `records` is a list of 1 to 1000 items [name, dept, score] (name and dept lowercase strings, score an integer with |score| <= 1000; names may repeat). Return four lists of NAMES, each in the order of the records after the sort described: A = one `sorted` call with `key=lambda r: (r[1], -r[2])` (department ascending, score descending); B = two stable passes, first `sort(key=score, reverse=True)` then `sort(key=dept)`; C = `sorted(records, key=dept, reverse=True)`; D = `sorted(records, key=dept)[::-1]`. Return `[A, B, C, D]`. Explain: Python's sort is stable, so records with equal keys keep their input order; that is why two passes (least significant key first) equal the single tuple key and why this is the way to sort by a string descending (strings cannot be negated); and that `reverse=True` preserves the original order of equal elements (it behaves as if the comparisons were reversed, not as if the result were reversed), so C and D differ whenever two records share a department. Mention `functools.cmp_to_key` as the general fallback. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an index-aware manual comparison (original position as the final tie-break) on small inputs. Example: records=[['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]] -> [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'], ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]; records=[['x', 'a', 1]] -> [['x'], ['x'], ['x'], ['x']]; records=[['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]] -> [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13)

**Pattern:** Python sort stability, `key=`, `reverse=`, and multi-key sorting by passes.

**Say this first (1 line):** "Python's sort is stable, so equal keys keep input order. That makes two passes, least significant key first, equal to one tuple key. `reverse=True` keeps equal items in their original order, so it is not the same as reversing the sorted list."

**Brute force:** Write an explicit comparison that finishes with the original index as a tie-break and sort the indices with `cmp_to_key`. It does not depend on stability at all, and I use it as the reference. Cost: O(n log n) comparisons, each a Python call.

**Optimal:**
- A: `sorted(records, key=lambda r: (r[1], -r[2]))`. One pass, tuple key: dept ascending, score descending. Negating works for numbers only.
- B: sort by score with `reverse=True` first, then by dept. The second pass is stable, so inside each dept the earlier score order survives. Result equals A.
- Strings cannot be negated (`-'hr'` raises TypeError, shown below). For dept DESCENDING with score ascending use two passes: score first, then dept with `reverse=True`. General fallback: `functools.cmp_to_key` with a comparator.
- C: `sorted(records, key=dept, reverse=True)`. Departments descending, and records with the same dept stay in input order, because `reverse=True` behaves as if the comparisons were reversed, not as if the result list were flipped.
- D: `sorted(records, key=dept)[::-1]`. Flips everything, so equal-dept records come out in reverse input order. C and D differ whenever two records share a department (331 of my 400 random cases).
- Pass order matters: least significant key first. Sorting by dept first and score last gives a different list (in the output).

**Complexity:** Each sort is O(n log n) time and O(n) extra space (Timsort). Two passes cost twice that, same big-O. Key functions are called once per record, not per comparison.

**Dry run:** example 1, records ann(hr,5), bob(it,7), cat(hr,5), dan(it,9), eve(hr,8).
- A: keys ann (hr,-5), bob (it,-7), cat (hr,-5), dan (it,-9), eve (hr,-8). hr: eve, ann, cat (ann and cat tie, ann is first in input); it: dan, bob. A = eve, ann, cat, dan, bob.
- B: pass 1 (score desc): dan 9, eve 8, bob 7, ann 5, cat 5. Pass 2 (dept): hr: eve, ann, cat; it: dan, bob. Same as A.
- C: dept desc, input order inside: it: bob, dan; hr: ann, cat, eve.
- D: dept asc gives ann, cat, eve, bob, dan; flipped: dan, bob, eve, cat, ann.

**Code:**
```python
import functools
import random

random.seed(1314)

def four_sorts(records):
    name, dept, score = (lambda r: r[0]), (lambda r: r[1]), (lambda r: r[2])
    A = [r[0] for r in sorted(records, key=lambda r: (r[1], -r[2]))]
    t = list(records)
    t.sort(key=score, reverse=True)        # least significant key first
    t.sort(key=dept)                       # then the most significant key; stability keeps the score order inside a dept
    B = [r[0] for r in t]
    C = [r[0] for r in sorted(records, key=dept, reverse=True)]
    D = [r[0] for r in sorted(records, key=dept)[::-1]]
    return [A, B, C, D]

def brute(records):
    """Index-aware comparison: original position is the final tie-break, so no stability is assumed."""
    idx = list(range(len(records)))
    def cmp_a(i, j):                                   # dept asc, score desc, then position asc
        a, b = records[i], records[j]
        return (a[1] > b[1]) - (a[1] < b[1]) or (b[2] > a[2]) - (b[2] < a[2]) or (i > j) - (i < j)
    def cmp_c(i, j):                                   # dept DESC, position ASC (equal depts keep input order)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (i > j) - (i < j)
    def cmp_d(i, j):                                   # dept DESC, position DESC (the reversed result)
        a, b = records[i], records[j]
        return (b[1] > a[1]) - (b[1] < a[1]) or (j > i) - (j < i)
    pick = lambda c: [records[i][0] for i in sorted(idx, key=functools.cmp_to_key(c))]
    A = pick(cmp_a)
    return [A, A, pick(cmp_c), pick(cmp_d)]

examples = [
    ([['ann', 'hr', 5], ['bob', 'it', 7], ['cat', 'hr', 5], ['dan', 'it', 9], ['eve', 'hr', 8]],
     [['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'],
      ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]),
    ([['x', 'a', 1]], [['x'], ['x'], ['x'], ['x']]),
    ([['p', 'b', 2], ['q', 'a', 2], ['r', 'b', 2], ['s', 'a', 3]],
     [['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]),
]
for rec, exp in examples:
    got = four_sorts(rec)
    print(got)
    assert got == exp and brute(rec) == exp

# C vs D: reverse=True keeps equal records in input order, [::-1] reverses them
two = [['a', 'x', 0], ['b', 'x', 0]]
C, D = four_sorts(two)[2:]
print('two records, same dept: C =', C, ' D =', D)
assert C == ['a', 'b'] and D == ['b', 'a']

# strings cannot be negated: -r[1] raises, so the two-pass trick is the way to get dept DESC + score ASC
try:
    sorted(examples[0][0], key=lambda r: (-r[1], r[2]))
except TypeError as e:
    print('negating a str:', type(e).__name__)
t = list(examples[0][0]); t.sort(key=lambda r: r[2]); t.sort(key=lambda r: r[1], reverse=True)
print('dept desc then score asc via two passes:', [r[0] for r in t])
# the same with cmp_to_key
def cmp(a, b):
    return (b[1] > a[1]) - (b[1] < a[1]) or (a[2] > b[2]) - (a[2] < b[2])
assert [r[0] for r in sorted(examples[0][0], key=functools.cmp_to_key(cmp))] == [r[0] for r in t]

# the pass ORDER matters: dept first then score gives a different answer
wrong = list(examples[0][0]); wrong.sort(key=lambda r: r[1]); wrong.sort(key=lambda r: r[2], reverse=True)
print('wrong pass order:', [r[0] for r in wrong], '(A is', examples[0][1][0], ')')
assert [r[0] for r in wrong] != examples[0][1][0]

# key= is called once per record, not once per comparison
calls = [0]
def counting_key(r):
    calls[0] += 1
    return r[1]
sorted(examples[0][0], key=counting_key)
print('key calls for 5 records:', calls[0])
assert calls[0] == 5

# seeded random cross-check: A == B, all four equal the index-aware comparison
tie_seen = 0
for _ in range(400):
    n = random.randint(1, 12)
    rec = [[random.choice('abcde'), random.choice(['hr', 'it', 'ops']), random.randint(-3, 3)] for _ in range(n)]
    r = four_sorts(rec)
    assert r == brute(rec) and r[0] == r[1]
    if r[2] != r[3]:
        tie_seen += 1
print('random cross-check ok: 400 cases; C != D in', tie_seen, 'of them')

# edge asserts
assert four_sorts([['x', 'a', 1]]) == [['x']] * 4
assert four_sorts([['a', 'z', 1], ['b', 'z', 1]])[0] == ['a', 'b']   # all keys equal: input order survives in A
print('edge asserts ok')
```

**Output (my run):**
```
[['eve', 'ann', 'cat', 'dan', 'bob'], ['eve', 'ann', 'cat', 'dan', 'bob'], ['bob', 'dan', 'ann', 'cat', 'eve'], ['dan', 'bob', 'eve', 'cat', 'ann']]
[['x'], ['x'], ['x'], ['x']]
[['s', 'q', 'p', 'r'], ['s', 'q', 'p', 'r'], ['p', 'r', 'q', 's'], ['r', 'p', 's', 'q']]
two records, same dept: C = ['a', 'b']  D = ['b', 'a']
negating a str: TypeError
dept desc then score asc via two passes: ['bob', 'dan', 'ann', 'cat', 'eve']
wrong pass order: ['dan', 'eve', 'bob', 'ann', 'cat'] (A is ['eve', 'ann', 'cat', 'dan', 'bob'] )
key calls for 5 records: 5
random cross-check ok: 400 cases; C != D in 331 of them
edge asserts ok
```

**Edge cases:**
- Single record: all four lists equal.
- All keys equal: A keeps input order; D reverses it.
- Duplicate names are fine, since only the sort keys decide order.
- Negative scores: `-r[2]` is fine for ints (not for strings, or `bool`/`None` mixes).

**Follow-ups:**
- Why is the key function better than `cmp`? Called once per item, and Python 3 dropped `cmp=`. `cmp_to_key` wraps an old comparison when no key exists.
- Does `list.sort` guarantee stability? Yes, it is documented. The HOWTO page itself could not be fetched, so I verified the behaviour by running 3.13 (the documentation claim is editor knowledge).
- Sort descending but keep ties stable? `sort(key=..., reverse=True)` does that. Do not flip with `[::-1]`.

**Common mistakes:**
- Doing the passes in the wrong order (most significant key first).
- Using `[::-1]` and expecting stability for equal items.
- Trying `-r[1]` on a string key.
- Assuming a stable sort needs `(key, index)` pairs. It does not in Python, and this answer's reference uses them only to avoid assuming it.

### Q15 ⭐⭐⭐ 🟡 Merge sort from scratch, stable, with exact comparison counts. `records` is a list of 0 <= len <= 10^5 items [key, tag] with integer keys (|key| <= 10^9) and any integer tag. Sort them ascending by key, keeping equal keys in input order, without `sorted` or `list.sort`. Use top-down merge sort: split a list of length n at `mid = n // 2` (left part = first n // 2 items), sort both halves, then merge: while both halves have items, make ONE comparison `left.key <= right.key` and take the left item when it is true, else the right item; when one half runs out, append the rest of the other with no comparisons. Return `[sorted_records, comparisons]`, where `comparisons` totals all those key comparisons over the whole sort. Explain why `<=` (not `<`) makes it stable, why the work is O(n log n) in every case and the extra space O(n), and why the recursion depth is about log2 n (under 20 here, so recursion is fine) while a bottom-up version needs no recursion at all (its comparison count can differ from the top-down one). State the worst-case comparison count n * ceil(log2 n) - 2^ceil(log2 n) + 1 and check it by hand for n = 5. In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted(records, key=lambda r: r[0]) for the order and a separate recursive comparison counter on small inputs. Example: records=[[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]] -> [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]; records=[] -> [[], 0]; records=[[9, 0]] -> [[[9, 0]], 0]; records=[[1, 1], [2, 2], [3, 3], [4, 4]] -> [[[1, 1], [2, 2], [3, 3], [4, 4]], 4].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Divide and conquer: stable merge sort from scratch, with an exact comparison counter.

**Say this first (1 line):** "Split at n // 2, sort both halves, merge with one comparison `left.key <= right.key` per taken item. `<=` takes the left item on ties, which makes it stable. O(n log n) in every case, O(n) extra space."

**Brute force:** Insertion or selection sort, O(n^2) comparisons. Not good for n = 10^5.

**Optimal:**
- Base case: length 0 or 1 is sorted and costs no comparisons.
- Merge: two pointers. Each loop iteration is one comparison and moves one item. When one half is empty, append the rest of the other with no comparisons.
- Stability: on equal keys take the LEFT item, since left items came earlier in the input. With `<` the right item goes first and equal records swap (shown below).
- Every level of the recursion touches n items once, and there are about log2 n levels, so O(n log n) in the best, average and worst case. It needs a temporary list, O(n) extra space.
- Recursion depth is about log2 n, about 17 for n = 10^5, far below CPython's 1000 limit. Bottom-up (widths 1, 2, 4, ...) needs no recursion, but it splits differently (not at n // 2), so its comparison count can differ: for sorted [0,1,2] top-down uses 2 and bottom-up 3 (630 of the permutations with n <= 6 differ).
- Worst case is n * ceil(log2 n) - 2^ceil(log2 n) + 1. By hand for n = 5: 5 * 3 - 8 + 1 = 8. I checked this over all permutations for every n <= 8.

**Complexity:** Time O(n log n), at most 1,700,000 comparisons for n = 10^5 (the random run used 1,536,373). Space O(n) for the merge lists, plus O(log n) for the call stack.

**Dry run:** keys [3,1,3,2,1], split 2 | 3.
- Left half [[3,1],[1,2]]: 3<=1 is false, so the result is [[1,2],[3,1]]: 1 comparison.
- Right half [[3,3],[2,4],[1,5]] splits 1 | 2. [[2,4],[1,5]] costs 1 and gives [[1,5],[2,4]]. Merge [[3,3]] with it: 3<=1 no, 3<=2 no, then append [3,3]: 2 comparisons. Right total 3.
- Final merge of keys [1,3] with [1,2,3]: 1<=1 yes (take [1,2]), 3<=1 no (take [1,5]), 3<=2 no (take [2,4]), 3<=3 yes (take [3,1]), left empty, append [3,3]: 4 comparisons.
- Total 1 + 3 + 4 = 8, and equal keys keep input order: [1,2] before [1,5], [3,1] before [3,3].

**Code:**
```python
import itertools
import math
import random

random.seed(1315)

def merge_sort(records):
    """Top-down, split at n // 2, one comparison left.key <= right.key per taken item while both halves have items."""
    cmps = 0
    def sort(a):
        nonlocal cmps
        n = len(a)
        if n <= 1:
            return a
        mid = n // 2
        left, right = sort(a[:mid]), sort(a[mid:])
        out, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            cmps += 1
            if left[i][0] <= right[j][0]:          # <= takes the LEFT item on ties: that is stability
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        out.extend(left[i:]); out.extend(right[j:])   # leftovers: no comparisons
        return out
    res = sort([list(r) for r in records])
    return [res, cmps]

def brute(records):
    """Reference: sorted() for the order (stable) and a separate recursive counter over index ranges."""
    recs = [list(r) for r in records]
    def go(lo, hi):
        if hi - lo <= 1:
            return recs[lo:hi], 0
        mid = lo + (hi - lo) // 2
        (L, a), (R, b) = go(lo, mid), go(mid, hi)
        c, out = a + b, []
        while L and R:
            c += 1
            out.append(L.pop(0) if L[0][0] <= R[0][0] else R.pop(0))
        return out + L + R, c
    _, c = go(0, len(recs))
    return [sorted(recs, key=lambda r: r[0]), c]

def bottom_up_cmps(keys):
    """Bottom-up (width 1, 2, 4, ...): no recursion, but a different split, so the count can differ."""
    a = [[k, 0] for k in keys]; width = 1; cmps = 0
    while width < len(a):
        nxt = []
        for lo in range(0, len(a), 2 * width):
            L, R = a[lo:lo + width], a[lo + width:lo + 2 * width]
            i = j = 0
            while i < len(L) and j < len(R):
                cmps += 1
                if L[i][0] <= R[j][0]: nxt.append(L[i]); i += 1
                else: nxt.append(R[j]); j += 1
            nxt.extend(L[i:]); nxt.extend(R[j:])
        a, width = nxt, width * 2
    return cmps

examples = [
    ([[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]], [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]),
    ([], [[], 0]),
    ([[9, 0]], [[[9, 0]], 0]),
    ([[1, 1], [2, 2], [3, 3], [4, 4]], [[[1, 1], [2, 2], [3, 3], [4, 4]], 4]),
]
for rec, exp in examples:
    got = merge_sort(rec)
    print(rec, '->', got)
    assert got == exp and brute(rec) == exp

# worst case n*ceil(log2 n) - 2^ceil(log2 n) + 1, exhaustive over all permutations for n <= 8; by hand n = 5: 5*3 - 8 + 1 = 8
for n in range(1, 9):
    worst = max(merge_sort([[v, 0] for v in p])[1] for p in itertools.permutations(range(n)))
    c = math.ceil(math.log2(n))
    assert worst == n * c - 2 ** c + 1, (n, worst)
    print('n =', n, 'worst comparisons over all', math.factorial(n), 'permutations =', worst, '= formula', n * c - 2 ** c + 1)

# bottom-up can differ from top-down (n = 3 sorted input: top-down splits 1|2, bottom-up merges 2 then 1)
diff = [(p, merge_sort([[v, 0] for v in p])[1], bottom_up_cmps(p))
        for n in range(2, 7) for p in itertools.permutations(range(n)) if merge_sort([[v, 0] for v in p])[1] != bottom_up_cmps(p)]
print('bottom-up differs from top-down for', len(diff), 'permutations with n <= 6; first:', diff[0])
assert diff

# the '<' variant is unstable: equal keys come out reversed
def merge_lt(a, b):
    out = []
    while a and b:
        out.append(a.pop(0) if a[0][0] < b[0][0] else b.pop(0))
    return out + a + b
print('with < the two 5s come out as', [r[1] for r in merge_lt([[5, 'first']], [[5, 'second']])])
assert [r[1] for r in merge_lt([[5, 'first']], [[5, 'second']])] == ['second', 'first']

# seeded random cross-check (order AND count vs the separate counter)
for _ in range(400):
    rec = [[random.randint(0, 4), random.randint(0, 9)] for _ in range(random.randint(0, 30))]
    assert merge_sort(rec) == brute(rec)
print('random cross-check ok: 400 cases')

# maximum size: n = 10^5, comparisons <= n * ceil(log2 n)
rec = [[random.randint(-10 ** 9, 10 ** 9), i] for i in range(10 ** 5)]
out, c = merge_sort(rec)
assert out == sorted(rec, key=lambda r: r[0]) and c <= 10 ** 5 * math.ceil(math.log2(10 ** 5))
print('n = 10^5: ok, comparisons', c, '<= n*ceil(log2 n) =', 10 ** 5 * 17)

# edge asserts
assert merge_sort([[2, 0], [2, 1], [2, 2]]) == [[[2, 0], [2, 1], [2, 2]], 2]   # all equal: input order kept; split 1|2 costs 1 + 1
assert merge_sort([[1, 0], [2, 1]])[1] == 1
print('edge asserts ok')
```

**Output (my run):**
```
[[3, 1], [1, 2], [3, 3], [2, 4], [1, 5]] -> [[[1, 2], [1, 5], [2, 4], [3, 1], [3, 3]], 8]
[] -> [[], 0]
[[9, 0]] -> [[[9, 0]], 0]
[[1, 1], [2, 2], [3, 3], [4, 4]] -> [[[1, 1], [2, 2], [3, 3], [4, 4]], 4]
n = 1 worst comparisons over all 1 permutations = 0 = formula 0
n = 2 worst comparisons over all 2 permutations = 1 = formula 1
n = 3 worst comparisons over all 6 permutations = 3 = formula 3
n = 4 worst comparisons over all 24 permutations = 5 = formula 5
n = 5 worst comparisons over all 120 permutations = 8 = formula 8
n = 6 worst comparisons over all 720 permutations = 11 = formula 11
n = 7 worst comparisons over all 5040 permutations = 14 = formula 14
n = 8 worst comparisons over all 40320 permutations = 17 = formula 17
bottom-up differs from top-down for 630 permutations with n <= 6; first: ((0, 1, 2), 2, 3)
with < the two 5s come out as ['second', 'first']
random cross-check ok: 400 cases
n = 10^5: ok, comparisons 1536373 <= n*ceil(log2 n) = 1700000
edge asserts ok
```

**Edge cases:**
- Empty list and single item: zero comparisons.
- Already sorted input: still about (n/2) log2 n comparisons, never O(n). This plain merge sort is not adaptive (Timsort is).
- All equal keys: order unchanged, and with n = 3 it costs 2.
- Keys at +-10^9: Python ints, no overflow.

**Follow-ups:**
- Merge sort a linked list? It is the natural fit (O(1) extra space for the merge): Part 6 Q25 (heading as given).
- Why is merge sort used for objects and quicksort for primitives in some languages? Stability and the worst case against cache-friendly in-place partitioning. General statement, not tested here.
- Count inversions during the merge: Q17 in this part.

**Common mistakes:**
- `<` in the merge, which breaks stability.
- Slicing `a[:mid]` and `a[mid:]` and calling it O(1): slicing copies, which is fine for O(n) per level, but say it.
- Counting leftovers as comparisons.
- Believing the worst case is n log2 n exactly: it is n * ceil(log2 n) - 2^ceil(log2 n) + 1.

### Q16 ⭐⭐⭐ 🟡 Quicksort with the Lomuto partition, iteratively, with exact counts. `nums` has 1 <= len <= 3000 integers (duplicates allowed). Sort them ascending in place with quicksort WITHOUT recursion (use an explicit stack; sorted input of length 1500 makes this recursion nest about 1500 frames, above CPython's default recursion limit of 1000, so a recursive solution fails with RecursionError). Partition a range [lo, hi] with the last element as the pivot: `p = a[hi]; i = lo`; for j in lo..hi-1 do ONE comparison `a[j] < p` and, if true, swap `a[i]` and `a[j]` and do `i += 1`; finally swap `a[i]` with `a[hi]` and recurse (conceptually) on [lo, i - 1] and [i + 1, hi], skipping ranges with fewer than 2 items. Return `[sorted_list, comparisons, depth]`: `comparisons` is the total number of those `a[j] < p` tests, and `depth` is the largest number of nested partition calls the recursive version would reach (the first call counts 1; both are independent of the order in which you process the stack). Explain why an already sorted or all-equal input costs n * (n - 1) / 2 comparisons with depth n - 1 for this pivot rule, why a random pivot makes that unlikely, and why quicksort is not stable. Kth-largest by quickselect is Part 8 Q36; this question is the full sort. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive Lomuto quicksort (small inputs only) and sorted() on small inputs. Example: nums=[3, 1, 2] -> [[1, 2, 3], 2, 1]; nums=[1, 2, 3, 4] -> [[1, 2, 3, 4], 6, 3]; nums=[5, 5, 5] -> [[5, 5, 5], 3, 2]; nums=[4, 2, 7, 1, 9, 3] -> [[1, 2, 3, 4, 7, 9], 8, 2].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Quicksort with the Lomuto partition, made iterative with an explicit stack. Partition around a pivot, then handle both sides.

**Say this first (1 line):** "Pivot is the last element. One pass puts everything smaller than the pivot on the left, the pivot goes to its final slot, then I sort both sides. I use an explicit stack because sorted input nests n frames, and CPython stops at 1000."

**Brute force:** Insertion sort, O(n^2). Or recursive Lomuto quicksort, same algorithm with the call stack: correct on small inputs, but it raises `RecursionError` at n = 1500 sorted (shown in my run).

**Optimal:**
- Partition [lo, hi]: `p = a[hi]`, `i = lo`. For j in lo..hi-1: one comparison `a[j] < p`; if true swap a[i], a[j] and i += 1. Finally swap a[i] and a[hi]. Invariant: a[lo..i-1] < p and a[i..j] >= p.
- Push the two sub-ranges (only if they have at least 2 items) onto a stack of (lo, hi, depth). Popping order does not change the totals: each range is partitioned exactly once, so comparisons and depth do not depend on the order.
- Comparisons per partition = size - 1. Sorted or all-equal input: every partition peels off just the pivot (all equal items are `>= p`, so none moves), so sizes n, n-1, ..., 2: n * (n-1) / 2 comparisons and depth n-1.
- A random pivot makes a bad split unlikely: expected O(n log n) comparisons. In my random run (n = 3000) it used 38,808 comparisons and depth 26 against 4,498,500 for sorted input.
- Not stable: the long-range swaps jump equal items over each other. Smallest case found by search over keys 1 and 2: [(1,'a'), (2,'b'), (2,'c')] comes out with 'c' before 'b' (see output).

**Complexity:** Average O(n log n) time with a random or typical pivot; worst case O(n^2) (sorted, reverse, all equal with this rule). Space O(1) extra beyond the explicit stack, which holds O(depth) entries: O(n) in the worst case here. (Pushing the larger side first and looping on the smaller one would bound it to O(log n); not done here.)

**Dry run:** [3,1,2], pivot 2, i = 0. j=0: 3<2 no. j=1: 1<2 yes, swap a[0],a[1] -> [1,3,2], i=1. Swap a[1],a[2] -> [1,2,3]. 2 comparisons. Both sides have one item, skipped. Depth 1. For [4,2,7,1,9,3] (pivot 3): 5 comparisons give [2,1,3,4,9,7]; the left [2,1] costs 1 and the right [4,9,7] costs 2, total 8, depth 2.

**Code:**
```python
import random
import sys

random.seed(1316)

def quicksort_iter(nums):
    """Lomuto, last element as pivot, explicit stack. depth = most nested partition calls of the recursive version."""
    a = list(nums); cmps = 0; depth = 0
    stack = [(0, len(a) - 1, 1)] if len(a) > 1 else []
    while stack:
        lo, hi, d = stack.pop()
        depth = max(depth, d)
        p, i = a[hi], lo
        for j in range(lo, hi):
            cmps += 1                              # the ONE comparison per item
            if a[j] < p:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]                  # pivot to its final place i
        if i + 1 < hi: stack.append((i + 1, hi, d + 1))   # skip ranges with fewer than 2 items
        if lo < i - 1: stack.append((lo, i - 1, d + 1))
    return [a, cmps, depth]

def brute(nums):
    """Recursive Lomuto (only safe for small inputs)."""
    a = list(nums); cmps = 0; depth = 0
    def rec(lo, hi, d):
        nonlocal cmps, depth
        if lo >= hi: return
        depth = max(depth, d)
        p, i = a[hi], lo
        for j in range(lo, hi):
            cmps += 1
            if a[j] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        rec(lo, i - 1, d + 1); rec(i + 1, hi, d + 1)
    rec(0, len(a) - 1, 1)
    return [a, cmps, depth]

examples = [
    ([3, 1, 2], [[1, 2, 3], 2, 1]),
    ([1, 2, 3, 4], [[1, 2, 3, 4], 6, 3]),
    ([5, 5, 5], [[5, 5, 5], 3, 2]),
    ([4, 2, 7, 1, 9, 3], [[1, 2, 3, 4, 7, 9], 8, 2]),
]
for nums, exp in examples:
    got = quicksort_iter(nums)
    print(nums, '->', got)
    assert got == exp and brute(nums) == exp

# sorted and all-equal input: n(n-1)/2 comparisons, depth n-1
for n in range(1, 40):
    for arr in (list(range(n)), [5] * n):
        r = quicksort_iter(arr)
        assert r[1] == n * (n - 1) // 2 and (r[2] == n - 1 if n > 1 else r[2] == 0)
print('sorted / all-equal: comparisons n(n-1)/2 and depth n-1 verified for n < 40')

# n = 3000: iterative copes, the recursive version hits the default limit (1000)
big = quicksort_iter(list(range(3000)))
assert big[0] == list(range(3000)) and big[1] == 3000 * 2999 // 2 and big[2] == 2999
print('n = 3000 sorted: comparisons', big[1], 'depth', big[2], '| recursion limit', sys.getrecursionlimit())
try:
    brute(list(range(1500)))
    print('recursive n=1500: no error')
except RecursionError:
    print('recursive version, n = 1500: RecursionError')

# random input, n = 3000
rnd = [random.randint(-10 ** 9, 10 ** 9) for _ in range(3000)]
r = quicksort_iter(rnd)
assert r[0] == sorted(rnd)
print('random n = 3000: comparisons', r[1], 'depth', r[2], '(n(n-1)/2 would be', 3000 * 2999 // 2, ')')

# not stable: tag the items and run the same Lomuto on the keys; find an input where equal keys swap order
def lomuto_tagged(items):
    a = list(items)
    def rec(lo, hi):
        if lo >= hi: return
        p, i = a[hi][0], lo
        for j in range(lo, hi):
            if a[j][0] < p:
                a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]
        rec(lo, i - 1); rec(i + 1, hi)
    rec(0, len(a) - 1)
    return a
import itertools
ex = next([(k, 'abc'[i]) for i, k in enumerate(p)] for p in itertools.product([1, 2], repeat=3)
          if [t for k, t in lomuto_tagged([(k, 'abc'[i]) for i, k in enumerate(p)]) if k == 2]
          != [t for k, t in [(k, 'abc'[i]) for i, k in enumerate(p)] if k == 2])
print('unstable example:', ex, '->', lomuto_tagged(ex))

# seeded random cross-check vs recursive Lomuto and sorted()
for _ in range(400):
    nums = [random.randint(-5, 5) for _ in range(random.randint(1, 40))]
    r = quicksort_iter(nums)
    assert r == brute(nums) and r[0] == sorted(nums)
print('random cross-check ok: 400 cases')

# edge asserts
assert quicksort_iter([7]) == [[7], 0, 0]
assert quicksort_iter([2, 1]) == [[1, 2], 1, 1]
print('edge asserts ok')
```

**Output (my run):**
```
[3, 1, 2] -> [[1, 2, 3], 2, 1]
[1, 2, 3, 4] -> [[1, 2, 3, 4], 6, 3]
[5, 5, 5] -> [[5, 5, 5], 3, 2]
[4, 2, 7, 1, 9, 3] -> [[1, 2, 3, 4, 7, 9], 8, 2]
sorted / all-equal: comparisons n(n-1)/2 and depth n-1 verified for n < 40
n = 3000 sorted: comparisons 4498500 depth 2999 | recursion limit 1000
recursive version, n = 1500: RecursionError
random n = 3000: comparisons 38808 depth 26 (n(n-1)/2 would be 4498500 )
unstable example: [(1, 'a'), (2, 'b'), (2, 'c')] -> [(1, 'a'), (2, 'c'), (2, 'b')]
random cross-check ok: 400 cases
edge asserts ok
```

**Edge cases:**
- One element: no partition, 0 comparisons, depth 0 (the first call counts only when a range of at least 2 items exists).
- Sorted, reverse sorted, all equal: the quadratic cases, n * (n-1) / 2 for sorted and all-equal.
- Many duplicates: Lomuto degrades; three-way partition fixes it (another question in this part).
- n = 3000 sorted: 4,498,500 comparisons, still fast enough here.

**Follow-ups:**
- Why not raise `sys.setrecursionlimit`? It only moves the crash (very deep recursion can kill the interpreter; editor knowledge, not tested here); the stack-based version is the safe answer.
- Hoare partition? Fewer swaps, different pivot rules, covered by another question in this part.
- Kth largest without a full sort: quickselect, Part 8 Q36.

**Common mistakes:**
- Recursing on sorted input and hitting `RecursionError`.
- Pushing ranges with 0 or 1 items.
- Using `<=` in the Lomuto test, which moves equal items and changes the counts.
- Saying quicksort is stable. It is not.

### Q17 ⭐⭐⭐ 🟡 Count inversions with merge sort. `nums` has 0 <= len <= 10^5 integers (|value| <= 10^9, duplicates allowed). An inversion is a pair of positions i < j with nums[i] > nums[j] (strictly greater, equal values do not count). Return the number of inversions in O(n log n). During the merge of two sorted halves, when the next item taken comes from the right half, it is smaller than every item still waiting in the left half, so add the number of items remaining in the left half; take from the left when `left <= right` so ties are not counted. Explain why the count over the whole array is the sum of the left-half inversions, the right-half inversions and the cross inversions found while merging, why a merge cannot change the cross count (sorted halves), the maximum n * (n - 1) / 2 (strictly decreasing input) and that this number equals the number of element shifts made by insertion sort. The recursion depth is about log2 n (under 20), so recursion is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n^2) double loop on small inputs. Example: nums=[2, 4, 1, 3, 5] -> 3; nums=[5, 4, 3, 2, 1] -> 10; nums=[1, 1, 1] -> 0; nums=[] -> 0; nums=[3, 1, 2, 3, 1] -> 5.
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Merge sort with a counter. Count cross pairs while merging.

**Say this first (1 line):** "An inversion is i < j with nums[i] > nums[j]. Merge sort counts them: when I take an item from the right half, it is smaller than every item still waiting in the left half, so I add that many. O(n log n)."

**Brute force:** Two loops over every pair, O(n^2). For n = 10^5 that is 5 x 10^9 pair checks: too slow.

**Optimal:**
- Total inversions = inversions inside the left half + inside the right half + cross pairs (one item left, one right).
- Merge two sorted halves with two pointers. If `a[i] <= a[j]` take left (no count; equal values are not inversions). Else take right and add `mid - i`: the left items from i onward are all greater than a[j], because the left half is sorted.
- A merge never changes the cross count for a higher level: the halves are sorted, and the cross pairs between two sets do not depend on the order inside each set. Sorting the halves loses nothing.
- Maximum n * (n-1) / 2, reached by a strictly decreasing array (checked for n <= 11 and at n = 10^5).
- This number equals the shifts insertion sort makes: each shift moves one item past a strictly larger earlier item, which is exactly one inversion (checked equal on 400 random cases).
- Recursion depth is about log2 n (17 for n = 10^5), fine.

**Complexity:** O(n log n) time, O(n) space for the buffer. Counts can reach about 5 x 10^9 at n = 10^5, which is fine for Python ints (in a fixed-width language you need 64 bits).

**Dry run:** [2,4,1,3,5], split [2,4] | [1,3,5]. Inside each half: no inversions. Merge: 2 vs 1: 1 is smaller, take it, add the 2 left items (2 and 4): +2. 2 vs 3: take 2. 4 vs 3: take 3, add 1 (just 4): +1. 4 vs 5: take 4. Take 5. Total 3: (2,1), (4,1), (4,3).

**Code:**
```python
import random

random.seed(1317)

def count_inversions(nums):
    """Merge sort; when the right item is taken, it beats every item still waiting on the left."""
    a = list(nums)
    buf = [0] * len(a)
    def sort(lo, hi):
        if hi - lo <= 1:
            return 0
        mid = (lo + hi) // 2
        inv = sort(lo, mid) + sort(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if a[i] <= a[j]:                 # tie: take LEFT, equal values are not inversions
                buf[k] = a[i]; i += 1
            else:
                buf[k] = a[j]; j += 1
                inv += mid - i               # everything left in the left half is > a[j]
            k += 1
        while i < mid: buf[k] = a[i]; i += 1; k += 1
        while j < hi: buf[k] = a[j]; j += 1; k += 1
        a[lo:hi] = buf[lo:hi]
        return inv
    return sort(0, len(a))

def brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] > nums[j])

def insertion_shifts(nums):
    a = list(nums); shifts = 0
    for i in range(1, len(a)):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:          # strict >: equal items are not shifted
            a[j + 1] = a[j]; j -= 1; shifts += 1
        a[j + 1] = x
    return shifts

examples = [([2, 4, 1, 3, 5], 3), ([5, 4, 3, 2, 1], 10), ([1, 1, 1], 0), ([], 0), ([3, 1, 2, 3, 1], 5)]
for nums, exp in examples:
    got = count_inversions(nums)
    print(nums, '->', got)
    assert got == exp and brute(nums) == exp

# the '<' tie rule would count equal pairs as inversions
def wrong_tie(nums):
    n = len(nums); return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] >= nums[j])
print('counting ties too, [1, 1, 1] would give', wrong_tie([1, 1, 1]))

# max n(n-1)/2 for strictly decreasing input
for n in range(0, 12):
    assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
print('strictly decreasing input gives n(n-1)/2 for n <= 11')

# inversions == insertion-sort shifts; cross-check against the double loop
for _ in range(400):
    nums = [random.randint(-6, 6) for _ in range(random.randint(0, 25))]
    c = count_inversions(nums)
    assert c == brute(nums) == insertion_shifts(nums)
print('random cross-check ok: 400 cases (merge count == double loop == insertion shifts)')

# maximum size: n = 10^5 (decreasing = worst case, random, all equal)
n = 10 ** 5
assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
r = [random.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
print('n = 10^5 random:', count_inversions(r), '(about n(n-1)/4 =', n * (n - 1) // 4, ')')
assert count_inversions([7] * n) == 0

# edge asserts
assert count_inversions([1]) == 0 and count_inversions([2, 1]) == 1 and count_inversions([1, 2]) == 0
print('edge asserts ok')
```

**Output (my run):**
```
[2, 4, 1, 3, 5] -> 3
[5, 4, 3, 2, 1] -> 10
[1, 1, 1] -> 0
[] -> 0
[3, 1, 2, 3, 1] -> 5
counting ties too, [1, 1, 1] would give 3
strictly decreasing input gives n(n-1)/2 for n <= 11
random cross-check ok: 400 cases (merge count == double loop == insertion shifts)
n = 10^5 random: 2505411528 (about n(n-1)/4 = 2499975000 )
edge asserts ok
```

**Edge cases:**
- Empty and single: 0.
- All equal: 0. Using `<` in the take-left test (or counting `>=`) would count ties: [1,1,1] would give 3.
- Strictly decreasing: n * (n-1) / 2.
- Duplicates mixed with distinct values, like [3,1,2,3,1] giving 5.

**Follow-ups:**
- Count only "significant" pairs, nums[i] > 2 * nums[j]? Count before merging with a second pointer; same O(n log n).
- Same with a Fenwick tree after coordinate compression? Yes, O(n log n); Fenwick trees are Part 14 (named only).
- Minimum adjacent swaps to sort: equals the inversion count for distinct values.

**Common mistakes:**
- Adding 1 instead of `mid - i` when taking from the right.
- `<` vs `<=` on ties.
- Counting after the halves are merged back (positions are lost), instead of during the merge.
- Slicing the array every call, giving O(n) extra copies per level; use a shared buffer as in my code.

### Q18 ⭐⭐ 🟢 Happy number. For a positive integer n, repeatedly replace it by the sum of the squares of its decimal digits. `n` is an integer with 1 <= n <= 2^31 - 1. Return `[happy, steps, cycle_len]`: `happy` is True if the sequence reaches 1; `steps` is the number of replacements needed to reach 1 from n (0 when n is 1) or -1 when n is not happy; `cycle_len` is the length of the cycle the sequence eventually enters (1 for a happy number, because 1 maps to itself; for the others it is a fixed length you should find). Detect the cycle with Floyd's tortoise and hare in O(1) space (and compare it with a set of seen values). Explain why the sequence cannot grow forever (for a number with 4 or more digits the digit-square sum is smaller than the number, and for any 10-digit input it is at most 810) so it must repeat, and name the cycle every unhappy number ends in. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a dictionary of seen values to positions on small inputs. Example: n=19 -> [True, 4, 1]; n=2 -> [False, -1, 8]; n=1 -> [True, 0, 1]; n=7 -> [True, 5, 1]; n=4 -> [False, -1, 8].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Cycle detection on a number sequence (Floyd's tortoise and hare), plus a small proof that the sequence is bounded.

**Say this first (1 line):** "The map n -> sum of squared digits eventually repeats, because it shrinks large numbers. A happy number reaches the fixed point 1; every other number ends in the same 8-cycle 4, 16, 37, 58, 89, 145, 42, 20. Floyd's two pointers find it in O(1) space."

**Brute force:** Keep a dict `seen[value] = position`. Stop when a value repeats; the cycle length is the current position minus the earlier one. O(steps) time and space. Simple and what I check against.

**Optimal:**
- Floyd: slow moves one step, fast moves two. Stop when fast is 1 or slow == fast. If it stopped on 1 the number is happy. Otherwise `fast` is now inside the cycle.
- Cycle length: from that point step until you return to it, counting.
- Steps (for a happy number): just apply the map again from n until 1.
- Why it must repeat: for a number with d digits the digit-square sum is at most 81 d. For d >= 4, 81 d < 10^(d-1) <= n, so the sum is smaller than n (I checked f(n) < n for every n from 1000 to 300,000 and the inequality for d up to 39). So every value drops below 1000 and then stays under 243 (at most 3 x 81). A 10-digit input (the 2^31-1 range) gives at most 810 after one step. A finite set of values forces a repeat.
- The cycle for unhappy numbers is [4, 16, 37, 58, 89, 145, 42, 20], length 8. I checked every n < 200,000: happy implies cycle length 1, and every other number has cycle length 8.

**Complexity:** Each step costs O(digits), about 10 for the input range. The number of steps is small (the first step brings any input under 811; the output shows the longest run I measured). O(1) extra space for Floyd; the dict version is O(steps).

**Dry run:** n = 19: 1 + 81 = 82, 64 + 4 = 68, 36 + 64 = 100, 1 + 0 + 0 = 1. That is 4 steps, happy, cycle length 1 (1 maps to 1). Floyd on 19: slow 19, fast 82. Move: slow 82, fast f(f(82)) = 100. Move: slow 68, fast f(f(100)) = f(1) = 1. Stop on 1. n = 2: 4, 16, 37, 58, 89, 145, 42, 20, 4: back to 4 after 8 steps, so [False, -1, 8].

**Code:**
```python
import random

random.seed(1318)

def f(v):
    s = 0
    while v:
        v, d = divmod(v, 10)
        s += d * d
    return s

def happy(n):
    """Floyd: tortoise moves 1 step, hare 2; O(1) space. Then measure the cycle length from the meeting point."""
    slow, fast = n, f(n)
    while fast != 1 and slow != fast:
        slow, fast = f(slow), f(f(fast))
    x, c = fast, 1                          # fast is inside the cycle (or is 1)
    y = f(x)
    while y != x:
        y, c = f(y), c + 1
    steps = -1
    if fast == 1 or n == 1:
        steps, v = 0, n
        while v != 1:
            v, steps = f(v), steps + 1
    return [steps >= 0, steps, c]

def brute(n):
    """Dictionary of seen value -> position."""
    seen, v, i = {}, n, 0
    while v not in seen:
        seen[v] = i; i += 1
        v = f(v)
    return [1 in seen, seen.get(1, -1), i - seen[v]]

examples = [(19, [True, 4, 1]), (2, [False, -1, 8]), (1, [True, 0, 1]), (7, [True, 5, 1]), (4, [False, -1, 8])]
for n, exp in examples:
    got = happy(n)
    print(n, '->', got)
    assert got == exp and brute(n) == exp
print('trace of 19:', [19, f(19), f(f(19)), f(f(f(19))), f(f(f(f(19))))])

# exhaustive: every n < 200000 is happy or ends in the 8-cycle; list the cycle
for n in range(1, 200000):
    h, st, cl = happy(n)
    assert (cl == 1) if h else (cl == 8)
    assert [h, st, cl] == brute(n)
cyc, v = [], 4
while True:
    cyc.append(v); v = f(v)
    if v == 4: break
print('unhappy cycle:', cyc, '| checked every n < 200000: happy => cycle 1, unhappy => cycle of 8')

# why the sequence cannot grow: f(n) < n for n >= 1000 (checked), and the 10-digit bound
assert all(f(n) < n for n in range(1000, 300000))
assert all(81 * k < 10 ** (k - 1) for k in range(4, 40))
print('81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) =', f(2 ** 31 - 1),
      ', f(1999999999) =', f(1999999999))
assert f(2 ** 31 - 1) <= 810 and max(f(n) for n in range(10 ** 9, 10 ** 9 + 1000)) <= 810

# longest run before a value repeats, over every n < 100000
def run_len(n):
    seen, v = set(), n
    while v not in seen:
        seen.add(v); v = f(v)
    return len(seen)
print('longest run before a repeat for n < 100000:', max(run_len(n) for n in range(1, 100000)), 'values')

# seeded random cross-check on large values too
for _ in range(500):
    n = random.choice([random.randint(1, 3000), random.randint(1, 2 ** 31 - 1)])
    assert happy(n) == brute(n)
print('random cross-check ok: 500 cases')

# edge asserts
assert happy(2 ** 31 - 1)[0] in (True, False)
assert happy(10) == [True, 1, 1] and happy(100) == [True, 1, 1] and happy(1) == [True, 0, 1]
print('edge asserts ok; 2^31-1 ->', happy(2 ** 31 - 1))
```

**Output (my run):**
```
19 -> [True, 4, 1]
2 -> [False, -1, 8]
1 -> [True, 0, 1]
7 -> [True, 5, 1]
4 -> [False, -1, 8]
trace of 19: [19, 82, 68, 100, 1]
unhappy cycle: [4, 16, 37, 58, 89, 145, 42, 20] | checked every n < 200000: happy => cycle 1, unhappy => cycle of 8
81*d < 10^(d-1) for every d >= 4; 10-digit bound 10*81 = 810; f(2^31-1) = 260 , f(1999999999) = 730
longest run before a repeat for n < 100000: 20 values
random cross-check ok: 500 cases
edge asserts ok; 2^31-1 -> [False, -1, 8]
```

**Edge cases:**
- n = 1: 0 steps, cycle 1.
- n = 10, 100: one step to 1.
- Largest input 2^31 - 1 is unhappy (result `[False, -1, 8]`).
- n = 4 (inside the unhappy cycle already): `[False, -1, 8]`.

**Follow-ups:**
- Why not just detect "reaches 4"? That works (the whole unhappy family goes through 4), but the proof that 4 is on every unhappy path is the same exhaustive check; Floyd or a set needs no such fact.
- Same technique elsewhere? Linked-list cycle (Floyd), and duplicate-number-as-cycle problems.
- Count happy numbers below N? Precompute with the map for each value; the map shrinks, so a memo works.

**Common mistakes:**
- Fast pointer started equal to slow, so the loop exits immediately.
- Assuming the sequence grows forever for big inputs.
- Forgetting n = 1 (already happy, 0 steps).
- Recomputing digits with strings in a hot loop without need (fine here, but say it).

### Q19 ⭐⭐ 🟢 Excel column titles and numbers. `title` is a column title of 1 to 7 uppercase letters whose number is at most 2^31 - 1 (A = 1, ..., Z = 26, AA = 27, AB = 28, ..., AZ = 52, BA = 53, ...), and `number` is an integer with 1 <= number <= 2^31 - 1. Return `[number_of_title, title_of_number]`. This is base 26 with digits 1..26 and no zero digit (bijective numeration). Convert a title with `r = r * 26 + (ord(ch) - 64)` and a number with the loop `n, d = divmod(n - 1, 26)` taking letter `chr(65 + d)`, then reverse; explain why the `n - 1` is needed (there is no zero digit, so plain base 26 would turn 26 into nonsense: the naive `divmod(n, 26)` with `chr(64 + d)` gives 'A@' for 26 and 'B@' for 52, not 'Z' and 'AZ') and why both directions are O(length), about log26 of the value. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an explicit table of all titles up to length 4 on small inputs. Example: title='AB', number=28 -> [28, 'AB']; title='A', number=1 -> [1, 'A']; title='ZY', number=701 -> [701, 'ZY']; title='FXSHRXW', number=2147483647 -> [2147483647, 'FXSHRXW'].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Bijective base 26 (digits 1..26, no zero). Number base conversion with an offset.

**Say this first (1 line):** "Title to number is a plain Horner loop, r = r * 26 + (ord(ch) - 64). Number to title peels letters with divmod(n - 1, 26); the minus one is there because there is no zero digit."

**Brute force:** Build a table of every title in order (A..Z, AA..ZZ, ...) and look up by position or by index. Fine for short titles; the table grows 26^L, so it cannot hold seven-letter titles. I use it for all titles up to four letters (475,254 of them).

**Optimal:**
- Title to number: each letter is a digit 1..26. Horner: r = r * 26 + digit. 'AB' = 1 * 26 + 2 = 28.
- Number to title: shift by one first. `n, d = divmod(n - 1, 26)` gives a digit 0..25, which is the letter `chr(65 + d)`. Repeat while n > 0, then reverse the collected letters.
- Why n - 1: in plain base 26 a remainder of 0 means "no letter". The titles have no zero digit, so 26 must be 'Z', not "1 then 0". Subtracting 1 turns digits 1..26 into 0..25 each round. Plain `divmod(n, 26)` gives '@' for a zero remainder (`26 -> 'A@'`, `52 -> 'B@'` in the output).
- Both directions loop once per letter: about log26 of the value. The largest allowed number 2^31 - 1 is the 7-letter title 'FXSHRXW'; the next title 'FXSHRXX' is exactly 2^31.

**Complexity:** O(L), L = number of letters (at most 7). Space O(L) for the output.

**Dry run:** number 28: divmod(27, 26) = (1, 1): letter 'B'. n = 1: divmod(0, 26) = (0, 0): letter 'A'. Collected 'BA', reversed 'AB'. Title 'AB': r = 0*26 + 1 = 1, then 1*26 + 2 = 28. Check 26: divmod(25, 26) = (0, 25), letter 'Z'.

**Code:**
```python
import itertools
import random
import string

random.seed(1319)

def title_to_number(title):
    r = 0
    for ch in title:
        r = r * 26 + (ord(ch) - 64)         # A=1 .. Z=26: digits 1..26, no zero digit
    return r

def number_to_title(n):
    out = []
    while n:
        n, d = divmod(n - 1, 26)            # shift to 0..25 first, then peel a letter
        out.append(chr(65 + d))
    return ''.join(reversed(out))

def solve(title, number):
    return [title_to_number(title), number_to_title(number)]

# brute force: an explicit table of ALL titles up to length 4, in order (shorter first, then alphabetical)
TABLE = [''.join(p) for L in range(1, 5) for p in itertools.product(string.ascii_uppercase, repeat=L)]
INDEX = {t: i + 1 for i, t in enumerate(TABLE)}
assert len(TABLE) == 26 + 26 ** 2 + 26 ** 3 + 26 ** 4

def brute(title, number):
    # for the 7-letter maximum the table is too small, so fall back to digit-by-digit counting
    if len(title) <= 4 and number <= len(TABLE):
        return [INDEX[title], TABLE[number - 1]]
    k, L = number - 1, 1
    while k >= 26 ** L:
        k -= 26 ** L; L += 1
    digs = []
    for _ in range(L):
        k, r = divmod(k, 26); digs.append(chr(65 + r))
    return [sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(title))), ''.join(reversed(digs))]

examples = [('AB', 28, [28, 'AB']), ('A', 1, [1, 'A']), ('ZY', 701, [701, 'ZY']),
            ('FXSHRXW', 2147483647, [2147483647, 'FXSHRXW'])]
for t, n, exp in examples:
    got = solve(t, n)
    print(t, n, '->', got)
    assert got == exp and brute(t, n) == exp

# why n - 1: plain base 26 breaks on the multiples of 26
def naive(n):
    out = []
    while n:
        n, d = divmod(n, 26); out.append(chr(64 + d))     # d == 0 gives '@'
    return ''.join(reversed(out))
print('naive divmod(n, 26): 26 ->', repr(naive(26)), ', 52 ->', repr(naive(52)), '| with n-1:', number_to_title(26), number_to_title(52))
assert naive(26) == '@' + '' or '@' in naive(26)

# round trip over the WHOLE table (475254 titles) and against the table in both directions
for i, t in enumerate(TABLE, start=1):
    assert title_to_number(t) == i and number_to_title(i) == t
print('round trip ok for all', len(TABLE), 'titles up to length 4')

# seeded random cross-check
for _ in range(500):
    L = random.randint(1, 4)
    t = ''.join(random.choice(string.ascii_uppercase) for _ in range(L))
    n = random.randint(1, len(TABLE))
    assert solve(t, n) == brute(t, n)
print('random cross-check ok: 500 cases')

# limits: 2^31 - 1 is 7 letters, and 8 letters would overflow int32 (Python has no overflow; the bound is the prompt's)
assert number_to_title(2 ** 31 - 1) == 'FXSHRXW' and len(number_to_title(2 ** 31 - 1)) == 7
assert title_to_number('FXSHRXX') > 2 ** 31 - 1
print('length of title(2^31-1) =', len(number_to_title(2 ** 31 - 1)), '; next title FXSHRXX =', title_to_number('FXSHRXX'))

# edge asserts
assert number_to_title(26) == 'Z' and number_to_title(27) == 'AA' and number_to_title(52) == 'AZ' and number_to_title(53) == 'BA'
assert number_to_title(703) == 'AAA'
assert title_to_number('Z') == 26 and title_to_number('AA') == 27 and title_to_number('ZZ') == 702 and number_to_title(702) == 'ZZ'
print('edge asserts ok')
```

**Output (my run):**
```
AB 28 -> [28, 'AB']
A 1 -> [1, 'A']
ZY 701 -> [701, 'ZY']
FXSHRXW 2147483647 -> [2147483647, 'FXSHRXW']
naive divmod(n, 26): 26 -> 'A@' , 52 -> 'B@' | with n-1: Z AZ
round trip ok for all 475254 titles up to length 4
random cross-check ok: 500 cases
length of title(2^31-1) = 7 ; next title FXSHRXX = 2147483648
edge asserts ok
```

**Edge cases:**
- 26 -> 'Z', 27 -> 'AA', 52 -> 'AZ', 53 -> 'BA', 702 -> 'ZZ', 703 -> 'AAA'.
- Single letter.
- The maximum 2^31 - 1: 'FXSHRXW'. Python has no overflow, so the only limit is the prompt's bound.
- Number 0 is not valid input; the loop would return an empty string.

**Follow-ups:**
- Why does this differ from hexadecimal? Hex has a zero digit; this system does not, so every value has a unique spelling without leading zeros.
- Add two column titles? Convert, add, convert back.
- Generalise to base b with digits 1..b: same loop with 26 replaced by b.

**Common mistakes:**
- `divmod(n, 26)` with `chr(64 + d)` and no `- 1`: '@' for multiples of 26.
- Taking the digit from n - 1 but dividing plain n by 26 (wrong at 26, 52, 702).
- Forgetting to reverse the letters.
- Using `ord(ch) - 65` for the title direction (A would be 0 and 'AA' collides with 'A').

### Q20 ⭐⭐ 🟢 Pascal's triangle. `num_rows` is an integer with 0 <= num_rows <= 30 and `row_index` is an integer with 0 <= row_index <= 200. Return `[triangle, row]`: `triangle` is the first `num_rows` rows as lists (row i has i + 1 entries, starts and ends with 1, and every inner entry is the sum of the two above it; `num_rows = 0` gives an empty list), and `row` is row number `row_index` (0-indexed) alone, built with only O(row_index) extra space by updating one list from right to left. Explain why the right-to-left order matters, give the closed form C(n, k) = n! / (k! (n - k)!) and the recurrence C(n, k) = C(n, k-1) * (n - k + 1) / k that is always an exact integer step, and say from which row on the entries stop fitting in a signed 32-bit integer (the largest entry of row 33 is below 2^31 - 1 and row 34 has an entry above it) while Python needs no change. In the answer include a dry run on the first example and a seeded random cross-check of your solution against math.comb on small inputs. Example: num_rows=5, row_index=4 -> [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]; num_rows=0, row_index=0 -> [[], [1]]; num_rows=1, row_index=1 -> [[[1]], [1, 1]]; num_rows=3, row_index=10 -> [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]].
**Asked at:** Number-theory and math pattern guides (techinterview.org math and number-theory posts, talentd.in math topic pages; search snippets only, not opened)

**Pattern:** Dynamic programming on a triangle (Pascal), with a one-row, right-to-left update for O(row) space.

**Say this first (1 line):** "Each entry is the sum of the two above it, edges are 1. For a single row I keep one list and update it from right to left, so the value I read from the left is still last row's value. That is O(row_index) space."

**Brute force:** Use the closed form C(n, k) = n! / (k! (n-k)!) per entry. Correct, but computing factorials per entry wastes work; `math.comb` is the checked reference here (`math.comb` exists since 3.8, editor knowledge).

**Optimal:**
- Triangle: row i = [1] + [prev[j-1] + prev[j] for j in 1..i-1] + [1]; row 0 is [1]; `num_rows = 0` returns [].
- Single row without keeping rows: start with row = [1] * (n + 1). For i from 1 to n, update j = i-1 down to 1 with `row[j] += row[j-1]`. Right to left: `row[j-1]` has not been touched in this round yet, so it still holds last round's value. Left to right would add an already-updated neighbour: for row 4 it gives [1, 4, 8, 9, 1] (shown in the output).
- Multiplicative recurrence: C(n, k) = C(n, k-1) * (n - k + 1) / k. Multiply first, then use integer `//`: the division is always exact (checked for every row below 200), so no floats are needed.
- Overflow: Python ints do not overflow. In a signed 32-bit integer the largest entry of row 33 is 1,166,803,110 (fits under 2,147,483,647) and row 34 has an entry 2,333,606,220 (does not), so from row 34 on you need 64 bits in other languages.

**Complexity:** Triangle: O(num_rows^2) time and space (it is the output). One row: O(n^2) time for the nested loop, O(n) space. The multiplicative way is O(n) time for the row (n big-int multiplications), also O(n) space.

**Dry run:** row_index 4: row = [1,1,1,1,1]. i=1: nothing to update. i=2: j=1: row[1] = 1 + 1 = 2 -> [1,2,1,1,1]. i=3: j=2: row[2] = 1 + 2 = 3; j=1: row[1] = 2 + 1 = 3 -> [1,3,3,1,1]. i=4: j=3: 1+3 = 4; j=2: 3+3 = 6; j=1: 3+1 = 4 -> [1,4,6,4,1].

**Code:**
```python
import math
import random

random.seed(1320)

def pascal(num_rows, row_index):
    tri = []
    for i in range(num_rows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = tri[i - 1][j - 1] + tri[i - 1][j]
        tri.append(row)
    row = [1] * (row_index + 1)
    for i in range(1, row_index + 1):
        for j in range(i - 1, 0, -1):          # RIGHT to LEFT: row[j-1] is still last row's value when we use it
            row[j] += row[j - 1]
    return [tri, row]

def brute(num_rows, row_index):
    return [[[math.comb(i, j) for j in range(i + 1)] for i in range(num_rows)],
            [math.comb(row_index, j) for j in range(row_index + 1)]]

examples = [
    (5, 4, [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]),
    (0, 0, [[], [1]]),
    (1, 1, [[[1]], [1, 1]]),
    (3, 10, [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]),
]
for nr, ri, exp in examples:
    got = pascal(nr, ri)
    print(nr, ri, '->', got)
    assert got == exp and brute(nr, ri) == exp

# left-to-right update is wrong: it re-uses a value already overwritten
def wrong_row(n):
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, i):
            row[j] += row[j - 1]
    return row
print('left-to-right row 4:', wrong_row(4), '(correct [1, 4, 6, 4, 1])')
assert wrong_row(4) != [1, 4, 6, 4, 1]

# the multiplicative recurrence C(n,k) = C(n,k-1) * (n-k+1) / k is ALWAYS exact: multiply first, then //
for n in range(0, 200):
    c = 1
    for k in range(1, n + 1):
        assert (c * (n - k + 1)) % k == 0
        c = c * (n - k + 1) // k
        assert c == math.comb(n, k)
print('exact-division recurrence checked for every row n < 200')

# int32 boundary: largest entry of row 33 is below 2^31 - 1, row 34 has an entry above it
mx = lambda n: max(math.comb(n, k) for k in range(n + 1))
print('max entry row 33 =', mx(33), ' row 34 =', mx(34), ' 2^31 - 1 =', 2 ** 31 - 1)
assert mx(33) < 2 ** 31 - 1 < mx(34) and all(mx(n) < 2 ** 31 - 1 for n in range(34))

# row sums are 2^n; symmetry
for n in range(0, 61):
    r = pascal(0, n)[1]
    assert sum(r) == 2 ** n and r == r[::-1]
print('row sums 2^n and symmetry ok for n <= 60')

# seeded random cross-check against math.comb
for _ in range(300):
    nr, ri = random.randint(0, 30), random.randint(0, 200)
    assert pascal(nr, ri) == brute(nr, ri)
print('random cross-check ok: 300 cases')

# edge asserts
assert pascal(0, 0) == [[], [1]] and pascal(2, 0)[1] == [1] and len(pascal(30, 200)[0]) == 30 and len(pascal(30, 200)[1]) == 201
print('edge asserts ok; C(200, 100) has', len(str(math.comb(200, 100))), 'digits')
```

**Output (my run):**
```
5 4 -> [[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]], [1, 4, 6, 4, 1]]
0 0 -> [[], [1]]
1 1 -> [[[1]], [1, 1]]
3 10 -> [[[1], [1, 1], [1, 2, 1]], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]
left-to-right row 4: [1, 4, 8, 9, 1] (correct [1, 4, 6, 4, 1])
exact-division recurrence checked for every row n < 200
max entry row 33 = 1166803110  row 34 = 2333606220  2^31 - 1 = 2147483647
row sums 2^n and symmetry ok for n <= 60
random cross-check ok: 300 cases
edge asserts ok; C(200, 100) has 59 digits
```

**Edge cases:**
- num_rows = 0: empty triangle; row_index = 0: [1].
- Rows are symmetric and sum to 2^n (checked for n <= 60).
- Row 200 has entries with up to 59 digits (C(200, 100)); Python handles it.
- `num_rows` and `row_index` are independent inputs here.

**Follow-ups:**
- Why is the sum 2^n? Each element in a set of n is in or out of a subset; C(n, k) counts subsets of size k.
- Row mod a prime for large n? Use the multiplicative recurrence with a modular inverse (modular inverse is another question in this part).
- Only the k-th entry? One loop of the recurrence, O(k) time, O(1) space.

**Common mistakes:**
- Updating left to right and corrupting the row.
- Writing the recurrence with float division (`/`) and getting rounding errors for large rows.
- Off-by-one: row 0 is [1] (row_index is 0-indexed).
- Forgetting that `num_rows = 0` must return `[]`, not `[[]]`.

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

### Q31 ⭐⭐ 🟡 Floating point versus exact arithmetic. `prices` has 1 to 50 decimal strings (each like '0.10' or '-3.2', at most 3 decimals) and `target` is a decimal string. Return `[float_sum, exact_sum, equal, close, fsum]`: `float_sum = repr(s)` where s adds `float(p)` for the prices left to right starting from 0.0; `exact_sum` is `str(Fraction)` of the exact sum of the decimal prices (e.g. '3/10'); `equal` is `s == float(target)`; `close` is `math.isclose(s, float(target))` with its default relative tolerance 1e-9 and no absolute tolerance; `fsum = repr(math.fsum(floats))`. Explain why 0.1 + 0.2 == 0.3 is False (the doubles for 0.1, 0.2 and 0.3 are not those decimals), why you should compare floats with `math.isclose` (and why `math.isclose(1e-12, 0.0)` is False unless you give `abs_tol`), why `math.fsum` is more accurate than the plain left-to-right loop `s += v` (observed on Python 3.13: the built-in `sum` of floats is itself compensated, so `sum([0.1] * 10)` is 1.0 while the loop gives 0.9999999999999999; do not assume that for older versions), and when to switch to `Fraction` (exact rationals) or `Decimal` (decimal money) or integer cents. In the answer include a dry run on the first example and a seeded random cross-check of your solution against exact Fraction arithmetic built from the decimal strings on small inputs. Example: prices=['0.1', '0.2'], target='0.3' -> ['0.30000000000000004', '3/10', False, True, '0.30000000000000004']; prices=['0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1', '0.1'], target='1' -> ['0.9999999999999999', '1', False, True, '1.0']; prices=['0.25', '0.5'], target='0.75' -> ['0.75', '3/4', True, True, '0.75']; prices=['19.99', '5.01', '-0.5'], target='24.5' -> ['24.5', '49/2', True, True, '24.5'].
**Asked at:** Python documentation for int, float, Decimal and Fraction (docs.python.org fetch failed with ENOTFOUND, not opened; behaviour verified by running Python 3.13)

**Pattern:** Numeric representation. Binary floats store the nearest double, not the decimal you typed. So: compare with a tolerance, sum with `math.fsum`, and use `Fraction`, `Decimal` or integer cents when the answer must be exact.

**Say this first (1 line):** "0.1, 0.2 and 0.3 are not stored exactly, so I never use `==` on computed floats; I use `math.isclose` with an explicit tolerance, `math.fsum` for sums, and exact types (`Fraction`, `Decimal`, integer cents) for money."

**Brute force:** Parse each decimal string by hand into an exact `Fraction` (integer of all digits over a power of ten), add them, and separately add the floats left to right. That is the oracle in the code. It is exact but slow and verbose. The point of the question is knowing which tool to reach for.

**Optimal:**
- `float_sum`: `s = 0.0; for v in floats: s += v`. A plain loop, on purpose, to show the drift.
- `exact_sum`: `sum(Fraction(Decimal(p)))`. `Decimal('0.1')` is exactly one tenth, so the `Fraction` is exactly 1/10.
- `equal`: `s == float(target)`. `close`: `math.isclose(s, float(target))`, default `rel_tol=1e-9`, `abs_tol=0.0`.
- `fsum`: `math.fsum(floats)` returns the correctly rounded sum of the doubles it was given.
- Why `0.1 + 0.2 == 0.3` is False: the doubles are `3602879701896397/36028797018963968`, `3602879701896397/18014398509481984` and `5404319552844595/18014398509481984` (printed in the run). None is the decimal value. The sum of the first two rounds to a double that is one step above the double for 0.3.
- `math.isclose(1e-12, 0.0)` is False: the tolerance is relative (`1e-9 * max(|a|, |b|)` = 1e-21 here), and relative to zero nothing is close. Give `abs_tol` (for example `1e-9`) when zero is a possible target.
- `fsum` versus the loop: each `s += v` rounds, and the rounding errors pile up (1000 times 0.1 gives `99.9999999999986` in the loop). `fsum` tracks the lost low-order bits and rounds once.
- Observed on Python 3.13 (this run): the built-in `sum([0.1] * 10)` is `1.0` while the loop gives `0.9999999999999999`. So on 3.13 `sum` of floats is itself compensated. That the change came in 3.12 is editor knowledge, not tested here; do not assume it on older versions and use `math.fsum` when it matters.
- When to leave floats: `Fraction` for exact rationals (slow, can grow); `Decimal` for decimal money with explicit rounding (build it from strings, never from a float: `Decimal(0.1)` is the long exact double); integer cents for the fastest, simplest exact money. Note that `fsum` is exact for the doubles, not for your decimals: the sum of the doubles `0.1`, `0.2` is `0.30000000000000004` even under `fsum`.

**Complexity:** O(n) time for each of the sum, `fsum` and the `Fraction` total (the `Fraction` sum has denominators up to 1000, so each addition is cheap). O(n) space for the float list. n is at most 50.

**Dry run:** `prices = ['0.1', '0.2']`, `target = '0.3'`.
- Doubles: 3602879701896397/36028797018963968 plus 3602879701896397/18014398509481984 is exactly 10808639105689191/36028797018963968, which is exactly halfway between the doubles 5404319552844595/2^54 (the double for 0.3) and 5404319552844596/2^54; ties go to the even numerator, so it rounds up to 5404319552844596/2^54 (printed `0.30000000000000004`).
- Exact: 1/10 + 2/10 = 3/10, so `exact_sum = '3/10'`.
- `equal`: that double is not the double of 0.3, so False.
- `close`: the difference is about 5.5e-17, far below 1e-9 times 0.3, so True.
- `fsum`: the doubles themselves sum to that same neighbour of 0.3, so `0.30000000000000004` (fsum cannot fix a representation error that is already in the inputs).

**Code:**
```python
import math
import random
import sys
from decimal import Decimal
from fractions import Fraction

random.seed(3101)


def solve(prices, target):
    floats = [float(p) for p in prices]
    s = 0.0
    for v in floats:                                   # plain left-to-right loop, NOT the built-in sum
        s += v
    exact = sum(Fraction(Decimal(p)) for p in prices)  # Decimal(p) is exact for a decimal string
    t = float(target)
    return [repr(s), str(exact), s == t, math.isclose(s, t), repr(math.fsum(floats))]


def brute(prices, target):
    """Independent oracle: parse the decimal strings by hand into integer cents*10^3, no Decimal."""
    def parse(p):
        sign = -1 if p.startswith("-") else 1
        whole, _, frac = p.lstrip("-").partition(".")
        return sign * Fraction(int(whole + frac), 10 ** len(frac))
    exact = sum(parse(p) for p in prices)
    s = 0.0
    for p in prices:
        s = s + float(p)
    # fsum returns the correctly rounded sum of the DOUBLES, so compare with the exact sum of those doubles
    fs = float(sum(Fraction(float(p)) for p in prices))
    t = float(target)
    close = abs(s - t) <= 1e-9 * max(abs(s), abs(t))
    return [repr(s), str(exact), s == t, close, repr(fs)]


# dry run on the first example: show the doubles that are really stored
print("0.1 is stored as", Fraction(0.1))
print("0.2 is stored as", Fraction(0.2))
print("0.3 is stored as", Fraction(0.3))
print("0.1 + 0.2 =", repr(0.1 + 0.2), "| as a fraction:", Fraction(0.1 + 0.2), "| equals 0.3's double?", 0.1 + 0.2 == 0.3)

examples = [
    (["0.1", "0.2"], "0.3", ["0.30000000000000004", "3/10", False, True, "0.30000000000000004"]),
    (["0.1"] * 10, "1", ["0.9999999999999999", "1", False, True, "1.0"]),
    (["0.25", "0.5"], "0.75", ["0.75", "3/4", True, True, "0.75"]),
    (["19.99", "5.01", "-0.5"], "24.5", ["24.5", "49/2", True, True, "24.5"]),
]
for pr, tg, want in examples:
    got = solve(pr, tg)
    assert got == want == brute(pr, tg), (pr, got)
    print(len(pr), "prices ->", got)


def dec(rng):
    k = rng.randint(0, 3)
    v = rng.randint(-5000, 5000)
    q = abs(v)
    return ("-" if v < 0 else "") + (str(q // 10 ** k) + ("." + str(q % 10 ** k).zfill(k) if k else ""))


rng = random.Random(31)
for _ in range(2000):
    pr = [dec(rng) for _ in range(rng.randint(1, 50))]
    tg = rng.choice([dec(rng), str(sum(Fraction(Decimal(p)) for p in pr).limit_denominator(1000))])
    if "/" in tg:
        tg = str(float(Fraction(tg)))
    assert solve(pr, tg) == brute(pr, tg), (pr, tg)
print("2000 seeded random cases match the hand-parsed Fraction oracle")

# the claims, as observed on THIS interpreter
print("python", sys.version.split()[0])
loop10 = 0.0
for v in [0.1] * 10:
    loop10 += v
print("loop  [0.1]*10 :", repr(loop10))
print("sum() [0.1]*10 :", repr(sum([0.1] * 10)))
print("fsum  [0.1]*10 :", repr(math.fsum([0.1] * 10)))
print("isclose(1e-12, 0.0)                  :", math.isclose(1e-12, 0.0))
print("isclose(1e-12, 0.0, abs_tol=1e-9)    :", math.isclose(1e-12, 0.0, abs_tol=1e-9))
print("isclose(0.1 + 0.2, 0.3)              :", math.isclose(0.1 + 0.2, 0.3))
print("Decimal('0.1') + Decimal('0.2')      :", Decimal("0.1") + Decimal("0.2"), Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print("Decimal(0.1) (from the float)        :", Decimal(0.1))
print("cents as ints: 10 + 20 == 30         :", 10 + 20 == 30)
# a loop that really drifts and where sum() and fsum differ from the loop
xs = [0.1] * 1000
loop = 0.0
for v in xs:
    loop += v
print("1000 x 0.1: loop", repr(loop), "| sum", repr(sum(xs)), "| fsum", repr(math.fsum(xs)))
assert sum([0.1] * 10) == 1.0 and loop != 100.0 and math.fsum(xs) == 100.0

# edge cases
assert solve(["0"], "0") == ["0.0", "0", True, True, "0.0"]
assert solve(["-0.5", "0.5"], "0") == ["0.0", "0", True, True, "0.0"]     # isclose(0.0, 0.0) is True: identical values
assert solve(["0.001"], "0")[2:4] == [False, False]                        # near zero, isclose without abs_tol says no
assert solve(["1.000"], "1")[1] == "1"
print("edge asserts ok")
```

**Output (my run):**
```
0.1 is stored as 3602879701896397/36028797018963968
0.2 is stored as 3602879701896397/18014398509481984
0.3 is stored as 5404319552844595/18014398509481984
0.1 + 0.2 = 0.30000000000000004 | as a fraction: 1351079888211149/4503599627370496 | equals 0.3's double? False
2 prices -> ['0.30000000000000004', '3/10', False, True, '0.30000000000000004']
10 prices -> ['0.9999999999999999', '1', False, True, '1.0']
2 prices -> ['0.75', '3/4', True, True, '0.75']
3 prices -> ['24.5', '49/2', True, True, '24.5']
2000 seeded random cases match the hand-parsed Fraction oracle
python 3.13.17
loop  [0.1]*10 : 0.9999999999999999
sum() [0.1]*10 : 1.0
fsum  [0.1]*10 : 1.0
isclose(1e-12, 0.0)                  : False
isclose(1e-12, 0.0, abs_tol=1e-9)    : True
isclose(0.1 + 0.2, 0.3)              : True
Decimal('0.1') + Decimal('0.2')      : 0.3 True
Decimal(0.1) (from the float)        : 0.1000000000000000055511151231257827021181583404541015625
cents as ints: 10 + 20 == 30         : True
1000 x 0.1: loop 99.9999999999986 | sum 100.0 | fsum 100.0
edge asserts ok
```

**Edge cases:**
- One price `'0'` and target `'0'`: everything agrees (`'0.0'`, `'0'`, True, True, `'0.0'`).
- Values that cancel (`-0.5`, `0.5`): sum `0.0`; `isclose(0.0, 0.0)` is True because identical values short-circuit.
- Near zero (`0.001` against `0`): `==` False and `isclose` False without `abs_tol`.
- Target given as `'1'` while the float sum is `0.9999999999999999`: `==` False, `isclose` True.
- `-0.0` can appear from float arithmetic and compares equal to `0.0`.

**Follow-ups:**
- *Round-half-even?* `round(0.5)` is 0, `round(2.5)` is 2, and `round(2.675, 2)` is `2.67` because the double is below 2.675; use `Decimal` with a rounding mode if the business rule says half-up.
- *Why not always `Decimal`?* It is slower and sticky: mixing `Decimal` and `float` in arithmetic raises `TypeError`.
- *How do you compare floats in a test?* `math.isclose(a, b, rel_tol=..., abs_tol=...)`, choosing both tolerances from the problem.

**Common mistakes:**
- Comparing computed floats with `==`.
- `math.isclose(x, 0.0)` with no `abs_tol`.
- Building `Decimal` from a float instead of a string.
- Assuming `sum()` and `fsum` always differ (on 3.13 they agree here) or that they never do (on older versions they can).
- Believing `fsum` fixes input representation error; it only removes the summation error.

### Q32 ⭐⭐ 🟡 The classic biased shuffle, measured exactly. `n` is an integer with 1 <= n <= 6. The buggy shuffle starts from `a = [0, 1, ..., n - 1]` and for i = 0, 1, ..., n - 1 picks j from the WHOLE range 0..n-1 and swaps `a[i]` with `a[j]`. Run it on every possible sequence of n choices and return `[sequences, distinct, min_count, max_count, most_likely, least_likely]`: the number of sequences (n^n), the number of different permutations produced, the smallest and largest number of sequences leading to one particular permutation, and, as lists, the lexicographically smallest permutation that has the largest count and the lexicographically smallest permutation that has the smallest count. Explain why this can never be uniform for n >= 3: the n^n equally likely sequences would have to split evenly into n! permutations, but n - 1 divides n! and not n^n (n - 1 and n share no factor and n - 1 >= 2). Show the n = 3 table, then contrast it with the correct loop in Q11. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive enumeration of the swap tree on small inputs. Example: n=1 -> [1, 1, 1, 1, [0], [0]]; n=2 -> [4, 2, 2, 2, [0, 1], [0, 1]]; n=3 -> [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]; n=4 -> [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Exact enumeration of a random process. Treat the shuffle as a function of its random choices, run it on all of them, and count how often each permutation appears.

**Say this first (1 line):** "The buggy loop makes n choices each from n options, so there are n^n equally likely sequences; for n >= 3, n! does not divide n^n, so the permutations cannot be equally likely, and I can show the exact counts."

**Brute force:** Recursive enumeration of the swap tree: at step `i` try every `j` in `0..n-1`, swap, recurse; count the leaf permutations. That is the oracle (`brute` in the code), n^n leaves.

**Optimal:** There is no faster way to get exact counts than going through the n^n sequences (n <= 6, so at most 46,656). The loop version is `itertools.product(range(n), repeat=n)` and applies the swaps. The real "optimal" is the idea:
- Buggy shuffle: `for i in range(n): j = random in 0..n-1; swap(a[i], a[j])`. Sequences: n^n.
- Correct shuffle (Q11): `for i from n-1 down to 1: j = random in 0..i; swap`. Sequences: n * (n-1) * ... * 2 = n!, each permutation exactly once.
- Why the bug cannot be fixed by luck: if all n! permutations had the same count, then n! would divide n^n. For n >= 3, the number n - 1 is at least 2, divides n! (it is one of its factors), and shares no factor with n (consecutive integers are coprime), so it cannot divide n^n. Check: n^n mod (n - 1) = 1 for every n (printed for n = 3..200 in the run).
- For n = 1 and 2 the argument does not apply (1 and 4 sequences, 1 and 2 permutations) and the shuffle happens to be uniform.
- Table for n = 3 (from the run): `[0,1,2]`, `[2,0,1]`, `[2,1,0]` each appear 4 times, and `[0,2,1]`, `[1,0,2]`, `[1,2,0]` each 5 times, out of 27. A fair shuffle would give 4.5 each, which is impossible in whole sequences. The correct loop gives each of the six permutations exactly once in 6 sequences.
- The bias grows with n: the most likely permutation is 1.25 times, 1.875, 2.94 and 4.97 times as likely as the least likely one for n = 3, 4, 5, 6.

**Complexity:** O(n^n * n) time for the enumeration (every sequence replays n swaps), O(n!) space for the counter. Fine for n <= 6. Each shuffle itself is O(n); the correct shuffle is O(n) time and in-place.

**Dry run:** `n = 3`, start `[0,1,2]`; the choice sequence is `(j0, j1, j2)`.
- `(0, 0, 0)`: i=0 swaps a[0] with itself, `[0,1,2]`; i=1 swaps a[1] with a[0], `[1,0,2]`; i=2 swaps a[2] with a[0], `[2,0,1]`.
- `(0, 1, 2)`: all three swaps are with themselves, so `[0,1,2]`. Three other sequences also end on the identity: `(0,2,1)`, `(1,0,2)`, `(2,1,0)`. That is 4 hits for `[0,1,2]`.
- Five sequences end on `[0,2,1]`: `(0,1,1)`, `(0,2,2)`, `(1,0,1)`, `(1,2,0)`, `(2,0,0)`. Also 5 for `[1,0,2]` and `[1,2,0]`; 4 for `[2,0,1]` and `[2,1,0]`.
- Most hits is 5 (smallest permutation with 5: `[0,2,1]`), fewest is 4 (smallest with 4: `[0,1,2]`). Result `[27, 6, 4, 5, [0,2,1], [0,1,2]]`.

**Code:**
```python
import itertools
import math
import random
from collections import Counter

random.seed(3201)


def solve(n):
    """Run the buggy shuffle on every one of the n^n choice sequences (j in 0..n-1 for each i)."""
    cnt = Counter()
    for js in itertools.product(range(n), repeat=n):
        a = list(range(n))
        for i, j in enumerate(js):
            a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    hi, lo = max(cnt.values()), min(cnt.values())
    return [n ** n, len(cnt), lo, hi,
            list(min(p for p, c in cnt.items() if c == hi)),
            list(min(p for p, c in cnt.items() if c == lo))], cnt


def brute(n):
    """Oracle: recursive enumeration of the swap tree."""
    cnt = Counter()

    def rec(a, i):
        if i == n:
            cnt[tuple(a)] += 1
            return
        for j in range(n):
            b = a[:]
            b[i], b[j] = b[j], b[i]
            rec(b, i + 1)
    rec(list(range(n)), 0)
    hi, lo = max(cnt.values()), min(cnt.values())
    return [sum(cnt.values()), len(cnt), lo, hi,
            list(sorted(p for p in cnt if cnt[p] == hi)[0]),
            list(sorted(p for p in cnt if cnt[p] == lo)[0])]


def correct(n):
    """Fisher-Yates: i from n-1 down to 1, j in 0..i. Exactly n! sequences."""
    cnt = Counter()
    for js in itertools.product(*[range(i + 1) for i in range(n - 1, 0, -1)]):
        a = list(range(n))
        for i, j in zip(range(n - 1, 0, -1), js):
            a[i], a[j] = a[j], a[i]
        cnt[tuple(a)] += 1
    return cnt


for n, want in [(1, [1, 1, 1, 1, [0], [0]]), (2, [4, 2, 2, 2, [0, 1], [0, 1]]),
                (3, [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]), (4, [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]])]:
    got, _ = solve(n)
    assert got == want == brute(n), (n, got)
    print("n =", n, "->", got)

# the n = 3 table: all 27 sequences, then the counts per permutation next to the correct shuffle
res3, cnt3 = solve(3)
print("\nn = 3, buggy shuffle (j from the whole range), 27 sequences:")
fy3 = correct(3)
print("perm        buggy count   buggy prob   correct count (6 sequences)")
for p in sorted(cnt3):
    print(f"{str(list(p)):<11} {cnt3[p]:>11}   {cnt3[p]:>2}/27        {fy3[p]:>5}")
print("sum", sum(cnt3.values()), "| correct sum", sum(fy3.values()), "| ideal 27/6 =", 27 / 6)

# bias grows: statistics for n = 1..6 (6^6 = 46656 sequences is the largest enumeration)
print("\n n   n^n   n!  distinct  min  max   max/min")
for n in range(1, 7):
    r, c = solve(n)
    assert r == brute(n)
    assert r[1] == math.factorial(n)                        # every permutation is reachable, just not evenly
    assert (r[2] == r[3]) == (n <= 2)                       # uniform only for n <= 2
    assert sum(c.values()) == n ** n
    fy = correct(n)
    assert len(fy) == math.factorial(n) and set(fy.values()) == {1}   # correct: every permutation exactly once
    print(f"{n:>2} {n ** n:>5} {math.factorial(n):>4} {r[1]:>8} {r[2]:>4} {r[3]:>4}   {r[3] / r[2]:.3f}")

# the divisibility argument, checked for n = 3..200: n^n is never divisible by n!, because n-1 | n! but gcd(n-1, n) = 1
for n in range(3, 201):
    assert math.factorial(n) % (n - 1) == 0 and math.gcd(n - 1, n) == 1 and n - 1 >= 2
    assert (n ** n) % (n - 1) == 1 and (n ** n) % math.factorial(n) != 0
print("n = 3..200: n^n mod (n-1) = 1 and n! does not divide n^n")
print("n = 1, 2: n^n / n! =", 1 / 1, 4 / 2, "(integers, so uniform is possible and happens)")

# seeded sampling is only a sanity picture, the exact table above is the proof
rng = random.Random(7)
s = Counter()
for _ in range(60000):
    a = [0, 1, 2]
    for i in range(3):
        j = rng.randrange(3)
        a[i], a[j] = a[j], a[i]
    s[tuple(a)] += 1
print("60000 seeded samples (picture only):", {tuple(p): s[p] for p in sorted(s)})

# random cross-check of solve against the recursive oracle (n small; all n in 1..5, each repeated seeded)
for _ in range(60):
    n = random.randint(1, 5)
    assert solve(n)[0] == brute(n)
print("60 seeded checks: loop enumeration equals recursive enumeration")
assert solve(1)[0] == [1, 1, 1, 1, [0], [0]]
print("edge asserts ok")
```

**Output (my run):**
```
n = 1 -> [1, 1, 1, 1, [0], [0]]
n = 2 -> [4, 2, 2, 2, [0, 1], [0, 1]]
n = 3 -> [27, 6, 4, 5, [0, 2, 1], [0, 1, 2]]
n = 4 -> [256, 24, 8, 15, [1, 0, 3, 2], [3, 0, 1, 2]]

n = 3, buggy shuffle (j from the whole range), 27 sequences:
perm        buggy count   buggy prob   correct count (6 sequences)
[0, 1, 2]             4    4/27            1
[0, 2, 1]             5    5/27            1
[1, 0, 2]             5    5/27            1
[1, 2, 0]             5    5/27            1
[2, 0, 1]             4    4/27            1
[2, 1, 0]             4    4/27            1
sum 27 | correct sum 6 | ideal 27/6 = 4.5

 n   n^n   n!  distinct  min  max   max/min
 1     1    1        1    1    1   1.000
 2     4    2        2    2    2   1.000
 3    27    6        6    4    5   1.250
 4   256   24       24    8   15   1.875
 5  3125  120      120   16   47   2.938
 6 46656  720      720   32  159   4.969
n = 3..200: n^n mod (n-1) = 1 and n! does not divide n^n
n = 1, 2: n^n / n! = 1.0 2.0 (integers, so uniform is possible and happens)
60000 seeded samples (picture only): {(0, 1, 2): 8894, (0, 2, 1): 11165, (1, 0, 2): 11080, (1, 2, 0): 11199, (2, 0, 1): 8867, (2, 1, 0): 8795}
60 seeded checks: loop enumeration equals recursive enumeration
edge asserts ok
```

**Edge cases:**
- `n = 1`: one sequence, one permutation, uniform.
- `n = 2`: 4 sequences, 2 permutations, 2 each: the only uniform case besides n = 1.
- `n = 3`: the smallest non-uniform case; all 6 permutations still occur, so "reachable" is not the same as "uniform".
- All permutations are always reachable for n <= 6 (`distinct == n!` in the table).

**Follow-ups:**
- *Is there a fixed version that keeps `j` in `0..n-1`?* Not without rejection tricks. Just shrink the range (`0..i`) as Fisher-Yates does.
- *Why was `random.shuffle` correct?* It uses the backward loop with `randbelow(i + 1)`.
- *Can you detect this bias by sampling?* Only roughly (the 60,000 seeded draws in the run show 5/27 against 4/27 for n = 3 as a picture); the exact count above is the proof.

**Common mistakes:**
- Picking `j` from the whole array on every step.
- Thinking "all permutations are reachable" means "uniform".
- Testing fairness by eyeballing a few samples.
- Forgetting that this is an `n^n` versus `n!` counting argument, not a statement about the random number generator.

### Q33 ⭐⭐ 🟡 Reservoir sampling of k items (Algorithm R), checked exactly. `stream` is a list of n items (1 <= n <= 7 integers) and 1 <= k <= n. Keep a reservoir list of the first k items. For the i-th item (i = k+1..n, counting from 1) take the next number d from `draws` (`draws[i - k - 1]`, with 0 <= d <= i - 1) and, if d < k, put the i-th item into reservoir slot d. Return `[reservoir, inclusion, sequences, subsets, min_subset, max_subset]`: `reservoir` is the final list of VALUES for the given `draws` (n - k numbers); `sequences` is the number of possible draw sequences; `inclusion[t]` is the number of those sequences in which the item at position t (0-indexed) ends up in the reservoir; `subsets` is the number of different k-element sets of positions that occur at the end, and `min_subset` and `max_subset` are the smallest and largest number of sequences ending in one particular such set. Use these numbers to show every item is kept with probability k / n and every k-subset is equally likely, and give the proof by induction on the stream length. State the O(k) memory and why n need not be known in advance. In the answer include a dry run on the first example and a seeded random cross-check of your solution against recursive enumeration of all draw sequences on small inputs. Example: stream=[10, 20, 30, 40], k=2, draws=[1, 3] -> [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]; stream=[7, 8], k=2, draws=[] -> [[7, 8], [1, 1], 1, 1, 1, 1]; stream=[5, 6, 7], k=1, draws=[0, 2] -> [[6], [2, 2, 2], 6, 3, 2, 2].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Streaming sample with a fixed-size reservoir (Algorithm R). Fill the reservoir with the first k, then give item i a k/i chance to enter and kick out a random current member.

**Say this first (1 line):** "Keep the first k; for item i draw d in 0..i-1 and if d < k put item i in slot d; by induction every item ends up kept with probability k/n, and I can confirm it exactly by counting all draw sequences."

**Brute force:** Store the whole stream, then choose k of the n items at random (for example shuffle and take k). O(n) memory and n must be known (or the stream must end). The oracle here enumerates all draw sequences recursively.

**Optimal:**
- Reservoir of k slots. For the i-th item (i = k+1..n, counted from 1) draw d uniformly in `0..i-1`.
- If `d < k`: write item i into slot d. Else drop item i. The new item enters with probability k/i, and it evicts the item in slot d, which is uniform among the k current members.
- Proof by induction on the stream length i. Claim: after i items every k-subset of the first i items is equally likely (probability 1 / C(i, k)). Base i = k: the one subset. Step: take a fixed k-subset T of the first i items.
  - If item i is in T: the previous reservoir must be `T minus {i}` plus one other item x among the first i-1 items (i - k choices of x), and then d must hit exactly x's slot (probability 1/i). Probability: (i - k) * (1 / C(i-1, k)) * (1/i).
  - If item i is not in T: the previous reservoir must be T, and d >= k (probability (i - k)/i): (1 / C(i-1, k)) * (i - k)/i.
  - Both cases give (i - k) / (i * C(i-1, k)). Since C(i, k) = i * C(i-1, k) / (i - k), that equals 1 / C(i, k). So every k-subset is equally likely, and each item is in C(i-1, k-1) / C(i, k) = k/i of them.
- Memory O(k). n need not be known: after any prefix the reservoir is already a uniform sample of that prefix; you can stop at any time.
- Exact check (run): for n = 4, k = 2 there are 3 * 4 = 12 sequences; each item is kept in 6 of them (12 * 2 / 4), each of the 6 pairs arises 2 times. For all n <= 7 and all k <= n the same two facts hold (asserted).

**Complexity:** Time O(n) with one random draw per item after the first k; space O(k) (plus the output). The verification here is O(n!/k!) and is only for small n.

**Dry run:** `stream = [10, 20, 30, 40]`, `k = 2`, `draws = [1, 3]`.
- Start reservoir `[10, 20]`.
- Item 3 (value 30): draw 1 in `0..2`; 1 < 2, so slot 1 gets 30: `[10, 30]`.
- Item 4 (value 40): draw 3 in `0..3`; 3 >= 2, so ignore: `[10, 30]`.
- Enumeration: 12 draw sequences (3 * 4); inclusion `[6, 6, 6, 6]`; the 6 possible pairs each occur twice. Result `[[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]`.

**Code:**
```python
import itertools
import math
import random
from collections import Counter

random.seed(3301)


def run(stream, k, draws):
    """Algorithm R with fixed draws. Slots hold positions so we can count, values are read at the end."""
    n = len(stream)
    slots = list(range(k))                       # slot s holds the position of an item
    for i, d in zip(range(k + 1, n + 1), draws):  # i = 1-based index of the new item, d in 0..i-1
        if d < k:
            slots[d] = i - 1
    return slots


def solve(stream, k, draws):
    n = len(stream)
    reservoir = [stream[p] for p in run(stream, k, draws)]
    inclusion = [0] * n
    subsets = Counter()
    seqs = 0
    for ds in itertools.product(*[range(i) for i in range(k + 1, n + 1)]):   # ALL draw sequences
        slots = run(stream, k, ds)
        seqs += 1
        subsets[frozenset(slots)] += 1
        for p in slots:
            inclusion[p] += 1
    return [reservoir, inclusion, seqs, len(subsets), min(subsets.values()), max(subsets.values())]


def brute(stream, k, draws):
    n = len(stream)
    res = list(stream[:k])
    for idx, d in enumerate(draws):
        if d < k:
            res[d] = stream[k + idx]
    acc = []

    def rec(i, r):                               # recursion over the item number, tries every d in 0..i-1
        if i > n:
            acc.append(tuple(r))
            return
        for d in range(i):
            r2 = list(r)
            if d < k:
                r2[d] = i - 1
            rec(i + 1, r2)
    rec(k + 1, list(range(k)))
    cnt = [sum(p in r for r in acc) for p in range(n)]
    subs = Counter(frozenset(r) for r in acc)
    return [res, cnt, len(acc), len(subs), min(subs.values()), max(subs.values())]


# dry run on the first example: stream [10, 20, 30, 40], k = 2, draws [1, 3]
stream, k, draws = [10, 20, 30, 40], 2, [1, 3]
res = list(stream[:k])
print("start reservoir", res)
for i, d in zip(range(k + 1, len(stream) + 1), draws):
    item = stream[i - 1]
    if d < k:
        res[d] = item
    print(f"item {i} = {item}, draw d = {d} (0..{i - 1}): {'d < k, slot ' + str(d) + ' <- ' + str(item) if d < k else 'd >= k, ignore'} -> {res}")

for st, kk, dr, want in [([10, 20, 30, 40], 2, [1, 3], [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]),
                         ([7, 8], 2, [], [[7, 8], [1, 1], 1, 1, 1, 1]),
                         ([5, 6, 7], 1, [0, 2], [[6], [2, 2, 2], 6, 3, 2, 2])]:
    got = solve(st, kk, dr)
    assert got == want == brute(st, kk, dr), (st, kk, got)
    print(st, "k =", kk, "draws", dr, "->", got)

# exact uniformity for EVERY n <= 7 and k <= n: inclusion = k * seqs / n, all C(n,k) subsets, each seqs / C(n,k) times
print("\n n k  sequences  inclusion per item        subsets  per subset")
for n in range(1, 8):
    for kk in range(1, n + 1):
        r = solve(list(range(n)), kk, [0] * (n - kk))
        seqs = r[2]
        assert seqs == math.factorial(n) // math.factorial(kk)          # prod_{i=k+1..n} i
        assert set(r[1]) == {kk * seqs // n} and kk * seqs % n == 0      # every item kept k/n of the time
        assert r[3] == math.comb(n, kk) and r[4] == r[5] == seqs // math.comb(n, kk)
        if n in (5, 7) or (n == 4 and kk in (1, 2)):
            print(f"{n:>2} {kk} {seqs:>10}  {str(r[1][:1]) + ' x ' + str(n):<22}  {r[3]:>5}  {r[4]:>6}")
print("all n <= 7, all k <= n: each item is held in k/n of the sequences, all C(n,k) subsets occur equally often")

# seeded random cross-check against the recursive enumeration
for _ in range(300):
    n = random.randint(1, 6)
    kk = random.randint(1, n)
    st = [random.randint(0, 9) for _ in range(n)]
    dr = [random.randint(0, i - 1) for i in range(kk + 1, n + 1)]
    assert solve(st, kk, dr) == brute(st, kk, dr)
print("300 seeded random cases match the recursive enumeration")

# edge cases
assert solve([4], 1, [])[:3] == [[4], [1], 1]                 # n = 1
assert solve([1, 2, 3], 3, [])[0] == [1, 2, 3]                # k = n: no draws, nothing is replaced
assert solve([1, 2, 3], 1, [0, 0])[0] == [3]                  # d = 0 each time replaces slot 0
print("edge asserts ok")
```

**Output (my run):**
```
start reservoir [10, 20]
item 3 = 30, draw d = 1 (0..2): d < k, slot 1 <- 30 -> [10, 30]
item 4 = 40, draw d = 3 (0..3): d >= k, ignore -> [10, 30]
[10, 20, 30, 40] k = 2 draws [1, 3] -> [[10, 30], [6, 6, 6, 6], 12, 6, 2, 2]
[7, 8] k = 2 draws [] -> [[7, 8], [1, 1], 1, 1, 1, 1]
[5, 6, 7] k = 1 draws [0, 2] -> [[6], [2, 2, 2], 6, 3, 2, 2]

 n k  sequences  inclusion per item        subsets  per subset
 4 1         24  [6] x 4                     4       6
 4 2         12  [6] x 4                     6       2
 5 1        120  [24] x 5                    5      24
 5 2         60  [24] x 5                   10       6
 5 3         20  [12] x 5                   10       2
 5 4          5  [4] x 5                     5       1
 5 5          1  [1] x 5                     1       1
 7 1       5040  [720] x 7                   7     720
 7 2       2520  [720] x 7                  21     120
 7 3        840  [360] x 7                  35      24
 7 4        210  [120] x 7                  35       6
 7 5         42  [30] x 7                   21       2
 7 6          7  [6] x 7                     7       1
 7 7          1  [1] x 7                     1       1
all n <= 7, all k <= n: each item is held in k/n of the sequences, all C(n,k) subsets occur equally often
300 seeded random cases match the recursive enumeration
edge asserts ok
```

**Edge cases:**
- k = n: there are no draws; the reservoir is the whole stream (1 sequence).
- n = 1 (so k = 1): nothing to draw.
- k = 1 is the classic "pick one uniformly" (item i replaces with probability 1/i; Q35 uses it for indices).
- Draw 0 each time with k = 1 keeps the last item, a legal outcome of probability 1 / n!.
- Duplicate values in the stream are fine: the counts are over positions, not values.

**Follow-ups:**
- *Weighted items?* Algorithm A-Res assigns key `u ** (1 / w)` to each item and keeps the k largest (editor knowledge; not tested here).
- *Faster for huge streams?* Algorithm L skips ahead by a geometric jump, so it draws about k * log(n / k) random numbers instead of n (editor knowledge).
- *Why not "keep with probability k/n" with a first pass for n?* That needs two passes or a known n, and it gives a sample of random size.

**Common mistakes:**
- Drawing `d` in `0..k-1` instead of `0..i-1` (then the last items are over-represented).
- Off-by-one on `i` (counting from 0 instead of 1).
- Replacing slot `i % k` or always the oldest: that is a sliding window, not a uniform sample.
- Using `random.randint(0, i)` (inclusive) with `i` already 1-based.

### Q34 ⭐⭐ 🟡 Rejection sampling: a uniform random integer from a smaller generator. You have `rand_m()` that returns integers uniformly in 1..m and want `rand_t()` uniform in 1..t, where 2 <= m <= 10 and 2 <= t <= m * m. One round reads two values a, b from the generator, forms x = m * (a - 1) + (b - 1) (uniform over 0..m*m-1), and accepts when x < (m*m // t) * t, returning `x % t + 1`; otherwise it rejects x and starts a new round (both values are consumed either way). `stream` is a list of generator values in 1..m (up to 200, possibly odd length; an unpaired last value is unused). Return `[outputs, consumed, counts, expected]`: `outputs` is the list of results produced by the successive full rounds of `stream` (rejected rounds produce nothing); `consumed` is the number of stream values read (2 per round); `counts[v - 1]` is the number of the m * m equally likely pairs (a, b) that produce the result v (all equal, which proves uniformity); and `expected` is the exact expected number of generator calls per output as a reduced fraction string, e.g. '50/21' for m = 5, t = 7 (each round uses 2 calls and succeeds with probability q, so the expected calls are 2 / q). Explain why (a + b) % t is NOT uniform (show the counts for m = 5, t = 7) and why you must reject rather than wrap the leftover values. In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating all m * m pairs and a truncated geometric series for the expectation on small inputs. Example: m=5, t=7, stream=[1, 1, 5, 5, 4, 3, 2, 2] -> [[1, 4, 7], 8, [3, 3, 3, 3, 3, 3, 3], '50/21']; m=7, t=10, stream=[1, 1, 3, 4, 7, 7] -> [[1, 8], 6, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], '49/20']; m=2, t=4, stream=[1, 2, 2, 2, 1] -> [[2, 4], 4, [1, 1, 1, 1], '2'].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Rejection sampling. Build a uniform number over a range that is a multiple of the target, throw away the leftover tail, take a remainder. Retrying (not wrapping) is what keeps it exactly uniform.

**Say this first (1 line):** "Two calls give a uniform x in 0..m*m-1; I accept only x below the largest multiple of t, reduce mod t, and retry otherwise, so every output has exactly the same number of pairs behind it."

**Brute force:** Compute the output distribution by enumerating all m * m pairs `(a, b)`, accept the same ones, and count per result (the oracle, which is also how the answer's `counts` are obtained). For the expected number of calls, sum the truncated series `sum_r (2r) * q * (1 - q)^(r-1)`.

**Optimal:**
- Round: read a, b in 1..m; `x = m * (a - 1) + (b - 1)` is uniform over 0..m*m-1 (a base-m two-digit number).
- Let `lim = (m*m // t) * t`. Accept if `x < lim`, output `x % t + 1`; else reject and start a new round. Each of the t residues has exactly `lim / t = m*m // t` accepted x values behind it, so the output is exactly uniform.
- Success probability per round `q = lim / m^2`. Rounds until success are geometric with mean 1/q, each costing 2 calls, so expected calls are `2 / q = 2 * m^2 / lim`. For m = 5, t = 7: lim = 21, q = 21/25, expected 50/21 = 2.38 calls.
- `q > 1/2` always (`lim >= m^2 / 2` because `floor(y) >= y / 2` for y >= 1, and t <= m^2), so the expected cost is below 4 calls; the run finds the worst over all m in 2..10, t in 2..m^2 is 162/41 = 3.95.
- Why not `(a + b) % t`: the sum of two uniform values is not uniform (sums 2..10 have triangular weights): for m = 5, t = 7 the 25 pairs fall as `[4, 3, 3, 3, 3, 4, 5]` over results 1..7.
- Why not wrap the leftovers (`x % t + 1` without rejecting): 25 = 3 * 7 + 4, so results 1..4 get 4 pairs and results 5..7 only 3: `[4, 4, 4, 4, 3, 3, 3]`. The leftover 4 values would favour the small results. You must reject them.
- Stream handling: only full rounds are read; an unpaired last value is unused and not counted in `consumed`.

**Complexity:** Expected O(1) rounds (below 2 rounds, below 4 calls); worst case unbounded (a run of rejections), but the chance of r consecutive rejections is `(1 - q)^r`, below `2^-r`. Space O(1). The verification table costs O(m^2).

**Dry run:** `m = 5, t = 7`, stream `[1,1,5,5,4,3,2,2]`, `lim = 21`.
- Pair (1,1): x = 0, accepted, 0 % 7 + 1 = 1.
- Pair (5,5): x = 24 >= 21, rejected.
- Pair (4,3): x = 5*3 + 2 = 17, accepted, 17 % 7 + 1 = 4.
- Pair (2,2): x = 5*1 + 1 = 6, accepted, 6 % 7 + 1 = 7.
- `outputs = [1, 4, 7]`, `consumed = 8`, `counts = [3,3,3,3,3,3,3]` (21 accepted pairs / 7), `expected = '50/21'`.

**Code:**
```python
import random
from collections import Counter
from fractions import Fraction

random.seed(3401)


def solve(m, t, stream):
    lim = (m * m // t) * t                       # largest multiple of t that fits in 0..m*m-1 (exclusive bound)
    outputs, consumed = [], 0
    for k in range(0, len(stream) - 1, 2):       # full rounds only: an unpaired last value is unused
        a, b = stream[k], stream[k + 1]
        consumed += 2
        x = m * (a - 1) + (b - 1)                # uniform over 0..m*m-1 when a, b are uniform in 1..m
        if x < lim:
            outputs.append(x % t + 1)
    counts = [0] * t
    for a in range(1, m + 1):                    # exact: push every one of the m*m equally likely pairs through
        for b in range(1, m + 1):
            x = m * (a - 1) + (b - 1)
            if x < lim:
                counts[x % t] += 1
    return [outputs, consumed, counts, str(Fraction(2 * m * m, lim))]   # 2 / q with q = lim / m^2


def brute(m, t, stream):
    pairs = list(zip(stream[0::2], stream[1::2]))
    out = []
    for a, b in pairs:
        x = (a - 1) * m + b - 1
        if x < t * (m * m // t):
            out.append(x % t + 1)
    cnt = Counter(((a - 1) * m + b - 1) % t
                  for a in range(1, m + 1) for b in range(1, m + 1) if (a - 1) * m + b - 1 < t * (m * m // t))
    q = Fraction(t * (m * m // t), m * m)
    # expectation as a truncated geometric series: sum over rounds r of (2r calls) * P(first success at round r)
    series = sum(Fraction(2 * r) * q * (1 - q) ** (r - 1) for r in range(1, 400))
    exact = 2 / q
    assert exact - series < Fraction(1, 10 ** 6) and series <= exact
    return [out, 2 * len(pairs), [cnt[i] for i in range(t)], str(exact)]


# dry run on the first example: m = 5, t = 7, stream [1,1,5,5,4,3,2,2]
m, t = 5, 7
lim = (m * m // t) * t
print(f"m*m = {m * m}, t = {t}, accept x < {lim} (= {m * m // t} * {t}), reject x in {lim}..{m * m - 1}")
stream = [1, 1, 5, 5, 4, 3, 2, 2]
for k in range(0, len(stream), 2):
    a, b = stream[k], stream[k + 1]
    x = m * (a - 1) + (b - 1)
    verdict = f"accept, output {x % t + 1}" if x < lim else "reject (x >= 21)"
    print(f"pair ({a},{b}): x = {m}*{a - 1} + {b - 1} = {x} -> {verdict}")

for mm, tt, st, want in [(5, 7, [1, 1, 5, 5, 4, 3, 2, 2], [[1, 4, 7], 8, [3, 3, 3, 3, 3, 3, 3], "50/21"]),
                         (7, 10, [1, 1, 3, 4, 7, 7], [[1, 8], 6, [4] * 10, "49/20"]),
                         (2, 4, [1, 2, 2, 2, 1], [[2, 4], 4, [1, 1, 1, 1], "2"])]:
    got = solve(mm, tt, st)
    assert got == want == brute(mm, tt, st), (mm, tt, got)
    print(mm, tt, st, "->", got)

# why NOT (a + b) % t, and why not "wrap" x % t without rejecting: exact counts over all 25 pairs
print("\nm = 5, t = 7, all 25 pairs:")
wrongsum = Counter((a + b) % 7 + 1 for a in range(1, 6) for b in range(1, 6))
wrap = Counter((5 * (a - 1) + b - 1) % 7 + 1 for a in range(1, 6) for b in range(1, 6))
print("(a + b) % 7 + 1      :", [wrongsum[v] for v in range(1, 8)], "(sums 2..10 have triangular weights)")
print("x % 7 + 1, no reject :", [wrap[v] for v in range(1, 8)], "(values 1..4 get 4 pairs, 5..7 get 3: leftover 21..24 wrapped)")
assert len(set(wrongsum.values())) > 1 and len(set(wrap.values())) > 1

# exact uniformity and expected cost for EVERY m in 2..10, t in 2..m*m
worst = Fraction(0)
for mm in range(2, 11):
    for tt in range(2, mm * mm + 1):
        r = solve(mm, tt, [])
        lim = (mm * mm // tt) * tt
        assert len(set(r[2])) == 1 and r[2][0] == mm * mm // tt and sum(r[2]) == lim
        assert lim > mm * mm - tt and lim >= tt                     # q = lim / m^2 > 1/2 because floor(y) >= y / 2 for y >= 1
        q = Fraction(lim, mm * mm)
        assert q > Fraction(1, 2) and Fraction(r[3]) == 2 / q
        worst = max(worst, 2 / q)
print(f"all m in 2..10, t in 2..m*m: counts equal, q > 1/2, worst expected calls = {worst} = {float(worst):.3f} (< 4)")

# seeded random cross-check of the stream behaviour and the truncated geometric series
for _ in range(300):
    mm = random.randint(2, 8)
    tt = random.randint(2, mm * mm)
    st = [random.randint(1, mm) for _ in range(random.randint(0, 40))]
    assert solve(mm, tt, st) == brute(mm, tt, st)
print("300 seeded random cases match the pair enumeration and the geometric series")

# edge cases
assert solve(2, 2, [1]) == [[], 0, [2, 2], "2"]        # one unpaired value: nothing read
assert solve(3, 9, [3, 3])[0] == [9] and solve(3, 9, [3, 3])[3] == "2"   # t = m*m: never rejects
assert solve(5, 24, [5, 5, 5, 4])[0] == [24] and solve(5, 24, [5, 5, 5, 4])[3] == "25/12"  # only x = 24 is rejected: q = 24/25
print("edge asserts ok")
```

**Output (my run):**
```
m*m = 25, t = 7, accept x < 21 (= 3 * 7), reject x in 21..24
pair (1,1): x = 5*0 + 0 = 0 -> accept, output 1
pair (5,5): x = 5*4 + 4 = 24 -> reject (x >= 21)
pair (4,3): x = 5*3 + 2 = 17 -> accept, output 4
pair (2,2): x = 5*1 + 1 = 6 -> accept, output 7
5 7 [1, 1, 5, 5, 4, 3, 2, 2] -> [[1, 4, 7], 8, [3, 3, 3, 3, 3, 3, 3], '50/21']
7 10 [1, 1, 3, 4, 7, 7] -> [[1, 8], 6, [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], '49/20']
2 4 [1, 2, 2, 2, 1] -> [[2, 4], 4, [1, 1, 1, 1], '2']

m = 5, t = 7, all 25 pairs:
(a + b) % 7 + 1      : [4, 3, 3, 3, 3, 4, 5] (sums 2..10 have triangular weights)
x % 7 + 1, no reject : [4, 4, 4, 4, 3, 3, 3] (values 1..4 get 4 pairs, 5..7 get 3: leftover 21..24 wrapped)
all m in 2..10, t in 2..m*m: counts equal, q > 1/2, worst expected calls = 162/41 = 3.951 (< 4)
300 seeded random cases match the pair enumeration and the geometric series
edge asserts ok
```

**Edge cases:**
- `t = m*m`: lim = m^2, never rejects (q = 1, expected 2 calls).
- `t = m*m - 1`: only x = m^2 - 1 is rejected, q = (m^2 - 1)/m^2; for m = 5, t = 24 the expected cost is `25/12`.
- `t = 2` with an odd m: still works, rejects the last value (for m = 5 that is x = 24).
- Empty or one-element stream: no round, `outputs = []`, `consumed = 0`.
- `t <= m` can be done with one call plus rejection, but the two-call round is the general rule asked for here.

**Follow-ups:**
- *Fewer wasted calls?* Reuse the rejected tail: `x - lim` is uniform over `0..m*m-lim-1` and can seed the next round (not implemented here).
- *rand7 from rand5 with m = 5, t = 7?* Exactly this; expected 50/21 calls per output.
- *Bias-free alternative with floats?* None that is exact; floats make the problem worse.

**Common mistakes:**
- `(a + b) % t`, or `rand_m() * rand_m() % t` (both non-uniform).
- Wrapping instead of rejecting.
- Forgetting the `- 1` offsets, making x range over 1..m^2 and breaking `x % t`.
- Rejecting only the pair, but not counting its two consumed calls.
- Forgetting that a pair is consumed even on rejection.

### Q35 ⭐⭐ 🟡 Random index of a target value, uniform over its occurrences. `nums` has 1 to 8 integers (duplicates allowed), `target` occurs c >= 1 times in it, and `draws` is a list of c numbers. Scan `nums` from left to right keeping one held index: at the j-th occurrence of `target` (j = 0..c-1) take `draws[j]` (with 0 <= draws[j] <= j) and replace the held index by this occurrence's index exactly when `draws[j] == 0`. Return `[index, counts, sequences]`: `index` is the held index at the end for the given draws; `sequences` is the number of possible draw sequences (c!); and `counts[j]` is the number of those sequences after which the j-th occurrence (in left-to-right order) is held. Use the counts to show each occurrence is chosen with probability 1/c, and explain the O(n) time and O(1) space of this single scan, versus the O(n) memory of building a dictionary from value to a list of indices (which gives O(1) per pick after an O(n) build). In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating all draw sequences on small inputs. Example: nums=[1, 2, 3, 3, 3], target=3, draws=[0, 1, 0] -> [4, [2, 2, 2], 6]; nums=[9, 9], target=9, draws=[0, 1] -> [0, [1, 1], 2]; nums=[4, 5, 6], target=5, draws=[0] -> [1, [1], 1].
**Asked at:** Probability and sampling guides (Wikipedia reservoir-sampling article, techinterview.org probability and sampling posts, a Codemia rand7-from-rand5 page; search snippets only, not opened)

**Pattern:** Reservoir sampling of size 1 over the matching positions. At the j-th occurrence replace the held index with probability 1/(j+1); every occurrence ends up with probability 1/c.

**Say this first (1 line):** "I scan once, count the occurrences of the target, and at the j-th one I take the new index with probability 1/(j+1); that makes every occurrence equally likely, O(n) time and O(1) memory."

**Brute force:** Build a dictionary from value to the list of its indices, then `random.choice` from the target's list. Pick in O(1) after an O(n) build, but O(n) memory. Good when you pick many times.

**Optimal:**
- One left-to-right scan. At the j-th occurrence (0-based) take a draw in `0..j`; if it is 0 the held index becomes this occurrence's index.
- The first occurrence always takes (its draw range is only `0..0`).
- Probability that occurrence j is held at the end: it must be taken (1/(j+1)) and not replaced by any later occurrence i > j (probability 1 - 1/(i+1) = i/(i+1) each). The product telescopes: `1/(j+1) * (j+1)/(j+2) * ... * (c-1)/c = 1/c`.
- Exact count (run): the last occurrence holding it is the last draw of 0; there are c! sequences and each occurrence is held in (c-1)! of them, so `counts` are all equal, for every c from 1 to 8. The telescoping product is also checked as an exact `Fraction` for c up to 11.
- Time O(n) per pick, extra space O(1). The dictionary version uses O(n) memory and O(1) per pick after an O(n) build. If `pick` is called once or the array is huge and read-only, scan; if called many times, build the index.

**Complexity:** Scan O(n) time, O(1) extra space and one random number per occurrence. Dictionary: build O(n), pick O(1), memory O(n). The enumeration for verification is O(c!) and only runs on c <= 8.

**Dry run:** `nums = [1, 2, 3, 3, 3]`, `target = 3`, `draws = [0, 1, 0]`.
- Index 0, 1: not the target.
- Index 2: occurrence 0, draw 0 in `0..0`: held = 2.
- Index 3: occurrence 1, draw 1 in `0..1` is not 0: keep 2.
- Index 4: occurrence 2, draw 0 in `0..2`: held = 4.
- Result held 4. There are 1 * 2 * 3 = 6 draw sequences; the held index is 4 when the last draw is 0 (2 sequences), 3 when the last draw is not 0 and the middle draw is 0 (2 sequences), and 2 when neither is 0 (2 sequences): `counts = [2, 2, 2]`. Output `[4, [2, 2, 2], 6]`.

**Code:**
```python
import itertools
import math
import random

random.seed(3501)


def solve(nums, target, draws):
    """One scan, O(1) extra space for the pick itself. counts/sequences are the exact enumeration."""
    held, j = -1, 0
    for i, v in enumerate(nums):
        if v == target:                       # the j-th occurrence (0-based)
            if draws[j] == 0:                 # draws[j] in 0..j: replace with probability 1/(j+1)
                held = i
            j += 1
    c = j
    occ = [i for i, v in enumerate(nums) if v == target]
    counts = [0] * c
    seqs = 0
    for ds in itertools.product(*[range(jj + 1) for jj in range(c)]):   # ALL c! draw sequences
        last = -1
        for jj, d in enumerate(ds):
            if d == 0:
                last = jj
        counts[last] += 1                      # draws[0] is always 0, so last >= 0
        seqs += 1
    return [held, counts, seqs]


def brute(nums, target, draws):
    occ = [i for i, v in enumerate(nums) if v == target]
    c = len(occ)

    def rec(j, held, acc):                     # recursion over the occurrence number
        if j == c:
            acc[held] = acc.get(held, 0) + 1
            return
        for d in range(j + 1):
            rec(j + 1, occ[j] if d == 0 else held, acc)
    acc = {}
    rec(0, -1, acc)
    last = max(jj for jj, d in enumerate(draws) if d == 0)
    return [occ[last], [acc[o] for o in occ], sum(acc.values())]


# dry run on the first example: nums = [1, 2, 3, 3, 3], target 3, draws [0, 1, 0]
nums, target, draws = [1, 2, 3, 3, 3], 3, [0, 1, 0]
held, j = None, 0
for i, v in enumerate(nums):
    if v != target:
        print(f"index {i} value {v}: not the target, skip")
        continue
    d = draws[j]
    print(f"index {i} value {v}: occurrence {j}, draw {d} in 0..{j}, {'replace' if d == 0 else 'keep'}", end="")
    if d == 0:
        held = i
    print(f" -> held {held}")
    j += 1

for nm, tg, dr, want in [([1, 2, 3, 3, 3], 3, [0, 1, 0], [4, [2, 2, 2], 6]),
                         ([9, 9], 9, [0, 1], [0, [1, 1], 2]),
                         ([4, 5, 6], 5, [0], [1, [1], 1])]:
    got = solve(nm, tg, dr)
    assert got == want == brute(nm, tg, dr), (nm, got)
    print(nm, tg, dr, "->", got)

# exact uniformity for every number of occurrences c = 1..8: counts all (c-1)!, total c!
print("\n c   sequences  count per occurrence")
for c in range(1, 9):
    r = solve([7] * c, 7, [0] * c)
    assert r[2] == math.factorial(c) and set(r[1]) == {math.factorial(c - 1)} and len(r[1]) == c
    print(f"{c:>2} {r[2]:>11}  {r[1][0]:>6} x {c}")

# the probability argument as exact fractions: P(j-th held) = 1/(j+1) * prod_{i>j} (1 - 1/(i+1)) = 1/c
from fractions import Fraction
for c in range(1, 12):
    for jj in range(c):
        p = Fraction(1, jj + 1)
        for i in range(jj + 1, c):
            p *= 1 - Fraction(1, i + 1)
        assert p == Fraction(1, c)
print("telescoping product equals 1/c for c = 1..11, every j")

# seeded random cross-check against enumeration of all draw sequences
for _ in range(300):
    nm = [random.randint(1, 3) for _ in range(random.randint(1, 8))]
    tg = random.choice(nm)
    c = nm.count(tg)
    dr = [random.randint(0, jj) for jj in range(c)]
    assert solve(nm, tg, dr) == brute(nm, tg, dr)
    assert nm[solve(nm, tg, dr)[0]] == tg
print("300 seeded random cases match the recursive enumeration; the held index always holds the target")

# the dictionary alternative: O(n) build, O(1) per pick, O(n) memory
def build(nums):
    pos = {}
    for i, v in enumerate(nums):
        pos.setdefault(v, []).append(i)
    return pos
pos = build([1, 2, 3, 3, 3])
assert pos[3] == [2, 3, 4] and pos[3][2 % 3] in (2, 3, 4)
print("dict of positions:", pos)

# edge cases
assert solve([5], 5, [0]) == [0, [1], 1]                       # single occurrence: first draw is always 0
assert solve([3, 3, 3, 3], 3, [0, 0, 0, 0])[0] == 3            # all zeros: always replace, last wins
assert solve([3, 3, 3, 3], 3, [0, 1, 2, 3])[0] == 0            # only the forced first draw is 0: first stays
print("edge asserts ok")
```

**Output (my run):**
```
index 0 value 1: not the target, skip
index 1 value 2: not the target, skip
index 2 value 3: occurrence 0, draw 0 in 0..0, replace -> held 2
index 3 value 3: occurrence 1, draw 1 in 0..1, keep -> held 2
index 4 value 3: occurrence 2, draw 0 in 0..2, replace -> held 4
[1, 2, 3, 3, 3] 3 [0, 1, 0] -> [4, [2, 2, 2], 6]
[9, 9] 9 [0, 1] -> [0, [1, 1], 2]
[4, 5, 6] 5 [0] -> [1, [1], 1]

 c   sequences  count per occurrence
 1           1       1 x 1
 2           2       1 x 2
 3           6       2 x 3
 4          24       6 x 4
 5         120      24 x 5
 6         720     120 x 6
 7        5040     720 x 7
 8       40320    5040 x 8
telescoping product equals 1/c for c = 1..11, every j
300 seeded random cases match the recursive enumeration; the held index always holds the target
dict of positions: {1: [0], 2: [1], 3: [2, 3, 4]}
edge asserts ok
```

**Edge cases:**
- Single occurrence: the draw is always 0, the held index is that occurrence.
- Target at every position: all of `nums` are candidates; draws up to `n - 1`.
- Target adjacent to itself or at the ends: positions do not matter, only the order of occurrences.
- Draw sequence with only the forced first 0: the first occurrence stays.
- The problem guarantees the target occurs at least once; with zero occurrences there is nothing to pick (raise or return -1 in real code).

**Follow-ups:**
- *Many picks?* Build the dict once (`defaultdict(list)`), then `random.choice(pos[target])`.
- *Stream where nothing can be stored?* This scan is exactly size-1 reservoir sampling (Q33 with k = 1).
- *Random pick of a whole subarray, or a mutable set?* Part 1 Q35 handles the randomised set.

**Common mistakes:**
- Drawing in `0..n-1` (the array length) instead of `0..j` (occurrences so far).
- Counting every element, not only the matches.
- Keeping probability 1/2 each time (favours the last occurrences).
- Returning the index of the last match by default.

### Q36 ⭐⭐ 🟡 What Python's sort accepts and rejects. `cases` is a list of 1 to 20 lists, each with 0 to 6 values that are integers, floats, booleans, None, strings, lists or tuples of those (no NaN). For every case return `[plain, none_last]`: `plain` is `sorted(case)` and `none_last` is `sorted(case, key=lambda v: (v is None, v))`; either one is the string 'TypeError' when Python raises TypeError. Explain from the results: `<` between an int and a str, or between None and an int, raises TypeError in Python 3 (so a list that mixes such types cannot be sorted, however you write the sort); ints, floats and bools compare with each other; tuples and lists compare element by element and only use `<` on the first position where the two items are not `==` (so `(1, 'a') < (2, None)` works but `(1, 'a') < (1, None)` raises); a list of 0 or 1 items never compares anything and so never raises; and why the key `(v is None, v)` puts None last (False sorts before True) without ever comparing None to a number, but still raises for an int mixed with a str; and why `[None, None]` raises for the plain sort (None < None is a TypeError) but not for the key version (equal tuples are never ordered with `<`). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a hand-written insertion sort using only the < operator on small inputs. Example: cases=[[3, 1, 2], [1, 'a'], [null, 3, 1], [null], [(1, 'a'), (2, null)], [(1, 'a'), (1, null)], [True, 2, 1.5], [null, null]] -> [[[1, 2, 3], [1, 2, 3]], ['TypeError', 'TypeError'], ['TypeError', [1, 3, null]], [[null], [null]], [[(1, 'a'), (2, null)], [(1, 'a'), (2, null)]], ['TypeError', 'TypeError'], [[True, 1.5, 2], [True, 1.5, 2]], ['TypeError', [null, null]]].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13)

**Pattern:** Comparison protocol of `list.sort`. `sort` only ever uses `<`; any pair it compares must support `<`, and a total order must connect every element to every other, so some cross-type comparison is unavoidable in a mixed list.

**Say this first (1 line):** "Python 3 only sorts what `<` can compare: ints, floats and bools mix, but `int < str` and `None < int` raise TypeError, so I clean or key the data first; the key `(v is None, v)` pushes None to the end without ever comparing None with a number."

**Brute force:** Write an insertion sort that uses only `<` and run it on each case, catching `TypeError`. It is the oracle here; insertion sort compares a different set of pairs than Timsort, so the cross-check also shows that, for these inputs, the two agree on which cases raise.

**Optimal:** Call `sorted(case)` and `sorted(case, key=lambda v: (v is None, v))`, each in `try / except TypeError`. What the results teach (all observed on 3.13 in the run):
- `1 < 'a'`: `TypeError: '<' not supported between instances of 'int' and 'str'`. Same for `None < 1`.
- int, float and bool compare freely (`True == 1`, `True < 1.5`).
- Tuples and lists compare element by element: Python finds the first position where the two items are NOT `==`, and only then applies `<` to that position. The run prints this with a loud class: `==` on the first pair, `==` on the second pair (not equal), then one `<`. So `(1, 'a') < (2, None)` works (decided at position 0; `'a'` and `None` are never compared), but `(1, 'a') < (1, None)` raises (first positions equal, then `'a' < None`).
- 0 or 1 items: no comparison happens at all, so never an error, whatever the element is (the run shows an object whose `<` raises, sorted alone without error).
- Mixed kinds in one list (str with a number, or None with a number): the algorithm must relate every element to the rest (otherwise the order of groups would be undefined), so at least one cross-kind `<` must happen and raises. The run checks 3000 seeded lists: every list with two of {str, number, None} raised.
- `[None, None]`: plain `sorted` raises (`None < None` is not defined). With the key, the keys are `(True, None)` and `(True, None)`; tuple comparison finds them equal via `==` and never calls `<` on the None parts, so no error.
- The None-last key: `(False, x)` sorts before `(True, None)` because `False < True` decides at slot 0, so None is never compared with a number. But `[1, 'a']` still raises with the key (slot 1 compares `1` and `'a'`).
- Whether an error shows can depend on the algorithm and the order of the data (which pairs it compares), except in the cases above where every algorithm must hit it. Do not rely on a mixed list "happening to work".

**Complexity:** `sorted` is O(n log n) comparisons (Timsort; O(n) on already-sorted input) with O(n) space. Here n <= 6, so everything is instant. The key function is called once per element.

**Dry run:** the first example's 8 cases.
- `[3, 1, 2]`: both `[1, 2, 3]`.
- `[1, 'a']`: `'a' < 1` raises, both `'TypeError'`.
- `[None, 3, 1]`: plain raises; key: `(True, None)`, `(False, 3)`, `(False, 1)` sort to `[1, 3, None]`.
- `[None]`: nothing to compare; `[None]` both ways.
- `[(1,'a'), (2,None)]`: first slots differ, fine.
- `[(1,'a'), (1,None)]`: `'a'` vs `None` raises, both.
- `[True, 2, 1.5]`: `[True, 1.5, 2]` both.
- `[None, None]`: plain `TypeError`, key `[None, None]`.

**Code:**
```python
import random

random.seed(3601)


def solve(cases):
    out = []
    for c in cases:
        try:
            plain = sorted(c)
        except TypeError:
            plain = "TypeError"
        try:
            none_last = sorted(c, key=lambda v: (v is None, v))
        except TypeError:
            none_last = "TypeError"
        out.append([plain, none_last])
    return out


def ins_sort(c, key=None):
    """Oracle: insertion sort that uses ONLY the < operator (like list.sort does)."""
    k = key or (lambda v: v)
    a = []
    for v in c:
        j = len(a)
        while j > 0 and k(v) < k(a[j - 1]):
            j -= 1
        a.insert(j, v)
    return a


def brute(cases):
    out = []
    for c in cases:
        row = []
        for key in (None, lambda v: (v is None, v)):
            try:
                row.append(ins_sort(c, key))
            except TypeError:
                row.append("TypeError")
        out.append(row)
    return out


cases = [[3, 1, 2], [1, "a"], [None, 3, 1], [None], [(1, "a"), (2, None)], [(1, "a"), (1, None)], [True, 2, 1.5], [None, None]]
want = [[[1, 2, 3], [1, 2, 3]], ["TypeError", "TypeError"], ["TypeError", [1, 3, None]], [[None], [None]],
        [[(1, "a"), (2, None)], [(1, "a"), (2, None)]], ["TypeError", "TypeError"], [[True, 1.5, 2], [True, 1.5, 2]],
        ["TypeError", [None, None]]]
got = solve(cases)
assert got == want == brute(cases)
for c, g in zip(cases, got):
    print(f"{str(c):<28} plain={g[0]!s:<22} none_last={g[1]}")

# the exact messages (3.13 wording is what you see here)
for expr in ("1 < 'a'", "None < 1", "None < None", "(1, 'a') < (1, None)", "(1, 'a') < (2, None)", "[1, 'a'] < [1, 2]"):
    try:
        print(f"{expr:<22} ->", eval(expr))
    except TypeError as e:
        print(f"{expr:<22} -> TypeError: {e}")
print("1 == 1.0 == True:", 1 == 1.0 == True, "| True < 1.5:", True < 1.5, "| 2 > True:", 2 > True)

# tuple/list comparison uses == to find the first differing position, then < only there
class Loud:
    def __init__(self, n): self.n = n
    def __eq__(self, o): print(f"   == {self.n},{o.n}"); return self.n == o.n
    def __lt__(self, o): print(f"   <  {self.n},{o.n}"); return self.n < o.n
print("(Loud(1), Loud(5)) < (Loud(1), Loud(9)):")
print("  result", (Loud(1), Loud(5)) < (Loud(1), Loud(9)))

# 0 or 1 items never compare anything
class Boom:
    def __lt__(self, o): raise AssertionError("compared")
assert sorted([]) == [] and sorted([Boom()]) and True
print("sorted([]) and sorted([Boom()]) made no comparison")

# claim: any list with a str and a number (2+ items) raises in plain sort, whatever the order; None with a number too
rng = random.Random(36)
pool = [1, 2, 1.5, True, "a", "b", None]
for _ in range(3000):
    lst = [rng.choice(pool) for _ in range(rng.randint(0, 6))]
    has_str = any(isinstance(v, str) for v in lst)
    has_num = any(isinstance(v, (int, float)) for v in lst)
    has_none = any(v is None for v in lst)
    kinds = has_str + has_num + has_none
    try:
        sorted(lst)
        raised = False
    except TypeError:
        raised = True
    if kinds >= 2:
        assert raised, lst           # a total order must connect the groups, so some cross-type '<' happens
    assert (len(lst) >= 2 and has_none and len([v for v in lst if v is None]) == len(lst)) <= raised
print("3000 seeded mixed lists: two kinds among {str, number, None} always raises; an all-None list of 2+ raises")

# the none-last key
assert sorted([3, None, 1, None, 2], key=lambda v: (v is None, v)) == [1, 2, 3, None, None]
assert (False, 1) < (True, None)       # decided by the first slot, so None is never compared with a number

# seeded random cross-check of solve against the insertion-sort oracle
def pick(rng):
    k = rng.randint(0, 3)
    if k == 0: return [rng.choice([None, 1, 2, 3, 1.5, True]) for _ in range(rng.randint(0, 6))]
    if k == 1: return [rng.choice("abc") for _ in range(rng.randint(0, 6))]
    if k == 2: return [rng.choice([(1, "a"), (1, None), (2, None), (1, 2), (2, "b")]) for _ in range(rng.randint(0, 5))]
    return [rng.choice(pool + [(1, "a"), [1, 2]]) for _ in range(rng.randint(0, 5))]
rng = random.Random(3602)
diff = 0
for _ in range(2000):
    cs = [pick(rng) for _ in range(rng.randint(1, 20))]
    s, b = solve(cs), brute(cs)
    for x, y in zip(s, b):
        if x != y:
            diff += 1
print("2000 seeded batches compared with the insertion-sort oracle, differing rows:", diff)
assert diff == 0

# edge cases
assert solve([[]]) == [[[], []]] and solve([[None, None, None]]) == [["TypeError", [None, None, None]]]
assert solve([[(1, None), (1, None)]]) == [[[(1, None), (1, None)], [(1, None), (1, None)]]]   # equal tuples: == only
print("edge asserts ok")
```

**Output (my run):**
```
[3, 1, 2]                    plain=[1, 2, 3]              none_last=[1, 2, 3]
[1, 'a']                     plain=TypeError              none_last=TypeError
[None, 3, 1]                 plain=TypeError              none_last=[1, 3, None]
[None]                       plain=[None]                 none_last=[None]
[(1, 'a'), (2, None)]        plain=[(1, 'a'), (2, None)]  none_last=[(1, 'a'), (2, None)]
[(1, 'a'), (1, None)]        plain=TypeError              none_last=TypeError
[True, 2, 1.5]               plain=[True, 1.5, 2]         none_last=[True, 1.5, 2]
[None, None]                 plain=TypeError              none_last=[None, None]
1 < 'a'                -> TypeError: '<' not supported between instances of 'int' and 'str'
None < 1               -> TypeError: '<' not supported between instances of 'NoneType' and 'int'
None < None            -> TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'
(1, 'a') < (1, None)   -> TypeError: '<' not supported between instances of 'str' and 'NoneType'
(1, 'a') < (2, None)   -> True
[1, 'a'] < [1, 2]      -> TypeError: '<' not supported between instances of 'str' and 'int'
1 == 1.0 == True: True | True < 1.5: True | 2 > True: True
(Loud(1), Loud(5)) < (Loud(1), Loud(9)):
   == 1,1
   == 5,9
   <  5,9
  result True
sorted([]) and sorted([Boom()]) made no comparison
3000 seeded mixed lists: two kinds among {str, number, None} always raises; an all-None list of 2+ raises
2000 seeded batches compared with the insertion-sort oracle, differing rows: 0
edge asserts ok
```

**Edge cases:**
- Empty list: `[]` both ways.
- All the same type: always fine, subject to that type's `<`.
- NaN is excluded by the prompt: `nan < x` is always False, so sort "works" but the result is meaningless.
- Strings compare by code point, not by locale.
- Equal tuples that contain None never raise.

**Follow-ups:**
- *Sort records by a nullable field descending, None last?* `key=lambda v: (v is None, -v if v is not None else 0)` or sort by `(v is None, v)` then handle reverse carefully (`reverse=True` would put None first).
- *Why did Python 3 drop mixed-type ordering?* Python 2 had arbitrary cross-type ordering that hid bugs (editor knowledge).
- *Does `sort` use `==`?* Not for ordering; stability means equal items keep their order, and "equal" means neither is `<` the other.

**Common mistakes:**
- Assuming a mixed list "usually works".
- Believing a single `None` is harmless in a list with other items (it raises as soon as it is compared with a number).
- Using `key=lambda v: v or 0`, which turns real zeros and empty strings into other values.
- Using `reverse=True` with the None-last key (it puts None first).

### Q37 ⭐⭐ 🟡 Counting sort and LSD radix sort. `records` has 1 to 10^5 items [key, tag] with integer keys 0 <= key <= 10^9 and any integer tags. Sort them ascending by key, keeping equal keys in input order, with an LSD (least significant digit first) radix sort in base 10, without `sorted`: for each decimal digit position from the units upward, do one stable counting-sort pass on that digit (count the 10 digit values, turn the counts into prefix sums, place the items by walking the input from the LAST item to the first, decrementing the digit's counter). Stop after the pass for the highest digit of the largest key. Return `[sorted_records, passes]` where `passes` is the number of digit passes (at least 1, equal to the number of decimal digits of the largest key). Explain why each pass must be stable (an unstable pass destroys the order established by the earlier, less significant digits), why walking backwards is what keeps it stable, the time O(passes * (n + 10)) and the extra space O(n), and when counting sort on the key itself beats comparison sorting (a small key range k: O(n + k)). In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted(records, key=lambda r: r[0]) and len(str(max key)) on small inputs. Example: records=[[170, 1], [45, 2], [75, 3], [90, 4], [802, 5], [24, 6], [2, 7], [66, 8]] -> [[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]; records=[[5, 1]] -> [[[5, 1]], 1]; records=[[3, 1], [3, 2], [0, 3], [3, 4]] -> [[[0, 3], [3, 1], [3, 2], [3, 4]], 1].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** Non-comparison sorting. Counting sort places items by digit in O(n + k) with a stable pass; LSD radix sort chains one stable pass per digit from the least significant up.

**Say this first (1 line):** "For each decimal digit from the units up I do a stable counting sort on that digit; stability is what keeps the earlier digits' order, and walking the input backwards while filling from the block ends is what makes the pass stable."

**Brute force:** `sorted(records, key=lambda r: r[0])`: O(n log n) comparisons and already stable. It is the oracle here. The prompt forbids it in the solution, but it is what you should write in real code unless the keys are small integers.

**Optimal:**
- Number of passes: the digits of the largest key (`len(str(max))`, at least 1; the key 0 still needs one pass). Loop with `exp = 1, 10, 100, ...` and stop once `exp > max key`.
- One pass on digit `d = key // exp % 10`:
  - Count: `cnt[d] += 1` for each record (10 counters).
  - Prefix sums: `cnt[d] += cnt[d-1]`, so `cnt[d]` becomes one past the last slot of digit d's block.
  - Place: walk the input from the LAST record to the first; `cnt[d] -= 1; out[cnt[d]] = record`. The last record of a digit group goes to the end of its block, the previous one just before it, and so on, so equal digits keep their input order.
- Why each pass must be stable: when you sort on the hundreds digit, records with the same hundreds digit must stay in the order the tens and units passes gave them. An unstable pass shuffles ties and throws that work away. The run shows a forward walk reversing equal keys (`[3,1],[3,2],[3,3]` becomes `[3,3],[3,2],[3,1]`) and breaking the sort of `[21, 11, 12]` (gives `[12, 11, 21]`).
- The first example: keys `[170, 45, 75, 90, 802, 24, 2, 66]`. After the units pass `[170, 90, 802, 2, 24, 45, 75, 66]`; after tens `[802, 2, 24, 45, 66, 170, 75, 90]`; after hundreds `[2, 24, 45, 66, 75, 90, 170, 802]`. 3 passes.
- Counting sort on the key itself (one pass) wins when the key range k is small: O(n + k) time and O(n + k) space, with no comparisons, against O(n log n). Radix with base b and d digits is O(d * (n + b)); with a 10^9 range and base 10 that is 10 passes.

**Complexity:** O(passes * (n + 10)) time, passes <= 10 here, so O(n) for n up to 10^5. Extra space O(n) for the output array of each pass plus 10 counters. Not in place. Stable overall.

**Dry run:** units pass on the first example. Units digits `[0, 5, 5, 0, 2, 4, 2, 6]`; counts `[2,0,2,0,1,2,1,0,0,0]`; prefix sums `[2,2,4,4,5,7,8,8,8,8]`, so digit 0 fills slots 0-1, digit 2 slot 2-3, digit 4 slot 4, digit 5 slots 5-6, digit 6 slot 7. Walking from the last record: 66 (digit 6) goes to slot 7, 2 to slot 3, 24 to slot 4, 802 to slot 2, 90 to slot 1, 75 to slot 6, 45 to slot 5, 170 to slot 0. Result `[170, 90, 802, 2, 24, 45, 75, 66]`, matching the run. Tens and hundreds passes follow the same way.

**Code:**
```python
import random
import time

random.seed(3701)


def solve(records, trace=None, backwards=True):
    """LSD radix sort, base 10. backwards=False is the BROKEN forward walk, kept only to show why it matters."""
    a = [list(r) for r in records]
    mx = max(r[0] for r in a)
    passes, exp = 0, 1
    while True:
        passes += 1
        cnt = [0] * 10
        for r in a:
            cnt[r[0] // exp % 10] += 1                  # 1. count each digit value
        for d in range(1, 10):
            cnt[d] += cnt[d - 1]                        # 2. prefix sums: cnt[d] = end (exclusive) of digit d's block
        out = [None] * len(a)
        for r in (reversed(a) if backwards else a):     # 3. walk from the LAST item, fill each block from its end
            dg = r[0] // exp % 10
            cnt[dg] -= 1
            out[cnt[dg]] = r
        a = out
        if trace is not None:
            trace.append((exp, [r[0] for r in a]))
        exp *= 10
        if exp > mx:                                    # no digit left above the largest key's top digit
            break
    return [a, passes]


def brute(records):
    return [sorted([list(r) for r in records], key=lambda r: r[0]), len(str(max(r[0] for r in records)))]


# dry run on the first example
recs = [[170, 1], [45, 2], [75, 3], [90, 4], [802, 5], [24, 6], [2, 7], [66, 8]]
tr = []
res = solve(recs, tr)
print("input keys :", [r[0] for r in recs])
for exp, keys in tr:
    print(f"after digit {len(str(exp)) - 1} (10^{len(str(exp)) - 1}):", keys)
print(res)

for rc, want in [(recs, [[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]),
                 ([[5, 1]], [[[5, 1]], 1]),
                 ([[3, 1], [3, 2], [0, 3], [3, 4]], [[[0, 3], [3, 1], [3, 2], [3, 4]], 1])]:
    assert solve(rc) == want == brute(rc), rc
print("all three examples match sorted(key=...) and len(str(max))")

# the counting-sort block of ONE pass, written out for the units digit of the example
digits = [r[0] % 10 for r in recs]
cnt = [0] * 10
for d in digits:
    cnt[d] += 1
print("\nunits digits :", digits)
print("counts       :", cnt)
pre = list(cnt)
for d in range(1, 10):
    pre[d] += pre[d - 1]
print("prefix sums  :", pre, "(digit d fills slots pre[d-1]..pre[d]-1)")

# why backwards: the forward walk puts equal digits in REVERSE input order, so stability is lost
tiny = [[3, 1], [3, 2], [3, 3]]
print("\nbackwards walk:", solve(tiny, backwards=True)[0])
print("forward walk  :", solve(tiny, backwards=False)[0], "(equal keys reversed: NOT stable)")
assert solve(tiny, backwards=False)[0] == [[3, 3], [3, 2], [3, 1]]
# and an unstable pass breaks the radix idea itself: keys that tie on the low digit end up out of order
two = [[21, 0], [11, 1], [12, 2]]
assert solve(two)[0] == [[11, 1], [12, 2], [21, 0]]
print("forward walk on [21, 11, 12]:", [r[0] for r in solve(two, backwards=False)[0]], "| correct:", [r[0] for r in solve(two)[0]])

# passes = digits of the max key, for 0, 9, 10, 99, 100, 10^9
for mx, p in [(0, 1), (9, 1), (10, 2), (99, 2), (100, 3), (10 ** 9, 10)]:
    assert solve([[mx, 0], [0, 1]])[1] == p == len(str(mx))
print("passes for max key 0, 9, 10, 99, 100, 10^9 :", [solve([[m, 0]])[1] for m in (0, 9, 10, 99, 100, 10 ** 9)])

# seeded random cross-check against sorted() and len(str(max))
for _ in range(500):
    n = random.randint(1, 30)
    hi = random.choice([1, 9, 10, 99, 1000, 10 ** 9])
    rc = [[random.randint(0, hi), random.randint(-5, 5)] for _ in range(n)]
    assert solve(rc) == brute(rc)
print("500 seeded random cases match sorted(key=r[0]) (stable) and the pass count")

# maximum size: 10^5 records, keys up to 10^9 -> 10 passes; time is sandbox-only
big = [[random.randint(0, 10 ** 9), i] for i in range(10 ** 5)]
t0 = time.perf_counter()
r = solve(big)
t1 = time.perf_counter()
assert r == brute(big) and r[1] == len(str(max(x[0] for x in big)))
print(f"10^5 records: passes {r[1]}, radix {t1 - t0:.2f}s (sandbox-only timing, not a proof of big-O)")

# edge cases
assert solve([[0, 9]]) == [[[0, 9]], 1] and solve([[7, 1], [7, 2]]) == [[[7, 1], [7, 2]], 1]
assert solve([[10 ** 9, 1], [10 ** 9 - 1, 2]])[0] == [[10 ** 9 - 1, 2], [10 ** 9, 1]]
print("edge asserts ok")
```

**Output (my run):**
```
input keys : [170, 45, 75, 90, 802, 24, 2, 66]
after digit 0 (10^0): [170, 90, 802, 2, 24, 45, 75, 66]
after digit 1 (10^1): [802, 2, 24, 45, 66, 170, 75, 90]
after digit 2 (10^2): [2, 24, 45, 66, 75, 90, 170, 802]
[[[2, 7], [24, 6], [45, 2], [66, 8], [75, 3], [90, 4], [170, 1], [802, 5]], 3]
all three examples match sorted(key=...) and len(str(max))

units digits : [0, 5, 5, 0, 2, 4, 2, 6]
counts       : [2, 0, 2, 0, 1, 2, 1, 0, 0, 0]
prefix sums  : [2, 2, 4, 4, 5, 7, 8, 8, 8, 8] (digit d fills slots pre[d-1]..pre[d]-1)

backwards walk: [[3, 1], [3, 2], [3, 3]]
forward walk  : [[3, 3], [3, 2], [3, 1]] (equal keys reversed: NOT stable)
forward walk on [21, 11, 12]: [12, 11, 21] | correct: [11, 12, 21]
passes for max key 0, 9, 10, 99, 100, 10^9 : [1, 1, 2, 2, 3, 10]
500 seeded random cases match sorted(key=r[0]) (stable) and the pass count
10^5 records: passes 9, radix 0.28s (sandbox-only timing, not a proof of big-O)
edge asserts ok
```

**Edge cases:**
- Single record, or all keys 0: one pass.
- Max key 9, 10, 99, 100, 10^9: 1, 2, 2, 3, 10 passes (asserted).
- Equal keys keep the input tags in order (`[3,1],[3,2],[3,4]`).
- Keys with fewer digits than the max (2 versus 802): their missing high digits are 0 and they sort first.
- Negative keys are out of range here; they would need an offset or a separate sign pass.

**Follow-ups:**
- *Base 256 or 2^16?* Fewer passes, bigger counter array: choose the base so that `n + base` stays small (typically 4 passes for 32-bit keys with base 256).
- *Is radix always faster than `sorted`?* Not in Python: the per-item loop is interpreted while `sorted` runs in C. The run's timing for 10^5 records is sandbox-only and says nothing about big-O. The point is the algorithm and its O(n) bound.
- *Strings of equal length?* Same idea, per character, from the last to the first.
- *MSD radix?* Recursive by buckets from the most significant digit; used for variable-length strings.

**Common mistakes:**
- Walking the input forwards while decrementing counters: equal keys come out reversed.
- Sorting by the most significant digit first with an LSD loop.
- Using an unstable pass (for example `sort` with a bad key).
- Stopping after `max key` digits computed with floats, or counting 0 as 0 digits.
- Forgetting the prefix-sum step (counts alone give no positions).

### Q38 ⭐⭐ 🟡 Heap sort from scratch. `records` has 0 to 5000 items [key, tag] with integer keys; sort ascending by key in place with heap sort using this exact algorithm (a max-heap on the keys, array form: children of i are 2i + 1 and 2i + 2). `sift(root, size)`: while 2 * root + 1 < size: let `ch = 2 * root + 1`; if `ch + 1 < size`, make ONE comparison `a[ch + 1].key > a[ch].key` and if true take `ch += 1`; then make ONE comparison `a[root].key < a[ch].key`: if true swap them and continue from ch, else stop. Build: for s from `n // 2 - 1` down to 0 call sift(s, n). Sort: for end from n - 1 down to 1 swap `a[0]` and `a[end]` and call sift(0, end). Return `[sorted_records, comparisons]` where `comparisons` counts every key comparison made by sift. Explain why the sort is O(n log n) in the worst case with O(1) extra space, why it is NOT stable (give a tiny failing input from this algorithm and the order it produces) and why quicksort usually beats it in practice (cache behaviour). Heap theory (sift up and down, the O(n) build bound) is Part 8 Q28 and is not repeated. In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted() on the keys and a recursive sift with its own comparison counter on small inputs. Example: records=[[3, 1], [1, 2], [2, 3]] -> [[[1, 2], [2, 3], [3, 1]], 3]; records=[[0, 0], [0, 1]] -> [[[0, 1], [0, 0]], 1]; records=[[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]] -> [[[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]], 10]; records=[] -> [[], 0].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)

**Pattern:** In-place selection with a heap. Build a max-heap in the array, then repeatedly swap the maximum to the end of the shrinking heap and sift the new root down.

**Say this first (1 line):** "I heapify the array into a max-heap, then n - 1 times swap the root with the last heap element and sift down within the smaller heap; O(n log n) worst case, O(1) extra space, not stable."

**Brute force:** `sorted(records, key=...)`, or selection sort (find the maximum n times, O(n^2)). The oracle here is `sorted` on the keys plus a recursive sift with its own comparison counter.

**Optimal:**
- Array heap: children of `i` are `2i + 1` and `2i + 2`.
- `sift(root, size)`: while the root has a child, pick the larger child (one comparison if there are two children), then one comparison of the root against it; swap and continue if the root is smaller, otherwise stop. Each level costs at most 2 comparisons and there are at most `floor(log2 size)` levels.
- Build: `sift(s, n)` for `s = n//2 - 1` down to 0. Sort: for `end = n-1` down to 1, swap `a[0]` and `a[end]`, then `sift(0, end)`.
- Worst case O(n log n) because each of about n/2 + n sifts costs O(log n) (the run asserts comparisons <= 2 * (n/2 + n) * floor(log2 n)). The build alone is O(n) (Part 8 Q28 owns that proof). There is no bad input: sorted, reversed, random and all-equal inputs all land near n log n (see the table).
- O(1) extra space: everything happens in the array (the code copies the input only so the caller's list is not changed).
- Not stable: the long-distance swaps in the sort phase jump equal keys over each other. Smallest example from this algorithm: `[[0,0],[0,1]]` becomes `[[0,1],[0,0]]`; `[[1,'a'],[1,'b'],[1,'c']]` becomes `b, c, a`.
- Why quicksort usually wins in practice: quicksort scans memory sequentially (cache friendly), while sift jumps between index `i` and `2i + 1`, far apart in a big array (cache misses). This is the standard explanation (editor knowledge; not measured here, and in Python interpreter overhead hides it).

**Complexity:** Time O(n log n) in every case (comparisons shown in the run: about 1.7 to 1.8 times `n log2 n`, that is 0.84 to 0.91 of the bound `2n log2 n`, for random, sorted and reversed input with n = 1000 and 5000; about 3n for all-equal, which stops each sift after one level). Space O(1) extra. Not stable.

**Dry run:** keys `[5, 4, 3, 2, 1]` (already a max-heap).
- Build: sift(1, 5) compares children 2 and 1 (one comparison, picks 2) and root 4 against 2 (one), no swap; sift(0, 5): children 4, 3 (one), root 5 vs 4 (one), no swap. 4 comparisons.
- `end = 4`: swap to `[1,4,3,2,5]`, sift(0, 4): children 4, 3 (1), 1 < 4 (1) swap, then at index 1 the child 2 (index 3) vs 1: one comparison, swap: `[4,2,3,1,5]`. Comparisons so far 7.
- `end = 3`: swap to `[1,2,3,4,5]`, sift(0, 3) compares children 2, 3 (picks 3) and root 1 against 3 (2 comparisons) and swaps: `[3,2,1,4,5]`; total 9.
- `end = 2`: swap to `[1,2,3,4,5]`, sift(0, 2) has one child: 1 comparison, swap: `[2,1,3,4,5]`; total 10.
- `end = 1`: swap to `[1,2,3,4,5]`; the heap has size 1, nothing to sift; total 10. Matches the example's `10`.

**Code:**
```python
import math
import random

random.seed(3801)


def solve(records):
    """In-place heap sort on a copy; every key comparison in sift is counted."""
    a = [list(r) for r in records]
    n = len(a)
    cmps = 0

    def sift(root, size):
        nonlocal cmps
        while 2 * root + 1 < size:
            ch = 2 * root + 1
            if ch + 1 < size:
                cmps += 1
                if a[ch + 1][0] > a[ch][0]:      # pick the larger child
                    ch += 1
            cmps += 1
            if a[root][0] < a[ch][0]:            # child bigger than the root: swap and keep sinking
                a[root], a[ch] = a[ch], a[root]
                root = ch
            else:
                break

    for s in range(n // 2 - 1, -1, -1):          # build the max-heap
        sift(s, n)
    for end in range(n - 1, 0, -1):              # move the max to the end, shrink the heap
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    return [a, cmps]


def brute(records):
    """Oracle: recursive sift with its own counter."""
    a = [list(r) for r in records]
    n = len(a)
    c = [0]

    def sift(root, size):
        ch = 2 * root + 1
        if ch >= size:
            return
        if ch + 1 < size:
            c[0] += 1
            if a[ch + 1][0] > a[ch][0]:
                ch += 1
        c[0] += 1
        if a[root][0] < a[ch][0]:
            a[root], a[ch] = a[ch], a[root]
            sift(ch, size)
    for s in reversed(range(n // 2)):
        sift(s, n)
    for end in reversed(range(1, n)):
        a[0], a[end] = a[end], a[0]
        sift(0, end)
    assert [r[0] for r in a] == sorted(r[0] for r in records)
    return [a, c[0]]


# dry run on [[5,1],[4,2],[3,3],[2,4],[1,5]] with the array printed after each step (keys only)
a = [[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]]
n = len(a)
print("keys at start         :", [r[0] for r in a], "(already a max-heap)")
tr = []
cm = 0
def sift_t(root, size):
    global cm
    while 2 * root + 1 < size:
        ch = 2 * root + 1
        if ch + 1 < size:
            cm += 1
            if a[ch + 1][0] > a[ch][0]:
                ch += 1
        cm += 1
        if a[root][0] < a[ch][0]:
            a[root], a[ch] = a[ch], a[root]
            root = ch
        else:
            break
for s in range(n // 2 - 1, -1, -1):
    sift_t(s, n)
print("after build           :", [r[0] for r in a], "comparisons so far", cm)
for end in range(n - 1, 0, -1):
    a[0], a[end] = a[end], a[0]
    sift_t(0, end)
    print(f"after end={end} sift     :", [r[0] for r in a], "comparisons so far", cm)

for rc, want in [([[3, 1], [1, 2], [2, 3]], [[[1, 2], [2, 3], [3, 1]], 3]),
                 ([[0, 0], [0, 1]], [[[0, 1], [0, 0]], 1]),
                 ([[5, 1], [4, 2], [3, 3], [2, 4], [1, 5]], [[[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]], 10]),
                 ([], [[], 0])]:
    assert solve(rc) == want == brute(rc), rc
print("all four examples match, including the recursive oracle")

# not stable: the smallest failing input from this algorithm
print("unstable:", solve([[0, 0], [0, 1]])[0], "(tags 0,1 became 1,0)")
print("unstable 3 items:", solve([[1, "a"], [1, "b"], [1, "c"]])[0])

# bound: sift makes at most 2 comparisons per level, so comparisons <= 2 * (n/2 + n) * floor(log2 n); compare with n log2 n
print("\n     n   random   sorted  reversed  all equal   2n*log2(n)")
for n in (10, 100, 1000, 5000):
    rows = []
    for kind in ("random", "sorted", "reversed", "equal"):
        ks = {"random": [random.randint(0, 10 ** 6) for _ in range(n)], "sorted": list(range(n)),
              "reversed": list(range(n, 0, -1)), "equal": [7] * n}[kind]
        cm_ = solve([[k, i] for i, k in enumerate(ks)])[1]
        assert cm_ <= 2 * (n // 2 + n) * max(1, int(math.log2(n)))
        rows.append(cm_)
    print(f"{n:>6} {rows[0]:>8} {rows[1]:>8} {rows[2]:>9} {rows[3]:>10} {2 * n * math.log2(n):>12.0f}")

# seeded random cross-check against sorted() on the keys and the recursive sift counter
for _ in range(500):
    n = random.randint(0, 40)
    rc = [[random.randint(-5, 5), i] for i in range(n)]
    got = solve(rc)
    assert got == brute(rc) and [r[0] for r in got[0]] == sorted(r[0] for r in rc)
    assert sorted(map(tuple, got[0])) == sorted(map(tuple, rc))          # same records, nothing lost
print("500 seeded random cases: sorted keys, same records, same comparison count as the recursive sift")

# edge cases
assert solve([]) == [[], 0] and solve([[4, 4]]) == [[[4, 4]], 0] and solve([[2, 0], [1, 1]])[1] == 1
assert solve([[1, 0], [2, 1]])[0] == [[1, 0], [2, 1]]
print("edge asserts ok")
```

**Output (my run):**
```
keys at start         : [5, 4, 3, 2, 1] (already a max-heap)
after build           : [5, 4, 3, 2, 1] comparisons so far 4
after end=4 sift     : [4, 2, 3, 1, 5] comparisons so far 7
after end=3 sift     : [3, 2, 1, 4, 5] comparisons so far 9
after end=2 sift     : [2, 1, 3, 4, 5] comparisons so far 10
after end=1 sift     : [1, 2, 3, 4, 5] comparisons so far 10
all four examples match, including the recursive oracle
unstable: [[0, 1], [0, 0]] (tags 0,1 became 1,0)
unstable 3 items: [[1, 'b'], [1, 'c'], [1, 'a']]

     n   random   sorted  reversed  all equal   2n*log2(n)
    10       41       41        35         24           66
   100     1036     1081       944        294         1329
  1000    16865    17583     15965       2994        19932
  5000   107625   112126    103227      14994       122877
500 seeded random cases: sorted keys, same records, same comparison count as the recursive sift
edge asserts ok
```

**Edge cases:**
- Empty: `[[], 0]`. One record: no comparisons.
- Two records: `[[2,0],[1,1]]` takes 1 comparison (the root has a single child, so only the root-versus-child comparison).
- All equal keys: no swaps in the sift (`<` is strict), but the end-swaps still reorder tags: unstable.
- Already sorted ascending: still O(n log n); heap sort is not adaptive.
- Duplicates in keys: fine; ties never trigger a swap in `sift` since `a[root] < a[ch]` is strict.

**Follow-ups:**
- *Why use heap sort at all?* Guaranteed O(n log n) with O(1) space; introsort falls back to it when quicksort recursion gets too deep (editor knowledge).
- *Make it stable?* Sort `(key, original_index)` pairs, at the cost of O(n) extra memory.
- *Fewer comparisons?* Bottom-up heapsort sifts to a leaf first then climbs back, saving about half the comparisons (editor knowledge; not implemented).
- *Top-k only?* Use a heap of size k (Part 8).

**Common mistakes:**
- Using a min-heap and then reversing, which needs extra space or a second pass.
- Forgetting `ch + 1 < size` and reading past the heap end (it holds the sorted tail).
- Building with `n // 2` instead of `n // 2 - 1` (harmless but one wasted sift) or starting the build from 0 upward (wrong).
- Calling `sift(0, n)` instead of `sift(0, end)` after the swap.
- Claiming stability.

### Q39 ⭐⭐ 🟡 Largest number from a list. `nums` has 1 to 100 integers with 0 <= value <= 10^9. Arrange them in some order and join their decimal strings into the largest possible number; return it as a string (if every number is 0, return '0', not '000'). Sort the strings with a custom comparison: put `a` before `b` when `a + b > b + a` as strings (e.g. '9' before '34' because '934' > '349'). Python 3 has no `cmp=` argument for `sort`, so use `functools.cmp_to_key`; also show the key-based alternative that repeats each string until it is at least 20 characters long (`s * (20 // len(s) + 1)`) and sorts descending. Explain why plain descending string order is wrong ('3' vs '30'), why this comparison is a valid total preorder (transitive) so that sort is allowed to use it, and the O(n log n) comparisons each costing O(length) time. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trying every permutation (n <= 7) on small inputs. Example: nums=[3, 30, 34, 5, 9] -> '9534330'; nums=[10, 2] -> '210'; nums=[0, 0] -> '0'; nums=[824, 8247] -> '8248247'; nums=[1] -> '1'.
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened) | Python Sorting HOWTO on cmp_to_key (search snippet only)

**Pattern:** Sort with a custom pairwise order. Put `a` before `b` when `a + b > b + a`; this order is a valid total preorder, so a normal sort can use it.

**Say this first (1 line):** "Compare two numbers as strings by which concatenation is bigger, `a+b` against `b+a`; sort with `cmp_to_key`, join, and special-case an all-zero result."

**Brute force:** Try every permutation of the numbers, join each and keep the maximum: O(n! * n). The oracle (n <= 7).

**Optimal:**
- Convert to strings. Sort with `functools.cmp_to_key(cmp)` where `cmp(a, b) = -1 if a + b > b + a, 1 if a + b < b + a, else 0`. Python 3 has no `cmp=` argument for `sort`, so `cmp_to_key` is the bridge (editor knowledge about why it exists; the code shows it works on 3.13).
- Join; if the first character is `'0'` the whole result is zeros, so return `'0'`.
- Key alternative: sort descending with key `s * (20 // len(s) + 1)`. Each number has at most 10 digits, so `a + b` has at most 20 digits; repeating each string to more than 20 characters makes plain string order agree with the concatenation order. The run checks all 65,536 pairs of strings over the digits 0-3 (lengths 1-4): zero strict disagreements. Where `a + b == b + a` (for example `'1'` and `'11'`) the keys differ only in length, so the key still orders the pair, but both orders give the same joined text.
- Why plain descending string order is wrong: `'3'` vs `'30'`: descending string order puts `'30'` before `'3'` (longer string with the same prefix is larger), giving `...303`, but `'330' > '303'`, so `3` must come first. For the example plain descending gives `9534303`, the comparator `9534330`.
- Why the order is valid: sort needs a strict weak order. "a before b iff a+b > b+a" has an equivalence of ties (`a+b == b+a`) and is transitive. Proof sketch: `a+b >= b+a` is the same as comparing `a/(10^len(a) - 1)` with `b/(10^len(b) - 1)` as numbers, a real-number order (editor's derivation); so transitivity follows. The run also checks it exhaustively: all 59,319 triples of strings over {0,1,2} up to length 3 have zero violations of "a >= b and b >= c implies a >= c".
- Cost: O(n log n) comparisons, each O(L) for string length L (at most 20 characters here), so O(n log n * L).

**Complexity:** O(n log n * L) time with L <= 20 (a constant for ints up to 10^9), O(n * L) space. With n <= 100 this is tiny. The key version computes each key once: O(n * L) for keys plus O(n log n) comparisons of 21 to 30 character strings.

**Dry run:** `[3, 30, 34, 5, 9]`.
- `'3'` vs `'30'`: `'330'` > `'303'`, so `3` before `30`.
- `'34'` vs `'3'`: `'343'` > `'334'`, so `34` before `3`; `34` vs `30`: `'3430'` > `'3034'`, `34` first.
- `5` and `9` beat everything starting with 3 (`'53'` > `'35'`), and `9` beats `5`.
- Order `['9', '5', '34', '3', '30']`, joined `9534330`. The repeat keys (`'3' * 21`, `'3030...'`, `'3434...'`, ...) sort the same way.

**Code:**
```python
import functools
import itertools
import random

random.seed(3901)


def cmp(a, b):
    """a before b (negative) when a + b > b + a as strings."""
    if a + b > b + a:
        return -1
    if a + b < b + a:
        return 1
    return 0


def solve(nums):
    strs = sorted(map(str, nums), key=functools.cmp_to_key(cmp))
    r = "".join(strs)
    return "0" if r[0] == "0" else r          # sorted first = the biggest; a leading '0' means everything is 0


def solve_key(nums):
    """Key-based alternative: repeat each string to >= 20 chars (a + b has at most 20 digits), sort descending."""
    strs = sorted(map(str, nums), key=lambda s: s * (20 // len(s) + 1), reverse=True)
    r = "".join(strs)
    return "0" if r[0] == "0" else r


def brute(nums):
    best = max("".join(map(str, p)) for p in itertools.permutations(nums))
    return "0" if best[0] == "0" else best


# dry run on [3, 30, 34, 5, 9]
print("pairs: '3' vs '30':", "330" if "330" > "303" else "303", "wins ('330' > '303'), so 3 goes first")
print("pairs: '34' vs '3':", "343 vs 334 -> 34 first")
print("plain descending strings:", "".join(sorted(map(str, [3, 30, 34, 5, 9]), reverse=True)),
      "| comparator:", solve([3, 30, 34, 5, 9]))
ss = sorted(map(str, [3, 30, 34, 5, 9]), key=functools.cmp_to_key(cmp))
print("order chosen:", ss, "-> joined", "".join(ss))
print("repeat keys :", [(s, s * (20 // len(s) + 1)) for s in map(str, [3, 30, 34, 5, 9])])

for nums, want in [([3, 30, 34, 5, 9], "9534330"), ([10, 2], "210"), ([0, 0], "0"), ([824, 8247], "8248247"), ([1], "1")]:
    got = solve(nums)
    assert got == solve_key(nums) == brute(nums) == want, (nums, got)
    print(nums, "->", repr(got))

# exact check 1: the key trick agrees with the comparator on EVERY pair of digit strings over {0,1,2,3}, length 1..4 (no leading zero)
strs = ["".join(p) for L in range(1, 5) for p in itertools.product("0123", repeat=L) if p[0] != "0" or L == 1]
key = lambda s: s * (20 // len(s) + 1)
bad = ties_split = 0
for a, b in itertools.product(strs, repeat=2):
    c = cmp(a, b)
    k = (key(a) < key(b)) - (key(a) > key(b))       # descending key: bigger key first = negative
    if c == 0:
        ties_split += (k != 0)                      # a + b == b + a, e.g. '1' and '11': the keys differ in LENGTH only
        assert a + b == b + a
    else:
        bad += (c != k)
print(f"pairs checked: {len(strs) ** 2} over {len(strs)} strings; strict disagreements: {bad}; "
      f"tied pairs (a+b == b+a) that the key still orders: {ties_split} (harmless: tied strings join to the same text)")
assert bad == 0

# exact check 2: transitivity of 'a before-or-equal b'  (a+b >= b+a) on all triples of strings over {0,1,2}, length 1..3
small = ["".join(p) for L in range(1, 4) for p in itertools.product("012", repeat=L)]
ge = lambda a, b: a + b >= b + a
viol = 0
for a, b, c in itertools.product(small, repeat=3):
    if ge(a, b) and ge(b, c) and not ge(a, c):
        viol += 1
print(f"triples checked: {len(small) ** 3}, transitivity violations: {viol}")
assert viol == 0
# total: for every pair one of a+b >= b+a, b+a >= a+b holds, trivially; ties (a+b == b+a) are equal-key strings
assert all(ge(a, b) or ge(b, a) for a, b in itertools.product(small, repeat=2))

# seeded random cross-check against all permutations (n <= 7)
for _ in range(400):
    n = random.randint(1, 7)
    nums = [random.choice([0, 1, 2, 3, 10, 30, 34, 99, 100, 824, 8247, 10 ** 9, random.randint(0, 10 ** 9)]) for _ in range(n)]
    got = solve(nums)
    assert got == brute(nums) == solve_key(nums), nums
print("400 seeded random cases match the permutation brute force and the key version")

# maximum size: 100 numbers up to 10^9
big = [random.randint(0, 10 ** 9) for _ in range(100)]
assert solve(big) == solve_key(big) and len(solve(big)) == sum(len(str(x)) for x in big)
print("n = 100 up to 10^9: comparator and key agree, length", len(solve(big)))

# edge cases
assert solve([0]) == "0" and solve([0, 0, 0]) == "0" and solve([10, 0]) == "100" and solve([0, 1]) == "10"
assert solve([121, 12]) == "12121" and solve([12, 121]) == "12121"          # a + b == b + a: a tie, any order
assert solve([10 ** 9, 10 ** 9 - 1]) == "9999999991000000000"
print("edge asserts ok")
```

**Output (my run):**
```
pairs: '3' vs '30': 330 wins ('330' > '303'), so 3 goes first
pairs: '34' vs '3': 343 vs 334 -> 34 first
plain descending strings: 9534303 | comparator: 9534330
order chosen: ['9', '5', '34', '3', '30'] -> joined 9534330
repeat keys : [('3', '333333333333333333333'), ('30', '3030303030303030303030'), ('34', '3434343434343434343434'), ('5', '555555555555555555555'), ('9', '999999999999999999999')]
[3, 30, 34, 5, 9] -> '9534330'
[10, 2] -> '210'
[0, 0] -> '0'
[824, 8247] -> '8248247'
[1] -> '1'
pairs checked: 65536 over 256 strings; strict disagreements: 0; tied pairs (a+b == b+a) that the key still orders: 48 (harmless: tied strings join to the same text)
triples checked: 59319, transitivity violations: 0
400 seeded random cases match the permutation brute force and the key version
n = 100 up to 10^9: comparator and key agree, length 886
edge asserts ok
```

**Edge cases:**
- All zeros (`[0, 0]`): the join would be `'00'`; return `'0'`.
- Zero mixed with others: `[10, 0]` gives `'100'`, `[0, 1]` gives `'10'`.
- Ties: `[121, 12]` and `[12, 121]` both give `'12121'`.
- One number: itself as a string.
- Largest values: `[10**9, 10**9 - 1]` gives `'9999999991000000000'`.

**Follow-ups:**
- *Why not sort numerically descending?* `[824, 8247]` must give `8248247`; numeric order puts 8247 first and gives `8247824`.
- *Why not compare `a + b` as ints?* Same result, but creating ints is slower than comparing strings; strings of equal length compare like numbers.
- *Smallest number instead?* Flip the comparison (and avoid a leading zero).
- *Python 2?* It had `cmp=`; Python 3 requires `cmp_to_key` or a key.

**Common mistakes:**
- Plain descending string sort (`'30'` before `'3'`).
- Returning `'000'` for all zeros.
- Using `sorted(..., cmp=...)` (a TypeError in Python 3).
- A comparator that returns a bool instead of -1/0/1 (the result is inconsistent).
- Mixing up the sign: `-1` must mean "a comes first".

### Q40 ⭐ 🟡 Matrix region sums with point updates (basic level). `matrix` is an m x n list of lists of integers (1 <= m, n <= 100) and `ops` has up to 10^4 operations, each `['update', r, c, v]` (set `matrix[r][c] = v`) or `['sum', r1, c1, r2, c2]` (the sum of the rectangle with corners (r1, c1) and (r2, c2), both included, 0 <= r1 <= r2 < m, 0 <= c1 <= c2 < n). Return one result per operation in order: None for an update, the sum for a sum. Keep a prefix-sum list per ROW: an update rebuilds one row in O(n), a query adds one prefix difference per row in O(r2 - r1 + 1) = O(m). Compare this with the static 2D table of Q5 (O(1) query but O(m * n) per update) and with a 2D Fenwick tree (O(log m * log n) both ways); the Fenwick tree and the segment tree are the standard answer for many updates and queries and belong to Part 14, so only name them here. In the answer include a dry run on the first example and a seeded random cross-check of your solution against recomputing the sum of the rectangle from the current matrix on every query on small inputs. Example: matrix=[[3, 0, 1], [5, 6, 3], [1, 2, 0]], ops=[['sum', 0, 0, 2, 2], ['update', 1, 1, 10], ['sum', 1, 1, 2, 2], ['sum', 0, 0, 1, 1]] -> [21, null, 15, 18]; matrix=[[4]], ops=[['update', 0, 0, -4], ['sum', 0, 0, 0, 0]] -> [null, -4].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Row-wise prefix sums with point updates: trade the O(1) query of a static 2D table for an O(n) update that touches one row only.

**Say this first (1 line):** "One prefix list per row: an update rebuilds a single row in O(n), and a sum adds one prefix difference per row in the rectangle, O(m); a 2D Fenwick tree does both in O(log m * log n) and is Part 14."

**Brute force:** On each query add up all cells of the rectangle (O(m * n), up to 10^4 per query); an update is O(1). With 10^4 operations that can be 10^8 steps. It is the oracle here.

**Optimal:**
- Keep `rows[r]` = `accumulate(matrix[r], initial=0)`, so `rows[r][c]` is the sum of the first c cells and the sum of columns `c1..c2` of row r is `rows[r][c2+1] - rows[r][c1]`.
- `update r c v`: set the cell, rebuild `rows[r]` (O(n)); nothing else changes.
- `sum r1 c1 r2 c2`: add `rows[r][c2+1] - rows[r][c1]` for `r` in `r1..r2` (O(r2 - r1 + 1) <= O(m)).
- Comparison:

| Method | Update | Query | Memory |
|---|---|---|---|
| Recompute from the matrix | O(1) | O(m * n) | O(1) extra |
| Static 2D prefix table (Q5) | O(m * n) | O(1) | O(m * n) |
| Row prefix lists (this answer) | O(n) | O(m) | O(m * n) |
| 2D Fenwick tree (Part 14, named only) | O(log m * log n) | O(log m * log n) | O(m * n) |

- Why the static table's update is O(m*n): changing cell (r, c) changes every table entry at or below row r and right of column c. The run shows a corner update on a 4 x 4 matrix changes all 16 table entries, while the last cell changes 1.
- At the maximum size (100 x 100, 10^4 mixed operations) the run counts about 5.1 * 10^5 row-rebuild steps and about 1.2 * 10^5 query row-differences in total (deterministic counts), against up to 10^4 cell reads per query for the brute force.
- Which to pick: many queries and few updates, the static table; balanced updates and queries on big grids, a Fenwick or segment tree; this row-wise form is the simple middle ground with m, n <= 100.

**Complexity:** Build O(m * n). Update O(n). Query O(m). Total for q operations: O(q * max(m, n)), at most about 10^6 steps here. Space O(m * n) for the matrix plus the same again for the prefix rows.

**Dry run:** `matrix = [[3,0,1],[5,6,3],[1,2,0]]`.
- Row prefixes: `[0,3,3,4]`, `[0,5,11,14]`, `[0,1,3,3]`.
- `sum (0,0)-(2,2)`: row 0 `4 - 0 = 4`, row 1 `14`, row 2 `3`: total 21.
- `update (1,1) = 10`: row 1 becomes `[5,10,3]`, prefixes `[0,5,15,18]`; rows 0 and 2 untouched.
- `sum (1,1)-(2,2)`: row 1 `18 - 5 = 13`, row 2 `3 - 1 = 2`: 15.
- `sum (0,0)-(1,1)`: row 0 `3 - 0 = 3`, row 1 `15 - 0 = 15`: 18. Result `[21, None, 15, 18]`.

**Code:**
```python
import itertools
import random

random.seed(4001)


def solve(matrix, ops, stats=None):
    mat = [list(r) for r in matrix]
    rows = [list(itertools.accumulate(r, initial=0)) for r in mat]   # rows[r][c] = sum of mat[r][:c]
    out = []
    for op in ops:
        if op[0] == "update":
            _, r, c, v = op
            mat[r][c] = v
            rows[r] = list(itertools.accumulate(mat[r], initial=0))  # rebuild ONE row: O(n)
            if stats is not None:
                stats["update_work"] += len(mat[r])
            out.append(None)
        else:
            _, r1, c1, r2, c2 = op
            out.append(sum(rows[r][c2 + 1] - rows[r][c1] for r in range(r1, r2 + 1)))   # one difference per row: O(m)
            if stats is not None:
                stats["query_work"] += r2 - r1 + 1
    return out


def brute(matrix, ops):
    mat = [list(r) for r in matrix]
    out = []
    for op in ops:
        if op[0] == "update":
            mat[op[1]][op[2]] = op[3]
            out.append(None)
        else:
            out.append(sum(mat[i][j] for i in range(op[1], op[3] + 1) for j in range(op[2], op[4] + 1)))
    return out


# dry run on the first example
matrix = [[3, 0, 1], [5, 6, 3], [1, 2, 0]]
rows = [list(itertools.accumulate(r, initial=0)) for r in matrix]
print("row prefix lists:", rows)
print("sum (0,0)-(2,2): row0", rows[0][3] - rows[0][0], "+ row1", rows[1][3] - rows[1][0], "+ row2", rows[2][3] - rows[2][0], "= 21")
matrix[1][1] = 10
rows[1] = list(itertools.accumulate(matrix[1], initial=0))
print("update (1,1)=10 rebuilds only row 1:", rows[1], "(other rows untouched)")
print("sum (1,1)-(2,2): row1", rows[1][3] - rows[1][1], "+ row2", rows[2][3] - rows[2][1], "= 15")
print("sum (0,0)-(1,1): row0", rows[0][2] - rows[0][0], "+ row1", rows[1][2] - rows[1][0], "= 18")

for mt, ops, want in [([[3, 0, 1], [5, 6, 3], [1, 2, 0]], [["sum", 0, 0, 2, 2], ["update", 1, 1, 10], ["sum", 1, 1, 2, 2], ["sum", 0, 0, 1, 1]], [21, None, 15, 18]),
                      ([[4]], [["update", 0, 0, -4], ["sum", 0, 0, 0, 0]], [None, -4])]:
    got = solve(mt, ops)
    assert got == want == brute(mt, ops)
    print(got)


# the static 2D prefix table (Q5 style): O(1) query, but one update changes up to m*n cells
def static_table(mat):
    m, n = len(mat), len(mat[0])
    p = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            p[i + 1][j + 1] = mat[i][j] + p[i][j + 1] + p[i + 1][j] - p[i][j]
    return p

m = [[1] * 4 for _ in range(4)]
p1 = static_table(m)
m[0][0] = 2
p2 = static_table(m)
changed = sum(p1[i][j] != p2[i][j] for i in range(5) for j in range(5))
print("\nstatic table: updating the corner cell (0,0) of a 4x4 matrix changes", changed, "of 16 table cells")
m[3][3] = 2
p3 = static_table(m)
print("updating cell (3,3) changes", sum(p2[i][j] != p3[i][j] for i in range(5) for j in range(5)), "table cell")

# seeded random cross-check against recomputing every rectangle from the current matrix
def rand_case(rng, mmax=6, nmax=6, k=40):
    m_, n_ = rng.randint(1, mmax), rng.randint(1, nmax)
    mt = [[rng.randint(-9, 9) for _ in range(n_)] for _ in range(m_)]
    ops = []
    for _ in range(rng.randint(0, k)):
        if rng.random() < 0.4:
            ops.append(["update", rng.randrange(m_), rng.randrange(n_), rng.randint(-9, 9)])
        else:
            r1 = rng.randrange(m_); r2 = rng.randint(r1, m_ - 1)
            c1 = rng.randrange(n_); c2 = rng.randint(c1, n_ - 1)
            ops.append(["sum", r1, c1, r2, c2])
    return mt, ops
rng = random.Random(40)
for _ in range(500):
    mt, ops = rand_case(rng)
    assert solve(mt, ops) == brute(mt, ops)
print("500 seeded random cases match the recompute-from-matrix oracle")

# maximum size: 100 x 100 matrix, 10^4 ops; count elementary steps (deterministic, unlike wall time)
mt = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(100)] for _ in range(100)]
ops = []
for _ in range(10 ** 4):
    if rng.random() < 0.5:
        ops.append(["update", rng.randrange(100), rng.randrange(100), rng.randint(-10 ** 6, 10 ** 6)])
    else:
        r1 = rng.randrange(100); r2 = rng.randint(r1, 99); c1 = rng.randrange(100); c2 = rng.randint(c1, 99)
        ops.append(["sum", r1, c1, r2, c2])
st = {"update_work": 0, "query_work": 0}
res = solve(mt, ops, st)
assert res == brute(mt, ops)
print("10^4 ops on 100 x 100:", st, "| the brute force would touch up to 10^4 cells per query")

# edge cases
assert solve([[7]], [["sum", 0, 0, 0, 0]]) == [7]
assert solve([[1, 2], [3, 4]], [["sum", 0, 0, 1, 1], ["update", 1, 1, 0], ["sum", 0, 0, 1, 1], ["sum", 1, 0, 1, 0]]) == [10, None, 6, 3]
assert solve([[5]], [["update", 0, 0, 5]]) == [None]
print("edge asserts ok")
```

**Output (my run):**
```
row prefix lists: [[0, 3, 3, 4], [0, 5, 11, 14], [0, 1, 3, 3]]
sum (0,0)-(2,2): row0 4 + row1 14 + row2 3 = 21
update (1,1)=10 rebuilds only row 1: [0, 5, 15, 18] (other rows untouched)
sum (1,1)-(2,2): row1 13 + row2 2 = 15
sum (0,0)-(1,1): row0 3 + row1 15 = 18
[21, None, 15, 18]
[None, -4]

static table: updating the corner cell (0,0) of a 4x4 matrix changes 16 of 16 table cells
updating cell (3,3) changes 1 table cell
500 seeded random cases match the recompute-from-matrix oracle
10^4 ops on 100 x 100: {'update_work': 506200, 'query_work': 124976} | the brute force would touch up to 10^4 cells per query
edge asserts ok
```

**Edge cases:**
- 1 x 1 matrix: update then sum.
- A query that is a single row or single column.
- Updating a cell to the same value: still rebuilds the row (harmless).
- Negative values and large sums: Python ints do not overflow.
- A query before any update, and updates that are never queried.

**Follow-ups:**
- *Can the update be O(1)?* Store the change and only re-sum lazily, or keep a Fenwick tree per row (O(log n) update and O(m log n) query).
- *Fully O(log) both ways?* 2D Fenwick tree or segment tree (Part 14).
- *Immutable matrix?* Use the static table (Q5) with O(1) query.
- *Heavy updates, few queries?* The brute force with O(1) update wins.

**Common mistakes:**
- Rebuilding the whole prefix structure on every update.
- Off-by-one: using `rows[r][c2]` instead of `rows[r][c2 + 1]` (the lists have n + 1 entries).
- Forgetting to update the stored matrix before rebuilding the row.
- Returning 0 instead of `None` for an update.

### Q41 ⭐ 🟡 Hoare partition, one call. `nums` has 2 <= len <= 50 integers (duplicates allowed). Run exactly this partition with pivot `p = nums[0]`: `i = -1; j = len(nums)`; loop: `i += 1` then keep doing `i += 1` while `a[i] < p`; `j -= 1` then keep doing `j -= 1` while `a[j] > p`; if `i >= j` return j; otherwise swap `a[i]` and `a[j]` and repeat. Return `[array_after, j]`. Explain what the result guarantees (every item at positions 0..j is <= p and every item at positions j+1..end is >= p, and 0 <= j < len - 1, so recursing on [0, j] and [j + 1, end] always shrinks), why the pivot is NOT placed in its final position (unlike Lomuto), why the recursion must use j and j + 1 (not j - 1 and j + 1), why choosing the LAST element as the pivot with this exact loop can return j = len - 1 (and recurse forever), and why Hoare's scheme handles many equal keys better than Lomuto (both pointers stop on equal keys, so they meet near the middle). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a version written with while True loops and checking the guarantees on small inputs. Example: nums=[5, 3, 8, 1, 9, 2] -> [[2, 3, 1, 8, 9, 5], 2]; nums=[2, 1] -> [[1, 2], 0]; nums=[1, 2] -> [[1, 2], 0]; nums=[4, 4, 4, 4] -> [[4, 4, 4, 4], 1].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Two pointers walking toward each other (Hoare partition, the original quicksort partition). It applies because we only need "small stuff left, big stuff right", not one exact final spot for the pivot.

**Say this first (1 line):** "Two pointers start outside the array and move inward; each stops on anything that is on the wrong side or equal to the pivot, I swap, and when they cross I return j, so [0..j] is all <= pivot and [j+1..] is all >= pivot."

**Brute force:** Build the answer from a definition: copy the array, then check the contract by scanning (every item at 0..j is <= p, every item after is >= p). There is no simple brute force that reproduces the exact same swaps, so the cross-check is a second implementation (while True loops, pointers moved after a swap) plus the contract check on every array of length 2 to 7 over small values.

**Optimal:**
- `p = a[0]`, `i = -1`, `j = n`. Each round: move i right past items `< p`, move j left past items `> p`.
- If `i >= j`, return j. Otherwise swap `a[i]`, `a[j]` and go on.
- Both pointers stop on items equal to p. That looks wasteful (extra swaps) but it keeps the split balanced.
- Guarantee: everything left of i is <= p, everything right of j is >= p. When they meet or cross, j is the last position of the "<= p" side.
- Why `0 <= j < n - 1` with pivot a[0]: in the first round i stops at index 0 (the pivot is not `< p`), so j is at most n - 1 there. Either they meet at j = 0 (return 0), or we swap, and then j is decremented again before it is returned, so j <= n - 2. The exhaustive run below confirms it. So [0, j] and [j + 1, end] are both non-empty and both shorter than the input.
- Why the pivot is not placed: Hoare only separates the two sides. The pivot may be swapped around and ends somewhere in [0..j] or even on the right (see the first example, the 5 moved to the end). Lomuto puts the pivot at its final index and recurses on both sides excluding it.
- Why recurse on j and j + 1: index j still belongs to the left side and may not be the pivot's final place. Using `j - 1` drops an element that has not been placed: in my run that left 305 of 500 small arrays unsorted.
- Why a last-element pivot can break: with `p = a[-1]` the first i-scan can stop at the last index, then j stops at the same index and the function returns j = n - 1. Recursing on [0, j] is then the full range again: infinite recursion. Example [1, 2].
- Equal keys: with all keys equal both pointers stop at once every round, swap, and meet in the middle (j = 49 for n = 100). Lomuto with `<` sends every equal key to one side and gets n - 1 (quadratic quicksort).

**Complexity:** One call is O(n) time (each pointer only moves inward, so at most n + 1 steps in total) and O(1) extra space. At most n / 2 swaps. A full quicksort with it is O(n log n) on average, O(n^2) on bad pivots, as usual.

**Dry run:** nums = [5, 3, 8, 1, 9, 2], p = 5.
| step | i | j | action |
|---|---|---|---|
| start | -1 | 6 | |
| round 1 | 0 (5 is not < 5) | 5 (2 is not > 5) | i < j, swap -> [2, 3, 8, 1, 9, 5] |
| round 2 | 2 (3 < 5, then 8 stops) | 3 (1 is not > 5) | i < j, swap -> [2, 3, 1, 8, 9, 5] |
| round 3 | 3 (8 stops at once) | 2 (j steps from 3 to 2, where 1 is not > 5) | i = 3 >= j = 2, return 2 |
Result [[2, 3, 1, 8, 9, 5], 2]. Left part [2, 3, 1] all <= 5, right part [8, 9, 5] all >= 5. The pivot 5 ended up in the right part.

**Code:**
```python
import random, itertools
random.seed(41)

# ---- the exact partition from the question (pivot = a[lo], returns the new array and j)
def hoare(nums):
    a = list(nums); p = a[0]; i, j = -1, len(a)
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]

# ---- the examples
assert hoare([5, 3, 8, 1, 9, 2]) == [[2, 3, 1, 8, 9, 5], 2]
assert hoare([2, 1]) == [[1, 2], 0]
assert hoare([1, 2]) == [[1, 2], 0]
assert hoare([4, 4, 4, 4]) == [[4, 4, 4, 4], 1]
print('examples ok:', hoare([5, 3, 8, 1, 9, 2]), hoare([2, 1]), hoare([1, 2]), hoare([4, 4, 4, 4]))

def guarantees(orig, a, j):
    p = orig[0]
    return (sorted(a) == sorted(orig) and 0 <= j < len(a) - 1
            and all(x <= p for x in a[:j + 1]) and all(x >= p for x in a[j + 1:]))

# ---- exhaustive check: every array of length 2..7 over values 0..3 (and 0..4 for length <= 5)
cnt = 0
for n in range(2, 8):
    for t in itertools.product(range(4 if n > 5 else 5), repeat=n):
        a, j = hoare(t)
        assert guarantees(t, a, j), t
        cnt += 1
print('guarantees hold for', cnt, 'arrays (all arrays of length 2..7 over small value sets)')

# ---- seeded random cross-check against the while-True version (same i/j walk, different loop shape)
def hoare_alt(nums):
    a = list(nums); p = a[0]; i, j = 0, len(a) - 1
    while True:
        while a[i] < p: i += 1
        while a[j] > p: j -= 1
        if i >= j: return [a, j]
        a[i], a[j] = a[j], a[i]
        i += 1; j -= 1
for _ in range(2000):
    t = [random.randint(-5, 5) for _ in range(random.randint(2, 50))]
    assert hoare(t) == hoare_alt(t)
    a, j = hoare(t); assert guarantees(t, a, j)
print('2000 random arrays: both loop shapes agree and the guarantees hold')

# ---- recursion on [lo, j] and [j+1, hi] sorts; j-1 / j+1 (Lomuto style) does not
def part_range(a, lo, hi, pivot_index):
    p = a[pivot_index]; i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: return j
        a[i], a[j] = a[j], a[i]
def qs(a, lo, hi, wrong=False, depth=0):
    if depth > 200: raise RecursionError('no progress')
    if lo >= hi: return
    j = part_range(a, lo, hi, lo)
    if wrong: qs(a, lo, j - 1, True, depth + 1); qs(a, j + 1, hi, True, depth + 1)
    else: qs(a, lo, j, False, depth + 1); qs(a, j + 1, hi, False, depth + 1)
for _ in range(500):
    t = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
    a = list(t); qs(a, 0, len(a) - 1); assert a == sorted(t)
bad = 0
for _ in range(500):
    t = [random.randint(0, 9) for _ in range(random.randint(2, 12))]
    a = list(t); qs(a, 0, len(a) - 1, wrong=True); bad += a != sorted(t)
print('recursing on [lo, j] and [j+1, hi]: 500/500 sorted; on [lo, j-1] and [j+1, hi]:', bad, '/ 500 left unsorted')

# ---- last element as pivot with the same loop: j can be len-1, so [lo, j] is the whole range
a = [1, 2]; j = part_range(a, 0, 1, 1)
print('pivot = last element, [1, 2] -> j =', j, '(= len - 1, so recursing on [0, j] never shrinks)')
try:
    b = [1, 2, 3]
    def qs_last(a, lo, hi, depth=0):
        if depth > 50: raise RecursionError('stuck: same range again and again')
        if lo >= hi: return
        j = part_range(a, lo, hi, hi); qs_last(a, lo, j, depth + 1); qs_last(a, j + 1, hi, depth + 1)
    qs_last(b, 0, 2)
except RecursionError as e: print('last-element pivot quicksort:', e)
# count how often the last-element pivot can return len-1 on small arrays
hits = sum(1 for t in itertools.product(range(3), repeat=4) if (lambda a: part_range(a, 0, 3, 3))(list(t)) == 3)
print('last-element pivot returned j = n-1 for', hits, 'of 81 arrays of length 4 over {0,1,2}')

# ---- equal keys: both pointers stop on equal keys, so j lands in the middle; Lomuto (last pivot) would give n-1
for n in (8, 100):
    a, j = hoare([7] * n); print('all equal, n =', n, '-> j =', j, '(middle); Lomuto with all equal puts the pivot at', n - 1)
swaps = []
for n in (8, 100):
    a = [7] * n; p = a[0]; i, j, s = -1, n, 0
    while True:
        i += 1
        while a[i] < p: i += 1
        j -= 1
        while a[j] > p: j -= 1
        if i >= j: break
        a[i], a[j] = a[j], a[i]; s += 1
    swaps.append(s)
print('swaps on all-equal input of size 8 and 100:', swaps, '(useless swaps, but the split is balanced)')

# ---- edge asserts
assert hoare([3, 3]) == [[3, 3], 0]
assert hoare([9, 1]) == [[1, 9], 0]
assert hoare([1, 9, 1]) == [[1, 9, 1], 0]
assert hoare([2, 2, 1]) == [[1, 2, 2], 1]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[2, 3, 1, 8, 9, 5], 2] [[1, 2], 0] [[1, 2], 0] [[4, 4, 4, 4], 1]
guarantees hold for 24380 arrays (all arrays of length 2..7 over small value sets)
2000 random arrays: both loop shapes agree and the guarantees hold
recursing on [lo, j] and [j+1, hi]: 500/500 sorted; on [lo, j-1] and [j+1, hi]: 305 / 500 left unsorted
pivot = last element, [1, 2] -> j = 1 (= len - 1, so recursing on [0, j] never shrinks)
last-element pivot quicksort: stuck: same range again and again
last-element pivot returned j = n-1 for 9 of 81 arrays of length 4 over {0,1,2}
all equal, n = 8 -> j = 3 (middle); Lomuto with all equal puts the pivot at 7
all equal, n = 100 -> j = 49 (middle); Lomuto with all equal puts the pivot at 99
swaps on all-equal input of size 8 and 100: [4, 50] (useless swaps, but the split is balanced)
edge asserts ok
```

**Edge cases:**
- Length 2: [2, 1] gives j = 0, [1, 2] gives j = 0. Both halves have size 1.
- All equal: j in the middle.
- Pivot is the unique maximum at index 0: i stops at the first item, j walks left to 0 and meets it, j = 0 (left side is only the pivot's slot).
- Pivot is the unique minimum: every other item is larger, so j walks all the way left to index 0 and the call returns j = 0.
- Duplicates of the pivot on both sides: they are swapped around but stay on valid sides.

**Follow-ups:**
- Can I pick a random pivot? Yes: swap the random item to a[0] first, then run the same loop. Never use the last element with this exact loop (or switch to the `i = lo, j = hi` do-while form with matching rules).
- Which is faster in practice, Lomuto or Hoare? The usual textbook claim is that Hoare does fewer swaps on random data and handles duplicates better. I did not measure that here.
- Does Hoare quicksort need the pivot to end in place? No, that is why the recursion ranges overlap on j.

**Common mistakes:**
- Recursing on (lo, j - 1) and (j + 1, hi). It loses an element.
- Using the last element as pivot with this loop and getting an infinite recursion.
- Stopping the scans on `<=` / `>=` instead of strict `<` / `>`: the pointers then run off the array on equal keys.
- Expecting the pivot to sit at index j.

---

### Q42 ⭐ 🟡 Three-way partition quicksort versus Lomuto on duplicates. `nums` has 1 <= len <= 2000 integers with many repeats allowed. Return `[sorted_list, lomuto_comparisons, three_way_comparisons]`. `lomuto_comparisons` is the total number of `a[j] < p` tests of the Lomuto quicksort defined in Q16 (last element as pivot). The three-way quicksort partitions a range [lo, hi] around `p = a[hi]` with `lt = lo, i = lo, gt = hi` and `while i <= gt:` ONE comparison of `a[i]` with p: if `a[i] < p` swap `a[lt]` and `a[i]` and do `lt += 1; i += 1`; if `a[i] > p` swap `a[i]` and `a[gt]` and do `gt -= 1`; if equal do `i += 1`. Then it sorts [lo, lt - 1] and [gt + 1, hi] and skips ranges with fewer than 2 items. Both must be iterative (an all-equal input makes the Lomuto recursion about n deep, above CPython's recursion limit for n near 1000 and over). Explain why all-equal input costs n * (n - 1) / 2 comparisons for Lomuto but n for three-way, that this is the Dutch national flag partition, and that the equal block is never touched again. The same partition idea drives quickselect (Part 8 Q36). In the answer include a dry run on the first example and a seeded random cross-check of your solution against recursive versions of both partition schemes on small inputs on small inputs. Example: nums=[2, 2, 2, 2] -> [[2, 2, 2, 2], 6, 4]; nums=[3, 1, 2, 3, 1] -> [[1, 1, 2, 3, 3], 8, 8]; nums=[1, 2, 3, 4, 5] -> [[1, 2, 3, 4, 5], 10, 14].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Quicksort partitioning, and duplicates. Three-way partition is the Dutch national flag idea: one pass splits a range into `< p`, `== p`, `> p`.

**Say this first (1 line):** "Lomuto puts all equal keys on one side so all-equal input costs n(n-1)/2; three-way partition parks every key equal to the pivot in the middle block and never looks at it again, so all-equal input is one pass of n."

**Brute force:** Lomuto quicksort with the last element as pivot (Q16), counting every `a[j] < p` test. It is correct, but with many equal keys the pivot lands at the end of its range every time, so recursion peels one item per level: about n levels deep and n^2 / 2 comparisons. Recursive code would also crash on an all-equal input of around 1000 items (default recursion limit 1000; my run raised RecursionError at 1500).

**Optimal:**
- Keep three pointers on the range [lo, hi] with `p = a[hi]`: `a[lo..lt-1] < p`, `a[lt..i-1] == p`, `a[i..gt] unknown`, `a[gt+1..hi] > p`.
- Look at `a[i]` once: smaller, swap to `lt` and advance both; larger, swap to `gt` and shrink gt (do not advance i, the swapped-in item is unseen); equal, just advance i.
- Stop when `i > gt`. Then sort only [lo, lt-1] and [gt+1, hi]. The block `[lt..gt]` holds the pivot value and is already in its final place.
- Iterative: push the two ranges on a list used as a stack, pop, skip ranges with fewer than 2 items. No recursion, so no recursion-limit problem whatever the input.
- All-equal input: every item is equal, so one pass of n comparisons and both sub-ranges are empty. Lomuto: n - 1, n - 2, ... 1 comparisons = n(n-1)/2 (checked for n = 1, 2, 3, 10, 57, 2000).
- Quickselect (Part 8 Q36) uses the same partition and then recurses into only the side that holds the wanted rank.

**Complexity:**
- Lomuto: O(n log n) on average with distinct keys, O(n^2) when the pivot is an extreme (sorted input, all equal). Space O(n) for the stack in the worst case.
- Three-way: the same on distinct keys; on k distinct values it is O(n log k) with a good pivot. With only a few distinct values it is close to linear (see the run: 6102 comparisons against 205321 for 2000 items from 10 values).
- Honest warning: the three-way scheme with the last element as pivot is NOT immune to sorted input. On 1..n the pivot is the maximum, one pass of n comparisons peels one item, and the total is n(n+1)/2 - 1 (14 for n = 5, higher than Lomuto's 10; asserted in the code). A random or median-of-three pivot fixes that; three-way only fixes duplicates.

**Dry run:** nums = [3, 1, 2, 3, 1], three-way, p = a[4] = 1.
| i | a | lt | gt | action |
|---|---|---|---|---|
| 0 | [3,1,2,3,1] | 0 | 4 | 3 > 1: swap a[0], a[4] -> [1,1,2,3,3], gt = 3 |
| 0 | [1,1,2,3,3] | 0 | 3 | 1 == 1: i = 1 |
| 1 | | 0 | 3 | 1 == 1: i = 2 |
| 2 | | 0 | 3 | 2 > 1: swap a[2], a[3] -> [1,1,3,2,3], gt = 2 |
| 2 | | 0 | 2 | 3 > 1: swap a[2], a[2], gt = 1; now i > gt, stop |
5 comparisons. Equal block = [0..1], so ranges [0..-1] (empty) and [2..4] = [3,2,3] remain. Sorting that range with p = 3 takes 3 more comparisons (3 == p, then 2 < p swaps to the front, then 3 == p) and gives [2,3,3]; the leftover ranges have fewer than 2 items and are skipped. Total 8 comparisons, sorted [1,1,2,3,3]. Lomuto also costs 8 on this input.

**Code:**
```python
import random, itertools, sys
random.seed(42)

# ---- optimal: both quicksorts iterative (explicit stack of ranges), with comparison counters
def lomuto_iter(nums):
    a = list(nums); cmps = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi: continue
        p = a[hi]; i = lo
        for j in range(lo, hi):
            cmps += 1                                  # one test a[j] < p
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]                      # pivot to its final index i
        stack.append((lo, i - 1)); stack.append((i + 1, hi))
    return a, cmps

def three_way_iter(nums):
    a = list(nums); cmps = 0
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if hi - lo < 1: continue                       # fewer than 2 items
        p = a[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            cmps += 1                                  # ONE comparison, three outcomes (<, >, ==)
            if a[i] < p: a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > p: a[i], a[gt] = a[gt], a[i]; gt -= 1
            else: i += 1
        stack.append((lo, lt - 1)); stack.append((gt + 1, hi))   # the block [lt..gt] == p is never touched again
    return a, cmps

def solve(nums):
    s, cl = lomuto_iter(nums); s3, c3 = three_way_iter(nums)
    assert s == s3
    return [s, cl, c3]

# ---- recursive versions, written separately, as the cross-check
def rec_versions(nums):
    c = [0, 0]; a = list(nums); b = list(nums)
    def rl(lo, hi):
        if lo >= hi: return
        p = a[hi]; i = lo
        for j in range(lo, hi):
            c[0] += 1
            if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
        a[i], a[hi] = a[hi], a[i]; rl(lo, i - 1); rl(i + 1, hi)
    def r3(lo, hi):
        if hi - lo < 1: return
        p = b[hi]; lt, i, gt = lo, lo, hi
        while i <= gt:
            c[1] += 1
            if b[i] < p: b[lt], b[i] = b[i], b[lt]; lt += 1; i += 1
            elif b[i] > p: b[i], b[gt] = b[gt], b[i]; gt -= 1
            else: i += 1
        r3(lo, lt - 1); r3(gt + 1, hi)
    rl(0, len(a) - 1); r3(0, len(b) - 1)
    assert a == b == sorted(nums)
    return [a, c[0], c[1]]

# ---- examples
assert solve([2, 2, 2, 2]) == [[2, 2, 2, 2], 6, 4]
assert solve([3, 1, 2, 3, 1]) == [[1, 1, 2, 3, 3], 8, 8]
assert solve([1, 2, 3, 4, 5]) == [[1, 2, 3, 4, 5], 10, 14]
print('examples ok:', solve([2, 2, 2, 2]), solve([3, 1, 2, 3, 1]), solve([1, 2, 3, 4, 5]))

# ---- seeded random cross-check (small value ranges give many repeats)
for _ in range(3000):
    n = random.randint(1, 30); k = random.choice([1, 2, 3, 5, 50])
    t = [random.randint(0, k) for _ in range(n)]
    assert solve(t) == rec_versions(t) and solve(t)[0] == sorted(t)
print('3000 random inputs: iterative == recursive (sorted list and both counters)')

# ---- exact claims, checked
for n in (1, 2, 3, 10, 57, 2000):
    s, cl, c3 = solve([7] * n)
    assert cl == n * (n - 1) // 2 and c3 == (n if n >= 2 else 0)
print('all equal, n = 2000: Lomuto', solve([7] * 2000)[1], '= n(n-1)/2 ; three-way', solve([7] * 2000)[2], '= n')
# sorted input is bad for Lomuto (last element = maximum) and fine-ish for three-way only by luck of the pivot rule
print('sorted 1..2000: Lomuto', solve(list(range(2000)))[1], ' three-way', solve(list(range(2000)))[2])
d = [random.randint(0, 9) for _ in range(2000)]
print('2000 random items from 10 distinct values: Lomuto', solve(d)[1], ' three-way', solve(d)[2])

# ---- why iterative: the recursive Lomuto on all-equal input of size n is about n frames deep
try:
    rec_versions([7] * 1500)
except RecursionError:
    print('recursive version on 1500 equal items: RecursionError (limit', sys.getrecursionlimit(), ')')
print('iterative version on 2000 equal items worked (no recursion at all)')

# ---- edge asserts
assert solve([]) == [[], 0, 0]
assert solve([5]) == [[5], 0, 0]
assert solve([2, 1]) == [[1, 2], 1, 2]
assert solve([1, 1, 1, 2, 2, 2]) [0] == [1, 1, 1, 2, 2, 2]
assert solve([-3, -3, 0, -3])[0] == [-3, -3, -3, 0]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[2, 2, 2, 2], 6, 4] [[1, 1, 2, 3, 3], 8, 8] [[1, 2, 3, 4, 5], 10, 14]
3000 random inputs: iterative == recursive (sorted list and both counters)
all equal, n = 2000: Lomuto 1999000 = n(n-1)/2 ; three-way 2000 = n
sorted 1..2000: Lomuto 1999000  three-way 2000999
2000 random items from 10 distinct values: Lomuto 205321  three-way 6102
recursive version on 1500 equal items: RecursionError (limit 1000 )
iterative version on 2000 equal items worked (no recursion at all)
edge asserts ok
```

**Edge cases:**
- Empty and single item: 0 comparisons for both.
- Two items: Lomuto 1, three-way 2 (the pivot is compared with itself once).
- All equal: 6 vs 4 for four items; n(n-1)/2 vs n in general.
- Already sorted with a last-element pivot: quadratic for both.
- Negative numbers and a mix: nothing special, comparisons only.

**Follow-ups:**
- How do you avoid the sorted-input worst case? Random pivot or median of three; for adversarial input, introsort (fall back to heap sort at depth 2 log n).
- Why does the equal block never get touched again? Everything left of it is smaller and everything right is larger, so those items are in final place.
- Which sort does Python use? Timsort, not quicksort (Q43, Q44).

**Common mistakes:**
- Advancing i after swapping with gt: the swapped-in item has not been examined.
- Looping while `i < gt` instead of `i <= gt` and missing the last item.
- Recursing on [lo, lt] or [gt, hi] and re-sorting the equal block.
- Writing the recursive version and trusting it on sorted or all-equal input of size 1000 and over.
- Claiming three-way is O(n log n) in the worst case with a bad pivot.

---

### Q43 ⭐ 🟡 Adaptive sorting: nearly sorted inputs. `nums` has 0 <= len <= 300 integers. Return `[timsort, insertion, shifts, inversions, merge]`: `timsort` is the number of `<` comparisons CPython's `list.sort` performs on the list (measured by sorting objects whose `__lt__` increments a counter; this is the observed behaviour of CPython 3.13 and the checker accepts exactly that count); `insertion` is the number of comparisons `a[j - 1] > x` made by plain insertion sort (for each i from 1, take x = a[i], and while j > 0 compare a[j - 1] with x and shift while it is greater); `shifts` is the number of element moves that insertion sort makes; `inversions` is the number of pairs i < j with nums[i] > nums[j]; `merge` is the number of comparisons of the top-down merge sort of Q15 on keys = the values. Explain why `shifts == inversions`, why insertion sort costs about n + inversions comparisons (so it is O(n) on nearly sorted data and O(n^2) on reversed data), why merge sort does not adapt, and why Timsort needs only n - 1 comparisons on an already sorted list and on a strictly descending one (it finds one natural run, reversing it if it descends strictly) while it still guarantees O(n log n) on any input. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a separately written counting wrapper class and the O(n^2) inversion count on small inputs. Example: nums=[1, 2, 3, 4, 5] -> [4, 4, 0, 0, 5]; nums=[5, 4, 3, 2, 1] -> [4, 10, 10, 10, 7]; nums=[1, 2, 4, 3, 5, 6] -> [10, 6, 1, 1, 8]; nums=[2, 2, 1, 1] -> [5, 6, 4, 4, 4]; nums=[] -> [0, 0, 0, 0, 0].
**Asked at:** Python Sorting HOWTO (search-result snippets only; the docs.python.org fetch failed with ENOTFOUND, so behaviour was verified by running Python 3.13) | Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Adaptive sorting and inversion counting. The cost of insertion sort is "n plus the number of inversions"; a sort is adaptive if it gets cheaper on input that is already nearly in order.

**Say this first (1 line):** "Every shift in insertion sort removes exactly one inversion, so shifts equal inversions and comparisons are about n plus inversions; merge sort ignores the order; Timsort looks for runs first, so a sorted or strictly descending list costs n - 1 comparisons."

**Brute force:** Count inversions with the double loop (O(n^2)); simulate each algorithm with a counter. The `Timsort` count is not simulated: it is measured by sorting objects whose `__lt__` increments a counter (this is observed CPython 3.13 behaviour, and a plain int list is, from editor knowledge that I did not test, sorted with a faster internal comparison that bypasses `__lt__`, which is why wrapper objects are used).

**Optimal:**
- Insertion sort: for each i take x = a[i] and shift larger items to the right until a smaller or equal one appears. The array keeps a sorted prefix.
- `shifts == inversions`: a shift moves one larger item past x, which fixes exactly one pair (that item, x) that was out of order, and an inversion is only ever fixed by a shift. Sorted at the end means zero inversions left. It was also checked on 3280 small lists.
- Comparisons: each i makes one comparison per shift plus one failed comparison, unless x travels all the way to the front (then the loop ends on `j == 0` with no failed comparison). So comparisons = inversions + (n - 1) - (number of items that become a strict new minimum of the prefix). That is between inversions and inversions + n - 1: O(n) on nearly sorted data, O(n^2) on reversed data (n(n-1)/2).
- Merge sort (Q15 version): it always splits and merges, so it does not adapt: 1180 comparisons for a sorted list of 300 and 1308 for the reversed one, within the same n log n band.
- Timsort: first finds a natural run at the start (the longest non-decreasing stretch, or a strictly descending one, which it reverses in place). A fully sorted or strictly descending list is one run, found with n - 1 comparisons and no merging. Checked for every length 1..299. Ties break it: [2, 2, 1, 1] is not strictly descending, and costs 5. Why strictly: reversing a non-strictly descending run would swap equal items and break stability.
- It still guarantees O(n log n) for any input because short runs are extended by binary insertion sort and runs are merged under balance rules (details in Q44).
- Honest note: adaptive does not mean best everywhere. On my 300-item list with 5 adjacent swaps, Timsort used 541 comparisons while plain insertion sort used 304. Insertion sort is the cheapest when the displacement is tiny. Timsort's promise is "never much worse than n log n, linear on the common easy shapes".

**Complexity:**
- Insertion sort O(n + inversions) time, O(1) space, stable.
- Inversion counting by merge sort O(n log n) (used here only as a check; the brute force O(n^2) is also in the code).
- Top-down merge sort always about n log2 n comparisons, O(n) extra space.
- Timsort O(n) best case (one run), O(n log n) worst case, O(n) extra space.

**Dry run:** nums = [1, 2, 4, 3, 5, 6], insertion sort.
| i | x | compare | result |
|---|---|---|---|
| 1 | 2 | 1 > 2? no | 1 comparison |
| 2 | 4 | 2 > 4? no | 1 |
| 3 | 3 | 4 > 3 yes (shift), 2 > 3 no | 2 comparisons, 1 shift |
| 4 | 5 | 4 > 5? no | 1 |
| 5 | 6 | 5 > 6? no | 1 |
Total 6 comparisons, 1 shift, 1 inversion (the pair 4, 3). Formula: 1 inversion + 5 - 0 new minima = 6. Merge sort: 8 comparisons (observed from the counter, independent of order). Timsort: 10 observed on CPython 3.13 (a short list is handled by finding the run [1, 2, 4] then binary insertion of the remaining items; I report the measured number, not a hand derivation).

**Code:**
```python
import random, itertools, functools, math
random.seed(43)

# ---- Timsort: count the '<' calls CPython's list.sort makes, by sorting objects that count them
class Cnt:
    n = 0
    __slots__ = ('v',)
    def __init__(self, v): self.v = v
    def __lt__(self, o): Cnt.n += 1; return self.v < o.v
def timsort_cmps(nums):
    Cnt.n = 0; sorted(Cnt(v) for v in nums); return Cnt.n

# ---- plain insertion sort: comparisons a[j-1] > x, element moves
def insertion(nums):
    a = list(nums); cmps = shifts = 0
    for i in range(1, len(a)):
        x = a[i]; j = i
        while j > 0:
            cmps += 1
            if a[j - 1] > x: a[j] = a[j - 1]; shifts += 1; j -= 1
            else: break
        a[j] = x
    assert a == sorted(nums)
    return cmps, shifts

# ---- inversions in O(n log n) by merge counting; (the brute force below is O(n^2))
def inversions(nums):
    a = list(nums)
    def go(lo, hi):
        if hi - lo < 2: return 0
        mid = (lo + hi) // 2; inv = go(lo, mid) + go(mid, hi)
        L, R = a[lo:mid], a[mid:hi]; i = j = 0; k = lo
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: a[k] = L[i]; i += 1
            else: a[k] = R[j]; j += 1; inv += len(L) - i
            k += 1
        a[k:hi] = L[i:] + R[j:]
        return inv
    return go(0, len(a))

# ---- top-down merge sort of Q15: split at n // 2, take from the left on ties (<=), count comparisons
def merge_cmps(nums):
    c = 0
    def sort(x):
        nonlocal c
        if len(x) <= 1: return x
        m = len(x) // 2; L, R = sort(x[:m]), sort(x[m:]); out = []; i = j = 0
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(list(nums)); return c

def solve(nums):
    ic, sh = insertion(nums)
    return [timsort_cmps(nums), ic, sh, inversions(nums), merge_cmps(nums)]

# ---- examples
ex = {(1, 2, 3, 4, 5): [4, 4, 0, 0, 5], (5, 4, 3, 2, 1): [4, 10, 10, 10, 7], (1, 2, 4, 3, 5, 6): [10, 6, 1, 1, 8],
      (2, 2, 1, 1): [5, 6, 4, 4, 4], (): [0, 0, 0, 0, 0]}
for k, v in ex.items(): assert solve(list(k)) == v, (k, solve(list(k)))
print('examples ok:', [solve(list(k)) for k in ex])

# ---- cross-check: separate counting wrapper (cmp_to_key counts calls of the comparison function) and O(n^2) inversions
def tim_alt(nums):
    c = [0]
    def cmp(x, y): c[0] += 1; return -1 if x < y else (1 if x > y else 0)
    sorted(nums, key=functools.cmp_to_key(cmp)); return c[0]
for _ in range(1500):
    n = random.randint(0, 40); k = random.choice([2, 5, 100])
    t = [random.randint(0, k) for _ in range(n)]
    inv2 = sum(t[i] > t[j] for i in range(n) for j in range(i + 1, n))
    r = solve(t)
    assert r[0] == tim_alt(t) and r[3] == inv2 and r[2] == inv2
print('1500 random lists: Timsort count == cmp_to_key counter, merge-count inversions == O(n^2) count == insertion shifts')

# ---- exhaustive claims for small n (all lists over 0..2, lengths <= 7)
tested = 0
for n in range(0, 8):
    for t in itertools.product(range(3), repeat=n):
        ic, sh = insertion(t); inv = sum(t[i] > t[j] for i in range(n) for j in range(i + 1, n))
        assert sh == inv                                            # each shift removes exactly one inversion
        minima = sum(1 for i in range(1, n) if all(t[p] > t[i] for p in range(i)))   # items that go all the way to the front
        assert ic == inv + (n - 1 if n else 0) - minima             # exact comparison count
        tested += 1
print('shifts == inversions and comparisons == inversions + (n-1) - (strict new prefix minima) for', tested, 'lists')

# ---- Timsort on already sorted / strictly descending lists: n - 1 comparisons (CPython 3.13, observed)
for n in range(1, 300):
    assert timsort_cmps(list(range(n))) == max(n - 1, 0)
    assert timsort_cmps(list(range(n, 0, -1))) == max(n - 1, 0)
print('sorted and strictly descending lists of every length 1..299: exactly n - 1 comparisons')
print('descending with ties [2,2,1,1]:', timsort_cmps([2, 2, 1, 1]), '(not strictly descending, so not one run)')

# ---- n = 300: nearly sorted versus random versus reversed
base = list(range(300))
near = list(base)
for _ in range(5):
    i = random.randrange(299); near[i], near[i + 1] = near[i + 1], near[i]
rnd = random.sample(base, 300)
print('n = 300  (timsort, insertion, shifts, inversions, merge)')
for name, t in (('sorted', base), ('5 adjacent swaps', near), ('reversed', base[::-1]), ('random', rnd)):
    print(f'  {name:17}', solve(t))

# ---- edge asserts
assert solve([7]) == [0, 0, 0, 0, 0]
assert solve([1, 1, 1, 1]) == [3, 3, 0, 0, 4]
assert solve([2, 1]) == [1, 1, 1, 1, 1]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[4, 4, 0, 0, 5], [4, 10, 10, 10, 7], [10, 6, 1, 1, 8], [5, 6, 4, 4, 4], [0, 0, 0, 0, 0]]
1500 random lists: Timsort count == cmp_to_key counter, merge-count inversions == O(n^2) count == insertion shifts
shifts == inversions and comparisons == inversions + (n-1) - (strict new prefix minima) for 3280 lists
sorted and strictly descending lists of every length 1..299: exactly n - 1 comparisons
descending with ties [2,2,1,1]: 5 (not strictly descending, so not one run)
n = 300  (timsort, insertion, shifts, inversions, merge)
  sorted            [299, 299, 0, 0, 1180]
  5 adjacent swaps  [541, 304, 5, 5, 1182]
  reversed          [299, 44850, 44850, 44850, 1308]
  random            [2083, 22710, 22418, 22418, 2089]
edge asserts ok
```

**Edge cases:**
- Empty list and one item: all counts 0.
- All equal: insertion makes n - 1 comparisons and 0 shifts because the test is `>` (strict), which is also why it is stable. Merge sort still makes about n log n.
- Reversed: insertion sort's worst case, n(n-1)/2 for all three counters, while Timsort only needs n - 1.
- Ties in a descending list ([2, 2, 1, 1]): not one strict run.
- Wrapper objects versus plain ints: counting is only possible with objects; the ordering result is the same.

**Follow-ups:**
- Why is insertion sort used inside Timsort? It is the fastest option for tiny ranges (low overhead, adaptive); Timsort uses a binary-search variant for ranges below minrun (Q44).
- Does `sorted` call `__gt__`? CPython's list sort asks only for `<` (that is why the counter only defines `__lt__`).
- How would you count inversions in O(n log n)? During the merge: when a right item goes out before a left item, add the number of left items still waiting. The code does this.

**Common mistakes:**
- Saying insertion sort is O(n) on nearly sorted data without saying how nearly (it is O(n + inversions)).
- Forgetting the last failed comparison per item, so comparisons are not exactly the number of shifts.
- Using `>=` in the insertion loop: it moves equal items and loses stability.
- Claiming Timsort always beats insertion sort.
- Reading a Timsort count from a plain int list and assuming `__lt__` is called.

---

### Q44 ⭐ 🟡 Timsort ingredients: minrun and natural runs (editor-level description of CPython's algorithm, labelled as such: this exact description was not checked against the CPython source here). `nums` has 1 <= len <= 10^5 integers. Let n = len(nums). Compute `minrun(n)`: `r = 0; while n >= 64: r |= n & 1; n >>= 1` and return `n + r` (so for n < 64 it returns n). A natural run starting at position lo is the longest stretch that is either non-decreasing (a[i] >= a[i-1]) or strictly descending (a[i] < a[i-1]), decided by comparing a[lo + 1] with a[lo]; a run starting at the last position has length 1. Timsort scans from the left: the next run starts at lo and has length max(natural run length at lo, min(minrun, n - lo)) (short runs are extended to minrun by insertion sort), and the following run starts right after it. Return `[minrun, runs]`: the minrun value for n = len(nums) and the list of these run lengths in order. Explain why minrun lies between 32 and 64 for n >= 64 (and why, with s the number of right shifts the loop performs, n <= minrun * 2^s and minrun * 2^(s-1) < n, so n / minrun is never above a power of two and the merges stay balanced), why a strictly descending run is reversed (and why it must be STRICTLY descending to keep stability), and what the merge step with galloping adds. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursive scan that rebuilds the run boundaries on small inputs. Example: nums=[30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133] -> [32, [32, 32]]; nums=[9] -> [1, [1]]; nums=[4, 4, 4, 3] -> [4, [4]]; nums=[1, 2, 3, 2, 1, 0, 5, 6] -> [8, [8]].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** (Label: this answer is an editor-level description of CPython's Timsort. I tested my own implementation of the description (minrun and run scan) and claims about minrun for every n up to 10^5, but I did NOT check the description against the CPython source (`listobject.c`). Treat the galloping and merge-stack remarks below as interview-level knowledge, not verified facts.) Run detection plus a minimum run length, the first stage of Timsort: find the existing order in the data, pad short runs, then merge runs of balanced size.

**Say this first (1 line):** "Timsort scans for natural runs, a non-decreasing stretch or a strictly descending one it can reverse; anything shorter than minrun, a value between 32 and 64 chosen from n, is padded up to minrun by insertion sort; then runs are merged so that the number of runs is about a power of two."

**Brute force:** A recursive scan that rebuilds the run boundaries from scratch (the code's `solve_rec`): at each start find the natural run, pad to min(minrun, remaining), recurse on the rest. It is the same logic written differently; there is no independent definition to test it against except the description in the question.

**Optimal:** (a single left-to-right scan, O(n))
- `minrun(n)`: while n >= 64, shift right and remember if any 1 bit fell off (`r |= n & 1`); return `n + r`. For n < 64 it returns n: the whole list is one insertion-sort job.
- Natural run at lo: if `a[lo+1] < a[lo]` the run is strictly descending and extends while `a[i] < a[i-1]`; otherwise it is non-decreasing and extends while `a[i] >= a[i-1]`. A run at the last position has length 1.
- Run length = `max(natural, min(minrun, n - lo))`; the next run starts right after it.
- Why 32 <= minrun <= 64 for n >= 64: the loop stops when the shifted value k is below 64, and it only ever shifts a value that was >= 64, so k >= 32. Then minrun = k or k + 1 is at most 64. Checked for every n up to 10^5.
- Why merges stay balanced: with s the number of shifts, `n <= minrun * 2^s` and `minrun * 2^(s-1) < n`. So n / minrun is at most the power of two 2^s and more than 2^(s-1): the runs, each about minrun long, can be merged pairwise like a balanced tree of depth s with no leftover tiny run. The sticky bit `r` rounds minrun up whenever a 1 bit was dropped, so that n / minrun does not creep just above a power of two (which would leave one tiny extra run to merge). Also verified for every n up to 10^5.
- Why a descending run is reversed: reversing makes it ascending in O(length) without comparisons. It must be STRICTLY descending: if equal items were allowed in a descending run, reversing would flip their original order and break stability. Equal neighbours therefore end the descending run. With `[4, 4, 4, 3]` the scan sees a non-decreasing run of three 4s then a 3: the run is length 3, padded to 4.
- Merge step (editor-level): runs go on a stack and are merged when their lengths break an invariant (each run longer than the sum of the next two, in the usual description), using a temporary array of the smaller run. Galloping mode: if one run keeps winning, the merge switches to exponential search ("gallop") to skip many items at once, which makes merging two runs where one dominates close to linear in the smaller run. That is why nearly-sorted data is cheap.

**Complexity:**
- Scan: O(n) time, O(number of runs) space for the run list. The number of runs is at most about n / minrun for random data (2041 runs for 10^5 random items with minrun 49) and 1 for sorted data.
- Whole Timsort (editor knowledge): O(n) best case, O(n log n) worst case, O(n) extra space, stable.

**Dry run:** the first example has 64 items: 30, 29, ..., 1, then 100, 101, ..., 133.
- n = 64: the loop `while n >= 64` runs once (64 >> 1 = 32, remembered bit 0), so minrun = 32.
- lo = 0: `a[1] = 29 < 30`, strictly descending. It continues down to the item 1 at index 29, then `a[30] = 100` is not below 1, stop: natural length 30. `max(30, min(32, 64)) = 32`, so the run is padded by 2 items (100 and 101), and insertion sort puts them in place after the reversal.
- lo = 32: `a[33] = 103 >= a[32] = 102`, non-decreasing to the end: length 32. `max(32, min(32, 32)) = 32`.
- Result `[32, [32, 32]]`.

**Code:**
```python
import random
random.seed(44)
# Editor-level description of Timsort's run detection (NOT checked against the CPython source here).

def minrun(n):
    r = 0
    while n >= 64:
        r |= n & 1                 # remember if any 1 bit was shifted out
        n >>= 1
    return n + r

def solve(nums):
    n = len(nums); mr = minrun(n); runs = []; lo = 0
    while lo < n:
        i = lo + 1
        if i < n:
            if nums[i] < nums[lo]:                              # strictly descending run
                while i < n and nums[i] < nums[i - 1]: i += 1
            else:                                               # non-decreasing run
                while i < n and nums[i] >= nums[i - 1]: i += 1
        length = max(i - lo, min(mr, n - lo))                   # short runs are padded to minrun by insertion sort
        runs.append(length); lo += length
    return [mr, runs]

# ---- recursive scan that rebuilds the run boundaries, written separately
def solve_rec(nums):
    n = len(nums)
    k, r = n, 0
    while k >= 64: r |= k & 1; k >>= 1
    m = k + r
    def natural(lo):
        if lo == n - 1: return 1
        desc = nums[lo + 1] < nums[lo]
        e = lo + 1
        while e < n and ((nums[e] < nums[e - 1]) if desc else (nums[e] >= nums[e - 1])): e += 1
        return e - lo
    def go(lo):
        if lo >= n: return []
        rl = max(natural(lo), min(m, n - lo))
        return [rl] + go(lo + rl)            # depth = number of runs: keep the lists small
    return [m, go(0)]

# ---- examples
ex1 = list(range(30, 0, -1)) + list(range(100, 134))
assert solve(ex1) == [32, [32, 32]]
assert solve([9]) == [1, [1]]
assert solve([4, 4, 4, 3]) == [4, [4]]
assert solve([1, 2, 3, 2, 1, 0, 5, 6]) == [8, [8]]
print('examples ok:', solve(ex1), solve([9]), solve([4, 4, 4, 3]), solve([1, 2, 3, 2, 1, 0, 5, 6]))

# ---- seeded random cross-check (short inputs so the recursion in solve_rec stays shallow)
for _ in range(3000):
    n = random.randint(1, 120)
    mode = random.choice(['rand', 'runs', 'few'])
    if mode == 'rand': t = [random.randint(0, 30) for _ in range(n)]
    elif mode == 'few': t = [random.randint(0, 2) for _ in range(n)]
    else:
        t = []
        while len(t) < n:
            L = random.randint(1, 40); s = random.randint(0, 100); d = random.choice([-1, 1, 0])
            t += [s + d * k for k in range(L)]
        t = t[:n]
    assert solve(t) == solve_rec(t), t
    mr, runs = solve(t); assert sum(runs) == n and all(r >= min(mr, n) or r == runs[-1] for r in runs)
print('3000 random inputs: scan == recursive rebuild; run lengths sum to n; every run but the last is >= minrun')

# ---- claims about minrun, checked for EVERY n up to 10^5
for n in range(1, 100001):
    m = minrun(n)
    if n < 64: assert m == n; continue
    k, s = n, 0
    while k >= 64: k >>= 1; s += 1
    assert 32 <= m <= 64
    assert n <= m * 2 ** s and m * 2 ** (s - 1) < n
print('every n in 1..100000: n < 64 -> minrun = n; n >= 64 -> 32 <= minrun <= 64, n <= minrun * 2^s and minrun * 2^(s-1) < n')
print('examples of minrun:', {n: minrun(n) for n in (63, 64, 65, 127, 128, 1000, 2048, 2049, 100000)})
print('n / minrun for some n (always <= the next power of two, here 2, 2, 16, 64, 2048):',
      {n: round(n / minrun(n), 3) for n in (65, 127, 1000, 2049, 100000)})

# ---- a run-structure demonstration at the maximum size
big = [random.randint(0, 10**9) for _ in range(100000)]
mr, runs = solve(big)
print('random 100000 items: minrun', mr, ', number of runs', len(runs), ', first runs', runs[:3], ', last run', runs[-1])
inc = list(range(100000)); mr, runs = solve(inc)
print('sorted 100000 items: runs', runs)

# ---- edge asserts
assert solve([2, 1]) == [2, [2]]
assert solve([3, 3, 3]) == [3, [3]]
assert minrun(64) == 32 and minrun(65) == 33 and minrun(127) == 64 and minrun(128) == 32
n = 130; t = list(range(100, 0, -1)) + list(range(30))       # 100..1 then 0..29
assert solve(t) == [33, [101, 29]]     # the 0 after 1 continues the strict descent
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [32, [32, 32]] [1, [1]] [4, [4]] [8, [8]]
3000 random inputs: scan == recursive rebuild; run lengths sum to n; every run but the last is >= minrun
every n in 1..100000: n < 64 -> minrun = n; n >= 64 -> 32 <= minrun <= 64, n <= minrun * 2^s and minrun * 2^(s-1) < n
examples of minrun: {63: 63, 64: 32, 65: 33, 127: 64, 128: 32, 1000: 63, 2048: 32, 2049: 33, 100000: 49}
n / minrun for some n (always <= the next power of two, here 2, 2, 16, 64, 2048): {65: 1.97, 127: 1.984, 1000: 15.873, 2049: 62.091, 100000: 2040.816}
random 100000 items: minrun 49 , number of runs 2041 , first runs [49, 49, 49] , last run 40
sorted 100000 items: runs [100000]
edge asserts ok
```

**Edge cases:**
- n = 1: minrun 1, one run of length 1.
- n < 64: always a single run [n]; Timsort is then just binary insertion sort after the first run.
- All equal: non-decreasing, one run.
- n = 64 gives minrun 32 (not 64); n = 65 gives 33 (the dropped bit is remembered); n = 127 gives 64.
- Strictly descending whole list: one run, reversed.
- Non-strict descent such as [4, 4, 3] is not a descending run (it is non-decreasing for 2 items, then breaks).

**Follow-ups:**
- Why not minrun = 64 always? Then n = 65 would give runs 64 + 1 and an unbalanced merge. The rounding rule keeps n / minrun at or below a power of two.
- Why a minimum run at all? Insertion sort on 32..64 items is cheaper than merging tiny runs, and it uses cache well.
- Is Timsort quicksort-like? No. It is a merge sort with run detection and insertion sort for short runs (Q43, Q16).

**Common mistakes:**
- Letting the descending run be non-strict, which breaks stability after the reversal.
- Treating `n // 64` as minrun.
- Forgetting the last item can be a run of length 1.
- Presenting galloping thresholds or the merge-stack invariant as verified facts; they are described from memory here.

---

### Q45 ⭐ 🟡 Big integers: Fibonacci by fast doubling. `n` is an integer with 0 <= n <= 10^5 (F(0) = 0, F(1) = 1). Return `[mod, digits, lead]`: F(n) modulo 10^9 + 7, the number of decimal digits of F(n) (F(n) itself has up to about 21000 digits), and the string of its first min(5, digits) decimal digits. Compute F(n) exactly with the doubling identities F(2k) = F(k) * (2 * F(k+1) - F(k)) and F(2k+1) = F(k)^2 + F(k+1)^2 (O(log n) big multiplications, recursion depth about 17), and compare with the O(n) additions of the simple loop. Python integers have unlimited size, but in recent Python versions (the limit appeared in 3.11, editor knowledge, not checked against a page; the default of 4300 digits is observed on 3.13) converting an int with more than 4300 decimal digits to a string with `str()` or `int(s)` raises ValueError by default (`sys.set_int_max_str_digits` changes the limit; the limit does not apply to power-of-two bases such as `hex`); state how you get the digit count and the leading digits for large n despite this (for example by raising the limit, or from the bit length and `math.log10`) and what the checker accepts: exact values only. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n) addition loop with the digits counted by chunked division on small inputs. Example: n=10 -> [55, 2, '55']; n=0 -> [0, 1, '0']; n=100 -> [687995182, 21, '35422']; n=30000 -> [393965141, 6270, '19042'].
**Asked at:** Python documentation for int, float, Decimal and Fraction (docs.python.org fetch failed with ENOTFOUND, not opened; behaviour verified by running Python 3.13)
**Pattern:** Fast doubling (a divide and conquer on the exponent, like fast power) on Python's unbounded integers. It applies because F(2k) and F(2k+1) can be computed from F(k) and F(k+1) alone.

**Say this first (1 line):** "Python ints never overflow, so I compute F(n) exactly with the doubling identities in O(log n) big multiplications, take it mod 10^9 + 7 at the end, and get the digit count and leading digits without calling str() on a huge int, because that has a default limit of 4300 digits."

**Brute force:** Loop n additions: `a, b = b, a + b`. It is exact and simple, but O(n) big additions, each O(size of the number), so O(n^2) bit operations overall (F(10^5) is about 69,000 bits, 20899 digits). The code uses it as the checker, with digits counted by chunked division.

**Optimal:**
- `fib_pair(n)` returns `(F(n), F(n+1))`. Recurse on `n >> 1` to get `(a, b) = (F(k), F(k+1))`.
- `F(2k) = a * (2b - a)` and `F(2k+1) = a^2 + b^2`. If n is odd return `(F(2k+1), F(2k) + F(2k+1))`, else `(F(2k), F(2k+1))`.
- Depth is the bit length of n, 17 for n = 10^5: safe for the recursion limit. Base case `(0, 1)`.
- Mod 10^9 + 7: take `% MOD` of the exact value at the end. (If you only wanted the modulus, you could reduce at every step and keep numbers small; here the exact value is needed for the digits.)
- Digit count without `str()`: estimate `bit_length * log10(2)` (a float estimate), then correct it with exact comparisons against powers of ten (`x >= 10**d` raise, `x < 10**(d-1)` lower). Leading digits: `x // 10**(d - 5)` is an int below 10^5, so `str()` of it is safe.
- The limit: from Python 3.11 (editor knowledge, not checked against a page), `str(int)` and `int(str)` raise ValueError above 4300 digits by default. On 3.13 I observed the 4300 default and the ValueError for F(30000) (6270 digits) and for `int('9' * 5000)`. `sys.set_int_max_str_digits(0)` lifts it (the code does that once as a check and restores the old value); `hex()` is not affected because the limit applies to non-power-of-two bases. Exact values only are accepted, so no float estimate is the final answer: the float is used only as a starting guess and fixed by exact comparisons.

**Complexity:**
- Doubling: O(log n) multiplications of numbers up to about 0.694 * n bits. Each big multiplication is subquadratic (Karatsuba in CPython, editor knowledge), so the total is dominated by the last few steps, about O(M(n)) where M is the cost of one multiplication of n-bit numbers.
- Addition loop: n additions of numbers up to 0.694 n bits, O(n^2) bit operations overall.
- Space: O(n) bits for the result, O(log n) recursion frames.
- Sandbox timings, not proof: at n = 10^5 the doubling took about 0.002 s and the loop about 0.1 s.

**Dry run:** n = 10, binary 1010.
| call | k = n >> 1 | (F(k), F(k+1)) | result |
|---|---|---|---|
| fib_pair(0) | | | (0, 1) |
| fib_pair(1) | 0 | (0, 1) | F(0) = 0*(2*1-0) = 0, F(1) = 0 + 1 = 1; n odd -> (1, 0 + 1) = (1, 1) |
| fib_pair(2) | 1 | (1, 1) | F(2) = 1*(2-1) = 1, F(3) = 1 + 1 = 2; even -> (1, 2) |
| fib_pair(5) | 2 | (1, 2) | F(4) = 1*(4-1) = 3, F(5) = 1 + 4 = 5; odd -> (5, 3 + 5) = (5, 8) |
| fib_pair(10) | 5 | (5, 8) | F(10) = 5*(16-5) = 55, F(11) = 25 + 64 = 89; even -> (55, 89) |
F(10) = 55: mod 55, 2 digits, lead '55'.

**Code:**
```python
import sys, math, random, time
random.seed(45)
MOD = 10**9 + 7

# ---- fast doubling: returns (F(n), F(n+1)); depth = bit length of n (about 17 for 10^5)
def fib_pair(n):
    if n == 0: return 0, 1
    a, b = fib_pair(n >> 1)                 # a = F(k), b = F(k+1), k = n // 2
    c = a * (2 * b - a)                     # F(2k)
    d = a * a + b * b                       # F(2k+1)
    return (d, c + d) if n & 1 else (c, d)

def fib_loop(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a

# ---- digit count and leading digits WITHOUT calling str() on a huge int:
#      estimate from the bit length, then fix by an exact comparison with a power of ten
def digits_and_lead(x):
    if x == 0: return 1, '0'
    d = max(1, int(x.bit_length() * 0.30102999566398114))      # a lower estimate of the digit count
    while x >= 10 ** d: d += 1                                 # exact: d is the smallest with x < 10^d
    while d > 1 and x < 10 ** (d - 1): d -= 1
    k = max(0, d - 5)
    lead = x // 10 ** k                                        # the first min(5, d) digits, as an int < 10^5 (str is safe)
    return d, str(lead)

def solve(n):
    f = fib_pair(n)[0]
    dg, lead = digits_and_lead(f)
    return [f % MOD, dg, lead]

# ---- examples
assert solve(10) == [55, 2, '55']
assert solve(0) == [0, 1, '0']
assert solve(100) == [687995182, 21, '35422']
assert solve(30000) == [393965141, 6270, '19042']
print('examples ok:', solve(10), solve(0), solve(100), solve(30000))

# ---- cross-check: O(n) addition loop; digits counted by chunked division (no str on a big int)
def digits_chunked(x):
    if x == 0: return 1
    chunk = 10 ** 1000; count = 0
    while x >= chunk: x //= chunk; count += 1000
    return count + len(str(x))                  # the remainder has < 1001 digits, so str() is safe
for n in list(range(0, 400)) + [random.randint(400, 20000) for _ in range(60)]:
    f = fib_loop(n)
    assert fib_pair(n)[0] == f
    dg, lead = digits_and_lead(f)
    assert dg == digits_chunked(f)
    # leading digits independent check: divide away the low digits in 1000-digit chunks, then use str on the small rest
    y, rest = f, dg
    while rest > 1000: y //= 10 ** 1000; rest -= 1000
    assert lead == str(y)[:5], (n, lead)
    assert solve(n) == [f % MOD, dg, lead]
print('460 values of n (0..399 and 60 random up to 20000): doubling == addition loop; digits and leading digits agree with chunked division')

# ---- the int-to-str digit limit (observed on this Python; the 3.11 introduction is editor knowledge)
big = fib_pair(30000)[0]
print('default limit:', sys.get_int_max_str_digits(), '; F(30000) has', digits_and_lead(big)[0], 'digits')
try: str(big)
except ValueError as e: print('str(F(30000)) ->', type(e).__name__)
try: int('9' * 5000)
except ValueError as e: print("int('9' * 5000) ->", type(e).__name__)
print('hex works (power-of-two base):', len(hex(big)), 'characters; bit_length', big.bit_length())
old = sys.get_int_max_str_digits(); sys.set_int_max_str_digits(0)
assert len(str(big)) == 6270 and str(big)[:5] == '19042'
sys.set_int_max_str_digits(old)
print('with the limit lifted str() gives the same 6270 digits and lead 19042; limit restored to', sys.get_int_max_str_digits())

# ---- maximum size and the cost shape (sandbox timings, not proof of big-O)
t = time.perf_counter(); r = solve(100000); t1 = time.perf_counter() - t
t = time.perf_counter(); f = fib_loop(100000); t2 = time.perf_counter() - t
assert f == fib_pair(100000)[0] and r[0] == f % MOD
print('n = 100000:', r, ', digits by length-estimate method;  (sandbox timing) doubling %.4f s, addition loop %.4f s' % (t1, t2))

# ---- Binet's formula in floats: where does it first go wrong?
a = 0
for n in range(200):
    if round(((1 + 5 ** 0.5) / 2) ** n / 5 ** 0.5) != fib_pair(n)[0]: break
print('float Binet first differs from the exact value at n =', n)

# ---- edge asserts
assert solve(1) == [1, 1, '1'] and solve(2) == [1, 1, '1'] and solve(5) == [5, 1, '5']
assert solve(12) == [144, 3, '144'] and solve(20) == [6765, 4, '6765']
assert fib_pair(0) == (0, 1) and fib_pair(1) == (1, 1)
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [55, 2, '55'] [0, 1, '0'] [687995182, 21, '35422'] [393965141, 6270, '19042']
460 values of n (0..399 and 60 random up to 20000): doubling == addition loop; digits and leading digits agree with chunked division
default limit: 4300 ; F(30000) has 6270 digits
str(F(30000)) -> ValueError
int('9' * 5000) -> ValueError
hex works (power-of-two base): 5209 characters; bit_length 20827
with the limit lifted str() gives the same 6270 digits and lead 19042; limit restored to 4300
n = 100000: [911435502, 20899, '25974'] , digits by length-estimate method;  (sandbox timing) doubling 0.0026 s, addition loop 0.0798 s
float Binet first differs from the exact value at n = 71
edge asserts ok
```

**Edge cases:**
- n = 0: F = 0, which has 1 digit and lead '0'. n = 1 and 2: F = 1.
- Fewer than 5 digits: the lead is the whole number (`10**0 = 1` divisor).
- Digit count near a power of ten: the estimate can be off by one, which is why the comparisons with `10**d` are exact.
- Doing `str(F(30000))` directly: ValueError on the default setting.
- Applying `% MOD` inside the identities: `2*b - a` can go negative when reduced, fix with `+ MOD` (not needed here because the exact value is used).

**Follow-ups:**
- Fibonacci mod m only, for huge n (10^18)? Same doubling with every product reduced mod m. Or the matrix power of [[1, 1], [1, 0]].
- Why not Binet's formula? Floats lose precision: the float version first gives a wrong value at n = 71 in my run.
- Is the pisano period relevant? For a single known modulus it can shorten n, but doubling is already O(log n).

**Common mistakes:**
- Calling `str()` on a 6000-digit number and getting ValueError.
- Using `len(str(...))` after setting the limit to 0 for untrusted input (the limit exists to stop denial of service on parsing).
- Using floats for the digit count and trusting them without an exact check.
- Reducing mod in the middle and then trying to read digits from the reduced value.

---

### Q46 ⭐ 🟡 The comparison-sort lower bound, measured for tiny n. `n` is an integer with 1 <= n <= 5. Return `[info_bound, merge_worst, insertion_worst, optimal]`: `info_bound` = ceil(log2(n!)), the information-theoretic lower bound on comparisons for any comparison sort in the worst case; `merge_worst` = the largest number of comparisons the top-down merge sort of Q15 (keys compared with `<=`) makes over all n! orderings of n distinct keys; `insertion_worst` = the largest number of comparisons of binary insertion sort (insert the next item into the sorted prefix by binary search with `lo = 0, hi = len(prefix)`, `mid = (lo + hi) // 2`, one comparison `x < a[mid]` per probe: if true `hi = mid` else `lo = mid + 1`) over all orderings; `optimal` = the true minimum worst-case number of comparisons of ANY comparison-based sorting strategy for n items, found by exhaustive search over decision trees. Explain the decision-tree argument (n! leaves, a binary tree of depth d has at most 2^d leaves, so d >= log2(n!), which is Theta(n log n) by Stirling) and that for n = 5 the bound is met only by a cleverer algorithm than merge or binary insertion (seven comparisons suffice). Say what this does not cover: counting sort and radix sort are not comparison sorts, so the bound does not apply to them. In the answer include a dry run on the first example and a seeded random cross-check of your solution against closed-form worst-case recurrences and a table of the known optimal values on small inputs. Example: n=3 -> [3, 3, 3, 3]; n=4 -> [5, 5, 5, 5]; n=5 -> [7, 8, 8, 7].
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Decision-tree argument (information theory) for a lower bound, plus exhaustive search over tiny cases to see how close real algorithms get.

**Say this first (1 line):** "A comparison sort is a binary decision tree with n! leaves, a tree of depth d has at most 2^d leaves, so some input needs at least ceil(log2(n!)) comparisons, which is Theta(n log n); for n = 5 that is 7, and merge sort and binary insertion need 8, but a cleverer algorithm does it in 7."

**Brute force:** Compute every number by running the algorithms over all n! orderings (n <= 5 means at most 120 inputs): the worst case of merge sort and of binary insertion sort are max over all permutations. The optimal value is found by exhaustive search over decision trees: a state is the set of permutations still consistent with the answers so far; `can(S, L)` asks whether some comparison splits S into two non-empty parts that both can be finished in L - 1 more comparisons. Prune with "a tree of depth L has at most 2^L leaves". Try L = 0, 1, 2, ... until the full set works.

**Optimal:** (the computed table, every number from the run below)
| n | n! | info bound ceil(log2 n!) | merge sort worst | binary insertion worst | optimal (exhaustive) |
|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 1 | 1 | 1 | 1 |
| 3 | 6 | 3 | 3 | 3 | 3 |
| 4 | 24 | 5 | 5 | 5 | 5 |
| 5 | 120 | 7 | 8 | 8 | 7 |
- The argument: every comparison sort, run on distinct keys, must reach a different leaf for each of the n! orderings (otherwise two orderings would get the same output, and one is wrong). A binary tree of depth d has at most 2^d leaves, so 2^d >= n!, d >= log2(n!). Stirling gives log2(n!) = n log2 n - n log2 e + O(log n), so Theta(n log n).
- For n <= 4 merge sort and binary insertion already hit the bound. For n = 5 the bound is 7 and the true optimum is 7 (exhaustive search), but both simple algorithms need 8.
- The gap is closed by a cleverer algorithm. I implemented merge insertion (Ford-Johnson) in the code: pair up items, sort the larger of each pair recursively, insert the small partners by binary search in a special (Jacobsthal) order. Its worst case over all permutations is 0, 1, 3, 5, 7, 10, 13 for n = 1..7. That is a constructive proof that 7 comparisons sort 5 items.
- What it does not cover: counting sort and radix sort are not comparison sorts (they read key digits and index arrays), so Omega(n log n) does not apply to them. The bound is also a worst-case bound over inputs with distinct keys; with many equal keys or special structure (nearly sorted, Q43) fewer comparisons suffice.
- Closed forms used as a cross-check: merge sort worst `W(n) = W(n // 2) + W(n - n // 2) + n - 1` (gives 0, 1, 3, 5, 8); binary insertion worst = sum over i = 1..n-1 of ceil(log2(i + 1)) = sum of `bit_length(i)` (gives 0, 1, 3, 5, 8). For larger n the same formulas give merge worst 11, 17, 25, 33 against the info bound 10, 16, 22, 29 at n = 6, 8, 10, 12; those are formulas, not searches (the exhaustive optimum was computed only for n <= 5).

**Complexity:**
- The lower bound: Omega(n log n) comparisons, since log2(n!) >= (n / 2) log2(n / 2) (half of the factors are at least n / 2).
- My exhaustive search is only for tiny n: 5! = 120 permutations, states are subsets of them, and the number of subsets that can appear grows very fast with n, so I ran it only for n <= 5 (well under a second here) and claim nothing about its cost or results beyond that.
- Merge sort: O(n log n), binary insertion: O(n log n) comparisons but O(n^2) element moves with a list.

**Dry run:** n = 3. There are 6 orderings, so the tree needs 6 leaves; depth 2 gives only 4 leaves, depth 3 gives 8, so the bound is 3.
- Merge sort on 3 items: split [a] and [b, c]; sorting [b, c] costs 1 comparison; merging [a] with the sorted pair costs at most 2: worst case 3.
- Binary insertion: the second item costs 1 probe; the third is inserted into 2 items with 2 probes at most: 3.
- Optimal is 3: nothing can be below the bound 3, and the exhaustive search finds a depth-3 strategy. So the row is `[3, 3, 3, 3]`.

**Code:**
```python
import itertools, math, functools, random
random.seed(46)

# ---- one comparison counter shared by the sorters below
def merge_sort_cmps(perm):                    # top-down merge sort of Q15: split at n // 2, `<=` on ties
    c = 0
    def sort(x):
        nonlocal c
        if len(x) <= 1: return x
        m = len(x) // 2; L, R = sort(x[:m]), sort(x[m:]); out = []; i = j = 0
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(list(perm)); return c

def binary_insertion_cmps(perm):              # exactly the probe rule of the question
    a = []; c = 0
    for x in perm:
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2; c += 1
            if x < a[mid]: hi = mid
            else: lo = mid + 1
        a.insert(lo, x)
    assert a == sorted(perm)
    return c

# ---- optimal: exhaustive search over decision trees.
# State = the set of permutations (as indices) still consistent with the answers so far.
# can(S, L): can some comparison strategy of depth <= L identify the permutation inside S?
def optimal(n):
    perms = list(itertools.permutations(range(n)))
    pos = [[p.index(v) for v in range(n)] for p in perms]          # pos[k][v] = place of value v in permutation k
    pairs = list(itertools.combinations(range(n), 2))
    @functools.lru_cache(None)
    def can(S, L):
        if len(S) == 1: return True
        if L == 0 or len(S) > 2 ** L: return False                  # a tree of depth L has at most 2^L leaves
        for i, j in pairs:
            yes = frozenset(k for k in S if pos[k][i] < pos[k][j]); no = S - yes
            if yes and no and can(yes, L - 1) and can(no, L - 1): return True
        return False
    L = 0; full = frozenset(range(len(perms)))
    while not can(full, L): L += 1
    return L

def solve(n):
    perms = list(itertools.permutations(range(n)))
    return [math.ceil(math.log2(math.factorial(n))), max(merge_sort_cmps(p) for p in perms),
            max(binary_insertion_cmps(p) for p in perms), optimal(n)]

# ---- examples
assert solve(3) == [3, 3, 3, 3] and solve(4) == [5, 5, 5, 5] and solve(5) == [7, 8, 8, 7]
print('examples ok')

# ---- the computed table
print(' n  n!   info_bound  merge_worst  insertion_worst  optimal')
table = {}
for n in range(1, 6):
    table[n] = solve(n)
    print(f'{n:2} {math.factorial(n):4} {table[n][0]:10} {table[n][1]:12} {table[n][2]:16} {table[n][3]:8}')
assert [table[n][0] for n in range(1, 6)] == [0, 1, 3, 5, 7] and [table[n][3] for n in range(1, 6)] == [0, 1, 3, 5, 7]

# ---- cross-check 1: closed-form worst cases
W = {0: 0, 1: 0}
for n in range(2, 13): W[n] = W[n // 2] + W[n - n // 2] + n - 1                 # merge sort worst-case recurrence
for n in range(1, 6):
    assert table[n][1] == W[n]
    assert table[n][2] == sum(i.bit_length() for i in range(1, n))              # inserting into a prefix of i items needs ceil(log2(i+1)) = i.bit_length() probes
    assert table[n][3] >= table[n][0]                                           # nobody beats the information bound
print('closed forms agree: merge worst W(n) = W(n//2) + W(n - n//2) + n - 1, binary insertion worst = sum of bit_length(i), i < n')

# ---- cross-check 2: a real algorithm that reaches the optimum for n = 5 (Ford-Johnson merge insertion, editor-implemented)
def ford_johnson(perm):
    c = 0
    def less(x, y):
        nonlocal c; c += 1; return x < y
    def fj(items):
        n = len(items)
        if n <= 1: return list(items)
        big, small = [], {}
        for i in range(0, n - 1, 2):
            x, y = items[i], items[i + 1]
            if less(x, y): x, y = y, x               # x is the larger of the pair
            big.append(x); small[x] = y
        rest = items[-1] if n % 2 else None
        chain = fj(big)                              # sort the larger elements recursively
        main = [small[chain[0]]] + chain             # b1 < a1 < a2 ...
        pend = [small[a] for a in chain[1:]] + ([rest] if rest is not None else [])   # b2, b3, ...
        bound = {small[a]: a for a in chain[1:]}      # b_j must be inserted below its partner a_j
        done, t_prev, k = 0, 1, 1
        # Jacobsthal numbers 1, 3, 5, 11, 21 ... give the insertion order: b_t, b_{t-1}, ..., b_{t_prev + 1}
        jac = [1, 3, 5, 11, 21, 43]
        order = []; prev = 1
        for t in jac[1:]:
            t = min(t, len(pend) + 1)
            order += list(range(t, prev, -1))
            prev = t
            if t >= len(pend) + 1: break
        for j in order:                              # j is 2-based: pend[j - 2] is b_j
            b = pend[j - 2]
            hi = main.index(bound[b]) if b in bound else len(main)
            lo = 0
            while lo < hi:
                mid = (lo + hi) // 2
                if less(b, main[mid]): hi = mid
                else: lo = mid + 1
            main.insert(lo, b)
        return main
    out = fj(list(perm)); assert out == sorted(perm), (perm, out)
    return c
fj_worst = {n: max(ford_johnson(p) for p in itertools.permutations(range(n))) for n in range(1, 8)}
print('Ford-Johnson merge insertion, worst case over all permutations, n = 1..7:', [fj_worst[n] for n in range(1, 8)])
assert [fj_worst[n] for n in range(1, 6)] == [0, 1, 3, 5, 7]
print('so seven comparisons really do sort 5 items (matches the exhaustive optimum 7), while merge sort and binary insertion need 8')

# ---- information bound for larger n (formula only; no search is claimed beyond n = 5)
print('n: info_bound / merge_worst (closed forms) :', {n: (math.ceil(math.log2(math.factorial(n))), W[n]) for n in (6, 8, 10, 12)})

# ---- edge asserts
assert solve(1) == [0, 0, 0, 0] and solve(2) == [1, 1, 1, 1]
assert math.factorial(5) == 120 and 2 ** 6 < 120 <= 2 ** 7
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok
 n  n!   info_bound  merge_worst  insertion_worst  optimal
 1    1          0            0                0        0
 2    2          1            1                1        1
 3    6          3            3                3        3
 4   24          5            5                5        5
 5  120          7            8                8        7
closed forms agree: merge worst W(n) = W(n//2) + W(n - n//2) + n - 1, binary insertion worst = sum of bit_length(i), i < n
Ford-Johnson merge insertion, worst case over all permutations, n = 1..7: [0, 1, 3, 5, 7, 10, 13]
so seven comparisons really do sort 5 items (matches the exhaustive optimum 7), while merge sort and binary insertion need 8
n: info_bound / merge_worst (closed forms) : {6: (10, 11), 8: (16, 17), 10: (22, 25), 12: (29, 33)}
edge asserts ok
```

**Edge cases:**
- n = 1: no comparisons, all four values 0. n = 2: one comparison.
- n = 5 is the first size where simple algorithms miss the bound. For n = 6 the formulas give merge worst 11 against bound 10 (formula only, not searched).
- Equal keys can make some leaves identical, so the bound above is for distinct keys.
- ceil(log2(n!)) needs an exact computation: `(n! - 1).bit_length()` avoids float rounding; the code uses `math.log2`, which is fine at this size.

**Follow-ups:**
- Is the bound ever tight for large n? Not exactly; merge-insertion is close and was conjectured optimal for a long time, but it is known not to be optimal for some n (editor knowledge, not checked here).
- How do counting and radix sort beat n log n? They are not comparison-based: O(n + k) and O(d (n + k)) (Q37).
- What about the average case? The same argument gives log2(n!) on average too, since a balanced tree has leaves at depth about log2(n!) (editor-level).

**Common mistakes:**
- Saying "n log n is a lower bound for sorting" without "comparison-based".
- Forgetting that a tree of depth d has at most 2^d leaves, not d.
- Thinking merge sort is optimal at every n (it is not at n = 5).
- Using floats for ceil(log2(n!)) at large n.

---

### Q47 ⭐ 🔴 Count of range sums with merge sort. `nums` has 1 <= len <= 5*10^4 integers (|value| <= 10^9) and `lo <= hi` are integers with |lo|, |hi| <= 10^14. Return the number of pairs (i, j) with 0 <= i <= j < len(nums) such that the sum nums[i] + ... + nums[j] lies in [lo, hi]. Turn it into pairs of prefix sums `pre[a] < pre[b]` positions a < b with lo <= pre[b] - pre[a] <= hi (with `pre[0] = 0`), then count them while merge sorting the prefix array: for every left-half value count the right-half values within [v + lo, v + hi] using two moving pointers on the already sorted right half, in O(n log n). Explain why the counting step must happen before the merge of the two halves, why each of the two pointers only moves forward, and why a Fenwick tree over coordinate-compressed prefix sums (Part 14) is the other standard answer. Recursion depth is about 17. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the O(n^2) double loop over subarrays on small inputs. Example: nums=[-2, 5, -1], lo=-2, hi=2 -> 3; nums=[0], lo=0, hi=0 -> 1; nums=[1, 2, 3], lo=3, hi=5 -> 3.
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened) | Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened)
**Pattern:** Prefix sums turn "subarray sum in a range" into "pairs of prefix values in a range"; merge sort counts such pairs while sorting (the same skeleton as counting inversions). Part 14 shows the Fenwick-tree alternative.

**Say this first (1 line):** "With pre[0] = 0 a subarray sum is pre[b] - pre[a] for a < b, so I count position-ordered pairs whose difference is in [lo, hi]; in a merge sort I count for each left value the right values in [v + lo, v + hi] with two forward-moving pointers, before merging."

**Brute force:** Double loop with a running sum: O(n^2). For n = 5 * 10^4 that is about 1.25 * 10^9 sums: too slow in Python. It is in the code as the checker.

**Optimal:**
- `pre = [0] + accumulate(nums)`, length n + 1.
- Merge sort on `pre`. At each node the left half holds earlier positions (smaller a), the right half later ones (larger b). Both halves are already sorted by value.
- Counting step: for each v in the sorted left half, the wanted right values lie in [v + lo, v + hi]. Two pointers on the sorted right half: `x` = first index with `R[x] - v >= lo`, `y` = first index with `R[y] - v > hi`; add `y - x`.
- Why the pointers only move forward: the left half is processed in ascending order, so v grows, so both thresholds v + lo and v + hi grow, and the first index satisfying a "value >= threshold" condition on a sorted list can only move right.
- Why count BEFORE merging: counting needs to know which values came from the left (earlier positions) and which from the right. After merging they are interleaved, and the pair (a, b) with a < b is no longer distinguishable. My wrong version that counts after the merge gave a wrong answer on 385 of 500 random cases. Pairs inside one half are counted at deeper levels, and every pair (a, b) is counted exactly once, at the node where the two positions are split into different halves.
- Fenwick alternative (Part 14, only named): scan the prefix sums left to right, coordinate-compress them, and ask a Fenwick tree for how many earlier prefix values lie in [pre - hi, pre - lo]. Same O(n log n).

**Complexity:**
- Each level of the recursion does O(n) pointer movement and O(n) merging, there are about log2(n + 1) = 16 levels for n = 5 * 10^4 (so recursion depth is about 17 and safe), so O(n log n) time.
- Space O(n) for the slices (this version creates new lists at each level; an index-based merge with one buffer would keep it at O(n) with a smaller constant).
- Python ints have no overflow, so sums up to 5 * 10^13 and bounds up to 10^14 are no problem (in a fixed-width language they need 64 bits).
- Sandbox timing, not proof: about 0.2 s for n = 50000.

**Dry run:** nums = [-2, 5, -1], lo = -2, hi = 2. `pre = [0, -2, 3, 2]`.
- Split into left `[0, -2]` and right `[3, 2]`.
- Left node: halves `[0]` and `[-2]`. For v = 0 look for R values in [-2, 2]: -2 qualifies, count 1 (subarray [-2]). Merge to `[-2, 0]`.
- Right node: `[3]` and `[2]`. For v = 3 look in [1, 5]: 2 qualifies, count 1 (subarray [-1]). Merge to `[2, 3]`.
- Root: L = `[-2, 0]`, R = `[2, 3]`. v = -2 wants [-4, 0]: none. v = 0 wants [-2, 2]: the value 2 qualifies, count 1 (the whole array, sum 2).
- Total 3.

**Code:**
```python
import random, itertools, bisect, time
random.seed(47)

# ---- optimal: prefix sums + merge sort; count BEFORE merging, with two forward-only pointers
def count_range_sum(nums, lo, hi):
    pre = [0] + list(itertools.accumulate(nums))        # pre[b] - pre[a] = sum of nums[a:b]
    count = 0
    def sort(a):                                         # returns the sorted list; depth about log2(n + 1)
        nonlocal count
        if len(a) <= 1: return a
        mid = len(a) // 2
        L, R = sort(a[:mid]), sort(a[mid:])             # L holds EARLIER positions than R
        x = y = 0
        for v in L:                                      # L is sorted ascending, so v + lo and v + hi only increase
            while x < len(R) and R[x] - v < lo: x += 1  # x: first R item with R - v >= lo
            while y < len(R) and R[y] - v <= hi: y += 1 # y: first R item with R - v > hi
            count += y - x                               # R[x:y] all lie in [v + lo, v + hi]
        out = []; i = j = 0                              # now merge (positions no longer matter above this level)
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        return out + L[i:] + R[j:]
    sort(pre)
    return count

# ---- brute force: every subarray with a running sum, O(n^2)
def brute(nums, lo, hi):
    c = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if lo <= s <= hi: c += 1
    return c

# ---- second independent method: sorted list + bisect (counts earlier prefix sums in [pre - hi, pre - lo]); O(n^2) inserts but tiny n
def with_bisect(nums, lo, hi):
    seen = [0]; s = 0; c = 0
    for v in nums:
        s += v
        c += bisect.bisect_right(seen, s - lo) - bisect.bisect_left(seen, s - hi)
        bisect.insort(seen, s)
    return c

# ---- a WRONG version: merge first, then count (positions are lost, so it counts pairs in the wrong order)
def wrong_count_after_merge(nums, lo, hi):
    pre = [0] + list(itertools.accumulate(nums)); count = 0
    def sort(a):
        nonlocal count
        if len(a) <= 1: return a
        mid = len(a) // 2; L, R = sort(a[:mid]), sort(a[mid:])
        merged = sorted(L + R)                           # merge first ...
        x = y = 0
        for v in L:                                      # ... then the pointers see a mixed list
            while x < len(merged) and merged[x] - v < lo: x += 1
            while y < len(merged) and merged[y] - v <= hi: y += 1
            count += y - x
        return merged
    sort(pre); return count

# ---- examples
assert count_range_sum([-2, 5, -1], -2, 2) == 3
assert count_range_sum([0], 0, 0) == 1
assert count_range_sum([1, 2, 3], 3, 5) == 3
print('examples ok:', count_range_sum([-2, 5, -1], -2, 2), count_range_sum([0], 0, 0), count_range_sum([1, 2, 3], 3, 5))

# ---- seeded random cross-check against the O(n^2) double loop (and the bisect method)
for _ in range(3000):
    n = random.randint(1, 12); m = random.choice([1, 3, 10])
    nums = [random.randint(-m, m) for _ in range(n)]
    lo = random.randint(-3 * m, 3 * m); hi = lo + random.randint(0, 4 * m)
    r = count_range_sum(nums, lo, hi)
    assert r == brute(nums, lo, hi) == with_bisect(nums, lo, hi), (nums, lo, hi)
print('3000 random cases: merge-sort count == double loop == bisect count')
wrong = 0
for _ in range(500):
    nums = [random.randint(-5, 5) for _ in range(random.randint(2, 8))]
    lo = random.randint(-6, 3); hi = lo + random.randint(0, 6)
    wrong += wrong_count_after_merge(nums, lo, hi) != brute(nums, lo, hi)
print('counting AFTER the merge was wrong on', wrong, 'of 500 random cases')

# ---- maximum size: n = 50000, values up to 1e9, bounds up to 1e14
nums = [random.randint(-10**9, 10**9) for _ in range(50000)]
t = time.perf_counter(); r = count_range_sum(nums, -10**14, 10**14); dt = time.perf_counter() - t
assert r == 50000 * 50001 // 2                         # every subarray sum is within +-5*10^13, so all pairs count
t = time.perf_counter(); r2 = count_range_sum(nums, 10**14 - 1, 10**14); dt2 = time.perf_counter() - t
assert r2 == 0
r3 = count_range_sum(nums, -10**9, 10**9); assert r3 == with_bisect(nums, -10**9, 10**9)
print('n = 50000:', r, 'pairs counted (all of them, the bounds cover every sum); a window above every sum counts', r2, '; (sandbox timing) about %.2f s' % dt)
print('window [-1e9, 1e9] on the same 50000 values:', r3, '(agrees with the bisect method)')

# ---- edge asserts
assert count_range_sum([5], 6, 7) == 0 and count_range_sum([5], 5, 5) == 1
assert count_range_sum([0, 0, 0], 0, 0) == 6            # all 3 + 2 + 1 subarrays have sum 0
assert count_range_sum([-1, -1], -2, -1) == 3
assert count_range_sum([1, -1, 1], 0, 0) == 2          # [1, -1] and [-1, 1]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: 3 1 3
3000 random cases: merge-sort count == double loop == bisect count
counting AFTER the merge was wrong on 385 of 500 random cases
n = 50000: 1250025000 pairs counted (all of them, the bounds cover every sum); a window above every sum counts 0 ; (sandbox timing) about 0.19 s
window [-1e9, 1e9] on the same 50000 values: 26095082 (agrees with the bisect method)
edge asserts ok
```

**Edge cases:**
- Single element: prefix sums are [0, x]; the only pair is (pre[0], pre[1]), so nums = [0] with lo = hi = 0 gives 1.
- All zeros with [0, 0]: all 6 subarrays of three zeros count.
- lo = hi: exact sum counting.
- Bounds wider than any sum: every one of n(n+1)/2 pairs counts (1250025000 for n = 50000).
- Negative values: the prefix sums are not monotone, which is why a sort (not a plain two-pointer scan) is needed.

**Follow-ups:**
- Why not a sliding window? Negative numbers break monotonicity (Part 1 Q13 uses a hash map for equality, here we need a range).
- Can I use a sorted list with bisect for the same count? Yes (the code does, as a cross-check): bisect over earlier prefix sums, O(n) per insert on a list, so O(n^2) in the worst case without a balanced structure.
- What if you needed pairs counted only for exact equality? Hash map of prefix counts, O(n) (Part 1 Q13).

**Common mistakes:**
- Merging before counting.
- Counting empty subarrays, that is pairing pre[a] with itself (sum 0): the merge sort never does this because it counts only pairs split across halves, but a hand-written double loop over prefix sums can.
- Resetting the pointers for each v instead of moving them forward (turns O(n log n) into O(n^2)).
- Using `<` instead of `<=` at the upper bound (the range is inclusive on both ends).

---

### Q48 ⭐ 🔴 Add one to many rectangles with a 2D difference array. `n` is an integer with 1 <= n <= 500 and `queries` has up to 10^4 items [r1, c1, r2, c2] with 0 <= r1 <= r2 < n and 0 <= c1 <= c2 < n. Start from an n x n matrix of zeros; each query adds 1 to every cell of the rectangle with corners (r1, c1) and (r2, c2), both included. Return the final matrix. Use a (n + 1) x (n + 1) difference matrix: `d[r1][c1] += 1`, `d[r1][c2 + 1] -= 1`, `d[r2 + 1][c1] -= 1`, `d[r2 + 1][c2 + 1] += 1`, then take a running sum along every row and then along every column; the total time is O(n^2 + len(queries)). Explain why the four corner updates turn into exactly the rectangle after the two prefix passes (the 2D analogue of the 1D range-add trick), why the order of the two passes does not matter, and compare with O(len(queries) * n^2) direct updates. In the answer include a dry run on the first example and a seeded random cross-check of your solution against applying every rectangle cell by cell on small inputs. Example: n=3, queries=[[1, 1, 2, 2], [0, 0, 1, 1]] -> [[1, 1, 0], [1, 2, 1], [0, 1, 1]]; n=2, queries=[[0, 0, 1, 1]] -> [[1, 1], [1, 1]]; n=1, queries=[] -> [[0]].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)
**Pattern:** 2D difference array: record only the four corners of each rectangle, then recover the matrix with prefix sums. It is the 2D version of the 1D range-add trick (add at l, subtract at r + 1, then take a running sum).

**Say this first (1 line):** "Instead of touching every cell of every rectangle, I mark four corners in an (n+1) x (n+1) difference matrix, then one running sum along rows and one along columns turns those marks back into the rectangles."

**Brute force:** For each query loop over all its cells and add 1: O(len(queries) * n^2) in the worst case. For n = 500 and 10^4 queries my random test below needs 159,593,686 cell updates (see the output), and the worst case (every query the full matrix) is 10^4 * 250000 = 2.5 * 10^9. Too slow. It is the checker in the code.

**Optimal:**
- Matrix `d` of size (n + 1) x (n + 1), all zeros. For each query: `d[r1][c1] += 1`, `d[r1][c2+1] -= 1`, `d[r2+1][c1] -= 1`, `d[r2+1][c2+1] += 1`. The extra row and column absorb the updates that fall off the edge.
- Row pass: `d[i][j] += d[i][j-1]`. After it, row r1 holds 1 on columns c1..c2 (the +1 starts it, the -1 at c2 + 1 ends it) and row r2 + 1 holds the opposite, -1 on columns c1..c2. All other rows are 0.
- Column pass: `d[i][j] += d[i-1][j]`. The row r1 profile (1 on columns c1..c2) is carried down; at row r2 + 1 the opposite profile cancels it exactly. So the rectangle rows r1..r2 get 1 on columns c1..c2, and everything else is 0.
- Why the order of the two passes does not matter: both passes are linear and the 2D prefix sum is `sum over i' <= i, j' <= j` of d, which does not care in which order the double sum is taken (the code runs both orders and they agree).
- Linearity also gives queries combined: sums of rectangles are the sum of their difference matrices, so overlapping queries just add up.
- Finally drop the extra row and column.

**Complexity:**
- Corner updates O(len(queries)), the two passes O(n^2), so O(n^2 + len(queries)): about 2 * 501^2 + 4 * 10^4 = 542,002 operations for the maximum input.
- Space O(n^2) for the matrix (it is also the output size).
- The direct method is O(len(queries) * n^2) in the worst case.
- Sandbox timing, not proof: about 0.04 s for n = 500 and 10^4 queries.

**Dry run:** n = 3, queries `[1,1,2,2]` and `[0,0,1,1]`. The matrix `d` has 4 x 4 cells.
Corner marks after both queries:
| | c0 | c1 | c2 | c3 |
|---|---|---|---|---|
| r0 | 1 | 0 | -1 | 0 |
| r1 | 0 | 1 | 0 | -1 |
| r2 | -1 | 0 | 1 | 0 |
| r3 | 0 | -1 | 0 | 1 |
Row pass gives rows `[1,1,0,0]`, `[0,1,1,0]`, `[-1,-1,0,0]`, `[0,-1,-1,0]`. Column pass gives rows `[1,1,0,0]`, `[1,2,1,0]`, `[0,1,1,0]`, `[0,0,0,0]`. Drop the last row and column: `[[1,1,0],[1,2,1],[0,1,1]]`. Matches the example.

**Code:**
```python
import random, time
random.seed(48)

# ---- optimal: (n+1) x (n+1) difference matrix, four corner updates per query, then two prefix passes
def add_rectangles(n, queries, rows_first=True):
    d = [[0] * (n + 1) for _ in range(n + 1)]
    for r1, c1, r2, c2 in queries:
        d[r1][c1] += 1; d[r1][c2 + 1] -= 1; d[r2 + 1][c1] -= 1; d[r2 + 1][c2 + 1] += 1
    def rows():
        for i in range(n + 1):
            for j in range(1, n + 1): d[i][j] += d[i][j - 1]
    def cols():
        for j in range(n + 1):
            for i in range(1, n + 1): d[i][j] += d[i - 1][j]
    if rows_first: rows(); cols()
    else: cols(); rows()
    return [row[:n] for row in d[:n]]

# ---- brute force: touch every cell of every rectangle
def brute(n, queries):
    a = [[0] * n for _ in range(n)]
    for r1, c1, r2, c2 in queries:
        for i in range(r1, r2 + 1):
            for j in range(c1, c2 + 1): a[i][j] += 1
    return a

# ---- examples
assert add_rectangles(3, [[1, 1, 2, 2], [0, 0, 1, 1]]) == [[1, 1, 0], [1, 2, 1], [0, 1, 1]]
assert add_rectangles(2, [[0, 0, 1, 1]]) == [[1, 1], [1, 1]]
assert add_rectangles(1, []) == [[0]]
print('examples ok:', add_rectangles(3, [[1, 1, 2, 2], [0, 0, 1, 1]]), add_rectangles(2, [[0, 0, 1, 1]]), add_rectangles(1, []))

# ---- seeded random cross-check against cell-by-cell updates, both pass orders
def rand_query(n):
    r1 = random.randrange(n); r2 = random.randint(r1, n - 1); c1 = random.randrange(n); c2 = random.randint(c1, n - 1)
    return [r1, c1, r2, c2]
for _ in range(2000):
    n = random.randint(1, 8); qs = [rand_query(n) for _ in range(random.randint(0, 10))]
    want = brute(n, qs)
    assert add_rectangles(n, qs, True) == want and add_rectangles(n, qs, False) == want
print('2000 random cases: difference matrix == cell-by-cell, and rows-first == columns-first')

# ---- the single-corner picture: one rectangle leaves exactly the rectangle after the passes
n = 6
for _ in range(200):
    q = rand_query(n); m = add_rectangles(n, [q])
    r1, c1, r2, c2 = q
    assert all(m[i][j] == (1 if r1 <= i <= r2 and c1 <= j <= c2 else 0) for i in range(n) for j in range(n))
print('one rectangle at a time: the matrix is 1 inside and 0 outside, 200 cases')

# ---- maximum size: n = 500, 10^4 queries; count the work instead of running the brute force
n = 500; qs = [rand_query(n) for _ in range(10000)]
cells = sum((r2 - r1 + 1) * (c2 - c1 + 1) for r1, c1, r2, c2 in qs)
t = time.perf_counter(); res = add_rectangles(n, qs); dt = time.perf_counter() - t
assert sum(map(sum, res)) == cells                     # the total added equals the total area of all rectangles
ops_fast = 4 * len(qs) + 2 * (n + 1) ** 2
print('n = 500, 10000 random rectangles: cell updates by brute force =', cells, '; difference-matrix operations about', ops_fast)
print('(sandbox timing for the difference matrix: about %.2f s)' % dt)

# ---- edge asserts
assert add_rectangles(3, [[0, 0, 2, 2]]) == [[1] * 3] * 3           # corners on the border: d[n][*] and d[*][n] are written, then dropped
assert add_rectangles(3, [[2, 2, 2, 2]]) == [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
assert add_rectangles(2, [[0, 0, 0, 0]] * 3) == [[3, 0], [0, 0]]    # repeated query
assert add_rectangles(4, [[0, 1, 3, 1]]) == [[0, 1, 0, 0]] * 4      # a full-height column
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[1, 1, 0], [1, 2, 1], [0, 1, 1]] [[1, 1], [1, 1]] [[0]]
2000 random cases: difference matrix == cell-by-cell, and rows-first == columns-first
one rectangle at a time: the matrix is 1 inside and 0 outside, 200 cases
n = 500, 10000 random rectangles: cell updates by brute force = 159593686 ; difference-matrix operations about 542002
(sandbox timing for the difference matrix: about 0.04 s)
edge asserts ok
```

**Edge cases:**
- A rectangle that touches the last row or column: the "- 1" marks land in row n or column n, which exist only for this purpose.
- A single cell: all four marks close together.
- No queries: all zeros.
- Repeated identical queries: the marks add up (3 stays 3).
- n = 1.

**Follow-ups:**
- What if updates and reads interleave? Then a difference array does not work (reads need the prefix sums); use a 2D Fenwick tree (Part 14).
- What if the added value is v instead of 1? Add v and -v at the corners.
- How is this related to the 2D range sum query? It is the inverse operation: prefix sum answers many rectangle reads after a static build; the difference array handles many rectangle writes before one read.

**Common mistakes:**
- Using an n x n difference matrix and then going out of range at c2 + 1 or r2 + 1.
- Taking the prefix sum of only one direction.
- Putting the - marks at (r2, c2 + 1) instead of (r2 + 1, c2 + 1).
- Applying the prefix passes after reading values (they are destructive, so work on a copy if you need the marks again).

---

### Q49 ⭐ 🔴 Rotate every layer of a matrix counter-clockwise (a classic from an online coding platform). `matrix` is an m x n list of lists of integers with 2 <= m, n <= 300 and min(m, n) even, and `r` is an integer with 0 <= r <= 10^9. Think of the matrix as nested rectangular rings (the outer ring is layer 0; because min(m, n) is even every layer is a real ring). Rotate each ring r times by one position counter-clockwise (every value moves one step along its ring in the counter-clockwise direction per rotation), the rings independently, and return the new matrix. For the 4 x 4 matrix of 1..16 and r = 2 the result is [[3,4,8,12],[2,11,10,16],[1,7,6,15],[5,9,13,14]]. List the cells of a ring clockwise starting at its top-left corner; the ring of length L rotated r times counter-clockwise puts the value of ring position idx at position (idx - r) mod L; reduce r modulo L first, since r can be 10^9 while a ring has at most 2 * (m + n) - 4 cells. Explain why you must not simulate r single steps, the O(m * n) total time, and why odd min(m, n) (a middle row or column that is not a ring) is excluded. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a deque rotation of each ring with positions taken independently on small inputs. Example: matrix=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], r=2 -> [[3, 4, 8, 12], [2, 11, 10, 16], [1, 7, 6, 15], [5, 9, 13, 14]]; matrix=[[1, 2], [3, 4]], r=1 -> [[2, 4], [1, 3]]; matrix=[[1, 2, 3, 4], [5, 6, 7, 8]], r=3 -> [[4, 8, 7, 6], [3, 2, 1, 5]].
**Asked at:** HackerRank matrix-layer-rotation problem (snippets of third-party solution write-ups; the HackerRank page itself returned only a login notice, not opened) | Matrix coding-question lists and guides (Educative matrix questions blog, Techie Delight matrix list, talentd.in matrix topic pages, labuladong matrix-traversal notes; search snippets only, not opened)
**Pattern:** Layer-by-layer matrix traversal: unroll each ring into a flat list, rotate the list with modular arithmetic, write it back. Reduce r modulo the ring length first.

**Say this first (1 line):** "Each ring is an independent cycle; I list its cells clockwise from the top-left, and rotating it counter-clockwise r times just means the value at position idx + r (mod L) lands on idx, so there is no need to simulate r steps."

**Brute force:** Rotate every ring one step, r times. With r up to 10^9 and 90,000 cells that is far too slow. It stays in the code as a checker for small r (r <= 40), next to a second independent version that finds ring cells by walking with direction vectors and rotates with `collections.deque`.

**Optimal:**
- Layers `k = 0 .. min(m, n) // 2 - 1`. Ring k has top row k, bottom row m-1-k, left column k, right column n-1-k.
- Cells clockwise from the top-left corner: top row left to right; right column downwards (excluding the corner already listed); bottom row right to left (excluding the corner); left column upwards (excluding both corners). Ring length `L = 2 * (h + w) - 4` with h, w the ring's height and width.
- Counter-clockwise by one step: every value moves to the previous position in the clockwise list. After r steps the value from position idx lands at `(idx - r) mod L`, equivalently the new value at position p is the old value at `(p + r) mod L`.
- `r % L` first: r can be 10^9, the ring has at most 2 * (300 + 300) - 4 = 1196 cells, and a rotation by L is the identity (checked).
- Rings are independent and every cell is in exactly one ring when min(m, n) is even (checked for all 2 <= m, n <= 10).
- Why odd min(m, n) is excluded: the innermost layer is then a single row or a single column (or one cell), not a cycle. The ring generator lists the same cell twice there (`[(1, 1), (1, 2), (1, 1)]` for 3 x 4), so "move one step along the ring" has no clear meaning. The question avoids that case.

**Complexity:**
- Each cell is read and written once: O(m * n) time, independent of r. The modulo is O(1) per ring. Extra space O(m * n) for the output copy plus O(L) for one ring's values.
- Simulating steps would cost O(r * m * n).
- Sandbox timing, not proof: about 0.02 s for 300 x 300 with r = 10^9.

**Dry run:** the 4 x 4 matrix of 1..16 with r = 2.
- Ring 0, clockwise from the top-left: `1 2 3 4 8 12 16 15 14 13 9 5`, L = 12, shift 2. New value at position p = old value at p + 2: `3 4 8 12 16 15 14 13 9 5 1 2`. Written back in the same cell order: top row `3 4 8 12`, then (1,3) = 16, (2,3) = 15, (3,3) = 14, then the bottom row right to left (3,2) = 13, (3,1) = 9, (3,0) = 5, then going up (2,0) = 1, (1,0) = 2.
- Ring 1: `6 7 11 10`, L = 4, shift 2: `11 10 6 7` at cells (1,1), (1,2), (2,2), (2,1).
- Result: row 0 `[3, 4, 8, 12]`, row 1 `[2, 11, 10, 16]`, row 2 `[1, 7, 6, 15]`, row 3 `[5, 9, 13, 14]`. It matches the given result.

**Code:**
```python
import random, collections, time
random.seed(49)

# ---- optimal: cells of each ring in clockwise order from the top-left corner, rotate the flat list by r % L
def ring_cells(m, n, k):
    t, b, l, r = k, m - 1 - k, k, n - 1 - k
    return ([(t, j) for j in range(l, r + 1)] + [(i, r) for i in range(t + 1, b + 1)]
            + [(b, j) for j in range(r - 1, l - 1, -1)] + [(i, l) for i in range(b - 1, t, -1)])

def rotate_layers(matrix, r):
    m, n = len(matrix), len(matrix[0]); out = [row[:] for row in matrix]
    for k in range(min(m, n) // 2):
        cells = ring_cells(m, n, k); L = len(cells)
        vals = [matrix[i][j] for i, j in cells]; s = r % L
        for idx, (i, j) in enumerate(cells):
            out[i][j] = vals[(idx + s) % L]        # the value at position idx + s moves to position idx
    return out

# ---- independent check 1: ring positions found by WALKING (direction vectors), values rotated with a deque
def rotate_walk(matrix, r):
    m, n = len(matrix), len(matrix[0]); out = [row[:] for row in matrix]
    for k in range(min(m, n) // 2):
        h, w = m - 2 * k, n - 2 * k; L = 2 * (h + w) - 4
        pos = []; i = j = k
        for di, dj, steps in ((0, 1, w - 1), (1, 0, h - 1), (0, -1, w - 1), (-1, 0, h - 1)):
            for _ in range(steps): pos.append((i, j)); i += di; j += dj
        assert len(pos) == L and len(set(pos)) == L and (i, j) == (k, k)
        dq = collections.deque(matrix[a][b] for a, b in pos); dq.rotate(-(r % L))   # counter-clockwise by r
        for (a, b), v in zip(pos, dq): out[a][b] = v
    return out

# ---- independent check 2: simulate r single steps (only for small r)
def rotate_steps(matrix, r):
    cur = [row[:] for row in matrix]
    for _ in range(r): cur = rotate_layers(cur, 1)
    return cur

# ---- examples
g4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
assert rotate_layers(g4, 2) == [[3, 4, 8, 12], [2, 11, 10, 16], [1, 7, 6, 15], [5, 9, 13, 14]]
assert rotate_layers([[1, 2], [3, 4]], 1) == [[2, 4], [1, 3]]
assert rotate_layers([[1, 2, 3, 4], [5, 6, 7, 8]], 3) == [[4, 8, 7, 6], [3, 2, 1, 5]]
print('examples ok:', rotate_layers(g4, 2), rotate_layers([[1, 2], [3, 4]], 1), rotate_layers([[1, 2, 3, 4], [5, 6, 7, 8]], 3))

# ---- seeded random cross-check: walk + deque version, and single-step simulation for r <= 40
def rand_grid(m, n): return [[random.randint(0, 99) for _ in range(n)] for _ in range(m)]
for _ in range(1500):
    m, n = random.randint(2, 9), random.randint(2, 9)
    while min(m, n) % 2: m, n = random.randint(2, 9), random.randint(2, 9)
    g = rand_grid(m, n); r = random.choice([0, 1, 2, 3, 7, 40, random.randint(0, 10**9)])
    a = rotate_layers(g, r); assert a == rotate_walk(g, r)
    if r <= 40: assert a == rotate_steps(g, r)
print('1500 random even-min grids: flat-list rotation == walk + deque == r single steps (r <= 40)')

# ---- structural claims, checked
for m in range(2, 11):
    for n in range(2, 11):
        if min(m, n) % 2: continue
        cells = [c for k in range(min(m, n) // 2) for c in ring_cells(m, n, k)]
        assert len(cells) == m * n == len(set(cells))                        # the rings partition the matrix exactly
print('even min(m, n): rings cover every cell of every grid with 2 <= m, n <= 10 exactly once')
dup = ring_cells(3, 4, 1)
print('odd min (3 x 4): layer 1 is a single row; the generator lists', dup, '-> the cell (1, 1) appears twice, so it is not a ring')
g = rand_grid(6, 4); L = 2 * (6 + 4) - 4
assert rotate_layers(g, L * 5) == g and rotate_layers(rotate_layers(g, 3), 4) == rotate_layers(g, 7)
print('rotating by the ring length is the identity; rotating by 3 then 4 equals rotating by 7 (ring lengths differ per layer: here 16 and 8)')

# ---- maximum size, r = 10^9: never simulate r steps
big = [[i * 300 + j for j in range(300)] for i in range(300)]
t = time.perf_counter(); res = rotate_layers(big, 10**9); dt = time.perf_counter() - t
assert sorted(v for row in res for v in row) == list(range(90000))
print('300 x 300 with r = 10^9: a permutation of the values, rings of length 1196 down to 4 (sandbox timing about %.2f s)' % dt)

# ---- edge asserts
assert rotate_layers([[1, 2], [3, 4]], 0) == [[1, 2], [3, 4]]
assert rotate_layers([[1, 2], [3, 4]], 4) == [[1, 2], [3, 4]]
assert rotate_layers([[1, 2], [3, 4], [5, 6], [7, 8]], 1) == [[2, 4], [1, 6], [3, 8], [5, 7]]
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: [[3, 4, 8, 12], [2, 11, 10, 16], [1, 7, 6, 15], [5, 9, 13, 14]] [[2, 4], [1, 3]] [[4, 8, 7, 6], [3, 2, 1, 5]]
1500 random even-min grids: flat-list rotation == walk + deque == r single steps (r <= 40)
even min(m, n): rings cover every cell of every grid with 2 <= m, n <= 10 exactly once
odd min (3 x 4): layer 1 is a single row; the generator lists [(1, 1), (1, 2), (1, 1)] -> the cell (1, 1) appears twice, so it is not a ring
rotating by the ring length is the identity; rotating by 3 then 4 equals rotating by 7 (ring lengths differ per layer: here 16 and 8)
300 x 300 with r = 10^9: a permutation of the values, rings of length 1196 down to 4 (sandbox timing about 0.01 s)
edge asserts ok
```

**Edge cases:**
- r = 0 or r a multiple of every ring length: the matrix is unchanged.
- 2 x 2: one ring of 4 cells.
- A thin matrix such as 4 x 2 or 2 x 4: min is 2, one ring that is the whole matrix (L = 8).
- Different rings have different lengths, so r % L is per ring, not one shift for all.
- Inputs with odd min(m, n) are outside the stated limits.

**Follow-ups:**
- Clockwise instead of counter-clockwise? Use `(idx - s) % L`.
- In place with O(1) extra space? Possible with a reverse trick per ring, but it is fiddly; for an interview a flat list per ring is acceptable.
- How is this different from rotating the whole matrix by 90 degrees? That is transpose plus reverse and moves whole rows; this rotates each ring along itself by a few steps.

**Common mistakes:**
- Simulating r single steps.
- Reducing r modulo the matrix size or one common length instead of per ring.
- Listing the corner cells twice when walking the ring.
- Rotating in the wrong direction (check the 2 x 2 example).
- Reading values from a matrix that you are already overwriting (the code reads from the original and writes to a copy).

---

### Q50 ⭐ 🔴 Maximum gap in linear time. `nums` has 0 <= len <= 10^5 integers with 0 <= value <= 10^9. Return the largest difference between two consecutive elements of the SORTED list (0 if len < 2, and 0 if all values are equal), in O(n) time without a comparison sort. Use the pigeonhole idea: with lo = min, hi = max and n items there are n - 1 gaps that sum to hi - lo, so the maximum gap is at least ceil((hi - lo) / (n - 1)); split the range into buckets of size `max(1, (hi - lo) // (n - 1))`, keep only the minimum and maximum of each non-empty bucket, and the answer is the largest `min(next non-empty bucket) - max(previous non-empty bucket)`. Explain why the maximum gap can never lie inside a single bucket, why storing only min and max per bucket is enough, and why this beats an O(n log n) sort for large n (radix sort with the counting passes of Q37 is the other linear answer). In the answer include a dry run on the first example and a seeded random cross-check of your solution against sorted() and adjacent differences on small inputs. Example: nums=[3, 6, 9, 1] -> 3; nums=[10] -> 0; nums=[5, 5, 5] -> 0; nums=[1, 10000000] -> 9999999.
**Asked at:** Sorting interview guides (techinterview.org sorting-algorithm posts, Techie Delight sorting list, GeeksforGeeks sorting problems page; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)
**Pattern:** Pigeonhole bucketing: if the answer is at least some bound g, buckets narrower than g cannot contain the answer inside them, so only bucket boundaries matter. It beats comparison sorting because the lower bound in Q46 does not apply to bucket and radix methods.

**Say this first (1 line):** "With n values spread over a range hi - lo there are n - 1 gaps adding up to hi - lo, so some gap is at least ceil((hi - lo) / (n - 1)); I use buckets slightly narrower than that, so the biggest gap must cross a bucket boundary, and I only need the min and max of each bucket."

**Brute force:** `sorted(nums)` and the maximum of adjacent differences: O(n log n) time. It is what the code uses as the checker.

**Optimal:**
- n < 2 or all values equal: return 0.
- `lo, hi = min, max`; bucket width `size = max(1, (hi - lo) // (n - 1))`; bucket index `(v - lo) // size`; number of buckets `(hi - lo) // size + 1`.
- Keep only the minimum and maximum of each bucket. Scan the buckets in order: for each non-empty bucket, candidate gap = its min minus the max of the previous non-empty bucket. Answer = the largest candidate.
- Why the maximum gap is never inside a bucket: the n - 1 gaps sum to hi - lo, so the largest is at least ceil((hi - lo) / (n - 1)) >= size. Two values in the same bucket differ by at most size - 1, which is smaller than that gap. (Checked exhaustively on 66,384 small lists, including that every pair achieving the maximum gap straddles two buckets.)
- Why min and max are enough: a gap that crosses buckets starts at the largest value of some bucket and ends at the smallest value of the next non-empty one, because everything else in those buckets lies between them and would split the gap. Empty buckets in between make the gap longer; skipping them handles that.
- Why width is at least 1: if hi - lo < n - 1 then (hi - lo) // (n - 1) is 0; the `max(1, ...)` gives one bucket per value, and then the answer is found by the same scan.
- Bucket count: at most 2n (asserted exhaustively for small lists; with width 1 it is hi - lo + 1 <= 2(n - 1), and it was 100000 buckets for n = 10^5 in the run), so space is O(n).
- Compared with sorting: this is O(n) in the number of operations (no comparison sort, so no n log n lower bound). Radix sort with the counting passes of Q37 is the other linear answer. In CPython practice the C-level `sorted` is very fast, and in my run the two took about the same time at n = 10^5, so the claim here is about complexity, not about speed.

**Complexity:**
- Time O(n): one pass for min and max, one to fill buckets, one over at most 2n buckets.
- Space O(n) for the two bucket arrays.
- Python ints have no overflow, values up to 10^9 and differences fit anyway.
- Sandbox timing, not proof: about 0.02 s for each method at n = 10^5 (see the output; it varies from run to run).

**Dry run:** nums = [3, 6, 9, 1].
- n = 4, lo = 1, hi = 9, range 8, n - 1 = 3 gaps, so some gap is at least ceil(8 / 3) = 3. Width = 8 // 3 = 2, buckets = 8 // 2 + 1 = 5.
- Bucket index (v - 1) // 2: 1 -> 0, 3 -> 1, 6 -> 2, 9 -> 4, bucket 3 is empty.
- Scan: bucket 0 (min 1, max 1), bucket 1 (3): gap 3 - 1 = 2, bucket 2 (6): gap 6 - 3 = 3, bucket 3 empty, bucket 4 (9): gap 9 - 6 = 3. Answer 3.

**Code:**
```python
import random, itertools, time, math
random.seed(50)

# ---- optimal: bucket by value, keep min and max per bucket, scan the buckets once
def max_gap(nums):
    n = len(nums)
    if n < 2: return 0
    lo, hi = min(nums), max(nums)
    if lo == hi: return 0
    size = max(1, (hi - lo) // (n - 1))               # bucket width: never above the guaranteed minimum gap
    nb = (hi - lo) // size + 1
    mins = [None] * nb; maxs = [None] * nb
    for v in nums:
        b = (v - lo) // size
        if mins[b] is None or v < mins[b]: mins[b] = v
        if maxs[b] is None or v > maxs[b]: maxs[b] = v
    best = 0; prev_max = None
    for b in range(nb):
        if mins[b] is None: continue                   # empty bucket: skip it, the gap spans over it
        if prev_max is not None: best = max(best, mins[b] - prev_max)
        prev_max = maxs[b]
    return best

# ---- brute force: comparison sort and adjacent differences
def brute(nums):
    s = sorted(nums)
    return max((y - x for x, y in zip(s, s[1:])), default=0)

# ---- examples
assert max_gap([3, 6, 9, 1]) == 3 and max_gap([10]) == 0 and max_gap([5, 5, 5]) == 0 and max_gap([1, 10000000]) == 9999999
print('examples ok:', max_gap([3, 6, 9, 1]), max_gap([10]), max_gap([5, 5, 5]), max_gap([1, 10000000]))

# ---- seeded random cross-check against sorted()
for _ in range(5000):
    n = random.randint(0, 30); m = random.choice([3, 10, 100, 10**9])
    t = [random.randint(0, m) for _ in range(n)]
    assert max_gap(t) == brute(t), t
print('5000 random lists (n <= 30, values up to 3, 10, 100 or 10^9): equal to sorted() + adjacent differences')

# ---- the pigeonhole claims, checked exhaustively on small inputs: every list of length 2..5 over values 0..8
checked = 0
for n in range(2, 6):
    for t in itertools.product(range(9), repeat=n):
        lo, hi = min(t), max(t)
        if lo == hi: continue
        g = brute(t); size = max(1, (hi - lo) // (n - 1))
        assert g >= -(-(hi - lo) // (n - 1))                                  # max gap >= ceil((hi - lo) / (n - 1))
        assert size - 1 < g                                                   # two values in one bucket differ by at most size - 1 < the max gap
        s = sorted(t)
        for x, y in zip(s, s[1:]):
            if y - x == g: assert (x - lo) // size != (y - lo) // size        # a maximum gap pair never shares a bucket
        assert (hi - lo) // size + 1 <= 2 * n                                 # at most 2n buckets, so O(n) space
        checked += 1
print('exhaustive on', checked, 'lists: max gap >= ceil(range/(n-1)); bucket width - 1 < max gap; every maximum-gap pair straddles buckets; buckets <= 2n')

# ---- bucket count for large n (the 2n bound is checked above only on small lists; here is the actual number)
n = 10**5; big = [random.randint(0, 10**9) for _ in range(n)]
lo, hi = min(big), max(big); size = max(1, (hi - lo) // (n - 1))
print('n = 100000, values up to 10^9: bucket width', size, ', buckets', (hi - lo) // size + 1)
t = time.perf_counter(); r = max_gap(big); t1 = time.perf_counter() - t
t = time.perf_counter(); r2 = brute(big); t2 = time.perf_counter() - t
assert r == r2
print('max gap =', r, '; (sandbox timing, varies run to run) bucket method %.3f s, sorted() + differences %.3f s' % (t1, t2))

# ---- edge asserts
assert max_gap([]) == 0 and max_gap([7]) == 0 and max_gap([1, 1]) == 0
assert max_gap([0, 10**9]) == 10**9 and max_gap([1, 2, 3, 4, 5]) == 1
assert max_gap([1, 3]) == 2 and max_gap([0, 5, 5, 10]) == 5
assert max_gap([0, 1, 100]) == 99 and max_gap([100, 0, 1]) == 99
print('edge asserts ok')
```

**Output (my run):**
```text
examples ok: 3 0 0 9999999
5000 random lists (n <= 30, values up to 3, 10, 100 or 10^9): equal to sorted() + adjacent differences
exhaustive on 66384 lists: max gap >= ceil(range/(n-1)); bucket width - 1 < max gap; every maximum-gap pair straddles buckets; buckets <= 2n
n = 100000, values up to 10^9: bucket width 10000 , buckets 100000
max gap = 130321 ; (sandbox timing, varies run to run) bucket method 0.027 s, sorted() + differences 0.024 s
edge asserts ok
```

**Edge cases:**
- Empty list, single item: 0. Two items: their difference. All equal: 0 (lo == hi would give a zero width).
- Duplicates: they fall into the same bucket and change nothing.
- Range smaller than n - 1 (many repeats): width 1, one bucket per value.
- Huge range with few items: [0, 10^9] has width 10^9 and 2 buckets.
- Unsorted input with the extreme values anywhere: min and max come from the first pass.

**Follow-ups:**
- Can you do it by radix sort? Yes: sort with LSD radix (Q37) in O(d (n + base)) and scan adjacent pairs.
- Does it work for negative numbers? Yes, after shifting by lo (the code already subtracts lo).
- Why not a bucket per value? The range is up to 10^9, too much memory.

**Common mistakes:**
- Taking the difference between neighbours inside a bucket.
- Storing every element per bucket instead of min and max.
- Using a width of 0 when hi - lo < n - 1.
- Forgetting empty buckets, comparing each bucket with the one right before it even if that one is empty.
- Making the width larger than the guaranteed gap (for example 2 * ceil(range / (n - 1))): then the biggest gap can hide inside one bucket.

