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


def brute(arr, k):                     # on a Python list: reverse each full block of k
    out = []
    for i in range(0, len(arr), k):
        block = arr[i:i + k]
        out += block[::-1] if len(block) == k else block
    return out

def reverse_k_group(head, k):          # iterative: O(n) time, O(1) space
    dummy = ListNode(0, head)
    group_prev = dummy                 # last node of the already-finished part
    while True:
        kth = group_prev
        for _ in range(k):             # are there k nodes left?
            kth = kth.next
            if kth is None:
                return dummy.next      # fewer than k left: leave them as they are
        group_next = kth.next          # first node after this group
        prev, cur = group_next, group_prev.next      # start 'prev' at group_next so the tail reconnects
        for _ in range(k):             # reverse exactly k nodes
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        first = group_prev.next        # the old first node is now the group's tail
        group_prev.next = prev         # prev = old kth = new first node of the group
        group_prev = first

depth = [0, 0]                         # [current depth, max depth] for the recursive version
def reverse_k_group_rec(head, k):
    depth[0] += 1; depth[1] = max(depth[1], depth[0])
    node, count = head, 0
    while node and count < k:          # find the start of the next group
        node = node.next; count += 1
    if count < k:
        depth[0] -= 1
        return head                    # short tail: unchanged
    new_tail_next = reverse_k_group_rec(node, k)     # solve the rest first
    prev, cur = new_tail_next, head
    for _ in range(k):                 # reverse this group, ending on the solved rest
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    depth[0] -= 1
    return prev

def run(f, arr, k):
    head, nodes = from_array(arr)
    r = f(head, k)
    ids = node_ids(r)
    assert sorted(ids) == sorted(id(n) for n in nodes)      # same node objects, none lost, none repeated
    return to_array(r), ids

for arr, k, want in (([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]), ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),
                     ([1, 2, 3], 1, [1, 2, 3]), ([1, 2, 3, 4], 4, [4, 3, 2, 1])):
    for f in (reverse_k_group, reverse_k_group_rec):
        assert run(f, arr, k)[0] == want == brute(arr, k)
    print(arr, 'k =', k, '->', want)

# exhaustive: every length 1..14 and every k in 1..len, values all distinct
for n in range(1, 15):
    for k in range(1, n + 1):
        arr = list(range(n))
        depth[1] = 0
        a, ids_a = run(reverse_k_group, arr, k)
        b, _ = run(reverse_k_group_rec, arr, k)
        assert a == b == brute(arr, k)
        assert depth[1] <= n // k + 1                       # recursion depth ~ n / k
print('exhaustive n=1..14, all k ok')

# identity: the k nodes of a group are the same objects in reverse order
head, nodes = from_array(list(range(6)))
r = reverse_k_group(head, 3)
assert node_ids(r) == [id(n) for n in (nodes[2], nodes[1], nodes[0], nodes[5], nodes[4], nodes[3])]

# seeded random cross-check with repeated values
random.seed(13)
for _ in range(500):
    n = random.randint(1, 40); k = random.randint(1, n)
    arr = [random.randint(0, 3) for _ in range(n)]
    assert run(reverse_k_group, arr, k)[0] == brute(arr, k)
# max size, iterative only: no recursion trouble
arr = list(range(5000))
assert run(reverse_k_group, arr, 7)[0] == brute(arr, 7)
depth[1] = 0
assert run(reverse_k_group_rec, arr, 7)[0] == brute(arr, 7)
print('recursive depth for n=5000, k=7:', depth[1], '(about n/k =', 5000 // 7, ')')
print('random cross-check ok (500 cases + n=5000)')
# k = 1 makes the recursive depth n, so 5000 nodes overflow the default recursion limit of 1000
try:
    run(reverse_k_group_rec, arr, 1)
    print('unexpected: no error')
except RecursionError:
    print('recursive version, n=5000, k=1: RecursionError (depth ~ n / k = 5000)')
assert run(reverse_k_group, arr, 1)[0] == arr
