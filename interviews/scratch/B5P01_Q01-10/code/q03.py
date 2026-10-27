import random
import string
from collections import Counter


def anagram_brute(s, t):
    return sorted(s) == sorted(t)


def anagram_array(s, t):
    if len(s) != len(t):
        return False
    cnt = [0] * 26
    for a, b in zip(s, t):
        cnt[ord(a) - 97] += 1
        cnt[ord(b) - 97] -= 1
    return not any(cnt)


def anagram_counter(s, t):
    # works for any Unicode string: Counter keys are code points
    return len(s) == len(t) and Counter(s) == Counter(t)


print("listen/silent:", anagram_array("listen", "silent"), "(expected True)")
print("rat/car:", anagram_array("rat", "car"), "(expected False)")

random.seed(3)
for _ in range(1000):
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
    if random.random() < 0.5:
        t = list(s)
        random.shuffle(t)
        t = "".join(t)
    else:
        t = "".join(random.choice("abc") for _ in range(random.randint(0, 6)))
    b = anagram_brute(s, t)
    assert anagram_array(s, t) == b == anagram_counter(s, t), (s, t)
print("cross-check: 1000 seeded cases agree")

assert anagram_array("", "") is True
assert anagram_array("a", "a") is True
assert anagram_array("ab", "a") is False
assert anagram_array("aab", "abb") is False
big = "".join(random.choice(string.ascii_lowercase) for _ in range(50000))
shuf = list(big)
random.shuffle(shuf)
assert anagram_array(big, "".join(shuf)) is True

# Unicode: the 26-slot array breaks (ord - 97 can be negative or huge); Counter is fine
try:
    anagram_array("\u00e9a", "a\u00e9")
except IndexError:
    print("26-slot array on e-acute: IndexError (ord 233 - 97 = 136, out of range)")
# worse: a char whose index lands in -26..-1 wraps silently (negative list index)
print("26-slot array on '[' vs 'u' (wrong True):", anagram_array("[", "u"))
print("Counter on Unicode:", anagram_counter("naïve", "ïvena"), anagram_counter("éa", "ae"))
# combining characters: same text, different code points
a, b = "é", "é"
print("precomposed vs combining look equal but len:", len(a), len(b), "Counter equal:", anagram_counter(a, b))
import unicodedata
print("after NFC normalisation:", anagram_counter(unicodedata.normalize("NFC", a), unicodedata.normalize("NFC", b)))
print("edge asserts passed")
