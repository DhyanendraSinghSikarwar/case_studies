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
