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
# ---------- brute force: walk with a set, first repeated node is the cycle start ----------
def cycle_start_set(head):
    seen = set()
    while head is not None:
        if head in seen:
            return head
        seen.add(head)
        head = head.next
    return None

# ---------- Floyd phase 1 (meet) + phase 2 (restart from head) ----------
def cycle_start(head, steps_out=None):
    slow = fast = head
    t = 0
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        t += 1
        if slow is fast:
            p = head
            s2 = 0
            while p is not slow:        # both move ONE step per round
                p = p.next
                slow = slow.next
                s2 += 1
            if steps_out is not None:
                steps_out.extend([t, s2])
            return p
    return None

for arr, pos in [([3,2,0,-4],1), ([1,2],0), ([1],0), ([1,2,3],-1)]:
    head, nodes = build(arr, pos)
    r = cycle_start(head)
    assert r is (nodes[pos] if pos != -1 else None) and r is cycle_start_set(head)
    print(arr, "pos =", pos, "->", None if r is None else "index %d (value %d)" % (nodes.index(r), r.val))

# ---- exhaustive check of the proof's claims: tail length mu 0..15, cycle length lam 1..15 ----
pairs = 0
for mu in range(0, 16):
    for lam in range(1, 16):
        head, nodes = build(list(range(mu + lam)), mu)           # tail of mu nodes, then a cycle of lam
        out = []
        r = cycle_start(head, out)
        t, phase2 = out
        smallest = next(m for m in range(lam, 10 * (mu + lam) + 1, lam) if m >= mu)   # smallest POSITIVE multiple of lam >= mu
        k = (t - mu) % lam                                        # distance from cycle start to meeting point
        assert t == smallest                                      # first meeting time
        assert (mu + k) % lam == 0                                # mu + k is a multiple of lambda
        assert r is nodes[mu] and phase2 == mu                    # restart pointer meets at the start after mu steps
        pairs += 1
print("exhaustive ok:", pairs, "(mu, lambda) pairs: t = smallest positive multiple of lambda >= mu; mu + k = 0 mod lambda; phase 2 takes mu steps")

# ---- random lists with repeated values vs the set version ----
random.seed(6)
for _ in range(1000):
    n = random.randint(0, 25)
    arr = [random.randint(0, 2) for _ in range(n)]
    pos = random.randint(-1, n - 1) if n else -1
    head, nodes = build(arr, pos)
    assert cycle_start(head) is cycle_start_set(head) is (nodes[pos] if pos != -1 else None)
print("cross-check ok (1000 random lists, repeated values, identity compared)")
