import itertools

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
# ---------- O(n) space: set of node identities ----------
def has_cycle_set(head):
    seen = set()
    while head is not None:
        if head in seen:                # ListNode has no __eq__/__hash__, so this is identity
            return True
        seen.add(head)
        head = head.next
    return False

# ---------- WRONG: set of VALUES ----------
def has_cycle_values_wrong(head, limit=10**5):
    seen = set()
    steps = 0
    while head is not None and steps < limit:
        if head.val in seen:
            return True
        seen.add(head.val)
        head = head.next
        steps += 1
    return False

# ---------- O(1) space: Floyd tortoise and hare ----------
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                # compare identity, never values
            return True
    return False

for arr, pos, exp in [([3,2,0,-4],1,True), ([1,2],0,True), ([1],-1,False), ([1,1,1],-1,False), ([],-1,False)]:
    head, _n = build(arr, pos)
    assert has_cycle(head) is has_cycle_set(head) is exp
    print(arr, "pos =", pos, "->", has_cycle(head))
head, _n = build([1, 1, 1])
print("values-set on [1,1,1] (no cycle):", has_cycle_values_wrong(head), "<- wrong")
assert has_cycle_values_wrong(head) is True

# exhaustive: every length 0..9, every pos -1..n-1, small value alphabets (repeats included)
count = 0
for n in range(0, 10):
    for pos in range(-1, n):
        for vals in ([0] * n, list(range(n)), [i % 2 for i in range(n)]):
            head, _nodes = build(vals, pos)
            expect = pos != -1
            assert has_cycle(head) is has_cycle_set(head) is expect
            count += 1
print("exhaustive ok:", count, "lists (all lengths 0..9, all pos)")

# the gap closes by exactly 1 per step once both are inside the cycle, so fast cannot jump over slow
head, nodes = build(list(range(5)) + list(range(5, 12)), 5)      # mu = 5, lambda = 7
slow = fast = head
steps = 0
while True:
    slow, fast = slow.next, fast.next.next
    steps += 1
    if slow is fast:
        break
print("mu=5, lambda=7: slow and fast first meet after", steps, "steps")
