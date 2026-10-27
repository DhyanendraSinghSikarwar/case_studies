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

# ---------- baseline: copy values to an array, O(n) space ----------
def is_pal_array(head):
    vals = to_list(head)
    return vals == vals[::-1]

# ---------- optimal: middle, reverse second half, compare, restore ----------
def is_pal(head):
    slow = fast = head
    while fast and fast.next:           # slow ends at the second middle (even) or the exact middle (odd)
        slow = slow.next
        fast = fast.next.next
    second = reverse(slow)              # reversed second half; for odd n it starts at the last node and ends at the middle
    p, q = head, second
    ok = True
    while q is not None:                # q covers n - n//2 nodes; for odd n the middle compares with itself
        if p.val != q.val:
            ok = False
            break
        p, q = p.next, q.next
    reverse(second)                     # restore: reverse the second half back (the first half still points at slow)
    return ok

def is_pal_no_restore(head):            # shows the damage of forgetting to restore
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    reverse(slow)
    return None

for arr, exp in [([1,2,2,1],True), ([1,2,3,2,1],True), ([1,2],False), ([1],True), ([1,0,0],False)]:
    head, nodes = build(arr)
    before = node_ids(head)
    assert is_pal(head) is is_pal_array(head) is exp
    assert node_ids(head) == before and to_list(head) == arr          # list unchanged, same node order
    print(arr, "->", exp)

head, _n = build([1, 2, 3, 2, 1])
is_pal_no_restore(head)
print("[1,2,3,2,1] after forgetting to restore, head onward:", to_list(head))

random.seed(7)
for _ in range(2000):
    n = random.randint(1, 12)
    half = [random.randint(0, 2) for _ in range(n // 2)]
    mid = [random.randint(0, 2)] if n % 2 else []
    arr = half + mid + (half[::-1] if random.random() < 0.7 else [random.randint(0, 2) for _ in half])
    head, nodes = build(arr)
    assert is_pal(head) is (arr == arr[::-1])
    assert [id(x) for x in nodes] == node_ids(head) and to_list(head) == arr
print("cross-check ok (2000 random lists, odd and even, input restored by identity)")

big = [i % 7 for i in range(50000)]
big = big + big[::-1]                   # length 100000 palindrome
head, nodes = build(big)
assert is_pal(head) and node_ids(head) == [id(x) for x in nodes]
print("palindrome of length", len(big), "ok, restored")
