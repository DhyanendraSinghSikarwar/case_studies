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
