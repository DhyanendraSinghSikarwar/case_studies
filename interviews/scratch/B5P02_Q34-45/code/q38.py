import random

def brute(arr):
    best = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 2, n):
            seg = arr[i:j + 1]
            p = 0
            while p + 1 < len(seg) and seg[p] < seg[p + 1]: p += 1
            if p == 0 or p == len(seg) - 1: continue
            q = p
            while q + 1 < len(seg) and seg[q] > seg[q + 1]: q += 1
            if q == len(seg) - 1: best = max(best, len(seg))
    return best

def longest_mountain(arr):
    n, best, i = len(arr), 0, 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:        # i is a peak
            l = i - 1
            while l > 0 and arr[l - 1] < arr[l]: l -= 1
            r = i + 1
            while r < n - 1 and arr[r] > arr[r + 1]: r += 1
            best = max(best, r - l + 1)
            i = r + 1                                # jump past the mountain: each index scanned O(1) times
        else:
            i += 1
    return best

for a, exp in [([2, 1, 4, 7, 3, 2, 5], 5), ([2, 2, 2], 0)]:
    assert longest_mountain(a) == brute(a) == exp
    print(a, "->", longest_mountain(a))
assert longest_mountain([]) == 0 and longest_mountain([1]) == 0 and longest_mountain([1, 2]) == 0
assert longest_mountain([1, 2, 3]) == 0 and longest_mountain([3, 2, 1]) == 0 and longest_mountain([1, 3, 2]) == 3
assert longest_mountain([1, 3, 3, 2]) == 0 and longest_mountain([0, 1, 0, 1, 0]) == 3
random.seed(38)
for _ in range(1500):
    a = [random.randint(0, 4) for _ in range(random.randint(0, 11))]
    assert longest_mountain(a) == brute(a), a
print("1500 seeded cases match brute force; edges pass")
