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


def brute_ids(ids):                      # on a Python list: positions 1,3,5,... then 2,4,6,...
    return ids[0::2] + ids[1::2]

def odd_even(head):
    if head is None:
        return None
    odd = head
    even = head.next
    even_head = even
    while even and even.next:            # even runs ahead of odd, so test even
        odd.next = even.next             # odd skips over an even node
        odd = odd.next
        even.next = odd.next             # even skips over the new odd node
        even = even.next
    odd.next = even_head                 # join: odd tail -> even head
    return head

def odd_even_wrong(head):                # tests odd instead of even
    if head is None:
        return None
    odd = head
    even = head.next
    even_head = even
    while odd and odd.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next             # odd can be None here for even lengths
        even = even.next
    odd.next = even_head
    return head

def run(arr):
    head = from_array(arr)
    before = node_ids(head)
    res = odd_even(head)
    assert is_acyclic(res)
    assert node_ids(res) == brute_ids(before), "same nodes, odd positions then even positions"
    assert to_array(res) == arr[0::2] + arr[1::2]
    return to_array(res)

for arr in ([1, 2, 3, 4, 5], [2, 1, 3, 5, 6, 4, 7], [1], [1, 2], []):
    print(arr, "->", run(arr))

for n in range(0, 12):                   # every length 0..11
    run(list(range(n)))
random.seed(20)
for _ in range(500):
    run([random.randint(-5, 5) for _ in range(random.randint(0, 60))])
print("cross-check ok")

# testing odd instead of even breaks on even lengths
bad = []
for n in range(1, 9):
    try:
        odd_even_wrong(from_array(list(range(n))))
    except AttributeError:
        bad.append(n)
print("wrong loop condition raises for lengths:", bad)
assert bad == [2, 4, 6, 8]
