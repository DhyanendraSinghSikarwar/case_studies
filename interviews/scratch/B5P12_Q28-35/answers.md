### Q28 ⭐ 🟡 Single number II (every other value three times). `nums` has 1 <= len <= 10^4 integers with -2^31 <= value < 2^31: one value appears exactly once and every other value appears exactly three times. Return the single value in O(n) time and O(1) extra space: for each of the 32 bit positions count how many numbers have that bit set, take the count modulo 3 and set the bit of the answer. Because Python integers have no fixed width, you must convert the 32-bit result back to a signed value yourself: if bit 31 is set, subtract 2^32 (show a negative answer and what you would get without this step). Mention the two-register `ones`/`twos` state machine as an alternative and why it needs no sign fix in Python. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter on small inputs. Example: nums=[-5, 7, -5, 7, -5, 7, 9] -> 9; nums=[-8, 3, 3, 3] -> -8; nums=[4] -> 4; nums=[1, 1, 1, -2147483648] -> -2147483648.
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Bit counting with modulo 3 (a 32-column counter), the bit-manipulation relative of "count and take the remainder". Every value outside the single one appears 3 times, so in each bit column the number of 1s from the repeated values is a multiple of 3. What is left over after `% 3` is the single value's bit.

**Say this first (1 line):** "For each of the 32 bit positions I count how many numbers have that bit set, take the count mod 3, and that is the bit of the answer; then I fix the sign by hand because Python has no 32-bit width."

**Brute force:** `Counter(nums)` and return the key whose count is 1. Correct, O(n) time, but O(n) space (about n/3 keys). A sort also works at O(n log n) time. Both break the O(1) space ask.

**Optimal:**
- Column rule: a value that appears 3 times adds 0 or 3 to the count of any column, so it vanishes mod 3. The single value adds 0 or 1. So `count % 3` is exactly its bit.
- For `b` in 0..31: `bit = sum((v >> b) & 1 for v in nums) % 3`; if it is 1, set `1 << b` in `ans`.
- Why `(v >> b) & 1` is safe for negatives: Python's `>>` on a negative int copies the sign bit in from the left, so bit `b` for `b <= 31` is the two's-complement bit of a 32-bit value. Values here are in [-2^31, 2^31), so 32 columns see everything.
- The sign fix (the Python-specific step): `ans` is built only from bits 0..31, so it is a non-negative number in [0, 2^32). If bit 31 is set the true answer is negative: `ans - 2**32`. Without it, `-8` comes back as `4294967288` (observed below, Python 3.13).
- State machine alternative: keep `ones` (bits seen 1 mod 3 times) and `twos` (bits seen 2 mod 3 times). For each `x`: `ones = (ones ^ x) & ~twos`, then `twos = (twos ^ x) & ~ones`. At the end `ones` is the answer. It needs no sign fix in Python because Python ints behave as if sign-extended to infinity: a negative `x` already has infinitely many leading 1s, the update rules act on every column the same way, and the final `ones` is the negative number itself. `~twos` is also fine (it is just `-twos - 1`). The column method builds the answer from 32 bits only, so it is the one that needs the fix.
- Space: O(1) in both (32 counters or two integers).

**Complexity:** Time O(32 * n) = O(n) for the column method (32 passes), O(n) for the state machine (one pass). Space O(1).

**Dry run:** `nums = [-5, 7, -5, 7, -5, 7, 9]`. In 32-bit two's complement `-5` is `...11111011`, `7` is `00000111`, `9` is `00001001`.

| bit | set bits (3 x -5, 3 x 7, 1 x 9) | count | count % 3 |
|---|---|---|---|
| 0 | 3 + 3 + 1 | 7 | 1 |
| 1 | 3 + 3 + 0 | 6 | 0 |
| 2 | 0 + 3 + 0 | 3 | 0 |
| 3 | 3 + 0 + 1 | 4 | 1 |
| 4 | 3 + 0 + 0 | 3 | 0 |
| 31 | 3 + 0 + 0 | 3 | 0 |

(Bits 5 to 30 look like bit 4.) The result has bits 0 and 3 set: `0b1001 = 9`, bit 31 is 0, so no sign change. For `[-8, 3, 3, 3]` the single value is `-8`: it is the only one with bit 31 set, so that column counts 1 (mod 3 = 1) and `ans = 4294967288`; bit 31 is set, so `ans - 2**32 = -8`.

**Code:**
```python
import random
from collections import Counter

random.seed(2801)


def single_count_bits(nums):
    """For each of 32 bit positions count the set bits, mod 3, rebuild, then fix the sign."""
    ans = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3:   # v >> b works for negatives: sign bits are copied in
            ans |= 1 << b
    return ans - (1 << 32) if ans & (1 << 31) else ans   # bit 31 set -> negative in 32-bit two's complement


def no_sign_fix(nums):
    ans = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3:
            ans |= 1 << b
    return ans


def single_ones_twos(nums):
    """Two registers: ones = bits seen 1 mod 3 times, twos = bits seen 2 mod 3 times."""
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones          # Python ints sign-extend forever, so a negative answer is already negative


def brute(nums):
    return next(k for k, c in Counter(nums).items() if c == 1)


# dry run table for the first example
ex = [-5, 7, -5, 7, -5, 7, 9]
print("bit : count of set bits, count mod 3")
for b in (0, 1, 2, 3, 4, 31):
    c = sum((v >> b) & 1 for v in ex)
    print(f"{b:>3} : {c}, {c % 3}")

# the four prompt examples
for nums, want in [([-5, 7, -5, 7, -5, 7, 9], 9), ([-8, 3, 3, 3], -8), ([4], 4), ([1, 1, 1, -2147483648], -2147483648)]:
    got = single_count_bits(nums)
    assert got == single_ones_twos(nums) == brute(nums) == want, (nums, got)
    print(nums, "->", got)

# the sign fix, shown
raw = no_sign_fix([-8, 3, 3, 3])
print("without the fix:", raw, "= 2^32 - 8 =", 2**32 - 8, "| with the fix:", single_count_bits([-8, 3, 3, 3]))
print("bit 31 of the raw result:", (raw >> 31) & 1, "| 0xFFFFFFF8 as binary:", format(raw, "032b"))

# seeded random cross-check against Counter
done = 0
while done < 500:
    k = random.randint(0, 6)
    triples = random.sample(range(-20, 20), k) if random.random() < 0.7 else random.sample([-2**31, 2**31 - 1, -1, 0, 1, 2**30], min(k, 6))
    single = random.choice([v for v in range(-2**31, -2**31 + 3)] + [2**31 - 1, 0, -1, 5, -7])
    if single in triples:
        continue
    nums = [single] + [t for t in triples for _ in range(3)]
    random.shuffle(nums)
    assert single_count_bits(nums) == single_ones_twos(nums) == brute(nums) == single, nums
    done += 1
print("500 seeded random cases ok (extremes -2^31 and 2^31-1 included)")

# edge asserts
assert single_count_bits([2**31 - 1]) == 2**31 - 1
assert single_count_bits([-1, 0, 0, 0]) == -1
assert single_count_bits([-2**31, 5, 5, 5]) == -2**31
assert single_ones_twos([-2**31, 5, 5, 5]) == -2**31
print("edge asserts ok")
```

**Output (my run):**
```
bit : count of set bits, count mod 3
  0 : 7, 1
  1 : 6, 0
  2 : 3, 0
  3 : 4, 1
  4 : 3, 0
 31 : 3, 0
[-5, 7, -5, 7, -5, 7, 9] -> 9
[-8, 3, 3, 3] -> -8
[4] -> 4
[1, 1, 1, -2147483648] -> -2147483648
without the fix: 4294967288 = 2^32 - 8 = 4294967288 | with the fix: -8
bit 31 of the raw result: 1 | 0xFFFFFFF8 as binary: 11111111111111111111111111111000
500 seeded random cases ok (extremes -2^31 and 2^31-1 included)
edge asserts ok
```

**Edge cases:**
- Single element: `[4]` gives 4 (every other column is 0 mod 3 trivially).
- The smallest value `-2**31` as the single: only bit 31 is set, the fix turns `2**31` into `-2**31`. Checked above.
- The largest value `2**31 - 1`: bit 31 is 0, no fix, checked above.
- `-1` as the single (all 32 bits set) returns `-1` after the fix; `0` as the single works because every column then reads `0 mod 3`.
- Values outside the stated range (for example `2**40`) would be silently truncated to 32 columns by the column method. The `ones`/`twos` method would still work. Say that if the interviewer widens the range, loop to the wider bit length.

**Follow-ups:**
- *Every other value appears 5 times, not 3?* Same column method with `% 5`. The state machine needs three registers instead of two (the number of registers is the number of bits in the modulus counter).
- *Why can't plain XOR do this one?* XOR is addition mod 2, so it cancels pairs. Triples need addition mod 3, which is why you count per column.
- *Why does `ones` update before `twos`?* `twos` must see the new `ones`: a bit that just entered `ones` must not also enter `twos`. Swap the order and the machine miscounts.

**Common mistakes:**
- Forgetting the sign fix and returning `4294967288` for `-8`.
- Looping `range(31)` and missing bit 31 (the sign bit).
- Using `& 0xFFFFFFFF` on the input and then doing the fix on the wrong side: mask once, fix once.
- Writing `ones ^= x` and `twos ^= ones` in the wrong order; the order and the `& ~` terms are what make the machine count mod 3.
- Claiming the `Counter` solution is O(1) space.

### Q29 ⭐ 🟡 Sum of two integers without + or -. `a` and `b` are integers with |a|, |b| <= 10^9. Compute a + b using only bitwise operators and shifts, and return `[sum, rounds]`, where `rounds` is how many times this loop body runs: start with `a &= 0xFFFFFFFF; b &= 0xFFFFFFFF` and while `b` is nonzero, replace `(a, b)` by `((a ^ b) & 0xFFFFFFFF, ((a & b) << 1) & 0xFFFFFFFF)`. When the loop ends convert back to a signed value (if `a > 0x7FFFFFFF` the result is `~(a ^ 0xFFFFFFFF)`). Explain what XOR (sum without carry) and AND shifted left (the carries) mean, why the masking is needed in Python (a negative operand has infinitely many leading 1 bits, so without the mask the loop can fail to terminate, for example for a = -1 and b = 1; show that) and why the result fits in 32 bits for this input range (|a + b| <= 2 * 10^9 < 2^31). In the answer include a dry run on the first example and a seeded random cross-check of your solution against a 32-bit ripple-carry adder built from single bits on small inputs. Example: a=7, b=5 -> [12, 3]; a=-3, b=3 -> [0, 32]; a=1000000000, b=1000000000 -> [2000000000, 2]; a=-1000000000, b=-1000000000 -> [-2000000000, 2]; a=0, b=0 -> [0, 0].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Addition as XOR plus a shifted AND (half-adder loop), with explicit 32-bit masking because Python integers have no fixed width.

**Say this first (1 line):** "XOR is the sum without carries, AND shifted left is the carries; repeat until no carry is left, and mask to 32 bits every step because a negative Python int has infinitely many leading 1s."

**Brute force:** A 32-bit ripple-carry adder: walk bits 0..31, compute `sum = x ^ y ^ carry` and `carry = (x & y) | (carry & (x ^ y))` per bit, then convert the 32-bit result back to signed. It is 32 steps always and is the oracle in the code.

**Optimal:**
- Split `a + b` into two parts: `a ^ b` (the sum of each column ignoring carries) and `(a & b) << 1` (the carries, moved one column up). Then `a + b = (a ^ b) + ((a & b) << 1)`. The new problem is the same shape but the carry part moves left every round.
- Loop `while b:` and replace `(a, b)` by `((a ^ b) & M, ((a & b) << 1) & M)` with `M = 0xFFFFFFFF`. Stop when no carry is left; `a` holds the sum.
- Why the mask (Python only): `-1` is `...1111` with infinitely many 1s. For `a = -1, b = 1` the unmasked loop gives `(a, b) = (-2, 2)`, then `(-4, 4)`, then `(-8, 8)`: the carry never dies, it only moves left forever (shown below, stopped after 40 rounds). Masking to 32 bits drops the carry that falls off the top, so it reaches 0 after at most 32 rounds here (`a = -3, b = 3` takes exactly 32).
- Convert back: after the loop `a` is in [0, 2^32). If `a > 0x7FFFFFFF` bit 31 is set and the value is negative: `~(a ^ 0xFFFFFFFF)`. That equals `a - 2**32` (XOR with all ones flips the 32 bits to get the complement, `~` negates it).
- Why the result fits: `|a + b| <= 2 * 10^9 < 2^31 = 2147483648`, so the true sum is representable as a signed 32-bit number and the conversion is exact. For inputs where the sum overflows 32 bits this method would wrap around silently, like C.
- Invariant: `a + b` (as numbers mod 2^32) is the same before and after each round.

**Complexity:** Time O(w) rounds with w = 32 the word width: the lowest set bit of the carry word moves up at least one column every round (the next carry is a subset of the old carry's columns shifted left), and the mask drops anything past bit 31, so after at most 32 rounds the carry is 0. `-3 + 3` reaches 32; the most rounds in my 20,000 random pairs was 18. Space O(1).

**Dry run:** `a = 7 (0111), b = 5 (0101)`.
- Round 1: `a ^ b = 0010 (2)`, `(a & b) << 1 = (0101) << 1 = 1010 (10)`.
- Round 2: `a = 0010, b = 1010`: `a ^ b = 1000 (8)`, `(a & b) << 1 = (0010) << 1 = 0100 (4)`.
- Round 3: `a = 1000, b = 0100`: `a ^ b = 1100 (12)`, `a & b = 0`, so `b = 0`. Stop: `[12, 3]`.

**Code:**
```python
import random

random.seed(2901)
MASK = 0xFFFFFFFF


def add(a, b):
    """a + b with only ^, &, <<. Returns [sum, rounds]. Everything is masked to 32 bits."""
    a &= MASK
    b &= MASK
    rounds = 0
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK   # sum without carry, carries moved one place left
        rounds += 1
    return [a if a <= 0x7FFFFFFF else ~(a ^ MASK), rounds]   # ~(a ^ MASK) == a - 2**32 for bit 31 set


def add_no_mask(a, b, cap=40):
    """The same loop WITHOUT masking: for a = -1, b = 1 it never ends (we stop it after `cap` rounds)."""
    trace = []
    for _ in range(cap):
        if b == 0:
            return a, trace
        a, b = a ^ b, (a & b) << 1
        trace.append((a, b))
    return None, trace


def ripple(a, b):
    """Brute force: a 32-bit ripple-carry adder built from single bits (full adders)."""
    out, carry = 0, 0
    for i in range(32):
        x, y = (a >> i) & 1, (b >> i) & 1
        out |= (x ^ y ^ carry) << i
        carry = (x & y) | (carry & (x ^ y))
    return out - (1 << 32) if out >> 31 else out


# dry run on a = 7, b = 5
a, b, r = 7, 5, 0
while b:
    a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    r += 1
    print(f"round {r}: a = {a:04b} ({a}), b = {b:04b} ({b})")

for (x, y), want in [((7, 5), [12, 3]), ((-3, 3), [0, 32]), ((10**9, 10**9), [2 * 10**9, 2]),
                     ((-10**9, -10**9), [-2 * 10**9, 2]), ((0, 0), [0, 0])]:
    got = add(x, y)
    assert got == want and got[0] == ripple(x, y) == x + y, (x, y, got)
    print(f"add({x}, {y}) -> {got}")

res, trace = add_no_mask(-1, 1)
print("no mask, a=-1, b=1: result after 40 rounds =", res, "| first states (a, b):", trace[:3], "... last b =", trace[-1][1])

# seeded random cross-check against the ripple-carry adder (sum only) and against +
mx = 0
for _ in range(20000):
    x, y = random.randint(-10**9, 10**9), random.randint(-10**9, 10**9)
    s, rounds = add(x, y)
    assert s == ripple(x, y) == x + y
    mx = max(mx, rounds)
for x in range(-70, 71):
    for y in range(-70, 71):
        assert add(x, y)[0] == ripple(x, y) == x + y
print("20000 random + 141*141 small pairs ok; most rounds seen in the random run:", mx)
assert 2 * 10**9 < 2**31
assert add(10**9, 10**9)[0] == 2 * 10**9 and add(-1, 1) == [0, 32]
print("edge asserts ok")
```

**Output (my run):**
```
round 1: a = 0010 (2), b = 1010 (10)
round 2: a = 1000 (8), b = 0100 (4)
round 3: a = 1100 (12), b = 0000 (0)
add(7, 5) -> [12, 3]
add(-3, 3) -> [0, 32]
add(1000000000, 1000000000) -> [2000000000, 2]
add(-1000000000, -1000000000) -> [-2000000000, 2]
add(0, 0) -> [0, 0]
no mask, a=-1, b=1: result after 40 rounds = None | first states (a, b): [(-2, 2), (-4, 4), (-8, 8)] ... last b = 1099511627776
20000 random + 141*141 small pairs ok; most rounds seen in the random run: 18
edge asserts ok
```

**Edge cases:**
- `a = 0, b = 0`: no round at all, `[0, 0]`.
- `a = -b` (for example `-3 + 3`): the carry runs all the way off the top, 32 rounds, result 0.
- Both negative (`-10^9 + -10^9`): `a` ends above `0x7FFFFFFF`, the conversion gives `-2000000000`.
- Same-sign large values (`10^9 + 10^9`): the sum `2000000000` stays under `0x7FFFFFFF`, no conversion.
- Subtraction: negate with `~b + 1`, then add. Mask it too.

**Follow-ups:**
- *Do it recursively?* `add(a ^ b, (a & b) << 1)` with the same masking; the recursion depth is at most the number of rounds (32), safe under the default limit.
- *Multiply without `*`?* Shift-and-add over the bits of one operand, using this adder.
- *Why not just use `a + b`?* The question is about what carries are, and about Python's missing fixed width.

**Common mistakes:**
- No mask: infinite loop on negative operands, as shown above.
- Masking `a` and `b` at the start but not inside the loop (the shifted carry grows past 32 bits again).
- Converting with `a - 2**32` only when `a > 2**31` (off by one: bit 31 set means `a >= 2**31`, which is `a > 0x7FFFFFFF`).
- Writing `a & b << 1` without brackets: `<<` binds tighter than `&`.

### Q30 ⭐ 🟡 Enumerate subsets with a bitmask, and submasks. `items` has 0 <= len <= 12 distinct integers (any sign, |value| <= 100) and `target` is an integer. Using the mask `m` in 0..2^n - 1 where bit i means 'take items[i]', return `[found, pairs]`: `found` is the list of all subsets (each a list in the order of `items`) whose sum equals `target`, listed in increasing order of the mask value (so the empty subset, mask 0, comes first when target is 0); `pairs` is the number of (mask, submask) pairs visited when, for every mask m, you loop `sub = m; while sub: ...; sub = (sub - 1) & m` (non-empty submasks only). Explain why `(sub - 1) & m` visits every non-empty submask of `m` exactly once in decreasing order, and why `pairs` equals 3^n - 2^n (each item is in the submask, in the mask but not the submask, or in neither; subtract the empty submask of every mask). Say when a bitmask is better than recursion (small n, set as an integer, fast union and test) and when it is not. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a loop over all subsets using list slicing logic and a double loop testing `s & m == s` on small inputs. Example: items=[3, 1, 4, 2], target=5 -> [[[1, 4], [3, 2]], 65]; items=[], target=0 -> [[[]], 0]; items=[1, -1, 2], target=0 -> [[[], [1, -1]], 19]; items=[5], target=3 -> [[], 1].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** Bitmask enumeration of subsets (mask bit i = take item i) and the submask loop `sub = (sub - 1) & m`. The loop that makes subset DP over masks 3^n instead of 4^n.

**Say this first (1 line):** "Every integer m in 0..2^n - 1 is a subset; bit i says take item i. To list the subsets of a subset, step `sub = (sub - 1) & m`, which visits each non-empty submask once, biggest first."

**Brute force:** For every mask, build the subset with list logic and sum it (`2^n * n`). For the pair count, a double loop over all `m` and all `s` testing `s & m == s` is `4^n` steps. Both are the oracle in the code (n <= 7 there).

**Optimal:**
- Subsets: for `mask` in `range(1 << n)`, collect `items[i]` where `mask >> i & 1`; keep the list if the sum is `target`. Increasing mask order is the output order required: mask 0 (the empty subset) first, and a subset using a higher-index item comes later than any subset using only lower-index items. Cost O(2^n * n), at most 4096 * 12 steps here.
- Submasks: start with `sub = m`, loop `while sub:`, then `sub = (sub - 1) & m`.
- Why it visits every non-empty submask once, in decreasing order: let `p` be the lowest set bit of `sub`. `sub - 1` clears bit `p` and sets every bit below it; AND with `m` keeps only allowed bits. So `(sub - 1) & m` agrees with `sub` above `p`, has 0 at `p`, and has every bit of `m` that lies below `p`. It is smaller than `sub`, and any other submask of `m` that is smaller than `sub` must first differ from `sub` at bit `p` or above (below `p` `sub` has only zeros, so a difference there would make it bigger), so it cannot exceed this number. Hence it is the next smaller submask: the sequence strictly decreases through every submask and ends at 0, where the loop stops. (The code also checks this for every `m < 256`.)
- Why `pairs = 3^n - 2^n`: for a pair `(mask, sub)` with `sub` inside `mask`, each item is in `sub`, or in `mask` but not in `sub`, or in neither: 3 choices, so `3^n` pairs including the empty submask; the empty submask is excluded for each of the `2^n` masks. For n = 12 that is 531,441 - 4,096 = 527,345 (the code runs the real loop for n = 0..12 and checks).
- Bitmask versus recursion: a mask is great when n is small (<= about 20), the set is an integer, so union is `|`, intersection `&`, membership `mask >> i & 1`, and it is a key for a DP array or a dict. It is not great when n is large (2^n states), when you need pruning (a recursion can stop early; a plain mask loop cannot), or when the items are not a small fixed list.
- Negatives and zero are fine here: no bit trick touches the item values, only the mask integers, which are non-negative, so Python's unbounded negative integers never matter in this question.

**Complexity:** Subsets: time O(2^n * n), space O(output). Submask pair loop: time and count exactly 3^n - 2^n (about 5.3 * 10^5 for n = 12). Not polynomial: that is the nature of the problem, not of the code.

**Dry run:** `items = [3, 1, 4, 2], target = 5`. Bit 0 = item 3, bit 1 = item 1, bit 2 = item 4, bit 3 = item 2. Masks with sum 5: `0110` (6) takes items 1 and 4, sum 5; `1001` (9) takes 3 and 2, sum 5. Increasing order gives `[[1, 4], [3, 2]]`. The pair count is `3^4 - 2^4 = 81 - 16 = 65`. For the submask loop on `m = 1011`: `1011, 1010, 1001, 1000, 0011, 0010, 0001`, then `sub = 0001 - 1 = 0000`, stop. That is 7 = 2^3 - 1 non-empty submasks (decreasing, each once).

**Code:**
```python
import random

random.seed(3001)


def solve(items, target):
    n = len(items)
    found = []
    for mask in range(1 << n):                       # increasing mask order
        total = 0
        for i in range(n):
            if mask >> i & 1:                        # bit i set = take items[i]
                total += items[i]
        if total == target:
            found.append([items[i] for i in range(n) if mask >> i & 1])
    pairs = 0
    for mask in range(1 << n):
        sub = mask
        while sub:                                   # non-empty submasks only
            pairs += 1
            sub = (sub - 1) & mask                   # next smaller submask of mask
    return [found, pairs]


def brute(items, target):
    n = len(items)
    all_subsets = [[items[i] for i in range(n) if (m >> i) % 2 == 1] for m in range(1 << n)]
    found = [s for s in all_subsets if sum(s) == target]
    pairs = sum(1 for m in range(1 << n) for s in range(1, 1 << n) if s & m == s)   # double loop
    return [found, pairs]


# dry run: submasks of m = 0b1011 (11) in the order the loop visits them
m, sub, order = 0b1011, 0b1011, []
while sub:
    order.append(format(sub, "04b"))
    sub = (sub - 1) & m
print("submasks of 1011:", order, "count", len(order), "= 2^3 - 1")

# dry run: items [3, 1, 4, 2], target 5 -> which masks hit
items = [3, 1, 4, 2]
for mask in range(16):
    pick = [items[i] for i in range(4) if mask >> i & 1]
    if sum(pick) == 5:
        print(f"mask {mask:>2} = {mask:04b} takes {pick} sum 5")

for it, tg, want in [([3, 1, 4, 2], 5, [[[1, 4], [3, 2]], 65]), ([], 0, [[[]], 0]),
                     ([1, -1, 2], 0, [[[], [1, -1]], 19]), ([5], 3, [[], 1])]:
    got = solve(it, tg)
    assert got == want == brute(it, tg), (it, tg, got)
    print(it, tg, "->", got)

# pairs = 3^n - 2^n for every n up to 12 (runs the real loop)
for n in range(13):
    assert solve(list(range(n)), 10**9)[1] == 3**n - 2**n
print("pairs == 3^n - 2^n for n = 0..12; at n = 12 that is", 3**12 - 2**12)

# submask claim: decreasing order, each exactly once, for every m < 256
for m in range(256):
    seen, sub = [], m
    while sub:
        seen.append(sub)
        sub = (sub - 1) & m
    assert seen == sorted((s for s in range(1, 256) if s & m == s), reverse=True)

# seeded random cross-check
for _ in range(300):
    n = random.randint(0, 7)
    it = random.sample(range(-100, 101), n)
    tg = random.choice([0, random.randint(-20, 20), sum(random.sample(it, random.randint(0, n))) if n else 0])
    assert solve(it, tg) == brute(it, tg)
print("300 seeded random cases ok; submask order claim ok for every m < 256")
assert solve([], 0) == [[[]], 0] and solve([0], 0)[0] == [[], [0]]
print("edge asserts ok")
```

**Output (my run):**
```
submasks of 1011: ['1011', '1010', '1001', '1000', '0011', '0010', '0001'] count 7 = 2^3 - 1
mask  6 = 0110 takes [1, 4] sum 5
mask  9 = 1001 takes [3, 2] sum 5
[3, 1, 4, 2] 5 -> [[[1, 4], [3, 2]], 65]
[] 0 -> [[[]], 0]
[1, -1, 2] 0 -> [[[], [1, -1]], 19]
[5] 3 -> [[], 1]
pairs == 3^n - 2^n for n = 0..12; at n = 12 that is 527345
300 seeded random cases ok; submask order claim ok for every m < 256
edge asserts ok
```

**Edge cases:**
- `items = []`: one mask (0), the empty subset sums to 0. If `target == 0` the answer is `[[]]`, and `pairs = 0`.
- `target` unreachable: `found = []`, but `pairs` is still `3^n - 2^n`.
- Zero in the items (`[0]`, target 0): both `[]` and `[0]` match, in mask order: `[[], [0]]`.
- Negative values: `[1, -1, 2]`, target 0 gives `[[], [1, -1]]`; the empty subset is a legitimate match.
- `n = 12`: 4096 masks, about 4 * 10^3 * 12 steps for the sums, and 527,345 pair steps.

**Follow-ups:**
- *Same problem with meet in the middle?* Split the items in two halves, list the sums of each half (2^(n/2) each), and match with a dict. It beats 2^n for n around 40. Not run here.
- *Where does 3^n show up in a real problem?* Subset DP where `dp[m]` is built from `dp[sub]` and `dp[m ^ sub]` for each submask (partition-into-groups problems). Say it is 3^n, not 4^n.
- *Next larger mask with the same popcount?* Gosper's hack. I would only mention it, not write it from memory.

**Common mistakes:**
- Looping `while sub >= 0`, or forgetting that `sub = 0` must stop the loop (otherwise `(0 - 1) & m = m` and it cycles forever).
- Writing `(sub - 1) | m`, which gives larger numbers, not submasks.
- Counting the empty submask and getting `3^n`.
- Listing subsets in a different order (for example by size) when the prompt asks for increasing mask order.
- Using `1 << n` as the upper bound with `range(1 << n - 1)`: `<<` binds looser than `-` in Python, so that means `1 << (n - 1)`. Bracket it.

### Q31 ⭐ 🟡 Pruning and the cost of backtracking: count the calls. `candidates` has 1 <= len <= 8 distinct positive integers (each <= 20) and `target` is 1 <= target <= 40. Two recursions find the combinations (unlimited reuse) that sum to `target`. Version A keeps the candidates in the given order: `dfs(start, rem)` counts one call, returns if `rem < 0`, records a hit and returns if `rem == 0`, otherwise loops `j` from `start` to the end and calls `dfs(j, rem - c[j])`. Version B sorts the candidates first and also breaks out of the loop as soon as `c[j] > rem` (so it never calls with a negative remainder). Return `[calls_A, calls_B, hits]` (counting the first call `dfs(0, target)`, and `hits` is the same for both). Explain why B never makes more calls than A, why the two hit counts agree, and give one example where B saves a lot and one where it saves nothing. Do not claim a complexity from these counts; they only measure two implementations on inputs. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the same two recursions rewritten with an explicit stack on small inputs. Example: candidates=[5, 2, 3], target=8 -> [19, 13, 3]; candidates=[7], target=1 -> [2, 1, 0]; candidates=[4, 2, 3, 1], target=10 -> [102, 94, 23]; candidates=[1], target=5 -> [6, 6, 1].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking cost measurement: choose, explore, undo, with a pruning rule (sort, then `break` once a candidate is too big) judged by counting recursive calls. Counting calls measures an implementation on an input, it does not prove a big-O.

**Say this first (1 line):** "Both versions explore the same combinations; B sorts and breaks on `c[j] > rem`, so it never makes the call that would only return on `rem < 0`, and I will show the call counts on real inputs, not claim a complexity from them."

**Brute force:** Version A: keep the given order and try every candidate at every node; return at `rem < 0` (wasted call) and record a hit at `rem == 0`. It is correct and is also the unpruned baseline. An explicit-stack rewrite of both versions is the oracle in the code.

**Optimal:** Version B (the pruned one):
- Sort once so candidates ascend.
- In the loop over `j`, `break` when `c[j] > rem`: every later candidate is at least as big, so every later call would have `rem < 0`. This is a safe cut, not a heuristic.
- Decision tree: a node is `dfs(start, rem)`; its children are "take `c[j]`" for `j >= start` (staying on `j` allows reuse, starting at `j` stops order permutations from repeating a combination). Undo is implicit because `rem` is passed by value.
- Why B never makes more calls than A: every call B makes corresponds to a multiset of candidates with total at most `target` (the empty multiset is the root). In A, the same multiset, taken in A's index order, is also a call: all its proper prefixes have a smaller total than the full total, so all have `rem > 0` and none stops early. B visits each such multiset once; A visits all of them as well and also makes the calls with `rem < 0`. So `calls_B <= calls_A`. (The code checks `calls_B` equals the number of multisets with sum at most `target` on random inputs, and the inequality exhaustively on 5,376 cases.)
- Why the hit counts agree: a hit is a multiset with total exactly `target`, and both versions visit each such multiset exactly once.
- Where B saves a lot: candidates that are mostly big compared with the remainder, so many loop iterations are over-shoots (`[3, 5, 7, 11, 13, 17, 19, 20]`, target 40: 2,282 calls against 573). Where it saves nothing: a single candidate of 1 (`[1]`, target 5: every call is useful, 6 and 6), or a list that is already descending such as `[20, 1]` with target 40 (63 and 63 in my run: the 20 is only ever tried at the root and at `rem = 20`, where it fits, so A makes no wasted call).
- Depth: at most `target / min(candidate) + 1`, so 41 at most (candidate 1, target 40), far below the recursion limit of 1000.

**Complexity:** Reasoned, not measured: the number of calls in B is the number of multisets of the candidates with sum at most `target`, which can grow fast with the target; the counts below are examples on inputs, nothing more. Space O(depth) <= 41 frames plus the output counters.

**Dry run:** `candidates = [5, 2, 3]`, target 8. Version A prints a 19-call tree (6 of its calls are `rem < 0` leaves); version B on the sorted `[2, 3, 5]` prints 13 calls and the break removes all 6 over-shoots. Both have the 3 hits `2+2+2+2`, `2+3+3` and `3+5`. The trees are in the output below. Reading A: root `rem=8`; `take 5` leaves 3; from there `take 5` gives `-2` (wasted), `take 2` gives 1, `take 3` gives 0 (hit). In B a node with `rem=2` (after `take 3, take 3`) makes no call at all, because every remaining candidate (3 and 5) is bigger than 2.

**Code:**
```python
import itertools
import random

random.seed(3101)


def run(c, prune, target, trace=None):
    """Version A (prune=False, c as given) or version B (prune=True, c must be sorted).
    Returns (calls, hits). If trace is a list, appends an indented line per call."""
    calls = hits = 0

    def dfs(start, rem, depth, label):
        nonlocal calls, hits
        calls += 1
        note = "rem<0 stop" if rem < 0 else "HIT" if rem == 0 else ""
        if trace is not None:
            trace.append("  " * depth + f"{label}rem={rem} {note}".rstrip())
        if rem < 0:
            return
        if rem == 0:
            hits += 1
            return
        for j in range(start, len(c)):
            if prune and c[j] > rem:
                break                        # sorted: every later candidate is at least as big
            dfs(j, rem - c[j], depth + 1, f"take {c[j]}: ")

    dfs(0, target, 0, "")
    return calls, hits


def solve(candidates, target):
    a, ha = run(list(candidates), False, target)
    b, hb = run(sorted(candidates), True, target)
    assert ha == hb
    return [a, b, ha]


def brute(candidates, target):
    """Same two rules with an explicit stack (no recursion), children pushed in reverse."""
    def go(c, prune):
        calls = hits = 0
        stack = [(0, target)]
        while stack:
            start, rem = stack.pop()
            calls += 1
            if rem < 0:
                continue
            if rem == 0:
                hits += 1
                continue
            for j in range(len(c) - 1, start - 1, -1):
                if prune and c[j] > rem:
                    continue                 # same as 'break' because c is sorted
                stack.append((j, rem - c[j]))
        return calls, hits
    a, ha = go(list(candidates), False)
    b, hb = go(sorted(candidates), True)
    return [a, b, ha]


# decision trees for candidates=[5, 2, 3], target=8
for name, c, prune in [("A (given order 5,2,3)", [5, 2, 3], False), ("B (sorted 2,3,5, with break)", [2, 3, 5], True)]:
    t = []
    calls, hits = run(c, prune, 8, t)
    print(f"--- {name}: {calls} calls, {hits} hits")
    print("\n".join(t))

for c, t, want in [([5, 2, 3], 8, [19, 13, 3]), ([7], 1, [2, 1, 0]), ([4, 2, 3, 1], 10, [102, 94, 23]), ([1], 5, [6, 6, 1])]:
    got = solve(c, t)
    assert got == want == brute(c, t), (c, t, got)
    print(c, t, "->", got)

big = [3, 5, 7, 11, 13, 17, 19, 20]
print("B saves a lot:", big, 40, "->", solve(big, 40))
print("B saves nothing:", [1], 5, "->", solve([1], 5), "| and", [20, 1], 40, "->", solve([20, 1], 40))

# why B <= A: B's calls are exactly the multisets with sum <= target (empty one = root); each also exists in A
def multisets_le(c, target):
    n = 0
    def go(start, total):
        nonlocal n
        n += 1
        for j in range(start, len(c)):
            if total + c[j] <= target:
                go(j, total + c[j])
    go(0, 0)
    return n

for _ in range(300):
    k = random.randint(1, 5)
    c = random.sample(range(1, 21), k)
    t = random.randint(1, 40)
    a, b, h = solve(c, t)
    assert b == multisets_le(sorted(c), t) and b <= a
    assert [a, b, h] == brute(c, t)
print("300 seeded random cases: B == #multisets with sum <= target, B <= A, hits agree, explicit stack agrees")

# exhaustive: every ordering of every 3-subset of 1..8, targets 1..16
cnt = 0
for cs in itertools.combinations(range(1, 9), 3):
    for perm in itertools.permutations(cs):
        for t in range(1, 17):
            a, ha = run(list(perm), False, t)
            b, hb = run(list(cs), True, t)
            assert b <= a and ha == hb
            cnt += 1
print("exhaustive over", cnt, "(ordering, target) cases: calls_B <= calls_A and hits agree")
assert solve([1], 40) == [41, 41, 1]
print("edge asserts ok (depth 41 for candidate 1, target 40)")
```

**Output (my run):**
```
--- A (given order 5,2,3): 19 calls, 3 hits
rem=8
  take 5: rem=3
    take 5: rem=-2 rem<0 stop
    take 2: rem=1
      take 2: rem=-1 rem<0 stop
      take 3: rem=-2 rem<0 stop
    take 3: rem=0 HIT
  take 2: rem=6
    take 2: rem=4
      take 2: rem=2
        take 2: rem=0 HIT
        take 3: rem=-1 rem<0 stop
      take 3: rem=1
        take 3: rem=-2 rem<0 stop
    take 3: rem=3
      take 3: rem=0 HIT
  take 3: rem=5
    take 3: rem=2
      take 3: rem=-1 rem<0 stop
--- B (sorted 2,3,5, with break): 13 calls, 3 hits
rem=8
  take 2: rem=6
    take 2: rem=4
      take 2: rem=2
        take 2: rem=0 HIT
      take 3: rem=1
    take 3: rem=3
      take 3: rem=0 HIT
    take 5: rem=1
  take 3: rem=5
    take 3: rem=2
    take 5: rem=0 HIT
  take 5: rem=3
[5, 2, 3] 8 -> [19, 13, 3]
[7] 1 -> [2, 1, 0]
[4, 2, 3, 1] 10 -> [102, 94, 23]
[1] 5 -> [6, 6, 1]
B saves a lot: [3, 5, 7, 11, 13, 17, 19, 20] 40 -> [2282, 573, 57]
B saves nothing: [1] 5 -> [6, 6, 1] | and [20, 1] 40 -> [63, 63, 3]
300 seeded random cases: B == #multisets with sum <= target, B <= A, hits agree, explicit stack agrees
exhaustive over 5376 (ordering, target) cases: calls_B <= calls_A and hits agree
edge asserts ok (depth 41 for candidate 1, target 40)
```

**Edge cases:**
- `[7]`, target 1: A makes 2 calls (root, then `rem = -6`), B makes 1 (7 > 1 breaks immediately), 0 hits.
- `[1]`, target 5: the tree is a chain of 6 calls in both.
- Target equal to a candidate: one hit, B makes few calls.
- Unsorted input: B sorts first; without sorting, the `break` would be wrong (a later candidate can be smaller). This is the usual bug.
- Candidates are distinct and positive by the prompt; a 0 or negative would break the termination argument and the `break` rule.

**Follow-ups:**
- *Why not memoise?* The question lists the combinations or counts calls; to count them, a DP (Part 10 Q10, coin change II) is O(n * target). The call counts here belong to the enumeration.
- *Does B change the answer order?* The sorted input changes the order of results if you print them; the count of hits is unchanged. Sort the result list if the output order is specified.
- *Is the count of calls a complexity?* No: it is one number for one input. A bound comes from reasoning (multisets with total at most `target`), not from a table of counts.

**Common mistakes:**
- Sorting but forgetting the `break` (the answer is right, the speed gain is gone: the loop still makes the wasted calls).
- Using `continue` instead of `break` after sorting; it works but still scans the whole tail of the loop.
- Breaking without sorting, which skips valid smaller candidates.
- Recursing with `dfs(j + 1, ...)` (each candidate once) when reuse is allowed.
- Saying "pruning makes it polynomial": it only removes dead calls.

### Q32 ⭐ 🟡 Iterative backtracking and the recursion limit. `board` is a list of rows (strings of equal length, lowercase) with 1 <= rows * cols <= 2000, and `word` is a string of length 1 to 2000. Return True if `word` can be spelled along a path of horizontally or vertically adjacent cells that uses no cell twice. The single-word recursion of Q9 nests one frame per letter, so a 1 x 1500 row of 'a' with `word = 'a' * 1500` raises RecursionError under CPython's default limit of 1000 (run it and show the message), while the same recursion on a row of 300 works; in this question your solution must be ITERATIVE: keep an explicit stack of (cell, next-direction-index) frames and a set of cells on the path, push when you extend the path, and pop (removing the cell from the set) when all four directions are tried. The tests are corridor-shaped boards (one row, or a winding one-cell-wide path of 'a' bordered by 'b'), on which the search is fast; on an open board of equal letters the search time is exponential for ANY backtracking solution and is out of scope. Say what an explicit stack costs in Python compared with the call stack, and that raising the limit with sys.setrecursionlimit is an observation about one machine and Python version and not a fix you can promise. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the recursive version of Q9 on boards small enough for its depth on small inputs. Example: board=['aab', 'bba'], word='aba' -> True; board=['abc'], word='cba' -> True; board=['abc'], word='abca' -> False; board=['aaaa'], word='aaaa' -> True; board=['ab', 'ca'], word='acb' -> False.
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with an explicit stack: the call stack is replaced by a list of frames (cell, next direction), plus a set of cells on the path, so the depth is no longer limited by CPython's recursion limit.

**Say this first (1 line):** "Same search as the recursive word search, but each frame is an entry in my own list: I push when I extend the path and pop, removing the cell from the set, when all four directions are tried."

**Brute force:** The recursive word search of Q9: one Python frame per letter, add the cell to a set, try four neighbours, discard on the way back. It is correct, but on a 1 x 1500 row of `'a'` with a 1500-letter word it raises `RecursionError: maximum recursion depth exceeded` under the default limit of 1000 (shown below), and it works on a row of 300.

**Optimal:** The iterative version:
- Frames: `path` is a list of cells, `nxt[k]` is the next direction index (0..4) to try from `path[k]`, and `on_path` is a set of the same cells for O(1) membership.
- Loop `while path`: if `len(path) == L` return True. Take the top cell and its direction `d`. If `d == 4`, all directions are tried: pop the frame and discard the cell from the set (this is the undo). Otherwise increment `nxt[-1]` and look at the neighbour; if it is on the board, not on the path and equals `word[len(path)]`, push it.
- Start the search from every cell equal to `word[0]`; when a start finishes without success, `path` is empty again (every push was matched by a pop), so the next start begins clean.
- Cheap guard: `L > rows * cols` is an immediate False (a path needs L distinct cells).
- Invariant: `path` is a simple path spelling `word[:len(path)]`, `on_path` equals the set of its cells.
- What the explicit stack costs: you write and maintain the frame state by hand (more code, easier to get the undo wrong); the frames are heap objects in lists, which is O(L) memory just as the call stack would be, but with no limit of 1000 and no `RecursionError`; and each step is a loop iteration with list indexing instead of a function call. I did not time it and make no claim about which is faster.
- `sys.setrecursionlimit`: on this machine (Python 3.13) the 1 x 1500 recursive case works after setting the limit to 5000 (shown below). That is an observation about one machine and version. A very deep recursion can still exhaust the memory or the C stack on another build and crash the process rather than raise a clean error, so I would not promise it as the fix; I would use the explicit stack.
- Scope: this is fast on corridor-shaped boards (one row, or a one-cell-wide winding path bordered by other letters). On an open board of equal letters any backtracking solution is exponential in the worst case; that is out of scope.

**Complexity:** On the corridor tests: each start explores one path of at most L cells, with at most 4 neighbour checks per cell, so one start is O(4 * L) and all starts are O(R * C * L) at most (about 1960 * 1025 * 4 for the serpentine); on these boards no sub-search branches, because every `'a'` cell has at most two `'a'` neighbours. In general the worst case is exponential. Space O(L) for `path`, `nxt` and `on_path`.

**Dry run:** `board = ['aab', 'bba'], word = 'aba'` (cells as (row, col)). Directions are tried right, down, left, up.
- Start at (0,0) 'a'. Need 'b': right (0,1) is 'a' no; down (1,0) is 'b' yes, push. Need 'a': right (1,1) is 'b' no; down is off the board; left off; up (0,0) is on the path. Direction 4 reached, pop (1,0). Back at (0,0): left, up are off the board, pop (0,0).
- Start at (0,1) 'a'. Need 'b': right (0,2) is 'b', push. Need 'a': right off the board; down (1,2) is 'a', push. Length 3 equals L: True. The path a-b-a is (0,1), (0,2), (1,2).

**Code:**
```python
import random
import sys

random.seed(3201)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]          # right, down, left, up


def exist_iter(board, word, trace=None):
    """Iterative word search. path = list of cells, nxt = next direction index per frame, on_path = set."""
    R, C, L = len(board), len(board[0]), len(word)
    if L > R * C:
        return False
    for sr in range(R):
        for sc in range(C):
            if board[sr][sc] != word[0]:
                continue
            path, nxt, on_path = [(sr, sc)], [0], {(sr, sc)}
            if trace is not None:
                trace.append(f"start {path[0]}")
            while path:
                if len(path) == L:
                    return True
                r, c = path[-1]
                d = nxt[-1]
                if d == 4:                           # all four directions tried: undo this cell
                    path.pop()
                    nxt.pop()
                    on_path.discard((r, c))
                    if trace is not None:
                        trace.append(f"pop {(r, c)}")
                    continue
                nxt[-1] += 1
                nr, nc = r + DIRS[d][0], c + DIRS[d][1]
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in on_path and board[nr][nc] == word[len(path)]:
                    path.append((nr, nc))
                    nxt.append(0)
                    on_path.add((nr, nc))
                    if trace is not None:
                        trace.append(f"push {(nr, nc)} for '{word[len(path) - 1]}'")
    return False


def exist_rec(board, word):
    """The Q9 style recursion: one frame per letter."""
    R, C = len(board), len(board[0])
    on_path = set()

    def go(r, c, k):
        if board[r][c] != word[k] or (r, c) in on_path:
            return False
        if k == len(word) - 1:
            return True
        on_path.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                return True
        on_path.discard((r, c))                       # undo on the way back
        return False

    return any(go(r, c, 0) for r in range(R) for c in range(C))


def serpentine(rows_of_a, width):
    """One-cell-wide winding corridor of 'a' inside a border of 'b'. Returns (board, number of a cells)."""
    rows = []
    for i in range(2 * rows_of_a - 1):
        if i % 2 == 0:
            rows.append("a" * width)
        elif (i // 2) % 2 == 0:
            rows.append("b" * (width - 1) + "a")
        else:
            rows.append("a" + "b" * (width - 1))
    return rows, sum(r.count("a") for r in rows)


# dry run
tr = []
print("dry run board=['aab','bba'] word='aba':", exist_iter(["aab", "bba"], "aba", tr))
print("\n".join("  " + t for t in tr))

for b, w, want in [(["aab", "bba"], "aba", True), (["abc"], "cba", True), (["abc"], "abca", False),
                   (["aaaa"], "aaaa", True), (["ab", "ca"], "acb", False)]:
    assert exist_iter(b, w) == exist_rec(b, w) == want, (b, w)
    print(b, w, "->", exist_iter(b, w))

# the recursion limit, observed on this machine (Python %s)
print("python", sys.version.split()[0], "default recursion limit", sys.getrecursionlimit())
row = ["a" * 1500]
try:
    exist_rec(row, "a" * 1500)
except RecursionError as e:
    print("recursive, 1 x 1500:", type(e).__name__ + ":", e)
print("recursive, 1 x 300:", exist_rec(["a" * 300], "a" * 300))
print("iterative, 1 x 1500:", exist_iter(row, "a" * 1500), "| 1 x 1500 word of 1501:", exist_iter(row, "a" * 1501))

board, n_a = serpentine(25, 40)
cells = len(board) * len(board[0])
print(f"serpentine {len(board)} x {len(board[0])} = {cells} cells, {n_a} cells of 'a'")
print("iterative, word = 'a' * %d:" % n_a, exist_iter(board, "a" * n_a), "| word = 'a' * %d:" % (n_a + 1), exist_iter(board, "a" * (n_a + 1)))
assert exist_iter(board, "a" * n_a) is True and exist_iter(board, "a" * (n_a + 1)) is False
try:
    exist_rec(board, "a" * n_a)
except RecursionError:
    print("recursive on the same corridor: RecursionError")

# raising the limit: an observation about this machine and version, not a guarantee
old = sys.getrecursionlimit()
sys.setrecursionlimit(5000)
print("recursive, 1 x 1500 with limit 5000:", exist_rec(row, "a" * 1500))
sys.setrecursionlimit(old)

# seeded random cross-check of iterative vs recursive Q9 on small boards
for _ in range(600):
    r, c = random.randint(1, 4), random.randint(1, 4)
    al = random.choice(["ab", "abc", "a"])
    b = ["".join(random.choice(al) for _ in range(c)) for _ in range(r)]
    w = "".join(random.choice(al) for _ in range(random.randint(1, min(8, 2 * r * c))))
    assert exist_iter(b, w) == exist_rec(b, w), (b, w)
print("600 seeded random boards: iterative == recursive")
assert not exist_iter(["abc", "xxx"], "abcb") and not exist_rec(["abc", "xxx"], "abcb")
assert exist_iter(["a"], "a") and not exist_iter(["a"], "aa") and not exist_iter(["ab"], "ba" + "a")
print("edge asserts ok")
```

**Output (my run):**
```
dry run board=['aab','bba'] word='aba': True
  start (0, 0)
  push (1, 0) for 'b'
  pop (1, 0)
  pop (0, 0)
  start (0, 1)
  push (0, 2) for 'b'
  push (1, 2) for 'a'
['aab', 'bba'] aba -> True
['abc'] cba -> True
['abc'] abca -> False
['aaaa'] aaaa -> True
['ab', 'ca'] acb -> False
python 3.13.17 default recursion limit 1000
recursive, 1 x 1500: RecursionError: maximum recursion depth exceeded
recursive, 1 x 300: True
iterative, 1 x 1500: True | 1 x 1500 word of 1501: False
serpentine 49 x 40 = 1960 cells, 1024 cells of 'a'
iterative, word = 'a' * 1024: True | word = 'a' * 1025: False
recursive on the same corridor: RecursionError
recursive, 1 x 1500 with limit 5000: True
600 seeded random boards: iterative == recursive
edge asserts ok
```

**Edge cases:**
- `L > rows * cols`: False at once.
- 1 x 1 board: `['a']` with `'a'` is True, with `'aa'` is False (a cell cannot be reused).
- The word needs the same cell twice (`['abc', 'xxx']`, `'abcb'`): False, because the set blocks it even though L = 4 is below the 6 cells.
- Backtracking undo: forgetting to discard the cell from `on_path` on pop makes later starts see stale cells (wrong answers on some boards).
- The start cell is not unique: `['aab', 'bba']` first start at (0,0) fails and the second one succeeds.

**Follow-ups:**
- *Could you keep the recursion and raise the limit?* On one machine it worked (1500 deep with a limit of 5000 here). I would not rely on it; the limit protects the C stack and the safe value depends on the build.
- *A trick to convert any recursion to a stack?* Put the arguments plus a "which child next" counter into a frame, push for the call, pop for the return; that is exactly `(cell, next direction)` here.
- *Open boards of equal letters?* Exponential for any backtracking; with the word's letter counts or a quick reachability check you can prune, but the worst case stays.

**Common mistakes:**
- Pushing a neighbour but not adding it to `on_path`, or popping without discarding.
- Marking the starting cell on the path only when the first push happens (the start itself is on the path from the start).
- Checking the length only after a push and so missing `L == 1`: here the check is at the top of the loop, so a one-letter word is found at once.
- Raising the recursion limit and calling it solved.
- Testing the recursive version on large boards and believing a `RecursionError` means a wrong answer: it means the depth.

### Q33 ⭐ 🟡 Trie memory versus a dict of sets. `words` has 1 to 5000 lowercase words (length 1 to 20, repeats allowed). Return `[nodes, slots26, pairs, distinct]`: `nodes` is the number of trie nodes excluding the root; `slots26` is `26 * (nodes + 1)`, the number of child slots if every node, root included, holds a fixed array of 26 children; `pairs` is the number of (prefix, word) pairs you would store in a dict that maps every non-empty prefix to the set of distinct words having that prefix (the sum of the lengths of the distinct words); and `distinct` is the number of distinct words. Explain what each number means in memory terms (dict children store only the existing edges, an array of 26 stores empty slots too, the dict of sets repeats every word under each of its prefixes and its keys are exactly the trie's nodes), why `nodes <= pairs` and when they are equal (exactly when no two distinct words share a first letter), and what a trie does NOT save compared with a plain `set` of words. You may measure `sys.getsizeof` on your machine, labelled as a sandbox measurement for one Python version, but do not present sizes as proof. Part 7 Q41 builds the trie at concept level and Part 3 Q36 compares it with a sorted list for prefix counts; the full API is Q3. In the answer include a dry run on the first example and a seeded random cross-check of your solution against counting the distinct prefixes of the distinct words with a set on small inputs. Example: words=['car', 'cart', 'cat', 'dog', 'do', 'car'] -> [8, 234, 15, 5]; words=['a', 'b', 'c'] -> [3, 104, 3, 3]; words=['aaa'] -> [3, 104, 3, 1]; words=['ab', 'ac'] -> [3, 104, 4, 2].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Trie memory accounting (concept level): count nodes, child slots and stored pairs, and compare three layouts: a trie with dict children, a trie with a fixed array of 26 children, and a dict from every prefix to the set of words that have it.

**Say this first (1 line):** "Nodes are the distinct non-empty prefixes of the distinct words; a 26-array pays for every empty slot, a dict of sets repeats each word under all its prefixes, and a trie still does not beat a plain set of words when prefixes are not shared."

**Brute force:** Put every distinct word into a `set`, collect every non-empty prefix of every distinct word into another `set`, and count: `nodes` = number of distinct prefixes, `pairs` = sum of the distinct words' lengths. This is the oracle in the code.

**Optimal:** Build the dict-of-dicts trie once and count:
- `nodes`: each time an edge `ch` is missing and created, add 1. The root is not counted. Repeats of a word create nothing, so I insert distinct words only.
- `slots26 = 26 * (nodes + 1)`: with an array of 26 child slots per node, the root also holds an array, so there are `nodes + 1` arrays.
- `pairs`: the dict of sets stores `(prefix, word)` once per non-empty prefix of each distinct word, so `pairs = sum(len(w) for w in distinct)`.
- `distinct = len(set(words))`.
- What each number means in memory terms:
  - Dict children store only the edges that exist, so the number of entries is `nodes` (every non-root node has exactly one incoming edge), plus one dict object per node.
  - The array of 26 stores empty slots too: `slots26` is mostly empty for sparse tries, though it gives O(1) indexing by `ord(ch) - 97` and no hashing.
  - The dict of sets repeats every word under each of its prefixes: `pairs` set entries. Its keys are exactly the trie's nodes (the distinct non-empty prefixes), so it has the trie's node count in keys plus the repeated set entries. It answers "all words with this prefix" in O(answer) after one hash lookup, which is its reason to exist.
- Why `nodes <= pairs`: each node is a distinct prefix, and each distinct prefix of a distinct word is one of the `pairs` (prefix, word) pairs, so the number of distinct prefixes cannot exceed the number of pairs.
- When they are equal: exactly when no two distinct words share a first letter. If two words share a first letter they share that first node, so there are fewer nodes than pairs. If all first letters differ, no prefix is shared at all (different first letters mean different prefixes), so every pair is its own node. The code checks this on 1,500 random lists and exhaustively on small ones.
- What a trie does NOT save compared with a plain `set` of words: the set stores each word once (about its length in bytes plus a fixed object overhead) and answers "is this exact word present" in O(L) as well (hashing a word is O(L)). A trie wins only when prefixes are shared heavily or when you need prefix queries, ordered traversal or per-prefix counts; with unshared words it has more objects (one dict or array per node) than the set has strings. Sandbox sizes below agree on this machine.
- Sandbox sizes, labelled: shallow `sys.getsizeof` sums on this machine and Python 3.13. On 5,000 random words (4,582 distinct) with 38,952 nodes, the dict-children trie was about 6.7 MB (about 172 bytes per node), the trie of 26-lists about 10.3 MB, the plain set about 0.37 MB (about 81 bytes per distinct word) and the dict of sets about 12.3 MB. On 16 distinct words that share a 20-letter prefix the trie was smaller than the dict of sets (7.5 KB against 27.6 KB) but the set was smaller still (1.8 KB). These sizes are shallow, one run, one Python version: not a proof of anything.

**Complexity:** Building the trie is O(total length of the distinct words) time (here at most 5000 * 20 = 10^5 steps), with `nodes` <= that total. Memory is proportional to `nodes` (dict children) or `26 * (nodes + 1)` (arrays); the dict of sets is proportional to `pairs`.

**Dry run:** `words = ['car', 'cart', 'cat', 'dog', 'do', 'car']`. Distinct: `car, cart, cat, dog, do`, so `distinct = 5` (the repeated `car` adds nothing). Inserting in sorted order, new nodes (as prefixes): `car` makes `c, ca, car`; `cart` makes `cart`; `cat` makes `cat`; `do` makes `d, do`; `dog` makes `dog`. That is 3 + 1 + 1 + 2 + 1 = 8 nodes. `slots26 = 26 * 9 = 234`. `pairs = 3 + 4 + 3 + 3 + 2 = 15`. So `[8, 234, 15, 5]`. Note `8 < 15`: `car`, `cart`, `cat` share `c` and `ca`.

**Code:**
```python
import itertools
import random
import sys

random.seed(3301)


def trie_numbers(words):
    """Returns [nodes, slots26, pairs, distinct] using a dict-of-dicts trie."""
    distinct = set(words)
    root = {}
    nodes = 0
    for w in distinct:                       # repeats change nothing, so insert each distinct word once
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                nodes += 1
            node = node[ch]
    pairs = sum(len(w) for w in distinct)    # every non-empty prefix of w pairs with w once
    return [nodes, 26 * (nodes + 1), pairs, len(distinct)]


def brute(words):
    distinct = set(words)
    prefixes = {w[:i] for w in distinct for i in range(1, len(w) + 1)}   # distinct non-empty prefixes
    return [len(prefixes), 26 * (len(prefixes) + 1), sum(len(w) for w in distinct), len(distinct)]


# dry run on the first example
words = ["car", "cart", "cat", "dog", "do", "car"]
seen = set()
for w in sorted(set(words)):
    new = [w[:i] for i in range(1, len(w) + 1) if w[:i] not in seen]
    seen.update(new)
    print(f"insert {w!r:7} new nodes: {new}")
print("nodes =", len(seen), "(the distinct non-empty prefixes)")

for ws, want in [(["car", "cart", "cat", "dog", "do", "car"], [8, 234, 15, 5]), (["a", "b", "c"], [3, 104, 3, 3]),
                 (["aaa"], [3, 104, 3, 1]), (["ab", "ac"], [3, 104, 4, 2])]:
    got = trie_numbers(ws)
    assert got == want == brute(ws), (ws, got)
    print(ws, "->", got)

# claim: dict of sets has exactly the trie's nodes as keys; nodes <= pairs; equality iff first letters all differ
for _ in range(1500):
    ws = ["".join(random.choice("abc") for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 6))]
    nodes, slots, pairs, distinct = trie_numbers(ws)
    assert [nodes, slots, pairs, distinct] == brute(ws)
    d = {}
    for w in set(ws):
        for i in range(1, len(w) + 1):
            d.setdefault(w[:i], set()).add(w)
    assert len(d) == nodes and sum(len(v) for v in d.values()) == pairs and nodes <= pairs
    firsts = {w[0] for w in set(ws)}
    assert (nodes == pairs) == (len(firsts) == distinct)
print("1500 seeded random word lists: nodes == keys of the dict of sets, nodes <= pairs, equal iff first letters all differ")

# exhaustive: every list of up to 3 words from {a, b, ab, ba, bb, aab}
pool = ["a", "b", "ab", "ba", "bb", "aab"]
for k in (1, 2, 3):
    for ws in itertools.product(pool, repeat=k):
        n, _, p, dct = trie_numbers(list(ws))
        assert n <= p and ((n == p) == (len({w[0] for w in set(ws)}) == dct))
print("exhaustive small lists ok")


# sandbox measurement (this machine and Python version only): shallow sys.getsizeof sums, NOT a proof of anything
def sizes(ws):
    distinct = set(ws)
    root = {}
    node_dicts = [root]
    for w in distinct:
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                node_dicts.append(node[ch])
            node = node[ch]
    trie_dict = sum(sys.getsizeof(d) for d in node_dicts)
    trie_arr = len(node_dicts) * sys.getsizeof([None] * 26)
    plain_set = sys.getsizeof(distinct) + sum(sys.getsizeof(w) for w in distinct)
    dos = {}
    for w in distinct:
        for i in range(1, len(w) + 1):
            dos.setdefault(w[:i], set()).add(w)
    dict_sets = sys.getsizeof(dos) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in dos.items()) \
        + sum(sys.getsizeof(w) for w in distinct)
    return trie_dict, trie_arr, plain_set, dict_sets


print("sandbox sizes, Python", sys.version.split()[0], "(bytes: trie of dicts, trie of 26-lists, plain set, dict of sets)")
for name, ws in [("5000 random words, len 1-20 over 'abcdefghij'",
                  ["".join(random.choice("abcdefghij") for _ in range(random.randint(1, 20))) for _ in range(5000)]),
                 ("5000 words 'internationalisation' + 4 letters over 'ab'",
                  ["internationalisation" + "".join(random.choice("ab") for _ in range(4)) for _ in range(5000)])]:
    r = trie_numbers(ws)
    print(" ", name, "-> [nodes, slots26, pairs, distinct] =", r, "| sizes", sizes(ws))

assert trie_numbers(["a" * 20] * 5000) == [20, 26 * 21, 20, 1]
print("edge asserts ok")
```

**Output (my run):**
```
insert 'car'   new nodes: ['c', 'ca', 'car']
insert 'cart'  new nodes: ['cart']
insert 'cat'   new nodes: ['cat']
insert 'do'    new nodes: ['d', 'do']
insert 'dog'   new nodes: ['dog']
nodes = 8 (the distinct non-empty prefixes)
['car', 'cart', 'cat', 'dog', 'do', 'car'] -> [8, 234, 15, 5]
['a', 'b', 'c'] -> [3, 104, 3, 3]
['aaa'] -> [3, 104, 3, 1]
['ab', 'ac'] -> [3, 104, 4, 2]
1500 seeded random word lists: nodes == keys of the dict of sets, nodes <= pairs, equal iff first letters all differ
exhaustive small lists ok
sandbox sizes, Python 3.13.17 (bytes: trie of dicts, trie of 26-lists, plain set, dict of sets)
  5000 random words, len 1-20 over 'abcdefghij' -> [nodes, slots26, pairs, distinct] = [38952, 1012778, 52379, 4582] | sizes (6683920, 10283592, 371529, 12348642)
  5000 words 'internationalisation' + 4 letters over 'ab' -> [nodes, slots26, pairs, distinct] = [50, 1326, 384, 16] | sizes (7464, 13464, 1768, 27646)
edge asserts ok
```

**Edge cases:**
- Repeated words: counted once in all four numbers.
- A word that is a prefix of another (`do`, `dog`): the shorter word adds no new nodes after the longer one is there, but it still adds its own `len` to `pairs`.
- One word of length 20: `nodes = 20`, `pairs = 20`, equal (no sharing possible).
- Single-letter distinct words (`a, b, c`): `nodes = pairs = 3`, `slots26 = 104`.
- Same word 5,000 times: `[20, 546, 20, 1]` for a 20-letter word.
- 5,000 words of 20 letters, no sharing: up to 10^5 nodes, `slots26` up to 2.6 million slots.

**Follow-ups:**
- *Compact the trie?* A radix (compressed) tree stores a chain of single-child nodes as one edge with a string; it cuts the node count for sparse sets. Concept only here.
- *Where does the trie fit?* Part 7 Q41 builds it at concept level, Part 3 Q36 compares it with a sorted list for prefix counts, and the full API is Q3.
- *Which would you use for autocomplete?* A trie (or a sorted array plus binary search for a static list); the dict of sets is a memory-hungry alternative and fine for small dictionaries.

**Common mistakes:**
- Counting the root as a node, or forgetting the root's array in `slots26`.
- Counting repeated words twice in `pairs`.
- Presenting `sys.getsizeof` totals as proof, or comparing them across Python versions.
- Saying "a trie saves memory" without the condition (shared prefixes).
- Storing the whole word at the end node of every trie node (that is the dict of sets again).

### Q34 ⭐ 🟡 A minimal skip list (concept level). Implement an ordered set of integers as a skip list with up to 16 levels in which a new node gets level 1, and each further level with probability 1/2 (use a seeded `random.Random`). `ops` is a list (1 <= len <= 2000) of `['insert', x]` (True if x was absent and is now inserted, False if already present), `['contains', x]` and `['remove', x]` (True if x was present and is removed, False otherwise), with |x| <= 10^6. Return the list of results. Describe how a search starts at the top level and drops down, why the expected cost is O(log n) per operation with random levels and O(n) in the worst case, and why the results never depend on the random choices (only the speed does). Say one real use (an ordered in-memory index, for instance a sorted-set structure) and why a balanced tree is the alternative; do not build the whole data store. This is a concept-level question; the Bloom filter is Part 1 Q42 and the LRU idea is Part 6 Q30. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Python set tracked next to the skip list on small inputs. Example: ops=[['insert', 3], ['insert', 1], ['contains', 3], ['remove', 3], ['contains', 3], ['insert', 1]] -> [True, True, True, True, False, False]; ops=[['remove', 5]] -> [False]; ops=[['insert', -2], ['insert', -2], ['remove', -2], ['remove', -2]] -> [True, False, True, False].
**Asked at:** Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Skip list (concept level): a sorted linked list with extra "express" levels chosen at random, giving expected O(log n) search without rotations.

**Say this first (1 line):** "Level 0 is a sorted linked list of every key; each higher level is a random sample of the level below, so a search starts at the top, moves right while the next key is smaller, drops down a level, and repeats."

**Brute force:** A Python `set` (the oracle in the code) gives the same results in O(1) average per operation but has no order. A sorted list with `bisect` has O(log n) search but O(n) insert and remove. A plain sorted linked list is O(n) for everything.

**Optimal:** The skip list:
- Node: a key and a list `next` with one pointer per level it belongs to. A head sentinel has all 16 levels.
- Level choice: a new node starts at level 1 and gets one more level per fair coin flip (`rng.random() < 0.5`), up to 16. So about half of the nodes reach level 2, a quarter level 3, and so on.
- Search (`_path`): start at the head on the top level; while the next key on this level is less than `x`, step right; then drop to the level below, keeping the node you stand on. Record the last node before `x` on every level (`update`). At the bottom, the next node is either `x` or something larger.
- `contains(x)`: look at the next node on level 0. `insert(x)`: if it is already there return False; otherwise draw a level and splice the new node after `update[i]` on each of its levels. `remove(x)`: if the node is not there return False, otherwise unlink it on each of its levels using `update[i]`.
- Why expected O(log n): going from the bottom up, a node that has a higher level appears about every 2nd step on the level below, so you walk an expected O(1) steps per level, and with n keys about log2(n) levels are used. In my run, 2,000 sorted keys took about 11 steps per lookup on average with random levels, against about 1,000 when I forced every level to 1 (a plain list); that is one run, an illustration, not a proof.
- Why O(n) in the worst case: the levels are random, so with bad luck (all nodes at level 1, shown below) the structure is a plain linked list and a search walks the whole bottom level.
- Why the results never depend on the random choices: the bottom level always holds exactly the current set of keys in order, whatever the levels are; the levels only decide how many steps it takes to find a place. The code checks that 6 different seeds and forced levels of 1 and 16 give the same results as a set on 300 random operation lists.
- One real use: an ordered in-memory index (a sorted-set structure in a database or cache, for instance) where you need ordered range scans and fast insert. The alternative is a balanced tree (red-black, AVL): O(log n) worst case but rotations are harder to write and to make lock-free; the skip list is simpler to implement and to extend with concurrency, at the price of randomness and about two pointers per node on average.
- Concept scope: no deletion of empty levels, no range queries, no persistence; the Bloom filter is Part 1 Q42 and the LRU idea is Part 6 Q30.

**Complexity:** Expected O(log n) time per operation with n keys (random levels), O(n) in the worst case (all nodes at level 1, or a very unlucky run). Space O(n) expected (about 2 pointers per node on average because the expected level is 2), plus the 16-pointer head.

**Dry run:** `ops = [insert 3, insert 1, contains 3, remove 3, contains 3, insert 1]` with seed 7. The levels printed after each operation (bottom first):
- `insert 3`: True, the tower of 3 has level 3: levels `[[3], [3], [3]]`.
- `insert 1`: True, 1 gets level 2: bottom `[1, 3]`, level 1 `[1, 3]`, level 2 `[3]`. Search for 1 goes from the head at the top level, sees 3 is not smaller than 1, drops, drops, and splices.
- `contains 3`: True. Levels 3 to 15 of the head are empty, so the walk really starts at the top non-empty level (level 2 in 0-based numbering): the next key is 3, not smaller than 3, drop to level 1, next key is 1 < 3, step to 1, then 3 is not smaller, drop to level 0, the next node is 3: found.
- `remove 3`: True, the node is unlinked on all its levels: `[[1], [1]]`.
- `contains 3`: False. `insert 1`: False (already there). Result `[True, True, True, True, False, False]`, as in the prompt.

**Code:**
```python
import random

MAX_LEVEL = 16


class Node:
    __slots__ = ("key", "next")

    def __init__(self, key, level):
        self.key = key
        self.next = [None] * level          # next[i] = successor on level i (0 = bottom, holds every key)


class SkipList:
    """Ordered set of ints. A new node gets level 1, plus one more level per fair coin flip, up to 16."""

    def __init__(self, seed=0, level_fn=None):
        self.rng = random.Random(seed)
        self.level_fn = level_fn             # test hook: force levels (e.g. always 1 = plain linked list)
        self.head = Node(None, MAX_LEVEL)    # sentinel with all 16 levels
        self.steps = 0                       # nodes stepped onto while searching (for the O(log n) vs O(n) demo)

    def _random_level(self):
        if self.level_fn:
            return self.level_fn()
        lvl = 1
        while lvl < MAX_LEVEL and self.rng.random() < 0.5:
            lvl += 1
        return lvl

    def _path(self, x):
        """Start on the top level, move right while the next key is < x, then drop one level. Returns the
        last node before x on every level."""
        update = [None] * MAX_LEVEL
        cur = self.head
        for i in range(MAX_LEVEL - 1, -1, -1):
            while cur.next[i] is not None and cur.next[i].key < x:
                cur = cur.next[i]
                self.steps += 1
            update[i] = cur
        return update

    def contains(self, x):
        nxt = self._path(x)[0].next[0]
        return nxt is not None and nxt.key == x

    def insert(self, x):
        update = self._path(x)
        nxt = update[0].next[0]
        if nxt is not None and nxt.key == x:
            return False
        node = Node(x, self._random_level())
        for i in range(len(node.next)):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node
        return True

    def remove(self, x):
        update = self._path(x)
        node = update[0].next[0]
        if node is None or node.key != x:
            return False
        for i in range(len(node.next)):
            update[i].next[i] = node.next[i]
        return True

    def levels(self):
        """Keys on each level, bottom first, for printing."""
        out = []
        for i in range(MAX_LEVEL):
            row, cur = [], self.head.next[i]
            while cur is not None:
                row.append(cur.key)
                cur = cur.next[i]
            if not row:
                break
            out.append(row)
        return out


def run(ops, seed=0, level_fn=None):
    sl = SkipList(seed, level_fn)
    return [getattr(sl, name)(x) for name, x in ops], sl


def brute(ops):
    s, out = set(), []
    for name, x in ops:
        if name == "insert":
            out.append(x not in s)
            s.add(x)
        elif name == "contains":
            out.append(x in s)
        else:
            out.append(x in s)
            s.discard(x)
    return out


# dry run, first example, with the tower shape after every op
ex = [["insert", 3], ["insert", 1], ["contains", 3], ["remove", 3], ["contains", 3], ["insert", 1]]
sl = SkipList(seed=7)
for name, x in ex:
    r = getattr(sl, name)(x)
    print(f"{name:8} {x}: {r!s:5} levels (bottom first): {sl.levels()}")

for ops, want in [(ex, [True, True, True, True, False, False]), ([["remove", 5]], [False]),
                  ([["insert", -2], ["insert", -2], ["remove", -2], ["remove", -2]], [True, False, True, False])]:
    got, _ = run(ops)
    assert got == want == brute(ops), (ops, got)
    print(ops, "->", got)

# results never depend on the coin flips: seeds 0..5 and forced levels (all 1, all 16) agree with a set
random.seed(3401)
for _ in range(300):
    ops = [[random.choice(["insert", "contains", "remove"]), random.randint(-12, 12)] for _ in range(random.randint(1, 60))]
    want = brute(ops)
    for seed in range(6):
        assert run(ops, seed)[0] == want
    assert run(ops, level_fn=lambda: 1)[0] == want and run(ops, level_fn=lambda: 16)[0] == want
    lv = run(ops)[1].levels()
    assert not lv or lv[0] == sorted(set(lv[0])), "bottom level is sorted, no repeats"
print("300 seeded random op lists: same results for 6 seeds and for forced level 1 and 16, equal to a set")

# speed depends on the levels: 2000 inserts in increasing order, then 2000 lookups
keys = list(range(2000))
for name, fn in [("random levels", None), ("all level 1 (a sorted linked list)", lambda: 1)]:
    sl = SkipList(seed=1, level_fn=fn)
    for k in keys:
        sl.insert(k)
    sl.steps = 0
    for k in keys:
        sl.contains(k)
    print(f"{name}: average nodes stepped onto per lookup = {sl.steps / len(keys):.1f}")

# edge asserts
sl = SkipList()
assert sl.insert(0) and not sl.insert(0) and sl.contains(0) and sl.remove(0) and not sl.remove(0) and not sl.contains(0)
assert all(sl.insert(x) for x in (10**6, -10**6, 0)) and sl.levels()[0] == [-10**6, 0, 10**6]
print("edge asserts ok")
```

**Output (my run):**
```
insert   3: True  levels (bottom first): [[3], [3], [3]]
insert   1: True  levels (bottom first): [[1, 3], [1, 3], [3]]
contains 3: True  levels (bottom first): [[1, 3], [1, 3], [3]]
remove   3: True  levels (bottom first): [[1], [1]]
contains 3: False levels (bottom first): [[1], [1]]
insert   1: False levels (bottom first): [[1], [1]]
[['insert', 3], ['insert', 1], ['contains', 3], ['remove', 3], ['contains', 3], ['insert', 1]] -> [True, True, True, True, False, False]
[['remove', 5]] -> [False]
[['insert', -2], ['insert', -2], ['remove', -2], ['remove', -2]] -> [True, False, True, False]
300 seeded random op lists: same results for 6 seeds and for forced level 1 and 16, equal to a set
random levels: average nodes stepped onto per lookup = 10.9
all level 1 (a sorted linked list): average nodes stepped onto per lookup = 999.5
edge asserts ok
```

**Edge cases:**
- `remove` of an absent key: False and no change (`[['remove', 5]]` gives `[False]`).
- Duplicate insert: False and the structure is unchanged.
- Negative keys and keys up to 10^6 in absolute value: only `<` and `==` are used.
- Empty list: the head's pointers are all None; `contains` is False.
- A key that is the new minimum or maximum: `update[i]` is the head on every level for the minimum; the next pointer is None for the maximum.
- Level 16 cap: with up to 2,000 operations the cap is never the limit; it only bounds the head size.

**Follow-ups:**
- *What probability would you choose?* 1/2 is fine; 1/4 gives fewer pointers per node with slightly longer walks; the expected search cost stays O(log n).
- *Why not a balanced tree?* The tree has a worst-case guarantee; the skip list has an expected one, but is easier to code and to make lock-free for concurrent use.
- *Can I use it to get the k-th element?* Not without storing span lengths in the pointers (an "indexable" skip list); not in this question.

**Common mistakes:**
- Not keeping the `update` array, so you cannot splice on the higher levels.
- Forgetting to check whether the key is already present before inserting (duplicates get stored).
- Stepping right on `<=` instead of `<` (you overshoot the position to insert after).
- Saying the worst case is O(log n): it is expected, not worst-case.
- Depending on the random values in the results (a test that compares the levels instead of the answers).

### Q35 ⭐ 🔴 Expression add operators. `num` is a string of 1 to 8 digits and `target` is an integer with |target| <= 10^9. Insert the binary operators '+', '-' and '*' (or nothing, which joins digits into one multi-digit operand) between the digits so that the expression, evaluated with the usual precedence (multiplication first), equals `target`. An operand may not have a leading zero ('0' alone is fine; '05' and '00' are not). Return every such expression as a string, sorted ascending as Python strings, without duplicates; return an empty list if none exists. Recurse over the cut position while carrying the value so far and the last term, and for '*' use `value - last + last * operand` to undo the last addition; explain why that works and why the carried value avoids re-parsing the string at every leaf. State the upper bound of 4^(n-1) candidate fillings (each of the n - 1 gaps gets '+', '-', '*' or nothing), of which the leading-zero rule removes some. Depth is at most 8. In the answer include a dry run on the first example and a seeded random cross-check of your solution against enumerating all 4^(n-1) fillings and evaluating each with `eval` on small inputs. Example: num='2345', target=25 -> ['2+3+4*5']; num='105', target=5 -> ['1*0+5', '10-5']; num='00', target=0 -> ['0*0', '0+0', '0-0']; num='9', target=9 -> ['9']; num='9', target=0 -> [].
**Asked at:** Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Backtracking over cut positions with a carried value: choose the next operand (a cut), choose the operator before it, recurse, and undo by returning. The trick is carrying `(value, last)` so `*` can fix up precedence without re-parsing.

**Say this first (1 line):** "At each position I choose how many digits the next operand takes and which operator goes before it; I carry the running value and the last term, and for `*` I use `value - last + last * operand` to take the last term back out and put it back multiplied."

**Brute force:** For all `4^(n-1)` fillings of the `n - 1` gaps with `''`, `'+'`, `'-'`, `'*'`, build the string, drop it if any operand has a leading zero, `eval` it, and keep it when it equals `target`. Correct, and the oracle here (n <= 6 in the cross-check). It builds and parses 16,384 strings for n = 8.

**Optimal:**
- Recursion `dfs(i, expr, val, last)`: `i` is the next unused digit, `expr` the string so far, `val` the value of the expression so far under the usual precedence, `last` the signed last term (the one a following `*` would multiply).
- First operand: no operator before it; `val = last = int(tok)`.
- Later operands, `tok = num[i:j]`, `v = int(tok)`:
  - `+`: `val + v`, `last = v`.
  - `-`: `val - v`, `last = -v` (the subtracted term is the last term with sign).
  - `*`: `val - last + last * v`, `last = last * v`. Why it works: `val` already contains `last` added in, so remove it, then add `last * v`. Multiplication binds tighter, so it applies to the last term only. Example: `1-2*3`: after `1-2` we have `val = -1`, `last = -2`, so `-1 - (-2) + (-2) * 3 = -5 = 1 - 6`.
- Why carry the value: each leaf already has its value, so nothing is re-parsed or evaluated at the leaves; the brute force pays for an `eval` of a whole string per filling.
- Pruning rule (the only one used): an operand may not have a leading zero. When `num[i] == '0'` and the operand is longer than one digit, `break`: `'05'`, `'050'` and every longer operand from that start are illegal. A single `'0'` is fine.
- Undo: strings and numbers are passed by value, so returning from a call is the undo; nothing has to be restored.
- Output: collect leaves with `val == target`, then `sorted(...)`; each filling yields a different string, so there are no duplicates (the code asserts it). If none matches the list is empty.
- Node count compared with the unpruned search: the unpruned search has `4^(n-1)` fillings, 16,384 for n = 8, and `21,846` recursion calls in all. With the leading-zero rule the calls fall to 21,846 for `12345678` (no zeros, nothing to prune), 11,901 for `10203040`, 4,917 for `10000000` and 3,281 for `00000000`. The valid fillings are 16,384, 8,788, 3,280 and 2,187. So the rule never changes the bound, it only helps on inputs with zeros (see the table in the output).
- Depth: at most `n = 8` frames.
- No target-based pruning is used: with `*` the value can swing back (`9*9*9*0`), so a "too large already" cut would be wrong.

**Complexity:** Upper bound `4^(n-1)` leaves (each gap `+`, `-`, `*` or nothing); the leading-zero rule removes some. Each call does O(n) work (slicing and `int` on the operand, string concatenation), so about O(n * 4^(n-1)) worst case. For n = 8 that is about 22,000 calls. Space O(n) depth plus the output.

**Dry run:** `num = '105'`, `target = 5`. The tree is printed below (19 calls). Operands from index 0: `1`, `10`, `105`.
- `1`, then `0` with `+`, `-` or `*` (values `1`, `1`, and `1 - 1 + 1 * 0 = 0`), then `5` with each of the three operators: after `1+0` the totals are 6, -4 and 1; after `1-0` they are 6, -4 and 1; after `1*0` they are 5, -5 and 0. Only `1*0+5` equals 5 (HIT).
- `10`, then `5`: `10+5 = 15`, `10-5 = 5` (HIT), `10*5 = 50`.
- `105` alone: 105.
- No `'05'` operand ever appears: after `1`, a join of `0` and `5` is `05`, which is cut by the rule. Hits sorted: `['1*0+5', '10-5']`.

**Code:**
```python
import itertools
import random
import re

random.seed(3501)


def solve(num, target, zero_rule=True, trace=None):
    """Returns (sorted expressions, calls). calls counts every dfs call. zero_rule=False only exists
    to measure what the leading-zero rule prunes (its answers then include illegal operands)."""
    n = len(num)
    out = []
    calls = 0

    def dfs(i, expr, val, last, depth):
        nonlocal calls
        calls += 1
        if trace is not None:
            trace.append("  " * depth + f"i={i} expr={expr or '-'} val={val} last={last}" + (" HIT" if i == n and val == target else ""))
        if i == n:
            if val == target:
                out.append(expr)
            return
        for j in range(i + 1, n + 1):                 # operand = num[i:j]
            tok = num[i:j]
            if zero_rule and len(tok) > 1 and tok[0] == "0":
                break                                 # '0x...' and every longer operand starting here are illegal
            v = int(tok)
            if i == 0:
                dfs(j, tok, v, v, depth + 1)
            else:
                dfs(j, expr + "+" + tok, val + v, v, depth + 1)
                dfs(j, expr + "-" + tok, val - v, -v, depth + 1)
                dfs(j, expr + "*" + tok, val - last + last * v, last * v, depth + 1)   # undo last term, redo it times v

    dfs(0, "", 0, 0, 0)
    return sorted(out), calls


def brute(num, target):
    out = []
    for ops in itertools.product(["", "+", "-", "*"], repeat=len(num) - 1):
        e = num[0] + "".join(o + d for o, d in zip(ops, num[1:]))
        if any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", e)):
            continue
        if eval(e) == target:                         # eval applies the usual precedence
            out.append(e)
    return sorted(out)


# dry run: decision tree for '105', target 5
tr = []
res, calls = solve("105", 5, trace=tr)
print("\n".join(tr))
print("answer", res, "| dfs calls", calls)

for num, tg, want in [("2345", 25, ["2+3+4*5"]), ("105", 5, ["1*0+5", "10-5"]), ("00", 0, ["0*0", "0+0", "0-0"]),
                      ("9", 9, ["9"]), ("9", 0, [])]:
    got = solve(num, tg)[0]
    assert got == want == brute(num, tg), (num, tg, got)
    print(repr(num), tg, "->", got)

# why value - last + last * v works: '1-2*3' -> val after '1-2' is -1, last is -2
assert eval("1-2*3") == -1 - (-2) + (-2) * 3 == -5

# node counts: with the leading-zero rule against without it, against the 4^(n-1) leaves of the unpruned filling space
print("n  digits      4^(n-1)  calls without rule  calls with rule  valid leaves")
for num in ["12345678", "10203040", "00000000", "10000000", "11111111"]:
    n = len(num)
    c_without = solve(num, 0, zero_rule=False)[1]
    c_with = solve(num, 0)[1]
    leaves = sum(1 for _ in itertools.product(["", "+", "-", "*"], repeat=n - 1)
                 if not any(len(t) > 1 and t[0] == "0" for t in re.split(r"[+\-*]", num[0] + "".join(o + d for o, d in zip(_, num[1:])))))
    print(f"{n}  {num}  {4 ** (n - 1):>7}  {c_without:>18}  {c_with:>15}  {leaves:>12}")

# seeded random cross-check against eval over all 4^(n-1) fillings
for _ in range(300):
    n = random.randint(1, 6)
    num = "".join(random.choice("0123456789" if random.random() < 0.5 else "0012") for _ in range(n))
    tg = random.choice([0, random.randint(-30, 100), eval(num[0] + "".join(random.choice("+-*") + d for d in num[1:]))])
    got = solve(num, tg)[0]
    assert got == brute(num, tg) and got == sorted(set(got)), (num, tg)
print("300 seeded random cases: same sorted list as the eval enumeration, no duplicates")
assert solve("0", 0)[0] == ["0"] and solve("05", 5)[0] == ["0+5"] and solve("05", 0)[0] == ["0*5"] and solve("00", 0)[0] == ["0*0", "0+0", "0-0"]
assert solve("12345678", 10**9)[0] == [] and solve("99999999", 99999999)[0] == ["99999999"]
print("edge asserts ok")
```

**Output (my run):**
```
i=0 expr=- val=0 last=0
  i=1 expr=1 val=1 last=1
    i=2 expr=1+0 val=1 last=0
      i=3 expr=1+0+5 val=6 last=5
      i=3 expr=1+0-5 val=-4 last=-5
      i=3 expr=1+0*5 val=1 last=0
    i=2 expr=1-0 val=1 last=0
      i=3 expr=1-0+5 val=6 last=5
      i=3 expr=1-0-5 val=-4 last=-5
      i=3 expr=1-0*5 val=1 last=0
    i=2 expr=1*0 val=0 last=0
      i=3 expr=1*0+5 val=5 last=5 HIT
      i=3 expr=1*0-5 val=-5 last=-5
      i=3 expr=1*0*5 val=0 last=0
  i=2 expr=10 val=10 last=10
    i=3 expr=10+5 val=15 last=5
    i=3 expr=10-5 val=5 last=-5 HIT
    i=3 expr=10*5 val=50 last=50
  i=3 expr=105 val=105 last=105
answer ['1*0+5', '10-5'] | dfs calls 19
'2345' 25 -> ['2+3+4*5']
'105' 5 -> ['1*0+5', '10-5']
'00' 0 -> ['0*0', '0+0', '0-0']
'9' 9 -> ['9']
'9' 0 -> []
n  digits      4^(n-1)  calls without rule  calls with rule  valid leaves
8  12345678    16384               21846            21846         16384
8  10203040    16384               21846            11901          8788
8  00000000    16384               21846             3281          2187
8  10000000    16384               21846             4917          3280
8  11111111    16384               21846            21846         16384
300 seeded random cases: same sorted list as the eval enumeration, no duplicates
edge asserts ok
```

**Edge cases:**
- `'00'`, target 0: `['0*0', '0+0', '0-0']`; `'00'` joined is illegal.
- `'05'`, target 5: only `'0+5'` (`'05'` is illegal, `0-5` is -5, `0*5` is 0).
- One digit: `'9'` with 9 gives `['9']`; with 0 gives `[]`.
- Negative or large targets: `'12345678'` and 10^9 gives `[]`; the values stay far below 10^9 anyway.
- All same digits (`'99999999'`): the single join `99999999` matches itself.
- Overflow: Python ints do not overflow. Every term is below 10^8 (its digits are a subset of 8), so the sum of at most 8 terms stays below 8 * 10^8, inside 32 bits anyway.

**Follow-ups:**
- *Add parentheses or division?* The `value - last + last * v` trick no longer works; a recursion over split points returning a set of possible values per substring would be the approach.
- *How slow is the worst input?* About 22,000 calls for 8 digits, instant; the `4^(n-1)` growth only matters for longer strings.
- *Why `last = -v` for minus?* So that a following `*` multiplies the negative term: `1-2*3` is `1 - (2*3)`.

**Common mistakes:**
- Evaluating `'*'` as `val * v` (applies to the whole prefix, wrong precedence).
- Forgetting the sign in `last` after `-`.
- Allowing `'05'`, or breaking out of the whole recursion instead of just the operand loop when seeing a zero.
- Putting an operator before the first operand.
- Returning the list unsorted or with duplicates when the prompt asks for sorted and distinct.
