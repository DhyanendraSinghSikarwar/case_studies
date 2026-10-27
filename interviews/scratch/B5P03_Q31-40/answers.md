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
