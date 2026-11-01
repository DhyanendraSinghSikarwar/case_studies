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
