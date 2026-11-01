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
