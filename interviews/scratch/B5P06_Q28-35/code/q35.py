import random


class Node:
    __slots__ = ('val', 'next', 'random')

    def __init__(self, val):
        self.val, self.next, self.random = val, None, None


def build(spec):
    """spec: list of [val, random_index or None]. Returns (head, nodes)."""
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r is not None:
            nodes[i].random = nodes[r]
    return (nodes[0] if nodes else None), nodes


def spec_of(head):
    """Read a list back as [val, random_index]; fails loudly on a cycle or a random pointing outside the list."""
    nodes, p = [], head
    while p is not None:
        nodes.append(p)
        p = p.next
        assert len(nodes) < 10**5, "cycle"
    ix = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, None if n.random is None else ix[id(n.random)]] for n in nodes]


def chain(head):
    out, p = [], head
    while p is not None:
        out.append(p)
        p = p.next
        assert len(out) < 10**5, "cycle"
    return out


# Brute force: dict original -> copy, two passes. O(n) extra space. Keyed by node object (identity), not by value.
def copy_map(head):
    m = {None: None}
    p = head
    while p is not None:
        m[p] = Node(p.val)
        p = p.next
    p = head
    while p is not None:
        m[p].next = m[p.next]
        m[p].random = m[p.random]
        p = p.next
    return m[head]


# Optimal: interleave, set randoms, unweave. Extra space O(1) apart from the output nodes.
def copy_o1(head):
    if head is None:
        return None
    p = head                                   # step 1: A -> A' -> B -> B' -> ...
    while p is not None:
        c = Node(p.val)
        c.next = p.next
        p.next = c
        p = c.next
    p = head                                   # step 2: copy.random = original.random.next
    while p is not None:
        c = p.next
        c.random = p.random.next if p.random is not None else None
        p = c.next
    new_head = head.next                       # step 3: unweave and restore the input
    p = head
    while p is not None:
        c = p.next
        p.next = c.next                        # original links skip the copy
        c.next = c.next.next if c.next is not None else None   # copy links skip the original
        p = p.next
    return new_head


def check(fn, spec):
    head, nodes = build(spec)
    before_chain = chain(head)
    before_rand = [n.random for n in nodes]
    res = fn(head)
    # the copy has equal structure
    assert spec_of(res) == spec, (spec_of(res), spec)
    # no node of the copy is an original node, and the copy has its own nodes
    cp = chain(res)
    assert len(cp) == len(nodes) and not ({id(n) for n in cp} & {id(n) for n in nodes})
    for n in cp:
        assert n.random is None or any(n.random is m for m in cp)     # randoms point inside the copy
    # the input is restored exactly: same nodes, same order, same randoms
    assert chain(head) == before_chain and all(a is b for a, b in zip(chain(head), nodes))
    assert all(a is b for a, b in zip([n.random for n in nodes], before_rand))
    assert not nodes or nodes[-1].next is None
    assert spec_of(head) == spec
    return cp


examples = [
    [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
    [[1, 1], [2, 1]],
    [[5, 0]],
    [],
]
for spec in examples:
    for fn in (copy_map, copy_o1):
        check(fn, spec)
    head, _ = build(spec)
    print(spec, '-> copy', spec_of(copy_o1(head)), '| input after:', spec_of(head))

# a copy of the self-pointing node points at itself, not at the original
head, nodes = build([[5, 0]])
cp = copy_o1(head)
assert cp.random is cp and cp is not nodes[0] and nodes[0].random is nodes[0]
print('self random: copy.random is copy ->', cp.random is cp)

# seeded randomised cross-check, 800 random lists (including many repeated values)
rng = random.Random(35)
for _ in range(800):
    n = rng.randint(0, 12)
    spec = [[rng.randint(0, 3), rng.choice([None] + list(range(n)))] for _ in range(n)]
    check(copy_map, spec)
    check(copy_o1, spec)
print('800 random lists: map copy and O(1) copy both give equal structure, no shared nodes, input restored by identity')

# a long list: iterative, no recursion
spec = [[i, (i * 7) % 1000] for i in range(1000)]
check(copy_o1, spec)
print('1000 nodes OK')
