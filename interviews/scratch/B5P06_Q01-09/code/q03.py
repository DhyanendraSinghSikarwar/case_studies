import random

class ListNode:
    __slots__ = ("val", "next")
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build(arr, pos=-1):
    """Build a list from an array; pos != -1 makes the tail point back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos != -1:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_list(head, cap=10**6):
    """Values from head onward; the cap stops an accidental cycle from hanging the test."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out
# ---------- brute force: stable sort of the node objects by value ----------
def merge_brute(a, b):
    nodes = []
    for h in (a, b):
        while h is not None:
            nodes.append(h)
            h = h.next
    nodes.sort(key=lambda n: n.val)     # sorted() is stable: list-1 nodes stay before list-2 on ties
    for x, y in zip(nodes, nodes[1:]):
        x.next = y
    if nodes:
        nodes[-1].next = None
    return nodes[0] if nodes else None

# ---------- optimal: dummy head + tail pointer ----------
def merge_two(a, b):
    dummy = tail = ListNode()
    while a is not None and b is not None:
        if b.val < a.val:               # strict <: on a tie take from a (the first list) -> stable
            tail.next = b
            b = b.next
        else:
            tail.next = a
            a = a.next
        tail = tail.next
    tail.next = a if a is not None else b   # splice the leftover run in one step
    return dummy.next

def run(fn, x, y):
    ha, na = build(x)
    hb, nb = build(y)
    out = fn(ha, hb)
    return to_list(out), node_ids(out), na, nb

for x, y, exp in [([1,2,4],[1,3,4],[1,1,2,3,4,4]), ([],[],[]), ([],[0],[0]), ([2,5],[1],[1,2,5])]:
    vals, ids, na, nb = run(merge_two, x, y)
    assert vals == exp and sorted(ids) == sorted(map(id, na + nb))   # same node objects, none lost
    print(x, y, "->", vals)
vals, ids, na, nb = run(merge_two, [1,2,4], [1,3,4])
assert ids[0] == id(na[0]) and ids[1] == id(nb[0])                    # tie: first list's 1 comes first
print("tie check: first 1 is from list 1 -> ok")

random.seed(3)
for _ in range(1000):
    x = sorted(random.randint(0, 6) for _ in range(random.randint(0, 12)))
    y = sorted(random.randint(0, 6) for _ in range(random.randint(0, 12)))
    v1, i1, na, nb = run(merge_two, x, y)
    ha, na2 = build(x); hb, nb2 = build(y)
    exp_nodes = sorted(na2 + nb2, key=lambda n: n.val)                # stable expected order
    v2 = to_list(merge_brute(ha, hb))
    assert v1 == v2 == sorted(x + y)
    # stability by identity: the k-th result node comes from the same list/position as the brute one
    pos = {id(n): ("a", i) for i, n in enumerate(na)}; pos.update({id(n): ("b", i) for i, n in enumerate(nb)})
    pos2 = {id(n): ("a", i) for i, n in enumerate(na2)}; pos2.update({id(n): ("b", i) for i, n in enumerate(nb2)})
    assert [pos[i] for i in i1] == [pos2[id(n)] for n in exp_nodes]
print("cross-check ok (1000 random pairs with many ties, stability and identity checked)")
