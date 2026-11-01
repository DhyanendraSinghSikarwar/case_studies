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


def make(prefix_a, prefix_b, shared):
    """A = prefix_a + shared, B = prefix_b + the SAME shared node objects."""
    s_head, _ = from_array(shared)
    def with_prefix(prefix):
        dummy = tail = ListNode()
        for v in prefix:
            tail.next = ListNode(v)
            tail = tail.next
        tail.next = s_head
        return dummy.next
    return with_prefix(prefix_a), with_prefix(prefix_b), s_head

def length(h):
    n = 0
    while h:
        n += 1
        h = h.next
    return n

def brute(a, b):                       # O(m + n) time, O(m) space
    seen = set()
    while a:
        seen.add(a)                    # default hash is identity
        a = a.next
    while b:
        if b in seen:
            return b
        b = b.next
    return None

def by_length(a, b):                   # O(m + n) time, O(1) space
    m, n = length(a), length(b)
    while m > n:
        a = a.next; m -= 1             # skip the extra head of the longer list
    while n > m:
        b = b.next; n -= 1
    while a is not b:                  # same distance to the end: walk together
        a, b = a.next, b.next
    return a                           # the shared node, or None when both ran off

def switch(a, b, counter=None):        # O(m + n) time, O(1) space
    p, q = a, b
    while p is not q:
        p = p.next if p else b         # at the end (None), restart on the OTHER list
        q = q.next if q else a
        if counter is not None:
            counter[0] += 1
    return p

# the four examples
for pa, pb, sh, want in (([4, 1], [5, 6, 1], [8, 4, 5], 8), ([1, 9, 1], [3], [2, 4], 2),
                         ([2, 6, 4], [1, 5], [], None), ([], [], [7], 7)):
    a, b, s = make(pa, pb, sh)
    ia, ib = node_ids(a), node_ids(b)
    for f in (brute, by_length, switch):
        r = f(a, b)
        assert r is (s if sh else None)
        assert (r.val if r else None) == want
    assert node_ids(a) == ia and node_ids(b) == ib       # nothing modified
    print(pa, pb, sh, '->', want)

# exhaustive over small shapes; ALL values are 0, so a value comparison cannot tell nodes apart
cases = 0
for la in range(5):
    for lb in range(5):
        for ls in range(5):
            a, b, s = make([0] * la, [0] * lb, [0] * ls)
            for f in (brute, by_length, switch):
                assert f(a, b) is (s if ls else None), (la, lb, ls, f.__name__)
            cnt = [0]
            switch(a, b, cnt)
            if ls == 0:
                # equal lengths: they hit None together after m steps; else after m + n node steps plus the step onto None
                assert cnt[0] == (la if la == lb else la + lb + 1)
            cases += 1
print('exhaustive shapes ok:', cases)

# no shared tail but equal values: val comparison would say 'intersect', identity says None
a, _ = from_array([1, 2, 3]); b, _ = from_array([1, 2, 3])
assert switch(a, b) is None and brute(a, b) is None and by_length(a, b) is None
print('equal values, different nodes -> None')

# seeded random cross-check (values drawn from 0..2 so they repeat)
random.seed(10)
for _ in range(500):
    pa = [random.randint(0, 2) for _ in range(random.randint(0, 8))]
    pb = [random.randint(0, 2) for _ in range(random.randint(0, 8))]
    sh = [random.randint(0, 2) for _ in range(random.randint(0, 6))]
    a, b, s = make(pa, pb, sh)
    ans = s if sh else None
    assert brute(a, b) is ans and by_length(a, b) is ans and switch(a, b) is ans
print('random cross-check ok (500 cases)')
