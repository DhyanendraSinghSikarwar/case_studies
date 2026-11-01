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
