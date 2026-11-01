# Book 5 Part 3, Q21-Q30 answers (Wave B)


### Q21 ⭐⭐ 🟡 Encode and decode strings with escaping. Part 1 Q24 solves a list-of-strings codec with length prefixes; here use the escaping design instead. Rules: every string is escaped by writing '/' as '//' and '#' as '/#', and then followed by the terminator '#'; the codec is the concatenation. Implement `encode(strs)` and `decode(s)` that round-trip every list including [] and lists with empty strings, decode in one pass with a state flag, and compare the two designs (streaming, random access, overhead). Example: encode(['a#b','c','']) -> 'a/#b#c##'; encode([]) -> ''; encode(['']) -> '#'; decode('a/#b#c##') -> ['a#b','c',''].
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports

**Pattern:** String codec with an escape character, decoded by a one-pass state machine. The question is "how do I make a delimiter safe?" There are two answers: length prefix (Part 1 Q24) or escaping (this one).

**Say this first (1 line):** "A plain separator is unsafe because the data can contain it. So I escape: `/` becomes `//`, `#` becomes `/#`, and every string ends with a bare `#`. Decode is a one-pass state machine with one flag: 'the last character was an escape'."

**Brute force:** Join with a separator, `'#'.join(strs)`, and split on it. It breaks three ways: `['a#b']` splits into two items, `[]` and `['']` both give `''`, and there is no way to tell them apart. A safer brute force is a regex that splits on an unescaped `#`: `re.findall(r'((?:[^/#]|/.)*)#', s)`. It is correct, and I use it as the checker. The hand-written state machine is clearer and faster to reason about.

**Optimal:**
- Encode: for each string, `replace('/', '//')`, then `replace('#', '/#')`, then append `#`. The second replace never touches a `/`, so the order is safe.
- Decode: walk the characters with `esc = False` and a buffer.
  - If `esc`: append the character literally, set `esc = False`.
  - Else if `/`: set `esc = True`.
  - Else if `#`: the current string is finished, push it, reset the buffer.
  - Else: append.
- Invariant: outside an escape, a `#` is always a terminator, and inside an escape the next character is always data. Every data `#` or `/` was written with a `/` before it, so no data character can look like a terminator.
- Empty list gives `''`. A list with one empty string gives `'#'`. They differ, so every list round-trips.

**Complexity:** Time O(total characters) for both, one pass each. Space O(total characters) for the output. Worst-case overhead is 2x plus one per string (all data is `/` or `#`).

Design comparison:
| | Length prefix (Part 1 Q24) | Escaping (this) |
|---|---|---|
| Overhead | digits of length + 1 per string | 1 per string + 1 per special character |
| Random access to item k | yes, hop over lengths without reading data | no, you must scan every character |
| Streaming decode | needs the length first, then reads that many | one character at a time, O(1) state |
| Binary or any text data | yes, no special characters | yes, but you pay escaping on data |
| Malformed input | length can point past the end | dangling `/` or missing last `#` |

**Dry run:** `decode('a/#b#c##')`
| char | esc before | action | buffer | out |
|---|---|---|---|---|
| a | no | append | a | [] |
| / | no | set esc | a | [] |
| # | yes | append literally | a# | [] |
| b | no | append | a#b | [] |
| # | no | terminator | (reset) | ['a#b'] |
| c | no | append | c | ['a#b'] |
| # | no | terminator | (reset) | ['a#b','c'] |
| # | no | terminator, empty buffer | (reset) | ['a#b','c',''] |

**Code:**
```python
import random
import re


def encode_naive(strs):
    return '#'.join(strs)            # broken on purpose: shown only to prove the point


def encode(strs):
    return ''.join(s.replace('/', '//').replace('#', '/#') + '#' for s in strs)


def decode(s):
    out, buf, esc = [], [], False
    for ch in s:
        if esc:
            buf.append(ch)
            esc = False
        elif ch == '/':
            esc = True
        elif ch == '#':
            out.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
    if esc or buf:
        raise ValueError('malformed: dangling escape or missing terminator')
    return out


def decode_regex(s):                 # brute force checker
    pieces = re.findall(r'((?:[^/#]|/.)*)#', s, re.S)
    return [re.sub(r'/(.)', r'\1', p, flags=re.S) for p in pieces]


# Why a plain separator fails.
print(encode_naive(['a#b']).split('#'), encode_naive([]) == encode_naive(['']))

print(encode(['a#b', 'c', '']))
print(repr(encode([])), repr(encode([''])))
print(decode('a/#b#c##'))

assert encode(['a#b', 'c', '']) == 'a/#b#c##'
assert encode([]) == '' and encode(['']) == '#'
assert decode('a/#b#c##') == ['a#b', 'c', '']
assert decode('') == [] and decode('#') == ['']
for tricky in (['/'], ['#'], ['//'], ['/#'], ['#/'], ['', ''], ['/', '#', ''], ['a' * 5], ['###'], ['/#/#']):
    assert decode(encode(tricky)) == tricky, tricky
for bad in ('a', '/', 'a/', 'ab#c'):
    try:
        decode(bad)
        raise AssertionError('should have failed: ' + bad)
    except ValueError:
        pass

rng = random.Random(7)
cases = 0
seen = {}
for _ in range(3000):
    k = rng.randint(0, 5)
    strs = [''.join(rng.choice('/#ab0') for _ in range(rng.randint(0, 6))) for _ in range(k)]
    e = encode(strs)
    assert decode(e) == strs
    assert decode_regex(e) == strs
    assert seen.setdefault(e, strs) == strs          # two lists never share an encoding
    cases += 1
print('random round-trip and regex cross-check passed:', cases, 'cases')

worst = encode(['/' * 10])
print(len('/' * 10), '->', len(worst))
```

**Output (my run):**
```
['a', 'b'] True
a/#b#c##
'' '#'
['a#b', 'c', '']
random round-trip and regex cross-check passed: 3000 cases
10 -> 21
```
Both prompt examples are correct.

**Edge cases:**
- `[]` encodes to `''` and `['']` to `'#'`: different, so the empty list is distinguishable.
- Strings that are only `/` or `#`, and strings ending in `/` (the escape must not eat the terminator: `['a/']` gives `'a//#'`).
- A string that already looks like an encoding.
- Malformed input: a trailing `/`, or data with no final `#`. Decide whether to raise (I do) or be lenient, and say so.

**Follow-ups:**
- *Why not just use JSON?* `json.dumps(strs)` is the production answer. This question tests whether you can build the escaping yourself. JSON does the same thing with quotes and backslashes.
- *Which is better for a network protocol?* Length prefix when payloads are large or binary: no scanning, easy to skip. Escaping when the stream is text and you want to resynchronise after corruption at the next terminator.
- *Does it work on bytes?* Yes, with `bytes.replace` and byte values; pick the escape and terminator bytes and the same argument holds.

**Common mistakes:**
- Escaping `#` but forgetting to escape the escape character itself, so `'/'` followed by the terminator looks like an escaped `#`.
- Escaping `/` after `#` (the `/` you just added gets doubled).
- Treating `[]` and `['']` as the same.
- Splitting the decoded stream on `'#'` first and unescaping afterwards; an escaped `#` has already been cut in two.


### Q22 ⭐⭐ 🟡 Z-function and pattern search. The Z-array of a string `s` has Z[i] equal to the length of the longest common prefix of `s` and `s[i:]` (Z[0] = n by convention). Build it in O(n) with the [l, r) window of the rightmost match and explain why each character is compared a bounded number of times. Then use it to list every start of `pattern` in `text` by running Z on pattern + '\x00' + text. Example: Z('aabxaab') -> [7,1,0,0,3,1,0]; occurrences of 'aba' in 'abababa' -> [0,2,4].
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Z-function: for every position, the length of the longest match with the start of the string, built with a "rightmost match window" so earlier work is reused. Used for linear-time pattern search.

**Say this first (1 line):** "Z[i] is how long `s[i:]` agrees with `s`. I keep the window `[l, r)` of the match that reaches furthest right; inside it, `s[i:]` mirrors `s[i-l:]`, so I copy the old answer, capped at the window edge, and only extend by comparing past `r`."

**Brute force:** For each `i`, compare `s[k]` with `s[i+k]` until they differ. O(n^2) in the worst case (`'aaaa...'`). Search by `text.find` in a loop or slicing every window is O(n*m).

**Optimal:**
- Keep `l, r` with `s[l:r] == s[0:r-l]`, `r` as large as possible.
- For `i`: if `i < r`, start with `z[i] = min(r - i, z[i - l])` (the mirror position already told us). Then extend with a `while` loop while characters match.
- If `i + z[i] > r`, set `l, r = i, i + z[i]`.
- Why each character is compared a bounded number of times: a comparison that succeeds moves `r` right, and `r` never moves left, so at most `n` successful comparisons overall. Each `i` causes at most one failing comparison. Total under `2n`.
- Search: build Z on `pattern + '\x00' + text`. The sentinel cannot appear in either string, so no Z value inside the text part exceeds `m`. A position `i > m` with `Z[i] == m` is a match at text index `i - m - 1`.

**Complexity:** Time O(n + m) where n + m + 1 is the length of the combined string. Space O(n + m) for the combined string and the Z array.

**Dry run:** `Z('aabxaab')`, `n = 7`
| i | window before | start z | extend | z[i] | window after |
|---|---|---|---|---|---|
| 1 | [0,0) | 0 | a=a, then b vs a stop | 1 | [1,2) |
| 2 | [1,2) | 0 | a vs b stop | 0 | [1,2) |
| 3 | [1,2) | 0 | a vs x stop | 0 | [1,2) |
| 4 | [1,2) | 0 | aab match, end | 3 | [4,7) |
| 5 | [4,7) | min(2, z[1]=1) = 1 | s[1]=a vs s[6]=b stop | 1 | [4,7) |
| 6 | [4,7) | min(1, z[2]=0) = 0 | b vs a stop | 0 | [4,7) |
Z[0] = 7 by convention. Result `[7,1,0,0,3,1,0]`.

**Code:**
```python
import random


def z_brute(s):
    n = len(s)
    z = [0] * n
    for i in range(n):
        k = 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        z[i] = k
    return z


def z_function(s):
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0                                   # s[l:r] == s[0:r-l], r as far right as seen
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])         # copy from the mirror, capped at the window
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1                           # only reaches past r when the copy hit the edge
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def search_z(text, pattern):
    if not pattern:
        raise ValueError('empty pattern')
    m = len(pattern)
    z = z_function(pattern + '\x00' + text)     # sentinel must not occur in either string
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] == m]


def search_brute(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


print(z_function('aabxaab'))
print(search_z('abababa', 'aba'))
assert z_function('aabxaab') == [7, 1, 0, 0, 3, 1, 0]
assert search_z('abababa', 'aba') == [0, 2, 4]
assert z_function('') == [] and z_function('a') == [1]
assert z_function('aaaa') == [4, 3, 2, 1]
assert z_function('abcd') == [4, 0, 0, 0]
assert search_z('aaaa', 'aa') == [0, 1, 2]
assert search_z('abc', 'abcd') == [] and search_z('', 'a') == []
assert search_z('abc', 'abc') == [0]

rng = random.Random(22)
cases = 0
for _ in range(3000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 14)))
    assert z_function(s) == z_brute(s), s
    text = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 14)))
    pat = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 4)))
    assert search_z(text, pat) == search_brute(text, pat), (text, pat)
    cases += 1
print('random cross-check passed:', cases, 'cases')
big = 'a' * 20000                               # the quadratic-for-brute shape, linear here
assert z_function(big)[1] == 19999
print('20000 a-characters done')
```

**Output (my run):**
```
[7, 1, 0, 0, 3, 1, 0]
[0, 2, 4]
random cross-check passed: 3000 cases
20000 a-characters done
```
Both prompt examples are correct.

**Edge cases:**
- Empty string: `[]`. One character: `[1]`. All equal: `[n, n-1, ..., 1]`.
- Empty pattern: reject (or define it as matching at every index); say which.
- Pattern longer than text: no match.
- Sentinel collision: if the text can contain `'\x00'`, pick a character outside the alphabet, or avoid the concatenation and compare against the pattern's Z array directly.

**Follow-ups:**
- *Smallest period of a string?* The smallest `p >= 1` with `p + Z[p] == n` and `n % p == 0`; the string is then `s[:p]` repeated `n // p` times (if no such p below n, the period is n).
- *Z versus KMP?* Same power. Z is a "forward" array (match with prefix starting here), the prefix function is a "backward" array (border ending here). Each can be turned into the other in O(n).
- *Why is `z[0] = n` and not computed?* The loop starts at 1; position 0 would compare the string with itself, so it is defined as `n`.

**Common mistakes:**
- Forgetting the `min(r - i, ...)` cap. Without it you trust the mirror beyond what is known, and get wrong answers.
- Updating `l, r` even when `i + z[i] <= r`. It does not break correctness, but it can hurt the bound.
- No sentinel, so a Z value runs from the pattern part into the text part and overshoots `m`.
- Starting the loop at 0 and overwriting `z[0]`.


### Q23 ⭐⭐ 🟡 KMP prefix function and matching. The prefix function pi of a string stores, for each i, the length of the longest proper prefix of s[:i+1] that is also a suffix of it. Build pi in O(n) (explain the fallback `k = pi[k-1]` loop and its amortised bound), then use it to return all start indices of `pattern` in `text` in O(n + m) without moving the text pointer backwards. Example: pi('abacaba') -> [0,0,1,0,1,2,3]; pi('aabaaab') -> [0,1,0,1,2,2,3]; all matches of 'aa' in 'aaaa' -> [0,1,2].
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** KMP: precompute the prefix function (borders) of the pattern, then scan the text once and never move the text pointer backwards. On a mismatch, fall back inside the pattern instead.

**Say this first (1 line):** "`pi[i]` is the length of the longest proper prefix of `s[:i+1]` that is also its suffix. When a match fails after `k` characters, I do not restart; I fall back to `k = pi[k-1]`, the longest border of what I already matched."

**Brute force:** Try every start and compare up to `m` characters: O(n*m). Worst case `'aaaa...a'` against `'aaa...ab'`.

**Optimal:**
- Build `pi`: `k = 0`; for `i` from 1: `while k and s[i] != s[k]: k = pi[k-1]`; if `s[i] == s[k]`: `k += 1`; `pi[i] = k`.
- Match: same loop, with `pattern` as the thing being extended and the text as the stream. When `k == m`, record `i - m + 1` and set `k = pi[m-1]` so overlapping matches are found.
- Why fallback is safe: if `pattern[:k]` matched the end of the text read so far, any shorter match that still ends here must be a border of `pattern[:k]`. `pi[k-1]` is the longest one, and following the chain gives all of them in decreasing order.
- Amortised bound: `k` goes up by at most 1 per character and every fallback step lowers it, never below 0. So total fallbacks are at most the total increments, at most n.

**Complexity:** Time O(m) for pi, O(n) for the scan: O(n + m) in total. Space O(m) for pi.

**Dry run:** `pi('abacaba')`
| i | char | k before | fallback | match? | pi[i] |
|---|---|---|---|---|---|
| 1 | b | 0 | none | b vs a no | 0 |
| 2 | a | 0 | none | a vs a yes | 1 |
| 3 | c | 1 | s[1]=b no, k=pi[0]=0 | c vs a no | 0 |
| 4 | a | 0 | none | yes | 1 |
| 5 | b | 1 | none | b vs b yes | 2 |
| 6 | a | 2 | none | a vs a yes | 3 |
Result `[0,0,1,0,1,2,3]`.

**Code:**
```python
import random


def pi_function(s, stats=None):
    n = len(s)
    pi = [0] * n
    k = 0
    for i in range(1, n):
        while k and s[i] != s[k]:
            k = pi[k - 1]                      # fall back to the next shorter border
            if stats is not None:
                stats['fallbacks'] += 1
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def pi_brute(s):
    n = len(s)
    out = []
    for i in range(n):
        sub = s[:i + 1]
        best = 0
        for L in range(1, len(sub)):           # proper: L < len(sub)
            if sub[:L] == sub[-L:]:
                best = L
        out.append(best)
    return out


def kmp_search(text, pattern):
    if not pattern:
        raise ValueError('empty pattern')
    m = len(pattern)
    pi = pi_function(pattern)
    res, k = [], 0
    for i, c in enumerate(text):               # i only moves forward
        while k and c != pattern[k]:
            k = pi[k - 1]
        if c == pattern[k]:
            k += 1
        if k == m:
            res.append(i - m + 1)
            k = pi[k - 1]                      # allow overlapping matches
    return res


def search_brute(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


print(pi_function('abacaba'))
print(pi_function('aabaaab'))
print(kmp_search('aaaa', 'aa'))
assert pi_function('abacaba') == [0, 0, 1, 0, 1, 2, 3]
assert pi_function('aabaaab') == [0, 1, 0, 1, 2, 2, 3]
assert kmp_search('aaaa', 'aa') == [0, 1, 2]
assert pi_function('') == [] and pi_function('a') == [0]
assert pi_function('aaaa') == [0, 1, 2, 3]
assert kmp_search('abc', 'abcd') == [] and kmp_search('', 'a') == []
assert kmp_search('abababa', 'aba') == [0, 2, 4]

rng = random.Random(23)
cases = 0
for _ in range(3000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 14)))
    assert pi_function(s) == pi_brute(s), s
    text = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 16)))
    pat = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 5)))
    assert kmp_search(text, pat) == search_brute(text, pat), (text, pat)
    cases += 1
print('random cross-check passed:', cases, 'cases')

# The amortised bound, checked: total fallback steps never exceed n.
worst = 0
for _ in range(2000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 40)))
    st = {'fallbacks': 0}
    pi_function(s, st)
    assert st['fallbacks'] <= len(s)
    worst = max(worst, st['fallbacks'] / len(s))
print('max fallbacks / n over random strings:', round(worst, 3))
```

**Output (my run):**
```
[0, 0, 1, 0, 1, 2, 3]
[0, 1, 0, 1, 2, 2, 3]
[0, 1, 2]
random cross-check passed: 3000 cases
max fallbacks / n over random strings: 0.75
```
Both prompt examples are correct (all three `pi` and match results).

**Edge cases:**
- Empty text, pattern longer than text.
- Pattern of one character.
- All equal characters (`'aaaa'` in `'aaaa'`): overlapping matches, so after a full match you must fall back, not reset to 0.
- Empty pattern: reject, or return every index; state the choice.

**Follow-ups:**
- *Why is it O(n) when there is a `while` inside the `for`?* Amortised: fallbacks are paid for by earlier increments of `k` (potential argument above). I also assert the count in the code above.
- *Smallest period?* `p = n - pi[n-1]`; if `n % p == 0` the string is `s[:p]` repeated `n // p` times. (This is the repeated-substring check.)
- *KMP vs `str.find`?* Use `find` in real code. In an interview, show the algorithm and say `find` exists; do not claim anything about CPython internals beyond "it is optimised C".

**Common mistakes:**
- Starting the pi loop at 0 (everything would match itself, `pi[0]` must be 0).
- Falling back with `k -= 1` instead of `k = pi[k-1]`, which gives O(n*m).
- Forgetting `k = pi[k-1]` after a full match, so `pattern[k]` goes out of range or overlaps are missed.
- Using `<=` when computing a proper border, which counts the whole string.


### Q24 ⭐⭐ 🟡 Rabin-Karp with collision handling. Find every start index of `pattern` in `text` with a polynomial rolling hash: hash = sum(ord(c) * B^(m-1-i)) mod M, rolled in O(1) per step. Hash equality is not string equality, so on every hash hit compare the actual substrings (or use a second independent modulus and state the residual risk), pick the base at random for adversarial input, and give the expected and worst-case time. Show that your code still returns correct answers with a deliberately tiny modulus such as M = 7 where collisions are frequent. Example: text='abracadabra', pattern='abra' -> [0, 7]; text='aaaaa', pattern='aa' -> [0,1,2,3]; text='abcabc', pattern='cab' -> [2].
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Rolling hash: a window of `m` characters is turned into one integer, and moving the window by one character costs O(1). A hash match is only a hint, so verify.

**Say this first (1 line):** "Hash the pattern once, roll a hash over the text, and on every hash hit compare the real substrings. Equal hashes do not prove equal strings, so the verify step is what makes the answer correct; the hash only makes verifying rare."

**Brute force:** Compare `text[i:i+m]` with the pattern at every `i`: O(n*m).

**Optimal:**
- `hash(w) = sum(ord(w[i]) * B^(m-1-i)) mod M`.
- Roll from window `i` to `i+1`: `h = ((h - ord(text[i]) * B^(m-1)) * B + ord(text[i+m])) mod M`. Precompute `B^(m-1) mod M` with `pow(B, m-1, M)`. Python `%` is never negative, so no fix-up is needed (in C you would add `M`).
- On `h == target`, check `text[i:i+m] == pattern`. Only then record `i`.
- Pick `B` at random (seeded here) so an adversary who knows the code cannot craft collisions. Use a large prime `M` such as `2^61 - 1`.
- Expected time: for distinct windows and a prime M with random base, a collision has probability at most about `m / M`, so expected verifies are the true matches plus a tiny number of false ones. Worst case O(n*m), which is also what you pay if many windows really match (`'aaaa'` against `'aa'`) or if the modulus is tiny.
- "Verify" is what protects correctness. A second modulus lowers the false-hit rate further but without the verify step the answer stays probabilistic.

**Complexity:** Time O(n + m) expected with a large prime modulus; O(n*m) worst case. Space O(1) beyond the output.

**Dry run:** text `'abcabc'`, pattern `'cab'`, tiny `M = 7`, `B = 3`. Values of `ord` are large, but we only need them mod 7: `a=97 -> 6`, `b=98 -> 0`, `c=99 -> 1`. `B^(m-1) = 9 mod 7 = 2`.
| window | hash mod 7 | = target? | verify | match |
|---|---|---|---|---|
| abc (0) | 6*2 + 0*3 + 1 = 13 -> 6 | pattern hash is 6, so yes | `abc != cab` | spurious hit, rejected |
| bca (1) | 0*2 + 1*3 + 6 = 9 -> 2 | no | | |
| cab (2) | 1*2 + 6*3 + 0 = 20 -> 6 | yes | `cab == cab` | match at index 2 |
| abc (3) | 6 | yes | `abc != cab` | spurious hit, rejected |
The window `abc` has the same hash as `cab` (twice), so without the verify step the answer would be `[0, 2, 3]`, which is wrong.

**Code:**
```python
import random

BIG = (1 << 61) - 1                              # a Mersenne prime
seed_rng = random.Random(24)                     # base chosen at random, but reproducibly


def rabin_karp(text, pattern, M=BIG, B=None, verify=True, stats=None):
    n, m = len(text), len(pattern)
    if m == 0:
        raise ValueError('empty pattern')
    if B is None:
        B = seed_rng.randrange(2, M - 1)
    if m > n:
        return []
    high = pow(B, m - 1, M)
    hp = ht = 0
    for i in range(m):
        hp = (hp * B + ord(pattern[i])) % M
        ht = (ht * B + ord(text[i])) % M
    res = []
    for i in range(n - m + 1):
        if ht == hp:
            if stats is not None:
                stats['hits'] += 1
            if not verify or text[i:i + m] == pattern:
                res.append(i)
        if i + m < n:
            ht = ((ht - ord(text[i]) * high) * B + ord(text[i + m])) % M
    return res


def search_brute(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text[i:i + len(pattern)] == pattern]


print(rabin_karp('abracadabra', 'abra'))
print(rabin_karp('aaaaa', 'aa'))
print(rabin_karp('abcabc', 'cab'))
assert rabin_karp('abracadabra', 'abra') == [0, 7]
assert rabin_karp('aaaaa', 'aa') == [0, 1, 2, 3]
assert rabin_karp('abcabc', 'cab') == [2]
assert rabin_karp('abc', 'abcd') == [] and rabin_karp('', 'a') == []
assert rabin_karp('abc', 'abc') == [0]
assert rabin_karp('abc', 'c') == [2]

# Deliberately tiny modulus: collisions everywhere, still correct because we verify.
rng = random.Random(240)
cases = 0
for _ in range(3000):
    text = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 16)))
    pat = ''.join(rng.choice('abc') for _ in range(rng.randint(1, 4)))
    expected = search_brute(text, pat)
    assert rabin_karp(text, pat, M=7, B=3) == expected, (text, pat)
    assert rabin_karp(text, pat, M=7, B=5) == expected, (text, pat)
    assert rabin_karp(text, pat) == expected, (text, pat)
    cases += 1
print('random cross-check passed (M = 7, M = 7 other base, M = 2^61-1):', cases, 'cases')

# What goes wrong without the verify step: find the first wrong answer (seeded search).
rng = random.Random(241)
for _ in range(10000):
    text = ''.join(rng.choice('abc') for _ in range(rng.randint(3, 8)))
    pat = ''.join(rng.choice('abc') for _ in range(rng.randint(2, 3)))
    if rabin_karp(text, pat, M=7, B=3, verify=False) != search_brute(text, pat):
        print('no-verify wrong example:', text, pat, rabin_karp(text, pat, M=7, B=3, verify=False), search_brute(text, pat))
        break

# Spurious hits: tiny M versus large M on the same random input.
rng = random.Random(242)
text = ''.join(rng.choice('abcd') for _ in range(2000))
pat = 'abcdabcd'
for M in (7, BIG):
    st = {'hits': 0}
    found = rabin_karp(text, pat, M=M, B=3 if M == 7 else None, stats=st)
    print('M =', M, 'matches:', len(found), 'hash hits:', st['hits'])
```

**Output (my run):**
```
[0, 7]
[0, 1, 2, 3]
[2]
random cross-check passed (M = 7, M = 7 other base, M = 2^61-1): 3000 cases
no-verify wrong example: cabccaac cb [5] []
M = 7 matches: 0 hash hits: 265
M = 2305843009213693951 matches: 0 hash hits: 0
```
All three prompt examples are correct. The hit counts above depend on the seed and are an observation, not a proof of the bound; the bound comes from the collision-probability argument.

**Edge cases:**
- Pattern longer than text, empty text.
- Overlapping matches (`'aaaaa'`, `'aa'`).
- Negative intermediate value in the roll: fine in Python; in C or Java add `M` before taking the remainder.
- A hash of 0 for a window (a character with `ord` 0 or a base that cancels): fine, since we compare the full hash value, but never use `0` as a "no hash" marker.

**Follow-ups:**
- *Where does the rolling hash really shine?* When you need to compare many substrings: longest repeated substring (binary search on length plus hash set), multi-pattern search with equal-length patterns, and 2D pattern search.
- *One mod or two?* Two independent moduli make false positives astronomically unlikely, but you still verify if the answer must be exact.
- *Why a random base?* A fixed base and modulus can be attacked with a crafted collision pair (Thue-Morse strings are the classic example against a power-of-two modulus). A random base makes that attack impractical.

**Common mistakes:**
- Returning on hash equality without checking the strings.
- A non-prime or tiny modulus with a fixed base: too many collisions, easy to attack.
- Computing `B^(m-1)` with `B ** (m-1) % M`, which builds a huge integer; use three-argument `pow`.
- Rolling with the wrong power: removing the leading character needs `B^(m-1)`, not `B^m`.


### Q25 ⭐⭐ 🟡 Lexicographically smallest rotation. Given a lowercase string `s` (1 <= len <= 10^5), find the smallest string among all its rotations and the smallest start index achieving it. Give the O(n^2) brute force over all n rotations, then an O(n) method with two candidate start indices i, j and an offset k (advance past equal characters, drop the larger candidate, jump by k + 1); also name the alternative of running Booth's algorithm or building the minimal suffix of s + s. Example: 'bca' -> ('abc', 2); 'cba' -> ('acb', 2); 'abab' -> ('abab', 0); 'aaa' -> ('aaa', 0).
**Asked at:** Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution) | Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports

**Pattern:** Two-candidate elimination on a circular string. Keep two start indices and discard the loser of each comparison in bulk, skipping `k + 1` starts at once.

**Say this first (1 line):** "Brute force builds all n rotations, O(n^2). The linear way keeps two candidates `i` and `j`, compares them character by character with offset `k`, and when one is larger at the first difference, every start from that candidate to `candidate + k` is also beaten, so I jump `k + 1`."

**Brute force:** For each start `i`, build `s[i:] + s[:i]`, take the minimum, and break ties by the smaller `i`. O(n) rotations at O(n) each: O(n^2) time, and each rotation is a new string.

**Optimal:**
- `i = 0`, `j = 1`, `k = 0`.
- While `i, j, k < n`: compare `a = s[(i+k) % n]` and `b = s[(j+k) % n]`.
  - Equal: `k += 1`.
  - `a > b`: candidate `i` loses, and so do `i+1 .. i+k`, so `i += k + 1`.
  - `a < b`: symmetric, `j += k + 1`.
  - After a jump, if `i == j`, bump `j += 1`; set `k = 0`.
- Answer start: `min(i, j)`. Result string: `s[start:] + s[:start]`.
- Why the skip is valid: if `s[i..i+k-1] == s[j..j+k-1]` and `s[i+k] > s[j+k]`, then for any `t` in `0..k` the start `i+t` is beaten by the start `j+t`, since they share `k - t` equal characters and then differ with `i+t` larger.
- If `k` reaches `n`, the two candidates give the same rotation (the string is periodic); `min(i, j)` is the smaller index. The cross-check below tests that tie rule against the brute force.
- Alternatives I would name: Booth's algorithm (KMP-style failure function on `s + s`), and Duval's Lyndon factorisation on `s + s`.

**Complexity:** Time O(n): each comparison either advances `k` or advances `i` or `j` by `k + 1`, and `i` and `j` never pass `n`, so the work is paid for by the jumps (a small constant times n). Space O(1) besides the returned string.

**Dry run:** `s = 'bca'`, `n = 3`
| i | j | k | compare | action |
|---|---|---|---|---|
| 0 | 1 | 0 | s[0]=b vs s[1]=c | b < c, `j += 1` -> 2, k = 0 |
| 0 | 2 | 0 | s[0]=b vs s[2]=a | b > a, `i += 1` -> 1, k = 0 |
| 1 | 2 | 0 | s[1]=c vs s[2]=a | c > a, `i += 1` -> 2, now i == j so `j += 1` -> 3 |
Loop ends (`j == n`). `min(i, j) = 2`. Rotation `s[2:] + s[:2] = 'abc'`.

**Code:**
```python
import random


def min_rotation_brute(s):
    n = len(s)
    best = min(range(n), key=lambda i: (s[i:] + s[:i], i))
    return s[best:] + s[:best], best


def min_rotation(s):
    n = len(s)
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = s[(i + k) % n], s[(j + k) % n]
        if a == b:
            k += 1
            continue
        if a > b:
            i += k + 1
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    start = min(i, j)
    return s[start:] + s[:start], start


for s, exp in [('bca', ('abc', 2)), ('cba', ('acb', 2)), ('abab', ('abab', 0)), ('aaa', ('aaa', 0))]:
    print(s, min_rotation(s))
    assert min_rotation(s) == exp == min_rotation_brute(s)
assert min_rotation('a') == ('a', 0)
assert min_rotation('ba') == ('ab', 1)
assert min_rotation('abcabc') == ('abcabc', 0)
assert min_rotation('cabcab') == ('abcabc', 1)       # periodic: smallest index among ties
assert min_rotation('zzzy') == ('yzzz', 3)

rng = random.Random(25)
cases = 0
for _ in range(5000):
    s = ''.join(rng.choice('ab' if rng.random() < 0.7 else 'abc') for _ in range(rng.randint(1, 12)))
    assert min_rotation(s) == min_rotation_brute(s), s
    cases += 1
print('random cross-check passed:', cases, 'cases')
big = 'a' * 100000 + 'b'
print(min_rotation(big)[1])                          # linear time on a long adversarial-looking input
```

**Output (my run):**
```
bca ('abc', 2)
cba ('acb', 2)
abab ('abab', 0)
aaa ('aaa', 0)
random cross-check passed: 5000 cases
0
```
All four prompt examples are correct.

**Edge cases:**
- Length 1: the `j = 1` start is already out of range, the loop does not run, the answer is index 0.
- All equal characters: `k` runs to `n` once, answer index 0.
- Periodic strings (`'abab'`, `'cabcab'`): ties among rotations; the contract says smallest index. The code returns it, and the cross-check proves it on random inputs (it is a test, not a proof for all inputs).
- Empty string: define separately (return `('', 0)`); the code assumes `n >= 1`.

**Follow-ups:**
- *Use it to test rotation equivalence?* Canonicalise both strings to their minimum rotation and compare. O(n) each, no `s + s` substring search needed.
- *Compare to `goal in s + s`?* That answers "is it a rotation?" (Part 3 Q5). This finds the canonical rotation.
- *Simple alternative?* `min(s[i:] + s[:i] for i in range(n))` is fine for small n and a good checker, but it is O(n^2).

**Common mistakes:**
- Advancing by 1 instead of `k + 1` after a mismatch: correct but O(n^2) on strings like `'aaaa...b'`.
- Forgetting `if i == j: j += 1`, so the two candidates become the same index and the loop stalls.
- Returning `max(i, j)` or the one that "won" last; the survivor is the smaller index.
- Comparing without the modulo, so `i + k` runs off the string.


### Q26 ⭐⭐ 🔴 Longest happy prefix. Given `s` (1 <= len <= 10^5, lowercase), return the longest non-empty proper prefix that is also a suffix (proper means it is not the whole string), or '' if none. Solve it with the prefix function (the answer is pi[n-1]) and explain why that value is exactly the border you want; also give the Z-function view (the smallest i with Z[i] = n - i) and a rolling-hash alternative with its collision caveat. Example: 'level' -> 'l'; 'ababab' -> 'abab'; 'abc' -> ''; 'a' -> ''.
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports

**Pattern:** Border of a string (a prefix that is also a suffix). The KMP prefix function gives the longest border directly.

**Say this first (1 line):** "A happy prefix is a proper prefix that is also a suffix, which is a border. `pi[n-1]` is by definition the length of the longest proper border of the whole string, so the answer is `s[:pi[-1]]`."

**Brute force:** For `L` from `n-1` down to 1, test `s[:L] == s[-L:]`. The first success is the answer. O(n^2) because each test costs O(L).

**Optimal:**
- Compute `pi` in O(n) (Part 3 Q23).
- Return `s[:pi[n-1]]`.
- Why it is exactly the border you want: `pi[i]` is defined as the longest proper prefix of `s[:i+1]` that is also a suffix of `s[:i+1]`. At `i = n-1` the string is all of `s`. "Proper" excludes the whole string, "non-empty" is `pi[n-1] > 0`.
- Z view: a border of length `L` means `s[n-L:]` equals `s[:L]`, so `Z[n-L] == L`, i.e. `i + Z[i] == n` with `i = n - L`. The longest border is the smallest such `i >= 1`.
- Rolling-hash view: compare the hash of each prefix of length `L` with the hash of the suffix of length `L`. A hash match can be a collision, so collect the matching lengths and verify the longest one first, falling back to shorter ones.

**Complexity:** Pi or Z: O(n) time, O(n) space. Rolling hash: O(n) expected time. Brute force: O(n^2).

**Dry run:** `s = 'ababab'`
| i | char | pi[i] | reason |
|---|---|---|---|
| 0 | a | 0 | |
| 1 | b | 0 | b vs a no |
| 2 | a | 1 | a = a |
| 3 | b | 2 | b = b |
| 4 | a | 3 | a = a |
| 5 | b | 4 | b = b |
`pi[5] = 4`, answer `s[:4] = 'abab'`. Check: suffix `s[2:] = 'abab'`.

**Code:**
```python
import random

BIG = (1 << 61) - 1


def happy_brute(s):
    for L in range(len(s) - 1, 0, -1):
        if s[:L] == s[-L:]:
            return s[:L]
    return ''


def pi_function(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def happy_pi(s):
    return s[:pi_function(s)[-1]] if s else ''


def z_function(s):
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def happy_z(s):
    z = z_function(s)
    for i in range(1, len(s)):
        if i + z[i] == len(s):                  # smallest i = longest border
            return s[i:]
    return ''


def happy_hash(s, B=911382323, M=BIG):
    n = len(s)
    pre = suf = 0
    power = 1
    hits = []
    for L in range(1, n):                       # prefix hash grows right, suffix hash grows left
        pre = (pre * B + ord(s[L - 1])) % M
        suf = (suf + ord(s[n - L]) * power) % M
        power = power * B % M
        if pre == suf:
            hits.append(L)
    for L in reversed(hits):                    # verify longest first; a collision is skipped
        if s[:L] == s[-L:]:
            return s[:L]
    return ''


for s, exp in [('level', 'l'), ('ababab', 'abab'), ('abc', ''), ('a', '')]:
    r = (happy_pi(s), happy_z(s), happy_hash(s), happy_brute(s))
    print(repr(s), r)
    assert all(x == exp for x in r), (s, r)
assert happy_pi('aaaa') == 'aaa' and happy_pi('abcab') == 'ab'
assert happy_pi('aabaaab') == 'aab'
assert happy_z('') == '' and happy_hash('') == ''

rng = random.Random(26)
cases = 0
for _ in range(4000):
    s = ''.join(rng.choice('ab') for _ in range(rng.randint(1, 14)))
    b = happy_brute(s)
    assert happy_pi(s) == b and happy_z(s) == b and happy_hash(s) == b, s
    # tiny modulus: many collisions, still right because hits are verified
    assert happy_hash(s, B=3, M=7) == b, s
    cases += 1
print('random cross-check passed (pi, Z, hash, hash with M=7):', cases, 'cases')
```

**Output (my run):**
```
'level' ('l', 'l', 'l', 'l')
'ababab' ('abab', 'abab', 'abab', 'abab')
'abc' ('', '', '', '')
'a' ('', '', '', '')
random cross-check passed (pi, Z, hash, hash with M=7): 4000 cases
```
All four prompt examples are correct.

**Edge cases:**
- Length 1: no proper prefix, answer `''`.
- No border (`'abc'`): `pi[-1] = 0`.
- All equal (`'aaaa'`): answer `'aaa'`, length `n - 1`, and the border may overlap itself.
- A border that overlaps (`'ababa'` has `'aba'`; the prefix and suffix share the middle `a`).

**Follow-ups:**
- *Do I need the longest border only?* Every shorter border is reachable by following `pi[k-1]` repeatedly from `pi[n-1]`.
- *Smallest period?* `n - pi[n-1]`, and the string is a repeat of that block only if it divides `n`.
- *Why not just compare hashes without verifying?* It is probabilistic; with a large prime modulus and random base the failure chance is tiny, but if the answer must be exact, verify.

**Common mistakes:**
- Returning `s[:pi[-1] + 1]` or confusing a length with an index.
- Allowing `L = n`, which makes the whole string its own happy prefix.
- In the hash version, rolling the suffix hash in the same direction as the prefix hash, so the two never line up.
- Using Z but taking the largest `i` instead of the smallest, which gives the shortest border.


### Q27 ⭐⭐ 🔴 Shortest palindrome by prepending. Given `s` (0 <= len <= 5*10^4, lowercase), return the shortest palindrome you can make by adding characters only at the front. Reduce it to the longest palindromic prefix of `s`, and find that in O(n) by running the prefix function on s + '#' + reverse(s). Contrast with the O(n^2) loop that tries each prefix. Example: 'aacecaaa' -> 'aaacecaaa'; 'abcd' -> 'dcbabcd'; '' -> ''; 'aba' -> 'aba'.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports

**Pattern:** Reduce to the longest palindromic prefix, and find that with the prefix function on a glued string.

**Say this first (1 line):** "To add characters only at the front, I keep the longest palindromic prefix as is and mirror the rest. The longest palindromic prefix is the last prefix-function value of `s + '#' + reverse(s)`."

**Brute force:** For `L` from `n` down to 0, check whether `s[:L]` is a palindrome. The first hit gives the answer `reverse(s[L:]) + s`. O(n^2) time.

**Optimal:**
- If `s[:L]` is a palindrome, then the characters `s[L:]` are what is left unmatched. Put their reverse in front: `reverse(s[L:]) + s`. The result is `reverse(s[L:]) + s[:L] + s[L:]`, a palindrome because `s[:L]` is one and the outer parts mirror. To be shortest, `L` must be as large as possible.
- Build `t = s + '#' + reverse(s)`. A prefix of `s` of length `L` is a palindrome exactly when it equals the matching suffix of `reverse(s)`, which is a prefix of `s` read backward. In `t`, that is a border of `t` of length `L`. The `#` stops the border from growing past `n`.
- `L = pi(t)[-1]`.
- The separator must not occur in `s` (the problem says lowercase). If it could, use a character outside the alphabet.

**Complexity:** Time O(n), space O(n) for `t` and `pi`. Brute force: O(n^2).

**Dry run:** `s = 'aacecaaa'`, `reverse = 'aaacecaa'`, `t = 'aacecaaa#aaacecaa'`
- The longest border of `t`: prefix `'aacecaa'` (length 7) equals the suffix `'aacecaa'` of `t`. Length 8 would be `'aacecaaa'`, but the suffix of length 8 is `'aaacecaa'`: no.
- `L = 7`, `s[7:] = 'a'`, reversed `'a'`, answer `'a' + 'aacecaaa' = 'aaacecaaa'`.

**Code:**
```python
import itertools
import random


def is_pal(x):
    return x == x[::-1]


def shortest_pal_brute(s):
    for L in range(len(s), -1, -1):
        if is_pal(s[:L]):
            return s[L:][::-1] + s
    return s                                   # unreachable: L = 0 always works


def pi_function(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def shortest_pal(s):
    if not s:
        return s
    t = s + '#' + s[::-1]
    L = pi_function(t)[-1]
    return s[L:][::-1] + s


def shortest_pal_exhaustive(s, alphabet):
    # truly exhaustive: try every possible prefix string of growing length
    for k in range(len(s) + 1):
        for pre in itertools.product(alphabet, repeat=k):
            cand = ''.join(pre) + s
            if is_pal(cand):
                return cand


for s, exp in [('aacecaaa', 'aaacecaaa'), ('abcd', 'dcbabcd'), ('', ''), ('aba', 'aba')]:
    print(repr(s), '->', repr(shortest_pal(s)))
    assert shortest_pal(s) == exp == shortest_pal_brute(s)
assert shortest_pal('a') == 'a' and shortest_pal('ab') == 'bab'
assert shortest_pal('aaaa') == 'aaaa'

rng = random.Random(27)
cases = 0
for _ in range(3000):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 14)))
    assert shortest_pal(s) == shortest_pal_brute(s), s
    cases += 1
for n in range(0, 7):                          # all strings over {a, b}, against the exhaustive search
    for tup in itertools.product('ab', repeat=n):
        s = ''.join(tup)
        assert shortest_pal(s) == shortest_pal_exhaustive(s, 'ab'), s
        cases += 1
print('random and exhaustive cross-check passed:', cases, 'cases')
big = 'a' * 30000 + 'b'
print(len(shortest_pal(big)))                  # linear time at the stated size limit
```

**Output (my run):**
```
'aacecaaa' -> 'aaacecaaa'
'abcd' -> 'dcbabcd'
'' -> ''
'aba' -> 'aba'
random and exhaustive cross-check passed: 3127 cases
30002
```
All four prompt examples are correct.

**Edge cases:**
- Empty string: return it (the code guards it; `pi_function('#')` would also work).
- Already a palindrome: `L = n`, nothing is added.
- No palindromic prefix longer than 1 (`'abcd'`): `L = 1`, add `n - 1` characters.
- Separator character present in the input: use one outside the alphabet.

**Follow-ups:**
- *Why does `#` matter?* Without it the border could cross from `s` into `reverse(s)` and report a length that is not a palindromic prefix (for example `'aaaa'` glued to itself).
- *Manacher instead?* Run Manacher and take the longest palindrome that starts at index 0. Also O(n), more code.
- *Appending at the end instead?* Symmetric: apply it to `reverse(s)`.

**Common mistakes:**
- Gluing without a separator.
- Mirroring the wrong part: prepend `reverse(s[L:])`, not `reverse(s[:L])`.
- Treating `L = 0` as an error for the empty string.
- Believing it is a DP (Part 11) or backtracking (Part 12) problem; it is a border problem.


### Q28 ⭐⭐ 🔴 Valid number. Decide whether a string (len <= 20, no spaces) is a valid decimal number under this grammar: an optional sign '+' or '-', then either digits optionally followed by '.' and more digits (so '4.' is valid) or '.' followed by at least one digit, then an optional exponent 'e' or 'E' followed by an optional sign and at least one digit. Parse it left to right with explicit stages (sign, integer digits, dot, fraction digits, exponent) and no regex in your main answer; mention the regex alternative and the finite-automaton view. Example: each of '2', '0089', '-0.1', '+3.14', '4.', '-.9', '2e10', '3e+7', '53.5e93' -> True; each of 'abc', '1a', '1e', 'e3', '99e2.5', '--6', '-+3', '95a54e53', '.', '+.' -> False.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports

**Pattern:** Staged scanner (a small hand-made finite automaton). Walk left to right once and move through fixed stages: sign, integer digits, dot, fraction digits, exponent, exponent sign, exponent digits.

**Say this first (1 line):** "I scan once with a position pointer. I count digits before and after the dot, and the mantissa is valid only if there is at least one digit on either side. Then an optional exponent needs at least one digit. If the pointer ends at the end of the string, it is valid."

**Brute force:** A regex, `[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?` with `fullmatch`. It is correct and I use it as the checker, but it is a black box in an interview and hides the stages. `float(s)` is wrong here: it accepts `'inf'`, `'nan'`, `'1_0'` and surrounding spaces.

**Optimal:**
- Stage 1: one optional `+` or `-`.
- Stage 2: count digits `a` (characters `'0'..'9'`).
- Stage 3: one optional `.`, then count digits `b`.
- The mantissa is valid iff `a + b > 0`. That one test covers `'4.'` (a=1), `'.9'` (b=1), and rejects `'.'` and `'+.'`.
- Stage 4: if the next character is `e` or `E`: skip it, one optional sign, count digits `c`; need `c > 0`.
- Finish: valid iff the pointer is at the end. This rejects `'99e2.5'` (a dot after the exponent) and `'1a'`.
- The automaton view: states `start, sign, int, dot-after-int, dot-no-int, frac, e, e-sign, e-digits`; accepting states are `int`, `dot-after-int`, `frac`, `e-digits`.

**Complexity:** Time O(n), space O(1), one pass, no backtracking.

**Dry run:** `'-.9'`
- `-`: sign, `i = 1`.
- digits before dot: none, `a = 0`.
- `.`: consumed, `i = 2`; digits after: `9`, `b = 1`, `i = 3`.
- `a + b = 1 > 0`, ok. No `e`. `i == n`: True.

`'99e2.5'`: `a = 2`, no dot, `e` consumed, exponent digits `2`, stop at `.`: `i = 4 != 6`: False.

**Code:**
```python
import itertools
import re

PATTERN = re.compile(r'[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?')


def is_number_regex(s):
    return PATTERN.fullmatch(s) is not None


def is_digit(c):
    return '0' <= c <= '9'                      # not c.isdigit(): that accepts Unicode digits


def is_number(s):
    n, i = len(s), 0
    if i < n and s[i] in '+-':
        i += 1
    a = 0
    while i < n and is_digit(s[i]):
        i += 1
        a += 1
    b = 0
    if i < n and s[i] == '.':
        i += 1
        while i < n and is_digit(s[i]):
            i += 1
            b += 1
    if a + b == 0:
        return False
    if i < n and s[i] in 'eE':
        i += 1
        if i < n and s[i] in '+-':
            i += 1
        c = 0
        while i < n and is_digit(s[i]):
            i += 1
            c += 1
        if c == 0:
            return False
    return i == n


yes = ['2', '0089', '-0.1', '+3.14', '4.', '-.9', '2e10', '3e+7', '53.5e93']
no = ['abc', '1a', '1e', 'e3', '99e2.5', '--6', '-+3', '95a54e53', '.', '+.']
for s in yes:
    assert is_number(s), s
for s in no:
    assert not is_number(s), s
print('yes ->', [is_number(s) for s in yes])
print('no  ->', [is_number(s) for s in no])
assert not is_number('') and not is_number('+') and not is_number('e') and not is_number('.e1')
assert is_number('0') and is_number('.5e-3') and is_number('5.e3') and is_number('-0')
assert not is_number(' 1') and not is_number('1 ') and not is_number('1e5e5')

# Exhaustive cross-check: every string up to length 7 over this alphabet, against the regex.
count = valid = 0
for n in range(0, 8):
    for tup in itertools.product('+-.eE1', repeat=n):
        s = ''.join(tup)
        r = is_number(s)
        assert r == is_number_regex(s), s
        count += 1
        valid += r
print('exhaustive cross-check passed:', count, 'strings,', valid, 'valid')

# The Unicode trap: isdigit and a bare \d accept more than ASCII digits.
print('\u0663'.isdigit(), '\u00b2'.isdigit(), bool(re.fullmatch(r'\d+', '\u0663')), is_number('\u0663'))
print(float('1_0'), float(' 1e3 '), float('inf'))
```

**Output (my run):**
```
yes -> [True, True, True, True, True, True, True, True, True]
no  -> [False, False, False, False, False, False, False, False, False, False]
exhaustive cross-check passed: 335923 strings, 488 valid
True True True False
10.0 1000.0 inf
```
All nineteen prompt examples are correct (nine valid, ten invalid).

**Edge cases:**
- `'4.'` is valid and `'.'` is not: the "digits on either side" rule.
- `'1e'`, `'e3'`, `'.e1'`: exponent without digits, or no mantissa.
- `'1e5e5'`, `'99e2.5'`: second exponent or dot after the exponent.
- Spaces: the grammar here has none, so `' 1'` is invalid (real `float` strips them).
- Unicode digits: `'\u0663'` (Arabic-Indic three) is `isdigit()`, and a bare `\d` in `re` matches it too, so compare against `'0'..'9'` or use `re.ASCII`.

**Follow-ups:**
- *Only integers, or also `inf`/`nan`?* A different grammar; extend the stage list, or special-case words.
- *Write it as a table-driven DFA?* A dict `state -> {char_class: next_state}`, same O(n). It is the right answer if the grammar keeps growing.
- *Why not `try: float(s)`?* It accepts extra forms (`'inf'`, `'nan'`, underscores, whitespace) and is not the specified grammar.

**Common mistakes:**
- Requiring digits on both sides of the dot (`'4.'` and `'.5'` are both valid).
- Allowing an exponent with no digits, or a dot inside the exponent.
- Using `str.isdigit`, which says yes to superscripts and non-ASCII digits.
- Treating a bare sign or a bare dot as valid.


### Q29 ⭐ 🟡 Bytes, code points and graphemes. Explain the difference between bytes, code points and user-perceived characters (graphemes) in Python and write `counts(s)` returning (number of code points, number of UTF-8 bytes, number of UTF-16 code units) for a str. State what `len(s)` counts, why the same visible 'e-acute' can be 1 or 2 code points, why a flag or family emoji is several code points, and why slicing, indexing and reversal can cut a grapheme (the standard library has no grapheme segmenter; name the third-party options). Example: counts('a\u00e9\U0001F600') -> (3, 7, 4); len('e\u0301') -> 2 but len('\u00e9') -> 1; len('\U0001F600'.encode('utf-8')) -> 4.
**Asked at:** Unicode and Python text-handling docs and tutorials (pandas and xarray str.normalize pages and the pyunormalize project surfaced by search; snippets only, the official Python unicodedata and str docs were not opened, so claims about casefold and grapheme clusters rest on editor knowledge and the sandbox run) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Three different "lengths" of the same text. A **byte** is what is stored or sent (depends on the encoding). A **code point** is one Unicode number, and it is what Python's `str` indexes. A **grapheme** is what a person sees as one character, and it can be several code points.

**Say this first (1 line):** "`len(s)` counts code points, not bytes and not what the eye sees. Bytes depend on the encoding, UTF-16 counts surrogate pairs as two units, and a visible character like an accented letter, a flag or a family emoji can be several code points."

**Brute force:** There is no algorithmic brute force here, but there is a second way to count that I use as a checker: take the UTF-8 bytes, count the bytes that are not continuation bytes (`b & 0xC0 != 0x80`) to get code points, and give each code point 1 UTF-16 unit, or 2 if it is above `0xFFFF`.

**Optimal:**
- `counts(s) = (len(s), len(s.encode('utf-8')), len(s.encode('utf-16-le')) // 2)`.
- Use `utf-16-le` (no BOM). Plain `'utf-16'` adds a 2-byte byte-order mark, so the length is off by one unit.
- UTF-8 uses 1 byte up to U+007F, 2 up to U+07FF, 3 up to U+FFFF, 4 above. UTF-16 uses 1 unit up to U+FFFF and a surrogate pair (2 units) above. JavaScript and Java `length` is this UTF-16 count.
- `len('e\u0301') == 2` and `len('\u00e9') == 1` for the same visible letter: one is a base letter plus a combining accent, the other a precomposed letter. NFC normalisation joins them where a precomposed form exists (Part 3 Q30).
- A flag (two regional-indicator letters) and a family emoji (several people joined by zero-width joiners) are several code points but look like one symbol.
- Slicing, indexing and reversing work on code points, so they can cut a grapheme in the middle: split the accent from its letter, or reverse a flag into a different flag.
- The standard library has no grapheme segmenter. Third-party options include the `regex` module (`\X`), the `grapheme` package, `uniseg`, and PyICU. None of these is installed in my sandbox, so I did not run them.
- Python 3.13 detail, as observed: a `str` is stored per object with 1, 2 or 4 bytes per character depending on the widest character (PEP 393), so `sys.getsizeof` grows by 1, 1, 2 and 4 bytes per character for `'a'`, `'\u00e9'`, a CJK character and an emoji. That is an implementation detail, not a language promise.

**Complexity:** `len` is O(1). `counts` is O(n) because it encodes. Space O(n) for the temporary byte strings.

**Dry run:** `'a\u00e9\U0001F600'`
| char | code point | UTF-8 bytes | UTF-16 units |
|---|---|---|---|
| a | U+0061 | 1 | 1 |
| e-acute | U+00E9 | 2 | 1 |
| grinning face | U+1F600 | 4 | 2 |
| total | 3 | 7 | 4 |

**Code:**
```python
import random
import sys
import unicodedata


def counts(s):
    return len(s), len(s.encode('utf-8')), len(s.encode('utf-16-le')) // 2


def counts_by_bytes(s):                         # brute force, built from the raw UTF-8 bytes
    b = s.encode('utf-8')
    cps = sum(1 for x in b if x & 0xC0 != 0x80)
    units = 0
    i = 0
    while i < len(b):
        lead = b[i]
        if lead < 0x80:
            step, units = 1, units + 1
        elif lead < 0xE0:
            step, units = 2, units + 1
        elif lead < 0xF0:
            step, units = 3, units + 1
        else:
            step, units = 4, units + 2
        i += step
    return cps, len(b), units


print(counts('a\u00e9\U0001F600'))
assert counts('a\u00e9\U0001F600') == (3, 7, 4)
assert counts('') == (0, 0, 0) and counts('abc') == (3, 3, 3)
print(len('e\u0301'), len('\u00e9'), len('\U0001F600'.encode('utf-8')))
assert len('e\u0301') == 2 and len('\u00e9') == 1 and len('\U0001F600'.encode('utf-8')) == 4

rng = random.Random(29)
cases = 0
for _ in range(3000):
    chars = []
    for _ in range(rng.randint(0, 8)):
        lo, hi = rng.choice([(0, 0x7F), (0x80, 0x7FF), (0x800, 0xD7FF), (0xE000, 0xFFFF), (0x10000, 0x10FFFF)])
        chars.append(chr(rng.randint(lo, hi)))
    s = ''.join(chars)
    assert counts(s) == counts_by_bytes(s), s
    cases += 1
print('random cross-check passed:', cases, 'cases')

# A visible character as 1 or 2 code points; NFC joins them where a precomposed form exists.
decomposed, precomposed = 'e\u0301', '\u00e9'
print(decomposed == precomposed, unicodedata.normalize('NFC', decomposed) == precomposed)

# A flag is two regional indicators; reversing the string gives a different flag.
flag = '\U0001F1EE\U0001F1F3'
print(len(flag), counts(flag), [unicodedata.name(c).split()[-1] for c in flag])
print([unicodedata.name(c).split()[-1] for c in flag[::-1]])

# A family emoji: three people joined by two zero-width joiners.
family = '\U0001F468\u200d\U0001F469\u200d\U0001F467'
print(len(family), counts(family))

# Slicing cuts a grapheme: the accent is left behind.
print(repr('cafe\u0301'[:4]), repr('cafe\u0301'[:5]))

# Plain 'utf-16' adds a byte-order mark; lone surrogates cannot be encoded to UTF-8 by default.
print(len('a'.encode('utf-16')), len('a'.encode('utf-16-le')))
try:
    '\ud800'.encode('utf-8')
except UnicodeEncodeError as e:
    print(type(e).__name__)

# CPython storage width per character (observed in this run; an implementation detail).
for ch in ('a', '\u00e9', '\u4e2d', '\U0001F600'):
    print(hex(ord(ch)), sys.getsizeof(ch * 200) - sys.getsizeof(ch * 100), 'bytes per 100 chars')
print(sys.version.split()[0])
```

**Output (my run):**
```
(3, 7, 4)
2 1 4
random cross-check passed: 3000 cases
False True
2 (2, 8, 4) ['I', 'N']
['N', 'I']
5 (5, 18, 8)
'cafe' 'café'
4 2
UnicodeEncodeError
0x61 100 bytes per 100 chars
0xe9 100 bytes per 100 chars
0x4e2d 200 bytes per 100 chars
0x1f600 400 bytes per 100 chars
3.13.17
```
All three prompt examples are correct. Python 3.13 behaviour is as observed above, including that `'a'.encode('utf-16')` is 4 bytes (2 BOM plus 2).

**Edge cases:**
- Empty string: `(0, 0, 0)`.
- Lone surrogate (`'\ud800'`): a legal `str` in Python but not encodable to UTF-8 by default; use `errors='surrogatepass'` if you must.
- Characters above U+FFFF: 4 UTF-8 bytes, 2 UTF-16 units (a surrogate pair).
- Combining marks, zero-width joiners and flags: code points that are not characters on their own.

**Follow-ups:**
- *How would you count graphemes?* Use a segmenter per Unicode UAX #29 (the `regex` module's `\X`, or `grapheme`/`uniseg`/ICU). Do not use `len` or a combining-mark check; the latter covers accents only (Part 3 Q31).
- *What does `len(b'...')` count?* Bytes. A `bytes` object has no characters; decoding is the step that creates code points.
- *Why do databases and APIs report different "lengths"?* Each counts a different unit: bytes (UTF-8), UTF-16 units (JS, Java), or code points (Python). Check which one a limit means.

**Common mistakes:**
- Assuming `len(s)` equals bytes, or equals what the user sees.
- Using `'utf-16'` (with BOM) when counting units.
- Truncating by slicing at a byte or code-point boundary in the middle of a grapheme.
- Sorting or comparing without normalising, so `'e\u0301'` and `'\u00e9'` differ.


### Q30 ⭐ 🟡 Normalisation and case-folding. Write `same_text(a, b, compat=False)` that decides whether two strings are 'the same text' for a username or search key: apply casefold (not lower) and Unicode normalisation, in the order that is safe (normalise, casefold, normalise again), using NFC or NFD canonical form by default and NFKC/NFKD compatibility form when `compat` is True. Explain the difference between canonical and compatibility equivalence, why 'ss' matches the German sharp s under casefold but not under lower, and one security reason for normalising before comparing. Example: same_text('Stra\u00dfe','STRASSE') -> True; same_text('e\u0301','\u00e9') -> True; same_text('\u2460','1') -> False; same_text('\u2460','1', compat=True) -> True.
**Asked at:** Unicode and Python text-handling docs and tutorials (pandas and xarray str.normalize pages and the pyunormalize project surfaced by search; snippets only, the official Python unicodedata and str docs were not opened, so claims about casefold and grapheme clusters rest on editor knowledge and the sandbox run) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Canonical key for text equality: normalise, case-fold, normalise again, then compare. Python's `unicodedata` and `str.casefold` do the work.

**Say this first (1 line):** "Equal-looking text can be different code points, so I compare a canonical form. `casefold` handles case (stronger than `lower`), normalisation handles composed versus decomposed forms, and I normalise again because casefolding can produce new combining sequences."

**Brute force:** `a.lower() == b.lower()` or `a == b`. Both fail: `'Stra\u00dfe'.lower()` stays `'stra\u00dfe'` (the sharp s has no lowercase change), and `'e\u0301' != '\u00e9'`. A second reference method I use as a checker: the Unicode Standard's own definitions of caseless matching, which are `NFD(casefold(NFD(x)))` for canonical matching and `NFKD(casefold(NFKD(casefold(NFD(x)))))` for compatibility matching.

**Optimal:**
- `form = 'NFKC' if compat else 'NFC'`.
- `key(x) = normalize(form, normalize(form, x).casefold())`.
- `same_text(a, b, compat) = key(a) == key(b)`.
- Canonical versus compatibility equivalence:
  - Canonical: same abstract character, different encoding (`'e' + U+0301` and `U+00E9`). NFC and NFD only reorder and compose or decompose; they do not change meaning.
  - Compatibility: similar characters that differ in form (circled one `U+2460` and `'1'`, the fi ligature, fullwidth letters, superscripts). NFKC and NFKD fold these, and that loses information, so use it for search keys, not for storing the original text.
- `casefold` versus `lower`: `casefold` is for caseless comparison and maps `'\u00df'` to `'ss'`, so `'Stra\u00dfe'` matches `'STRASSE'`. `lower` keeps `'\u00df'`.
- Why normalise again after the casefold: casefold can output a sequence that is not normalised. The code below counts them: in Python 3.13's Unicode data (15.1) there are 26 single code points (for example U+01F0, j with caron, which folds to `'j'` plus a combining caron) where `casefold` returns text that NFC changes. So the second normalise is not decoration.
- Reference check: the code compares this three-step key with the Unicode Standard's caseless-matching formulas on a pool of tricky strings, and on every single code point. Observed: zero disagreements (pool and single code points) in both modes.
- Security reason: without normalising, two usernames can look the same but be different strings (precomposed versus decomposed), so one person can register a look-alike account, or a blocklist and a uniqueness check can be bypassed. Normalisation fixes canonical look-alikes only. It does not fix homoglyphs from other scripts: Cyrillic `'\u0430'` and Latin `'a'` stay different; that needs a confusables check.
- Two caveats: casefold is locale-independent (Turkish dotless and dotted i are not handled specially), and normalisation form choice must be fixed and documented when keys are stored.

**Complexity:** O(n) time and space in the length of the strings (normalisation and casefold are linear passes; a rare long combining sequence needs reordering, which is still linear in practice).

**Dry run:** `same_text('Stra\u00dfe', 'STRASSE')`
- `'Stra\u00dfe'` NFC is unchanged, casefold gives `'strasse'`, NFC unchanged.
- `'STRASSE'` NFC unchanged, casefold `'strasse'`.
- Keys equal: True.

`same_text('\u2460', '1')`
- NFC leaves circled one alone, casefold leaves it alone: key `'\u2460'` against `'1'`: False.
- With `compat=True`: NFKC maps circled one to `'1'`: True.

**Code:**
```python
import random
import unicodedata

N = unicodedata.normalize


def same_text(a, b, compat=False):
    form = 'NFKC' if compat else 'NFC'
    key = lambda x: N(form, N(form, x).casefold())
    return key(a) == key(b)


def same_text_standard(a, b, compat=False):     # reference: the Unicode Standard's formulas
    if compat:
        key = lambda x: N('NFKD', N('NFKD', N('NFD', x).casefold()).casefold())
    else:
        key = lambda x: N('NFD', N('NFD', x).casefold())
    return key(a) == key(b)


def same_text_naive(a, b):
    return a.lower() == b.lower()


print(same_text('Stra\u00dfe', 'STRASSE'))
print(same_text('e\u0301', '\u00e9'))
print(same_text('\u2460', '1'))
print(same_text('\u2460', '1', compat=True))
assert same_text('Stra\u00dfe', 'STRASSE') is True
assert same_text('e\u0301', '\u00e9') is True
assert same_text('\u2460', '1') is False
assert same_text('\u2460', '1', compat=True) is True

print('lower vs casefold:', 'Stra\u00dfe'.lower(), 'Stra\u00dfe'.casefold(), same_text_naive('Stra\u00dfe', 'STRASSE'))
print('raw equality of e-acute forms:', 'e\u0301' == '\u00e9', len('e\u0301'), len('\u00e9'))
print('homoglyph (Cyrillic a vs Latin a):', same_text('\u0430', 'a'), same_text('\u0430', 'a', compat=True))
print('dotted capital I:', ascii('\u0130'.casefold()), same_text('\u0130', 'i'))
print('ligature fi:', same_text('\ufb01', 'fi'))
print('fullwidth A:', same_text('\uff21', 'a'), same_text('\uff21', 'a', compat=True))
print('unidata version in this Python:', unicodedata.unidata_version)

assert same_text('', '') and not same_text('a', '')
assert same_text('\u00c5', 'A\u030a') and same_text('\u212b', '\u00e5')   # angstrom sign, A-ring
assert same_text('a\u0323\u0301', 'a\u0301\u0323')                          # mark order is normalised
assert same_text('\u03c2', '\u03a3') and same_text('\u00b2', '2', compat=True)

pool = ['a', 'A', 'e', 'E', 's', 'S', 'i', 'I', 'k', 'K', '1', '\u00e9', '\u00c9', 'e\u0301', 'E\u0301',
        '\u00df', '\u1e9e', 'ss', 'SS', '\u2460', '\ufb01', 'fi', '\uff21', '\u0130', '\u03c3', '\u03c2', '\u03a3',
        '\u212a', '\u212b', '\u00e5', 'a\u030a', '\u0345', '\u1f80', '\u2126', '\u03c9', '\u01c5', '\u00b2', '2']
rng = random.Random(30)
cases = diff_compat = 0
for _ in range(6000):
    a = ''.join(rng.choice(pool) for _ in range(rng.randint(0, 3)))
    b = ''.join(rng.choice(pool) for _ in range(rng.randint(0, 3)))
    for compat in (False, True):
        assert same_text(a, b, compat) == same_text_standard(a, b, compat), (a, b, compat)
    assert same_text(a, a) and same_text(a, a, True)                    # reflexive
    assert same_text(a, b) == same_text(b, a)                           # symmetric
    if same_text(a, b):
        assert same_text(a, b, True)                                    # canonical match implies compat match
    else:
        diff_compat += same_text(a, b, True)
    cases += 1
print('pool cross-check against the standard formulas passed:', cases, 'cases;',
      'compat matched where canonical did not:', diff_compat > 0)

# Exhaustive over single code points (about 1.1 million), both modes.
# (The comparison below pits NFC/NFKC of the 3-step key against the standard's NFD/NFKD formulas, normalised the same way.)
bad = 0
for cp in range(0x110000):
    if 0xD800 <= cp < 0xE000:
        continue
    c = chr(cp)
    if N('NFC', N('NFC', c).casefold()) != N('NFC', N('NFD', N('NFD', c).casefold())):
        bad += 1
    if N('NFKC', N('NFKC', c).casefold()) != N('NFKC', N('NFKD', N('NFKD', N('NFD', c).casefold()).casefold())):
        bad += 1
print('single code points where the 3-step key and the standard disagree:', bad)

# Is the second normalise needed? Count code points where casefold output is not already normalised.
need = sum(1 for cp in range(0x110000) if not 0xD800 <= cp < 0xE000
           and N('NFC', N('NFC', chr(cp)).casefold()) != N('NFC', chr(cp)).casefold())
print('code points where casefold output changes under a second NFC:', need)
```

**Output (my run):**
```
True
True
False
True
lower vs casefold: straße strasse False
raw equality of e-acute forms: False 2 1
homoglyph (Cyrillic a vs Latin a): False False
dotted capital I: 'i\u0307' False
ligature fi: True
fullwidth A: False True
unidata version in this Python: 15.1.0
pool cross-check against the standard formulas passed: 6000 cases; compat matched where canonical did not: True
single code points where the 3-step key and the standard disagree: 0
code points where casefold output changes under a second NFC: 26
```
All four prompt examples are correct. The line `same_text('\u0130', 'i')` shows casefold turning dotted capital I into `'i'` plus a combining dot, so it is not equal to plain `'i'`; no locale rules apply.

**Edge cases:**
- Empty strings.
- Strings with multiple combining marks (order matters; normalisation puts them in canonical order, so `'a\u0323\u0301'` and `'a\u0301\u0323'` become equal).
- Final sigma `'\u03c2'` versus `'\u03c3'` and capital `'\u03a3'`: casefold maps all three to the same lowercase sigma.
- Compatibility mode is lossy: `'\u00b2'` (superscript two) equals `'2'`. Do not use it where `x2` and `x` squared must stay different.
- Unicode version: the answers for new or rare characters depend on the Unicode data in your Python build (here 15.1).

**Follow-ups:**
- *Why not `str.upper()` for comparison?* Same issue as `lower`; `casefold` is the tool designed for caseless matching.
- *Should I store the folded key or the original?* Store the original for display and a normalised, case-folded key for uniqueness checks and lookups.
- *Is that enough to stop spoofing?* No: homoglyphs from other scripts, zero-width characters and bidirectional controls need extra checks (confusables detection, restricting scripts).

**Common mistakes:**
- Using `lower()` for caseless matching.
- Normalising only one side, or comparing different forms (NFC on one, NFD on the other).
- Applying compatibility normalisation to data you will later display or store as the user's real text.
- Forgetting that normalisation does not touch homoglyphs.
