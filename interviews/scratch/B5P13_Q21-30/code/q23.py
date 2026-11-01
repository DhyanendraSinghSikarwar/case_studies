import random

random.seed(2301)
STOPS = 1001   # stops 0..1000

def car_pool(capacity, trips, stops=STOPS):
    d = [0] * (stops + 1)
    for p, a, b in trips:
        d[a] += p            # board at a
        d[b] -= p            # alight at b (not counted at b)
    load = peak = first = 0
    for x in range(stops):
        load += d[x]
        if load > peak:      # strict: keeps the SMALLEST stop of the max
            peak, first = load, x
    return [peak <= capacity, peak, first]

def brute(capacity, trips, stops=STOPS):
    loads = [sum(p for p, a, b in trips if a <= x < b) for x in range(stops)]
    peak = max(loads)
    return [all(l <= capacity for l in loads), peak, loads.index(peak)]

examples = [(4, [[2, 1, 5], [3, 3, 7]], [False, 5, 3]),
            (5, [[2, 1, 5], [3, 3, 7]], [True, 5, 3]),
            (3, [[2, 1, 5], [3, 5, 7]], [True, 3, 5])]
for cap, trips, want in examples:
    assert car_pool(cap, trips) == want == brute(cap, trips)
    print(cap, trips, '->', car_pool(cap, trips))

# dry run: difference array and running sum for example 1 (stops 0..7)
d = [0] * 8
for p, a, b in [[2, 1, 5], [3, 3, 7]]:
    d[a] += p; d[b] -= p
load, row = 0, []
for x in range(8):
    load += d[x]; row.append(load)
print('diff array :', d)
print('load by stop:', row)

# seeded random cross-check
for _ in range(3000):
    trips = []
    for _ in range(random.randint(1, 8)):
        a = random.randint(0, 999); b = random.randint(a + 1, min(1000, a + random.randint(1, 30)))
        trips.append([random.randint(1, 100), a, b])
    cap = random.randint(1, 400)
    assert car_pool(cap, trips) == brute(cap, trips)
print('random cross-check ok: 3000 cases (stops 0..1000)')

# exhaustive on a tiny world: 4 stops, every multiset of up to 3 trips with 1..2 passengers
import itertools
all_trips = [[p, a, b] for p in (1, 2) for a in range(4) for b in range(a + 1, 4)]
count = 0
for r in (1, 2, 3):
    for trips in itertools.combinations_with_replacement(all_trips, r):
        for cap in (1, 2, 3, 5):
            assert car_pool(cap, list(trips), 4) == brute(cap, list(trips), 4)
            count += 1
print('exhaustive tiny-world ok:', count, 'cases')

# boundary: a trip ending at x and one starting at x never overlap at x
assert car_pool(2, [[2, 0, 5], [2, 5, 9]]) == [True, 2, 0]
# max end 1000 uses d[1000]; the last stop counted is 999 (end is exclusive)
assert car_pool(1, [[1, 0, 1000]]) == [True, 1, 0]
# max load: 1000 trips of 100 passengers all over 0..1000 -> 100000 = capacity bound
trips = [[100, 0, 1000]] * 1000
assert car_pool(10**5, trips) == [True, 100000, 0] and car_pool(99999, trips)[0] is False
# work: difference array does len(trips) + 1001 steps, the direct method len(trips) * 1001 checks
print('work: diff array', 1000 + 1001, 'steps vs direct', 1000 * 1001, 'trip-stop checks (counted from the formula)')
print('edge asserts ok')
