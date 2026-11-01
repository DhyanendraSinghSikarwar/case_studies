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


def brute(arr):                          # on a Python list: swap values pairwise
    a = list(arr)
    for i in range(0, len(a) - 1, 2):
        a[i], a[i + 1] = a[i + 1], a[i]
    return a

def swap_iter(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a = prev.next
        b = a.next
        a.next = b.next                  # 1: a skips b, keeps the rest of the list
        b.next = a                       # 2: b points back at a
        prev.next = b                    # 3: the previous part now enters at b
        prev = a                         # a is the new tail of the finished part
    return dummy.next

def swap_rec(head):
    if head is None or head.next is None:
        return head
    b = head.next
    head.next = swap_rec(b.next)         # a points at the already-swapped rest
    b.next = head
    return b

def swap_values(head):                   # the WRONG answer for this question: moves values, not nodes
    p = head
    while p and p.next:
        p.val, p.next.val = p.next.val, p.val
        p = p.next.next
    return head

def wrong_order(head):                   # step 2 before step 1: loses the rest of the list
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(10):                  # step cap: the bug would loop forever
        if not (prev.next and prev.next.next):
            break
        a = prev.next
        b = a.next
        b.next = a                       # b's old next (the rest) is gone
        a.next = b.next                  # now a.next is b.next is a: a self-loop
        prev.next = b
        prev = a
    return dummy.next

def run(fn, arr):
    head = from_array(arr)
    before = node_ids(head)
    res = fn(head)
    assert is_acyclic(res)
    expect_ids = list(before)            # nodes must be the same objects, pairs swapped
    for i in range(0, len(expect_ids) - 1, 2):
        expect_ids[i], expect_ids[i + 1] = expect_ids[i + 1], expect_ids[i]
    assert node_ids(res) == expect_ids, "node objects did not move as required"
    return to_array(res)

# examples from the prompt
for arr in ([1, 2, 3, 4], [1, 2, 3], [1], [], [1, 2]):
    assert run(swap_iter, arr) == run(swap_rec, arr) == brute(arr)
    print(arr, "->", run(swap_iter, arr))

# exhaustive over lengths 0..10 plus 500 seeded random lists with repeated values
for n in range(11):
    arr = list(range(n))
    assert run(swap_iter, arr) == run(swap_rec, arr) == brute(arr)
random.seed(19)
for _ in range(500):
    arr = [random.randint(-3, 3) for _ in range(random.randint(0, 100))]
    assert run(swap_iter, arr) == run(swap_rec, arr) == brute(arr)
print("cross-check ok")

# value swapping gives the right values but fails the identity check
try:
    run(swap_values, [1, 2, 3, 4])
    print("value swap passed identity (unexpected)")
except AssertionError:
    print("value swap: right values, fails identity check")

# wrong assignment order creates a cycle (caught by the Floyd check, no hang)
h = wrong_order(from_array([1, 2, 3, 4]))
print("wrong order acyclic?", is_acyclic(h))
assert not is_acyclic(h)
