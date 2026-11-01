import random


def abc_brute(s):
    total = 0
    for i in range(len(s)):
        for j in range(i + 3, len(s) + 1):
            if {"a", "b", "c"} <= set(s[i:j]):
                total += 1
    return total


def abc_window(s):
    # for each right end, count the starts that are still valid; left only moves forward
    cnt = {"a": 0, "b": 0, "c": 0}
    left = total = 0
    n = len(s)
    for right, ch in enumerate(s):
        cnt[ch] += 1
        while cnt["a"] and cnt["b"] and cnt["c"]:
            # window [left, right] is valid, and so is every longer window to the right
            total += n - right
            cnt[s[left]] -= 1
            left += 1
    return total


def abc_lastseen(s):
    # simplest: starts 0..min(last a, last b, last c) all work for this right end
    last = {"a": -1, "b": -1, "c": -1}
    total = 0
    for i, ch in enumerate(s):
        last[ch] = i
        total += min(last.values()) + 1  # -1 + 1 = 0 until all three have appeared
    return total


for s, want in (("abcabc", 10), ("aaacb", 3), ("abc", 1)):
    print(repr(s), abc_window(s), abc_lastseen(s), f"(expected {want})")

random.seed(31)
for _ in range(1000):
    n = random.randint(0, 12)
    s = "".join(random.choice("abc") for _ in range(n))
    b = abc_brute(s)
    assert abc_window(s) == b == abc_lastseen(s), s
print("cross-check: 1000 seeded cases agree")

assert abc_window("") == 0 == abc_lastseen("")
assert abc_window("a") == 0
assert abc_window("ab") == 0
assert abc_window("aaaa") == 0
assert abc_window("abc") == 1
assert abc_window("cba") == 1
big = "".join(random.choice("abc") for _ in range(5 * 10 ** 4))
assert abc_window(big) == abc_lastseen(big)
n = 3 * 10 ** 4
assert abc_window("abc" * (n // 3)) == abc_lastseen("abc" * (n // 3))
print("edge asserts passed")
