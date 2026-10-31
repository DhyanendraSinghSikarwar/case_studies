import random
import sys


class MNode:
    __slots__ = ('val', 'prev', 'next', 'child')

    def __init__(self, val):
        self.val, self.prev, self.next, self.child = val, None, None, None


def build(nested):
    """Nested array -> head. A list item is the child list of the node just before it."""
    head, last = None, None
    for item in nested:
        if isinstance(item, list):
            assert last is not None, "a child list needs a parent node before it"
            last.child = build(item)
        else:
            n = MNode(item)
            if last is None:
                head = n
            else:
                last.next, n.prev = n, last
            last = n
    return head


def all_nodes(head, out=None):
    """Every node reachable via next and child (iterative, cap guards against cycles)."""
    out = [] if out is None else out
    stack = [head] if head else []
    while stack:
        n = stack.pop()
        while n is not None:
            out.append(n)
            assert len(out) < 10**5, "cycle"
            if n.child:
                stack.append(n.child)
            n = n.next
    return out


def flat_expected(nested):
    """Brute force on the nested array: depth-first, a child list goes right after its parent."""
    out = []
    for item in nested:
        out.extend(flat_expected(item) if isinstance(item, list) else [item])
    return out


def to_array(head):
    out, n, back_tail = [], head, None
    while n is not None:
        out.append(n.val)
        back_tail, n = n, n.next
        assert len(out) < 10**5, "cycle"
    return out, back_tail


def check_flat(head, expected_vals, original_ids):
    vals, tail = to_array(head)
    assert vals == expected_vals, (vals, expected_vals)
    # backward walk must mirror the forward walk, so every prev is right
    back, n = [], tail
    while n is not None:
        back.append(n.val)
        n = n.prev
        assert len(back) <= len(vals)
    assert back == vals[::-1]
    assert head is None or head.prev is None
    n = head
    while n is not None:
        assert n.child is None
        n = n.next
    ids = []
    n = head
    while n is not None:
        ids.append(id(n)); n = n.next
    assert set(ids) == original_ids and len(ids) == len(original_ids)   # same node objects, none lost, none new


def flatten_iter(head):
    cur = head
    while cur is not None:
        if cur.child is not None:
            child = cur.child
            tail = child
            while tail.next is not None:      # find the end of the child list
                tail = tail.next
            tail.next = cur.next              # child's tail -> old next
            if cur.next is not None:
                cur.next.prev = tail
            cur.next = child                  # cur -> child head
            child.prev = cur
            cur.child = None
        cur = cur.next                        # steps into the spliced child list if there was one
    return head


def flatten_rec(head):
    def go(node):                             # returns the tail of the flattened list starting at node
        cur, last = node, node
        while cur is not None:
            nxt = cur.next
            if cur.child is not None:
                child_tail = go(cur.child)
                cur.next, cur.child.prev = cur.child, cur
                cur.child = None
                if nxt is not None:
                    child_tail.next, nxt.prev = nxt, child_tail
                last = child_tail
            else:
                last = cur
            cur = nxt
        return last
    if head is not None:
        go(head)
    return head


examples = [
    ([1, 2, 3, [7, 8, [11, 12], 9], 4], [1, 2, 3, 7, 8, 11, 12, 9, 4]),
    ([1, [2], 3], [1, 2, 3]),
    ([], []),
    ([1, [2, [3]]], [1, 2, 3]),
    ([1, 2], [1, 2]),
]
for fn in (flatten_iter, flatten_rec):
    for nested, exp in examples:
        h = build(nested)
        ids = {id(n) for n in all_nodes(h)}
        r = fn(h)
        check_flat(r, exp, ids)
        assert exp == flat_expected(nested)
    print(fn.__name__, 'examples OK')
for nested, exp in examples:
    print(nested, '->', exp)


def rand_nested(rng, depth, budget):
    out = []
    for _ in range(rng.randint(1, 4)):
        if budget[0] <= 0:
            break
        out.append(rng.randint(0, 99))
        budget[0] -= 1
        if depth < 3 and budget[0] > 0 and rng.random() < 0.4:
            out.append(rand_nested(rng, depth + 1, budget))
    return out


rng = random.Random(31)
for _ in range(500):
    nested = rand_nested(rng, 0, [rng.randint(1, 25)])
    exp = flat_expected(nested)
    for fn in (flatten_iter, flatten_rec):
        h = build(nested)
        ids = {id(n) for n in all_nodes(h)}
        check_flat(fn(h), exp, ids)
print('500 random nested lists: iterative and recursive match the nested-array brute force, prev/child/identity OK')


def deep_chain(depth):
    head = MNode(0)
    cur = head
    for i in range(1, depth):
        cur.child = MNode(i)
        cur = cur.child
    return head


print('recursion limit:', sys.getrecursionlimit())
for depth in (500, 1200):
    for fn in (flatten_iter, flatten_rec):
        h = deep_chain(depth)
        try:
            r = fn(h)
            vals, _ = to_array(r)
            assert vals == list(range(depth))
            print(f'depth {depth:4} {fn.__name__}: ok')
        except RecursionError:
            print(f'depth {depth:4} {fn.__name__}: RecursionError')
