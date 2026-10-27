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

import itertools
from collections import Counter

def brute(arr):                          # keep only values that occur exactly once
    c = Counter(arr)
    return [i for i, v in enumerate(arr) if c[v] == 1]

def remove_all_dups(head):
    dummy = ListNode(0, head)
    prev = dummy                         # last node known to be kept
    cur = head
    while cur:
        if cur.next and cur.next.val == cur.val:
            v = cur.val
            while cur and cur.val == v:  # skip the whole run
                cur = cur.next
            prev.next = cur              # prev stays; the next node is not yet judged
        else:
            prev = cur
            cur = cur.next
    return dummy.next

def keep_one(head):                      # contrast: keep first of each run (Q15)
    cur = head
    while cur and cur.next:
        if cur.next.val == cur.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head

def run(arr):
    head = from_array(arr)
    before = node_ids(head)
    res = remove_all_dups(head)
    assert is_acyclic(res)
    keep = brute(arr)
    assert node_ids(res) == [before[i] for i in keep], "same node objects, only singles"
    assert to_array(res) == [arr[i] for i in keep]
    return to_array(res)

for arr in ([1, 2, 3, 3, 4, 4, 5], [1, 1, 1, 2, 3], [1, 1], [1, 2, 3], []):
    print(arr, "->", run(arr))

# exhaustive: every sorted list of length 0..7 over values 0..3 (multisets)
count = 0
for n in range(8):
    for combo in itertools.combinations_with_replacement(range(4), n):
        run(list(combo)); count += 1
random.seed(24)
for _ in range(500):
    run(sorted(random.randint(-6, 6) for _ in range(random.randint(0, 40))))
print("cross-check ok, exhaustive lists:", count)

print("keep one copy  :", to_array(keep_one(from_array([1, 1, 1, 2, 3]))))
print("remove all dups:", to_array(remove_all_dups(from_array([1, 1, 1, 2, 3]))))
