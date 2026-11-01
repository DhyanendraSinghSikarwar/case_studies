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
def from_int(x):                        # test helper: digits least significant first
    return build([int(c) for c in str(x)[::-1]])[0]

# ---------- brute force: convert to int, add, convert back ----------
def to_int(head):
    return int("".join(str(v) for v in to_list(head)[::-1]))

def add_brute(a, b):
    return from_int(to_int(a) + to_int(b))

# ---------- optimal: digit by digit with a carry and a dummy head ----------
def add_two(a, b):
    dummy = tail = ListNode()
    carry = 0
    while a is not None or b is not None or carry:      # the carry alone can force one more node
        s = carry
        if a is not None:
            s += a.val
            a = a.next
        if b is not None:
            s += b.val
            b = b.next
        carry, digit = divmod(s, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next

def run(x, y):
    ha, na = build(x)
    hb, nb = build(y)
    out = add_two(ha, hb)
    assert to_list(ha) == x and to_list(hb) == y                    # inputs untouched
    assert not (set(node_ids(out)) & set(map(id, na + nb)))          # result is made of NEW nodes
    return to_list(out)

for x, y, exp in [([2,4,3],[5,6,4],[7,0,8]), ([0],[0],[0]), ([9,9,9,9],[1],[0,0,0,0,1]), ([5],[5],[0,1])]:
    assert run(x, y) == exp
    print(x, y, "->", exp)

random.seed(8)
for _ in range(2000):
    def num():
        n = random.randint(1, 100)
        digits = [random.choice([0, 9, 9, random.randint(0, 9)]) for _ in range(n)]
        if n > 1 and digits[-1] == 0:
            digits[-1] = random.randint(1, 9)                       # no leading zeros except the number 0
        return digits
    x, y = num(), num()
    ha, _n = build(x)
    hb, _m = build(y)
    assert run(x, y) == to_list(add_brute(ha, hb))
print("cross-check ok (2000 random pairs up to 100 digits, many 9s, vs int addition)")

try:
    int("9" * 5000)
except ValueError:
    print("int() of a 5000-digit string raises ValueError under the default limit")
