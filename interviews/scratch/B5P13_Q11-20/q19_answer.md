### Q19 ⭐⭐ 🟢 Excel column titles and numbers. `title` is a column title of 1 to 7 uppercase letters whose number is at most 2^31 - 1 (A = 1, ..., Z = 26, AA = 27, AB = 28, ..., AZ = 52, BA = 53, ...), and `number` is an integer with 1 <= number <= 2^31 - 1. Return `[number_of_title, title_of_number]`. This is base 26 with digits 1..26 and no zero digit (bijective numeration). Convert a title with `r = r * 26 + (ord(ch) - 64)` and a number with the loop `n, d = divmod(n - 1, 26)` taking letter `chr(65 + d)`, then reverse; explain why the `n - 1` is needed (there is no zero digit, so plain base 26 would turn 26 into 'A0'-style nonsense) and why both directions are O(length), about log26 of the value. In the answer include a dry run on the first example and a seeded random cross-check of your solution against an explicit table of all titles up to length 4 on small inputs. Example: title='AB', number=28 -> [28, 'AB']; title='A', number=1 -> [1, 'A']; title='ZY', number=701 -> [701, 'ZY']; title='FXSHRXW', number=2147483647 -> [2147483647, 'FXSHRXW'].
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
