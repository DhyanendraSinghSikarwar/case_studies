import heapq
import random

random.seed(35)

def free_brute(schedule):
    """Unit-cell sweep: cell [t, t+1] is free if no busy interval covers it."""
    iv = [x for emp in schedule for x in emp]
    lo = min(s for s, e in iv); hi = max(e for s, e in iv)
    free = [not any(s <= t and t + 1 <= e for s, e in iv) for t in range(lo, hi)]
    out, t = [], 0
    while t < len(free):
        if free[t]:
            u = t
            while u < len(free) and free[u]:
                u += 1
            out.append([lo + t, lo + u]); t = u
        else:
            t += 1
    return out

def free_sort(schedule):
    iv = sorted(x for emp in schedule for x in emp)       # O(N log N), ignores that each list is already sorted
    out, end = [], iv[0][1]
    for s, e in iv[1:]:
        if s > end:
            out.append([end, s])
        end = max(end, e)
    return out

def free_heap(schedule):
    """k-way merge: heap holds (next start, employee, index). Employee index is unique, so the tuple never ties past it."""
    h = [(emp[0][0], i, 0) for i, emp in enumerate(schedule) if emp]
    heapq.heapify(h)
    out, end = [], None
    while h:
        s, i, j = heapq.heappop(h)
        e = schedule[i][j][1]
        if end is None:
            end = e
        else:
            if s > end:
                out.append([end, s])
            end = max(end, e)
        if j + 1 < len(schedule[i]):
            heapq.heappush(h, (schedule[i][j + 1][0], i, j + 1))
    return out

# ---- examples
ex = [
    ([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]], [[3, 4]]),
    ([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]], [[5, 6], [7, 9]]),
    ([[[1, 5]], [[5, 8]]], []),
    ([[[1, 2]]], []),
]
for sch, want in ex:
    assert free_sort(sch) == free_heap(sch) == free_brute(sch) == want, (sch, want)
    print(sch, '->', free_heap(sch))

# ---- tie-breaking: two employees start at the same time. (start, employee, index) is always orderable.
h = []
heapq.heappush(h, (1, 0, 0)); heapq.heappush(h, (1, 1, 0))
print('ties resolved by employee index:', heapq.heappop(h), heapq.heappop(h))
try:                                   # what goes wrong if the payload is an unorderable object
    h = []
    heapq.heappush(h, (1, {'emp': 0})); heapq.heappush(h, (1, {'emp': 1}))
except TypeError as e:
    print('TypeError on tied start with dict payload:', e)

# ---- random cross-check: valid schedule = per employee sorted, disjoint, start < end (touching allowed)
def rand_schedule():
    sch = []
    for _ in range(random.randint(1, 4)):
        t, emp = random.randint(0, 3), []
        for _ in range(random.randint(0, 3)):
            s = t + random.randint(0, 3); e = s + random.randint(1, 4)
            emp.append([s, e]); t = e + random.randint(0, 2)     # 0 gap = touching intervals inside one employee
        sch.append(emp)
    return sch if any(sch) else [[[0, 1]]]
for _ in range(1500):
    sch = rand_schedule()
    assert free_sort(sch) == free_heap(sch) == free_brute(sch), sch
print('1500 random schedules agree (sort, heap, unit-cell brute force)')

# ---- edge asserts
assert free_heap([[[1, 4]], [[2, 3]]]) == []                         # nested
assert free_heap([[[1, 2]], [[3, 4]], [[5, 6]]]) == [[2, 3], [4, 5]]
assert free_heap([[], [[1, 2], [4, 5]]]) == [[2, 4]]                 # an employee with no busy time
assert free_heap([[[1, 2], [2, 3]]]) == []                           # touching inside one employee
# size: 50 employees x 50 intervals
big = [[[100 * j + 10 * i, 100 * j + 10 * i + 5] for j in range(50)] for i in range(50)]
assert free_heap(big) == free_sort(big) == free_brute(big)
print('50x50 intervals gaps:', len(free_heap(big)), 'same as sort version:', free_heap(big) == free_sort(big))
