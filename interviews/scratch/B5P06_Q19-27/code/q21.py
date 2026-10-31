import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def brute_ids(ids, vals, x):             # stable partition on Python lists
    idx = [i for i in range(len(vals)) if vals[i] < x] + [i for i in range(len(vals)) if vals[i] >= x]
    return [ids[i] for i in idx], [vals[i] for i in idx]

def partition(head, x):
    small_d = ListNode()
    large_d = ListNode()
    s, l = small_d, large_d
    while head:
        if head.val < x:
            s.next = head
            s = head
        else:
            l.next = head
            l = head
        head = head.next
    l.next = None                        # terminate: l may still point into the small part
    s.next = large_d.next                # join small chain to large chain
    return small_d.next

def partition_no_terminate(head, x):     # the classic bug: forgets l.next = None
    small_d = ListNode()
    large_d = ListNode()
    s, l = small_d, large_d
    while head:
        nxt = head.next
        if head.val < x:
            s.next = head
            s = head
        else:
            l.next = head
            l = head
        head = nxt
    s.next = large_d.next                # no l.next = None
    return small_d.next

def run(arr, x):
    head = from_array(arr)
    before = node_ids(head)
    res = partition(head, x)
    assert is_acyclic(res)
    ids, vals = brute_ids(before, arr, x)
    assert node_ids(res) == ids and to_array(res) == vals
    return to_array(res)

for arr, x in (([1, 4, 3, 2, 5, 2], 3), ([2, 1], 2), ([], 0), ([3, 3], 3), ([1, 2, 3], 4)):
    print(arr, "x =", x, "->", run(arr, x))

random.seed(21)
for _ in range(600):
    arr = [random.randint(-4, 6) for _ in range(random.randint(0, 40))]
    run(arr, random.randint(-5, 7))
for n in range(7):                       # all 0/1/2 lists up to length 6 with every x in 0..3
    for t in range(3 ** n):
        arr = [(t // 3 ** i) % 3 for i in range(n)]
        for x in range(4):
            run(arr, x)
print("cross-check ok")

h = partition_no_terminate(from_array([1, 4, 3, 2, 5, 2]), 3)
print("without l.next = None, acyclic?", is_acyclic(h))
assert not is_acyclic(h)
