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
