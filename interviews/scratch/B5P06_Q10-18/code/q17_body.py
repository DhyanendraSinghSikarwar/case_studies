# NOPRE (this question defines its own node class and helpers)
import random, sys, tracemalloc

class ListNode:
    __slots__ = ('val', 'next')            # no per-instance __dict__; only these two attributes exist
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):                       # build from the back: no dummy needed, returns the head
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head

def to_array(head, cap=10**6):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def show(head):                            # cycle-safe: remember the index of each node seen
    if head is None:
        return 'None'
    seen, parts, i = {}, [], 0
    while head is not None:
        if id(head) in seen:
            return ' -> '.join(parts) + f' -> (cycle to index {seen[id(head)]})'
        seen[id(head)] = i
        parts.append(str(head.val))
        head = head.next
        i += 1
    return ' -> '.join(parts) + ' -> None'

def show_o1(head):                         # same output with O(1) extra space: Floyd, then find mu
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            mu, a = 0, head
            while a is not slow:
                a, slow, mu = a.next, slow.next, mu + 1
            lam, p = 1, a.next
            while p is not a:
                p, lam = p.next, lam + 1
            vals, p = [], head
            for _ in range(mu + lam):
                vals.append(str(p.val)); p = p.next
            return ' -> '.join(vals) + f' -> (cycle to index {mu})'
    return show(head)                      # no cycle: plain printing is safe

def with_cycle(arr, pos):
    head = from_array(arr)
    nodes, p = [], head
    while p:
        nodes.append(p); p = p.next
    nodes[-1].next = nodes[pos]
    return head

assert show(from_array([1, 2, 3])) == '1 -> 2 -> 3 -> None'
assert show(None) == 'None'
assert show(with_cycle([1, 2, 3], 1)) == '1 -> 2 -> 3 -> (cycle to index 1)'
assert to_array(from_array([4, 5])) == [4, 5]
print(show(from_array([1, 2, 3])))
print(show(from_array([])))
print(show(with_cycle([1, 2, 3], 1)))
print(to_array(from_array([4, 5])))

# identity versus equality
a, b = ListNode(1), ListNode(1)
print('a == b:', a == b, '| a is b:', a is b, '| a == a:', a == a)
assert (a == b) is False and (a is b) is False

# __slots__ behaviour
class Plain:                               # same fields, ordinary class
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
print('slots node has __dict__:', hasattr(a, '__dict__'), '| plain node has __dict__:', hasattr(Plain(), '__dict__'))
try:
    a.extra = 5
except AttributeError as e:
    print('new attribute on slots node:', type(e).__name__)

# memory, sandbox-only numbers (they vary by Python version and platform)
def bytes_per_node(cls, n=50_000):
    tracemalloc.start()
    nodes = [cls(i) for i in range(n)]
    cur = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    return cur / n
print('bytes per node incl. its int and list slot (sandbox only): slots %.0f, plain %.0f' % (bytes_per_node(ListNode), bytes_per_node(Plain)))
assert bytes_per_node(ListNode) < bytes_per_node(Plain)

# a naive loop never ends on a cycle: stop it by hand after 10**4 steps
p, steps = with_cycle([1, 2, 3], 1), 0
while p is not None and steps < 10**4:
    p = p.next; steps += 1
print('naive while node: still walking after', steps, 'steps')

# seeded random cross-check: show vs show_o1 vs a brute-force string, over lists with and without cycles
random.seed(17)
for _ in range(500):
    n = random.randint(0, 12)
    arr = [random.randint(0, 3) for _ in range(n)]
    if n and random.random() < 0.6:
        pos = random.randint(0, n - 1)
        head = with_cycle(arr, pos)
        want = ' -> '.join(map(str, arr)) + f' -> (cycle to index {pos})'
    else:
        head = from_array(arr)
        want = ' -> '.join(map(str, arr + [None])) if n else 'None'
    assert show(head) == show_o1(head) == want
print('random cross-check ok (500 cases)')
