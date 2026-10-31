import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


class Node:
    __slots__ = ('val', 'next', 'random')
    def __init__(self, val=0, next=None, random=None):
        self.val, self.next, self.random = val, next, random

def build_random(spec):
    """spec = [[val, random_index_or_None], ...] -> (head, nodes)."""
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r is not None:
            nodes[i].random = nodes[r]
    return (nodes[0] if nodes else None), nodes

def chain(head, cap=10**5):
    out = []
    while head is not None:
        out.append(head)
        head = head.next
        assert len(out) <= cap, "cycle in next chain"
    return out

def to_spec(head):
    nodes = chain(head)
    index = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, None if n.random is None else index[id(n.random)]] for n in nodes]

def copy_brute(head):
    """O(n^2): find every random target by scanning for its position."""
    nodes = chain(head)
    copies = [Node(n.val) for n in nodes]
    for i, n in enumerate(nodes):
        if i + 1 < len(nodes):
            copies[i].next = copies[i + 1]
        if n.random is not None:
            j = 0
            while nodes[j] is not n.random:
                j += 1
            copies[i].random = copies[j]
    return copies[0] if copies else None

def copy_map(head):
    """O(n) time, O(n) space: dict original node -> copy (keyed by node identity)."""
    old_to_new = {None: None}          # maps None -> None so next/random of None need no branch
    cur = head
    while cur:                         # pass 1: create every copy
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                         # pass 2: wire next and random through the map
        new = old_to_new[cur]
        new.next = old_to_new[cur.next]
        new.random = old_to_new[cur.random]
        cur = cur.next
    return old_to_new[head]

def copy_by_value_WRONG(head):         # keyed by val: duplicate values collide
    by_val = {None: None}
    cur = head
    while cur:
        by_val[cur.val] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        new = by_val[cur.val]
        new.next = by_val[cur.next.val] if cur.next else None
        new.random = by_val[cur.random.val] if cur.random else None
        cur = cur.next
    return by_val[head.val] if head else None

def check_copy(spec, f):
    head, nodes = build_random(spec)
    before = [id(n) for n in chain(head)]
    c = f(head)
    assert to_spec(c) == spec, (spec, to_spec(c))                  # same structure
    assert {id(n) for n in chain(c)}.isdisjoint(before)             # no node of the copy is an original
    for n in chain(c):                                              # random targets are copies too
        assert n.random is None or id(n.random) in {id(x) for x in chain(c)}
    assert [id(n) for n in chain(head)] == before and to_spec(head) == spec   # input untouched

examples = [[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]], [[1, 1], [2, 1]], []]
for spec in examples:
    for f in (copy_brute, copy_map):
        check_copy(spec, f)
    print(spec, '-> copy has the same structure, no shared nodes')

# a value-keyed map breaks on repeated values
spec = [[1, 1], [1, 0]]
head, _ = build_random(spec)
print('value-keyed copy of', spec, 'gives', to_spec(copy_by_value_WRONG(head)) if head else None, '(wrong)')
assert to_spec(copy_by_value_WRONG(head)) != spec

# seeded random cross-check, values repeat on purpose
random.seed(11)
for _ in range(400):
    n = random.randint(0, 12)
    spec = [[random.randint(0, 3), random.choice([None] + list(range(n)))] for _ in range(n)]
    for f in (copy_brute, copy_map):
        check_copy(spec, f)
big = [[0, (i * 7) % 1000] for i in range(1000)]                    # max size
check_copy(big, copy_map)
print('random cross-check ok (400 cases + n=1000)')
