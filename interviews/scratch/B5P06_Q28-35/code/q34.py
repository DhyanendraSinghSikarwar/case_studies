import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(arr, pos=-1):
    dummy = ListNode()
    tail, nodes = dummy, []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos != -1:
        tail.next = nodes[pos]
    return dummy.next, nodes


# Brute force: a set of visited node objects; the node whose next is already visited is the one to cut. O(n) space.
def break_brute(head):
    seen, prev = set(), None
    while head is not None:
        if head in seen:
            prev.next = None
            return prev
        seen.add(head)
        prev, head = head, head.next
    return None


# Optimal: Floyd to find the cycle start, then walk the cycle to the node whose next is the start.
def break_floyd(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            break
    else:
        return None                       # no cycle
    start, p = head, slow
    while start is not p:                 # restart step: both meet at the cycle start
        start, p = start.next, p.next
    last = start
    while last.next is not start:         # self-loop: start.next is start, so the loop body never runs
        last = last.next
    last.next = None
    return last


def acyclic(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def run(fn, arr, pos):
    head, nodes = build(arr, pos)
    last = fn(head)
    idx = None if last is None else next(i for i, n in enumerate(nodes) if n is last)
    # walk with a cap so a failed cut cannot hang the test
    out, n = [], head
    while n is not None:
        out.append(n)
        n = n.next
        assert len(out) <= len(nodes), "still cyclic"
    assert acyclic(head)
    assert out == nodes                   # same node objects, same order, none created, none lost
    return idx, [x.val for x in out]


for arr, pos, exp in [([3, 2, 0, -4], 1, 3), ([1, 2], 0, 1), ([1, 2, 3], 2, 2), ([1], -1, None)]:
    for fn in (break_brute, break_floyd):
        idx, vals = run(fn, arr, pos)
        assert idx == exp and vals == arr
    print(arr, 'pos =', pos, '-> cut at index', exp, ', list', arr)

# the cut node is always the original tail; check it exhaustively and with repeated values
rng = random.Random(34)
count = 0
for n in range(0, 25):
    for pos in range(-1, n):
        if n == 0 and pos != -1:
            continue
        arr = [rng.randint(0, 2) for _ in range(n)]
        for fn in (break_brute, break_floyd):
            idx, vals = run(fn, arr, pos)
            assert idx == (n - 1 if pos != -1 else None) and vals == arr
        count += 1
print(count, 'exhaustive (n, pos) cases, n up to 24, repeated values: both match, cut index is always n - 1')
print('empty list ->', break_floyd(None))
