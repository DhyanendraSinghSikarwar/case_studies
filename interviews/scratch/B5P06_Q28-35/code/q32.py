import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class CycleError(Exception):
    pass


def from_array(arr):
    dummy = ListNode()
    tail = dummy
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def has_cycle(head):                 # Floyd, O(1) space
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False


def to_array(head):
    if has_cycle(head):              # fail loudly instead of looping forever
        raise CycleError("list has a cycle")
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def node_ids(head):
    if has_cycle(head):
        raise CycleError("list has a cycle")
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
    return out


def same_structure(a, b):
    """Compare two lists by values, node by node, with a step cap so a cycle cannot hang us."""
    steps = 0
    while a is not None and b is not None:
        if a.val != b.val:
            return False
        a, b = a.next, b.next
        steps += 1
        if steps > 10**6:
            raise CycleError("step cap hit while comparing")
    return a is None and b is None


def no_shared_nodes(a, b):
    return not (set(node_ids(a)) & set(node_ids(b)))


def check_in_place(fn, arr, *args, subset=False):
    """Run fn on a fresh list. The result must be built only from the input's own node objects."""
    head = from_array(arr)
    keep = []                                    # hold references so no input node is freed and its id reused
    n = head
    while n is not None and len(keep) < 10**6:
        keep.append(n)
        n = n.next
    before = [id(n) for n in keep]               # record id of every input node first
    result = fn(head, *args)
    after = node_ids(result)                     # raises CycleError if fn made a cycle
    assert len(set(after)) == len(after), "a node appears twice"
    ok = set(after) <= set(before) if subset else set(after) == set(before)
    return to_array(result), ok


# --- solutions under test ---
def reverse_in_place(head):
    prev = None
    while head is not None:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    return prev


def reverse_new_nodes(head):                     # right values, WRONG: builds new nodes
    out = None
    while head is not None:
        out = ListNode(head.val, out)
        head = head.next
    return out


def reverse_buggy_cycle(head):                   # a bug: forgets to cut the old head's link
    prev = None
    first = head
    while head is not None:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    first.next = prev                            # links the new tail back to the new head
    return prev


# 1. the example from the prompt
h = from_array([1, 2, 3])
ids = node_ids(h)
print('3 distinct nodes:', len(set(ids)) == 3, '| to_array:', to_array(h))
vals, ok = check_in_place(reverse_in_place, [1, 2, 3])
print('reverse in place   ->', vals, '| same node objects:', ok)
vals, ok = check_in_place(reverse_new_nodes, [1, 2, 3])
print('reverse new nodes  ->', vals, '| same node objects:', ok)
try:
    check_in_place(reverse_buggy_cycle, [1, 2, 3])
except CycleError as e:
    print('buggy reverse      -> reported:', e)

# 2. what each helper catches
assert same_structure(from_array([1, 2, 3]), from_array([1, 2, 3]))
assert not same_structure(from_array([1, 2, 3]), from_array([1, 2]))
assert not same_structure(from_array([1, 2]), from_array([1, 3]))
assert same_structure(None, None)
a = from_array([1, 2, 3]); b = from_array([9, 8])
assert no_shared_nodes(a, b)
b.next.next = a.next                             # b now shares a's tail
assert not no_shared_nodes(a, b)
print('same_structure and aliasing check: OK')

# a cycle fed to the structure compare hits the step cap instead of hanging
loop = from_array([1, 2, 3])
loop.next.next.next = loop
try:
    same_structure(loop, loop)
except CycleError as e:
    print('compare of cyclic lists:', e)

# 3. random cross-check against a Python-list brute force, using the whole harness
rng = random.Random(32)
for _ in range(500):
    arr = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]
    vals, ok = check_in_place(reverse_in_place, arr)
    assert vals == arr[::-1] and ok
    vals2, ok2 = check_in_place(reverse_new_nodes, arr)
    assert vals2 == arr[::-1]                    # values alone cannot tell the two apart
    assert ok2 == (len(arr) == 0)                # only the identity check can (empty list has no nodes)
print('500 random lists: in-place version passes everything; new-node version passes values, fails identity')

# 4. subset mode for deleting solutions
def drop_first(head):
    return head.next if head else None
vals, ok = check_in_place(drop_first, [5, 6, 7], subset=True)
print('drop_first subset check ->', vals, ok)
