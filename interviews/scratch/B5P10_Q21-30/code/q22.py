import random, itertools

random.seed(22)

def kadane_pos(nums, restart_on_zero=False, update_on_smaller_l=True):
    """Kadane with the start index carried. Returns [best, l, r] with the tie rule smallest l, then smallest r.
    run = best sum of a subarray ENDING at i, start = its leftmost start."""
    best, bl, br = None, 0, 0
    run, start = 0, 0
    for i, x in enumerate(nums):
        if i == 0 or run < 0 or (restart_on_zero and run == 0):
            run, start = x, i            # restart: the old prefix cannot help (strictly hurts)
        else:
            run += x                     # run == 0 keeps the older start: same sum, smaller l
        if best is None or run > best or (update_on_smaller_l and run == best and start < bl):
            best, bl, br = run, start, i
    return [best, bl, br]

def brute(nums):
    """O(n^2): every subarray, key = (-sum, l, r)."""
    n = len(nums); cand = []
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += nums[r]; cand.append((-s, l, r))
    s, l, r = min(cand)
    return [-s, l, r]

for nums, exp in [([-2, 1, -3, 4, -1, 2, 1, -5, 4], [6, 3, 6]), ([0, 0, 0], [0, 0, 0]), ([3, -3, 3], [3, 0, 0]),
                  ([-5, -2, -9], [-2, 1, 1]), ([2, -2, 2, -2, 5], [5, 0, 4])]:
    assert kadane_pos(nums) == brute(nums) == exp, nums
    print('example', nums, '->', exp)

# hand table, first example
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
run, start, best = 0, 0, None
print('i  x  run start best[l,r]')
bl = br = 0
for i, x in enumerate(nums):
    if i == 0 or run < 0: run, start = x, i
    else: run += x
    if best is None or run > best or (run == best and start < bl): best, bl, br = run, start, i
    print(f'{i}  {x:2d}  {run:3d}  {start:3d}   {best} [{bl},{br}]')

# exhaustive: all lists of length 1..6 over -2..2
total = bad_zero = bad_strict = bad_main = 0
for n in range(1, 7):
    for t in itertools.product(range(-2, 3), repeat=n):
        l = list(t); want = brute(l); total += 1
        bad_main += kadane_pos(l) != want
        bad_zero += kadane_pos(l, restart_on_zero=True) != want
        bad_strict += kadane_pos(l, update_on_smaller_l=False) != want
print('exhaustive lists checked:', total)
print('main version wrong on', bad_main)
print('restart when run <= 0 wrong on', bad_zero)
print('update only on strictly greater sum (no smaller-l check) wrong on', bad_strict)
assert bad_main == 0 and total == 19530

# seeded random cross-check, longer lists
for _ in range(500):
    n = random.randint(1, 40); l = [random.randint(-6, 6) for _ in range(n)]
    assert kadane_pos(l) == brute(l)
print('500 random lists (len <= 40) agree with the O(n^2) enumeration')

# max size, runs in one pass
big = [random.randint(-10**4, 10**4) for _ in range(10**5)]
b = kadane_pos(big)
P = 0; s = sum(big[b[1]:b[2] + 1]); assert s == b[0]
print('n = 10^5 result', b)
assert kadane_pos([7]) == [7, 0, 0] and kadane_pos([-3]) == [-3, 0, 0]
print('edge asserts passed')
