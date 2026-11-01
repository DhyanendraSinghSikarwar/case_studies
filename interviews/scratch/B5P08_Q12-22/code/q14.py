import random
import itertools

random.seed(14)

def gas_greedy(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                         # cannot get from start to i + 1
            start = i + 1                    # so no station in start..i works
            tank = 0
    return start

def completes(gas, cost, s):
    t = 0
    n = len(gas)
    for k in range(n):
        i = (s + k) % n
        t += gas[i] - cost[i]
        if t < 0:
            return False
    return True

def gas_brute(gas, cost):                    # O(n^2): try every start in order
    for s in range(len(gas)):
        if completes(gas, cost, s):
            return s
    return -1

cases = [
    ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
    ([2, 3, 4], [3, 4, 3], -1),
    ([1, 1], [1, 1], 0),
    ([5], [4], 0),
]
for gas, cost, exp in cases:
    assert gas_greedy(gas, cost) == gas_brute(gas, cost) == exp
    print('gas =', gas, 'cost =', cost, '->', gas_greedy(gas, cost))

# exhaustive: every gas and cost list with n 1..4 and values 0..3
total = multi = 0
for n in range(1, 5):
    for gas in itertools.product(range(4), repeat=n):
        for cost in itertools.product(range(4), repeat=n):
            g = gas_greedy(gas, cost)
            assert g == gas_brute(gas, cost), (gas, cost)
            total += 1
            if sum(completes(gas, cost, s) for s in range(n)) > 1:
                multi += 1
print('exhaustive ok:', total, 'inputs; with 2 or more valid starts:', multi)

for _ in range(2000):
    n = random.randint(1, 12)
    gas = [random.randint(0, 6) for _ in range(n)]
    cost = [random.randint(0, 6) for _ in range(n)]
    assert gas_greedy(gas, cost) == gas_brute(gas, cost)
print('random ok: 2000 inputs')

# fact 1: if a trip from s first fails at j, every station k in s..j also fails
facts = 0
for _ in range(3000):
    n = random.randint(2, 8)
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    for s in range(n):
        t = 0
        for k in range(n):
            i = (s + k) % n
            t += gas[i] - cost[i]
            if t < 0:
                # failure at offset k: stations s, s+1, ..., s+k (mod n) all fail
                for m in range(k + 1):
                    assert not completes(gas, cost, (s + m) % n)
                facts += 1
                break
print('fact 1 checked on', facts, 'failing starts')

# fact 2: sum(gas) >= sum(cost) implies some start exists
for _ in range(3000):
    n = random.randint(1, 8)
    gas = [random.randint(0, 5) for _ in range(n)]
    cost = [random.randint(0, 5) for _ in range(n)]
    if sum(gas) >= sum(cost):
        assert gas_brute(gas, cost) != -1
    else:
        assert gas_brute(gas, cost) == -1
print('fact 2 ok: total gas >= total cost iff a start exists')

# edge cases
assert gas_greedy([0], [0]) == 0
assert gas_greedy([0, 0, 5], [0, 0, 5]) == 0     # zero-cost legs
assert gas_greedy([3, 1, 1], [1, 2, 2]) == 0
assert gas_greedy([1, 1, 1, 10], [2, 2, 2, 2]) == 3
big_n = 10 ** 5
assert gas_greedy([1] * big_n, [1] * big_n) == 0
assert gas_greedy([0] * (big_n - 1) + [big_n], [1] * big_n) == big_n - 1
print('edge cases ok')
