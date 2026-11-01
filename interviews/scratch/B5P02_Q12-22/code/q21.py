import random

def brute(nums, m=2):
    out = []
    for v in nums:
        if out.count(v) < m:        # keeps first m copies; O(n) count per element
            out.append(v)
    return len(out), out

def optimal(nums, m=2):
    k = 0                                    # write position
    for x in nums:
        if k < m or x != nums[k - m]:        # compare with the slot m behind the write head
            nums[k] = x
            k += 1
    return k

def run(a, m=2):
    b = list(a)
    k = optimal(b, m)
    return k, b[:k]

assert run([1, 1, 1, 2, 2, 3]) == (5, [1, 1, 2, 2, 3])
assert run([0, 0, 1, 1, 1, 1, 2, 3, 3]) == (7, [0, 0, 1, 1, 2, 3, 3])
assert run([]) == (0, [])
assert run([7]) == (1, [7])
assert run([5, 5, 5, 5, 5]) == (2, [5, 5])
assert run([1, 2, 3]) == (3, [1, 2, 3])
assert run([-1, -1, -1, 0, 0, 0]) == (4, [-1, -1, 0, 0])
assert run([1, 1, 1, 2, 2, 3], m=1) == (3, [1, 2, 3])        # generalises to m = 1
assert run([1, 1, 1, 1, 2], m=3) == (4, [1, 1, 1, 2])         # and m = 3

rng = random.Random(21)
for _ in range(1000):
    a = sorted(rng.randint(-3, 3) for _ in range(rng.randint(0, 12)))
    for m in (1, 2, 3):
        assert run(a, m) == brute(a, m), (a, m)
print("1000 random sorted lists, m in (1, 2, 3): agree with brute force")
print(run([1, 1, 1, 2, 2, 3]), run([0, 0, 1, 1, 1, 1, 2, 3, 3]))
