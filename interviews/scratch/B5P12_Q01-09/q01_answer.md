### Q1 ⭐⭐⭐ 🟢 Single number. `nums` has an odd number of integers (1 <= len <= 10^5, any sign): every value appears exactly twice except one value that appears once. Return that value in O(n) time and O(1) extra space. Explain which three properties of XOR make a plain left-to-right XOR work (a ^ a = 0, a ^ 0 = a, commutative and associative), and why a hash-set or Counter solution is correct but uses O(n) space. Also state why Python needs no masking here (integers are arbitrary precision and negative values XOR correctly). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter-based brute force on small inputs. Example: nums=[6, 3, 9, 3, 6] -> 9; nums=[7] -> 7; nums=[-3, -3, 5] -> 5; nums=[0, 1, 0] -> 1; nums=[-8, 2, 2, -8, -1] -> -1.
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** XOR cancellation (bit manipulation). Pairs cancel, the odd one out is left.

**Say this first (1 line):** "XOR everything. a ^ a = 0 and a ^ 0 = a, XOR is commutative and associative, so every pair cancels and the single value survives. O(n) time, O(1) space."

**Brute force:** Count with a `Counter` (or toggle values in a set) and return the key with count 1. Correct, O(n) time, but O(n) extra space. Sorting and scanning pairs is O(n log n) time.

**Optimal:**
- Keep one running value `x = 0` and do `x ^= v` for every value.
- Three properties make this work:
  - `a ^ a = 0`: two equal values wipe each other out.
  - `a ^ 0 = a`: zero is the identity, so the start value and the cancelled pairs add nothing.
  - Commutative and associative: the order and the grouping do not matter, so we may mentally regroup the list as (all pairs together) ^ (the single one), even though the pairs are not next to each other.
- Result: `(a ^ a) ^ (b ^ b) ^ ... ^ s = 0 ^ ... ^ s = s`.
- Why not masking: Python ints are arbitrary precision. A negative number behaves like an infinite string of leading 1 bits (two's complement), so `-3 ^ -3 == 0` and `-8 ^ 2 ^ 2 == -8` with no overflow and no `& 0xFFFFFFFF`. I ran both on Python 3.13 (output below). In C or Java the same loop works on fixed width; here you simply do not need a mask.

**Complexity:** Time O(n), one pass. Space O(1) (one int; the values are small, so one int is constant size). The hash-set or Counter version is also correct but stores up to about n/2 + 1 distinct values: O(n) space.

**Dry run:** `[6, 3, 9, 3, 6]`. In binary: 6 = 0110, 3 = 0011, 9 = 1001.
- x = 0 ^ 6 = 0110 (6)
- ^ 3 = 0101 (5)
- ^ 9 = 1100 (12)
- ^ 3 = 1111 (15). The 3 came back, so its bits are restored on top of 9 and 6.
- ^ 6 = 1001 (9). Answer 9.

**Code:**
```python
import random
from collections import Counter

random.seed(1201)

def single_xor(nums):
    x = 0
    for v in nums:
        x ^= v          # a ^ a = 0, 0 ^ b = b; order does not matter
    return x

def single_counter(nums):          # brute force: O(n) extra space
    return next(k for k, c in Counter(nums).items() if c == 1)

def single_set(nums):              # another O(n)-space version: toggle membership
    seen = set()
    for v in nums:
        seen.symmetric_difference_update({v})
    return next(iter(seen))

examples = [([6, 3, 9, 3, 6], 9), ([7], 7), ([-3, -3, 5], 5), ([0, 1, 0], 1), ([-8, 2, 2, -8, -1], -1)]
for nums, want in examples:
    got = single_xor(nums)
    assert got == want == single_counter(nums) == single_set(nums)
    print(nums, '->', got)

# dry run trace of the first example
x = 0
for v in [6, 3, 9, 3, 6]:
    x ^= v
    print(f'  x ^= {v:>2} -> {x:>2}  ({x:04b})')

# seeded cross-check: 3000 random inputs, negatives included, big magnitudes included
for _ in range(3000):
    pairs = random.sample(range(-50, 50), random.randint(0, 6))
    odd = random.choice([v for v in range(-60, 60) if v not in pairs] + [10**12, -10**12])
    nums = [odd] + pairs * 2
    random.shuffle(nums)
    assert single_xor(nums) == single_counter(nums) == odd
print('random cross-check ok: 3000 cases')

# Python specifics: no mask needed, negatives XOR like infinite two's complement
assert -3 ^ -3 == 0 and -3 ^ 0 == -3 and (-8 ^ 2) ^ 2 == -8
assert single_xor([-(2**70), 5, 5]) == -(2**70)
print('-8 ^ 2 =', -8 ^ 2, ' (-8 ^ 2) ^ 2 =', (-8 ^ 2) ^ 2)
print('big:', single_xor([2**100, 7, 2**100, 7, -(2**90)]) == -(2**90))
print('edge asserts ok')
```

**Output (my run):**
```
[6, 3, 9, 3, 6] -> 9
[7] -> 7
[-3, -3, 5] -> 5
[0, 1, 0] -> 1
[-8, 2, 2, -8, -1] -> -1
  x ^=  6 ->  6  (0110)
  x ^=  3 ->  5  (0101)
  x ^=  9 -> 12  (1100)
  x ^=  3 -> 15  (1111)
  x ^=  6 ->  9  (1001)
random cross-check ok: 3000 cases
-8 ^ 2 = -6  (-8 ^ 2) ^ 2 = -8
big: True
edge asserts ok
```

**Edge cases:**
- Single element `[7]` returns 7.
- Negatives and zero: `[-3, -3, 5]`, `[0, 1, 0]` (a 0 pair cancels like any other).
- Huge magnitudes (I tested 10**12 and 2**100): no overflow in Python.
- Input is guaranteed to have exactly one single value. If it may have none or two, XOR gives garbage (XOR of the two, see the follow-up).

**Follow-ups:**
- Two single values (Single number III, Q16): XOR gives a ^ b; split by a set bit of it.
- Every value three times except one (Q28): bit-by-bit count mod 3; XOR alone fails.
- Why does a hash set solution not violate the question? It does not: it is correct, only O(n) space. The interviewer asks for O(1).

**Common mistakes:**
- Adding a `& 0xFFFFFFFF` "to be safe" and then returning a large positive number for a negative answer.
- Using `sum(set(nums)) * 2 - sum(nums)`: correct but O(n) space for the set and can be called out; also not an XOR answer.
- Assuming the pairs must be adjacent. XOR does not care about order.
