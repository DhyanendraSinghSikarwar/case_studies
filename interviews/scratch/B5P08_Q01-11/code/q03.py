import random
from itertools import combinations

random.seed(3)

def can_attend(intervals):
    iv = sorted(intervals)                       # by start (then end)
    return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))

def can_attend_brute(intervals):
    # half-open [s, e): two meetings clash when each starts before the other ends
    return not any(a[0] < b[1] and b[0] < a[1] for a, b in combinations(intervals, 2))

assert can_attend([[0, 30], [5, 10], [15, 20]]) is False
assert can_attend([[7, 10], [2, 4]]) is True
assert can_attend([[1, 5], [5, 8]]) is True      # touching is fine for half-open
assert can_attend([]) is True
assert can_attend([[3, 4]]) is True
assert can_attend([[1, 4], [1, 4]]) is False     # duplicates clash
assert can_attend([[1, 10], [2, 3], [11, 12]]) is False   # sorted neighbours [1,10],[2,3] clash

for _ in range(3000):
    n = random.randint(0, 7)
    iv = []
    for _ in range(n):
        s = random.randint(0, 10)
        iv.append([s, random.randint(s + 1, 11)])
    assert can_attend(iv) == can_attend_brute(iv), iv
print('3000 random cases ok')

# why neighbours suffice: after sorting by start, if the meeting after i starts before end[i] we already clash;
# if no neighbour clashes then end[i] <= start[i+1] <= start[j] for every j > i, so ends are ordered too.
iv = sorted([[1, 4], [2, 3], [6, 7]])
print('sorted:', iv, '-> neighbour pair [1,4],[2,3] clashes:', iv[0][1] > iv[1][0])
# a classic bug: comparing with strict < treats touching meetings as clashes
wrong = lambda ivs: all(sorted(ivs)[i][1] < sorted(ivs)[i + 1][0] for i in range(len(ivs) - 1))
print('wrong strict check on [[1,5],[5,8]]:', wrong([[1, 5], [5, 8]]), '(should be True)')
