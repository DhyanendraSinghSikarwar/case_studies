import random
from collections import Counter

def brute(note, magazine):
    mag = list(magazine)
    for ch in note:
        if ch in mag:
            mag.remove(ch)           # O(len(magazine)) each time
        else:
            return False
    return True

def counter_version(note, magazine):
    need = Counter(note) - Counter(magazine)   # keeps only POSITIVE leftovers
    return not need                             # empty Counter means nothing missing

def manual(note, magazine):
    have = [0] * 26
    for ch in magazine:
        have[ord(ch) - 97] += 1
    for ch in note:
        i = ord(ch) - 97
        have[i] -= 1
        if have[i] < 0:
            return False
    return True

for f in (brute, counter_version, manual):
    assert f('aa', 'aab') is True
    assert f('aa', 'ab') is False
    assert f('', '') is True
    assert f('', 'abc') is True
    assert f('a', '') is False
    assert f('abc', 'cba') is True
    assert f('aab', 'baa') is True

# the pitfall: subtraction silently drops non-positive counts
d = Counter('aa') - Counter('aab')
print("Counter('aa') - Counter('aab') =", d, "(b:-1 is gone, a:0 is gone)")
d2 = Counter('aa'); d2.subtract(Counter('aab'))
print("subtract() keeps them:", d2)
# wrong direction: magazine - note is NOT the check
print("wrong direction magazine - note:", Counter('aab') - Counter('aa'), "(leftover b, says nothing about note)")

rng = random.Random(18)
for _ in range(1000):
    note = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 6)))
    mag = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    assert brute(note, mag) == counter_version(note, mag) == manual(note, mag), (note, mag)
print("1000 random cases agree")
print(manual('aa', 'aab'), manual('aa', 'ab'))
