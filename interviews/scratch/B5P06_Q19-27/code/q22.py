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


def brute(arr, k):                       # simulate k single right-rotations (small k only)
    a = list(arr)
    for _ in range(k):
        if a:
            a.insert(0, a.pop())
    return a

def rotate_right(head, k):
    if head is None or head.next is None:
        return head
    n, tail = 1, head
    while tail.next:                     # length and tail in one pass
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head                     # close the ring
    new_tail = head
    for _ in range(n - k - 1):           # new tail is the node at position n - k
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None                 # open the ring
    return new_head

def run(arr, k):
    head = from_array(arr)
    before = node_ids(head)
    res = rotate_right(head, k)
    assert is_acyclic(res)
    n = len(arr)
    s = (n - k % n) % n if n else 0      # rotation as a left shift of ids
    assert node_ids(res) == before[s:] + before[:s], "same nodes, rotated"
    return to_array(res)

for arr, k in (([1, 2, 3, 4, 5], 2), ([0, 1, 2], 4), ([1], 99), ([1, 2], 2), ([], 3), ([1, 2, 3], 2000000000)):
    print(arr, "k =", k, "->", run(arr, k))
    if k <= 100:
        assert run(arr, k) == brute(arr, k)
assert 2000000000 % 3 == 2

random.seed(22)
for _ in range(600):
    arr = [random.randint(-5, 5) for _ in range(random.randint(0, 25))]
    k = random.randint(0, 60)
    assert run(arr, k) == brute(arr, k)
for n in range(0, 9):                    # every k in 0..3n for each length
    for k in range(3 * n + 1):
        assert run(list(range(n)), k) == brute(list(range(n)), k)
big = list(range(500))
r = (2 * 10**9 + 7) % 500
assert run(big, 2 * 10**9 + 7) == big[-r:] + big[:-r]
print("cross-check ok")
