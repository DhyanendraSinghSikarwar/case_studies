import random

def brute(s, t):
    def build(x):
        st = []
        for ch in x:
            if ch == '#':
                if st:
                    st.pop()
            else:
                st.append(ch)
        return st
    return build(s) == build(t)

def next_valid(x, i):
    """Index of the next surviving character at or left of i, or -1."""
    skip = 0
    while i >= 0:
        if x[i] == '#':
            skip += 1
        elif skip > 0:
            skip -= 1          # this letter is erased by a later '#'
        else:
            return i           # a surviving letter
        i -= 1
    return -1

def optimal(s, t):
    i, j = len(s) - 1, len(t) - 1
    while True:
        i = next_valid(s, i)
        j = next_valid(t, j)
        if i < 0 and j < 0:
            return True
        if i < 0 or j < 0:
            return False
        if s[i] != t[j]:
            return False
        i -= 1
        j -= 1

assert optimal('ab#c', 'ad#c') is True
assert optimal('a#c', 'b') is False
assert optimal('a##c', '#a#c') is True
assert optimal('', '') is True
assert optimal('#', '') is True
assert optimal('###', 'a#') is True
assert optimal('a', 'a#') is False
assert optimal('ab', 'a') is False           # different lengths after deletion
assert optimal('abc', 'abc') is True
assert optimal('bxj##tw', 'bxj###tw') is False
assert optimal('xy#z', 'xzz#') is True

rng = random.Random(22)
for _ in range(2000):
    s = ''.join(rng.choice('ab#') for _ in range(rng.randint(0, 9)))
    t = ''.join(rng.choice('ab#') for _ in range(rng.randint(0, 9)))
    assert optimal(s, t) == brute(s, t), (s, t)
print("2000 random cases agree with the stack brute force")
print(optimal('ab#c', 'ad#c'), optimal('a#c', 'b'), optimal('a##c', '#a#c'))
