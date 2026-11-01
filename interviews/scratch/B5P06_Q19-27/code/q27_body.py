
def brute_keep(arr):                     # indices of first occurrences
    seen, keep = set(), []
    for i, v in enumerate(arr):
        if v not in seen:
            seen.add(v)
            keep.append(i)
    return keep

def dedup_set(head):
    seen = set()
    prev = None
    cur = head
    while cur:
        if cur.val in seen:
            prev.next = cur.next         # unlink cur (prev exists: the head is never a repeat)
        else:
            seen.add(cur.val)
            prev = cur
        cur = cur.next
    return head

def dedup_n2(head):
    cur = head
    while cur:
        runner = cur                     # scan the rest, unlink later copies of cur.val
        while runner.next:
            if runner.next.val == cur.val:
                runner.next = runner.next.next
            else:
                runner = runner.next
        cur = cur.next
    return head

def run(fn, arr):
    head = from_array(arr)
    before = node_ids(head)
    res = fn(head)
    assert is_acyclic(res)
    keep = brute_keep(arr)
    assert node_ids(res) == [before[i] for i in keep], "first occurrences, same node objects"
    assert to_array(res) == [arr[i] for i in keep]
    return to_array(res)

for arr in ([1, 2, 1, 3, 2, 4], [5, 5, 5], [], [3, 1, 2], [2, 1, 2, 1]):
    assert run(dedup_set, arr) == run(dedup_n2, arr)
    print(arr, "->", run(dedup_set, arr))

random.seed(27)
for _ in range(800):
    arr = [random.randint(-4, 4) for _ in range(random.randint(0, 40))]
    assert run(dedup_set, arr) == run(dedup_n2, arr)
for n in range(0, 9):                    # all lists of length <= 8 over {0,1,2}
    for t in range(3 ** n):
        arr = [(t // 3 ** i) % 3 for i in range(n)]
        run(dedup_set, arr); run(dedup_n2, arr)
arr = [random.randint(0, 1000) for _ in range(2000)]
assert run(dedup_set, arr) == run(dedup_n2, arr)
print("cross-check ok")

# sorting first changes which order survives
arr = [2, 1, 2, 1]
print("first-occurrence order:", run(dedup_set, arr), "| sort first, then dedupe:", sorted(set(arr)))
