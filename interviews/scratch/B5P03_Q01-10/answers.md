### Q1 ⭐⭐⭐ 🟢 Reverse words in a string. Given a string `s` (1 <= len <= 10^4) of letters, digits and spaces, with possible leading, trailing and repeated spaces, return the words in reverse order joined by exactly one space and no leading or trailing space. Give the `split()` one-liner, then a manual single-pass parse that does not rely on `split`, and the follow-up where the input is a mutable list of characters and you must use O(1) extra space (reverse everything, then reverse each word). Example: '  the sky  is blue ' -> 'blue is sky the'; 'a' -> 'a'; '   ' -> ''.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** String parsing in one pass (scan from the end, or two-phase reverse). Words are separated by runs of spaces, so I track word boundaries, not single characters.

**Say this first (1 line):** "In Python it is `' '.join(reversed(s.split()))`; `split()` with no argument already drops leading, trailing and repeated spaces. If they want it by hand, I scan from the right, cut each word, and join. For a mutable char list I reverse everything, then reverse each word."

**Brute force:** `' '.join(reversed(s.split()))`. O(n) time and O(n) space. It is also my checker. It is a fine answer, but the interviewer usually asks for the manual version next.

**Optimal:**
- Manual pass: start `i` at the last index. Skip spaces going left. Mark `j = i`. Walk left while not a space. The word is `s[i+1:j+1]`. Append it to a list. Repeat. Then `' '.join(words)`.
- In-place (list of chars, O(1) extra space):
  - Reverse the whole list. Words are now in the right order, but each word is backwards.
  - Walk the list, find each word, reverse it back.
  - Squeeze spaces with a write pointer: copy a word, put one space before it if it is not the first, skip all other spaces, then `del chars[w:]` to trim.
- Invariant for the manual scan: everything right of `i` has been turned into words already.

**Complexity:** Time O(n): every index is visited a constant number of times (each reverse touches each character at most twice). Space: `split` and manual versions O(n) for the output list; the in-place version O(1) extra, apart from the output it mutates.

**Dry run:** `s = '  the sky  is blue '`, manual scan from the right.
| step | i moves | word cut | words so far |
|---|---|---|---|
| 1 | skip trailing space, walk over 'blue' | blue | [blue] |
| 2 | skip space, walk over 'is' | is | [blue, is] |
| 3 | skip 2 spaces, walk over 'sky' | sky | [blue, is, sky] |
| 4 | skip space, walk over 'the' | the | [blue, is, sky, the] |
| 5 | skip 2 spaces, i < 0, stop | | join gives `blue is sky the` |

In-place on `'ab cd'`: reverse all gives `'dc ba'`; reverse each word gives `'cd ab'`.

**Code:**
```python
import random


def rev_words_split(s):
    return " ".join(reversed(s.split()))


def rev_words_manual(s):
    # scan from the right; collect each word, no split()
    words = []
    i = len(s) - 1
    while i >= 0:
        while i >= 0 and s[i] == " ":
            i -= 1
        if i < 0:
            break
        j = i
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:j + 1])
    return " ".join(words)


def rev_words_inplace(chars):
    # chars is a list of single characters; O(1) extra space, mutates and returns it
    def rev(a, b):  # reverse chars[a..b] inclusive
        while a < b:
            chars[a], chars[b] = chars[b], chars[a]
            a += 1
            b -= 1

    n = len(chars)
    rev(0, n - 1)
    i = 0
    while i < n:                      # reverse each word back
        if chars[i] == " ":
            i += 1
            continue
        j = i
        while j + 1 < n and chars[j + 1] != " ":
            j += 1
        rev(i, j)
        i = j + 1
    # squeeze spaces in place: write pointer w, one space between words
    w = 0
    i = 0
    while i < n:
        if chars[i] != " ":
            if w > 0:
                chars[w] = " "
                w += 1
            while i < n and chars[i] != " ":
                chars[w] = chars[i]
                w += 1
                i += 1
        else:
            i += 1
    del chars[w:]
    return chars


examples = [("  the sky  is blue ", "blue is sky the"), ("a", "a"), ("   ", "")]
for s, want in examples:
    a, b = rev_words_split(s), rev_words_manual(s)
    c = "".join(rev_words_inplace(list(s)))
    assert a == b == c == want, (s, a, b, c, want)
    print(repr(s), "->", repr(a))

assert rev_words_manual("") == "" and rev_words_split("") == ""
assert rev_words_manual("x  y") == "y x"
assert rev_words_manual(" ab") == "ab"
assert "".join(rev_words_inplace(list("hello   world  "))) == "world hello"
big = "ab " * 3333 + "z"
assert rev_words_manual(big) == rev_words_split(big)

rng = random.Random(3)
cases = 0
for _ in range(3000):
    s = "".join(rng.choice("ab1  ") for _ in range(rng.randint(1, 12)))
    want = rev_words_split(s)
    assert rev_words_manual(s) == want, s
    assert "".join(rev_words_inplace(list(s))) == want, s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'  the sky  is blue ' -> 'blue is sky the'
'a' -> 'a'
'   ' -> ''
random cross-check passed: 3000 cases
```
All three examples in the prompt are correct.

**Edge cases:**
- Only spaces (`'   '`): result is `''`, not `' '`.
- One word, with or without spaces around it.
- Repeated spaces between words: collapse to one.
- Length 10^4 is trivial here; the list-based version builds no big intermediate string.

**Follow-ups:**
- *Reverse the letters inside each word but keep word order?* Same helper, skip the whole-list reverse (split, reverse each, join).
- *Why not `s[::-1].split()`?* That reverses letters too. You would need to reverse each word again.
- *Why is `str.split(' ')` wrong here?* With an explicit space it keeps empty strings for repeated spaces. `split()` with no argument splits on any whitespace run and drops the empties. Note it also splits on tabs and newlines, which is fine for this problem as stated (letters, digits, spaces).

**Common mistakes:**
- Using `split(' ')` and leaving empty words, so the output has extra spaces.
- Forgetting the in-place version must also remove extra spaces, not only reorder.
- Not bounding the inner scans (`i >= 0`), which gives an index error at the string edges.
- Calling `s.strip()` and thinking it handles the repeated spaces inside.

### Q2 ⭐⭐⭐ 🟢 Longest common prefix. Given a list `strs` of lowercase strings (1 <= len(strs) <= 200, each length <= 200, empty strings allowed), return the longest string that is a prefix of every element, or '' if none. Show vertical scanning (compare column by column), the horizontal 'shrink the prefix' version, and the trick of comparing only the lexicographically smallest and largest strings; state the cost in terms of total characters. Example: ['flower','flow','flight'] -> 'fl'; ['dog','racecar','car'] -> ''; ['a'] -> 'a'; ['','b'] -> ''.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Scan by column (character index) across a list of strings. This is string comparison, not hashing.

**Say this first (1 line):** "Take the first string as the candidate and check each column against all other strings; stop at the first mismatch or at the end of any string. Cost is at most the total number of characters."

**Brute force:** For every length `k` from `len(strs[0])` down to 0, test whether `strs[0][:k]` is a prefix of all strings. About O(L * S) per length, so O(L^2 * S) in the worst case for first-string length L and S strings. Fine for size 200 but wasteful. It is my checker.

**Optimal:** Three equal-class options, all O(total characters) worst case:
- **Vertical scan:** for column `i`, compare `strs[0][i]` with `t[i]` for every other string `t`. Stop when `i == len(t)` or characters differ. Return `strs[0][:i]`.
- **Horizontal shrink:** `prefix = strs[0]`; for each next string, chop one character from the end of `prefix` until `t.startswith(prefix)`. Prefix only ever gets shorter.
- **Min and max trick:** the common prefix of the whole list equals the common prefix of the lexicographically smallest and largest strings. Any string between them in sorted order must share what those two share. Then compare just two strings.
- Invariant (vertical): at column `i`, every string agrees with `strs[0]` on columns `0..i-1`.

**Complexity:**
- Vertical and horizontal: O(S * m) where m is the length of the answer plus one (the mismatch column). In the worst case that is the total number of characters, O(sum of lengths). Space O(1) besides the returned slice.
- Min/max: `min` and `max` each compare strings, up to O(total chars) in the worst case, then O(L) for the final scan. Same bound, O(1) extra space.

**Dry run:** `['flower','flow','flight']`, vertical.
| column i | first[i] | others | result |
|---|---|---|---|
| 0 | f | f, f | ok |
| 1 | l | l, l | ok |
| 2 | o | 'flow'[2] = 'o' ok, but 'flight'[2] = 'i' | mismatch, return `first[:2]` = 'fl' |

Min/max: min = 'flight', max = 'flow'; they agree on 'f','l', then 'i' vs 'o' differ: 'fl'.

**Code:**
```python
import random


def lcp_brute(strs):
    # try every length k from the length of strs[0] downwards
    for k in range(len(strs[0]), -1, -1):
        p = strs[0][:k]
        if all(t.startswith(p) for t in strs):
            return p


def lcp_vertical(strs):
    first = strs[0]
    for i in range(len(first)):
        for t in strs[1:]:
            if i == len(t) or t[i] != first[i]:
                return first[:i]
    return first


def lcp_horizontal(strs):
    prefix = strs[0]
    for t in strs[1:]:
        while not t.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


def lcp_minmax(strs):
    lo, hi = min(strs), max(strs)      # lexicographic order
    i = 0
    while i < len(lo) and i < len(hi) and lo[i] == hi[i]:
        i += 1
    return lo[:i]


examples = [(["flower", "flow", "flight"], "fl"), (["dog", "racecar", "car"], ""),
            (["a"], "a"), (["", "b"], "")]
for strs, want in examples:
    r = [lcp_brute(strs), lcp_vertical(strs), lcp_horizontal(strs), lcp_minmax(strs)]
    assert all(x == want for x in r), (strs, r, want)
    print(strs, "->", repr(want))

assert lcp_vertical(["abc", "abc", "abc"]) == "abc"
assert lcp_vertical(["ab", "abc"]) == "ab"          # one string is a prefix of another
assert lcp_minmax(["abc", "ab", "abd"]) == "ab"
assert lcp_horizontal(["", ""]) == ""
assert lcp_minmax(["x" * 200] * 200) == "x" * 200

rng = random.Random(11)
cases = 0
for _ in range(3000):
    k = rng.randint(1, 5)
    strs = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 6))) for _ in range(k)]
    want = lcp_brute(strs)
    assert lcp_vertical(strs) == want, strs
    assert lcp_horizontal(strs) == want, strs
    assert lcp_minmax(strs) == want, strs
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
['flower', 'flow', 'flight'] -> 'fl'
['dog', 'racecar', 'car'] -> ''
['a'] -> 'a'
['', 'b'] -> ''
random cross-check passed: 3000 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- One string: the answer is that string.
- Empty string anywhere: answer is `''` (vertical hits `i == len(t)` at column 0).
- One string is a prefix of another (`['ab','abc']`): the shorter one is the answer; this is why the `i == len(t)` check matters.
- All strings identical: scan the full length once.

**Follow-ups:**
- *Why is min/max correct?* Strings between them in lexicographic order cannot break a shared prefix, so the two extremes bound the whole list.
- *Many queries on the same set?* Build a trie (Part 12 owns it) and walk until a node has more than one child or ends a word.
- *Sorted input?* Then just compare the first and last.

**Common mistakes:**
- Indexing `t[i]` without checking `i < len(t)`.
- Returning the wrong thing when the list is empty. The prompt promises at least one string, but say so out loud.
- Using `os.path.commonprefix` in an interview and calling it done; it is fine as a one-liner but they will ask for the algorithm.
- Claiming O(n) without saying what n is. Say total characters.

### Q3 ⭐⭐⭐ 🟢 Roman numeral to integer. Given a valid Roman numeral `s` for a value in 1..3999 (symbols I, V, X, L, C, D, M with the usual subtractive pairs IV, IX, XL, XC, CD, CM), return its integer value in one left-to-right pass. Explain the rule 'subtract when a symbol is smaller than the one after it' and why no stack is needed. Example: 'III' -> 3; 'LVIII' -> 58; 'MCMXCIV' -> 1994; 'IX' -> 9.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** One left-to-right pass with a one-symbol look-ahead. Roman numerals are a sum where a smaller symbol before a larger one is negated.

**Say this first (1 line):** "Add each symbol's value, but subtract it if the next symbol is bigger. IV is 5 minus 1 because I sits before V. One pass, O(n), no stack."

**Brute force:** Replace the six subtractive pairs first (`IV` to `IIII`, `IX` to `VIIII`, and so on), then add values. It works but costs several passes and string copies. As a checker I use the reverse direction instead: encode every integer 1..3999 to Roman and decode it back.

**Optimal:**
- Look-up table `I=1, V=5, X=10, L=50, C=100, D=500, M=1000`.
- For index `i`: if `i+1 < n` and `val[s[i]] < val[s[i+1]]`, subtract; else add.
- Why no stack: the only thing that matters about earlier symbols is their already-applied sign. Each symbol's sign depends only on its right neighbour, so one look-ahead is enough.
- Why subtract the left symbol and not the right: in `IX`, adding 1 and then 10 would give 11. Subtracting I gives -1 + 10 = 9. The sum is the same as the textbook rule because the pair counts as `10 - 1`.
- Equivalent: walk from the right and subtract when a symbol is smaller than the biggest seen so far. I include it as a second check.

**Complexity:** Time O(n). Space O(1) (the table has seven entries).

**Dry run:** `s = 'MCMXCIV'`
| symbol | next | action | total |
|---|---|---|---|
| M | C | 1000 >= 100, add | 1000 |
| C | M | 100 < 1000, subtract | 900 |
| M | X | add | 1900 |
| X | C | 10 < 100, subtract | 1890 |
| C | I | add | 1990 |
| I | V | 1 < 5, subtract | 1989 |
| V | none | add | 1994 |

**Code:**
```python
VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    total = 0
    for i, ch in enumerate(s):
        v = VAL[ch]
        if i + 1 < len(s) and v < VAL[s[i + 1]]:
            total -= v
        else:
            total += v
    return total


def int_to_roman(n):
    # brute-force oracle: greedy encode, used to test the decoder for every value
    table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
             (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    out = []
    for v, sym in table:
        while n >= v:
            out.append(sym)
            n -= v
    return "".join(out)


def roman_to_int_right_to_left(s):
    # alternative: walk from the right, remember the biggest symbol seen so far
    total = best = 0
    for ch in reversed(s):
        v = VAL[ch]
        if v < best:
            total -= v
        else:
            total += v
            best = v
    return total


examples = [("III", 3), ("LVIII", 58), ("MCMXCIV", 1994), ("IX", 9)]
for s, want in examples:
    assert roman_to_int(s) == roman_to_int_right_to_left(s) == want, (s, want)
    print(s, "->", roman_to_int(s))

assert roman_to_int("I") == 1
assert roman_to_int("MMMCMXCIX") == 3999
assert roman_to_int("IV") == 4 and roman_to_int("VI") == 6
for n in range(1, 4000):                       # exhaustive: every legal value
    r = int_to_roman(n)
    assert roman_to_int(r) == n, (n, r)
    assert roman_to_int_right_to_left(r) == n, (n, r)
print("exhaustive round-trip passed: 3999 values")
```

**Output (my run):**
```
III -> 3
LVIII -> 58
MCMXCIV -> 1994
IX -> 9
exhaustive round-trip passed: 3999 values
```
All four examples in the prompt are correct. The input is promised valid, so I do not validate the numeral (a validity check is a different question).

**Edge cases:**
- Single symbol (`'I'`).
- Maximum, `MMMCMXCIX` = 3999.
- Repeated symbols (`III`, `XXX`) just add.
- Subtractive pair at the very end (`IV`): the last symbol has no right neighbour, so it adds. Index guard matters.

**Follow-ups:**
- *Integer to Roman?* Greedy over a descending table of 13 values (including 900, 400, 90, 40, 9, 4). I use it as the checker.
- *Validate the input?* You need rules: at most three repeats of I, X, C, M; V, L, D never repeat; only specific subtractive pairs. A regex works for 1..3999.
- *Why is `I` before `X` fine but `I` before `C` not?* Only the six listed pairs are legal. The decoder here does not check that.

**Common mistakes:**
- Reading `s[i+1]` on the last index.
- Writing `if s[i] > s[i+1]` on characters, which compares letters, not values.
- Subtracting the right symbol instead of the left one.
- Building a dict with `IV: 4` style keys and scanning two characters at a time, then forgetting the single-char fallback.

### Q4 ⭐⭐⭐ 🟢 Find the first occurrence of a pattern (strStr). Given `haystack` and `needle` (lengths up to 10^4, lowercase), return the lowest index where `needle` occurs in `haystack`, or -1; an empty needle returns 0. Write the naive double loop without `str.find`, state its worst-case time (give an input that forces O(n*m)) and say what str.find does in CPython at a high level (do not claim exact internals). KMP and the other linear-time methods are separate questions. Example: ('sadbutsad','sad') -> 0; ('leetcode','leeto') -> -1; ('mississippi','issip') -> 4; ('abc','') -> 0.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Naive substring search, a sliding window of the needle's length over the haystack. Linear-time matchers (KMP, Z, Rabin-Karp) are separate questions.

**Say this first (1 line):** "Try every start index; at each, compare the needle character by character; return the first full match. Worst case O(n*m); in practice `str.find` is what I would call."

**Brute force / naive:** That is the whole question. Two loops:
- `i` runs over `0 .. n-m` (later starts cannot fit the needle).
- `j` walks the needle while `h[i+j] == nd[j]`.
- If `j == m`, return `i`. Empty needle returns 0 up front.

**Optimal:** For the question as asked, the naive loop is the answer. In real code: `h.find(nd)`. To go below O(n*m) you use KMP or Z (O(n+m)) or Rabin-Karp (expected linear, worst case still O(n*m)); I would name them and say they get their own questions.

**Complexity:** Time O(n * m) worst case, O(n) best case (first character mismatches everywhere). Space O(1).
- Input that forces the worst case: haystack `'a' * n`, needle `'a' * (m-1) + 'b'`. Every start matches m-1 characters and then fails on the `b`. There are n-m+1 starts, so about (n-m+1)*m comparisons; the code counts it exactly.

**What `str.find` does (high level, no exact claims):** it is C code, not a Python loop. It is not the naive double loop: CPython uses a tuned search that skips ahead (in the Boyer-Moore-Horspool family for short needles, with a different guaranteed-linear method for long ones in recent versions). I would not quote the exact algorithm or its cut-offs, because they have changed between versions. The sandbox timing below shows the gap on the adversarial input, but it is a sandbox-only timing, not proof of big-O.

**Dry run:** `('mississippi', 'issip')`, n=11, m=5, starts 0..6.
| i | window | result |
|---|---|---|
| 0 | missi | 'm' != 'i' |
| 1 | issis | 'i','s','s','i' match, then 's' vs 'p' differ |
| 2 | ssiss | 's' != 'i' |
| 3 | sissi | 's' != 'i' |
| 4 | issip | all 5 match, return 4 |

**Code:**
```python
import random
import time


def str_str(h, nd):
    if nd == "":
        return 0
    n, m = len(h), len(nd)
    for i in range(n - m + 1):
        j = 0
        while j < m and h[i + j] == nd[j]:
            j += 1
        if j == m:
            return i
    return -1


def str_str_counted(h, nd):
    # same loop, but counts character comparisons so we can see the O(n*m) blow-up
    n, m, cmp_ = len(h), len(nd), 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            cmp_ += 1
            if h[i + j] != nd[j]:
                break
            j += 1
        if j == m:
            return i, cmp_
    return -1, cmp_


examples = [("sadbutsad", "sad", 0), ("leetcode", "leeto", -1),
            ("mississippi", "issip", 4), ("abc", "", 0)]
for h, nd, want in examples:
    assert str_str(h, nd) == h.find(nd) == want, (h, nd)
    print((h, nd), "->", want)

assert str_str("a", "a") == 0
assert str_str("a", "b") == -1
assert str_str("abc", "abcd") == -1        # needle longer than haystack
assert str_str("aaa", "aaaa") == -1
assert str_str("", "") == 0 and str_str("", "a") == -1
assert str_str("abcabd", "abd") == 3

# adversarial input: every window matches almost to the end, then fails on the last char
n, m = 10000, 5001
h, nd = "a" * n, "a" * (m - 1) + "b"
res, comps = str_str_counted(h, nd)
print("adversarial: result", res, "| comparisons", comps, "| (n-m+1)*m =", (n - m + 1) * m)
assert res == -1 and comps == (n - m + 1) * m

t = time.perf_counter(); r1 = h.find(nd); t_find = time.perf_counter() - t
t = time.perf_counter(); r2 = str_str(h, nd); t_naive = time.perf_counter() - t
assert r1 == r2 == -1
print("sandbox-only timing: str.find %.5f s, naive Python loop %.2f s" % (t_find, t_naive))

rng = random.Random(7)
cases = 0
for _ in range(5000):
    h = "".join(rng.choice("ab") for _ in range(rng.randint(0, 10)))
    nd = "".join(rng.choice("ab") for _ in range(rng.randint(0, 4)))
    assert str_str(h, nd) == h.find(nd), (h, nd)
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
('sadbutsad', 'sad') -> 0
('leetcode', 'leeto') -> -1
('mississippi', 'issip') -> 4
('abc', '') -> 0
adversarial: result -1 | comparisons 25005000 | (n-m+1)*m = 25005000
sandbox-only timing: str.find 0.00001 s, naive Python loop 1.11 s
random cross-check passed: 5000 cases
```
All four examples in the prompt are correct. The timing line varies run to run; only the comparison count is exact.

**Edge cases:**
- Empty needle: 0 (check before the loop; otherwise `range(n - m + 1)` still works, but say it).
- Needle longer than haystack: the `range` is empty, so -1.
- Both empty: 0.
- Overlapping partial matches (`'aaab'` in `'aaaab'`).

**Follow-ups:**
- *Can you do O(n+m)?* Yes: KMP never moves the haystack pointer back, using the prefix function (its own question).
- *Why stop at `n - m`?* A window starting later would run past the end.
- *All occurrences?* Keep searching from `i + 1` (overlapping) or `i + m` (non-overlapping).

**Common mistakes:**
- Off-by-one: `range(n - m)` misses the last window.
- Forgetting the empty needle case (the expected answer is 0).
- Slicing `h[i:i+m] == nd` and calling it O(1); the slice copies and compares m characters, so it is still O(m) per start.
- Saying "Python `find` is O(n)" without qualification.

### Q5 ⭐⭐⭐ 🟢 Rotate string check. Given strings `s` and `goal` (1 <= len <= 100), return True if `goal` can be obtained by moving some number of leading characters of `s` to its end (left rotations, zero allowed). Show the `goal in s + s` test, explain why the length check must come first, and why it is correct. Example: ('abcde','cdeab') -> True; ('abcde','abced') -> False; ('aa','a') -> False.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports

**Pattern:** Doubling the string to see every rotation as a substring.

**Say this first (1 line):** "Check the lengths match, then test `goal in s + s`. Every rotation of `s` is a length-n window inside `s + s`."

**Brute force:** Try all n left rotations `s[k:] + s[:k]` and compare each to `goal`. O(n^2) time (n rotations, each built and compared in O(n)). It is my checker.

**Optimal:**
- `len(s) == len(goal) and goal in s + s`.
- Why it is correct: `s + s` contains `s[k:] + s[:k]` starting at index k, for every k from 0 to n-1. So `goal` is a rotation exactly when it appears as a window of that doubled string.
- Why the length check first: without it, a shorter `goal` that is a substring of `s` would pass. `('aa', 'a')`: `'a'` is in `'aaaa'`, but `'a'` is not a rotation of `'aa'`. The code prints this bug on purpose.
- (If the length equals n, a match can start at index n as well, but that is just the rotation for k = 0 again, so nothing extra is accepted.)

**Complexity:** Time: building `s + s` is O(n); the `in` check is O(n*m) worst case with the naive method, and CPython's `in` uses its tuned search (same family as `str.find`). With a linear matcher such as KMP the whole test is O(n) guaranteed. At n <= 100 it does not matter. Space O(n) for the doubled string.

**Dry run:** `s = 'abcde'`, `goal = 'cdeab'`. `s + s = 'abcdeabcde'`. Lengths are both 5. `'cdeab'` appears at index 2. True.
`goal = 'abced'`: same length, but no window of `'abcdeabcde'` equals it. False.

**Code:**
```python
import random


def rotate_brute(s, goal):
    if len(s) != len(goal):
        return False
    return any(s[k:] + s[:k] == goal for k in range(len(s)))


def rotate_check(s, goal):
    return len(s) == len(goal) and goal in s + s


def rotate_check_no_length(s, goal):      # the bug: forgets the length check
    return goal in s + s


examples = [("abcde", "cdeab", True), ("abcde", "abced", False), ("aa", "a", False)]
for s, g, want in examples:
    assert rotate_check(s, g) == rotate_brute(s, g) == want, (s, g)
    print((s, g), "->", want)

print("without the length check, ('aa','a') ->", rotate_check_no_length("aa", "a"), "(wrong)")
assert rotate_check_no_length("aa", "a") is True
assert rotate_check("a", "a") is True
assert rotate_check("ab", "ba") is True
assert rotate_check("abc", "abc") is True          # zero rotation allowed
assert rotate_check("abc", "abca") is False
assert rotate_check("a" * 100, "a" * 100) is True
assert rotate_check("a" * 99 + "b", "b" + "a" * 99) is True
assert rotate_check("abab", "baba") is True

rng = random.Random(5)
cases = trues = 0
for _ in range(5000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
    if rng.random() < 0.5:
        k = rng.randint(0, len(s))
        g = s[k:] + s[:k]
        if rng.random() < 0.3:
            g = g[:-1] + rng.choice("ab")
    else:
        g = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
    want = rotate_brute(s, g)
    assert rotate_check(s, g) == want, (s, g)
    trues += want
    cases += 1
print("random cross-check passed:", cases, "cases,", trues, "of them True")
```

**Output (my run):**
```
('abcde', 'cdeab') -> True
('abcde', 'abced') -> False
('aa', 'a') -> False
without the length check, ('aa','a') -> True (wrong)
random cross-check passed: 5000 cases, 2267 of them True
```
All three examples in the prompt are correct.

**Edge cases:**
- Different lengths: False immediately.
- `goal == s` (zero rotations): True.
- Single character.
- All-equal strings and periodic strings (`'abab'`, `'baba'`): several shifts give the same result; still correct.

**Follow-ups:**
- *Also allow right rotations?* A right rotation by k is a left rotation by n-k, so the same test covers both.
- *How do you make it linear for big inputs?* Use KMP (or Z) for the `in` test.
- *Minimum number of rotations?* `(s + s).find(goal)` gives the smallest left-shift count when it is a rotation.

**Common mistakes:**
- Skipping the length check (shown above).
- Using `goal in s` and forgetting to double.
- Thinking `s + s` is needed for lengths of unequal strings; it is only valid once lengths match.

### Q6 ⭐⭐⭐ 🟢 String building and immutability in Python. Strings are immutable. Given a list `words`, return them joined by ', '. Show three versions: `out += w` in a loop, collecting pieces in a list and calling `', '.join(...)`, and `io.StringIO`. Explain why the first can degrade to O(n^2) copying in principle, what CPython's in-place concatenation optimisation does and why you must not rely on it (other interpreters, other references to the string, `out = w + out`), and what `join` does in one pass (sizes first, then copies once). Any timing you show is sandbox-only and not proof of big-O. Example: ['ab','cd','e'] -> 'ab, cd, e'; [] -> ''; ['x'] -> 'x'.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** String building and immutability. The question is about copy cost, not about an algorithm.

**Say this first (1 line):** "Strings are immutable, so every `+=` conceptually builds a new string and copies the old one. Collect pieces in a list and `join` once: it measures first, allocates once, copies once."

**Brute force:** `out += w` in a loop (add `', '` between words). In principle each step copies everything built so far, so the total copying is 1 + 2 + ... + n pieces, which is O(n^2) in the total length.

**Optimal:**
- `', '.join(words)`. One pass to add up the sizes, one allocation, one copy of each piece. O(total length).
- `io.StringIO`: `write` each piece, `getvalue()` at the end. Linear as well. It is useful when pieces come from many places or you build text through an API that expects a file object.
- The CPython special case: when `out += w` runs and `out` has only one reference, CPython can often resize the string in place instead of copying. That makes simple loops look linear. Do not rely on it:
  - It is an implementation detail of CPython, not a language guarantee. Other interpreters (PyPy and others) do not promise it.
  - It stops working if another variable still points at the same string (my "aliased" version below).
  - It does not apply to `out = w + out`, which always builds a new string; I include it as a case that stays quadratic.

**Complexity:** `join` and `StringIO`: O(total length) time, O(total length) space for the result. `+=` is quadratic in principle, linear in practice only when CPython's optimisation applies. `w + out` is quadratic.

**Dry run:** `['ab','cd','e']`.
| approach | what happens |
|---|---|
| `+=` | 'ab' -> 'ab, ' -> 'ab, cd' -> 'ab, cd, ' -> 'ab, cd, e' (each step may copy the previous string) |
| `join` | sizes 2+2+1 plus 2 separators of 2 = 9; allocate 9 once; copy the three words and two separators |
| `StringIO` | write 'ab', ', ', 'cd', ', ', 'e'; `getvalue()` returns 'ab, cd, e' |

**Code:**
```python
import io
import sys
import time


def join_plus(words):
    out = ""
    for i, w in enumerate(words):
        if i:
            out += ", "
        out += w
    return out


def join_list(words):
    return ", ".join(words)


def join_stringio(words):
    buf = io.StringIO()
    for i, w in enumerate(words):
        if i:
            buf.write(", ")
        buf.write(w)
    return buf.getvalue()


def join_prepend(words):                 # out = w + out : never gets the in-place trick
    out = ""
    for w in reversed(words):
        out = w + (", " + out if out else "")
    return out


def join_plus_aliased(words):            # a second reference to the string defeats the trick
    out = ""
    for i, w in enumerate(words):
        if i:
            out += ", "
        out += w
        keep = out                       # second reference to the same str object
    return out


for words, want in [(["ab", "cd", "e"], "ab, cd, e"), ([], ""), (["x"], "x")]:
    for f in (join_plus, join_list, join_stringio, join_prepend, join_plus_aliased):
        assert f(words) == want, (f.__name__, words)
    print(words, "->", repr(want))

assert join_list(["", ""]) == ", "
assert join_plus(["", "a"]) == ", a"

print("python", sys.version.split()[0], sys.implementation.name)
print("sandbox-only timings (seconds), not proof of big-O:")
print("%8s %10s %10s %10s %10s %12s" % ("n", "+=", "join", "StringIO", "w+out", "+= aliased"))
for n in (10000, 20000, 40000, 80000):
    words = ["word%d" % i for i in range(n)]
    row = []
    for f in (join_plus, join_list, join_stringio, join_prepend, join_plus_aliased):
        t = time.perf_counter()
        r = f(words)
        row.append(time.perf_counter() - t)
        assert r == ", ".join(words)
    print("%8d %10.4f %10.4f %10.4f %10.4f %12.4f" % (n, *row))
```

**Output (my run):**
```
['ab', 'cd', 'e'] -> 'ab, cd, e'
[] -> ''
['x'] -> 'x'
python 3.13.17 cpython
sandbox-only timings (seconds), not proof of big-O:
       n         +=       join   StringIO      w+out   += aliased
   10000     0.0007     0.0000     0.0007     0.0268       0.0124
   20000     0.0017     0.0002     0.0014     0.0980       0.0492
   40000     0.0034     0.0004     0.0025     0.4498       0.1967
   80000     0.0065     0.0006     0.0052     3.0800       1.1294
```
How to read the timings: they are sandbox-only numbers and vary every run, so they are not proof of big-O. Observed on CPython 3.13 here: plain `+=` stayed fast, because the in-place optimisation applied. The `w + out` and the aliased version got about four times slower each time n doubled, which is the quadratic shape. `join` was fastest. All five versions returned identical strings, so the asserts passed. The prompt's three examples are correct.

**Edge cases:**
- Empty list: `''` (and `join([])` is `''`, no special case).
- One word: no separator.
- Empty strings in the list: `['', '']` gives `', '`.
- Non-string items: `join` raises `TypeError`; convert with `map(str, ...)` first.

**Follow-ups:**
- *Is `+=` on a list the same problem?* No. `list.append` is amortised O(1); lists are mutable.
- *Do f-strings or `%` help in a loop?* No, they build a new string each time too; use them for one-off formatting.
- *`bytearray`?* Mutable, amortised appends; good for binary data.

**Common mistakes:**
- Saying "`+=` is always O(n^2) in Python". On CPython it often is not, and claiming otherwise is easy to challenge.
- Saying "`+=` is fine, CPython optimises it" and relying on that for code that may run elsewhere or hold another reference.
- Building with `''.join` on a generator inside the hot loop repeatedly instead of once at the end.
- Presenting a timing as proof of complexity.

### Q7 ⭐⭐⭐ 🟡 String to integer (atoi). Implement `my_atoi(s)` for a string of up to 200 characters: skip leading spaces only, read an optional '+' or '-', read consecutive digits and stop at the first non-digit, return 0 if there are no digits, and clamp the result to the 32-bit signed range [-2^31, 2^31 - 1]. Do it in one left-to-right parse with an explicit state or pointer (no regex, no `int()` on the whole string) and show where you clamp so a Python big int never grows unbounded. Example: '42' -> 42; '   -042' -> -42; '1337c0d3' -> 1337; 'words and 987' -> 0; '-91283472332' -> -2147483648; '+-12' -> 0.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** One-pass parser with a pointer and early clamping. It is a tiny state machine: spaces, sign, digits, stop.

**Say this first (1 line):** "Skip spaces, read one optional sign, then accumulate digits; stop at the first non-digit; clamp as soon as the value passes the limit so the number never grows."

**Brute force:** Regex `^ *([+-]?[0-9]+)` plus `int()` on the match, then clamp. It is short and correct, and I use it as the checker. The question forbids it, because the point is to show the parse.

**Optimal:**
- States in order: leading spaces (only the space character), optional sign (one only), digits.
- `limit = 2**31` for a negative, `2**31 - 1` for a positive. After each digit `res = res*10 + d`; if `res > limit`, return the clamp value (`-2**31` or `2**31 - 1`) right away.
- So `res` never exceeds about 10 * 2^31, tiny for Python's big ints. Python has no overflow, so the clamp is for the answer, not for safety; we still stop early to avoid pointless work on a 200-digit string.
- Test digits with `'0' <= c <= '9'`, not `c.isdigit()`: `isdigit()` accepts characters like Arabic-Indic digits and superscripts (the code shows `'٣'`), and `int()` accepts some of those too.
- Leading zeros do not trigger the clamp because `res` stays 0.

**Complexity:** Time O(n), one pass. Space O(1).

**Dry run:** `s = '   -042'`
| step | pointer | state | res |
|---|---|---|---|
| spaces | 0..2 | skipped | 0 |
| sign | 3 '-' | sign = -1, limit 2^31 | 0 |
| digit '0' | 4 | | 0 |
| digit '4' | 5 | | 4 |
| digit '2' | 6 | | 42 |
| end | | return -1 * 42 | -42 |

`'+-12'`: sign '+' read, next char is '-', not a digit, so no digits: return 0.

**Code:**
```python
import random
import re

INT_MAX, INT_MIN = 2**31 - 1, -2**31


def my_atoi(s):
    i, n = 0, len(s)
    while i < n and s[i] == " ":          # skip leading spaces only (not tabs)
        i += 1
    sign = 1
    if i < n and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        i += 1
    limit = 2**31 if sign == -1 else 2**31 - 1
    res = 0
    while i < n and "0" <= s[i] <= "9":   # not str.isdigit(): that accepts other scripts
        res = res * 10 + (ord(s[i]) - 48)
        if res > limit:                   # clamp now; res never exceeds ~2^31 * 10
            return INT_MIN if sign == -1 else INT_MAX
        i += 1
    return sign * res


def atoi_regex(s):                        # oracle only: regex + int() on the matched part
    m = re.match(r" *([+-]?[0-9]+)", s)
    if not m:
        return 0
    return max(INT_MIN, min(INT_MAX, int(m.group(1))))


examples = [("42", 42), ("   -042", -42), ("1337c0d3", 1337), ("words and 987", 0),
            ("-91283472332", -2147483648), ("+-12", 0)]
for s, want in examples:
    assert my_atoi(s) == atoi_regex(s) == want, (s, my_atoi(s), want)
    print(repr(s), "->", my_atoi(s))

assert my_atoi("") == 0 and my_atoi("   ") == 0
assert my_atoi("-") == 0 and my_atoi("+") == 0
assert my_atoi("2147483647") == INT_MAX
assert my_atoi("2147483648") == INT_MAX
assert my_atoi("-2147483648") == INT_MIN
assert my_atoi("-2147483649") == INT_MIN
assert my_atoi("0" * 50 + "12") == 12                  # leading zeros never trigger the clamp
assert my_atoi("9" * 200) == INT_MAX
assert my_atoi("\t1") == 0                            # tab is not a skipped space
assert my_atoi("  +0 12") == 0
assert my_atoi("3.14") == 3
assert my_atoi("٣") == 0                         # Arabic-Indic digit three: not a digit here
assert "٣".isdigit() and int("٣") == 3      # but isdigit()/int() would accept it

rng = random.Random(9)
cases = 0
for _ in range(5000):
    parts = [" " * rng.randint(0, 2), rng.choice(["", "+", "-", "+-", "-+"]),
             "".join(rng.choice("0123456789") for _ in range(rng.randint(0, 12))),
             rng.choice(["", "x", " 5", ".5", "e3"])]
    s = "".join(parts)
    assert my_atoi(s) == atoi_regex(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'42' -> 42
'   -042' -> -42
'1337c0d3' -> 1337
'words and 987' -> 0
'-91283472332' -> -2147483648
'+-12' -> 0
random cross-check passed: 5000 cases
```
All six examples in the prompt are correct.

**Edge cases:**
- Empty, spaces only, or a lone sign: 0.
- Exactly `2147483648`: clamps to 2147483647. `-2147483648` is allowed exactly; `-2147483649` clamps to -2147483648.
- Tab or newline first (`'\t1'`): only the space character is skipped, so 0.
- Text after the number (`'3.14'`, `'1337c0d3'`): ignored.
- Two signs (`'+-12'`): 0.
- Very long digit strings: early clamp.

**Follow-ups:**
- *In C or Java with real 32-bit ints?* Check before multiplying: `res > INT_MAX // 10` or `res == INT_MAX // 10 and d > 7`.
- *Allow `1e3`, `.5`?* That is the valid-number state machine; different question.
- *Why not `int(s.strip())`?* It raises on `'12abc'`, accepts underscores (`'1_0'`) and non-ASCII digits, and cannot do the partial parse.

**Common mistakes:**
- Using `lstrip()` or `split()` which skip tabs and newlines too.
- Accepting a second sign.
- Using `isdigit()`.
- Clamping only after the loop with a giant intermediate.
- Treating `-0` or `+0` incorrectly; both give 0 here, which is right.

### Q8 ⭐⭐⭐ 🟡 Longest palindromic substring. Given a string `s` (1 <= len <= 1000, letters and digits), return the longest substring that reads the same in both directions; on ties return the leftmost. Give the O(n^3) brute force, then expand-around-center in O(n^2) time and O(1) space that handles both odd and even centers, and say in one line that Manacher's algorithm does this in O(n) (a separate question). Palindrome partitioning is a backtracking topic (Part 12) and only mentioned here. Example: 'babad' -> 'bab'; 'cbbd' -> 'bb'; 'a' -> 'a'; 'abacdfgdcaba' -> 'aba'.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Expand around centre. A palindrome mirrors around its middle, so for each possible middle, grow outwards while the two ends match.

**Say this first (1 line):** "There are 2n-1 centres, n single characters for odd lengths and n-1 gaps for even ones. For each, expand while the ends match, keep the longest. O(n^2) time, O(1) space. Manacher gets O(n)."

**Brute force:** Check every substring: O(n^2) substrings times an O(n) palindrome test = O(n^3). On ties, keep the first one found, which is the leftmost if you only replace on a strictly longer result.

**Optimal:**
- For each `c` in `0..n-1`, expand twice: `(c, c)` for odd length, `(c, c+1)` for even length.
- `expand(l, r)`: while `l >= 0`, `r < n` and `s[l] == s[r]`, step `l -= 1`, `r += 1`. The palindrome is `s[l+1:r]`, length `r - l - 1`.
- Replace the best only when strictly longer. Centres are visited left to right, and for equal lengths a later centre means a later start, so strict `>` keeps the leftmost.
- Invariant: when the loop stops, `s[l+1:r]` is the largest palindrome around that centre; the stop condition is an out-of-range index or a mismatch.
- Manacher's algorithm (separate question) reuses mirror information of earlier palindromes to get O(n). Palindrome partitioning is a backtracking topic (Part 12), only mentioned here.

**Complexity:** Time O(n^2) worst case (for example `'aaaa...'`: each centre expands to the edge). Space O(1) besides the answer slice. The brute force is O(n^3).

**Dry run:** `s = 'babad'`
| centre | odd expansion | even expansion | best |
|---|---|---|---|
| 0 | 'b' | 'b' vs 'a' no | 'b' |
| 1 | 'a', then 'b'=='b' gives 'bab' | 'a' vs 'b' no | 'bab' (3) |
| 2 | 'b', then 'a' vs 'a' gives 'aba' (3, not longer) | 'b' vs 'a' no | still 'bab' |
| 3, 4 | length 1 | none | 'bab' |

Answer 'bab'. 'aba' is also valid, but the leftmost wins.

**Code:**
```python
import random


def lps_brute(s):
    best = ""
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            t = s[i:j]
            if len(t) > len(best) and t == t[::-1]:      # strict > keeps the leftmost
                best = t
    return best


def lps_expand(s):
    start, best = 0, 1

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - l - 1                          # start, length

    for c in range(len(s)):
        for l, r in ((c, c), (c, c + 1)):                # odd centre, even centre
            st, ln = expand(l, r)
            if ln > best:                                # strict: ties keep the leftmost
                start, best = st, ln
    return s[start:start + best]


examples = [("babad", "bab"), ("cbbd", "bb"), ("a", "a"), ("abacdfgdcaba", "aba")]
for s, want in examples:
    assert lps_expand(s) == lps_brute(s) == want, (s, lps_expand(s), want)
    print(repr(s), "->", repr(want))

assert lps_expand("ab") == "a"
assert lps_expand("aa") == "aa"
assert lps_expand("aaaa") == "aaaa"
assert lps_expand("abcd") == "a"
assert lps_expand("racecar") == "racecar"
assert lps_expand("xabbay") == "abba"
assert lps_expand("z" * 1000) == "z" * 1000
s = "ab" * 500
assert lps_expand(s) == "ab" * 499 + "a"             # len 999, starts at 0

rng = random.Random(21)
cases = 0
for _ in range(4000):
    s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 12)))
    assert lps_expand(s) == lps_brute(s), s
    cases += 1
for _ in range(2000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 14)))
    assert lps_expand(s) == lps_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'babad' -> 'bab'
'cbbd' -> 'bb'
'a' -> 'a'
'abacdfgdcaba' -> 'aba'
random cross-check passed: 6000 cases
```
All four examples in the prompt are correct.

**Edge cases:**
- Single character.
- No repeats (`'abcd'`): the answer is the first character.
- Even-length palindrome (`'cbbd'`, `'aa'`): needs the even centres.
- All-equal string: the whole string; this is also the O(n^2) worst case.
- Tie between two palindromes of equal length: leftmost.

**Follow-ups:**
- *Can you do O(n)?* Manacher: transform with separators, keep the rightmost palindrome's centre and edge, and reuse the mirror's radius. Each character is expanded at most once on the right.
- *Why not DP?* An n-by-n table works in O(n^2) time but uses O(n^2) space; expansion has the same time with O(1) space.
- *Return only the length?* Same loop, track the length.

**Common mistakes:**
- Only odd centres, which fails on `'cbbd'`.
- Replacing on `>=`, which returns the rightmost on ties.
- Off-by-one when slicing: the result is `s[l+1:r]`, not `s[l:r]`.
- Reversing the string and finding the longest common substring without checking the positions match (that is a known bug for strings like `'abacdfgdcaba'`).

### Q9 ⭐⭐⭐ 🟡 Count palindromic substrings. Given `s` (1 <= len <= 1000), count the substrings (by position, so equal text at different positions counts separately) that are palindromes. Reuse expand-around-center for the 2n-1 centers and explain why the count of expansions that succeed is the answer. The single-string palindrome check itself is Part 2 Q1 and the delete-one variant Part 2 Q20; do not redo them. Example: 'abc' -> 3; 'aaa' -> 6; 'abba' -> 6.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports

**Pattern:** Same expand-around-centre as the longest palindromic substring, but count instead of keep the best.

**Say this first (1 line):** "For each of the 2n-1 centres, expand while the ends match; every successful expansion step is one new palindrome, so add one per step."

**Brute force:** For every pair `(i, j)`, slice and compare with its reverse. O(n^2) substrings times O(n) check = O(n^3). It is my checker.

**Optimal:**
- For each centre (single character `c`, or the gap between `c` and `c+1`), set `l, r` and loop `while l >= 0 and r < n and s[l] == s[r]`: do `total += 1`, then step outward.
- Why the count is right: a palindrome is fixed by its centre and its radius. If the radius-k palindrome around a centre exists, then so do all smaller radii (peel off the matching ends). So the number of successful steps for a centre is exactly the number of palindromes with that centre. Different centres give different substrings (by position), so nothing is double-counted. Equal text at different positions is counted separately, as the question wants.
- (The last even centre, between index n-1 and n, fails at once because `r < n` is false. Code can run `c` to `n-1` for both kinds.)
- The single-string palindrome check is Part 2 Q1 and the delete-one variant Part 2 Q20; not repeated here.

**Complexity:** Time O(n^2) worst case; all-equal strings hit it. Space O(1). The answer itself can be as large as n(n+1)/2, about 500,500 for n = 1000, which a Python int holds easily.

**Dry run:** `s = 'aaa'`
| centre | steps that succeed | count |
|---|---|---|
| 0 odd | 'a' | 1 |
| 0 even (0,1) | 'aa' (then l=-1 stops) | 1 |
| 1 odd | 'a', 'aaa' | 2 |
| 1 even (1,2) | 'aa' | 1 |
| 2 odd | 'a' | 1 |
| 2 even | none | 0 |
Total 6: three 'a', two 'aa', one 'aaa'.

**Code:**
```python
import random


def count_brute(s):
    n = len(s)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1)
               if s[i:j] == s[i:j][::-1])


def count_expand(s):
    n, total = len(s), 0
    for c in range(n):
        for l, r in ((c, c), (c, c + 1)):          # 2n-1 useful centres (last even one is empty)
            while l >= 0 and r < n and s[l] == s[r]:
                total += 1                         # every successful step is one new palindrome
                l -= 1
                r += 1
    return total


examples = [("abc", 3), ("aaa", 6), ("abba", 6)]
for s, want in examples:
    assert count_expand(s) == count_brute(s) == want, (s, count_expand(s), want)
    print(repr(s), "->", want)

assert count_expand("a") == 1
assert count_expand("ab") == 2
n = 1000
assert count_expand("a" * n) == n * (n + 1) // 2      # all equal: every substring counts
print("'a'*1000 ->", count_expand("a" * n), "= n(n+1)/2")
assert count_expand("ab" * 500) == count_brute("ab" * 500)       # max size, two ways agree

rng = random.Random(4)
cases = 0
for _ in range(5000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 12)))
    assert count_expand(s) == count_brute(s), s
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
'abc' -> 3
'aaa' -> 6
'abba' -> 6
'a'*1000 -> 500500 = n(n+1)/2
random cross-check passed: 5000 cases
```
All three examples in the prompt are correct.

**Edge cases:**
- Single character: 1.
- No repeats: n (only single characters).
- All equal: n(n+1)/2.
- Even-length palindromes such as `'abba'` need even centres (answer 6: four singles, 'bb', 'abba').

**Follow-ups:**
- *Distinct palindromic substrings instead?* Need a set (or a palindromic tree / eertree); counting by position is not enough.
- *Faster than O(n^2)?* Manacher's radii array gives the count in O(n): sum of radii.
- *DP version?* `dp[i][j]` true if `s[i] == s[j]` and `dp[i+1][j-1]`; O(n^2) time and space.

**Common mistakes:**
- Counting only the longest palindrome per centre.
- Forgetting the even centres.
- Adding 1 after the loop instead of inside it.
- Deduplicating equal substrings when the question counts by position.

### Q10 ⭐⭐⭐ 🟡 String compression in place. `chars` is a list of single characters. Compress it in place, using O(1) extra space: for each maximal run of the same character write the character, then, if the run length is above 1, write its decimal digits as separate characters (12 becomes '1','2'). Return the new length k; the first k slots must hold the result. Use a read pointer and a write pointer and say why the write pointer never overtakes the read pointer. Example: ['a','a','b','b','c','c','c'] -> k=6, prefix ['a','2','b','2','c','3']; ['a'] -> k=1, prefix ['a']; ['a','b','b','b','b','b','b','b','b','b','b','b','b'] -> k=4, prefix ['a','b','1','2'].
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)

**Pattern:** Read and write pointers over the same list (in-place, run-length compression).

**Say this first (1 line):** "Read pointer finds the end of each run; write pointer writes the character, then the digits of the run length if it is above 1. Return the write position."

**Brute force:** Build a new list with `itertools.groupby`: append the character, and the digits of the count when the count is above 1. O(n) time, O(n) space. It is my checker. The question wants O(1) extra space.

**Optimal:**
- `write = read = 0`. While `read < n`: remember `ch = chars[read]` and `start = read`, then advance `read` past the whole run.
- Write `ch` at `write`, then `write += 1`. If `read - start > 1`, write each character of `str(read - start)`.
- `write` never overtakes `read`: a run of length L has already been fully read when we write, so `read` has advanced L positions past `start`, and we write at most `1 + digits(L)` characters. For L = 1 that is 1, for L >= 2 it is `1 + digits(L) <= L` (L = 2 gives 2, L = 10 gives 3, L = 100 gives 4). So the output for a run never exceeds the input it came from, and the next run's write starts at or before where it starts being read. The code asserts this.
- `str(L)` makes a short temporary string, one character per digit of L (about log10 n characters). That is tiny and bounded for any realistic list, so I count it as O(1) extra space (strictly it is O(log n) bits-worth of digits).

**Complexity:** Time O(n): `read` only moves forward and each character is written at most once. Space O(1) (digits string of at most a few characters).

**Dry run:** `['a']` followed by twelve `'b'`.
| step | read after run | run | writes | write |
|---|---|---|---|---|
| 1 | 1 | 'a' x1 | 'a' | 1 |
| 2 | 13 | 'b' x12 | 'b', '1', '2' | 4 |
Return 4; prefix `['a','b','1','2']`.

**Code:**
```python
import random
from itertools import groupby


def compress_brute(chars):
    out = []
    for ch, grp in groupby(chars):
        k = len(list(grp))
        out.append(ch)
        if k > 1:
            out.extend(str(k))
    return out


def compress_inplace(chars):
    n = len(chars)
    write = read = 0
    while read < n:
        ch = chars[read]
        start = read
        while read < n and chars[read] == ch:      # read pointer jumps to the end of the run
            read += 1
        chars[write] = ch
        write += 1
        if read - start > 1:
            for d in str(read - start):            # digits of the run length, as characters
                chars[write] = d
                write += 1
        assert write <= read                       # the invariant, checked at run time
    return write


def run(chars):
    c = list(chars)
    k = compress_inplace(c)
    return k, c[:k]


examples = [(list("aabbccc"), 6, list("a2b2c3")), (["a"], 1, ["a"]),
            (list("a" + "b" * 12), 4, list("ab12"))]
for chars, wk, wp in examples:
    k, pre = run(chars)
    assert (k, pre) == (wk, wp) == (len(compress_brute(chars)), compress_brute(chars)), (chars, k, pre)
    print("k =", k, "prefix", pre)

assert run([]) == (0, [])
assert run(list("abc")) == (3, list("abc"))            # all runs of length 1: no digits
assert run(list("a" * 9)) == (2, list("a9"))
assert run(list("a" * 10)) == (3, list("a10"))
assert run(list("a" * 100)) == (4, list("a100"))
assert run(list("a" * 2000)) == (5, list("a2000"))
assert run(list("aab")) == (3, list("a2b"))
assert run(list("abba")) == (4, list("ab2a"))          # non-adjacent same letters stay separate

rng = random.Random(8)
cases = 0
for _ in range(4000):
    chars = []
    for _ in range(rng.randint(0, 6)):
        chars += [rng.choice("abc")] * rng.choice([1, 1, 2, 3, 9, 10, 11, 25])
    k, pre = run(chars)
    assert pre == compress_brute(chars) and k == len(pre), chars
    cases += 1
print("random cross-check passed:", cases, "cases")
```

**Output (my run):**
```
k = 6 prefix ['a', '2', 'b', '2', 'c', '3']
k = 1 prefix ['a']
k = 4 prefix ['a', 'b', '1', '2']
random cross-check passed: 4000 cases
```
All three examples in the prompt are correct.

**Edge cases:**
- Single character: k = 1, no digit.
- All runs of length 1 (`'abc'`): unchanged, k = n.
- Run length 10 or more: multiple digit characters, written left to right (12 becomes '1','2', never '12' as one item).
- One long run (2000 characters): five characters out.
- Same letter in two separate runs (`'abba'`): not merged, `a b 2 a`.
- Empty list: 0 (the prompt promises at least one; harmless).

**Follow-ups:**
- *Decompress in place?* Harder: the output can be longer than the input, so work from the end or use extra space.
- *Why not compress when it makes the string longer?* This question says always write the count above 1; length 2 gives the same size, so it never grows.
- *Why use a list of characters?* Python strings are immutable (Q6), so in-place work is only possible on a mutable sequence.

**Common mistakes:**
- Writing the count even for a run of length 1.
- Writing `'12'` into one slot instead of two digit characters.
- Updating the read pointer inside the write loop by mistake.
- Returning the compressed list instead of the length (the first k slots are the contract; the tail is garbage and is not checked).
