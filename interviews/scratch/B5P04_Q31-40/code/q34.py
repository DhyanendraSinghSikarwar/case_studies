import random


def exclusive_fast(n, logs):
    res, st, prev = [0] * n, [], 0
    for line in logs:
        i, kind, t = line.split(":")
        i, t = int(i), int(t)
        if kind == "start":
            if st:
                res[st[-1]] += t - prev      # time the caller ran before this call began
            st.append(i)
            prev = t
        else:
            res[st.pop()] += t - prev + 1    # the end unit t is included
            prev = t + 1
    return res


def exclusive_brute(n, logs):
    # reference: decide the owner of every single time unit
    res, st = [0] * n, []
    events = []
    for line in logs:
        i, kind, t = line.split(":")
        events.append((int(i), kind, int(t)))
    last_t = max(t for _, _, t in events)
    e = 0
    for unit in range(0, last_t + 1):
        while e < len(events) and events[e][1] == "start" and events[e][2] == unit:
            st.append(events[e][0]); e += 1
        if st:
            res[st[-1]] += 1                 # unit belongs to whoever is on top now
        while e < len(events) and events[e][1] == "end" and events[e][2] == unit:
            st.pop(); e += 1
    return res


def gen(rng):
    """Random valid log built from a call tree; also returns ground-truth owners."""
    n = rng.randint(1, 4)
    logs, owners, clock = [], [], [0]

    def run_units(f, k):
        owners.extend([f] * k)
        clock[0] += k

    def call(f, depth):
        logs.append(f"{f}:start:{clock[0]}")
        for _ in range(rng.randint(0, 2) if depth < 3 else 0):
            run_units(f, rng.randint(0, 3))
            call(rng.randrange(n), depth + 1)
        run_units(f, rng.randint(1, 3))
        logs.append(f"{f}:end:{clock[0] - 1}")

    call(rng.randrange(n), 0)
    truth = [owners.count(i) for i in range(n)]
    return n, logs, truth


# prompt examples
a = exclusive_fast(2, ['0:start:0', '1:start:2', '1:end:5', '0:end:6'])
b = exclusive_fast(1, ['0:start:0', '0:start:2', '0:end:5', '0:start:6', '0:end:6', '0:end:7'])
print(a, b)
assert a == [3, 4] and b == [8]
assert exclusive_brute(2, ['0:start:0', '1:start:2', '1:end:5', '0:end:6']) == [3, 4]
assert exclusive_brute(1, ['0:start:0', '0:start:2', '0:end:5', '0:start:6', '0:end:6', '0:end:7']) == [8]

# edge cases
assert exclusive_fast(1, ['0:start:0', '0:end:0']) == [1]                      # one unit
assert exclusive_fast(2, ['0:start:0', '1:start:0', '1:end:0', '0:end:0']) == [0, 1]                      # child owns the shared unit
assert exclusive_fast(3, ['0:start:5', '1:start:5', '2:start:5', '2:end:5', '1:end:5', '0:end:5']) == [0, 0, 1]
assert exclusive_fast(1, ['0:start:0', '0:end:3', '0:start:7', '0:end:9']) == [7]  # idle gap not counted

rng = random.Random(34)
for _ in range(1500):
    n, logs, truth = gen(rng)
    assert exclusive_fast(n, logs) == exclusive_brute(n, logs) == truth, (n, logs)
print("1500 seeded random call trees: stack == per-unit simulation == construction truth")
