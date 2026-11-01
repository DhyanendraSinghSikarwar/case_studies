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

import heapq

def merge2(a, b):
    """Stable merge: on a tie the node from a comes first. Reuses nodes."""
    dummy = tail = ListNode()
    while a and b:
        if b.val < a.val:
            tail.next = b; b = b.next
        else:
            tail.next = a; a = a.next
        tail = tail.next
    tail.next = a or b
    return dummy.next

def merge_accumulate(lists):           # O(k * N): the result is re-walked on every merge
    result = None
    for head in lists:
        result = merge2(result, head)  # result first, so ties keep the lower list index first
    return result

def merge_heap(lists):                 # O(N log k)
    heap = [(h.val, i, h) for i, h in enumerate(lists) if h]
    heapq.heapify(heap)                # at most k entries: one node per list
    peak = len(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node; tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
        peak = max(peak, len(heap))
    tail.next = None
    merge_heap.peak = peak
    return dummy.next

def merge_dc(lists):                   # O(N log k): merge neighbours pairwise, round by round
    if not lists:
        return None
    while len(lists) > 1:
        lists = [merge2(lists[i], lists[i + 1]) if i + 1 < len(lists) else lists[i]
                 for i in range(0, len(lists), 2)]
    return lists[0]

def build_all(arrays):
    heads, all_nodes = [], []
    for arr in arrays:
        h, ns = from_array(arr)
        heads.append(h); all_nodes.append(ns)
    return heads, all_nodes

def expected_ids(all_nodes):
    """Stable order: by value, then list index, then position inside the list."""
    flat = [(n.val, li, pos, id(n)) for li, ns in enumerate(all_nodes) for pos, n in enumerate(ns)]
    return [t[3] for t in sorted(flat)]

# the four examples
for arrays, want in (([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]), ([], []), ([[]], []), ([[], [2], []], [2])):
    for f in (merge_accumulate, merge_heap, merge_dc):
        heads, ns = build_all(arrays)
        r = f(heads)
        assert to_array(r) == want, (f.__name__, arrays)
        assert node_ids(r) == expected_ids(ns)          # same nodes, stable order
    print(arrays, '->', want)

# ListNode objects cannot be compared, so a (val, node) heap entry breaks on a tie
a, b = ListNode(1), ListNode(1)
try:
    heapq.heappush([(1, a)], (1, b))
    raise SystemExit('expected TypeError')
except TypeError as e:
    print('without the list index:', e)

# seeded random cross-check on shapes with many ties
random.seed(12)
for _ in range(500):
    k = random.randint(0, 8)
    arrays = [sorted(random.randint(0, 5) for _ in range(random.randint(0, 6))) for _ in range(k)]
    want = sorted(v for arr in arrays for v in arr)
    for f in (merge_accumulate, merge_heap, merge_dc):
        heads, ns = build_all(arrays)
        r = f(heads)
        assert to_array(r) == want
        assert node_ids(r) == expected_ids(ns)
# the heap never holds more than k nodes
heads, _ = build_all([[i, i + 100, i + 200] for i in range(7)])
merge_heap(heads)
assert merge_heap.peak <= 7
print('heap peak size for k = 7:', merge_heap.peak)
# max-ish size: k = 100, N = 10^4
arrays = [sorted(random.randint(0, 50) for _ in range(100)) for _ in range(100)]
for f in (merge_accumulate, merge_heap, merge_dc):
    heads, ns = build_all(arrays)
    r = f(heads)
    assert node_ids(r) == expected_ids(ns) and len(node_ids(r)) == 10**4
print('random cross-check ok (500 cases + k=100, N=10^4)')
