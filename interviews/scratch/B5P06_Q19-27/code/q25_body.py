import sys

def merge(a, b):                         # stable: ties take a (the earlier part) first; returns (head, tail)
    dummy = tail = ListNode()
    while a and b:
        if b.val < a.val:
            tail.next = b; b = b.next
        else:
            tail.next = a; a = a.next
        tail = tail.next
    tail.next = a or b
    while tail.next:                     # walk to the true tail (needed by the bottom-up caller)
        tail = tail.next
    return dummy.next, tail

depth_seen = 0
def sort_top_down(head, depth=1):
    global depth_seen
    depth_seen = max(depth_seen, depth)
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next         # slow ends on the FIRST middle, so both halves shrink
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    right = slow.next
    slow.next = None                     # cut
    return merge(sort_top_down(head, depth + 1), sort_top_down(right, depth + 1))[0]

def split(head, size):                   # keep `size` nodes in head's part, return the rest
    for _ in range(size - 1):
        if head is None:
            break
        head = head.next
    if head is None:
        return None
    rest = head.next
    head.next = None
    return rest

def sort_bottom_up(head):
    n, p = 0, head
    while p:
        n += 1
        p = p.next
    dummy = ListNode(0, head)
    size = 1
    while size < n:
        prev, cur = dummy, dummy.next
        while cur:
            left = cur
            right = split(left, size)
            cur = split(right, size)     # split(None, size) is None
            h, t = merge(left, right)
            prev.next = h
            prev = t
        size *= 2
    return dummy.next

def run(fn, arr):
    head = from_array(arr)
    before = node_ids(head)
    res = fn(head)
    assert is_acyclic(res)
    order = sorted(range(len(arr)), key=lambda i: arr[i])      # Python's sort is stable
    assert node_ids(res) == [before[i] for i in order], "stable and in place"
    assert to_array(res) == sorted(arr)
    return to_array(res)

for arr in ([4, 2, 1, 3], [-1, 5, 3, 4, 0], [], [2, 2, 1, 1], [1]):
    assert run(sort_top_down, arr) == run(sort_bottom_up, arr)
    print(arr, "->", run(sort_bottom_up, arr))

random.seed(25)
for _ in range(600):
    arr = [random.randint(-5, 5) for _ in range(random.randint(0, 70))]   # many ties
    run(sort_top_down, arr); run(sort_bottom_up, arr)
for n in range(0, 9):                    # all 0/1/2 lists up to length 8
    for t in range(3 ** n):
        arr = [(t // 3 ** i) % 3 for i in range(n)]
        run(sort_bottom_up, arr); run(sort_top_down, arr)
print("cross-check ok")

big = [random.randint(0, 10**6) for _ in range(50000)]
depth_seen = 0
run(sort_top_down, big)
print("top-down recursion depth on 50000 nodes:", depth_seen, "(about log2 n + 1)")
run(sort_bottom_up, big)
print("bottom-up on 50000 nodes ok, no recursion")
print("default recursion limit:", sys.getrecursionlimit())
