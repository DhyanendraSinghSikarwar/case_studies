import random

def brute(nums):
    # exact definition on the functional graph i -> (i + nums[i]) % n
    n = len(nums)
    nxt = [(i + nums[i]) % n for i in range(n)]
    for start in range(n):
        seen = {}
        cur, step = start, 0
        while cur not in seen:
            seen[cur] = step; cur = nxt[cur]; step += 1
        cyc = [c for c, st in seen.items() if st >= seen[cur]]      # nodes on the cycle reached from start
        if len(cyc) > 1 and (all(nums[c] > 0 for c in cyc) or all(nums[c] < 0 for c in cyc)):
            return True
    return False

def circular_loop(nums_in):
    nums = list(nums_in)                         # we mark visited with 0, so work on a copy
    n = len(nums)
    def step(i):
        return (i + nums[i]) % n
    for s in range(n):
        if nums[s] == 0: continue
        direction = nums[s] > 0
        slow = fast = s
        while True:
            ns = step(slow)
            if nums[ns] == 0 or (nums[ns] > 0) != direction: break
            nf = step(fast)
            if nums[nf] == 0 or (nums[nf] > 0) != direction: break
            nf2 = step(nf)
            if nums[nf2] == 0 or (nums[nf2] > 0) != direction: break
            slow, fast = ns, nf2
            if slow == fast:
                if step(slow) == slow: break     # self-loop, length 1: not a cycle
                return True
        i = s                                    # abandon: zero out the whole dead path
        while nums[i] != 0 and (nums[i] > 0) == direction:
            nxt = step(i); nums[i] = 0; i = nxt
    return False

for a, exp in [([2, -1, 1, 2, 2], True), ([-1, -2, -3, -4, -5, 6], False), ([1, -1, 5, 1, 4], True)]:
    assert circular_loop(a) == brute(a) == exp
    print(a, "->", circular_loop(a))
assert circular_loop([1]) is False and circular_loop([-1, -1]) is True and circular_loop([2, 2]) is False
assert circular_loop([1, -1]) is False and circular_loop([3, 1, 2]) is True and circular_loop([-2, 1, -1, -2, -2]) is False
data = [2, -1, 1, 2, 2]; circular_loop(data); assert data == [2, -1, 1, 2, 2]   # input not mutated
random.seed(44)
for _ in range(4000):
    n = random.randint(1, 8)
    a = [random.choice([-1, 1]) * random.randint(1, 9) for _ in range(n)]
    assert circular_loop(a) == brute(a), a
print("4000 seeded cases match the functional-graph brute force; edges pass")
