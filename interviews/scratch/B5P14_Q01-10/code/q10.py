import random

class NumArray:                        # optimal: Fenwick tree (1-based) + a copy of the values
    def __init__(self, nums):
        n = self.n = len(nums); self.a = list(nums); self.t = [0] * (n + 1)
        for i in range(1, n + 1):                     # O(n) build: push each node into its parent
            self.t[i] += nums[i - 1]
            j = i + (i & -i)
            if j <= n: self.t[j] += self.t[i]
    def update(self, i, val):
        d = val - self.a[i]; self.a[i] = val          # DELTA, not val
        i += 1                                        # shift to 1-based
        while i <= self.n:
            self.t[i] += d; i += i & -i               # climb to the next block that covers i
    def _prefix(self, i):                             # sum of nums[0 .. i-1]
        s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i               # strip the lowest set bit
        return s
    def sumRange(self, l, r): return self._prefix(r + 1) - self._prefix(l)

class NaiveArray:                      # brute force: plain list, O(n) query
    def __init__(self, nums): self.a = list(nums)
    def update(self, i, val): self.a[i] = val
    def sumRange(self, l, r): return sum(self.a[l:r + 1])

class WrongArray(NumArray):            # the classic bug: adds val instead of val - old
    def update(self, i, val):
        self.a[i] = val; i += 1
        while i <= self.n: self.t[i] += val; i += i & -i

def run(cls, init, ops):
    o = cls(*init); return [getattr(o, m)(*a) for m, a in ops]

e1 = ([[1,3,5]], [['sumRange',[0,2]],['update',[1,2]],['sumRange',[0,2]],['sumRange',[2,2]]], [9,None,8,5])
e2 = ([[-4,7]], [['sumRange',[0,1]],['update',[0,10]],['sumRange',[0,0]],['sumRange',[0,1]]], [3,None,10,17])
for init, ops, want in (e1, e2):
    assert run(NumArray, init, ops) == want == run(NaiveArray, init, ops)
print("examples:", run(NumArray, *e1[:2]), run(NumArray, *e2[:2]))
print("'add val' bug on example 1:", run(WrongArray, *e1[:2]), "(wanted [9, None, 8, 5])")
assert run(WrongArray, *e1[:2]) != e1[2]

random.seed(14)
for _ in range(1500):
    n = random.randint(1, 12); nums = [random.randint(-9, 9) for _ in range(n)]; ops = []
    for _ in range(random.randint(0, 40)):
        if random.random() < .5: ops.append(['update', [random.randrange(n), random.randint(-9, 9)]])
        else:
            l = random.randrange(n); ops.append(['sumRange', [l, random.randrange(l, n)]])
    assert run(NumArray, [nums], ops) == run(NaiveArray, [nums], ops), (nums, ops)
print("1500 random operation sequences: Fenwick == naive")

# the block rule: t[i] covers length i & -i ending at i, checked against direct sums
nums = [random.randint(-50, 50) for _ in range(37)]; f = NumArray(nums)
for i in range(1, 38): assert f.t[i] == sum(nums[i - (i & -i):i])
print("t[i] == sum of the block of length i & -i ending at i, for every i in 1..37")

# edge cases
assert run(NumArray, [[5]], [['sumRange',[0,0]],['update',[0,-5]],['sumRange',[0,0]]]) == [5, None, -5]   # n = 1
f = NumArray([0] * 8); f.update(7, 3); assert f.sumRange(0, 7) == 3 and f.sumRange(0, 6) == 0              # last index
n = 10**5; f = NumArray([10**9] * n); assert f.sumRange(0, n - 1) == 10**9 * n                           # big sums
f.update(0, -10**9); assert f.sumRange(0, n - 1) == 10**9 * (n - 2) and f.sumRange(0, 0) == -10**9
print("edge asserts ok (n=1, last index, 10^5 values of 10^9, negative set)")
