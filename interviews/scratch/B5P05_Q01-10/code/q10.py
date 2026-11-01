import random

def brute(m, t):
    return any(t in row for row in m)

def search_matrix(m, t):
    R, C = len(m), len(m[0])
    lo, hi = 0, R * C - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = m[mid // C][mid % C]
        if v == t: return True
        if v < t: lo = mid + 1
        else: hi = mid - 1
    return False

def two_step(m, t):
    lo, hi = 0, len(m) - 1               # last row whose first element <= t
    row = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if m[mid][0] <= t: row, lo = mid, mid + 1
        else: hi = mid - 1
    if row < 0: return False
    r = m[row]; lo, hi = 0, len(r) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if r[mid] == t: return True
        if r[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return False

random.seed(10)
for _ in range(2000):
    R, C = random.randint(1, 5), random.randint(1, 5)
    vals = sorted(random.sample(range(-20, 60), R * C))
    m = [vals[i*C:(i+1)*C] for i in range(R)]
    for t in range(-22, 62):
        assert search_matrix(m, t) == two_step(m, t) == brute(m, t)
print("cross-check ok")
M = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
print(search_matrix(M, 3), search_matrix(M, 13), search_matrix([[1]], 1), search_matrix([[1],[3]], 3))
