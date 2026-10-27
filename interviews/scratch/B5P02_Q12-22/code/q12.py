import random

def brute(nums, target):
    n, best = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s >= target:
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best

def optimal(nums, target):
    best = 0
    left = 0
    total = 0
    for right, x in enumerate(nums):
        total += x                      # expand
        while total >= target:          # shrink while still valid
            width = right - left + 1
            if best == 0 or width < best:
                best = width
            total -= nums[left]
            left += 1
    return best

assert optimal([2, 3, 1, 2, 4, 3], 7) == 2
assert optimal([1, 4, 4], 4) == 1
assert optimal([1] * 8, 11) == 0
assert optimal([], 5) == 0
assert optimal([5], 5) == 1
assert optimal([5], 6) == 0
assert optimal([1, 1, 1, 1], 4) == 4          # whole array
assert optimal([10, 1, 1], 3) == 1            # target already met by one element
assert optimal([3, 3, 3], 1) == 1             # tiny target

rng = random.Random(12)
for _ in range(600):
    a = [rng.randint(1, 6) for _ in range(rng.randint(0, 10))]
    t = rng.randint(1, 25)
    assert optimal(a, t) == brute(a, t), (a, t)
print("600 random cases agree with brute force")
print(optimal([2, 3, 1, 2, 4, 3], 7), optimal([1, 4, 4], 4), optimal([1] * 8, 11))
# why positivity matters: with a negative the window answer can be wrong
neg = [-3, 1]
true_len = min(j - i + 1 for i in range(len(neg)) for j in range(i, len(neg)) if sum(neg[i:j + 1]) >= 1)
print("with a negative", neg, "target 1: window says", optimal(neg, 1), "true answer", true_len)
