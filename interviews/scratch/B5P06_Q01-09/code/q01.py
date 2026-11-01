import random
import sys

class ListNode:
    __slots__ = ("val", "next")
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build(arr, pos=-1):
    """Build a list from an array; pos != -1 makes the tail point back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos != -1:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_list(head, cap=10**6):
    """Values from head onward; the cap stops an accidental cycle from hanging the test."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

# ---------- brute force: copy values out, build NEW nodes (not in place) ----------
def reverse_brute(head):
    vals = to_list(head)
    new_head = None
    for v in vals:                      # pushing each value on the front reverses the order
        new_head = ListNode(v, new_head)
    return new_head

# ---------- optimal 1: iterative three pointers ----------
def reverse_iter(head):
    prev, cur = None, head
    while cur is not None:
        nxt = cur.next                  # save the rest before we cut the link
        cur.next = prev                 # flip one link
        prev = cur                      # advance prev
        cur = nxt                       # advance cur
    return prev                         # prev is the old tail = new head

# ---------- optimal 2: recursive ----------
def reverse_rec(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_rec(head.next)   # reverses everything after head
    head.next.next = head               # the node after head now points back to head
    head.next = None                    # head becomes the tail
    return new_head

def check_inplace(fn, arr):
    head, nodes = build(arr)
    out = fn(head)
    assert to_list(out) == arr[::-1]
    assert node_ids(out) == [id(n) for n in reversed(nodes)]   # same objects, reversed order
    return to_list(out)

# ---- examples from the prompt ----
for arr, exp in [([1,2,3,4,5],[5,4,3,2,1]), ([1,2],[2,1]), ([7],[7]), ([],[])]:
    assert check_inplace(reverse_iter, arr) == exp
    assert check_inplace(reverse_rec, arr) == exp
    print(arr, "->", exp)

# ---- randomised cross-check (seeded) ----
random.seed(1)
for _ in range(500):
    arr = [random.randint(-5, 5) for _ in range(random.randint(0, 30))]
    head, _n = build(arr)
    assert to_list(reverse_brute(head)) == arr[::-1]       # brute is non-destructive
    assert check_inplace(reverse_iter, arr) == arr[::-1]
    assert check_inplace(reverse_rec, arr) == arr[::-1]
print("cross-check ok (500 random lists, identity checked)")

# ---- recursion depth: the prompt allows 5000 nodes ----
big, _n = build(list(range(5000)))
print("default recursion limit:", sys.getrecursionlimit())
try:
    reverse_rec(big)
    print("recursive on 5000 nodes: no error")
except RecursionError:
    print("recursive on 5000 nodes: RecursionError")
big, nodes = build(list(range(5000)))                      # fresh list (the failed call cut links)
out = reverse_iter(big)
assert to_list(out) == list(range(4999, -1, -1))
print("iterative on 5000 nodes: ok")
old = sys.getrecursionlimit()
sys.setrecursionlimit(20000)
big, nodes = build(list(range(5000)))
assert to_list(reverse_rec(big)) == list(range(4999, -1, -1))
sys.setrecursionlimit(old)
print("recursive on 5000 nodes with the limit raised to 20000: ok")
