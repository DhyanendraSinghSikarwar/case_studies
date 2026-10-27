import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def brute(arr, left, right):           # slice reversal on a Python list
    return arr[:left - 1] + arr[left - 1:right][::-1] + arr[right:]

def reverse_between(head, left, right):    # one pass, O(1) space, in place
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):          # stop on the node just before position left
        before = before.next
    tail = before.next                 # the node at position left; it ends up at the END of the reversed part
    for _ in range(right - left):      # head insertion: move tail.next to the front of the part
        moved = tail.next
        tail.next = moved.next         # unlink moved
        moved.next = before.next       # put it in front of the reversed part
        before.next = moved
    return dummy.next

def reverse_between_values(head, a, b):
    """Variant: reverse from the node holding value a to the node holding value b (values distinct, a before b).
    Only the first step changes: find the positions by walking, then reuse the same function."""
    pos, left, right, p = 1, None, None, head
    while p:
        if p.val == a and left is None:
            left = pos
        if p.val == b:
            right = pos
            break
        p, pos = p.next, pos + 1
    return reverse_between(head, left, right)

def run(arr, left, right):
    head, nodes = from_array(arr)
    r = reverse_between(head, left, right)
    ids = node_ids(r)
    want_nodes = nodes[:left - 1] + nodes[left - 1:right][::-1] + nodes[right:]
    assert ids == [id(n) for n in want_nodes]           # same objects, exactly this order
    return to_array(r)

for arr, l, r, want in (([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5]), ([5], 1, 1, [5]), ([3, 5], 1, 2, [5, 3]),
                        ([1, 2, 3], 1, 3, [3, 2, 1]), ([1, 2, 3], 2, 2, [1, 2, 3])):
    assert run(arr, l, r) == want == brute(arr, l, r)
    print(arr, l, r, '->', want)

# exhaustive: every length 1..9 and every 1 <= left <= right <= len
count = 0
for n in range(1, 10):
    arr = list(range(10, 10 + n))
    for l in range(1, n + 1):
        for r in range(l, n + 1):
            assert run(arr, l, r) == brute(arr, l, r)
            count += 1
print('exhaustive (length, left, right) triples ok:', count)

# no-op when left == right: the very same list comes back
head, nodes = from_array([1, 2, 3])
assert reverse_between(head, 2, 2) is head and node_ids(head) == [id(n) for n in nodes]

# value variant: [1,2,3,4,5], from value 2 to value 4
head, _ = from_array([1, 2, 3, 4, 5])
assert to_array(reverse_between_values(head, 2, 4)) == [1, 4, 3, 2, 5]
random.seed(18)
for _ in range(300):
    n = random.randint(1, 30)
    arr = random.sample(range(100), n)
    i = random.randint(0, n - 1); j = random.randint(i, n - 1)
    head, _ = from_array(arr)
    assert to_array(reverse_between_values(head, arr[i], arr[j])) == brute(arr, i + 1, j + 1)
    l = random.randint(1, n); r = random.randint(l, n)
    dup = [random.randint(0, 3) for _ in range(n)]
    assert run(dup, l, r) == brute(dup, l, r)
print('value variant and random cross-check ok (300 cases)')
head, _ = from_array(list(range(500)))
assert to_array(reverse_between(head, 1, 500)) == list(range(499, -1, -1))
print('n = 500, whole list ok')
