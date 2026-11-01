import random
from fractions import Fraction


def fleets_brute(target, position, speed):
    # real time of car i = max solo time over every car at or ahead of it
    n = len(position)
    solo = [Fraction(target - position[i], speed[i]) for i in range(n)]
    real = set()
    for i in range(n):
        real.add(max(solo[j] for j in range(n) if position[j] >= position[i]))
    return len(real)


def fleets_sim(target, position, speed):
    # exact time-grid simulation (small ints only): cars cannot pass, merge on touch
    n = len(position)
    order = sorted(range(n), key=lambda i: -position[i])        # front first
    pos = {i: Fraction(position[i]) for i in order}
    vel = {i: Fraction(speed[i]) for i in order}
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a

    road = list(order)
    dt = Fraction(1, 60)                                        # grid hits every catch-up time
    while road:
        newpos = {}
        prev = None
        for i in road:
            p = min(pos[i] + vel[i] * dt, Fraction(target))
            if prev is not None and p >= newpos[prev]:
                p = newpos[prev]
                vel[i] = vel[prev]
                parent[find(i)] = find(prev)
            newpos[i] = p
            prev = i
        pos.update(newpos)
        road = [i for i in road if pos[i] < target]
    return len({find(i) for i in range(n)})


def car_fleet(target, position, speed):
    stack = []                                                   # strictly increasing times
    for p, s in sorted(zip(position, speed), reverse=True):
        t = (target - p) / s
        if not stack or t > stack[-1]:
            stack.append(t)
    return len(stack)


examples = [(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3), (10, [3], [3], 1), (100, [0, 2, 4], [4, 2, 1], 1)]
for t, p, s, want in examples:
    got = car_fleet(t, p, s)
    assert got == fleets_brute(t, p, s) == fleets_sim(t, p, s) == want
    print((t, p, s), "->", got)

assert car_fleet(5, [], []) == 0
assert car_fleet(10, [0, 5], [1, 1]) == 2            # same speed, never meet
assert car_fleet(10, [0, 5], [5, 1]) == 1            # solo times 5.0 and 2.0: the rear car is faster and joins
assert car_fleet(10, [4, 0], [3, 6]) == 1            # solo times about 2.0 and 1.67: joins
assert car_fleet(10, [6, 0], [2, 5]) == 1            # times 2.0 and 2.0: exact tie joins
assert car_fleet(10, [6, 0], [2, 5]) == fleets_sim(10, [6, 0], [2, 5])

rng = random.Random(21)
trials = multi = 0
for _ in range(400):
    n = rng.randint(1, 6)
    target = rng.randint(2, 10)
    position = rng.sample(range(target), min(n, target))
    speed = [rng.randint(1, 5) for _ in position]
    a = car_fleet(target, position, speed)
    assert a == fleets_brute(target, position, speed) == fleets_sim(target, position, speed), (target, position, speed)
    trials += 1
    multi += a > 1
for _ in range(300):                                    # larger, brute only
    n = rng.randint(1, 60)
    target = rng.randint(n + 1, 500)
    position = rng.sample(range(target), n)
    speed = [rng.randint(1, 100) for _ in position]
    assert car_fleet(target, position, speed) == fleets_brute(target, position, speed)
    trials += 1
print("random cross-check passed:", trials, "cases;", multi, "of the small ones had 2+ fleets")
