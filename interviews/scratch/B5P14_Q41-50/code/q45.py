import random
random.seed(45)

class NumMatrix2D:
    def __init__(self, matrix):
        self.m = len(matrix); self.n = len(matrix[0])
        self.a = [[0] * self.n for _ in range(self.m)]            # current values (for the delta)
        self.t = [[0] * (self.n + 1) for _ in range(self.m + 1)]  # 1-indexed tree
        for i in range(self.m):
            for j in range(self.n):
                self.update(i, j, matrix[i][j])

    def update(self, r, c, v):
        d = v - self.a[r][c]
        self.a[r][c] = v
        i = r + 1
        while i <= self.m:
            j = c + 1
            while j <= self.n:
                self.t[i][j] += d
                j += j & -j
            i += i & -i

    def _pre(self, r, c):                     # sum of rows < r and columns < c
        s = 0; i = r
        while i > 0:
            j = c
            while j > 0:
                s += self.t[i][j]
                j -= j & -j
            i -= i & -i
        return s

    def sumRegion(self, r1, c1, r2, c2):
        return (self._pre(r2 + 1, c2 + 1) - self._pre(r1, c2 + 1)
                - self._pre(r2 + 1, c1) + self._pre(r1, c1))

class Naive:
    def __init__(self, matrix): self.a = [list(r) for r in matrix]
    def update(self, r, c, v): self.a[r][c] = v
    def sumRegion(self, r1, c1, r2, c2):
        return sum(self.a[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))

def run(cls, init, ops):
    obj = cls(*init)
    return [getattr(obj, m)(*a) for m, a in ops]

init = [[[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]]
ops = [['sumRegion', [0, 0, 2, 3]], ['sumRegion', [1, 1, 2, 2]], ['update', [1, 2, 10]], ['sumRegion', [1, 1, 2, 2]], ['sumRegion', [1, 2, 1, 2]]]
got = run(NumMatrix2D, init, ops)
assert got == [28, 11, None, 18, 10], got
print('example ->', got)

for _ in range(400):
    m, n = random.randint(1, 6), random.randint(1, 6)
    mat = [[random.randint(-9, 9) for _ in range(n)] for _ in range(m)]
    ops = []
    for _ in range(random.randint(0, 25)):
        if random.random() < .4:
            ops.append(['update', [random.randrange(m), random.randrange(n), random.randint(-9, 9)]])
        else:
            r1 = random.randrange(m); r2 = random.randrange(r1, m); c1 = random.randrange(n); c2 = random.randrange(c1, n)
            ops.append(['sumRegion', [r1, c1, r2, c2]])
    assert run(NumMatrix2D, [mat], ops) == run(Naive, [mat], ops), (mat, ops)
print('400 random operation sequences match the naive reference')

assert run(NumMatrix2D, [[[5]]], [['sumRegion', [0, 0, 0, 0]], ['update', [0, 0, -2]], ['sumRegion', [0, 0, 0, 0]]]) == [5, None, -2]
assert run(NumMatrix2D, [[[1, 2, 3]]], [['sumRegion', [0, 1, 0, 2]]]) == [5]     # single row
assert run(NumMatrix2D, [[[1], [2], [3]]], [['sumRegion', [0, 0, 2, 0]]]) == [6]  # single column
# update stores the DELTA: setting a cell to its current value changes nothing
assert run(NumMatrix2D, [[[4, 4], [4, 4]]], [['update', [1, 1, 4]], ['sumRegion', [0, 0, 1, 1]]]) == [None, 16]
t = NumMatrix2D([[1] * 200 for _ in range(200)])
assert t.sumRegion(0, 0, 199, 199) == 40000
t.update(199, 199, 101)
assert t.sumRegion(0, 0, 199, 199) == 40100 and t.sumRegion(199, 199, 199, 199) == 101
print('200 x 200 ok')
