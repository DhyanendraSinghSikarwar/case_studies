### Q28 ⭐ 🟡 Insertion sort on a linked list. Nodes are `ListNode(val, next)`. Sort a list (0 <= len <= 1500) ascending by insertion sort: take nodes one at a time from the input and insert each into the sorted part built behind a dummy head, reusing the nodes. The sort must be stable (equal values keep original order, tests check by identity). State the cost (O(n^2) worst case, O(n) when already sorted if you add the 'compare with the last sorted node first' shortcut), and why insertion is cheap on a list (no shifting) but finding the place still takes a walk. Example: [4,2,1,3] -> [1,2,3,4]; [-1,5,3,4,0] -> [-1,0,3,4,5]; [] -> []; [2,2,1] -> [1,2,2]; [1,2,3] -> [1,2,3].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Insertion sort on a linked list with a dummy head. Take nodes from the input one at a time and splice each into the sorted chain. This works well on a list because splicing is O(1). There is no shifting like in an array.

**Say this first (1 line):** "I keep a sorted chain behind a dummy, detach the next input node, walk the chain while the next value is <= mine (so ties stay stable), and splice. Worst case O(n^2), and a tail check makes sorted input O(n)."

**Brute force:** Copy the nodes into a Python list, `sorted(..., key=val)` (Python's sort is stable), relink the nodes in that order. O(n log n) time but O(n) extra space, and the question wants the insertion method. I use it as the checker in the code.

**Optimal:**
- `dummy` is a fake node in front of the sorted chain. It means "insert at the front" is the same code as "insert in the middle".
- Loop over the input. First save `nxt = cur.next`, because splicing will overwrite `cur.next`.
- Walk `p` from the dummy while `p.next` exists and `p.next.val <= cur.val`. Then `cur.next = p.next; p.next = cur`.
- Stability: the test is `<=`, so `cur` goes AFTER every equal node already in the chain. Equal values that came earlier stay earlier. With `<` the order of equals would flip.
- Why insertion is cheap here: an array has to shift every larger element right. A list changes two pointers. Finding the place still needs a walk, because a list has no random access, so no binary search either.
- Shortcut: remember the sorted tail. If `tail.val <= cur.val`, append at the tail with no walk. Sorted input then costs one comparison per node.
- Invariant: before each step the chain behind the dummy is the sorted, stable arrangement of the nodes seen so far, and `cur` is the first unseen node.

**Complexity:**
- Time worst case O(n^2): the i-th node can walk past about i nodes, so the total is about n(n-1)/2 comparisons.
- Best case with the shortcut O(n): already-sorted input costs n - 1 tail checks.
- Space O(1) extra. The nodes are reused and only a few pointers are held.
- Honest detail from the run below: WITHOUT the shortcut, the walk starts at the front, so sorted input is the worst case (19900 comparisons for n = 200) and reversed input is the best case (199). The shortcut flips that. With it, a list whose max comes first and the rest ascending still costs about n^2/2, since nothing is ever at the tail. So the shortcut helps sorted input, not every input.

**Dry run:** [4,2,1,3], shortcut on.
| cur | sorted chain before | what happens | sorted chain after |
|---|---|---|---|
| 4 | empty | walk ends at once, insert | 4 |
| 2 | 4 | tail 4 <= 2? no. Walk: 4 <= 2? no. Insert at front | 2 -> 4 |
| 1 | 2 -> 4 | tail check no. Walk: 2 <= 1? no. Insert at front | 1 -> 2 -> 4 |
| 3 | 1 -> 2 -> 4 | tail check no. Walk: 1 <= 3 yes, 2 <= 3 yes, 4 <= 3 no. Insert after 2 | 1 -> 2 -> 3 -> 4 |

**Code:**
```python
import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def from_array(arr):
    dummy = ListNode()
    tail = dummy
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def nodes_of(head, cap=100000):
    out = []
    while head is not None:
        out.append(head)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def to_array(head):
    return [n.val for n in nodes_of(head)]


# Brute force: copy the nodes into a Python list, sort (Python's sort is stable), relink.
def sort_brute(head):
    nodes = sorted(nodes_of(head), key=lambda n: n.val)
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if nodes:
        nodes[-1].next = None
    return nodes[0] if nodes else None


# Optimal: insertion sort with a dummy head. stats counts value comparisons.
def insertion_sort(head, shortcut=True, stats=None):
    dummy = ListNode()          # sorted part hangs behind this
    tail = None                 # last node of the sorted part
    cur = head
    while cur is not None:
        nxt = cur.next          # save before we relink cur
        if shortcut and tail is not None:
            if stats is not None:
                stats[0] += 1
            if tail.val <= cur.val:   # belongs at the very end: no walk
                tail.next = cur
                cur.next = None
                tail = cur
                cur = nxt
                continue
        p = dummy
        while p.next is not None:
            if stats is not None:
                stats[0] += 1
            if p.next.val <= cur.val:     # <= keeps equal values in original order (stable)
                p = p.next
            else:
                break
        cur.next = p.next
        p.next = cur
        if cur.next is None:
            tail = cur
        cur = nxt
    return dummy.next


# examples from the prompt
for arr, exp in [([4, 2, 1, 3], [1, 2, 3, 4]), ([-1, 5, 3, 4, 0], [-1, 0, 3, 4, 5]),
                 ([], []), ([2, 2, 1], [1, 2, 2]), ([1, 2, 3], [1, 2, 3])]:
    h = from_array(arr)
    before = nodes_of(h)
    r = insertion_sort(h)
    assert to_array(r) == exp
    assert {id(n) for n in nodes_of(r)} == {id(n) for n in before}   # same node objects
    print(arr, '->', to_array(r))

# stability by identity: tag equal values with their original position
h = from_array([2, 2, 1, 1])
orig = nodes_of(h)
r = insertion_sort(h)
got = nodes_of(r)
assert got == [orig[2], orig[3], orig[0], orig[1]]
print('stable by identity: True')

# seeded randomised cross-check against the brute force, including node identity order
rng = random.Random(28)
for _ in range(500):
    arr = [rng.randint(-4, 4) for _ in range(rng.randint(0, 12))]
    for sc in (True, False):
        h1 = from_array(arr)
        n1 = nodes_of(h1)
        r1 = insertion_sort(h1, shortcut=sc)
        h2 = from_array(arr)
        n2 = nodes_of(h2)
        r2 = sort_brute(h2)
        pos1 = {id(n): i for i, n in enumerate(n1)}
        pos2 = {id(n): i for i, n in enumerate(n2)}
        assert [pos1[id(n)] for n in nodes_of(r1)] == [pos2[id(n)] for n in nodes_of(r2)]
        assert to_array(r1) == sorted(arr)
print('500 random lists, both variants match brute force by identity order')

# cost counts on n = 200
n = 200
for name, arr in [('sorted', list(range(n))), ('reversed', list(range(n, 0, -1))), ('max-first', [n] + list(range(1, n)))]:
    for sc in (True, False):
        st = [0]
        insertion_sort(from_array(arr), shortcut=sc, stats=st)
        print(f'{name:9} shortcut={sc!s:5} comparisons={st[0]}')

# bigger than the prompt limit still fine (iterative, no recursion)
big = list(range(1500, 0, -1))
assert to_array(insertion_sort(from_array(big))) == sorted(big)
print('reversed 1500 nodes sorted OK')
```

**Output (my run):**
```text
[4, 2, 1, 3] -> [1, 2, 3, 4]
[-1, 5, 3, 4, 0] -> [-1, 0, 3, 4, 5]
[] -> []
[2, 2, 1] -> [1, 2, 2]
[1, 2, 3] -> [1, 2, 3]
stable by identity: True
500 random lists, both variants match brute force by identity order
sorted    shortcut=True  comparisons=199
sorted    shortcut=False comparisons=19900
reversed  shortcut=True  comparisons=398
reversed  shortcut=False comparisons=199
max-first shortcut=True  comparisons=20099
max-first shortcut=False comparisons=19900
reversed 1500 nodes sorted OK
```

**Edge cases:**
- Empty list: the loop never runs, `dummy.next` is None, return None.
- One node: it is inserted into an empty chain and `next` stays None.
- All equal values: every node takes the tail path (or walks to the end), so the order is unchanged.
- Forgetting to save `nxt` loses the rest of the input.
- With the tail shortcut, set `cur.next = None` when appending, or the old link can leave a stale chain behind the tail.
- A node inserted at the end of the chain must update `tail`. The code does that when `cur.next` is None after splicing.

**Follow-ups:**
- Merge sort instead? That is Q25. O(n log n) time, and bottom-up uses O(1) extra space.
- Could binary search find the place? No. A list cannot jump to the middle in O(1), so locating it still takes a walk.
- When is insertion sort the right pick? Small or nearly sorted inputs, and as the base case inside a hybrid sort.

**Common mistakes:**
- Using `<` in the walk, which breaks stability.
- Not saving `cur.next` before splicing.
- Claiming reversed input is the worst case. For this walk-from-front version it is the best case.
- Building new nodes, which breaks the "reuse the nodes" rule. Value-only tests would not notice, the identity check does.

---

### Q29 ⭐ 🟡 Doubly linked list operations with sentinels. Implement a doubly linked list with `prev` and `next` pointers and two sentinel nodes `head` and `tail` (the sentinels hold no data and are never removed) supporting `add_first(v)`, `add_last(v)`, `remove(node)` in O(1) given the node, `pop_first()`, `pop_last()` and `to_array()`. Explain why sentinels remove every empty-list and one-node special case, and the four pointer assignments needed for an insert between two nodes and for a removal. The tests check that following `next` forward and `prev` backward give mirror-image sequences after every operation. Example: add_last 1, add_last 2, add_first 0 -> [0,1,2]; then pop_last -> returns 2, list [0,1]; then pop_first -> returns 0, list [1]; then pop_first, then to_array -> [] (and a further pop returns None).
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Doubly linked list with sentinel (dummy) nodes at both ends. Every real node has a real neighbour on each side, so no operation ever has to ask "is this the first node?" or "is the list empty?".

**Say this first (1 line):** "Two sentinels, head and tail, hold no data. Every insert is 'splice between left and right' and every removal is 'bypass this node'. Each is a handful of pointer assignments, O(1)."

**Brute force:** Keep a Python list. `add_last` and `pop_last` are O(1), but `add_first` (`insert(0, v)`) and `pop_first` (`pop(0)`) are O(n), and `remove(node)` needs a search first, also O(n). I use that list as the model in the cross-check.

**Optimal:**
- Layout: `head <-> n1 <-> n2 <-> ... <-> tail`. Empty list: `head <-> tail`.
- Insert `v` between `left` and `right` (four assignments):
  1. `node.prev = left`
  2. `node.next = right`
  3. `left.next = node`
  4. `right.prev = node`
- `add_first` is insert between `head` and `head.next`. `add_last` is insert between `tail.prev` and `tail`. The same helper does both.
- Remove `node` (two assignments): `node.prev.next = node.next` and `node.next.prev = node.prev`. Then clear the node's own pointers so a second remove is caught.
- `pop_first` is `remove(head.next)`, `pop_last` is `remove(tail.prev)`. Check for "empty" by `head.next is tail`.
- Why sentinels help: without them, inserting into an empty list, removing the only node, and removing the first or last node are four special cases, each needing None checks and updates of `head`/`tail` variables. With sentinels, the left and right neighbours always exist, so the same code runs in all cases.
- Invariant: after every operation, going forward from `head` and backward from `tail` visit the same nodes in opposite order, and `head.prev` and `tail.next` stay None.

**Complexity:** `add_first`, `add_last`, `remove(node)`, `pop_first`, `pop_last` are O(1) time and O(1) extra space. `to_array` is O(n). The structure itself takes O(n) space plus two sentinels.

**Dry run:** `add_last 1, add_last 2, add_first 0`.
| step | list between sentinels | pointers touched |
|---|---|---|
| start | (empty) | head.next = tail, tail.prev = head |
| add_last 1 | 1 | insert between head and tail |
| add_last 2 | 1, 2 | insert between node 1 and tail |
| add_first 0 | 0, 1, 2 | insert between head and node 1 |
| pop_last | 0, 1 (returns 2) | node1.next = tail, tail.prev = node1 |
| pop_first | 1 (returns 0) | head.next = node1, node1.prev = head |

**Code:**
```python
import random


class DNode:
    __slots__ = ('val', 'prev', 'next')

    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DLL:
    """Doubly linked list with two sentinels. Real nodes always sit strictly between them."""

    def __init__(self):
        self.head = DNode()          # sentinel, never removed
        self.tail = DNode()          # sentinel, never removed
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _insert_between(self, v, left, right):
        node = DNode(v, left, right)   # new node's two pointers
        left.next = node               # left neighbour's next
        right.prev = node              # right neighbour's prev
        self.size += 1                 # 4 assignments in total
        return node

    def add_first(self, v):
        return self._insert_between(v, self.head, self.head.next)

    def add_last(self, v):
        return self._insert_between(v, self.tail.prev, self.tail)

    def remove(self, node):
        assert node is not self.head and node is not self.tail, "sentinels are never removed"
        assert node.prev is not None and node.next is not None, "node already removed"
        node.prev.next = node.next     # 2 assignments bypass the node
        node.next.prev = node.prev
        node.prev = node.next = None   # detach so a double remove is caught
        self.size -= 1
        return node.val

    def pop_first(self):
        if self.head.next is self.tail:
            return None
        return self.remove(self.head.next)

    def pop_last(self):
        if self.tail.prev is self.head:
            return None
        return self.remove(self.tail.prev)

    def to_array(self):
        out = []
        n = self.head.next
        while n is not self.tail:
            out.append(n.val)
            n = n.next
            assert len(out) <= self.size, "forward walk is longer than size (broken links)"
        return out

    def to_array_backward(self):
        out = []
        n = self.tail.prev
        while n is not self.head:
            out.append(n.val)
            n = n.prev
            assert len(out) <= self.size, "backward walk is longer than size (broken links)"
        return out

    def check(self):
        fwd, bwd = self.to_array(), self.to_array_backward()
        assert fwd == bwd[::-1] and len(fwd) == self.size
        assert self.head.prev is None and self.tail.next is None
        return fwd


# Brute force model: a plain Python list (insert(0) and pop(0) are O(n); removing a node means a search, O(n)).
# The prompt's walk-through
d = DLL()
d.add_last(1); d.add_last(2); d.add_first(0)
print('after add_last 1, add_last 2, add_first 0:', d.check())
print('pop_last ->', d.pop_last(), d.check())
print('pop_first ->', d.pop_first(), d.check())
print('pop_first ->', d.pop_first(), d.check())
print('pop_first on empty ->', d.pop_first(), '| pop_last on empty ->', d.pop_last(), '| to_array ->', d.to_array())

# remove(node) from the middle, with node handles
d = DLL()
a, b, c = d.add_last('a'), d.add_last('b'), d.add_last('c')
print('remove middle ->', d.remove(b), d.check())
try:
    d.remove(b)
except AssertionError as e:
    print('double remove caught:', e)
try:
    d.remove(d.head)
except AssertionError as e:
    print('sentinel remove caught:', e)

# seeded randomised cross-check against a Python list model; mirror check after EVERY operation
rng = random.Random(29)
ops_done = 0
for trial in range(300):
    d = DLL()
    model = []                       # list of (value, node) in order
    nxt = 0
    for _ in range(rng.randint(1, 40)):
        op = rng.choice(['af', 'al', 'rm', 'pf', 'pl'])
        if op == 'af':
            model.insert(0, (nxt, d.add_first(nxt))); nxt += 1
        elif op == 'al':
            model.append((nxt, d.add_last(nxt))); nxt += 1
        elif op == 'rm' and model:
            i = rng.randrange(len(model))
            v, node = model.pop(i)
            assert d.remove(node) == v
        elif op == 'pf':
            got = d.pop_first()
            assert got == (model.pop(0)[0] if model else None)
        elif op == 'pl':
            got = d.pop_last()
            assert got == (model.pop()[0] if model else None)
        assert d.check() == [v for v, _ in model]
        assert d.head.next is d.tail or d.head.next.prev is d.head
        ops_done += 1
print('300 random op sequences,', ops_done, 'operations, mirror check after each: OK')

# sentinels survive emptying
d = DLL()
for i in range(5):
    d.add_last(i)
while d.pop_first() is not None:
    pass
assert d.head.next is d.tail and d.tail.prev is d.head and d.size == 0
print('sentinels intact after emptying: True')
```

**Output (my run):**
```text
after add_last 1, add_last 2, add_first 0: [0, 1, 2]
pop_last -> 2 [0, 1]
pop_first -> 0 [1]
pop_first -> 1 []
pop_first on empty -> None | pop_last on empty -> None | to_array -> []
remove middle -> b ['a', 'c']
double remove caught: node already removed
sentinel remove caught: sentinels are never removed
300 random op sequences, 6197 operations, mirror check after each: OK
sentinels intact after emptying: True
```

**Edge cases:**
- Empty list: `pop_first` and `pop_last` return None; they must not remove a sentinel.
- Single node: removing it leaves `head <-> tail`, with no special code.
- `remove` called twice on the same node: the code clears the node's pointers on removal and asserts on the second call. Without that, the list is silently corrupted.
- Never return or remove a sentinel. The code asserts it.
- `size` is kept as a counter so the mirror check can detect a broken link as a walk that is too long, instead of hanging.

**Follow-ups:**
- Why does `remove(node)` need a doubly linked list? To unlink a node you need its predecessor. A singly linked list only gives that by walking from the head, which is O(n). The doubly linked list stores it.
- What does the extra `prev` pointer cost? One more pointer per node, and one more pair of assignments in every update.
- Where is this used? LRU caches (Q30) and deques.

**Common mistakes:**
- Wrong assignment order in an insert that overwrites a pointer you still need. Set the new node's pointers first, then the neighbours'.
- Updating `next` links but forgetting the `prev` links. Forward walks look fine and backward walks are broken, which is why the test walks both ways.
- Using `None` as an end marker and then needing `if node.next:` checks everywhere. That undoes the point of sentinels.

---

### Q30 ⭐ 🟡 LRU cache: the linked-list idea (concept only). A cache of capacity c supports `get(key)` and `put(key, value)` in O(1), evicting the least recently used key when full; a `get` or `put` of a key makes it the most recently used. Explain at concept level why a hash map alone cannot find the least recently used key in O(1) and a list alone cannot find a key in O(1), how a doubly linked list (most recent at the head side, with sentinels) plus a dict key -> node gives O(1) for both, what pointer moves `get` and `put` perform, and why a SINGLY linked list is not enough (you need the previous node to unlink). Mention that `collections.OrderedDict` does the same internally and that the full class design and thread-safety discussion belong to the design part of this book (Part 14). Example with capacity 2: put(1,1), put(2,2), get(1) -> 1, put(3,3) evicts key 2, get(2) -> -1, put(4,4) evicts key 1, get(1) -> -1, get(3) -> 3, get(4) -> 4.
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Hash map plus doubly linked list. The map finds a node by key in O(1). The list keeps use order, so the oldest is at one end and moving a node to the other end is O(1).

**Say this first (1 line):** "Dict key to node for O(1) lookup, doubly linked list with sentinels for O(1) reorder and eviction. Most recent right after the head sentinel, least recent right before the tail sentinel."

**Brute force:** A dict for values plus a Python list of keys in use order. `get` finds the key in the list (`remove`, O(c)) and appends it again. Eviction is `pop(0)`, also O(c). Correct, but O(capacity) per operation. I use it as a checker.

**Optimal:**
- Why a hash map alone fails: it finds a key fast but has no idea which key is least recently used. Finding that means scanning every key, O(c).
- Why a list alone fails: it knows the order but finding a key means a walk, O(c).
- Together: the map gives the node, the list gives the order.
- `get(key)`: look up the node. Miss returns -1. Hit: unlink it, push it right after the head sentinel, return the value.
- `put(key, value)`:
  - Key exists: update the value, move the node to the front.
  - New key and the cache is full: unlink `tail.prev` (the least recent), delete its key from the dict, then insert the new node at the front.
  - The node must store its key, otherwise you cannot delete the evicted entry from the dict.
- Why doubly: to unlink a node you must set its predecessor's `next`. In a singly linked list you only reach the predecessor by walking from the head, O(n). The `prev` pointer makes unlinking O(1) from a node you already hold.
- Sentinels remove the empty-list and one-node special cases (see Q29).
- `collections.OrderedDict` does the same inside. `move_to_end` and `popitem(last=False)` give a short version, which the code includes as a reference.
- Full class design, interfaces and thread safety belong to Part 14, not here.

**Complexity:** `get` and `put` are O(1) average time (dict average O(1), list steps O(1)). Space O(c) for the map and the nodes. The brute force costs O(c) per operation.

**Dry run:** capacity 2. List shown most recent first.
| call | result | list after |
|---|---|---|
| put(1,1) | | 1 |
| put(2,2) | | 2, 1 |
| get(1) | 1 | 1, 2 |
| put(3,3) | evicts 2 | 3, 1 |
| get(2) | -1 | 3, 1 |
| put(4,4) | evicts 1 | 4, 3 |
| get(1) | -1 | 4, 3 |
| get(3) | 3 | 3, 4 |
| get(4) | 4 | 4, 3 |

**Code:**
```python
import random
from collections import OrderedDict


class Node:
    __slots__ = ('key', 'val', 'prev', 'next')

    def __init__(self, key=None, val=None):
        self.key, self.val, self.prev, self.next = key, val, None, None


class LRU:
    """dict key -> node, plus a doubly linked list with sentinels. Most recent right after head."""

    def __init__(self, capacity):
        assert capacity >= 1
        self.cap = capacity
        self.map = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev

    def _push_front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        n = self.map.get(key)
        if n is None:
            return -1
        self._unlink(n)              # O(1) because we hold the node and it has prev
        self._push_front(n)          # now the most recently used
        return n.val

    def put(self, key, val):
        n = self.map.get(key)
        if n is not None:            # existing key: update and refresh
            n.val = val
            self._unlink(n)
            self._push_front(n)
            return
        if len(self.map) == self.cap:    # full: evict the least recently used, just before tail
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]        # the node stores its key so we can delete from the dict
        n = Node(key, val)
        self.map[key] = n
        self._push_front(n)

    def keys_recent_first(self):
        out, n = [], self.head.next
        while n is not self.tail:
            out.append(n.key)
            n = n.next
            assert len(out) <= len(self.map), "broken links"
        back, n = [], self.tail.prev
        while n is not self.head:
            back.append(n.key)
            n = n.prev
            assert len(back) <= len(self.map), "broken links"
        assert out == back[::-1] and set(out) == set(self.map)
        return out


class LRUBrute:
    """Brute force: dict plus a list of keys ordered by use. Refreshing a key is a list scan, O(capacity)."""

    def __init__(self, capacity):
        self.cap, self.d, self.order = capacity, {}, []   # order[0] is least recent

    def _touch(self, key):
        self.order.remove(key)           # O(c) search
        self.order.append(key)

    def get(self, key):
        if key not in self.d:
            return -1
        self._touch(key)
        return self.d[key]

    def put(self, key, val):
        if key in self.d:
            self.d[key] = val
            self._touch(key)
            return
        if len(self.d) == self.cap:
            old = self.order.pop(0)
            del self.d[old]
        self.d[key] = val
        self.order.append(key)


class LRUOrdered:
    """Reference: collections.OrderedDict (a hash map plus a doubly linked list inside)."""

    def __init__(self, capacity):
        self.cap, self.od = capacity, OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, val):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = val
        if len(self.od) > self.cap:
            self.od.popitem(last=False)


# prompt example, capacity 2
c = LRU(2)
c.put(1, 1); c.put(2, 2)
print('get(1) ->', c.get(1), '| recent first:', c.keys_recent_first())
c.put(3, 3)
print('put(3,3) evicts 2; get(2) ->', c.get(2), '| recent first:', c.keys_recent_first())
c.put(4, 4)
print('put(4,4) evicts 1; get(1) ->', c.get(1))
print('get(3) ->', c.get(3), '| get(4) ->', c.get(4), '| recent first:', c.keys_recent_first())

# put on an existing key refreshes it and updates the value
c = LRU(2)
c.put(1, 'a'); c.put(2, 'b'); c.put(1, 'A'); c.put(3, 'c')   # 2 is now least recent and is evicted
assert c.get(2) == -1 and c.get(1) == 'A' and c.get(3) == 'c'
# capacity 1
c = LRU(1)
c.put(1, 1); c.put(2, 2)
assert c.get(1) == -1 and c.get(2) == 2
print('refresh-on-put and capacity 1: OK')

# seeded randomised cross-check of all three
rng = random.Random(30)
ops = 0
for _ in range(300):
    cap = rng.randint(1, 5)
    a, b, o = LRU(cap), LRUBrute(cap), LRUOrdered(cap)
    for _ in range(rng.randint(1, 60)):
        k = rng.randint(0, 7)
        if rng.random() < 0.5:
            v = rng.randint(0, 99)
            a.put(k, v); b.put(k, v); o.put(k, v)
        else:
            assert a.get(k) == b.get(k) == o.get(k)
        assert a.keys_recent_first() == b.order[::-1] == list(reversed(o.od))
        assert len(a.map) <= cap
        ops += 1
print('300 random sessions,', ops, 'operations, LRU = brute force = OrderedDict: OK')
```

**Output (my run):**
```text
get(1) -> 1 | recent first: [1, 2]
put(3,3) evicts 2; get(2) -> -1 | recent first: [3, 1]
put(4,4) evicts 1; get(1) -> -1
get(3) -> 3 | get(4) -> 4 | recent first: [4, 3]
refresh-on-put and capacity 1: OK
300 random sessions, 9282 operations, LRU = brute force = OrderedDict: OK
```

**Edge cases:**
- `put` on an existing key must refresh recency and update the value, and it must not evict anything.
- `get` on a missing key returns -1 and changes nothing.
- Capacity 1: every new key evicts the previous one.
- Capacity 0 is outside the question; the code asserts capacity >= 1.
- Evicting without deleting the key from the dict leaves a dangling entry, so `len(map)` drifts above the capacity.

**Follow-ups:**
- Why not a singly linked list? You need the previous node to unlink in O(1), and a singly linked node does not have it.
- Why store the key inside the node? On eviction you hold the node, and you must also delete its dict entry.
- What changes for multiple threads? You need locking or a sharded design. That is Part 14.

**Common mistakes:**
- Moving the node on `get` but not on `put` of an existing key.
- Forgetting that the dict and the list can disagree. Delete from both on eviction.
- Evicting before checking whether the key already exists, which drops an entry for no reason.
- Using a list and `remove` and then claiming O(1).

---

### Q31 ⭐ 🟡 Flatten a multilevel doubly linked list. Each node has `val`, `prev`, `next` and `child` (a child is the head of a separate doubly linked list, which may have children of its own); total nodes <= 1000. Flatten into a single-level doubly linked list in place, where a node's child list is spliced in right after the node (depth-first order) and every `child` becomes None and every `prev` pointer is correct. Examples write the structure as nested arrays: a list item that is itself an array is the child list of the node just before it. Give the iterative stack-free splice (find the child's tail, connect it to the next node) and a recursive version, and mention its depth risk. Example: [1,2,3,[7,8,[11,12],9],4] -> [1,2,3,7,8,11,12,9,4]; [1,[2],3] -> [1,2,3]; [] -> []; [1,[2,[3]]] -> [1,2,3]; [1,2] -> [1,2].
**Asked at:** Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice) | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports
**Pattern:** Splice sublists into the main list. The child list goes in right after its parent, in depth-first order. Walking forward visits spliced-in nodes too, so deeper children are handled later by the same loop. No stack is needed.

**Say this first (1 line):** "Walk the list. At a node with a child, find the child list's tail, connect that tail to the node's old next, connect the node to the child head, fix both prev pointers, clear child. Then keep walking, and the spliced nodes are visited next."

**Brute force:** Do a DFS over the structure (a stack or recursion), collect the values in order, and build a brand-new flat list. O(n) time but O(n) extra space, and it creates new nodes, so it fails "in place". The code uses a nested-array walk as an independent expected answer.

**Optimal:** (iterative splice)
- `cur = head`. While `cur`: if `cur.child` exists:
  1. `child = cur.child`; walk `tail` to the end of the child list.
  2. `tail.next = cur.next`; if `cur.next` exists, `cur.next.prev = tail`.
  3. `cur.next = child`; `child.prev = cur`; `cur.child = None`.
- Then `cur = cur.next`. That is now `child`, so its nodes (and their children) are processed in turn.
- Why the tail walk is not a hidden O(n^2): the tail walk scans only the top level of that child list, before its own children are spliced. So each node is scanned once by a tail walk and once by `cur`. Total O(n).
- Order matters: connect the child's tail to the old next BEFORE overwriting `cur.next`, or the rest of the list is lost.
- Recursive version: `go(node)` flattens a list and returns its tail. At a node with a child, call `go(child)`, splice, and continue from the saved `nxt`. It is shorter to reason about, but the depth equals the child nesting depth.

**Complexity:** Time O(n), where n is the total number of nodes. Space O(1) extra for the iterative version. The recursive version uses O(d) stack for nesting depth d, up to O(n).

**Dry run:** `1 - 2 - 3 - 4`, where 3 has child `7 - 8 - 9` and 8 has child `11 - 12`.
| cur | action | list after |
|---|---|---|
| 1, 2 | no child | 1 2 3 4 |
| 3 | child 7. Its tail is 9. 9.next = 4, 4.prev = 9, 3.next = 7, 7.prev = 3, clear 3.child | 1 2 3 7 8 9 4 (8 still has a child) |
| 7 | no child | same |
| 8 | child 11. Its tail is 12. 12.next = 9, 9.prev = 12, 8.next = 11, 11.prev = 8, clear 8.child | 1 2 3 7 8 11 12 9 4 |
| 11, 12, 9, 4 | no child | done |

**Code:**
```python
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
```

**Output (my run):**
```text
flatten_iter examples OK
flatten_rec examples OK
[1, 2, 3, [7, 8, [11, 12], 9], 4] -> [1, 2, 3, 7, 8, 11, 12, 9, 4]
[1, [2], 3] -> [1, 2, 3]
[] -> []
[1, [2, [3]]] -> [1, 2, 3]
[1, 2] -> [1, 2]
500 random nested lists: iterative and recursive match the nested-array brute force, prev/child/identity OK
recursion limit: 1000
depth  500 flatten_iter: ok
depth  500 flatten_rec: ok
depth 1200 flatten_iter: ok
depth 1200 flatten_rec: RecursionError
```

The last four lines are the recursion risk. The list is a chain where each node has only a child. With the default limit of 1000, the recursive version fails at depth 1200 and the iterative one does not. (The check builds the nested structure from nodes directly, so building it needs no recursion.)

**Edge cases:**
- Empty list: return None.
- No children: the loop just walks, nothing changes.
- The child is on the LAST node: `cur.next` is None, so `tail.next = None` and there is no `prev` to fix. The code guards that.
- A child list that has a child on its first node: handled when `cur` steps into it.
- Forgetting `cur.child = None` leaves a stale pointer; the test checks every `child` is None.
- A wrong `prev` is invisible when printing forward, so the test walks backward from the tail and compares.

**Follow-ups:**
- Can it be done with an explicit stack instead? Yes: push `next` when you descend, pop at the end of a branch. That is O(d) extra space.
- What if the order were breadth first? You would need a queue, and it would not be an in-place splice.
- The same splice idea on a singly linked list? Drop the `prev` lines.

**Common mistakes:**
- Overwriting `cur.next` before saving it, which loses the rest of the list.
- Not updating `cur.next.prev` or `child.prev`.
- Leaving `child` set. A later traversal might expand it again.
- Rescanning from the head after each splice, which makes it O(n^2).

---

### Q32 ⭐ 🟡 Testing linked-list solutions: a harness. Describe and write the test harness used for this part: `from_array`, `to_array`, `same_structure(a, b)` comparing two lists by values, a cycle check (Floyd, O(1) space) so a broken solution fails instead of hanging, an aliasing check that two lists share no node (a set of `id`), and an in-place check that records `id` of every input node before the call and verifies afterwards that the result is made of exactly those node objects (for questions that say 'in place'). Explain why testing by values alone cannot catch an algorithm that builds new nodes, why a step cap is needed when a bug creates a cycle, and how to compare nodes in a random cross-check against a brute-force on Python lists. Example: from_array([1,2,3]) -> 3 distinct nodes and to_array gives [1,2,3]; reversing it in place -> [3,2,1] with the same 3 ids, so the in-place check is True; a reverse that builds new nodes -> [3,2,1] by values but the in-place check is False; a bug that links the tail to the head -> reported as a cycle instead of hanging.
**Asked at:** Python recursion-limit explainers (note.nkmk.me, educative.io, DEV Community recursion-limit posts; snippets only, not opened: default limit 1000, raising it risks crashes, iteration preferred); __slots__ behaviour not found in any snippet and was verified by running Python 3.13 in the sandbox | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports
**Pattern:** Test harness design. Linked-list bugs hide from value checks, so the harness tests structure, cycles, aliasing and node identity as well as values.

**Say this first (1 line):** "Five helpers: build from an array, read back to an array, compare structure, a Floyd cycle check so a bug fails instead of hanging, and an identity check that the result uses exactly the input's node objects."

**Brute force:** Compare `to_array(result)` with an expected Python list and nothing else. It is simple, and it has three blind spots:
- A solution that builds new nodes passes, although the question said "in place".
- A solution that creates a cycle makes `to_array` loop forever, so the test hangs.
- A solution that shares nodes between two lists passes, until someone mutates one list.

**Optimal:** the harness in the code.
- `from_array(arr)`: dummy head plus tail pointer. Always fresh nodes, so tests never share nodes by accident.
- `to_array(head)`: calls `has_cycle` first (Floyd, O(1) space) and raises `CycleError`. A broken solution now fails with a message.
- `same_structure(a, b)`: walk both lists together, compare `val`, require both to end together. It carries a step cap, so even a cycle cannot hang it.
- `no_shared_nodes(a, b)`: `set(id(node))` of each list; the intersection must be empty. Use it for copy and deep-copy questions.
- `check_in_place(fn, arr)`: record `id` of every input node BEFORE the call. After the call, the result's ids must equal that set (or be a subset, for questions that delete nodes), with no id repeated.
- Why values alone cannot catch new nodes: `[3,2,1]` built from fresh nodes has the same values as `[3,2,1]` built by relinking.
- Why a step cap: a bug that creates a cycle turns `while node:` into an infinite loop. Floyd (or a cap) turns that into a failed test. Floyd is exact and O(1) space; the cap is a blunt backstop for comparisons.
- Random cross-check: generate seeded random arrays, run the node-based solution, compare `to_array` with the brute force on a Python list, then also run the identity check. For stability questions, compare the ORDER of node identities with a stable sort of the original nodes.

**Complexity:** `from_array`, `to_array`, `same_structure`, `no_shared_nodes` and `check_in_place` are all O(n) time. Floyd is O(1) space. The id sets use O(n) space, which is fine for a test harness.

**Dry run:** `reverse_in_place` on `[1,2,3]` with `check_in_place`.
| step | state |
|---|---|
| from_array | nodes A(1), B(2), C(3) |
| record ids | {id(A), id(B), id(C)} |
| call fn | result is C -> B -> A |
| to_array | [3, 2, 1] |
| ids after | {id(C), id(B), id(A)}, equal to the recorded set, so True |

Now `reverse_new_nodes`: the values are also [3, 2, 1], but the ids are three new objects, so the set differs and the result is False. The buggy version sets `A.next = C`, which gives C -> B -> A -> C. Floyd finds the cycle, so a CycleError is raised, no hang.

**Code:**
```python
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
```

**Output (my run):**
```text
3 distinct nodes: True | to_array: [1, 2, 3]
reverse in place   -> [3, 2, 1] | same node objects: True
reverse new nodes  -> [3, 2, 1] | same node objects: False
buggy reverse      -> reported: list has a cycle
same_structure and aliasing check: OK
compare of cyclic lists: step cap hit while comparing
500 random lists: in-place version passes everything; new-node version passes values, fails identity
drop_first subset check -> [6, 7] True
```

**Edge cases:**
- Empty list: no nodes, so the identity check passes trivially. The random check accounts for that.
- Solutions that delete nodes need `subset=True`; solutions that merge two lists need the union of both input id sets.
- Never reuse a list across calls. A solution mutates its input, so build a fresh one every time.
- `id()` values can be reused once an object is freed. The harness keeps a list of the input nodes alive during the call, so a deleted node's id cannot be handed to a brand-new node and fake a pass.

**Follow-ups:**
- How do you test a function that returns a node, not a list (like finding a middle)? Compare by `is` to the node you picked in the input.
- How do you test a copy with random pointers? Walk both lists, check that no copy node is an original node, and that `random` targets match by index. That is Q35.
- Is a step cap enough alone? It catches loops but gives a vague failure. Floyd gives a precise "cycle" report.

**Common mistakes:**
- Testing only values and trusting it.
- Calling `to_array` on a possibly cyclic list without a guard.
- Comparing nodes with `==` and expecting a value comparison. Default equality is identity (Q17), so two nodes with equal values compare unequal. Compare `.val` on purpose, and use `is` for identity.
- Recording ids AFTER the call, which proves nothing.

---

### Q33 ⭐ 🔴 Cycle length and tail length with Floyd. Nodes are `ListNode(val, next)`. For a list with possible cycle (examples give the array plus `pos`, the index the tail points back to, -1 for none), return the pair (mu, lambda): mu is the number of nodes before the cycle starts and lambda is the number of nodes in the cycle; if there is no cycle return (n, 0) where n is the list length. Find the meeting point, then count the cycle by walking one pointer around once, then find mu by the restart-from-head step; give the total number of pointer moves as a bound in terms of mu and lambda and derive it (do not use loose phrases). Contrast with Brent's variant at one sentence. The cycle-in-an-array-of-jumps version is Part 2 Q44. Example: [3,2,0,-4], pos=1 -> (1, 3); [1,2], pos=0 -> (0, 2); [1], pos=-1 -> (1, 0); [1,2,3], pos=2 -> (2, 1); [], pos=-1 -> (0, 0).
**Asked at:** Floyd cycle-detection explanations (arXiv note on Pollard rho, Wikipedia cycle detection, VisuAlgo cycle finding, an Isabelle formalisation; snippets only, not opened: they give the mu + k = lambda*M relation, finding mu by restarting one pointer, finding lambda by looping once; none gives a complete written proof, so the proof here is the editor's own and is tested exhaustively) | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports
**Pattern:** Floyd's tortoise and hare, used as a measuring tool. One run gives a meeting point. A lap around the cycle gives lambda. A restart from the head gives mu. The same idea on an array of jumps is Part 2 Q44.

**Say this first (1 line):** "Phase 1: slow and fast until they meet. Phase 2: walk one pointer around once to count lambda. Phase 3: put one pointer at the head, move both one step at a time, count the steps until they meet: that is mu. No cycle: (n, 0)."

**Brute force:** Walk the list and store the index at which each node was first seen (a dict keyed by node identity). The first node seen twice gives mu (its stored index) and lambda (the current index minus mu). O(n) time, O(n) space.

**Optimal:**
- Setup: mu = nodes before the cycle, lambda = nodes in the cycle.
- Phase 1: slow moves 1, fast moves 2. If fast reaches None, there is no cycle. Count the nodes and return (n, 0).
- Meeting time: slow is inside the cycle from step mu on. Both are in the cycle and their positions agree only when the number of steps t is a multiple of lambda (fast has travelled 2t, slow t, and 2t - t = t must be a multiple of lambda). They can only meet inside the cycle, so t >= mu. So t is the smallest POSITIVE multiple of lambda with t >= mu. (If mu = 0 then t = lambda, not 0.)
- Hence t <= mu + lambda: for mu >= 1 it is at most mu + lambda - 1, and for mu = 0 it is exactly lambda.
- Phase 2 (lambda): from the meeting node, step around until you are back. That is lambda moves.
- Phase 3 (mu): at the meeting time, slow has travelled t, a multiple of lambda, with t >= mu. It sits at distance k = t - mu from the cycle start, so mu + k = t is a multiple of lambda. Walking mu more steps from the meeting point returns to the cycle start. A pointer from the head also reaches the cycle start after mu steps. So they meet exactly at the start, after mu steps each.
- Pointer-move count (each `.next` taken is one move):
  - Phase 1: slow t, fast 2t, so 3t.
  - Phase 2: lambda.
  - Phase 3: mu for each of two pointers, so 2mu.
  - Total = 3t + lambda + 2mu <= 3(mu + lambda) + lambda + 2mu = 5mu + 4lambda.
  - So O(mu + lambda), O(1) space. The run below checks the exact formula for all 900 pairs of mu in 0..30 and lambda in 1..30. The bound 5mu + 4lambda is reached when mu = 0.
- No cycle: about 3 * floor(n/2) moves for phase 1 plus n to count, which is O(n).
- Brent's variant, one sentence: the tortoise teleports to the hare's position at powers of two, which finds lambda directly and often takes fewer pointer moves, with the same O(1) space.

**Complexity:** Time O(mu + lambda) for a list with a cycle (O(n) since n = mu + lambda), O(n) with no cycle. Space O(1).

**Dry run:** [3,2,0,-4], pos = 1, so mu = 1, lambda = 3. Node indices 0..3.
| step | slow at | fast at |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 2 | 1 (2 -> 3 -> 1) |
| 3 | 3 | 3 (1 -> 2 -> 3), meet, t = 3 |

- t = 3 is the smallest positive multiple of lambda = 3 that is >= mu = 1.
- Phase 2: from index 3 around 1, 2, 3 is 3 moves, so lambda = 3.
- Phase 3: a = 0, b = 3. One step: a = 1, b = 1, so mu = 1.
- Moves: 3 * 3 + 3 + 2 * 1 = 14.

**Code:**
```python
import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(arr, pos=-1):
    """List from an array; if pos != -1 the tail's next points back to the node at index pos."""
    dummy = ListNode()
    tail, nodes = dummy, []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos != -1:
        tail.next = nodes[pos]
    return dummy.next, nodes


# Brute force: remember the index at which each node was first seen. O(n) space.
def mu_lambda_brute(head):
    seen, i = {}, 0
    while head is not None:
        if head in seen:                      # node hash is identity
            return seen[head], i - seen[head]
        seen[head] = i
        head, i = head.next, i + 1
    return i, 0                               # no cycle: n nodes, lambda = 0


# Optimal: Floyd in three phases. moves[0] counts every `.next` step taken.
def mu_lambda_floyd(head, moves=None, info=None):
    m = [0] if moves is None else moves
    if head is None:
        return 0, 0
    slow = fast = head
    t = 0
    while fast is not None and fast.next is not None:     # phase 1: find a meeting point
        slow = slow.next
        fast = fast.next.next
        m[0] += 3                                          # one step for slow, two for fast
        t += 1
        if slow is fast:
            break
    else:                                                  # fast fell off the end: no cycle
        n = 0
        while head is not None:                            # count the nodes
            head = head.next
            n += 1
            m[0] += 1
        return n, 0
    if info is not None:
        info['t'] = t
    lam, p = 1, slow.next                                  # phase 2: walk once around the cycle
    m[0] += 1
    while p is not slow:
        p = p.next
        lam += 1
        m[0] += 1
    mu, a, b = 0, head, slow                               # phase 3: restart one pointer at the head
    while a is not b:
        a, b = a.next, b.next
        mu += 1
        m[0] += 2
    return mu, lam


def expected(n, pos):
    return (pos, n - pos) if pos != -1 else (n, 0)


# examples from the prompt
for arr, pos, exp in [([3, 2, 0, -4], 1, (1, 3)), ([1, 2], 0, (0, 2)), ([1], -1, (1, 0)),
                      ([1, 2, 3], 2, (2, 1)), ([], -1, (0, 0))]:
    h, _ = build(arr, pos)
    got = mu_lambda_floyd(h)
    assert got == mu_lambda_brute(h) == exp == expected(len(arr), pos), (arr, pos, got)
    print(arr, 'pos =', pos, '->', got)

# exhaustive check over mu in 0..30, lambda in 1..30: results, meeting time t and the move count
worst_gap = 0
for mu in range(0, 31):
    for lam in range(1, 31):
        h, _ = build(list(range(mu + lam)), mu)
        m, info = [0], {}
        assert mu_lambda_floyd(h, m, info) == (mu, lam) == mu_lambda_brute(h)
        t = info['t']
        t_formula = max(1, -(-mu // lam)) * lam            # smallest positive multiple of lam that is >= mu
        assert t == t_formula and t <= mu + lam
        assert m[0] == 3 * t + lam + 2 * mu                # exact move count
        assert m[0] <= 5 * mu + 4 * lam                    # the stated bound
        worst_gap = max(worst_gap, (5 * mu + 4 * lam) - m[0])
print('900 (mu, lambda) pairs: t = smallest positive multiple of lambda >= mu, moves = 3t + lambda + 2mu <= 5mu + 4lambda')

# the bound is tight at mu = 0 and loose by at most this much elsewhere
h, _ = build(list(range(5)), 0)
m = [0]; mu_lambda_floyd(h, m)
print('mu = 0, lambda = 5: moves =', m[0], 'and 5mu + 4lambda =', 20)
h, _ = build(list(range(1 + 5)), 1)
m = [0]; mu_lambda_floyd(h, m)
print('mu = 1, lambda = 5: moves =', m[0], 'and 5mu + 4lambda =', 5 + 20)

# no-cycle lists: moves is about 3n/2 + n
for n in (0, 1, 2, 9, 10):
    h, _ = build(list(range(n)))
    m = [0]
    assert mu_lambda_floyd(h, m) == (n, 0)
    print('no cycle, n =', n, ': moves =', m[0])

# seeded random cross-check against the brute force
rng = random.Random(33)
for _ in range(1000):
    n = rng.randint(0, 40)
    pos = rng.randint(-1, n - 1) if n else -1
    h, _ = build([rng.randint(0, 3) for _ in range(n)], pos)     # repeated values on purpose
    assert mu_lambda_floyd(h) == mu_lambda_brute(h) == expected(n, pos)
print('1000 random lists (repeated values): Floyd = brute force = expected')
```

**Output (my run):**
```text
[3, 2, 0, -4] pos = 1 -> (1, 3)
[1, 2] pos = 0 -> (0, 2)
[1] pos = -1 -> (1, 0)
[1, 2, 3] pos = 2 -> (2, 1)
[] pos = -1 -> (0, 0)
900 (mu, lambda) pairs: t = smallest positive multiple of lambda >= mu, moves = 3t + lambda + 2mu <= 5mu + 4lambda
mu = 0, lambda = 5: moves = 20 and 5mu + 4lambda = 20
mu = 1, lambda = 5: moves = 22 and 5mu + 4lambda = 25
no cycle, n = 0 : moves = 0
no cycle, n = 1 : moves = 1
no cycle, n = 2 : moves = 5
no cycle, n = 9 : moves = 21
no cycle, n = 10 : moves = 25
1000 random lists (repeated values): Floyd = brute force = expected
```

**Edge cases:**
- Empty list: (0, 0) with no moves.
- Self-loop ([1], pos = 0): mu = 0, lambda = 1.
- Cycle starts at the head (pos = 0): mu = 0, and the restart pointer already meets the other at the start.
- No cycle: the pair is (n, 0), so n is the list length, as the prompt defines.
- Repeated values do not matter. Everything is by node identity, and the random test uses lots of equal values on purpose.

**Follow-ups:**
- Why must fast move exactly 2? Any step difference d works if gcd conditions hold, but 2 gives difference 1 per step, so it can never jump over slow inside the cycle.
- How do you get the cycle start without counting? That is Q6: phase 3 alone.
- What about a cycle in an array of jumps? Part 2 Q44.

**Common mistakes:**
- Saying "t = smallest multiple of lambda >= mu" and forgetting "positive". At mu = 0 the first meeting is at t = lambda.
- Starting `fast` one step ahead and breaking the t analysis.
- Counting lambda starting from the head rather than from the meeting node.
- Returning (0, 0) for a one-node list without a cycle. It is (1, 0).

---

### Q34 ⭐ 🔴 Break a cycle (remove the loop). Nodes are `ListNode(val, next)`. Given a list that may contain a cycle (array plus `pos` for the example, -1 for none), remove the cycle IN PLACE by setting `next = None` on the last node of the cycle, using O(1) extra space, and return the index of the node whose `next` you changed (None if there was no cycle). Use Floyd to find the cycle start, then walk the cycle until the node whose next is the start; explain the self-loop case where the start itself is that node. The tests check that the result is acyclic, has the same nodes in the same order and no node was created. Example: [3,2,0,-4], pos=1 -> cut at index 3, list [3,2,0,-4]; [1,2], pos=0 -> cut at index 1, list [1,2]; [1,2,3], pos=2 -> cut at index 2 (self-loop), list [1,2,3]; [1], pos=-1 -> None, list [1].
**Asked at:** Floyd cycle-detection explanations (arXiv note on Pollard rho, Wikipedia cycle detection, VisuAlgo cycle finding, an Isabelle formalisation; snippets only, not opened: they give the mu + k = lambda*M relation, finding mu by restarting one pointer, finding lambda by looping once; none gives a complete written proof, so the proof here is the editor's own and is tested exhaustively) | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports
**Pattern:** Floyd's cycle start (Q6), then one more walk around the cycle to find the node that points back to the start.

**Say this first (1 line):** "Find the cycle start with Floyd. Then walk from the start until `node.next is start`. Set that node's `next` to None. A self-loop works too, because the start itself is that node."

**Brute force:** Walk the list with a set of visited nodes. When `head` is already in the set, the previous node is the one pointing back, so set `prev.next = None`. O(n) time, O(n) space.

**Optimal:**
- Phase 1: slow and fast. If fast hits None, there is no cycle: return None, change nothing.
- Phase 2: restart one pointer at the head and move both by one. They meet at the cycle start (the proof is in Q6 and Q33).
- Phase 3: `last = start`; `while last.next is not start: last = last.next`. Then `last.next = None`.
- Self-loop: `start.next is start`, so the `while` body never runs, `last` is `start`, and its `next` becomes None.
- Observation checked by the run: the last node of the cycle is always the list's original tail, because a cycle in a singly linked list is created by the tail pointing back. So the returned index is always n - 1 here.
- Nothing is allocated: three pointers, O(1) space.

**Complexity:** Time O(mu + lambda) = O(n): Phase 1 takes at most mu + lambda steps, the restart takes mu, the cycle walk takes lambda. Space O(1).

**Dry run:** [3,2,0,-4], pos = 1 (index 3 points to index 1).
| step | what happens |
|---|---|
| Floyd phase 1 | slow and fast meet at index 3 |
| restart | pointer at index 0, other at 3. After one step both are at index 1: cycle start |
| walk the cycle | start = 1. 1.next = 2, 2.next = 3, and 3.next is 1, which is the start, so last = 3 |
| cut | index 3's next = None. Return 3. List is 3, 2, 0, -4 |

**Code:**
```python
import random


class ListNode:
    __slots__ = ('val', 'next')

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(arr, pos=-1):
    dummy = ListNode()
    tail, nodes = dummy, []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos != -1:
        tail.next = nodes[pos]
    return dummy.next, nodes


# Brute force: a set of visited node objects; the node whose next is already visited is the one to cut. O(n) space.
def break_brute(head):
    seen, prev = set(), None
    while head is not None:
        if head in seen:
            prev.next = None
            return prev
        seen.add(head)
        prev, head = head, head.next
    return None


# Optimal: Floyd to find the cycle start, then walk the cycle to the node whose next is the start.
def break_floyd(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            break
    else:
        return None                       # no cycle
    start, p = head, slow
    while start is not p:                 # restart step: both meet at the cycle start
        start, p = start.next, p.next
    last = start
    while last.next is not start:         # self-loop: start.next is start, so the loop body never runs
        last = last.next
    last.next = None
    return last


def acyclic(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def run(fn, arr, pos):
    head, nodes = build(arr, pos)
    last = fn(head)
    idx = None if last is None else next(i for i, n in enumerate(nodes) if n is last)
    # walk with a cap so a failed cut cannot hang the test
    out, n = [], head
    while n is not None:
        out.append(n)
        n = n.next
        assert len(out) <= len(nodes), "still cyclic"
    assert acyclic(head)
    assert out == nodes                   # same node objects, same order, none created, none lost
    return idx, [x.val for x in out]


for arr, pos, exp in [([3, 2, 0, -4], 1, 3), ([1, 2], 0, 1), ([1, 2, 3], 2, 2), ([1], -1, None)]:
    for fn in (break_brute, break_floyd):
        idx, vals = run(fn, arr, pos)
        assert idx == exp and vals == arr
    print(arr, 'pos =', pos, '-> cut at index', exp, ', list', arr)

# the cut node is always the original tail; check it exhaustively and with repeated values
rng = random.Random(34)
count = 0
for n in range(0, 25):
    for pos in range(-1, n):
        if n == 0 and pos != -1:
            continue
        arr = [rng.randint(0, 2) for _ in range(n)]
        for fn in (break_brute, break_floyd):
            idx, vals = run(fn, arr, pos)
            assert idx == (n - 1 if pos != -1 else None) and vals == arr
        count += 1
print(count, 'exhaustive (n, pos) cases, n up to 24, repeated values: both match, cut index is always n - 1')
print('empty list ->', break_floyd(None))
```

**Output (my run):**
```text
[3, 2, 0, -4] pos = 1 -> cut at index 3 , list [3, 2, 0, -4]
[1, 2] pos = 0 -> cut at index 1 , list [1, 2]
[1, 2, 3] pos = 2 -> cut at index 2 , list [1, 2, 3]
[1] pos = -1 -> cut at index None , list [1]
325 exhaustive (n, pos) cases, n up to 24, repeated values: both match, cut index is always n - 1
empty list -> None
```

**Edge cases:**
- No cycle: return None and leave the list as it was.
- Empty list: the loop does not run, returns None.
- Self-loop: the cut node is the start itself.
- Cycle includes the head (pos = 0): the restart pointer is already at the start.
- Duplicate values: no problem, since everything compares nodes with `is`.

**Follow-ups:**
- Can you do it without Floyd's restart step? Yes: measure lambda, advance a lead pointer lambda steps, then move two pointers from the head until they meet. That finds the start too.
- Why not just set `slow.next = None` at the meeting node? The meeting point is usually inside the cycle but not the node before the start, so you would cut the cycle in the wrong place and lose nodes.
- What if you must keep the cycle's start reachable? Cutting before the start (this question) keeps every node reachable from the head.

**Common mistakes:**
- Cutting at the meeting node.
- Writing `while last.next != start` with `!=` on values or nodes defined with `__eq__`. Use `is`.
- Forgetting the self-loop case with a loop that starts at `start.next`.
- Checking the result only by values. The test checks identity and order, and that the list is acyclic.

---

### Q35 ⭐ 🔴 Copy a list with random pointers in O(1) extra space. A node is `Node(val, next, random)`, `random` points to any node or None (0 <= len <= 1000). Return a deep copy WITHOUT a hash map: (1) interleave, inserting each copy right after its original, (2) set each copy's `random` to `original.random.next`, (3) unweave the two lists and, so that the INPUT list is restored exactly, put the original nodes back in their original order. State why step 2 is correct only after step 1 and why the order of the steps matters; state the extra space as O(1) apart from the output nodes. Examples write each node as [val, random_index]. Example: [[7,None],[13,0],[11,4],[10,2],[1,0]] -> an equal-structure copy and the input unchanged; [[1,1],[2,1]] -> an equal-structure copy; [[5,0]] -> a copy whose random points to itself; [] -> [].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)
**Pattern:** Interleave, then unweave. Putting each copy right after its original gives every original a direct link to its copy (`original.next`), so the hash map is not needed.

**Say this first (1 line):** "Three passes. One: insert each copy after its original. Two: `copy.random = original.random.next`. Three: unweave into two lists and put the original links back, so the input is exactly as it was."

**Brute force:** Hash map from original node to copy, keyed by the node object (identity). Pass one creates all copies. Pass two sets `next` and `random` through the map. O(n) time, O(n) extra space. Keying by value is wrong: values can repeat, so two different nodes would collapse into one entry.

**Optimal:**
- Step 1 (interleave): for each original `A`, create `A'`, set `A'.next = A.next`, `A.next = A'`. The list becomes A, A', B, B', C, C' ... and moves to the next original with `p = A'.next`.
- Step 2 (randoms): for each original `A`, `A'.random = A.random.next` if `A.random` exists, else None. The copy of any node X is simply `X.next`, so `A.random.next` is the copy of A's random target.
- Why step 2 only works after step 1: before the interleave, nothing connects an original to its copy, so you would need the map. And all copies must exist before any random is set, since a random can point forward.
- Why the order matters between steps 2 and 3: unweaving first would destroy the `X.next` link that step 2 reads.
- Step 3 (unweave): for each original `A` with `c = A.next`: `A.next = c.next`, then `c.next = c.next.next` if it exists. This restores the original chain exactly, and the `random` pointers of the originals were never touched, so the input is unchanged.
- Extra space: O(1) pointers. The n new nodes are the output, not extra space.

**Complexity:** Three linear passes, so O(n) time. Extra space O(1) beyond the output nodes. The map version is O(n) extra space.

**Dry run:** [[1,1],[2,1]]: A(1) has random B, B(2) has random B.
| step | list |
|---|---|
| start | A -> B |
| interleave | A -> A' -> B -> B' |
| randoms | A'.random = A.random.next = B.next = B'. B'.random = B.random.next = B' |
| unweave A | A.next = B; A'.next = B' |
| unweave B | B.next = None; B'.next = None |

Result: A' -> B' with A'.random = B', B'.random = B'. That reads as [[1,1],[2,1]]. The input is A -> B again.

**Code:**
```python
import random


class Node:
    __slots__ = ('val', 'next', 'random')

    def __init__(self, val):
        self.val, self.next, self.random = val, None, None


def build(spec):
    """spec: list of [val, random_index or None]. Returns (head, nodes)."""
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r is not None:
            nodes[i].random = nodes[r]
    return (nodes[0] if nodes else None), nodes


def spec_of(head):
    """Read a list back as [val, random_index]; fails loudly on a cycle or a random pointing outside the list."""
    nodes, p = [], head
    while p is not None:
        nodes.append(p)
        p = p.next
        assert len(nodes) < 10**5, "cycle"
    ix = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, None if n.random is None else ix[id(n.random)]] for n in nodes]


def chain(head):
    out, p = [], head
    while p is not None:
        out.append(p)
        p = p.next
        assert len(out) < 10**5, "cycle"
    return out


# Brute force: dict original -> copy, two passes. O(n) extra space. Keyed by node object (identity), not by value.
def copy_map(head):
    m = {None: None}
    p = head
    while p is not None:
        m[p] = Node(p.val)
        p = p.next
    p = head
    while p is not None:
        m[p].next = m[p.next]
        m[p].random = m[p.random]
        p = p.next
    return m[head]


# Optimal: interleave, set randoms, unweave. Extra space O(1) apart from the output nodes.
def copy_o1(head):
    if head is None:
        return None
    p = head                                   # step 1: A -> A' -> B -> B' -> ...
    while p is not None:
        c = Node(p.val)
        c.next = p.next
        p.next = c
        p = c.next
    p = head                                   # step 2: copy.random = original.random.next
    while p is not None:
        c = p.next
        c.random = p.random.next if p.random is not None else None
        p = c.next
    new_head = head.next                       # step 3: unweave and restore the input
    p = head
    while p is not None:
        c = p.next
        p.next = c.next                        # original links skip the copy
        c.next = c.next.next if c.next is not None else None   # copy links skip the original
        p = p.next
    return new_head


def check(fn, spec):
    head, nodes = build(spec)
    before_chain = chain(head)
    before_rand = [n.random for n in nodes]
    res = fn(head)
    # the copy has equal structure
    assert spec_of(res) == spec, (spec_of(res), spec)
    # no node of the copy is an original node, and the copy has its own nodes
    cp = chain(res)
    assert len(cp) == len(nodes) and not ({id(n) for n in cp} & {id(n) for n in nodes})
    for n in cp:
        assert n.random is None or any(n.random is m for m in cp)     # randoms point inside the copy
    # the input is restored exactly: same nodes, same order, same randoms
    assert chain(head) == before_chain and all(a is b for a, b in zip(chain(head), nodes))
    assert all(a is b for a, b in zip([n.random for n in nodes], before_rand))
    assert not nodes or nodes[-1].next is None
    assert spec_of(head) == spec
    return cp


examples = [
    [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
    [[1, 1], [2, 1]],
    [[5, 0]],
    [],
]
for spec in examples:
    for fn in (copy_map, copy_o1):
        check(fn, spec)
    head, _ = build(spec)
    print(spec, '-> copy', spec_of(copy_o1(head)), '| input after:', spec_of(head))

# a copy of the self-pointing node points at itself, not at the original
head, nodes = build([[5, 0]])
cp = copy_o1(head)
assert cp.random is cp and cp is not nodes[0] and nodes[0].random is nodes[0]
print('self random: copy.random is copy ->', cp.random is cp)

# seeded randomised cross-check, 800 random lists (including many repeated values)
rng = random.Random(35)
for _ in range(800):
    n = rng.randint(0, 12)
    spec = [[rng.randint(0, 3), rng.choice([None] + list(range(n)))] for _ in range(n)]
    check(copy_map, spec)
    check(copy_o1, spec)
print('800 random lists: map copy and O(1) copy both give equal structure, no shared nodes, input restored by identity')

# a long list: iterative, no recursion
spec = [[i, (i * 7) % 1000] for i in range(1000)]
check(copy_o1, spec)
print('1000 nodes OK')
```

**Output (my run):**
```text
[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]] -> copy [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]] | input after: [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]
[[1, 1], [2, 1]] -> copy [[1, 1], [2, 1]] | input after: [[1, 1], [2, 1]]
[[5, 0]] -> copy [[5, 0]] | input after: [[5, 0]]
[] -> copy [] | input after: []
self random: copy.random is copy -> True
800 random lists: map copy and O(1) copy both give equal structure, no shared nodes, input restored by identity
1000 nodes OK
```

**Edge cases:**
- Empty list: return None before touching anything.
- Random is None: copy's random must be None too, so guard `p.random.next`.
- Random points to itself ([[5,0]]): `A'.random = A.next = A'`, so the copy points at itself, not at the original.
- Random points forward or backward: fine, because all copies exist after step 1.
- Last node: `c.next` is None when unweaving, so guard it, or the copy list's tail would fail.
- The test also checks that no copy node is an original node and that the input chain, node order and randoms are unchanged.

**Follow-ups:**
- Is it really O(1) space? Yes, aside from the output; but it modifies the input temporarily, so it is not safe with concurrent readers.
- Why not skip the restore? The caller's list would stay interleaved with copies, and the question demands the input unchanged.
- Recursive version with a map? It uses O(n) stack as well, and Python's recursion limit makes it fail on long lists (Q26).

**Common mistakes:**
- Setting randoms during the interleave pass.
- Unweaving with a single loop and losing track of the next original.
- Forgetting to terminate the copy list: its last `next` must be None.
- Leaving original `next` pointers pointing at copies.
