import random


def collide_brute(a):
    a = list(a)
    while True:
        for i in range(len(a) - 1):
            if a[i] > 0 and a[i + 1] < 0:
                x, y = a[i], a[i + 1]
                if abs(x) > abs(y):
                    del a[i + 1]
                elif abs(x) < abs(y):
                    del a[i]
                else:
                    del a[i:i + 2]
                break
        else:
            return a


def collide(asteroids):
    st = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and st and st[-1] > 0:
            if st[-1] < -a:
                st.pop()                             # the right-mover explodes, keep fighting
            elif st[-1] == -a:
                st.pop()                             # both explode
                alive = False
            else:
                alive = False                        # the left-mover explodes
        if alive:
            st.append(a)
    return st


examples = [([5, 10, -5], [5, 10]), ([8, -8], []), ([10, 2, -5], [10]),
            ([-2, -1, 1, 2], [-2, -1, 1, 2]), ([3, 5, -6, 2, -1, 4], [-6, 2, 4])]
for a, want in examples:
    got = collide(a)
    assert got == collide_brute(a) == want, (a, got)
    print(a, "->", got)

assert collide([]) == []
assert collide([7]) == [7] and collide([-7]) == [-7]
assert collide([1, 1, 1, -1]) == [1, 1]
assert collide([-3, -3]) == [-3, -3]
assert collide([5, 5, -5, -5]) == []
assert collide([1, 2, 3, -10]) == [-10]
assert collide(list(range(1, 10001)) + [-10001]) == [-10001]    # max-size chain of pops

rng = random.Random(26)
bothdie = 0
for _ in range(1500):
    a = [rng.choice([-1, 1]) * rng.randint(1, 5) for _ in range(rng.randint(0, 9))]
    r = collide(a)
    assert r == collide_brute(a), a
    bothdie += len(r) < len(a) and any(a[i] == -a[i + 1] for i in range(len(a) - 1))
print("random cross-check passed: 1500 lists, tie-explosions exercised:", bothdie > 0)
