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


def remove_with_dummy(head, val):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next     # delete; do not advance prev
        else:
            prev = prev.next
    return dummy.next

def remove_without_dummy(head, val):
    while head and head.val == val:        # special case: skip matching heads
        head = head.next
    cur = head
    while cur and cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head

def brute(arr, val):
    return [v for v in arr if v != val]

def run(f, arr, val):
    head, nodes = from_array(arr)
    r = f(head, val)
    ids = node_ids(r)
    kept = [id(n) for n in nodes if n.val != val]
    assert ids == kept                      # same node objects, same order, no new nodes
    return to_array(r)

for arr, val, want in (([1, 2, 6, 3, 4, 5, 6], 6, [1, 2, 3, 4, 5]), ([], 1, []), ([7, 7, 7], 7, []),
                       ([1, 2], 3, [1, 2]), ([6, 1], 6, [1])):
    for f in (remove_with_dummy, remove_without_dummy):
        assert run(f, arr, val) == want == brute(arr, val)
    print(arr, 'remove', val, '->', want)

random.seed(16)
for _ in range(500):
    arr = [random.randint(0, 3) for _ in range(random.randint(0, 20))]
    val = random.randint(0, 4)
    for f in (remove_with_dummy, remove_without_dummy):
        assert run(f, arr, val) == brute(arr, val)
assert run(remove_with_dummy, [9] * 10**4, 9) == [] and run(remove_without_dummy, [9] * 10**4, 9) == []
print('random cross-check ok (500 cases + 10^4 equal values)')
