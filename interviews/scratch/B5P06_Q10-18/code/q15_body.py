import itertools

def brute(arr):                        # first value of each run of a sorted array
    return [k for k, _ in itertools.groupby(arr)]

def dedup(head):                       # O(n) time, O(1) space, in place
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next   # delete the successor; stay on cur to look at the new successor
        else:
            cur = cur.next             # advance only when nothing was deleted
    return head

def run(arr):
    head, nodes = from_array(arr)
    r = dedup(head)
    ids = node_ids(r)
    assert len(set(ids)) == len(ids)
    # in place: the survivors are exactly the first node of each run, same objects, same order
    first_of_run = [nodes[i] for i in range(len(arr)) if i == 0 or arr[i] != arr[i - 1]]
    assert ids == [id(n) for n in first_of_run]
    assert r is (nodes[0] if nodes else None)          # the head never changes
    return to_array(r)

for arr, want in (([1, 1, 2], [1, 2]), ([1, 1, 2, 3, 3], [1, 2, 3]), ([5, 5, 5], [5]), ([], []), ([1, 2, 3], [1, 2, 3])):
    assert run(arr) == want == brute(arr)
    print(arr, '->', want)

# exhaustive: every sorted list over values 0..3 up to length 7
count = 0
for n in range(8):
    for arr in itertools.combinations_with_replacement(range(4), n):
        assert run(list(arr)) == brute(list(arr))
        count += 1
print('exhaustive sorted lists ok:', count)

# if you advanced after deleting you would skip a duplicate
def dedup_buggy(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next
        cur = cur.next                 # BUG: advances even after a delete
    return head
h, _ = from_array([5, 5, 5])
print('buggy version on [5, 5, 5]:', to_array(dedup_buggy(h)))

random.seed(15)
for _ in range(300):
    arr = sorted(random.randint(-5, 5) for _ in range(random.randint(0, 40)))
    assert run(arr) == brute(arr)
assert run([7] * 300) == [7]
print('random cross-check ok (300 cases + 300 equal values)')
