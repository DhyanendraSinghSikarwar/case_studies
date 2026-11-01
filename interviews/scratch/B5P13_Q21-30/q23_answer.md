### Q23 ⭐⭐ 🟡 Car pooling with a difference array. `capacity` is the number of seats (1 <= capacity <= 10^5) and `trips` has 1 to 1000 items [passengers, start, end] with 1 <= passengers <= 100 and 0 <= start < end <= 1000: those passengers board at stop `start` and leave at stop `end`; at a stop, people leaving get off before people boarding get on, so the load at stop x counts trips with start <= x < end. Return `[ok, peak, first_stop]`: `ok` is True if the load never exceeds `capacity`; `peak` is the largest load over all stops 0..1000; `first_stop` is the smallest stop at which that largest load occurs. Do it in O(len(trips) + 1001) with a difference array (`d[start] += p`, `d[end] -= p`) and a running sum, and explain why this beats checking every trip at every stop (O(trips * stops)). The Corporate Flight Bookings problem is the same trick with 1-indexed inclusive ranges. In the answer include a dry run on the first example and a seeded random cross-check of your solution against counting, for every stop, the trips that cover it on small inputs. Example: capacity=4, trips=[[2, 1, 5], [3, 3, 7]] -> [False, 5, 3]; capacity=5, trips=[[2, 1, 5], [3, 3, 7]] -> [True, 5, 3]; capacity=3, trips=[[2, 1, 5], [3, 5, 7]] -> [True, 3, 5].
**Asked at:** Prefix-sum and difference-array pattern guides (techinterview.org prefix-sum and difference-array posts, a LeetCode Discuss study guide on range questions, talentd.in prefix-sum topic lists; search snippets only, not opened)

**Pattern:** Difference array plus a running sum. Do range updates in O(1) each and read the result with one prefix pass.

**Say this first (1 line):** "Add p at the start stop, subtract p at the end stop, take a running sum over stops 0 to 1000: that is the load at each stop."

**Brute force:** For every stop x in 0..1000 and every trip, add the passengers if `start <= x < end`. O(trips * stops), up to 1000 * 1001 = 1,001,000 checks. It is the oracle in the cross-check.

**Optimal:**
- `d[start] += p` and `d[end] -= p`.
- `load += d[x]` for x = 0..1000; `load` is the number of passengers on board at x.
- Why it works: the running sum of `d` at x is the sum of all `+p` placed at or before x minus all `-p` placed at or before x. That is exactly the trips with `start <= x` that have not yet ended (`end > x`). This is the "leaving before boarding" rule: the `-p` at `end` is already applied when we read stop `end`.
- Track the peak with a strict `>`. Then `first_stop` stays at the smallest stop where the peak first appears. `ok` is `peak <= capacity`.
- `d` needs index up to 1000 (an `end` of 1000), so allocate 1001 or 1002 slots.

**Complexity:** Time O(T + S) with T trips and S = 1001 stops, at most 2001 steps. Space O(S). The brute force is O(T * S), about 10^6 checks for the maximum input. The difference array wins because each trip is touched twice instead of once per stop.

**Dry run:** capacity 4, trips `[2,1,5]` and `[3,3,7]`. `d` after both trips: `[0, 2, 0, 3, 0, -2, 0, -3]`. Running sum: `[0, 2, 2, 5, 5, 3, 3, 0]`. The peak is 5, first reached at stop 3. 5 > 4, so `ok` is False. Result `[False, 5, 3]`. The program prints both arrays.

**Code:**
```python
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
```

**Output (my run):**
```
4 [[2, 1, 5], [3, 3, 7]] -> [False, 5, 3]
5 [[2, 1, 5], [3, 3, 7]] -> [True, 5, 3]
3 [[2, 1, 5], [3, 5, 7]] -> [True, 3, 5]
diff array : [0, 2, 0, 3, 0, -2, 0, -3]
load by stop: [0, 2, 2, 5, 5, 3, 3, 0]
random cross-check ok: 3000 cases (stops 0..1000)
exhaustive tiny-world ok: 1816 cases
work: diff array 2001 steps vs direct 1001000 trip-stop checks (counted from the formula)
edge asserts ok
```

**Edge cases:**
- A trip ending at x and another starting at x never overlap: `[[2,0,5],[2,5,9]]` gives peak 2, not 4.
- The last valid stop is 999 for a trip with end 1000 (end is exclusive), and `d[1000]` must exist.
- Ties for the peak: report the smallest stop, which the strict `>` gives.
- Peak equal to capacity is fine (`<=`): example 2 returns True.
- Largest input: 1000 trips of 100 passengers over 0..1000 gives 100000, equal to the largest capacity.

**Follow-ups:**
- *Corporate Flight Bookings?* The same, but the ranges are 1-indexed and inclusive, so subtract at `last + 1` instead of at `end`.
- *Huge coordinates?* Sort the events (start, +p) and (end, -p) and sweep; O(T log T). Part 8 covers the interval version.
- *Many point queries after many updates?* Interleaved updates and queries need a Fenwick tree (Part 14).

**Common mistakes:**
- Subtracting at `end + 1`, which counts the passengers at the stop where they should already have left.
- Using `>=` for the peak and reporting the last stop of the peak instead of the first.
- Allocating only 1000 slots and crashing on `end = 1000`.
- Sorting or merging trips first. The difference array does not need sorted input.
