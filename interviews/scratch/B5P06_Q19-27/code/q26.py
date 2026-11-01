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

import sys

def rev_it(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

def rev_rec(head):
    if head is None or head.next is None:
        return head
    new_head = rev_rec(head.next)        # one frame per node on the way down
    head.next.next = head
    head.next = None
    return new_head

def length_rec(head):
    return 0 if head is None else 1 + length_rec(head.next)

def merge_rec(a, b):                     # recursive merge of two sorted lists
    if a is None: return b
    if b is None: return a
    if b.val < a.val:
        b.next = merge_rec(a, b.next); return b
    a.next = merge_rec(a.next, b); return a

def fails(fn, n):
    try:
        fn(from_array(list(range(n))))
        return False
    except RecursionError:
        return True

print("default recursion limit:", sys.getrecursionlimit())

# correctness first, with identity, on short lists
random.seed(26)
for _ in range(400):
    arr = [random.randint(-9, 9) for _ in range(random.randint(0, 60))]
    h = from_array(arr); before = node_ids(h)
    r1 = rev_rec(h)
    assert to_array(r1) == arr[::-1] and node_ids(r1) == before[::-1]
    h = from_array(arr); before = node_ids(h)
    r2 = rev_it(h)
    assert to_array(r2) == arr[::-1] and node_ids(r2) == before[::-1]
print("recursive reverse of [1,2,3,4,5] ->", to_array(rev_rec(from_array([1, 2, 3, 4, 5]))))
print("recursive reverse, 100 nodes works:", not fails(rev_rec, 100))
print("recursive reverse, 2000 nodes RecursionError:", fails(rev_rec, 2000))
big = from_array(list(range(100000)))
print("iterative reverse, 100000 nodes ok:", to_array(rev_it(big))[:3], "...")
print("iterative reverse, 2000 nodes ok:", to_array(rev_it(from_array(list(range(2000)))))[:3], "...")

# the same wall for other recursive list code (2000 nodes)
print("recursive length, 2000 nodes fails:", fails(length_rec, 2000))
print("recursive merge, 2000 vs 2000 fails:", end=" ")
try:
    merge_rec(from_array(list(range(0, 4000, 2))), from_array(list(range(1, 4000, 2))))
    print(False)
except RecursionError:
    print(True)

# a failed descent changes nothing: the mutation happens on the way back
h = from_array(list(range(2000)))
try:
    rev_rec(h)
except RecursionError:
    pass
print("list unchanged after the failed call:", to_array(h) == list(range(2000)))

# where the wall is (sandbox, Python 3.13, called from module level; varies with caller depth)
n = 900
while not fails(rev_rec, n):
    n += 1
print("smallest failing length here:", n, "(limit", sys.getrecursionlimit(), "minus frames already in use)")

# raising the limit works but is a risk to weigh
old = sys.getrecursionlimit()
sys.setrecursionlimit(10000)
print("limit 10000, 5000 nodes works:", not fails(rev_rec, 5000))
sys.setrecursionlimit(old)
print("limit restored to", sys.getrecursionlimit())
