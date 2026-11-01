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


def to_int(head):
    v = 0
    for d in to_array(head):
        v = v * 10 + d
    return v

def digits(n):
    return [int(c) for c in str(n)]

def rev(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

def add_stacks(a, b):                    # inputs are only read
    sa, sb = [], []
    while a:
        sa.append(a.val)
        a = a.next
    while b:
        sb.append(b.val)
        b = b.next
    result, carry = None, 0
    while sa or sb or carry:
        s = carry + (sa.pop() if sa else 0) + (sb.pop() if sb else 0)
        carry, d = divmod(s, 10)
        result = ListNode(d, result)     # head insertion: new node in front
    return result

def add_reverse(a, b, restore=True):     # reverse both, add LSD first, reverse the sum
    ra, rb = rev(a), rev(b)
    dummy = tail = ListNode()
    carry = 0
    p, q = ra, rb
    while p or q or carry:
        s = carry + (p.val if p else 0) + (q.val if q else 0)
        carry, d = divmod(s, 10)
        tail.next = ListNode(d)
        tail = tail.next
        p = p.next if p else None
        q = q.next if q else None
    if restore:
        rev(ra)
        rev(rb)
    return rev(dummy.next)

def run(x, y, fn, **kw):
    a, b = from_array(digits(x)), from_array(digits(y))
    ia, ib = node_ids(a), node_ids(b)
    res = fn(a, b, **kw)
    assert is_acyclic(res)
    assert to_int(res) == x + y and to_array(res) == digits(x + y)
    assert node_ids(res) and not (set(node_ids(res)) & (set(ia) | set(ib))), "sum has its own nodes"
    assert node_ids(a) == ia and node_ids(b) == ib and to_array(a) == digits(x), "inputs restored"
    return to_array(res)

for arr1, arr2 in (([7, 2, 4, 3], [5, 6, 4]), ([2, 4, 3], [5, 6, 4]), ([0], [0]), ([9, 9], [1])):
    x, y = to_int(from_array(arr1)), to_int(from_array(arr2))
    r1, r2 = run(x, y, add_stacks), run(x, y, add_reverse)
    assert r1 == r2
    print(arr1, "+", arr2, "->", r1)

random.seed(23)
for _ in range(800):
    x = random.randint(0, 10 ** random.randint(0, 25))
    y = random.randint(0, 10 ** random.randint(0, 25))
    assert run(x, y, add_stacks) == run(x, y, add_reverse) == digits(x + y)
for x in range(0, 120):                  # all pairs below 120 (carry chains, 99 + 1, ...)
    for y in range(0, 120):
        assert run(x, y, add_stacks) == digits(x + y)
big = 10 ** 99 - 1
assert run(big, 1, add_stacks) == [1] + [0] * 99
print("cross-check ok")

# reverse-add-reverse WITHOUT restoring leaves the inputs reversed
a, b = from_array([7, 2, 4, 3]), from_array([5, 6, 4])
add_reverse(a, b, restore=False)
print("inputs after no-restore: a head now", a.val, "with next", a.next, "| a node is now the tail")
assert a.next is None
