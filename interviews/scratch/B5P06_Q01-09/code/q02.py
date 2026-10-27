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
# ---------- brute force: collect nodes in a Python list, index into it ----------
def middle_brute(head, first=False):
    nodes = []
    while head is not None:
        nodes.append(head)
        head = head.next
    n = len(nodes)
    return nodes[(n - 1) // 2] if first else nodes[n // 2]

# ---------- optimal: slow moves 1, fast moves 2, one pass ----------
def middle(head):                       # SECOND middle on even length
    slow = fast = head
    while fast and fast.next:           # fast can still jump two
        slow = slow.next
        fast = fast.next.next
    return slow

def middle_first(head):                 # FIRST middle on even length
    slow = fast = head
    while fast.next and fast.next.next: # stop one step earlier
        slow = slow.next
        fast = fast.next.next
    return slow

for arr, exp in [([1,2,3,4,5],[3,4,5]), ([1,2,3,4,5,6],[4,5,6]), ([1],[1]), ([1,2],[2])]:
    head, nodes = build(arr)
    m = middle(head)
    assert m is nodes[len(arr) // 2]    # identity, not just value
    assert to_list(m) == exp
    print(arr, "->", to_list(m))

random.seed(2)
for _ in range(500):
    arr = [random.randint(0, 3) for _ in range(random.randint(1, 100))]   # many repeats on purpose
    head, nodes = build(arr)
    assert middle(head) is middle_brute(head) is nodes[len(arr) // 2]
    assert middle_first(head) is middle_brute(head, first=True) is nodes[(len(arr) - 1) // 2]
print("cross-check ok (500 random lists, identity checked, both variants)")
head, nodes = build([1, 2, 3, 4])
print("first middle of [1,2,3,4]:", to_list(middle_first(head)), "| second middle:", to_list(middle(head)))
