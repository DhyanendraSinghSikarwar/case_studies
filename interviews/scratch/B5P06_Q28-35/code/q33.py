import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(arr, pos=-1):
    """List from an array; if pos != -1 the tail's next points back to the node at index pos."""
    dummy = ListNode()
    tail, nodes = dummy, []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos != -1:
        tail.next = nodes[pos]
    return dummy.next, nodes


# Brute force: remember the index at which each node was first seen. O(n) space.
def mu_lambda_brute(head):
    seen, i = {}, 0
    while head is not None:
        if head in seen:                      # node hash is identity
            return seen[head], i - seen[head]
        seen[head] = i
        head, i = head.next, i + 1
    return i, 0                               # no cycle: n nodes, lambda = 0


# Optimal: Floyd in three phases. moves[0] counts every `.next` step taken.
def mu_lambda_floyd(head, moves=None, info=None):
    m = [0] if moves is None else moves
    if head is None:
        return 0, 0
    slow = fast = head
    t = 0
    while fast is not None and fast.next is not None:     # phase 1: find a meeting point
        slow = slow.next
        fast = fast.next.next
        m[0] += 3                                          # one step for slow, two for fast
        t += 1
        if slow is fast:
            break
    else:                                                  # fast fell off the end: no cycle
        n = 0
        while head is not None:                            # count the nodes
            head = head.next
            n += 1
            m[0] += 1
        return n, 0
    if info is not None:
        info['t'] = t
    lam, p = 1, slow.next                                  # phase 2: walk once around the cycle
    m[0] += 1
    while p is not slow:
        p = p.next
        lam += 1
        m[0] += 1
    mu, a, b = 0, head, slow                               # phase 3: restart one pointer at the head
    while a is not b:
        a, b = a.next, b.next
        mu += 1
        m[0] += 2
    return mu, lam


def expected(n, pos):
    return (pos, n - pos) if pos != -1 else (n, 0)


# examples from the prompt
for arr, pos, exp in [([3, 2, 0, -4], 1, (1, 3)), ([1, 2], 0, (0, 2)), ([1], -1, (1, 0)),
                      ([1, 2, 3], 2, (2, 1)), ([], -1, (0, 0))]:
    h, _ = build(arr, pos)
    got = mu_lambda_floyd(h)
    assert got == mu_lambda_brute(h) == exp == expected(len(arr), pos), (arr, pos, got)
    print(arr, 'pos =', pos, '->', got)

# exhaustive check over mu in 0..30, lambda in 1..30: results, meeting time t and the move count
worst_gap = 0
for mu in range(0, 31):
    for lam in range(1, 31):
        h, _ = build(list(range(mu + lam)), mu)
        m, info = [0], {}
        assert mu_lambda_floyd(h, m, info) == (mu, lam) == mu_lambda_brute(h)
        t = info['t']
        t_formula = max(1, -(-mu // lam)) * lam            # smallest positive multiple of lam that is >= mu
        assert t == t_formula and t <= mu + lam
        assert m[0] == 3 * t + lam + 2 * mu                # exact move count
        assert m[0] <= 5 * mu + 4 * lam                    # the stated bound
        worst_gap = max(worst_gap, (5 * mu + 4 * lam) - m[0])
print('900 (mu, lambda) pairs: t = smallest positive multiple of lambda >= mu, moves = 3t + lambda + 2mu <= 5mu + 4lambda')

# the bound is tight at mu = 0 and loose by at most this much elsewhere
h, _ = build(list(range(5)), 0)
m = [0]; mu_lambda_floyd(h, m)
print('mu = 0, lambda = 5: moves =', m[0], 'and 5mu + 4lambda =', 20)
h, _ = build(list(range(1 + 5)), 1)
m = [0]; mu_lambda_floyd(h, m)
print('mu = 1, lambda = 5: moves =', m[0], 'and 5mu + 4lambda =', 5 + 20)

# no-cycle lists: moves is about 3n/2 + n
for n in (0, 1, 2, 9, 10):
    h, _ = build(list(range(n)))
    m = [0]
    assert mu_lambda_floyd(h, m) == (n, 0)
    print('no cycle, n =', n, ': moves =', m[0])

# seeded random cross-check against the brute force
rng = random.Random(33)
for _ in range(1000):
    n = rng.randint(0, 40)
    pos = rng.randint(-1, n - 1) if n else -1
    h, _ = build([rng.randint(0, 3) for _ in range(n)], pos)     # repeated values on purpose
    assert mu_lambda_floyd(h) == mu_lambda_brute(h) == expected(n, pos)
print('1000 random lists (repeated values): Floyd = brute force = expected')
