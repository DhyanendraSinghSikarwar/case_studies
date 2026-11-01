import random

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
def reverse(head):
    prev = None
    while head is not None:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

# ---------- brute force: node array and two indices (O(n) space) ----------
def reorder_order_brute(nodes):
    order, i, j = [], 0, len(nodes) - 1
    while i <= j:
        order.append(nodes[i])
        if i != j:
            order.append(nodes[j])
        i += 1
        j -= 1
    return order

# ---------- optimal: middle, reverse second half, interleave ----------
def reorder(head):
    if head is None or head.next is None:
        return head
    slow = fast = head
    while fast.next and fast.next.next: # slow stops at the LAST node of the first half
        slow = slow.next
        fast = fast.next.next
    second = reverse(slow.next)         # second half starts after slow
    slow.next = None                    # the cut: first half has ceil(n/2) nodes
    first = head
    while second is not None:           # second half is never longer than the first
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next
    return head

for arr, exp in [([1,2,3,4],[1,4,2,3]), ([1,2,3,4,5],[1,5,2,4,3]), ([1],[1]), ([1,2],[1,2])]:
    head, nodes = build(arr)
    out = reorder(head)
    assert out is head and to_list(out) == exp
    assert node_ids(out) == [id(n) for n in reorder_order_brute(nodes)]
    print(arr, "->", to_list(out))

count = 0
for n in range(1, 61):                  # exhaustive over lengths, distinct values
    arr = list(range(n))
    head, nodes = build(arr)
    out = reorder(head)
    assert node_ids(out) == [id(x) for x in reorder_order_brute(nodes)]
    assert len(set(node_ids(out))) == n # no node lost or repeated, so no cycle either
    count += 1
print("exhaustive ok: lengths 1..60 (", count, "lists ), identity order matches the index pattern 0, n-1, 1, n-2, ...")

random.seed(9)
for _ in range(500):
    arr = [random.randint(0, 3) for _ in range(random.randint(1, 200))]   # repeats on purpose
    head, nodes = build(arr)
    out = reorder(head)
    assert node_ids(out) == [id(x) for x in reorder_order_brute(nodes)]
    assert to_list(out) == [x.val for x in reorder_order_brute(nodes)]
print("cross-check ok (500 random lists, repeated values, identity compared)")
head, nodes = build(list(range(50000)))
out = reorder(head)
assert node_ids(out) == [id(x) for x in reorder_order_brute(nodes)]
print("length 50000 ok")
