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
# ---------- two-pass: count, then walk ----------
def remove_nth_two_pass(head, n):
    length = 0
    p = head
    while p is not None:
        length += 1
        p = p.next
    dummy = ListNode(0, head)
    p = dummy
    for _ in range(length - n):         # stop on the node BEFORE the target
        p = p.next
    p.next = p.next.next
    return dummy.next

# ---------- one-pass: dummy + two pointers with a gap of n ----------
def remove_nth(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):                  # fast gets a head start of n nodes
        fast = fast.next
    while fast.next is not None:        # fast stops ON the last node, so slow stops BEFORE the target
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next

def check(fn, arr, n):
    head, nodes = build(arr)
    out = fn(head, n)
    removed = nodes[len(arr) - n]
    assert node_ids(out) == [id(x) for x in nodes if x is not removed]   # same objects minus one
    return to_list(out)

for arr, n, exp in [([1,2,3,4,5],2,[1,2,3,5]), ([1],1,[]), ([1,2],1,[1]), ([1,2],2,[2])]:
    assert check(remove_nth, arr, n) == check(remove_nth_two_pass, arr, n) == exp
    print(arr, "n =", n, "->", exp)

# exhaustive: every length 1..30, every n 1..len, all values equal (so only identity can tell nodes apart)
count = 0
for L in range(1, 31):
    for n in range(1, L + 1):
        arr = [7] * L
        assert check(remove_nth, arr, n) == check(remove_nth_two_pass, arr, n) == arr[:L - n] + arr[L - n + 1:]
        count += 1
print("exhaustive ok:", count, "(length, n) pairs")

random.seed(5)
for _ in range(500):
    L = random.randint(1, 30)
    arr = [random.randint(0, 9) for _ in range(L)]
    n = random.randint(1, L)
    assert check(remove_nth, arr, n) == arr[:L - n] + arr[L - n + 1:]
print("cross-check ok (500 random lists vs list slicing)")
