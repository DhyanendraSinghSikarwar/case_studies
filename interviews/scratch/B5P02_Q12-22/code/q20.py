import random

def brute(s):
    if s == s[::-1]:
        return True
    return any((t := s[:i] + s[i + 1:]) == t[::-1] for i in range(len(s)))

def is_pal(s, l, r):
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True

def optimal(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            # one deletion allowed: skip the left char or the right char
            return is_pal(s, l + 1, r) or is_pal(s, l, r - 1)
        l += 1
        r -= 1
    return True

assert optimal('aba') is True
assert optimal('abca') is True
assert optimal('abc') is False
assert optimal('') is True
assert optimal('a') is True
assert optimal('ab') is True
assert optimal('abca') is True
assert optimal('deeee') is True            # delete the leading d
assert optimal('eeeed') is True            # delete the trailing d
assert optimal('abcdeba') is False

rng = random.Random(20)
for _ in range(1500):
    s = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 9)))
    assert optimal(s) == brute(s), s
print("1500 random cases agree with brute force")
print(optimal('aba'), optimal('abca'), optimal('abc'))
# the greedy trap: only skipping one side is wrong
def left_only(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return is_pal(s, l + 1, r)
        l += 1; r -= 1
    return True
print("skip-left-only on 'eeeed':", left_only('eeeed'), "(true answer True)")
