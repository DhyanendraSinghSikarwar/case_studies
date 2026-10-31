# Book 5 — Part 3: Strings

**Topic:** Python DSA for product-company interviews: palindromes (longest palindromic substring and counting by expand-around-center, shortest palindrome, Manacher at concept level, rearrangement counting), string building and immutability (join versus +=, StringIO), parsing and tokenising in one left-to-right pass (atoi, valid number, version comparison, basic calculator without a stack design), reverse words and in-place character-list work, run-length compression, encode and decode with escaping, longest common prefix, numeric-string arithmetic (add, add binary, multiply) and Roman numerals both ways, zigzag, pattern matching (naive search, KMP prefix function, Z-function, Rabin-Karp with collision handling, longest happy prefix, longest repeated substring with rolling hash plus binary search), repeated-substring and rotation problems (rotated string, lexicographically smallest rotation), Unicode versus bytes versus code points versus graphemes, normalisation and case-folding with unicodedata, UTF-8 validation, regex versus manual matching and catastrophic backtracking, wildcard matching, and edit distance, LCS and tries at concept level only

**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 13, ⭐⭐ 15, ⭐ 12)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns string algorithms and string-specific Python behaviour (palindromic substrings, parsing, numeric strings, pattern matching, Unicode). Part 1 already owns hashing and anagram grouping, valid anagram, isomorphic strings and word pattern, ransom note and the length-prefix list codec (cross-referenced here only as 'Part 1 Q3, Q24', each checked against its heading; isomorphic and word-pattern problems are not repeated). Part 2 owns sliding-window string problems (longest substring without repeats, minimum window substring, permutation in string, anagram start positions, character replacement) and the two-pointer valid palindrome and valid palindrome II (cross-referenced only as 'Part 2 Q1, Q20', checked against headings); none of those is repeated. Part 4 owns stacks and queues (the calculator question here is a single-pass parse with no stack design); Part 11 owns edit distance, LCS and regex matching as DP (concept level only here, with memoised recursion on tiny inputs); Part 12 owns backtracking (palindrome partitioning), tries and bit manipulation (the prefix-query question here is a sorted-list plus bisect answer with the trie described only); Part 13 owns number theory and sorting internals. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force or reference code (scratch/B5P03_wavea/check_examples.py, python3 -I) before freezing; one example was found wrong during that run (a ligature does not separate casefold from compatibility normalisation because casefold already expands it) and was replaced. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part03_sources.md). Searches for TCS, Infosys and Amazon string rounds returned generic aggregator and candidate-reported pages, and nothing for Google, so 'Asked at' tags name source types (public pattern lists, community roundups, Indian placement-style prep, pattern-matching tutorials, Unicode docs and tutorials, editor knowledge of standard lists), not verified company reports; company tags on community pages are unverified. The Unicode searches did not return the official Python docs, so the casefold and grapheme claims rest on editor knowledge and on the sandbox run. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

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

### Q31 ⭐ 🟡 Reverse text without breaking combining marks. Write `reverse_text(s)` that reverses a string by 'user characters' approximated as a base character plus all following combining marks (use `unicodedata.combining(c) != 0` to detect marks), so accents stay on the letter they belong to. Show what plain `s[::-1]` does to a decomposed accent, and state clearly what this approximation still gets wrong (emoji sequences, regional-indicator flags, Hangul jamo) and what a real grapheme segmenter adds. Example: reverse_text('cafe\u0301') -> 'e\u0301fac'; 'e\u0301x'[::-1] -> 'x\u0301e' (the accent now sits on x).
**Asked at:** Unicode and Python text-handling docs and tutorials (pandas and xarray str.normalize pages and the pyunormalize project surfaced by search; snippets only, the official Python unicodedata and str docs were not opened, so claims about casefold and grapheme clusters rest on editor knowledge and the sandbox run) | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Group first, then reverse the groups. A "user character" here is one base character plus the combining marks after it. The loop works on clusters, not on code points.

**Say this first (1 line):** "A Python str is a sequence of code points, so `[::-1]` can detach an accent from its letter. I reverse clusters instead: a base plus the marks that follow it."

**Brute force:** Walk left to right. If the character has `unicodedata.combining(c) != 0`, append it to the last cluster. Otherwise start a new cluster. Reverse the cluster list and join. O(n) time, O(n) space. This is my checker.

**Optimal:** One right-to-left scan with no intermediate list of clusters.
- Start at the end, `i`. Walk `j` left while `s[j]` is a combining mark.
- Stop at the base character (or at index 0). The slice `s[j:i+1]` is one cluster, in its original internal order.
- Append that slice to the output, set `i = j - 1`, repeat.
- Invariant: everything right of `i` is already emitted, in reverse cluster order, and no cluster is cut in half.
- Do not reverse the marks inside a cluster. Marks apply in order, so `a + acute + circumflex` must stay in that order.

**Complexity:** Time O(n): each index is visited once by `j` and once as part of a slice. Space O(n) for the output (strings are immutable, so we need a new one anyway). Slices are copied, but their total length is n.

**Dry run:** `s = 'café'` is five code points: c, a, f, e, U+0301.
| i | j walk | cluster emitted | out so far |
|---|---|---|---|
| 4 | s[4] is a mark, j=3, s[3]='e' is not | `é` | `é` |
| 2 | s[2]='f' | `f` | `éf` |
| 1 | s[1]='a' | `a` | `éfa` |
| 0 | s[0]='c' | `c` | `éfac` |

Plain `s[::-1]` gives `́efac`: the mark is now first, so it attaches to whatever came before it (or nothing).

**Code:**
```python
import random
import sys
import unicodedata


def reverse_text_brute(s):
    """Reference: split into clusters (base + following marks) with a list, reverse cluster order."""
    clusters = []
    for ch in s:
        if unicodedata.combining(ch) != 0 and clusters:
            clusters[-1] += ch
        else:
            clusters.append(ch)
    return "".join(reversed(clusters))


def reverse_text(s):
    """One right-to-left scan: collect trailing marks, then emit base + marks."""
    out = []
    i = len(s) - 1
    while i >= 0:
        j = i
        while j > 0 and unicodedata.combining(s[j]) != 0:   # walk left over marks
            j -= 1
        out.append(s[j:i + 1])      # base char (s[j]) followed by its marks
        i = j - 1
    return "".join(out)


s = "café"
print(sys.version.split()[0], "unidata", unicodedata.unidata_version)
print(len(s), ascii(s), "->", ascii(reverse_text(s)))
print("plain slice:", ascii("éx"[::-1]))
print("fixed      :", ascii(reverse_text("éx")))
assert reverse_text("café") == "éfac"
assert "éx"[::-1] == "x́e"
assert reverse_text("éx") == "xé"

# where the approximation still fails
flag = "\U0001F1EE\U0001F1F3"                       # regional indicators I + N = India flag
print("flag len", len(flag), "reversed", ascii(reverse_text("a" + flag)))
fam = "\U0001F468‍\U0001F469‍\U0001F467"  # man ZWJ woman ZWJ girl
print("family len", len(fam), "combining on ZWJ:", unicodedata.combining("‍"))
print("jamo combining:", unicodedata.combining("ᄒ"), unicodedata.combining("ᅡ"))
print("NFC recomposes:", ascii(unicodedata.normalize("NFC", "é")), len(unicodedata.normalize("NFC", "é")))
print("stacked marks:", ascii(reverse_text("á̂b")))

# edge cases
assert reverse_text("") == ""
assert reverse_text("a") == "a"
assert reverse_text("́") == "́"            # lone mark has no base
assert reverse_text("́a") == "á"          # leading orphan mark stays its own cluster
assert reverse_text("abc") == "abc"[::-1]
assert reverse_text("á̂b") == "bá̂"   # stacked marks keep order
assert reverse_text("́̂") == "́̂"       # only marks

rng = random.Random(31)
alphabet = ["a", "b", "e", "x", "́", "̂", "̈", "z"]
for _ in range(3000):
    t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 9)))
    got = reverse_text(t)
    assert got == reverse_text_brute(t), ascii(t)
    assert len(got) == len(t)
    assert sorted(got) == sorted(t)
print("random cross-check passed: 3000 cases")
```

**Output (my run):**
```text
3.13.17 unidata 15.1.0
5 'cafe\u0301' -> 'e\u0301fac'
plain slice: 'x\u0301e'
fixed      : 'xe\u0301'
flag len 2 reversed '\U0001f1f3\U0001f1eea'
family len 5 combining on ZWJ: 0
jamo combining: 0 0
NFC recomposes: '\xe9' 1
stacked marks: 'ba\u0301\u0302'
random cross-check passed: 3000 cases
```
Both prompt examples are correct. Observed on Python 3.13.17, which reports Unicode database 15.1.0 (`unicodedata.unidata_version`); `unicodedata.combining` answers from that version.

**What the approximation still gets wrong (all shown above):**
- Regional-indicator flags: the India flag is two code points (I, N). Reversing them gives N, I, which is another country's flag. Cluster size is 2 but neither is a combining mark.
- Emoji ZWJ sequences: the family emoji is 5 code points joined by U+200D. `combining('‍')` is 0, so each piece becomes its own cluster and the family comes apart in reverse order.
- Hangul jamo: a syllable written as separate conjoining jamo (leading, vowel, trailing) has `combining` 0 for each, so the syllable gets split. NFC would usually compose it first.
- Orphan marks: a leading mark has no base. After reversal it lands on the previous cluster's letter, silently attaching to a new base.
- Also: emoji skin-tone modifiers, variation selectors (those two are not "combining" by this test either).

**What a real grapheme segmenter adds:** The Unicode text-segmentation rules (UAX #29, "extended grapheme clusters") use a per-character property table: Extend, ZWJ, SpacingMark, Prepend, Regional_Indicator, Hangul L/V/T and Extended_Pictographic. They also keep regional indicators in pairs. The standard library has no such segmenter in Python 3.13 (I did not find one in `unicodedata`). In practice you use the third-party `regex` module's `\X` or the `grapheme` package. I did not install either here.

**Edge cases:**
- Empty string, one character.
- A lone mark, or only marks: returned as is.
- Stacked marks (`a`, acute, circumflex): the order inside the cluster must not flip.
- Precomposed `é` has no mark, so plain reversal already works. `unicodedata.normalize('NFC', ...)` first removes many (not all) of these cases.
- Equality trap: `'é' == 'é'` is False; they only match after normalisation.

**Follow-ups:**
- *Does NFC fix this?* Often. `normalize('NFC', 'é')` is one code point, `\xe9`, so `[::-1]` is safe for it. It cannot compose a letter and mark that have no precomposed form, and it never fixes flags or ZWJ emoji.
- *What does `len` count?* Code points, not user-perceived characters. `len('café')` is 5, a reader sees 4.
- *Why not reverse bytes?* Reversing UTF-8 bytes corrupts every multi-byte character. Not an option.

**Common mistakes:**
- Reversing the marks inside a cluster along with the clusters.
- Assuming "combining mark" equals "grapheme cluster". It is only an approximation.
- Treating a lone leading mark as having a base to its left.
- Claiming `len(s)` is the number of visible characters.

---

### Q32 ⭐ 🟡 Validate UTF-8 at the byte level. Given a list `data` of integers (each 0..255, len <= 2*10^4) representing bytes, return True if it forms a structurally valid UTF-8 sequence: a leading byte starting 0 (1 byte), 110 (2 bytes), 1110 (3 bytes) or 11110 (4 bytes), followed by exactly the right number of continuation bytes starting 10. Use bit masks, one pass, and a counter of continuation bytes still owed. Also say which real-decoder checks you skip (overlong forms, surrogates, range above U+10FFFF). Example: [197,130,1] -> True; [235,140,4] -> False; [255] -> False; [] -> True.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Single pass with a small state machine. The state is one integer: how many continuation bytes are still owed. Bit shifts classify each byte.

**Say this first (1 line):** "If I owe no continuation bytes, the byte must be a valid leader and it sets the debt. If I owe some, the byte must look like 10xxxxxx and pays one off. At the end the debt must be zero."

**Brute force:** Decode with the real decoder: `bytes(data).decode('utf-8')` in a try/except. It is correct and stricter than the prompt, but in an interview it hides the bit work. I use it as the checker. Another brute force is to slice out each character by looking ahead and testing its tail bytes; that is the same O(n) with more indexing.

**Optimal:** Shift right to expose the prefix bits.
- `b >> 7 == 0`: 1-byte character, nothing owed.
- `b >> 5 == 0b110`: leader of a 2-byte character, owe 1.
- `b >> 4 == 0b1110`: owe 2.
- `b >> 3 == 0b11110`: owe 3.
- Anything else when owing nothing is invalid: `10xxxxxx` is a stray continuation, `11111xxx` is not a legal leader.
- When owing, `b >> 6 == 0b10` is required, else invalid. Then `owed -= 1`.
- Return `owed == 0`, which rejects a sequence cut off at the end.

**Complexity:** Time O(n), one pass, a few shifts per byte. Space O(1). Python ints are unbounded, but the inputs are 0..255 so shifts stay cheap.

**Dry run:** `[235, 140, 4]`. 235 = 11101011, 140 = 10001100, 4 = 00000100.
| byte | owed before | test | owed after |
|---|---|---|---|
| 235 | 0 | `235 >> 4 == 0b1110` | 2 |
| 140 | 2 | `140 >> 6 == 0b10` ok | 1 |
| 4 | 1 | `4 >> 6 == 0`, not 10 | return False |

`[197, 130, 1]`: 197 is `110xxxxx`, owe 1. 130 is `10xxxxxx`, owe 0. 1 is ASCII. End owed 0, True.

**Code:**
```python
import random


def valid_utf8_reference(data):
    """Reference: Python's own decoder (stricter: also rejects overlong, surrogates, > U+10FFFF)."""
    try:
        bytes(data).decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def valid_utf8_structural(data):
    """Structure only, the version the prompt asks for."""
    owed = 0                                  # continuation bytes still expected
    for b in data:
        if owed == 0:
            if b >> 7 == 0b0:                 # 0xxxxxxx
                continue
            elif b >> 5 == 0b110:             # 110xxxxx
                owed = 1
            elif b >> 4 == 0b1110:            # 1110xxxx
                owed = 2
            elif b >> 3 == 0b11110:           # 11110xxx
                owed = 3
            else:                             # 10xxxxxx stray continuation, or 11111xxx
                return False
        else:
            if b >> 6 != 0b10:                # must be 10xxxxxx
                return False
            owed -= 1
    return owed == 0                          # sequence must not be cut off


print(valid_utf8_structural([197, 130, 1]))
print(valid_utf8_structural([235, 140, 4]))
print(valid_utf8_structural([255]))
print(valid_utf8_structural([]))
assert valid_utf8_structural([197, 130, 1]) is True
assert valid_utf8_structural([235, 140, 4]) is False
assert valid_utf8_structural([255]) is False
assert valid_utf8_structural([]) is True
assert valid_utf8_structural([0x80]) is False           # lone continuation
assert valid_utf8_structural([0xC2]) is False           # truncated at end
assert valid_utf8_structural([0xF0, 0x9F, 0x98, 0x80]) is True   # U+1F600
assert valid_utf8_structural([0xF0, 0x9F, 0x98]) is False
assert valid_utf8_structural(list("héllo €".encode("utf-8"))) is True
assert valid_utf8_structural([0xC2, 0xC2]) is False     # lead followed by lead

# what the structural check accepts but the real decoder rejects (the checks we skip)
for name, bs in [("overlong '/' C0 AF", [0xC0, 0xAF]),
                 ("surrogate U+D800 ED A0 80", [0xED, 0xA0, 0x80]),
                 ("above U+10FFFF F4 90 80 80", [0xF4, 0x90, 0x80, 0x80]),
                 ("F8 88 80 80 80 (5-byte lead)", [0xF8, 0x88, 0x80, 0x80, 0x80])]:
    print(f"{name}: structural={valid_utf8_structural(bs)} python={valid_utf8_reference(bs)}")

# random cross-check against the real decoder. The pool avoids C0/C1, E0, ED and F4-FF
# leads, but F0 followed by 80..8F is still an overlong form, so a few disagreements
# are expected and each one is checked to be exactly that kind.
rng = random.Random(32)
pool = [0x41, 0x7F, 0x80, 0xBF, 0xC2, 0xDF, 0xE1, 0xEC, 0xEE, 0xF0, 0xF1, 0xA9, 0x9F, 0x90]
agree = 0
for _ in range(20000):
    data = [rng.choice(pool) for _ in range(rng.randint(0, 6))]
    s = valid_utf8_structural(data)
    r = valid_utf8_reference(data)
    if s != r:
        # the only allowed disagreement: an F0 lead with a too-small second byte (overlong)
        assert s and not r, data
        assert 0xF0 in data, data
    agree += (s == r)
print("random cross-check passed, exact agreement on", agree, "of 20000")
# real encoder output always passes both
for _ in range(2000):
    txt = "".join(chr(rng.choice([0x41, 0xE9, 0x20AC, 0x1F600, 0x4E2D])) for _ in range(rng.randint(0, 8)))
    bs = list(txt.encode("utf-8"))
    assert valid_utf8_structural(bs) and valid_utf8_reference(bs)
print("encoder round-trip passed: 2000 cases")
```

**Output (my run):**
```text
True
False
False
True
overlong '/' C0 AF: structural=True python=False
surrogate U+D800 ED A0 80: structural=True python=False
above U+10FFFF F4 90 80 80: structural=True python=False
F8 88 80 80 80 (5-byte lead): structural=False python=False
random cross-check passed, exact agreement on 19995 of 20000
encoder round-trip passed: 2000 cases
```
All four prompt examples are correct. The cross-check compares against Python 3.13's real decoder on a restricted byte pool. Five of 20000 cases disagree, and the script asserts that every such case contains an `F0` lead (a 4-byte overlong form such as `F0 80 ..`), which is exactly the check we skip.

**Checks I skip (the real decoder does them, shown in the output):**
- Overlong forms: `C0 AF` encodes `/` in two bytes. Leaders `C0` and `C1` are never valid, and `E0 80..9F` or `F0 80..8F` are overlong.
- Surrogates: `ED A0 80` would be U+D800, which UTF-8 forbids.
- Range: `F4 90 ..` and above would exceed U+10FFFF.
- Observed on Python 3.13: all three are rejected by `decode('utf-8')` and accepted by the structural check. A 5-byte leader `F8` is rejected by both.

**Edge cases:**
- Empty list: True (owed is 0).
- Truncated tail, such as `[0xC2]` or `[0xF0, 0x9F, 0x98]`: False because `owed != 0`.
- Lone continuation byte `0x80`: False.
- Leader followed by another leader: False.
- Byte `255` and any `11111xxx`: False.

**Follow-ups:**
- *Make it strict?* Add per-leader checks: reject `C0`, `C1`, `F5` and above; `E0` needs second byte `A0..BF`; `ED` needs `80..9F`; `F0` needs `90..BF`; `F4` needs `80..8F`.
- *Streaming input?* Keep `owed` across chunks. That is why the state is one integer.
- *Why is UTF-8 self-synchronising?* Leaders and continuations have different prefixes, so after corruption you can resync at the next non-`10` byte.

**Common mistakes:**
- Forgetting the final `owed == 0` check.
- Accepting a `10xxxxxx` byte as a leader when `owed` is 0.
- Treating `11111xxx` as a 5-byte leader.
- Using string slicing of `bin(b)` instead of shifts; it is slow and easy to get wrong on bytes below 128.

---

### Q33 ⭐ 🟡 Regex versus manual matching. Explain when you reach for `re` and when you hand-roll a parser, at concept level: regex for tokenising and validation with a fixed grammar, manual loops for hot paths, streaming and anything that needs error positions. Demonstrate catastrophic backtracking: `re.fullmatch(r'(a+)+', 'a' * n + 'b')` takes exponential time in CPython's backtracking engine as n grows (show growth for n up to about 22 and label the timings sandbox-only), and write the linear manual check for the same language 'one or more a'. Mention that a DFA or Thompson-NFA engine avoids this and that full regex matching with '.' and '*' is a DP problem in Part 11. Example: re.fullmatch(r'(a+)+', 'aaaa') -> match; re.fullmatch(r'(a+)+', 'aaab') -> None.
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Concept question with a demonstration. The tool choice depends on grammar shape and on what happens on failure. The demo is exponential backtracking against a linear scan.

**Say this first (1 line):** "Regex for a fixed grammar I can write in one line and test. A hand-written loop when the hot path, streaming or error positions matter. And never nest quantifiers over the same characters, because CPython's engine backtracks."

**Brute force:** There is no brute force to optimise here. The "naive" thing is the nested pattern `(a+)+`. On a string of n letters `a` followed by `b`, the engine tries every way to split the run of a's among the inner and outer `+`, which is about 2^n ways, before it can say no.

**Optimal:** Two parts.
- Tool choice.
  - Use `re` for tokenising and validating a fixed grammar (dates, identifiers, log lines). It is short, declarative and reviewed in one glance.
  - Hand-roll a loop for hot paths (a Python loop over bytes is slow, but a specialised one can beat a heavy pattern), streaming (a regex wants the whole string in memory), and error positions or recovery (a parser can say "unexpected character at column 17"; a failed `fullmatch` only says `None`).
  - Always: untrusted input plus a backtracking regex is a denial-of-service risk (ReDoS).
- Linear check for "one or more `a`": scan once, return False on the first non-`a`, and require non-empty. Or write the same language as `a+`, with no nested quantifier.
- Why the nested form explodes: when `b` fails to match, the engine backtracks into the inner `a+` and tries each shorter length, and each choice re-enters the outer `+` with a new split of the rest. Each of the n-1 boundaries between a's is either a split point or not, which is 2^(n-1) paths.
- Engines that avoid it: a DFA, or a Thompson NFA simulation, tracks the set of live states and moves through the string once, O(n * m) for pattern size m. Google RE2 and Rust's `regex` crate work that way. The cost is that they drop backreferences and lookarounds. Full matching with `.` and `*` written by hand is a DP problem in Part 11.

**Complexity:** `(a+)+` on `a`*n + `b` in CPython: exponential, about O(2^n) steps (reasoned above; the table below is only evidence of the shape). The manual scan: O(n) time, O(1) space.

**Dry run:** `'aab'` against `(a+)+`. The a-run has length 2, so there is 1 boundary and 2^1 = 2 ways to split it.
- Split 1: inner `a+` takes `aa`, outer stops. `b` is left over, fail.
- Split 2: inner takes `a`, outer repeats and its inner takes the second `a`. `b` is left over, fail.
- Both fail, so the result is None. With n a's there are 2^(n-1) splits, which is the doubling in the table below.

**Code:**
```python
import re
import time


def one_or_more_a_manual(s):
    """Linear manual check for the language a+ (same language as (a+)+)."""
    if not s:
        return False
    for ch in s:
        if ch != "a":
            return False
    return True


print(bool(re.fullmatch(r"(a+)+", "aaaa")))
print(re.fullmatch(r"(a+)+", "aaab"))
assert re.fullmatch(r"(a+)+", "aaaa") is not None
assert re.fullmatch(r"(a+)+", "aaab") is None
assert one_or_more_a_manual("aaaa") is True
assert one_or_more_a_manual("aaab") is False
assert one_or_more_a_manual("") is False
assert one_or_more_a_manual("b") is False
assert one_or_more_a_manual("a") is True

# same language, safe regex: no nested quantifier
for s in ["", "a", "aaaa", "aaab", "b", "ba", "ab"]:
    assert (re.fullmatch(r"a+", s) is not None) == one_or_more_a_manual(s) == (re.fullmatch(r"(a+)+", s) is not None)

# catastrophic backtracking, SANDBOX-ONLY timings (machine and CPython build dependent)
print("n   regex (a+)+ on a*n+'b'   manual")
prev = None
for n in range(14, 23):
    s = "a" * n + "b"
    t0 = time.perf_counter()
    r = re.fullmatch(r"(a+)+", s)
    t1 = time.perf_counter()
    m = one_or_more_a_manual(s)
    t2 = time.perf_counter()
    assert r is None and m is False
    ratio = "" if prev is None else f"x{(t1 - t0) / prev:.1f}"
    print(f"{n:2d}  {t1 - t0:9.4f}s {ratio:>6}   {t2 - t1:.7f}s")
    prev = t1 - t0
```

**Output (my run):**
```text
True
None
n   regex (a+)+ on a*n+'b'   manual
14     0.0005s          0.0000007s
15     0.0010s   x2.1   0.0000011s
16     0.0020s   x2.0   0.0000009s
17     0.0040s   x2.0   0.0000014s
18     0.0080s   x2.0   0.0000022s
19     0.0157s   x1.9   0.0000011s
20     0.0313s   x2.0   0.0000032s
21     0.0665s   x2.1   0.0000045s
22     0.1266s   x1.9   0.0000082s
```
Both prompt examples are correct (`aaaa` matches, `aaab` gives `None`). Timings are sandbox-only: they depend on the machine and the CPython build and they will differ on every run. In this run each extra letter about doubled the time, which fits 2^n; that is a consistent shape, not a proof (the proof is the splitting argument above). With n = 22 it was around 0.12 s here; each +10 on n would multiply that about 1000 times, so n = 50 would be far beyond waiting for. I did not run that.

**Edge cases:**
- Empty string: `(a+)+` does not match it, and my manual check returns False.
- A string with no `b` (all a's) matches fast, with no backtracking: the pathology needs a failing suffix.
- `re.match` versus `re.fullmatch`: `match` anchors only at the start. Using `match` with `$` has its own newline quirk (`$` also matches before a trailing newline).

**Follow-ups:**
- *How do you defend in Python?* Rewrite the pattern without nested quantifiers, cap input length, run untrusted patterns in a separate process with a timeout, or use a linear-time engine (the third-party `re2` bindings). Python 3.13's `re` has no timeout argument that I know of, so I did not rely on one.
- *When do I need backreferences or lookaheads?* Then DFA engines cannot help, and you must write the pattern carefully or parse by hand.
- *What does `fullmatch` versus `^...$` change?* `fullmatch` requires the whole string; `$` accepts a trailing `\n`.

**Common mistakes:**
- Nesting quantifiers over the same characters (`(a+)+`, `(a|aa)+`, `(.*)*`).
- Believing regex is always O(n) because "it is a library".
- Quoting timings as proof of exponential growth.
- Using regex to parse nested structures (balanced brackets, HTML). That is not a regular language.

---

### Q34 ⭐ 🟡 One edit distance. Given strings `s` and `t` (len <= 10^4), return True if they are exactly one edit apart, where an edit is inserting one character, deleting one character or replacing one character. Solve in one pass and O(1) space: compare lengths first, find the first mismatch and then compare the remainders according to the length difference. This is a special case of edit distance (the DP is Part 11). Example: ('ab','acb') -> True; ('cab','ad') -> False; ('1203','1213') -> True; ('','') -> False; ('a','') -> True; ('ab','ab') -> False.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports
**Pattern:** Two strings, one scan to the first mismatch, then one comparison of the remainders. This is edit distance capped at 1, so no DP is needed.

**Say this first (1 line):** "Make `s` the shorter one. If the lengths differ by more than 1, it is False. Find the first mismatch. Equal lengths mean a replace, so skip one char in both. A length gap of 1 means an insert, so skip one char in the longer only. No mismatch means the answer is whether the gap is exactly 1."

**Brute force:** Generate every string one edit from `s` (n deletes, n*k replaces, (n+1)*k inserts over an alphabet of size k) and compare each with `t`. O(n^2 * k) time because each candidate costs O(n). Fine as the checker.

**Optimal:**
- Swap so `len(s) <= len(t)`. If `len(t) - len(s) > 1`, return False.
- Walk `i` from 0. At the first `s[i] != t[i]`:
  - same length: one replacement fixes it, so the rest must be equal, `s[i+1:] == t[i+1:]`;
  - length gap 1: `t` has an extra char at `i`, so `s[i:] == t[i+1:]`.
- If the loop ends with no mismatch, the strings are equal up to `len(s)`. Exactly one edit means `t` is one char longer. Equal strings (gap 0) must be False: zero edits is not one edit.
- Why only the first mismatch matters: everything before it matches, so any single edit must happen at or after that point, and after the edit the remainders must be identical.
- I compare remainders with an index loop (`same_from`) rather than slices, so extra space is truly O(1). The slice version is shorter but copies O(n).

**Complexity:** Time O(n): one pass to the mismatch plus one pass over the remainders, each index touched about once. Space O(1) with the index loop (slices would use O(n) temporary memory).

**Dry run:** `s = '1203'`, `t = '1213'`. Same length 4.
| i | s[i], t[i] | action |
|---|---|---|
| 0 | 1, 1 | match |
| 1 | 2, 2 | match |
| 2 | 0, 1 | mismatch, same length: compare `s[3:]='3'` with `t[3:]='3'` equal, True |

`'ab'`, `'acb'`: gap 1. i=0 match. i=1: `b` vs `c` mismatch. Compare `s[1:]='b'` with `t[2:]='b'`: True.

**Code:**
```python
import random


def one_edit_brute(s, t):
    """Reference: try every single edit of s and compare with t (O(n^2))."""
    letters = set(s) | set(t) | {"z"}
    for i in range(len(s)):
        if s[:i] + s[i + 1:] == t:                         # delete
            return True
        for c in letters:
            if c != s[i] and s[:i] + c + s[i + 1:] == t:   # replace
                return True
    for i in range(len(s) + 1):
        for c in letters:
            if s[:i] + c + s[i:] == t:                     # insert
                return True
    return False


def same_from(s, i, t, j):
    """True if s[i:] == t[j:], compared by index so no slice copy (keeps O(1) extra space)."""
    if len(s) - i != len(t) - j:
        return False
    while i < len(s):
        if s[i] != t[j]:
            return False
        i += 1
        j += 1
    return True


def one_edit(s, t):
    if len(s) > len(t):                  # make s the shorter one
        s, t = t, s
    ls, lt = len(s), len(t)
    if lt - ls > 1:
        return False
    for i in range(ls):
        if s[i] != t[i]:
            if ls == lt:
                return same_from(s, i + 1, t, i + 1)   # replace: remainders equal
            return same_from(s, i, t, i + 1)       # insert into s: skip t[i]
    return lt - ls == 1                             # no mismatch: need exactly one extra char


cases = [("ab", "acb", True), ("cab", "ad", False), ("1203", "1213", True),
         ("", "", False), ("a", "", True), ("ab", "ab", False)]
for s, t, want in cases:
    got = one_edit(s, t)
    print(repr(s), repr(t), got)
    assert got is want and one_edit_brute(s, t) is want

assert one_edit("", "a") is True
assert one_edit("a", "b") is True                  # replace single char
assert one_edit("ab", "ba") is False               # two replacements
assert one_edit("abc", "ab") is True               # delete last
assert one_edit("abc", "bc") is True               # delete first
assert one_edit("abc", "abcd") is True             # insert at end
assert one_edit("abc", "abcde") is False           # length gap 2
assert one_edit("aab", "ab") is True               # duplicates
assert one_edit("a" * 10000, "a" * 9999 + "b") is True

rng = random.Random(34)
for _ in range(5000):
    n = rng.randint(0, 6)
    s = "".join(rng.choice("abc") for _ in range(n))
    t = "".join(rng.choice("abc") for _ in range(max(0, n + rng.randint(-2, 2))))
    assert one_edit(s, t) == one_edit_brute(s, t), (s, t)
    assert one_edit(s, t) == one_edit(t, s)
print("random cross-check passed: 5000 cases")
```

**Output (my run):**
```text
'ab' 'acb' True
'cab' 'ad' False
'1203' '1213' True
'' '' False
'a' '' True
'ab' 'ab' False
random cross-check passed: 5000 cases
```
All six prompt examples are correct, including the `('','')` -> False and `('ab','ab')` -> False cases.

**Edge cases:**
- Equal strings: False (no edit), not True. This is the classic bug.
- Empty versus one character: True (a single insert).
- Both empty: False.
- Length gap 2 or more: False immediately.
- Mismatch at the last position of the shorter string: the remainder comparison is of empty strings, so True.
- Duplicates (`'aab'` versus `'ab'`): the first mismatch is at index 1, the remainder `'b'` equals `'b'`, True.

**Follow-ups:**
- *What if you need "at most one edit"?* Return True when the strings are equal as well.
- *Distance k in general?* Then it is the edit-distance DP, Part 11; the concept is in the next question.
- *Transposition counts as one edit?* Different problem (Damerau-Levenshtein); a swap of two adjacent letters needs an extra branch.

**Common mistakes:**
- Returning True for identical strings.
- Not swapping to make `s` the shorter, then writing four near-duplicate branches.
- After a replace mismatch, comparing `s[i:]` with `t[i+1:]` (an insert rule) for equal lengths.
- Counting mismatches over the whole string for different lengths: shifts make everything after the insert point mismatch.

---

### Q35 ⭐ 🟡 Edit distance and LCS at concept level. State what the Levenshtein edit distance and the longest common subsequence measure, write each recurrence on the last characters of the two prefixes, and compute both for small strings with a memoised recursion (`functools.cache`). Do not build the full tabulated, space-optimised DP here; that and its reconstruction are Part 11. State the link: if only insertions and deletions are allowed the distance is len(a) + len(b) - 2 * LCS(a, b), and why a subsequence differs from a substring. Example: edit_distance('horse','ros') -> 3; edit_distance('intention','execution') -> 5; lcs('abcde','ace') -> 3; lcs('abc','def') -> 0; indel-only distance of ('horse','ros') -> 4.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Two-string recurrence on the last characters of two prefixes. Memoised recursion (`functools.cache`) only; the tabulated and space-optimised DP and the reconstruction are Part 11.

**Say this first (1 line):** "Edit distance counts the fewest insert, delete and replace steps to turn one string into the other. LCS is the longest sequence of characters that appears in both, in order, not necessarily contiguous. Both look at the last characters of the two prefixes."

**Brute force:** For LCS, list every subsequence of `a` (2^n of them) and test each against `b`. For edit distance, a breadth-first search over strings reachable by one edit. Both are exponential. I use them only as checkers on strings of length 5 or less.

**Optimal:** Let `d(i, j)` be the distance between `a[:i]` and `b[:j]`.
- Edit distance.
  - `d(i, 0) = i` (delete everything) and `d(0, j) = j` (insert everything).
  - If `a[i-1] == b[j-1]`: `d(i, j) = d(i-1, j-1)`. Matching the last characters is never worse.
  - Else: `1 + min(d(i-1, j), d(i, j-1), d(i-1, j-1))` for delete, insert, replace.
- LCS: `f(i, 0) = f(0, j) = 0`. If the last characters are equal, `f = 1 + f(i-1, j-1)`. Else `max(f(i-1, j), f(i, j-1))`: drop the last char of one string.
- The link: with only insertions and deletions, the characters you keep must be a common subsequence, and the best is the longest. Everything else is deleted from `a` or inserted from `b`, so indel distance = `len(a) + len(b) - 2 * LCS`. Replace is one step instead of delete plus insert, so `edit_distance <= indel_distance`.
- Subsequence versus substring: a subsequence may skip characters but keeps order (`ace` in `abcde`). A substring is contiguous. `lcs('abcde','ace')` is 3 but their longest common substring is 1.

**Complexity:** Both have at most (n+1)(m+1) distinct states and O(1) work per state, so O(n*m) time. The cache holds that many entries, so O(n*m) space, plus recursion depth up to n+m. Python's default recursion limit is 1000, so long strings need the iterative table (Part 11), which also allows O(min(n, m)) space.

**Dry run:** `edit_distance('horse','ros')` = 3.
- horse -> rorse (replace h by r)
- rorse -> rose (delete r)
- rose -> ros (delete e)
- `lcs('horse','ros')` is 'os' or 'rs' (length 2), so the indel-only distance is 5 + 3 - 2*2 = 4, one more than 3 because replace is not allowed.
`lcs('abcde','ace')`: last chars e = e, 1 + lcs('abcd','ac'); d vs c differ, take max of two branches; c = c gives 1 + lcs('ab','a') = 2; total 3.

**Code:**
```python
import random
import sys
from functools import cache
from itertools import combinations, product


def edit_distance(a, b):
    @cache
    def d(i, j):                       # distance between a[:i] and b[:j]
        if i == 0:
            return j                   # insert j chars
        if j == 0:
            return i                   # delete i chars
        if a[i - 1] == b[j - 1]:
            return d(i - 1, j - 1)     # last chars equal: free
        return 1 + min(d(i - 1, j),        # delete a[i-1]
                       d(i, j - 1),        # insert b[j-1]
                       d(i - 1, j - 1))    # replace
    return d(len(a), len(b))


def lcs(a, b):
    @cache
    def f(i, j):                       # LCS length of a[:i] and b[:j]
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            return 1 + f(i - 1, j - 1)
        return max(f(i - 1, j), f(i, j - 1))
    return f(len(a), len(b))


def indel_distance(a, b):
    return len(a) + len(b) - 2 * lcs(a, b)


print(edit_distance("horse", "ros"))
print(edit_distance("intention", "execution"))
print(lcs("abcde", "ace"))
print(lcs("abc", "def"))
print(indel_distance("horse", "ros"))
assert edit_distance("horse", "ros") == 3
assert edit_distance("intention", "execution") == 5
assert lcs("abcde", "ace") == 3
assert lcs("abc", "def") == 0
assert indel_distance("horse", "ros") == 4
assert edit_distance("", "") == 0 and edit_distance("", "abc") == 3 and edit_distance("abc", "") == 3
assert lcs("", "abc") == 0 and lcs("aaa", "aa") == 2

# subsequence versus substring
print("lcs('abcde','ace') =", lcs("abcde", "ace"))


def longest_common_substring(a, b):
    return max((k for k in range(min(len(a), len(b)) + 1)
                if any(a[i:i + k] in b for i in range(len(a) - k + 1))), default=0)


print("longest common substring('abcde','ace') =", longest_common_substring("abcde", "ace"))
assert longest_common_substring("abcde", "ace") == 1


# brute-force references on tiny strings
def subsequences(s):
    for k in range(len(s) + 1):
        for idx in combinations(range(len(s)), k):
            yield "".join(s[i] for i in idx)


def lcs_brute(a, b):
    sb = set(subsequences(b))
    return max(len(x) for x in subsequences(a) if x in sb)


def edit_brute(a, b):
    """Breadth-first search over edit operations; independent of the recurrence."""
    letters = sorted(set(a) | set(b))
    frontier, seen, steps = {a}, {a}, 0
    while b not in frontier:
        nxt = set()
        for s in frontier:
            for i in range(len(s)):
                nxt.add(s[:i] + s[i + 1:])
                for c in letters:
                    nxt.add(s[:i] + c + s[i + 1:])
            for i in range(len(s) + 1):
                for c in letters:
                    nxt.add(s[:i] + c + s[i:])
        frontier = nxt - seen
        seen |= nxt
        steps += 1
    return steps


rng = random.Random(35)
for _ in range(300):
    a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
    b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
    assert lcs(a, b) == lcs_brute(a, b), (a, b)
    assert edit_distance(a, b) == edit_brute(a, b), (a, b)
    assert indel_distance(a, b) >= edit_distance(a, b)          # indel-only can only cost more
    assert edit_distance(a, b) == edit_distance(b, a) and lcs(a, b) == lcs(b, a)
print("random cross-check passed: 300 pairs")

# memoised recursion depth: Python's recursion limit
print("recursion limit", sys.getrecursionlimit())
try:
    edit_distance("a" * 2000, "b" * 2000)
except RecursionError:
    print("RecursionError at length 2000 with default limit")
```

**Output (my run):**
```text
3
5
3
0
4
lcs('abcde','ace') = 3
longest common substring('abcde','ace') = 1
random cross-check passed: 300 pairs
recursion limit 1000
RecursionError at length 2000 with default limit
```
All five prompt examples are correct. Python 3.13.17 reports `sys.getrecursionlimit()` as 1000 and the memoised version hits `RecursionError` at two strings of length 2000, as predicted. The 300 random pairs check both recurrences against independent brute force (subsequence enumeration, breadth-first edit search).

**Edge cases:**
- One or both strings empty: distance is the other length, LCS is 0.
- Identical strings: distance 0, LCS is the length.
- No common letters: LCS 0; edit distance is `max(len)` because you replace the overlap and insert or delete the rest.
- Different lengths: the distance is at least `abs(len(a) - len(b))`.

**Follow-ups:**
- *Reconstruct an actual edit script or LCS string?* Walk back through the table; that is Part 11.
- *Can you do it in O(min) space?* Yes, only the previous row is needed. Part 11.
- *Different costs for each operation?* Same recurrence with weights. A replace costing 2 or more makes it equal to indel distance.

**Common mistakes:**
- Mixing up subsequence with substring.
- Using `min` for LCS or `max` for edit distance.
- Forgetting the equal-characters shortcut, or adding 1 on a match.
- Using the recursion on strings longer than about 500 without raising the recursion limit or going iterative.

---

### Q36 ⭐ 🟡 Prefix queries: sorted list versus trie, at concept level. Given up to 10^5 distinct lowercase words, answer many queries 'how many words start with prefix p?'. Implement the sorted-list plus `bisect` version (the words that start with p form one contiguous block, found by two binary searches, the upper bound being p followed by a character just above 'z') and explain the O(L log n) per query cost; then describe, without implementing it, how a trie answers in O(L) with a count stored per node, and the memory trade-off. The trie itself is Part 12. Example: words=['apple','app','apt','bat','bath'], prefix 'ap' -> 3; 'bat' -> 2; 'c' -> 0; '' -> 5.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Sorted order turns "starts with p" into one contiguous block. Two binary searches find its edges. The trie is the concept-level alternative (Part 12 owns it).

**Say this first (1 line):** "Sort the words once. All words starting with `p` sit together, from the first word >= `p` up to the first word >= `p` followed by a character above `z`. The count is the difference of the two `bisect_left` positions."

**Brute force:** For each query, scan all n words with `startswith`. O(n * L) per query. With 10^5 words and many queries, too slow. This is the checker.

**Optimal:** Sorted list plus `bisect`.
- Build: `sorted(words)`, O(n log n) comparisons, each up to L characters.
- Query `p`:
  - `lo = bisect_left(a, p)`: first word >= `p`. Anything starting with `p` is >= `p`.
  - `hi = bisect_left(a, p + '{')`: `'{'` is `chr(ord('z') + 1)`. Every word starting with `p` is `p` plus lowercase letters, and that is below `p + '{'`. Any word outside the block is either below `p` or above `p + '{'`, so the block is exactly `[lo, hi)`.
  - Answer `hi - lo`.
- The empty prefix works: `lo = 0`, `hi` = bisect of `'{'`, which is n.
- Invariant: the words in `[lo, hi)` are exactly those with prefix `p`, because the sort is lexicographic and the prefix block is an interval of that order.

**Complexity:** Per query: two binary searches of log n steps, each step compares strings of up to L characters, so O(L log n). Build O(n * L log n) in the worst case. Space O(n * L) for the stored strings (the list holds references to existing strings, plus the sorted copy's pointers, O(n)).

**Trie, described only:** Each node is a character, each root-to-node path is a prefix, and each node stores a `count` of words passing through it. Insert increments counts along the path. A query walks `len(p)` steps and returns the count at the end node, or 0 if the path breaks. So query O(L), independent of n. Build is O(total characters).
- Trade-off: shared prefixes are stored once, but each trie node costs a Python object (a dict or an array of 26 pointers plus the count), which is far heavier than the characters it represents. Sorted list: compact, simple, cache-friendly, queries O(L log n). Trie: faster queries, much more memory, and supports dynamic inserts easily (a sorted list needs `insort`, O(n) per insert).
- In my random run below, 17136 words with 101107 characters have 41901 distinct prefixes, i.e. that many trie nodes; the node count is what you pay for, not the character count.

**Dry run:** words sorted: `app, apple, apt, bat, bath`. Prefix `ap`.
| step | value | position |
|---|---|---|
| `bisect_left(a, 'ap')` | first word >= 'ap' is 'app' | 0 |
| `bisect_left(a, 'ap{')` | 'apt' < 'ap{' (t < {), 'bat' > 'ap{' | 3 |
| answer | 3 - 0 | 3 |

Prefix `c`: `lo = bisect_left(a, 'c') = 5`, `hi = bisect_left(a, 'c{') = 5`, answer 0.

**Code:**
```python
import random
import sys
from bisect import bisect_left


def count_prefix_brute(words, p):
    return sum(1 for w in words if w.startswith(p))


class PrefixCounter:
    def __init__(self, words):
        self.sorted_words = sorted(words)          # O(n log n) once, comparisons cost up to L each

    def count(self, p):
        lo = bisect_left(self.sorted_words, p)             # first word >= p
        hi = bisect_left(self.sorted_words, p + "{")       # '{' is chr(ord('z') + 1)
        return hi - lo


words = ["apple", "app", "apt", "bat", "bath"]
pc = PrefixCounter(words)
for p in ["ap", "bat", "c", ""]:
    print(repr(p), pc.count(p))
assert pc.count("ap") == 3 and pc.count("bat") == 2 and pc.count("c") == 0 and pc.count("") == 5
assert chr(ord("z") + 1) == "{"
assert pc.count("apple") == 1 and pc.count("applez") == 0 and pc.count("zzz") == 0
assert PrefixCounter([]).count("a") == 0 and PrefixCounter([]).count("") == 0
assert PrefixCounter(["z", "zz", "zzz"]).count("z") == 3        # 'zzz{' still above 'zzz'
assert PrefixCounter(["a"]).count("a") == 1

# Why '{' and not a fixed sentinel: the bound must exceed every word starting with p.
# Every such word is p + (letters a..z)*, which is < p + '{'.
assert "zzzzzzzz" < "z{"

# a small trie sketch is NOT implemented here (Part 12); only the node-count estimate
rng = random.Random(36)
for _ in range(500):
    ws = list({"".join(rng.choice("abc") for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(0, 12))})
    pc = PrefixCounter(ws)
    for _ in range(10):
        p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
        assert pc.count(p) == count_prefix_brute(ws, p), (ws, p)
print("random cross-check passed: 500 word sets x 10 prefixes")

# memory vs time sketch (sandbox-only numbers): strings in a sorted list vs trie node count
ws = list({"".join(rng.choice("abcdefghij") for _ in range(rng.randint(3, 8))) for _ in range(20000)})
nodes = len({w[:k] for w in ws for k in range(1, len(w) + 1)})      # distinct prefixes = trie nodes
chars = sum(len(w) for w in ws)
print("words", len(ws), "total chars", chars, "distinct prefixes (trie nodes, excluding root)", nodes)
```

**Output (my run):**
```text
'ap' 3
'bat' 2
'c' 0
'' 5
random cross-check passed: 500 word sets x 10 prefixes
words 17136 total chars 101107 distinct prefixes (trie nodes, excluding root) 41901
```
All four prompt examples are correct (`ap` -> 3, `bat` -> 2, `c` -> 0, empty -> 5). The last line is a count of distinct prefixes for a seeded random set, used as the trie size, not a timing.

**Edge cases:**
- Empty word list: both searches return 0.
- Empty prefix: counts all words.
- Prefix equals a whole word: that word counts (`bat` counts `bat` and `bath`).
- Prefix made of `z`: the sentinel `{` is still above `zzz`.
- Prefix longer than any word: 0.
- Non-lowercase input breaks the sentinel idea; the prompt guarantees lowercase.
- Duplicates: the prompt says distinct. With duplicates the same formula counts each copy.

**Follow-ups:**
- *Why not append `'￿'` as the upper bound?* It works for any text, since `p + '￿'` is above anything made of ordinary characters. `'{'` is only right for lowercase a-z.
- *Another way for the upper bound?* Increment the last character of `p` (`'ap'` -> `'aq'`) and use `bisect_left`; handle the all-`z` or empty case separately.
- *Words arrive online?* Trie, or `insort` on a list (O(n) shift per insert).

**Common mistakes:**
- Using `bisect_right(a, p)` for the upper bound; that is just after `p` itself and misses longer words.
- Using `p + 'z'` as the bound: `'apzz'` starts with `ap` but is above `'apz'`.
- Forgetting the list must be sorted first.
- Saying the query is O(log n): string comparisons add the factor L.

---

### Q37 ⭐ 🟡 Minimum steps to make two strings anagrams. `s` and `t` are lowercase strings of equal length (<= 5*10^4). In one step you replace any one character of `t` with any character. Return the minimum steps so that `t` becomes an anagram of `s`. Count letters and sum the surplus on one side; explain why only the positive differences matter. The plain anagram test is Part 1 Q3 and is not repeated. Example: ('bab','aba') -> 1; ('leetcode','practice') -> 5; ('anagram','mangaar') -> 0.
**Asked at:** Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports | Indian placement and IT-services style prep (a search for TCS, Infosys, Amazon string rounds returned an AtoZ placement-kit post, talentd.in Infosys and TCS practice lists that name reverse-string, anagram and palindrome tasks, and AmbitionBox and Naukri Code360 candidate reports describing basic array and string questions; snippets only, not opened; candidate-reported and unverified, no company attribution)
**Pattern:** Frequency counting. Compare the letter counts of the two strings and add up what `s` has more of.

**Say this first (1 line):** "`t` is an anagram of `s` when the counts match. Each step fixes one letter, so the answer is the total of the positive differences `count_s - count_t`."

**Brute force:** Try every way to rewrite `t` over the letters involved (alphabet^n strings), keep those that are an anagram of `s`, and take the fewest positions changed. Exponential. Tiny inputs only, as the checker. (Restricting the alphabet to letters of `s` and `t` loses nothing: writing a letter that neither string has can never help.)

**Optimal:**
- `diff[c] = count_s[c] - count_t[c]`.
- A positive `diff[c]` means `t` is short of `c`. A negative one means `t` has too many `c`.
- One step replaces one surplus letter of `t` with one missing letter. It lowers one negative difference by one and one positive difference by one.
- Equal lengths mean the positives and negatives sum to zero in total, so total positive = total negative.
- Lower bound: every step can fix at most one missing letter, so at least `sum(positive diffs)` steps are needed. Upper bound: pair each surplus letter with a missing one, that many replacements suffice. So the answer is exactly the sum of the positive differences.
- Why only the positive ones: the negative ones are the same amount counted from the other side. Adding both would double count. A letter with equal counts needs no change.

**Complexity:** Time O(n + k) to count, where k is the alphabet size (26 here). Space O(k). With n up to 5*10^4 this is a single pass.

**Dry run:** `s = 'bab'`, `t = 'aba'`.
| letter | count in s | count in t | diff |
|---|---|---|---|
| a | 1 | 2 | -1 |
| b | 2 | 1 | +1 |

Positive sum is 1: replace one `a` in `t` with `b`, giving `abb`, an anagram of `bab`.
`'leetcode'` vs `'practice'`: s has l1 e3 t1 c1 o1 d1, t has p1 r1 a1 c2 t1 i1 e1. Positives: l+1, e+2, o+1, d+1 = 5. Matches the prompt.

**Code:**
```python
import random
from collections import Counter
from itertools import product


def min_steps_brute(s, t):
    """Try every string t2 of the same length reachable by changing k positions; pick the
    smallest k with sorted(t2) == sorted(s). Exponential, tiny inputs only."""
    n = len(t)
    best = n
    alphabet = sorted(set(s) | set(t))
    for t2 in product(alphabet, repeat=n):
        if sorted(t2) == sorted(s):
            k = sum(1 for x, y in zip(t, t2) if x != y)
            best = min(best, k)
    return best


def min_steps(s, t):
    diff = Counter(s)
    diff.subtract(Counter(t))                 # diff[c] = count in s minus count in t
    return sum(v for v in diff.values() if v > 0)


cases = [("bab", "aba", 1), ("leetcode", "practice", 5), ("anagram", "mangaar", 0)]
for s, t, want in cases:
    got = min_steps(s, t)
    print(s, t, got)
    assert got == want

assert min_steps("", "") == 0
assert min_steps("a", "a") == 0
assert min_steps("a", "b") == 1
assert min_steps("aaaa", "bbbb") == 4
assert min_steps("abc", "cba") == 0
assert min_steps("a" * 50000, "b" * 50000) == 50000
# symmetry: surplus on one side equals surplus on the other
assert min_steps("leetcode", "practice") == min_steps("practice", "leetcode")

rng = random.Random(37)
for _ in range(400):
    n = rng.randint(0, 5)
    s = "".join(rng.choice("abc") for _ in range(n))
    t = "".join(rng.choice("abc") for _ in range(n))
    assert min_steps(s, t) == min_steps_brute(s, t), (s, t)
    assert min_steps(s, t) == min_steps(t, s)
print("random cross-check passed: 400 cases")
```

**Output (my run):**
```text
bab aba 1
leetcode practice 5
anagram mangaar 0
random cross-check passed: 400 cases
```
All three prompt examples are correct.

**Edge cases:**
- Empty strings: 0.
- Already an anagram (even a scrambled one): 0.
- No letters in common: n steps.
- Single character each: 0 or 1.
- Unequal lengths are out of scope (the prompt says equal). With unequal lengths this becomes a different problem (insertions and deletions allowed).

**Follow-ups:**
- *Unequal lengths, steps are append or delete?* Then the answer is the sum of the absolute differences, since each differing letter needs one operation.
- *Replace in either string?* The answer is still the same positive sum, and it is symmetric: the surplus of `s` over `t` equals that of `t` over `s`.
- *Larger alphabet?* A `Counter` or dict; the answer is still the positive-difference sum.

**Common mistakes:**
- Summing the absolute differences: that gives twice the answer.
- Only counting letters of `t` missing from `s`, and not comparing counts (it misses a letter present in both but with different counts).
- Sorting both strings and comparing positions: that counts mismatches in sorted order, which is not the same quantity.
- Forgetting `Counter.subtract` keeps negative counts, while `Counter` subtraction with `-` drops them.

---

### Q38 ⭐ 🔴 Wildcard matching. Pattern `p` may contain '?' (matches exactly one character) and '*' (matches any sequence, including empty); decide whether `p` matches the whole string `s` (both lengths <= 2000). Solve it with two pointers and one remembered star position (on a mismatch, backtrack to the last star and let it absorb one more character), giving O(n*m) worst time and O(1) space; say how it differs from the 2D DP in Part 11 and from regex '*' semantics. Example: ('aa','a') -> False; ('aa','*') -> True; ('cb','?a') -> False; ('adceb','*a*b') -> True; ('acdcb','a*c?b') -> False; ('','*') -> True.
**Asked at:** Public pattern lists (NeetCode 150 style lists as mirrored in a LeetCode discuss post, GitHub roadmap repos and a freeCodeCamp guide; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); community lists, not verified company reports | Community string-problem roundups (a LeetCode discuss post 'Most Common String Interview Problems' and similar; search snippet only, not opened); prep content, not company reports
**Pattern:** Two pointers with one remembered star. Greedy: a star only ever needs to remember its latest position, because a later star can absorb anything an earlier one could.

**Say this first (1 line):** "Walk both strings. On a match or `?` advance both. On `*` remember where it is and in `s`, and try matching nothing. On a mismatch, go back to the last star and let it eat one more character of `s`."

**Brute force:** Recursion on `(i, j)`: for `*`, try matching empty (skip it) or consuming one character; for other characters, match and advance. Without memo it is exponential. With `functools.cache` it is O(n*m) time and space, which is the 2D DP of Part 11. I use the memoised version as one checker, and a regex translation as a second independent one.

**Optimal:**
- Pointers `i` in `s`, `j` in `p`. `star` is the index of the last `*` seen in `p` (or -1). `mark` is the index in `s` where that star's current attempt started.
- If `p[j]` is `?` or equals `s[i]`: `i += 1`, `j += 1`.
- Else if `p[j]` is `*`: `star = j`, `mark = i`, `j += 1`. The star first matches empty.
- Else if there is a remembered star: `mark += 1`, `i = mark`, `j = star + 1`. The star now covers one more character.
- Else: False.
- When `s` is finished, skip any remaining `*` in `p`; the match succeeds if `j` reached the end of `p`.
- Why only the last star: suppose we fail after a later star. Moving an earlier star to eat more only helps by shifting where the remaining pattern starts in `s`. The later star could already absorb that shift, so retrying earlier stars adds nothing. This is the greedy argument.

**Complexity:** Time O(n * m) worst case: each backtrack moves `mark` forward by one (at most n times), and between backtracks the inner matching run is at most m steps. Space O(1). In the output below, the adversarial run (n = 1000, pattern `*` then 500 `a` then `b`) took 251001 loop steps, about n*m/2, so the quadratic worst case is real. Typical inputs are far faster.

**How it differs from the DP:** the Part 11 DP fills an (n+1) by (m+1) table, O(n*m) time and space, and extends to regex features. This one gets O(1) space by exploiting that `*` here matches any sequence, so only the last star matters. It does not carry over directly to regex.

**Difference from regex `*`:** in wildcard matching `*` is a standalone token that matches any string. In regex `*` is a quantifier on the previous item (`a*` is zero or more a's); the regex equivalent of wildcard `*` is `.*`. So the Part 11 regex-matching problem needs a DP over "item plus star" and cannot use this single-star greedy.

**Dry run:** `s = 'adceb'`, `p = '*a*b'`.
| i | j | action | star, mark |
|---|---|---|---|
| 0 | 0 | `p[0]='*'`: remember | 0, 0; j=1 |
| 0 | 1 | `a` = `a`: advance | i=1, j=2 |
| 1 | 2 | `p[2]='*'`: remember | 2, 1; j=3 |
| 1 | 3 | `b` vs `d`: mismatch, backtrack | mark=2, i=2, j=3 |
| 2 | 3 | `b` vs `c`: backtrack | mark=3, i=3, j=3 |
| 3 | 3 | `b` vs `e`: backtrack | mark=4, i=4, j=3 |
| 4 | 3 | `b` = `b`: advance | i=5, j=4 |
`s` is finished, `j` equals `len(p)`: True.

**Code:**
```python
import random
import re
from functools import cache


def wildcard_brute(s, p):
    """Memoised recursion (the DP idea), used as the reference."""
    @cache
    def m(i, j):
        if j == len(p):
            return i == len(s)
        if p[j] == "*":
            return m(i, j + 1) or (i < len(s) and m(i + 1, j))
        return i < len(s) and (p[j] == "?" or p[j] == s[i]) and m(i + 1, j + 1)
    return m(0, 0)


def wildcard_regex(s, p):
    """Independent reference: translate to a regex ('*' -> '.*', '?' -> '.')."""
    rx = "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in p)
    return re.fullmatch(rx, s, re.DOTALL) is not None


def wildcard(s, p):
    i = j = 0
    star = -1                 # index of the last '*' in p
    mark = 0                  # index in s where that star's current match attempt started
    while i < len(s):
        if j < len(p) and (p[j] == "?" or p[j] == s[i]):
            i += 1
            j += 1
        elif j < len(p) and p[j] == "*":
            star = j          # remember the star, let it match empty for now
            mark = i
            j += 1
        elif star != -1:      # mismatch: backtrack, star absorbs one more char
            mark += 1
            i = mark
            j = star + 1
        else:
            return False
    while j < len(p) and p[j] == "*":   # leftover pattern may only be stars
        j += 1
    return j == len(p)


cases = [("aa", "a", False), ("aa", "*", True), ("cb", "?a", False),
         ("adceb", "*a*b", True), ("acdcb", "a*c?b", False), ("", "*", True)]
for s, p, want in cases:
    got = wildcard(s, p)
    print(repr(s), repr(p), got)
    assert got is want

assert wildcard("", "") is True
assert wildcard("a", "") is False
assert wildcard("", "?") is False
assert wildcard("abc", "***") is True
assert wildcard("abc", "a*c") is True
assert wildcard("abc", "a?c") is True
assert wildcard("mississippi", "m??*ss*?i*pi") is False
assert wildcard("abcabczzzde", "*abc???de*") is True
assert wildcard("a" * 2000, "*" * 1000 + "a" * 1000) is True

# worst case for the backtracking: many near-matches, still O(n*m), here counted
def wildcard_counting(s, p):
    steps = 0
    i = j = 0
    star = -1
    mark = 0
    while i < len(s):
        steps += 1
        if j < len(p) and (p[j] == "?" or p[j] == s[i]):
            i += 1; j += 1
        elif j < len(p) and p[j] == "*":
            star = j; mark = i; j += 1
        elif star != -1:
            mark += 1; i = mark; j = star + 1
        else:
            return False, steps
    while j < len(p) and p[j] == "*":
        j += 1
    return j == len(p), steps


n = 1000
s = "a" * n
p = "*" + "a" * (n // 2) + "b"
print("adversarial n=%d, pattern length %d: result, loop steps" % (n, len(p)), wildcard_counting(s, p))

rng = random.Random(38)
for _ in range(6000):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 7)))
    p = "".join(rng.choice("ab?**") for _ in range(rng.randint(0, 7)))
    r = wildcard(s, p)
    assert r == wildcard_brute(s, p) == wildcard_regex(s, p), (s, p)
print("random cross-check passed: 6000 cases")
```

**Output (my run):**
```text
'aa' 'a' False
'aa' '*' True
'cb' '?a' False
'adceb' '*a*b' True
'acdcb' 'a*c?b' False
'' '*' True
adversarial n=1000, pattern length 502: result, loop steps (False, 251001)
random cross-check passed: 6000 cases
```
All six prompt examples are correct. The 6000 random cases (strings and patterns over `a`, `b`, `?`, `*`) agree with both the memoised recursion and the regex translation.

**Edge cases:**
- Empty `s` with `*` or `***`: True. Empty `s` with `?`: False.
- Empty pattern: only an empty `s` matches.
- Consecutive stars behave like one star.
- Pattern ending in `*` after `s` is consumed: the final loop skips them.
- Leading `*` and trailing literal: the backtracking is where the cost lives.

**Follow-ups:**
- *Why not recursion?* Pattern length 2000 with the naive recursion is exponential, and even memoised it is a 4-million-cell table with recursion depth risk (Python's limit is 1000 by default).
- *Can it be worse than O(n*m)?* No: `mark` only increases and each retry does at most m steps.
- *Can it be faster?* Split the pattern at stars into literal segments with `?`, and find each segment greedily left to right; with a faster matcher for each segment you can improve on quadratic. Not needed in interviews.

**Common mistakes:**
- Resetting `mark` to `i` when backtracking rather than `mark + 1` (infinite loop).
- Forgetting to skip trailing stars after `s` ends.
- Remembering the first star instead of the last.
- Treating wildcard `*` as the regex quantifier.

---

### Q39 ⭐ 🔴 Manacher's algorithm. Explain how Manacher finds the longest palindromic substring in O(n): transform with separators ('#') so every palindrome has odd length, keep the centre and right edge of the rightmost palindrome found so far, initialise each radius from its mirror position, and expand only past the right edge, which gives an amortised linear bound. Implement it, return the leftmost longest palindrome, and also derive the count of all palindromic substrings from the radii. Concept level: you must be able to explain the mirror trick and the amortisation, not memorise the code. Example: 'babad' -> 'bab'; 'abacdfgdcaba' -> 'aba'; count for 'aaa' -> 6.
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Reuse of work by symmetry. A palindrome is its own mirror image, so inside a big palindrome the small ones on the right are copies of the ones on the left. Concept level: explain the mirror trick and the amortisation; do not memorise the code.

**Say this first (1 line):** "Insert `#` between characters so every palindrome has odd length. Keep the palindrome that reaches furthest right. For a new centre inside it, start from its mirror's radius, capped at the right edge, and only expand beyond the edge."

**Brute force:** Expand around each of the 2n-1 centres, O(n) each, so O(n^2) worst case (for `'aaaa...'`). Counting palindromes by testing every substring is O(n^3). Both are the checkers. Expand-around-centre is fine for most interviews; Manacher is the "can you go linear" follow-up.

**Optimal:**
- Transform: `s = 'aba'` becomes `t = '#a#b#a#'`. Now every palindrome, even or odd in `s`, has a single centre in `t`, and a palindrome of radius r in `t` is a palindrome of length r in `s`.
- State: `centre` and `right`, the centre and right edge of the palindrome that extends furthest right so far. `rad[i]` is the radius at `i`.
- For a new `i < right`: its mirror is `m = 2*centre - i`. The window `[centre-R, centre+R]` is a palindrome, so what lies around `m` is reflected around `i`. Therefore `rad[i] >= min(rad[m], right - i)`. The `min` caps it at the edge because we know nothing beyond `right`.
- If `rad[m]` ends strictly inside the window, the radius at `i` is exactly `rad[m]` and the expansion test fails at once. If it reaches or passes the edge, only then can we expand, starting from `right - i`.
- After expanding, if `i + rad[i] > right`, update `centre` and `right`.
- Answer: the largest radius gives the longest palindrome. Take the smallest `i` among ties to return the leftmost. Start in `s` is `(i - rad[i]) // 2`.
- Count of palindromic substrings: a centre with radius `r` in `t` contributes `ceil(r / 2)` palindromes in `s` (lengths r, r-2, ... down to 1 or 2). Sum `(r + 1) // 2` over all `i`.
- Amortisation: the `while` loop only runs successful steps when it pushes the right edge forward, and `right` never moves back. So total successful expansions are at most the length of `t`, 2n+1. Each of the `n` centres adds O(1) other work. Total O(n).

**Complexity:** Time O(n) (reasoning above), space O(n) for `t` and `rad`. Expand-around-centre is O(n^2) time, O(1) space.

**Dry run:** `s = 'aba'`, `t = '#a#b#a#'`, indices 0..6.
| i | t[i] | mirror cap | expand | rad | right |
|---|---|---|---|---|---|
| 0 | # | none | no | 0 | 0 |
| 1 | a | none | `#`=`#` yes | 1 | 2 |
| 2 | # | none (i is not below right) | a vs b no | 0 | 2 |
| 3 | b | none (i>=right) | `#`,`a`... expands to radius 3 | 3 | 6 |
| 4 | # | mirror rad[2]=0, cap 2 | stays | 0 | 6 |
| 5 | a | mirror rad[1]=1, cap 1 | edge reached, stop | 1 | 6 |
| 6 | # | mirror rad[0]=0 | stop | 0 | 6 |
`rad = [0,1,0,3,0,1,0]` (the program prints exactly this). Largest 3 at i=3, start (3-3)//2 = 0, so `'aba'`. Count: `(r+1)//2` per centre gives 0+1+0+2+0+1+0 = 4: `a`, `b`, `a`, `aba`.

**Code:**
```python
import random


def brute_longest(s):
    """Leftmost longest palindromic substring, expand-around-centre, O(n^2)."""
    best = ""
    for c in range(2 * len(s) - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        cand = s[l + 1:r]
        if len(cand) > len(best):          # strict '>' keeps the leftmost on ties
            best = cand
    return best


def brute_count(s):
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1)
               if s[i:j] == s[i:j][::-1])


def manacher(s):
    """Returns (leftmost longest palindrome, count of palindromic substrings, radii)."""
    if not s:
        return "", 0, []
    t = "#" + "#".join(s) + "#"          # every palindrome in t has odd length
    n = len(t)
    rad = [0] * n                         # rad[i] = palindrome radius at centre i in t
    centre = right = 0                    # rightmost palindrome found: centre, and its right edge
    for i in range(n):
        if i < right:
            rad[i] = min(right - i, rad[2 * centre - i])   # start from the mirror's radius
        # expand only when we may have reached or passed the right edge
        while (i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n
               and t[i - rad[i] - 1] == t[i + rad[i] + 1]):
            rad[i] += 1
        if i + rad[i] > right:            # new rightmost palindrome
            centre, right = i, i + rad[i]
    # radius in t equals palindrome length in s
    best_len, best_c = max((r, -i) for i, r in enumerate(rad))   # ties: smallest i => leftmost
    best_c = -best_c
    start = (best_c - best_len) // 2
    count = sum((r + 1) // 2 for r in rad)   # palindromes centred at i: ceil(r / 2)
    return s[start:start + best_len], count, rad


for s in ["babad", "abacdfgdcaba"]:
    print(s, "->", manacher(s)[0])
print("count 'aaa' ->", manacher("aaa")[1])
print("radii of 'aba' in '#a#b#a#':", manacher("aba")[2])
assert manacher("babad")[0] == "bab"
assert manacher("abacdfgdcaba")[0] == "aba"
assert manacher("aaa")[1] == 6
assert manacher("") == ("", 0, [])
assert manacher("a")[:2] == ("a", 1)
assert manacher("ab")[:2] == ("a", 2)          # leftmost on ties
assert manacher("abba")[:2] == ("abba", 6)
assert manacher("cbbd")[0] == "bb"
assert manacher("a" * 1000)[1] == 1000 * 1001 // 2
assert manacher("abc" * 100)[0] == "a"

rng = random.Random(39)
for _ in range(4000):
    s = "".join(rng.choice("ab" if rng.random() < 0.6 else "abc") for _ in range(rng.randint(0, 14)))
    got, cnt, _ = manacher(s)
    assert got == brute_longest(s), (s, got, brute_longest(s))
    assert cnt == brute_count(s), s
print("random cross-check passed: 4000 cases")


# amortisation evidence: count inner while-loop expansions (successful extra matches)
def expansions(s):
    t = "#" + "#".join(s) + "#"
    n = len(t)
    rad = [0] * n
    centre = right = 0
    work = 0
    for i in range(n):
        if i < right:
            rad[i] = min(right - i, rad[2 * centre - i])
        while (i - rad[i] - 1 >= 0 and i + rad[i] + 1 < n
               and t[i - rad[i] - 1] == t[i + rad[i] + 1]):
            rad[i] += 1
            work += 1
        if i + rad[i] > right:
            centre, right = i, i + rad[i]
    return work, n


for name, s in [("a*1000", "a" * 1000), ("ab*500", "ab" * 500), ("random", "".join(rng.choice("ab") for _ in range(1000)))]:
    w, n = expansions(s)
    print(f"{name}: len(t)={n}, successful expansions={w}, bound 'right edge moves only forward' => <= {n}")
    assert w <= n
```

**Output (my run):**
```text
babad -> bab
abacdfgdcaba -> aba
count 'aaa' -> 6
radii of 'aba' in '#a#b#a#': [0, 1, 0, 3, 0, 1, 0]
random cross-check passed: 4000 cases
a*1000: len(t)=2001, successful expansions=1999, bound 'right edge moves only forward' => <= 2001
ab*500: len(t)=2001, successful expansions=1998, bound 'right edge moves only forward' => <= 2001
random: len(t)=2001, successful expansions=1998, bound 'right edge moves only forward' => <= 2001
```
All three prompt examples are correct. The last three lines count successful expansions: for a 1000-letter string they are about 2000 each (a run of one letter, `ab` repeated, and a seeded random string), never above `len(t) = 2001`. That matches the amortised argument (the right edge only moves forward by one per expansion); it is an illustration of the argument, not a proof, and it is a count of loop steps, not timing.

**Edge cases:**
- Empty string: return empty and 0.
- One character: itself and 1.
- No repeated letters: the leftmost single character; count equals n.
- All the same letter: the whole string; count n(n+1)/2.
- Ties: strict comparison on the radius, with the smallest centre kept, to return the leftmost.
- Even-length palindromes such as `'abba'`: centred on a `#` in `t`.

**Follow-ups:**
- *Why does the mirror radius not just copy blindly?* If the mirror's palindrome sticks out past the left edge of the big one, the matching part on the right is cut off at `right`, and beyond it we have no information. Hence `min(..., right - i)` and the expansion.
- *Alternatives?* Expand-around-centre O(n^2); DP O(n^2) time and space (Part 11); suffix structures with reversed-string LCP; and rolling hash plus binary search, which is O(n log n) and has collision risk.
- *Does it handle both parities?* Yes, that is what the separators are for.

**Common mistakes:**
- Forgetting the `min(right - i, ...)` cap and trusting the mirror radius beyond the edge.
- Wrong index back to `s`: the start is `(centre - radius) // 2`, not `centre - radius`.
- Off-by-one with the sentinels: not bounds-checking the `while` when `t` has no outer sentinel.
- Counting palindromes as `r` instead of `ceil(r / 2)` per centre.
- Updating `centre` and `right` on every `i` instead of only when `i + rad[i] > right`.

---

### Q40 ⭐ 🔴 Longest repeated substring (rolling hash plus binary search). Given `s` (2 <= len <= 3*10^4, lowercase), return the length of the longest substring that occurs at least twice (occurrences may overlap), or 0. If a length L repeats then every shorter length repeats, so binary search on L and test each L with a rolling hash over all windows in a set, verifying actual substrings on any hash hit to rule out collisions. Give the O(n log n) expected time and the O(n^2) per-length cost of the naive test, and name suffix arrays as the exact alternative. Example: 'banana' -> 3 ('ana'); 'abcd' -> 0; 'aaaaa' -> 4; 'abcabcabc' -> 6.
**Asked at:** Pattern-matching tutorials and guides (techinterview.org string-algorithm patterns pages, a dev.to Z/KMP/Rabin-Karp article, HackerEarth exact-matching notes; search snippets only, not opened); tutorial content, not company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Binary search on the answer, with a rolling hash as the feasibility test. The predicate "some substring of length L occurs twice" is monotone: if length L repeats, every shorter length repeats (cut the same characters off both ends of the two copies).

**Say this first (1 line):** "Binary search the length L. To test L, slide a rolling hash over every window, keep hashes in a dict, and on a hit compare the real substrings so a collision cannot fool me."

**Brute force:** For each L from n-1 down, put all n-L+1 substrings of length L into a set and stop at the first duplicate. Each slice and hash costs O(L), so one length costs O(n * L), up to O(n^2), and all lengths O(n^3) in the worst case. With n = 3*10^4 that is far too slow. This is the checker.

**Optimal:**
- Monotone, so binary search `L` in `[0, n-1]`: if `has_repeat(L)` then `lo = mid` else `hi = mid - 1`. About log2(n) = 15 rounds.
- `has_repeat(L)` with a polynomial rolling hash modulo a large prime (2^61 - 1):
  - Hash of the first window: `h = sum(ord(c) * base^(L-1-k))`.
  - Slide: remove the leftmost character `ord(s[i-1]) * base^(L-1)`, multiply by `base`, add the new one. O(1) per step.
  - Store `hash -> list of start indexes`. On a hit, compare the actual substrings `s[j:j+L] == s[i:i+L]` for the stored starts. Only an equal pair returns True.
- Why verify: two different substrings can share a hash. Without the check a collision gives a false "repeat" and the answer can be too big. In the output below I set the modulus to 5 on purpose: the unverified version returns 4 for `'abcdefgh'` whose true answer is 0, while the verified version stays correct on every test.
- Overlap is allowed, which is why `'aaaaa'` gives 4 (`aaaa` at positions 0 and 1).

**Complexity:** Each round is O(n) expected for the hashing plus the occasional verification. With a 61-bit modulus a false hit is very unlikely, so verifications are almost all true repeats, and the round stops at the first one. Total O(n log n) expected time, O(n) space for the dict. Worst case is higher: if collisions are frequent (like my modulus-5 demo), the verification lists get long and a round can cost O(n * L). The naive per-length test builds O(n) slices of length up to L, so O(n^2) per length in the worst case.

**Exact alternative:** a suffix array. Sort all suffixes, compute the LCP (longest common prefix) array of neighbours, and the answer is the maximum LCP. Any repeated substring is a common prefix of two suffixes, and two suffixes with a long common prefix sort near each other. Construction is O(n log n) with the doubling method (or O(n) with SA-IS), and Kasai's algorithm builds LCP in O(n). No randomness, no collisions. Suffix automaton and suffix tree also work.

**Dry run:** `s = 'banana'`, n = 6. Search `[0, 5]`.
| lo, hi | mid | repeat of length mid? | next |
|---|---|---|---|
| 0, 5 | 3 | `ana` at 1 and 3: yes | lo = 3 |
| 3, 5 | 4 | `bana, anan, nana`: all distinct, no | hi = 3 |
Answer 3. For `'abcd'`: mid = 2, `ab, bc, cd` distinct, hi = 1; mid = 1, four distinct letters, hi = 0. Answer 0.

**Code:**
```python
import random


def lrs_brute(s):
    """Longest length L such that some substring of length L occurs twice (overlap allowed). O(n^2) per
    length set-building, O(n^3) overall via checking every length from the top."""
    n = len(s)
    for L in range(n - 1, 0, -1):
        seen = set()
        for i in range(n - L + 1):
            w = s[i:i + L]
            if w in seen:
                return L
            seen.add(w)
    return 0


MOD = (1 << 61) - 1          # large prime modulus
BASE = 911382323


def has_repeat(s, L, base=BASE, mod=MOD):
    """Does some substring of length L occur at least twice? Rolling hash, verify on hit."""
    n = len(s)
    if L == 0:
        return True
    top = pow(base, L - 1, mod)
    h = 0
    for k in range(L):
        h = (h * base + ord(s[k])) % mod
    seen = {h: [0]}                           # hash -> starts with that hash
    for i in range(1, n - L + 1):
        h = ((h - ord(s[i - 1]) * top) * base + ord(s[i + L - 1])) % mod
        if h in seen:
            for j in seen[h]:                 # verify real substrings: rules out collisions
                if s[j:j + L] == s[i:i + L]:
                    return True
            seen[h].append(i)
        else:
            seen[h] = [i]
    return False


def lrs(s, base=BASE, mod=MOD):
    lo, hi = 0, len(s) - 1                    # answer is in [0, n-1]; monotone predicate
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if has_repeat(s, mid, base, mod):
            lo = mid
        else:
            hi = mid - 1
    return lo


for s in ["banana", "abcd", "aaaaa", "abcabcabc"]:
    print(s, "->", lrs(s))
assert lrs("banana") == 3 and lrs("abcd") == 0 and lrs("aaaaa") == 4 and lrs("abcabcabc") == 6
assert lrs("aa") == 1 and lrs("ab") == 0 and lrs("abab") == 2
assert lrs("a" * 30000) == 29999
assert lrs("abcdefghijklmnopqrstuvwxyz" * 2) == 26
assert lrs("ab" * 5 + "c") == 8

# worst-case collisions: a tiny modulus forces hash hits, and the verification must keep the answer right
bad = lrs("abcabcabcxyz", base=7, mod=5)
print("with modulus 5 (heavy collisions):", bad, "expected", lrs_brute("abcabcabcxyz"))
assert bad == lrs_brute("abcabcabcxyz")


def lrs_no_verify(s, base=7, mod=5):
    """Deliberately WRONG: trusts the hash. Shows why verification matters."""
    def rep(L):
        h = 0
        hs = set()
        for i in range(len(s) - L + 1):
            h = sum(ord(c) * pow(base, L - 1 - k, mod) for k, c in enumerate(s[i:i + L])) % mod
            if h in hs:
                return True
            hs.add(h)
        return False
    lo, hi = 0, len(s) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if rep(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


print("no verification, modulus 5:", lrs_no_verify("abcdefgh"), "true answer", lrs_brute("abcdefgh"))
assert lrs_no_verify("abcdefgh") != lrs_brute("abcdefgh")

rng = random.Random(40)
for _ in range(1500):
    s = "".join(rng.choice("ab" if rng.random() < 0.5 else "abc") for _ in range(rng.randint(2, 16)))
    assert lrs(s) == lrs_brute(s), s
    assert lrs(s, base=7, mod=11) == lrs_brute(s), s       # tiny modulus: verification keeps it exact
print("random cross-check passed: 1500 cases (default and tiny modulus)")
```

**Output (my run):**
```text
banana -> 3
abcd -> 0
aaaaa -> 4
abcabcabc -> 6
with modulus 5 (heavy collisions): 6 expected 6
no verification, modulus 5: 4 true answer 0
random cross-check passed: 1500 cases (default and tiny modulus)
```
All four prompt examples are correct. The tiny-modulus runs (modulus 5 and 11) cross-check against brute force on the seeded random strings, and all agree because verification catches every collision; the deliberately unverified variant returns a wrong answer, as shown.

**Edge cases:**
- `'aa'`: length 1 repeats, answer 1. `'ab'`: 0.
- All the same letter: n-1 (maximal overlap).
- No repeated letter at all: 0 (the binary search must end with `lo = 0`, so keep length 0 and 1 both handled).
- A periodic string like `'abcabcabc'`: 6, the overlap case; a version requiring non-overlap would give 4.
- Upper search bound is n-1, because a length-n substring occurs once.

**Follow-ups:**
- *Non-overlapping occurrences only?* Keep the earliest start per hash and require `i - j >= L` on a hit; the binary search stays valid.
- *Return the substring, not the length?* Remember the start index from the last successful `has_repeat`.
- *Avoid the randomised risk?* Use a suffix array plus LCP, or pick a random base at run time so no input can be crafted against a fixed one.
- *Why not a set of the substrings?* It works and is simplest, but building the slices costs O(L) each and memory O(n * L).

**Common mistakes:**
- Not verifying on a hash hit.
- A wrong sliding update: forgetting to multiply the outgoing character by `base^(L-1)`, or a negative number from the subtraction (Python's `%` makes the result non-negative, but in C-like languages it needs care).
- Searching `[0, n]` with an unguarded window that does not exist (length n has one window only).
- Using a small base or modulus and claiming O(n log n) without the collision caveat.
- Assuming the search needs monotonicity of the hash. It is the length predicate that is monotone.

