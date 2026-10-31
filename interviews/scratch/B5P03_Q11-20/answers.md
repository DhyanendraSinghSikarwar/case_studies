### Q11 ⭐⭐⭐ 🟡 Multiply strings. `num1` and `num2` are non-negative integers written as decimal strings (1 <= len <= 200, no leading zeros except the single string '0'). Return their product as a string without converting either whole string to an int and without a big-integer library. Do schoolbook multiplication into an array of len1+len2 digit slots, handle carries and strip leading zeros, and state the O(len1 * len2) cost (mention that Python's own int multiplication is faster than this and what Karatsuba is, at concept level). Example: ('2','3') -> '6'; ('123','456') -> '56088'; ('0','9999') -> '0'; ('99','99') -> '9801'.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Schoolbook arithmetic on digit arrays. Digit `i` of one number times digit `j` of the other lands in slot `i + j + 1` (carry goes to `i + j`).

**Say this first (1 line):** "Allocate len1 + len2 digit slots, multiply every digit pair into its slot, carry as I go, strip leading zeros. O(len1 * len2)."

**Brute force:** `str(int(a) * int(b))`. Correct, and my checker, but the question bans it. The other brute force is repeated addition of shifted partial products as strings: it works but costs an extra string add per digit.

**Optimal:**
- A product of an n-digit and an m-digit number has at most n + m digits, so `res = [0] * (n + m)`.
- Loop `i` from the right of `a`, `j` from the right of `b`.
- `cur = res[i + j + 1] + da * db`. Keep `cur % 10` in that slot. Push `cur // 10` into slot `i + j`.
- Invariant: when I finish row `i`, slots `i+1 .. n+m-1` hold single digits. Slot `i` may hold a carry that the next row fixes.
- Strip leading zeros at the end. Special-case `'0'` so the answer is `'0'`, not `''`.

**Complexity:** Time O(n * m): two nested loops, constant work inside. Space O(n + m) for the slots.
- Python's own `int` multiply is faster: it works on 30-bit internal digits, not decimal digits, and CPython switches to Karatsuba for big operands.
- Karatsuba (concept only): split each number in two halves and do 3 half-size multiplications instead of 4, so about O(n^1.585) instead of O(n^2). I do not need it for 200 digits.

**Dry run:** `'99' * '99'`, slots `[0,0,0,0]`.
| i, j | slot | cur | slot digit | carry to slot-1 | res after |
|---|---|---|---|---|---|
| 1, 1 | 3 | 0+81 | 1 | 8 into slot 2 | [0,0,8,1] |
| 1, 0 | 2 | 8+81=89 | 9 | 8 into slot 1 | [0,8,9,1] |
| 0, 1 | 2 | 9+81=90 | 0 | 9 into slot 1 | [0,17,0,1] |
| 0, 0 | 1 | 17+81=98 | 8 | 9 into slot 0 | [9,8,0,1] |

No leading zero to strip. Answer `'9801'`.

**Code:**
```python
import random


def mul_brute(a, b):
    # reference only: uses Python's big int, which the real answer must avoid
    return str(int(a) * int(b))


def mul_school(a, b):
    if a == "0" or b == "0":
        return "0"
    n, m = len(a), len(b)
    res = [0] * (n + m)
    for i in range(n - 1, -1, -1):
        da = ord(a[i]) - 48
        for j in range(m - 1, -1, -1):
            cur = res[i + j + 1] + da * (ord(b[j]) - 48)
            res[i + j + 1] = cur % 10
            res[i + j] += cur // 10
    k = 0
    while k < len(res) - 1 and res[k] == 0:
        k += 1
    return "".join(map(str, res[k:]))


examples = [("2", "3", "6"), ("123", "456", "56088"), ("0", "9999", "0"), ("99", "99", "9801")]
for a, b, want in examples:
    got = mul_school(a, b)
    assert got == mul_brute(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert mul_school("9" * 200, "9" * 200) == mul_brute("9" * 200, "9" * 200)  # max size
assert mul_school("1", "1") == "1"
assert mul_school("10", "10") == "100"
assert mul_school("9999", "0") == "0"
assert mul_school("5", "5") == "25"

rng = random.Random(11)
cases = 0
for _ in range(1500):
    a = str(rng.randint(0, 10 ** rng.randint(1, 12)))
    b = str(rng.randint(0, 10 ** rng.randint(1, 12)))
    assert mul_school(a, b) == mul_brute(a, b), (a, b)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('2', '3') -> 6
('123', '456') -> 56088
('0', '9999') -> 0
('99', '99') -> 9801
random cross-check passed: 1500 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- Either input `'0'`: return `'0'` early (otherwise the strip loop would leave `'0'` anyway, but the early return is clearer).
- Product shorter than n + m digits (like `'10' * '10'` is 3 digits, not 4): the strip handles it.
- 200 by 200 digits: 40,000 inner steps, trivial.
- Slot `res[i + j]` can temporarily exceed 9 before its own turn; that is fine because it is normalised when it becomes `i + j + 1` for a later pair.

**Follow-ups:**
- *Why n + m slots?* Product < 10^n * 10^m = 10^(n+m), so at most n + m digits.
- *Faster?* Karatsuba, or FFT-based multiplication for huge inputs; real libraries (and CPython's `int`) already do this.
- *Add two numbers given as strings?* Same carry idea, one pass; see Add strings later in this part.

**Common mistakes:**
- Returning `'000'` or `''` for a zero product.
- Writing the carry into the wrong slot (`i + j + 1` is the digit slot, `i + j` the carry slot).
- Iterating left to right, so carries flow the wrong way.
- Calling `int()` on the inputs "just for the digits" and breaking the rule.

### Q12 ⭐⭐⭐ 🟡 Repeated substring pattern. Given `s` (1 <= len <= 10^4), decide whether it can be built by repeating some shorter non-empty block two or more times. Give the divisor-length check, the `s in (s + s)[1:-1]` trick with a proof sketch, and the prefix-function (KMP failure array) solution where the candidate period is n - pi[n-1]. Example: 'abab' -> True; 'aba' -> False; 'abcabcabcabc' -> True; 'a' -> False.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports

**Pattern:** Periodicity and borders. A string is a repeat of a block exactly when its smallest period divides its length and is shorter than the length.

**Say this first (1 line):** "Check divisor lengths for brute force; the neat way is s in (s+s)[1:-1]; the linear-time-guaranteed way is the prefix function, period = n - pi[n-1]."

**Brute force:** For each length `k` that divides `n` (k < n), test `s == s[:k] * (n // k)`. Each test is O(n), and a number up to 10^4 has at most 64 divisors, so about O(n * d(n)) in the worst case. Fine for n = 10^4.

**Optimal:**
- *Doubling trick:* `s in (s + s)[1:-1]`.
  - If `s = t * k` with k >= 2, then `s + s = t * 2k`. `s` also appears starting at offset `len(t)`, which is neither 0 nor n, so it survives when I drop the first and last character.
  - Conversely, if `s` occurs in `s + s` at offset `p` with 0 < p < n, then rotating `s` by `p` gives `s` back. That means `s = uv = vu`, and strings that commute are powers of one common word. So `s` has a block shorter than itself that repeats.
- *Prefix function:* `pi[i]` is the length of the longest proper prefix of `s[:i+1]` that is also a suffix. For the whole string, `b = pi[n-1]` is the longest border. The smallest period is `p = n - b`. The string is a repeat iff `p < n` (that is, `b > 0`) and `n % p == 0`.
- Invariant for the prefix function: `k` is always the length of the current border; on a mismatch I fall back to `pi[k-1]`, never restarting from 0.

**Complexity:** Prefix function: O(n) time, O(n) space; the `while` loop falls back at most as often as `k` grew in total (amortised). Doubling trick: building the doubled string is O(n) and the `in` test is a substring search. Python's `str.find` is fast in practice, and I believe recent CPython versions use a linear two-way algorithm for long needles, but I did not time or verify that here, so I would cite the prefix function when asked for a guaranteed O(n).

**Dry run:** `s = 'abcabcabcabc'`, n = 12.
| i | char | k before | action | pi[i] |
|---|---|---|---|---|
| 1 | b | 0 | b != a | 0 |
| 2 | c | 0 | c != a | 0 |
| 3 | a | 0 | match | 1 |
| 4 | b | 1 | match | 2 |
| 5 | c | 2 | match | 3 |
| 6..11 | a b c a b c | 3.. | keeps matching | 4,5,6,7,8,9 |

`pi[11] = 9`, so `p = 12 - 9 = 3`, `12 % 3 == 0`, True. For `'aba'`: `pi = [0,0,1]`, `p = 2`, `3 % 2 != 0`, False.

**Code:**
```python
import random


def rep_brute(s):
    n = len(s)
    return any(s == s[:k] * (n // k) for k in range(1, n) if n % k == 0)


def rep_double(s):
    return s in (s + s)[1:-1]


def prefix_function(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def rep_kmp(s):
    n = len(s)
    p = n - prefix_function(s)[-1]
    return p < n and n % p == 0


examples = [("abab", True), ("aba", False), ("abcabcabcabc", True), ("a", False)]
for s, want in examples:
    assert rep_brute(s) == rep_double(s) == rep_kmp(s) == want, s
    print(repr(s), "->", rep_kmp(s))

assert prefix_function("abcabc") == [0, 0, 0, 1, 2, 3]
assert rep_kmp("aaaa") and rep_double("aaaa")
assert not rep_kmp("abaab") and not rep_double("abaab")
assert not rep_kmp("abcab")            # period 3 but 5 % 3 != 0
assert rep_kmp("ab" * 5000) and not rep_kmp("a" * 9999 + "b")  # max size

rng = random.Random(12)
cases = 0
for _ in range(3000):
    if rng.random() < 0.5:
        s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 12)))
    else:
        blk = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
        s = blk * rng.randint(1, 4)
    assert rep_brute(s) == rep_double(s) == rep_kmp(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'abab' -> True
'aba' -> False
'abcabcabcabc' -> True
'a' -> False
random cross-check passed: 3000 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- Length 1: `pi = [0]`, `p = 1 = n`, not a repeat (needs two or more copies). The doubling trick gives `(s+s)[1:-1] = ''`, and `'a' in ''` is False.
- `'abcab'`: border 2, period 3, but 3 does not divide 5, so False. Forgetting the divisibility test is the classic bug.
- `'aaaa'`: border 3, period 1, True.
- Length 10^4: trivial.

**Follow-ups:**
- *Smallest repeating block?* Return `s[:p]` when the test passes.
- *Why not just test `p < n`?* Because a border can exist without the string being periodic in whole blocks (`'abcab'`).
- *Z-function version?* The smallest `p` dividing `n` with `z[p] + p == n`.

**Common mistakes:**
- Not slicing `[1:-1]`, so `s in s + s` is always True.
- Missing the `n % p == 0` check.
- Rebuilding the prefix function with a restart from 0 on mismatch (turns O(n) into O(n^2)).
- Treating length 1 as a repeat.

### Q13 ⭐⭐⭐ 🟡 Basic calculator without parentheses, in one pass. `expr` is a string (1 <= len <= 3*10^5) of non-negative integers, spaces and the operators + - * /, with no parentheses and no unary minus; division truncates toward zero and the input is valid. Evaluate it in a single left-to-right parse, keeping only the running total, the current 'last term' and the pending operator (multiplication and division fold into the last term; plus and minus flush it) rather than designing a stack of operands. The stack-based families (nested parentheses, monotonic stacks) are Part 4. Example: '3+2*2' -> 7; ' 3/2 ' -> 1; ' 3+5 / 2 ' -> 5; '14-3/2' -> 13; '10-20/3' -> 4.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** One-pass expression parsing with a "last term" accumulator. Precedence is handled by folding `*` and `/` into the last term, so I never need a stack.

**Say this first (1 line):** "Scan once keeping total, last term and the pending operator; on each operator I apply the pending one: plus and minus flush the last term into total, star and slash fold into it. O(n) time, O(1) space."

**Brute force:** Tokenise, then run two passes: first collapse every `*` and `/`, then evaluate the remaining `+` and `-`. Same O(n) time but O(n) space for the token list. That is my checker below. (Calling `eval` is not a real answer, and Python's `/` also gives a float.)

**Optimal:**
- State: `total` (finished terms), `last` (the term being built, with its sign), `num` (digits being read), `op` (operator that came before `num`).
- Read digits into `num`. When I see an operator (or the end), apply `op` to `num`:
  - `+`: `total += last; last = num`.
  - `-`: `total += last; last = -num`.
  - `*`: `last *= num`.
  - `/`: truncate toward zero.
- Then set `op` to the new operator and reset `num`.
- A sentinel `'+'` appended to the input flushes the last number. Answer is `total + last`.
- Invariant: `total + last` equals the value of everything parsed so far, treating the unfinished term as complete.
- Truncation: Python's `//` floors, so `-5 // 2 = -3`. Use `q = abs(last) // num` and restore the sign.

**Complexity:** Time O(n), one pass, each character touched once. Space O(1) beyond the input copy; `expr + "+"` makes a copy of length n + 1, which I could avoid with an index check.

**Dry run:** `'3+2*2'` (sentinel `+` at the end).
| char | op before | action | total | last |
|---|---|---|---|---|
| 3 | + | num = 3 | 0 | 0 |
| + | + | total += 0, last = 3 | 0 | 3 |
| 2 | + | num = 2 | 0 | 3 |
| * | + | total += 3, last = 2 | 3 | 2 |
| 2 | * | num = 2 | 3 | 2 |
| + (sentinel) | * | last = 2 * 2 | 3 | 4 |

Answer `3 + 4 = 7`.

**Code:**
```python
import random


def calc_brute(expr):
    # reference: Python eval with floor division replaced by truncation via tokens
    toks, i = [], 0
    while i < len(expr):
        c = expr[i]
        if c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            toks.append(int(expr[i:j])); i = j
        elif c in "+-*/":
            toks.append(c); i += 1
        else:
            i += 1
    # evaluate * and / first, then + and -
    out = [toks[0]]
    k = 1
    while k < len(toks):
        op, v = toks[k], toks[k + 1]
        if op == "*":
            out[-1] *= v
        elif op == "/":
            q = abs(out[-1]) // v
            out[-1] = q if out[-1] >= 0 else -q
        else:
            out += [op, v]
        k += 2
    total = out[0]
    for k in range(1, len(out), 2):
        total = total + out[k + 1] if out[k] == "+" else total - out[k + 1]
    return total


def calc(expr):
    total, last, num, op = 0, 0, 0, "+"
    for ch in expr + "+":   # sentinel flushes the final number
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                total += last; last = num
            elif op == "-":
                total += last; last = -num
            elif op == "*":
                last = last * num
            else:
                q = abs(last) // num
                last = q if last >= 0 else -q   # truncate toward zero
            op, num = ch, 0
    return total + last


examples = [("3+2*2", 7), (" 3/2 ", 1), (" 3+5 / 2 ", 5), ("14-3/2", 13), ("10-20/3", 4)]
for e, want in examples:
    got = calc(e)
    assert got == calc_brute(e) == want, (e, got)
    print(repr(e), "->", got)

assert calc("0") == 0
assert calc("7") == 7
assert calc("1-1+1") == 1
assert calc("2*3*4") == 24
assert calc("1-2*3/4") == 0        # 6/4 truncates to 1, then 1 - 1
assert calc("1-6/4") == 0          # 1 - 1
assert calc("0-5/2") == -2         # last = -5, then -5/2 truncates to -2, not -3
assert calc("100000*100000*100000") == 10 ** 15   # no overflow in Python
assert calc("1+" * 1000 + "1") == 1001

rng = random.Random(13)
cases = 0
for _ in range(3000):
    parts = [str(rng.randint(1, 20))]
    for _ in range(rng.randint(0, 6)):
        parts.append(rng.choice("+-*/"))
        parts.append(str(rng.randint(1, 20)))
    e = "".join(p if rng.random() < 0.8 else " " + p + " " for p in parts)
    assert calc(e) == calc_brute(e), e
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'3+2*2' -> 7
' 3/2 ' -> 1
' 3+5 / 2 ' -> 5
'14-3/2' -> 13
'10-20/3' -> 4
random cross-check passed: 3000 cases
```
All five examples in the prompt are correct.

**Edge cases:**
- Spaces anywhere: skipped by the `ch != " "` test, including the leading and trailing ones.
- Multi-digit numbers: handled by `num * 10 + digit`.
- Truncation toward zero: `'0-5/2'` gives `-2`, not `-3`, because `last = -5` and I truncate with `abs`.
- Only a number (`'7'`): the sentinel flushes it.
- Python has no overflow, so `100000*100000*100000` is fine. In C++ or Java this needs a wider type.
- Length 3*10^5: one loop, no recursion.

**Follow-ups:**
- *Add parentheses?* That needs a stack or recursion; the stack-based families belong to Part 4.
- *Unary minus?* Track whether the previous token was an operator and treat a leading `-` as `0 -`.
- *Division by zero?* The prompt says input is valid; in real code raise a clear error.

**Common mistakes:**
- Using `int(a / b)` (float rounding) or `a // b` (floors for negatives).
- Forgetting to flush the final number (no sentinel).
- Applying the operator that follows the number instead of the one that precedes it.
- Evaluating strictly left to right and getting `3+2*2 = 10`.

### Q14 ⭐⭐ 🟢 Add strings. `num1` and `num2` are non-negative decimal strings (len <= 10^4) with no leading zeros except '0'. Return their sum as a string without converting the whole inputs to int. Walk from the right with a carry, then reverse; explain why building the result by prepending would be O(n^2). Example: ('11','123') -> '134'; ('456','77') -> '533'; ('0','0') -> '0'; ('999','1') -> '1000'.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Right-to-left carry loop (digit-by-digit arithmetic), building output in a list and reversing once.

**Say this first (1 line):** "Two indices from the right, a carry, append each digit to a list, reverse at the end; prepending would be O(n^2)."

**Brute force:** `str(int(a) + int(b))`. It is my checker, and the question bans it. In Python 3.13 it also has a real limit: converting a string of more than 4300 digits raises `ValueError` by default (see the output below). That is a good reason the manual loop is not just an exercise for 10^4-digit inputs.

**Optimal:**
- `i`, `j` start at the last index of each string; `carry = 0`.
- Loop while `i >= 0 or j >= 0 or carry`. Add whichever digits exist plus the carry.
- Append `s % 10` to a list, set `carry = s // 10`.
- Reverse the list and join.
- Invariant: after each step the list holds the low digits of the sum, and `carry` is what is still owed to the next position.

**Complexity:** Time O(max(n, m)): one pass. Space O(max(n, m)) for the digits. Prepending (`res = digit + res`) copies the whole string each step, so n steps cost 1 + 2 + ... + n = O(n^2). `list.append` is amortised O(1) and `''.join` is O(n) once. (`list.insert(0, x)` has the same O(n^2) problem.)

**Dry run:** `'999' + '1'`.
| i, j | digits | carry in | sum | digit out | carry out |
|---|---|---|---|---|---|
| 2, 0 | 9 + 1 | 0 | 10 | 0 | 1 |
| 1, - | 9 | 1 | 10 | 0 | 1 |
| 0, - | 9 | 1 | 10 | 0 | 1 |
| - | none | 1 | 1 | 1 | 0 |

List `[0,0,0,1]`, reversed `'1000'`. The extra pass happens because `carry` keeps the loop alive after both indices run out.

**Code:**
```python
import random


def add_brute(a, b):
    return str(int(a) + int(b))


def add_strings(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out = []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0:
            s += ord(a[i]) - 48; i -= 1
        if j >= 0:
            s += ord(b[j]) - 48; j -= 1
        out.append(chr(48 + s % 10))
        carry = s // 10
    return "".join(reversed(out))


examples = [("11", "123", "134"), ("456", "77", "533"), ("0", "0", "0"), ("999", "1", "1000")]
for a, b, want in examples:
    got = add_strings(a, b)
    assert got == add_brute(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert add_strings("9" * 10000, "1") == "1" + "0" * 10000      # max size, long carry chain
big = add_strings("9" * 10000, "9" * 10000)
assert big == "1" + "9" * 9999 + "8"
try:
    add_brute("9" * 10000, "9" * 10000)
except ValueError as e:
    print("int() on 10000 digits:", str(e)[:44])   # default limit is 4300 digits in Python 3.13
assert add_strings("1", "9") == "10"
assert add_strings("0", "5") == "5"

rng = random.Random(14)
cases = 0
for _ in range(2000):
    a = str(rng.randint(0, 10 ** rng.randint(1, 30)))
    b = str(rng.randint(0, 10 ** rng.randint(1, 30)))
    assert add_strings(a, b) == add_brute(a, b), (a, b)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('11', '123') -> 134
('456', '77') -> 533
('0', '0') -> 0
('999', '1') -> 1000
int() on 10000 digits: Exceeds the limit (4300 digits) for integer 
random cross-check passed: 2000 cases
```
All four examples in the prompt are correct. The extra line shows the Python 3.13 default limit on `int()` of a long digit string, observed in this run.

**Edge cases:**
- Different lengths: the shorter one just stops contributing.
- Final carry (`'999' + '1'`, `'9' * 10000 + '1'`): the `or carry` in the loop condition adds the new leading digit.
- `'0' + '0'`: one iteration gives `'0'`.
- Inputs have no leading zeros, so the output has none either (the sum of two non-zero-leading strings cannot start with 0).

**Follow-ups:**
- *Can I avoid the reverse?* Pre-allocate a list of size max + 1 and fill from the right, then strip a leading `0`.
- *Add many numbers?* Same idea per column, or fold pairwise.
- *Subtract strings?* A borrow instead of a carry, and compare magnitudes first.

**Common mistakes:**
- Forgetting the final carry.
- Building the result with `res = str(digit) + res`.
- Using `int(ch)` with a lookup table when `ord(ch) - 48` is enough (minor, not wrong).
- Appending digits and forgetting to reverse.

### Q15 ⭐⭐ 🟢 Add binary. `a` and `b` are non-empty binary strings (len <= 10^4). Return their sum as a binary string using a right-to-left carry loop. Then state what `bin(int(a, 2) + int(b, 2))` costs and why interviewers still ask the manual loop. Example: ('11','1') -> '100'; ('1010','1011') -> '10101'; ('0','0') -> '0'.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Same right-to-left carry loop as decimal addition, in base 2.

**Say this first (1 line):** "Walk both strings from the right with a carry; bit is sum & 1, carry is sum >> 1; reverse at the end. The one-liner works too, but I should be able to do the loop."

**Brute force:** `bin(int(a, 2) + int(b, 2))[2:]` (the slice drops the `'0b'` prefix). Cost: parsing a binary string is O(n) because base 2 is a power of two, the addition is O(n), and `bin` is O(n). So it is linear, and in Python 3.13 the 4300-digit limit on int-string conversion does not apply to power-of-two bases (my run below adds a 10,000-bit string with it). Interviewers still ask the loop because it tests carry handling, indices and edge cases, and because in C++ or Java the big-integer shortcut does not exist.

**Optimal:**
- `i`, `j` at the ends, `carry = 0`.
- While any index is valid or `carry` is set: `s = carry + bit_a + bit_b`.
- Output bit `s & 1`, carry `s >> 1` (s is at most 3, so carry is 0 or 1).
- Reverse and join.
- Invariant: the output list holds the low bits of the sum; `carry` is 0 or 1.

**Complexity:** Time O(max(n, m)), space O(max(n, m)). Appending to a list and reversing once avoids the O(n^2) prepend.

**Dry run:** `'1010' + '1011'`.
| position (from right) | bits | carry in | s | out | carry out |
|---|---|---|---|---|---|
| 0 | 0 + 1 | 0 | 1 | 1 | 0 |
| 1 | 1 + 1 | 0 | 2 | 0 | 1 |
| 2 | 0 + 0 | 1 | 1 | 1 | 0 |
| 3 | 1 + 1 | 0 | 2 | 0 | 1 |
| after | none | 1 | 1 | 1 | 0 |

Out list `[1,0,1,0,1]`, reversed `'10101'`.

**Code:**
```python
import random


def add_builtin(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]


def add_binary(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out = []
    while i >= 0 or j >= 0 or carry:
        s = carry
        if i >= 0:
            s += a[i] == "1"; i -= 1
        if j >= 0:
            s += b[j] == "1"; j -= 1
        out.append("1" if s & 1 else "0")
        carry = s >> 1
    return "".join(reversed(out)) or "0"


examples = [("11", "1", "100"), ("1010", "1011", "10101"), ("0", "0", "0")]
for a, b, want in examples:
    got = add_binary(a, b)
    assert got == add_builtin(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert add_binary("1" * 10000, "1") == "1" + "0" * 10000 == add_builtin("1" * 10000, "1")  # int(.., 2) has no 4300-digit limit
assert add_binary("0", "1") == "1"
assert add_binary("00000", "0") == "00000"   # leading zeros (outside the contract) are not stripped
assert add_binary("1", "1") == "10"

rng = random.Random(15)
cases = 0
for _ in range(2000):
    a = rng.choice(["0", "1" + "".join(rng.choice("01") for _ in range(rng.randint(0, 39)))])
    b = rng.choice(["0", "1" + "".join(rng.choice("01") for _ in range(rng.randint(0, 39)))])
    assert int(add_binary(a, b), 2) == int(a, 2) + int(b, 2), (a, b)
    assert add_binary(a, b) == add_builtin(a, b), (a, b)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('11', '1') -> 100
('1010', '1011') -> 10101
('0', '0') -> 0
random cross-check passed: 2000 cases
```
All three examples in the prompt are correct.

**Edge cases:**
- `'0' + '0'` gives `'0'`.
- `'1' * 10000 + '1'` gives `'1'` followed by 10,000 zeros: a full carry chain.
- Unequal lengths: handled by the index checks.
- Inputs with leading zeros are outside the contract, and the loop does not strip them (`'00000' + '0'` stays `'00000'`).

**Follow-ups:**
- *Why does `int(a, 2)` not hit the digit limit?* The limit applies to non-power-of-two bases; I observed it for decimal in Python 3.13, and the run above shows the 10,000-bit binary case works.
- *Do it without extra memory?* Not with immutable strings; use a bytearray and fill from the right.
- *Add without `+`?* XOR for the sum and AND-then-shift for the carry (a bit-manipulation question, not this part).

**Common mistakes:**
- Forgetting the last carry.
- Comparing characters as ints (`a[i] == 1` instead of `'1'`).
- Leaving the `'0b'` prefix on the answer.
- Doing `res = bit + res`.

### Q16 ⭐⭐ 🟢 Longest palindrome you can build. Given a string `s` of letters (case-sensitive, len <= 2000), return the length of the longest palindrome that can be built by reordering some or all of its letters, each used at most as often as it appears. Count letters; every pair contributes 2 and at most one leftover odd letter can sit in the middle. Explain why this is a counting problem, not a substring problem. Example: 'abccccdd' -> 7; 'a' -> 1; 'Aa' -> 1; 'aaabbb' -> 5.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Frequency counting. Rearranging letters means only the multiset matters, so this is a counting problem and not a substring problem.

**Say this first (1 line):** "Count letters. Every letter contributes its even part to the palindrome, and if any letter has an odd count, one extra letter can sit in the middle."

**Brute force:** Try every sub-multiset of the letters and every ordering, keep the longest that reads the same both ways. Exponential, so only usable on 8 letters, but it is my checker.

**Optimal:**
- A palindrome mirrors around its centre, so every letter except possibly the middle one appears in a pair.
- For a letter with count `c`, I can use `c // 2` pairs, which is `c // 2 * 2` letters.
- If any count is odd, one leftover letter can go in the middle: add 1 once.
- Answer = total of the even parts + (1 if any odd count else 0).
- Case-sensitive: `'A'` and `'a'` are different letters.
- Why not a substring problem: I may reorder and skip letters, so positions are irrelevant. (If it asked for the longest palindromic substring, order would matter, and that is a different question.)

**Complexity:** Time O(n) to count, then O(k) over the distinct letters (k <= 52 here). Space O(k).

**Dry run:** `'abccccdd'`.
| letter | count | pairs used | leftover |
|---|---|---|---|
| a | 1 | 0 | 1 |
| b | 1 | 0 | 1 |
| c | 4 | 4 | 0 |
| d | 2 | 2 | 0 |

Pairs give 6. An odd count exists, so add 1: 7. One valid palindrome is `'dccaccd'`.

**Code:**
```python
import random
from collections import Counter
from itertools import permutations


def lp_brute(s):
    # try every ordering of every sub-multiset (tiny inputs only)
    best = 0
    n = len(s)
    for mask in range(1 << n):
        sub = [s[i] for i in range(n) if mask >> i & 1]
        if len(sub) <= best:
            continue
        if any(p == p[::-1] for p in set(permutations(sub))):
            best = len(sub)
    return best


def lp_count(s):
    pairs = 0
    odd = False
    for c in Counter(s).values():
        pairs += c // 2 * 2
        odd = odd or c % 2 == 1
    return pairs + (1 if odd else 0)


examples = [("abccccdd", 7), ("a", 1), ("Aa", 1), ("aaabbb", 5)]
for s, want in examples:
    got = lp_count(s)
    assert got == lp_brute(s) == want, (s, got)
    print(repr(s), "->", got)

assert lp_count("") == 0
assert lp_count("ab") == 1
assert lp_count("aaaa") == 4
assert lp_count("aA" * 1000) == 2000              # case-sensitive: 1000 a and 1000 A, all paired
assert lp_count("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") == 1  # 52 singletons
assert lp_count("a" * 2000) == 2000

rng = random.Random(16)
cases = 0
for _ in range(400):
    s = "".join(rng.choice("abcA") for _ in range(rng.randint(0, 8)))
    assert lp_count(s) == lp_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'abccccdd' -> 7
'a' -> 1
'Aa' -> 1
'aaabbb' -> 5
random cross-check passed: 400 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- Empty string: 0 (the prompt promises letters, but the code handles it).
- All letters distinct: 1.
- `'aaaa'`: 4, no middle needed.
- `'aaabbb'`: 5, not 6; two odd counts still give only one middle letter (the extra `a` and `b` cannot both fit).
- Case-sensitivity: `'Aa'` is 1.

**Follow-ups:**
- *Build the palindrome, not just the length?* Put half of each pair on the left, the odd letter in the middle, then mirror.
- *Can the letters be rearranged into a palindrome at all (all letters used)?* True iff at most one letter has an odd count.
- *Longest palindromic substring?* Different problem, expand around centres (earlier in this part).

**Common mistakes:**
- Adding 1 for every odd count instead of once.
- Counting each letter once instead of in pairs.
- Lowercasing the input, which breaks the case-sensitive rule.
- Solving it as a substring problem and writing an O(n^2) expansion.

### Q17 ⭐⭐ 🟢 Reverse only the vowels. Given `s` (len <= 3*10^5, printable ASCII), reverse the order of its vowels (a, e, i, o, u in either case) and leave every other character where it is. Use two pointers on a list of characters, each skipping consonants, and a set for O(1) vowel tests. Example: 'IceCreAm' -> 'AceCreIm'; 'leetcode' -> 'leotcede'; 'xyz' -> 'xyz'.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Opposite-ends two pointers with skipping, plus a set for O(1) membership.

**Say this first (1 line):** "Convert to a list, move a left pointer to the next vowel and a right pointer to the previous vowel, swap, and continue until they meet. O(n) time."

**Brute force:** Collect the vowels in order, reverse that list, then rebuild the string and drop the next reversed vowel into each vowel slot. O(n) time, O(n) extra space for the vowel list. Also correct; it is my checker.

**Optimal:**
- Strings are immutable in Python, so `a = list(s)` first.
- `i = 0`, `j = n - 1`.
- Advance `i` while it is not on a vowel; retreat `j` while it is not on a vowel; keep `i < j` in both inner loops.
- Swap `a[i]` and `a[j]`, then step both inward.
- Invariant: positions left of `i` and right of `j` already hold their final characters.
- Vowels are a `set('aeiouAEIOU')`, so the test is O(1). `y` is not a vowel here.

**Complexity:** Time O(n), each pointer moves one way. Space O(n) for the character list (unavoidable with immutable strings); the pointer logic itself is O(1).

**Dry run:** `'IceCreAm'`, indices I0 c1 e2 C3 r4 e5 A6 m7.
| step | i, j | action | list after |
|---|---|---|---|
| 1 | 0, 7 -> 6 | i is on I (vowel); j skips m and lands on A; swap | A c e C r e I m |
| 2 | 1 -> 2, 5 | i skips c to e; j is on e; swap (same letter) | A c e C r e I m |
| 3 | 3 -> 4, 4 | i skips C and r and meets j; the swap is a self-swap | A c e C r e I m |

Result `'AceCreIm'`.

**Code:**
```python
import random

VOWELS = set("aeiouAEIOU")


def rv_brute(s):
    v = [c for c in s if c in VOWELS][::-1]
    it = iter(v)
    return "".join(next(it) if c in VOWELS else c for c in s)


def rv_two_pointers(s):
    a = list(s)
    i, j = 0, len(a) - 1
    while i < j:
        while i < j and a[i] not in VOWELS:
            i += 1
        while i < j and a[j] not in VOWELS:
            j -= 1
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1
    return "".join(a)


examples = [("IceCreAm", "AceCreIm"), ("leetcode", "leotcede"), ("xyz", "xyz")]
for s, want in examples:
    got = rv_two_pointers(s)
    assert got == rv_brute(s) == want, (s, got)
    print(repr(s), "->", repr(got))

assert rv_two_pointers("") == ""
assert rv_two_pointers("a") == "a"
assert rv_two_pointers("aeiou") == "uoiea"
assert rv_two_pointers("AbcdE") == "EbcdA"
assert rv_two_pointers("y") == "y"                       # y is not a vowel here
assert rv_two_pointers("bcd" * 100000) == "bcd" * 100000  # max size, no vowels
big = "ab" * 150000
assert rv_two_pointers(big) == big                        # all vowels equal 'a'

rng = random.Random(17)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("aeiouAEIOUbcxyz ! ") for _ in range(rng.randint(0, 12)))
    assert rv_two_pointers(s) == rv_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'IceCreAm' -> 'AceCreIm'
'leetcode' -> 'leotcede'
'xyz' -> 'xyz'
random cross-check passed: 3000 cases
```
All three examples in the prompt are correct.

**Edge cases:**
- No vowels: pointers meet, nothing swaps.
- One vowel: pointers meet on it, nothing changes.
- Upper and lower case: both are in the set.
- Length 3*10^5: iterative, so the recursion limit is irrelevant.
- Empty string: `j = -1`, the loop does not run.

**Follow-ups:**
- *Reverse only letters?* Same code with `isalpha`.
- *Why not `s[::-1]` tricks?* They reverse everything; here only the vowel subsequence moves.
- *Include `y`?* Add it to the set; the algorithm is unchanged.

**Common mistakes:**
- Forgetting `i < j` in the inner loops, which can run off the ends on strings with no vowels.
- Not moving both pointers after a swap (infinite loop).
- Leaving out uppercase vowels.
- Trying to assign into a string (`s[i] = ...` raises `TypeError`).

### Q18 ⭐⭐ 🟡 Integer to Roman numeral. Convert an integer 1 <= num <= 3999 to a Roman numeral. Use a descending table of (value, symbol) pairs that includes the subtractive pairs (900 CM, 400 CD, 90 XC, 40 XL, 9 IX, 4 IV) and take each as many times as fits. Say why the greedy choice is safe here. Example: 3749 -> 'MMMDCCXLIX'; 58 -> 'LVIII'; 1994 -> 'MCMXCIV'; 4 -> 'IV'.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Greedy over a descending value table. Decimal places are independent in Roman numerals, so taking the biggest symbol that fits works.

**Say this first (1 line):** "Table of 13 (value, symbol) pairs including the subtractive ones, walk it from largest to smallest, take each as many times as it fits. Constant time."

**Brute force:** Build each decimal place from a fixed table of ten strings per place (units, tens, hundreds, thousands): `th[n//1000] + hu[n//100%10] + te[n//10%10] + on[n%10]`. Also constant time, and my checker below. It needs 40 hard-coded strings; the greedy table needs 13 pairs.

**Optimal:**
- Table: M 1000, CM 900, D 500, CD 400, C 100, XC 90, L 50, XL 40, X 10, IX 9, V 5, IV 4, I 1.
- For each pair, `count, n = divmod(n, value)` and append `symbol * count`.
- Invariant: the remaining `n` is always smaller than the last value I processed (or I have not reached it yet), so I never need a symbol I already passed.
- Why greedy is safe: I listed the subtractive pairs as their own entries, so every place's pattern (1-3 repeats, 4, 5, 6-8, 9) comes out of the table in one left-to-right sweep. This is not a general fact about greedy and coins (coins 1, 3, 4 and target 6 break greedy). It holds here because the table is "decimal-shaped": the digit table and the greedy agree for all 3999 inputs, which my run checks exhaustively.

**Complexity:** O(1) time and space: the table has 13 rows, and the output is at most 15 characters for 1..3999 (`MMMDCCCLXXXVIII`, as the run prints). If I say O(log n), it is the number of decimal digits.

**Dry run:** `1994`.
| value, symbol | divmod result | output so far | n left |
|---|---|---|---|
| 1000 M | 1, 994 | M | 994 |
| 900 CM | 1, 94 | MCM | 94 |
| 500, 400, 100 | 0 each | MCM | 94 |
| 90 XC | 1, 4 | MCMXC | 4 |
| 50, 40, 10, 9, 5 | 0 each | MCMXC | 4 |
| 4 IV | 1, 0 | MCMXCIV | 0 |

**Code:**
```python
TABLE = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
         (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
DIGITS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(r):
    # independent checker: a smaller symbol before a larger one is subtracted
    total = 0
    for i, ch in enumerate(r):
        v = DIGITS[ch]
        total += -v if i + 1 < len(r) and DIGITS[r[i + 1]] > v else v
    return total


def to_roman_digitwise(n):
    # brute force: build each decimal place from a fixed 10-entry table
    th = ["", "M", "MM", "MMM"]
    hu = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    te = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    on = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return th[n // 1000] + hu[n // 100 % 10] + te[n // 10 % 10] + on[n % 10]


def to_roman(n):
    out = []
    for val, sym in TABLE:
        count, n = divmod(n, val)
        out.append(sym * count)
    return "".join(out)


examples = [(3749, "MMMDCCXLIX"), (58, "LVIII"), (1994, "MCMXCIV"), (4, "IV")]
for n, want in examples:
    got = to_roman(n)
    assert got == to_roman_digitwise(n) == want, (n, got)
    print(n, "->", got)

assert to_roman(1) == "I"
assert to_roman(3999) == "MMMCMXCIX"
assert to_roman(2000) == "MM"
for n in range(1, 4000):          # exhaustive over the whole domain
    r = to_roman(n)
    assert r == to_roman_digitwise(n), n
    assert roman_to_int(r) == n, (n, r)
print("exhaustive check passed: 3999 values (greedy == digit table == round trip)")
print("longest numeral:", max((to_roman(n) for n in range(1, 4000)), key=len))
```

**Output (my run):**
```
3749 -> MMMDCCXLIX
58 -> LVIII
1994 -> MCMXCIV
4 -> IV
exhaustive check passed: 3999 values (greedy == digit table == round trip)
longest numeral: MMMDCCCLXXXVIII
```
All four examples in the prompt are correct.

**Edge cases:**
- 1 gives `'I'`; 3999 gives `'MMMCMXCIX'` (the largest in range).
- 4, 9, 40, 90, 400, 900 are the subtractive cases; leaving them out of the table gives `'IIII'`.
- 0 and numbers above 3999 are outside the range (no zero symbol; 4000 would need an overline or `MMMM`).
- Round-trip: converting back with the subtract-if-smaller-precedes-larger rule gives the original number for every input (checked in the run).

**Follow-ups:**
- *Roman to integer?* Scan; subtract a symbol if the next one is larger, else add. That is the checker in my code.
- *Why not a loop of `while n >= value`?* Same result; `divmod` avoids the inner loop.
- *Bigger range?* Needs overlined symbols; not standard in ASCII.

**Common mistakes:**
- Omitting the subtractive pairs.
- Putting them out of order (the table must be strictly descending).
- Using `n -= value` with a bug in the order of 4 and 5.
- Claiming greedy is always valid for coin-like tables.

### Q19 ⭐⭐ 🟡 Zigzag conversion. Write `s` in a zigzag of `numRows` rows (down the rows, then up diagonally, repeating), then read the rows left to right, top to bottom, and return the concatenation. Do it in O(n) by appending each character to its row's buffer while a direction flag flips at the top and bottom rows (handle numRows = 1). Example: ('PAYPALISHIRING', 3) -> 'PAHNAPLSIIGYIR'; ('PAYPALISHIRING', 4) -> 'PINALSIGYAHRPI'; ('AB', 1) -> 'AB'.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Simulation with a direction flag, one buffer per row.

**Say this first (1 line):** "One list per row; walk the string, append to the current row, flip direction at the top and bottom rows; join the rows. O(n). Row count 1 is a special case."

**Brute force:** Fill a 2D grid (rows by columns) with the zigzag shape and read it row by row. O(rows * columns) space, mostly empty cells. Another reference: character `i` lands in row `k` or `cycle - k`, where `k = i % cycle` and `cycle = 2 * (rows - 1)`. I use that as my checker.

**Optimal:**
- `bufs = [[] for _ in range(rows)]`, `r = 0`, `step = 1`.
- For each character: append to `bufs[r]`; if `r == 0` go down (`step = 1`), if `r == last row` go up (`step = -1`); then `r += step`.
- `numRows = 1` returns `s` immediately, because the flag logic would step out of range.
- If `numRows > len(s)`, use only `min(rows, len(s))` buffers: the zigzag never reaches the lower rows, and the answer is `s`.
- Invariant: `r` is always the row of the next character.

**Complexity:** Time O(n), each character appended once and joined once. Space O(n) for the buffers.

**Dry run:** `'PAYPALISHIRING'`, 3 rows. Row index per character: 0 1 2 1 0 1 2 1 0 1 2 1 0 1.
| row | characters (in order) | joined |
|---|---|---|
| 0 | P, A, H, N | PAHN |
| 1 | A, P, L, S, I, I, G | APLSIIG |
| 2 | Y, I, R | YIR |

Answer `'PAHNAPLSIIGYIR'`.

**Code:**
```python
import random


def zig_brute(s, rows):
    # reference: compute each character's row from the cycle position
    if rows == 1 or rows >= len(s):
        return s
    cycle = 2 * (rows - 1)
    buckets = [[] for _ in range(rows)]
    for i, c in enumerate(s):
        k = i % cycle
        buckets[k if k < rows else cycle - k].append(c)
    return "".join("".join(b) for b in buckets)


def zig_flag(s, rows):
    if rows == 1:
        return s
    bufs = [[] for _ in range(min(rows, len(s)))]
    r, step = 0, 1
    for c in s:
        bufs[r].append(c)
        if r == 0:
            step = 1
        elif r == len(bufs) - 1:
            step = -1
        r += step
    return "".join("".join(b) for b in bufs)


examples = [("PAYPALISHIRING", 3, "PAHNAPLSIIGYIR"), ("PAYPALISHIRING", 4, "PINALSIGYAHRPI"), ("AB", 1, "AB")]
for s, k, want in examples:
    got = zig_flag(s, k)
    assert got == zig_brute(s, k) == want, (s, k, got)
    print((s, k), "->", got)

assert zig_flag("A", 5) == "A"            # more rows than characters
assert zig_flag("AB", 5) == "AB"
assert zig_flag("ABC", 2) == "ACB"
assert zig_flag("", 3) == ""
assert zig_flag("ABCD", 4) == "ABCD"
assert zig_flag("x" * 1000, 1) == "x" * 1000

rng = random.Random(19)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("abcdefgh") for _ in range(rng.randint(0, 20)))
    k = rng.randint(1, 8)
    assert zig_flag(s, k) == zig_brute(s, k), (s, k)
    assert sorted(zig_flag(s, k)) == sorted(s)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('PAYPALISHIRING', 3) -> PAHNAPLSIIGYIR
('PAYPALISHIRING', 4) -> PINALSIGYAHRPI
('AB', 1) -> AB
random cross-check passed: 3000 cases
```
All three examples in the prompt are correct.

**Edge cases:**
- `numRows = 1`: return `s`.
- `numRows >= len(s)`: return `s`.
- Two rows: alternates down and up every character (`'ABC', 2 -> 'ACB'`).
- Empty string: returns `''`.
- Characters can be anything, including spaces and punctuation; they are never inspected.

**Follow-ups:**
- *Jump formula instead of a flag?* Row `r` takes indices `r, r + cycle - 2r, ...` with `cycle = 2 * (rows - 1)`; the middle rows alternate two different gaps.
- *Reverse (unzigzag)?* Compute the row lengths from the cycle pattern, split the string, and read it back using the same flag walk.
- *Why a list of lists, not strings?* Repeated `str +=` can degrade; lists plus one `join` are the safe habit.

**Common mistakes:**
- Not handling `numRows = 1` (index error or wrong output).
- Flipping direction one step late, so the walk runs past the last row.
- Allocating `rows` buffers when `rows > len(s)` and then trusting the last buffer to be reached.
- Joining the rows in the wrong order.

### Q20 ⭐⭐ 🟡 Compare version numbers. Two version strings consist of non-negative integer revisions separated by '.', each revision possibly with leading zeros (up to 500 characters per string). Return -1, 0 or 1 if the first is smaller, equal or larger, treating a missing revision as 0. Parse with two indices in one pass (no full split needed) and explain the pitfall of comparing revisions as strings. Example: ('1.2','1.10') -> -1; ('1.01','1.001') -> 0; ('1.0','1.0.0.0') -> 0; ('0.1','1.1') -> -1; ('2.0.1','2') -> 1.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Two-index scan over two strings, parsing numbers in place instead of splitting.

**Say this first (1 line):** "Never compare revisions as strings; parse each revision as an integer, missing means 0, and the first difference decides."

**Brute force:** `split('.')` both strings, convert to ints, `zip_longest(..., fillvalue=0)`, return at the first difference. O(n) time, O(n) space for the lists. It is correct and perfectly fine in practice; I use it as my checker.

**Optimal:**
- Keep `i` and `j` at the start of the current revision in each string.
- To read a revision: accumulate `v = v * 10 + digit` until a `.` or the end, and return the index just past the dot.
- If a string is finished, its revision is 0.
- Compare the two numbers. If they differ, return -1 or 1. Otherwise loop on.
- Leave the loop when both strings are used up: return 0.
- Leading zeros vanish naturally in the numeric parse (`'01'` and `'001'` both read as 1).

**Complexity:** Time O(len(a) + len(b)): each character is read once. Space O(1) beyond the input. Python integers are unbounded, so a 500-digit revision does not overflow; accumulating a long revision does cost a little more per step on big ints (still tiny at 500 digits). In a fixed-width language I would compare after stripping leading zeros: longer digit run wins, same length compares as strings.

**Dry run:** `('2.0.1', '2')`.
| round | a revision | b revision | verdict |
|---|---|---|---|
| 1 | 2 | 2 | equal |
| 2 | 0 | missing = 0 | equal |
| 3 | 1 | missing = 0 | 1 > 0, return 1 |

**Code:**
```python
import random
from itertools import zip_longest


def cmp_brute(a, b):
    x = [int(p) for p in a.split(".")]
    y = [int(p) for p in b.split(".")]
    for p, q in zip_longest(x, y, fillvalue=0):
        if p != q:
            return -1 if p < q else 1
    return 0


def next_rev(s, i):
    # read one revision starting at i; return (value, index after the dot)
    n, v = len(s), 0
    while i < n and s[i] != ".":
        v = v * 10 + (ord(s[i]) - 48)
        i += 1
    return v, i + 1


def cmp_version(a, b):
    i = j = 0
    while i < len(a) or j < len(b):
        x, i = next_rev(a, i) if i < len(a) else (0, i)
        y, j = next_rev(b, j) if j < len(b) else (0, j)
        if x != y:
            return -1 if x < y else 1
    return 0


examples = [("1.2", "1.10", -1), ("1.01", "1.001", 0), ("1.0", "1.0.0.0", 0), ("0.1", "1.1", -1), ("2.0.1", "2", 1)]
for a, b, want in examples:
    got = cmp_version(a, b)
    assert got == cmp_brute(a, b) == want, (a, b, got)
    print((a, b), "->", got)

assert "1.2" > "1.10"                         # the string-compare pitfall: wrongly says 1.2 is larger
assert cmp_version("1.2", "1.10") == -1
assert cmp_version("0", "0.0.0") == 0
assert cmp_version("1.0.1", "1") == 1
assert cmp_version("7", "7.0") == 0
assert cmp_version("001", "1") == 0
assert cmp_version("1." + "0." * 200 + "1", "1") == 1   # long, nonzero tail decides
assert cmp_version("9" * 100, "9" * 99) == 1             # big revisions are fine in Python

rng = random.Random(20)
cases = 0
for _ in range(4000):
    def gen():
        return ".".join(("0" * rng.randint(0, 2)) + str(rng.randint(0, 12)) for _ in range(rng.randint(1, 5)))
    a, b = gen(), gen()
    assert cmp_version(a, b) == cmp_brute(a, b), (a, b)
    assert cmp_version(a, b) == -cmp_version(b, a)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('1.2', '1.10') -> -1
('1.01', '1.001') -> 0
('1.0', '1.0.0.0') -> 0
('0.1', '1.1') -> -1
('2.0.1', '2') -> 1
random cross-check passed: 4000 cases
```
All five examples in the prompt are correct.

**Edge cases:**
- `'1.0'` versus `'1.0.0.0'`: all extra revisions are 0, so equal.
- `'1.0.1'` versus `'1'`: the third revision decides.
- Leading zeros: `'1.01'` equals `'1.001'`.
- Single revision, no dot.
- The string pitfall: `'1.2' > '1.10'` is True in Python because `'2' > '1'` at the first differing character. The code asserts this, then shows the numeric comparison says -1.

**Follow-ups:**
- *Pre-release tags like `1.0-beta`?* That needs a real versioning scheme; use a library (the `packaging` package is the usual one; I did not run it here).
- *Why not just `tuple(map(int, v.split('.')))`?* It works if you pad with zeros first; `(1, 0) < (1, 0, 0)` is True, which is wrong for this problem.
- *Space O(1) needed?* The two-index scan is exactly that.

**Common mistakes:**
- Comparing revisions as strings.
- Using `<` on `split` lists directly (trailing zeros break equality).
- Treating a missing revision as "smaller" instead of 0.
- Forgetting to skip the dot, which loops forever on the same revision.
