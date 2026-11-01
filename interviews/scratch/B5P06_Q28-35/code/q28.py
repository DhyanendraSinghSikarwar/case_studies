import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def from_array(arr):
    dummy = ListNode()
    tail = dummy
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def nodes_of(head, cap=100000):
    out = []
    while head is not None:
        out.append(head)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def to_array(head):
    return [n.val for n in nodes_of(head)]


# Brute force: copy the nodes into a Python list, sort (Python's sort is stable), relink.
def sort_brute(head):
    nodes = sorted(nodes_of(head), key=lambda n: n.val)
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes:
        nodes[-1].next = None
    return nodes[0] if nodes else None


# Optimal: insertion sort with a dummy head. stats counts value comparisons.
def insertion_sort(head, shortcut=True, stats=None):
    dummy = ListNode()          # sorted part hangs behind this
    tail = None                 # last node of the sorted part
    cur = head
    while cur is not None:
        nxt = cur.next          # save before we relink cur
        if shortcut and tail is not None:
            if stats is not None:
                stats[0] += 1
            if tail.val <= cur.val:   # belongs at the very end: no walk
                tail.next = cur
                cur.next = None
                tail = cur
                cur = nxt
                continue
        p = dummy
        while p.next is not None:
            if stats is not None:
                stats[0] += 1
            if p.next.val <= cur.val:     # <= keeps equal values in original order (stable)
                p = p.next
            else:
                break
        cur.next = p.next
        p.next = cur
        if cur.next is None:
            tail = cur
        cur = nxt
    return dummy.next


# examples from the prompt
for arr, exp in [([4, 2, 1, 3], [1, 2, 3, 4]), ([-1, 5, 3, 4, 0], [-1, 0, 3, 4, 5]),
                 ([], []), ([2, 2, 1], [1, 2, 2]), ([1, 2, 3], [1, 2, 3])]:
    h = from_array(arr)
    before = nodes_of(h)
    r = insertion_sort(h)
    assert to_array(r) == exp
    assert {id(n) for n in nodes_of(r)} == {id(n) for n in before}   # same node objects
    print(arr, '->', to_array(r))

# stability by identity: tag equal values with their original position
h = from_array([2, 2, 1, 1])
orig = nodes_of(h)
r = insertion_sort(h)
got = nodes_of(r)
assert got == [orig[2], orig[3], orig[0], orig[1]]
print('stable by identity: True')

# seeded randomised cross-check against the brute force, including node identity order
rng = random.Random(28)
for _ in range(500):
    arr = [rng.randint(-4, 4) for _ in range(rng.randint(0, 12))]
    for sc in (True, False):
        h1 = from_array(arr)
        n1 = nodes_of(h1)
        r1 = insertion_sort(h1, shortcut=sc)
        h2 = from_array(arr)
        n2 = nodes_of(h2)
        r2 = sort_brute(h2)
        pos1 = {id(n): i for i, n in enumerate(n1)}
        pos2 = {id(n): i for i, n in enumerate(n2)}
        assert [pos1[id(n)] for n in nodes_of(r1)] == [pos2[id(n)] for n in nodes_of(r2)]
        assert to_array(r1) == sorted(arr)
print('500 random lists, both variants match brute force by identity order')

# cost counts on n = 200
n = 200
for name, arr in [('sorted', list(range(n))), ('reversed', list(range(n, 0, -1))), ('max-first', [n] + list(range(1, n)))]:
    for sc in (True, False):
        st = [0]
        insertion_sort(from_array(arr), shortcut=sc, stats=st)
        print(f'{name:9} shortcut={sc!s:5} comparisons={st[0]}')

# bigger than the prompt limit still fine (iterative, no recursion)
big = list(range(1500, 0, -1))
assert to_array(insertion_sort(from_array(big))) == sorted(big)
print('reversed 1500 nodes sorted OK')
