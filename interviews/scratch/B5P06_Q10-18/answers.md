### Q10 ⭐⭐⭐ 🟡 Intersection of two linked lists. Nodes are `ListNode(val, next)`. Two lists may share a common tail (the same node objects from some point on, not merely equal values). Return the first shared node, or None, in O(m + n) time and O(1) space without modifying either list. Examples give `prefixA`, `prefixB` and `shared` arrays: A is prefixA followed by the shared nodes, B is prefixB followed by the SAME shared nodes. Give the length-difference method and the two-pointer switch trick (when a pointer reaches the end, restart it on the other list's head) and explain why both pointers travel m + n steps and meet at the intersection or both reach None together. Say why comparing `val` is wrong. Example: prefixA [4,1], prefixB [5,6,1], shared [8,4,5] -> the node with value 8; prefixA [1,9,1], prefixB [3], shared [2,4] -> value 2; prefixA [2,6,4], prefixB [1,5], shared [] -> None; prefixA [], prefixB [], shared [7] -> value 7.

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Two pointers on linked lists (alignment by length). Two lists that share a tail have the same distance to the end from the intersection node. If you remove the length difference, the pointers meet there.

**Say this first (1 line):** "Intersection means the same node object, not the same value. I will make both pointers walk A then B, so they cover m + n steps and line up at the shared node, with O(1) space."

**Brute force:** Put every node of A in a set (identity hash), walk B, return the first node that is in the set. O(m + n) time, O(m) space. A nested loop comparing every pair of nodes with `is` is O(m * n) time and O(1) space.

**Optimal:**
- Length-difference method: count m and n. Advance the head of the longer list by |m - n|. Now both are the same distance from the end. Walk together until `a is b`. That node is the answer, or None when both fall off the end together.
- Two-pointer switch trick: `p` starts on A, `q` on B. When a pointer falls off the end (None), put it on the OTHER list's head. Stop when `p is q`.
- Why it works: let the private part of A be a nodes, of B be b nodes, and the shared tail be c nodes. So m = a + c and n = b + c. `p` walks a + c, then b private nodes, then reaches the shared tail: a + c + b steps. `q` walks b + c + a. Both equal m + n, so after the switch both pointers have the same number of nodes left, and they are on the shared tail at the same moment. They meet at its first node.
- No intersection (c = 0): both pointers walk m + n nodes and step onto None at the same time, so `p is q` is True on None and the function returns None. The loop always ends.
- Equal lengths is the easy case: the pointers meet (or reach None together) before any switch.
- Never compare `val`. Values repeat; only `is` says it is the same node.

**Complexity:** Time O(m + n): each pointer walks at most m + n nodes (plus one step onto None). Space O(1): two pointers. Neither list is modified.

**Dry run:** A = 4 -> 1 -> 8 -> 4 -> 5, B = 5 -> 6 -> 1 -> 8 -> 4 -> 5 (the node 8 starts the shared tail). m = 5, n = 6.
- Length method: B is longer by 1, so move B to 6. Now A = 4, B = 6; step together: (1, 1) differ as nodes (different objects, same value), then (8, 8) is the same node. Answer: 8.
- Switch trick: p visits A4, A1, 8, 4, 5, then None (5 steps), then B's head 5, 6, 1, then 8: that is 9 steps. q visits 5, 6, 1, 8, 4, 5, then None (6 steps), then A's head 4, 1, then 8: also 9 steps. Both are on the shared 8 at the same time, so `p is q`.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def make(prefix_a, prefix_b, shared):
    """A = prefix_a + shared, B = prefix_b + the SAME shared node objects."""
    s_head, _ = from_array(shared)
    def with_prefix(prefix):
        dummy = tail = ListNode()
        for v in prefix:
            tail.next = ListNode(v)
            tail = tail.next
        tail.next = s_head
        return dummy.next
    return with_prefix(prefix_a), with_prefix(prefix_b), s_head

def length(h):
    n = 0
    while h:
        n += 1
        h = h.next
    return n

def brute(a, b):                       # O(m + n) time, O(m) space
    seen = set()
    while a:
        seen.add(a)                    # default hash is identity
        a = a.next
    while b:
        if b in seen:
            return b
        b = b.next
    return None

def by_length(a, b):                   # O(m + n) time, O(1) space
    m, n = length(a), length(b)
    while m > n:
        a = a.next; m -= 1             # skip the extra head of the longer list
    while n > m:
        b = b.next; n -= 1
    while a is not b:                  # same distance to the end: walk together
        a, b = a.next, b.next
    return a                           # the shared node, or None when both ran off

def switch(a, b, counter=None):        # O(m + n) time, O(1) space
    p, q = a, b
    while p is not q:
        p = p.next if p else b         # at the end (None), restart on the OTHER list
        q = q.next if q else a
        if counter is not None:
            counter[0] += 1
    return p

# the four examples
for pa, pb, sh, want in (([4, 1], [5, 6, 1], [8, 4, 5], 8), ([1, 9, 1], [3], [2, 4], 2),
                         ([2, 6, 4], [1, 5], [], None), ([], [], [7], 7)):
    a, b, s = make(pa, pb, sh)
    ia, ib = node_ids(a), node_ids(b)
    for f in (brute, by_length, switch):
        r = f(a, b)
        assert r is (s if sh else None)
        assert (r.val if r else None) == want
    assert node_ids(a) == ia and node_ids(b) == ib       # nothing modified
    print(pa, pb, sh, '->', want)

# exhaustive over small shapes; ALL values are 0, so a value comparison cannot tell nodes apart
cases = 0
for la in range(5):
    for lb in range(5):
        for ls in range(5):
            a, b, s = make([0] * la, [0] * lb, [0] * ls)
            for f in (brute, by_length, switch):
                assert f(a, b) is (s if ls else None), (la, lb, ls, f.__name__)
            cnt = [0]
            switch(a, b, cnt)
            if ls == 0:
                # equal lengths: they hit None together after m steps; else after m + n node steps plus the step onto None
                assert cnt[0] == (la if la == lb else la + lb + 1)
            cases += 1
print('exhaustive shapes ok:', cases)

# no shared tail but equal values: val comparison would say 'intersect', identity says None
a, _ = from_array([1, 2, 3]); b, _ = from_array([1, 2, 3])
assert switch(a, b) is None and brute(a, b) is None and by_length(a, b) is None
print('equal values, different nodes -> None')

# seeded random cross-check (values drawn from 0..2 so they repeat)
random.seed(10)
for _ in range(500):
    pa = [random.randint(0, 2) for _ in range(random.randint(0, 8))]
    pb = [random.randint(0, 2) for _ in range(random.randint(0, 8))]
    sh = [random.randint(0, 2) for _ in range(random.randint(0, 6))]
    a, b, s = make(pa, pb, sh)
    ans = s if sh else None
    assert brute(a, b) is ans and by_length(a, b) is ans and switch(a, b) is ans
print('random cross-check ok (500 cases)')
```

**Output (my run):**
```
[4, 1] [5, 6, 1] [8, 4, 5] -> 8
[1, 9, 1] [3] [2, 4] -> 2
[2, 6, 4] [1, 5] [] -> None
[] [] [7] -> 7
exhaustive shapes ok: 125
equal values, different nodes -> None
random cross-check ok (500 cases)
```

**Edge cases:**
- Either list empty: no intersection, return None (both pointers reach None together).
- Both lists are the same list (shared tail is the whole list, empty prefixes): the pointers are equal at the start.
- Shared tail is a single node (the last node).
- Equal values but different nodes: answer is None.
- Equal lengths with no intersection: they reach None together after m steps.

**Follow-ups:**
- What if a list may contain a cycle? Then the lists may meet inside the cycle or not at all; detect a cycle in each first (Floyd, Q4 in this part). The simple methods above assume no cycle.
- Can you modify the lists? Yes, but do not: you can link A's tail to A's head, so the cycle start found from B's head (Q6) is the intersection, then undo the link. It is O(1) space but mutates the input, so it is worse than the two-pointer trick.
- Hash set or two pointers? Say the set first as the baseline, then reduce the space.

**Common mistakes:**
- Comparing `p.val == q.val` instead of `p is q`.
- Switching on `p.next is None` instead of on `p is None`, so a no-intersection case never reaches None together and loops forever.
- Forgetting that the switch step lands on None and that None must be compared too.
- Mutating a list to mark visited nodes and leaving it broken.

### Q11 ⭐⭐⭐ 🟡 Copy a list with random pointers. A list node is `Node(val, next, random)` where `random` points to any node in the list or None (0 <= len <= 1000). Return a DEEP copy: new nodes with the same values whose `next` and `random` point only to new nodes (the tests check that no node of the copy is a node of the original, and that the pointer structure matches). Examples write each node as [val, random_index], where random_index is the position of its random target or None. Give the hash-map solution (original node to copy, two passes, O(n) space) and explain why a map keyed by node identity is needed rather than by value. The O(1)-extra-space variant is a separate question later in this part. Example: [[7,None],[13,0],[11,4],[10,2],[1,0]] -> an equal-structure copy; [[1,1],[2,1]] -> an equal-structure copy; [] -> [].

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Hash map from old node to new node (clone with a lookup table). The `random` pointer can point forward or backward, so one left-to-right pass cannot wire it; you need every copy to exist first.

**Say this first (1 line):** "Pass one creates a copy of every node and stores it in a dict keyed by the original node object. Pass two wires `next` and `random` through that dict."

**Brute force:** Copy the `next` chain first. Then for each node, scan the original list from the head to find the position of its `random` target and use the copy at that position. O(n^2) time, O(n) for the copies themselves. It works but is slow when n is large.

**Optimal:**
- Dict `old_to_new`, with `None -> None` pre-stored so a missing `next` or `random` needs no `if`.
- Pass 1: walk the original list and create `Node(cur.val)` for each node, `old_to_new[cur] = copy`.
- Pass 2: walk again and set `copy.next = old_to_new[cur.next]` and `copy.random = old_to_new[cur.random]`.
- Why keyed by identity: two nodes can have the same value, and two random pointers can point at different nodes with that value. A `val` key merges them into one copy and the structure is wrong (the output shows it). `ListNode`/`Node` define no `__eq__` or `__hash__`, so the default hash is identity and the node itself is a safe key.
- Invariant after pass 1: every original node has exactly one copy in the dict. Pass 2 therefore never meets a missing key.

**Complexity:** Time O(n): two walks and O(1) dict operations on average. Space O(n) for the dict plus the n new nodes (the output itself is O(n), so the extra space is the dict). The O(1) extra-space variant is a separate question later in this part.

**Dry run:** spec [[1,1],[2,1]]: nodes A(1), B(2); A.random = B, B.random = B.
- Pass 1: dict {A: A', B: B'}.
- Pass 2 at A: A'.next = dict[B] = B', A'.random = dict[B] = B'. At B: B'.next = dict[None] = None, B'.random = dict[B] = B'.
- Copy spec: [[1,1],[2,1]]. Same as input, and A', B' are new objects.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


class Node:
    __slots__ = ('val', 'next', 'random')
    def __init__(self, val=0, next=None, random=None):
        self.val, self.next, self.random = val, next, random

def build_random(spec):
    """spec = [[val, random_index_or_None], ...] -> (head, nodes)."""
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r is not None:
            nodes[i].random = nodes[r]
    return (nodes[0] if nodes else None), nodes

def chain(head, cap=10**5):
    out = []
    while head is not None:
        out.append(head)
        head = head.next
        assert len(out) <= cap, "cycle in next chain"
    return out

def to_spec(head):
    nodes = chain(head)
    index = {id(n): i for i, n in enumerate(nodes)}
    return [[n.val, None if n.random is None else index[id(n.random)]] for n in nodes]

def copy_brute(head):
    """O(n^2): find every random target by scanning for its position."""
    nodes = chain(head)
    copies = [Node(n.val) for n in nodes]
    for i, n in enumerate(nodes):
        if i + 1 < len(nodes):
            copies[i].next = copies[i + 1]
        if n.random is not None:
            j = 0
            while nodes[j] is not n.random:
                j += 1
            copies[i].random = copies[j]
    return copies[0] if copies else None

def copy_map(head):
    """O(n) time, O(n) space: dict original node -> copy (keyed by node identity)."""
    old_to_new = {None: None}          # maps None -> None so next/random of None need no branch
    cur = head
    while cur:                         # pass 1: create every copy
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:                         # pass 2: wire next and random through the map
        new = old_to_new[cur]
        new.next = old_to_new[cur.next]
        new.random = old_to_new[cur.random]
        cur = cur.next
    return old_to_new[head]

def copy_by_value_WRONG(head):         # keyed by val: duplicate values collide
    by_val = {None: None}
    cur = head
    while cur:
        by_val[cur.val] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        new = by_val[cur.val]
        new.next = by_val[cur.next.val] if cur.next else None
        new.random = by_val[cur.random.val] if cur.random else None
        cur = cur.next
    return by_val[head.val] if head else None

def check_copy(spec, f):
    head, nodes = build_random(spec)
    before = [id(n) for n in chain(head)]
    c = f(head)
    assert to_spec(c) == spec, (spec, to_spec(c))                  # same structure
    assert {id(n) for n in chain(c)}.isdisjoint(before)             # no node of the copy is an original
    for n in chain(c):                                              # random targets are copies too
        assert n.random is None or id(n.random) in {id(x) for x in chain(c)}
    assert [id(n) for n in chain(head)] == before and to_spec(head) == spec   # input untouched

examples = [[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]], [[1, 1], [2, 1]], []]
for spec in examples:
    for f in (copy_brute, copy_map):
        check_copy(spec, f)
    print(spec, '-> copy has the same structure, no shared nodes')

# a value-keyed map breaks on repeated values
spec = [[1, 1], [1, 0]]
head, _ = build_random(spec)
print('value-keyed copy of', spec, 'gives', to_spec(copy_by_value_WRONG(head)) if head else None, '(wrong)')
assert to_spec(copy_by_value_WRONG(head)) != spec

# seeded random cross-check, values repeat on purpose
random.seed(11)
for _ in range(400):
    n = random.randint(0, 12)
    spec = [[random.randint(0, 3), random.choice([None] + list(range(n)))] for _ in range(n)]
    for f in (copy_brute, copy_map):
        check_copy(spec, f)
big = [[0, (i * 7) % 1000] for i in range(1000)]                    # max size
check_copy(big, copy_map)
print('random cross-check ok (400 cases + n=1000)')
```

**Output (my run):**
```
[[7, None], [13, 0], [11, 4], [10, 2], [1, 0]] -> copy has the same structure, no shared nodes
[[1, 1], [2, 1]] -> copy has the same structure, no shared nodes
[] -> copy has the same structure, no shared nodes
value-keyed copy of [[1, 1], [1, 0]] gives [[1, 0]] (wrong)
random cross-check ok (400 cases + n=1000)
```

**Edge cases:**
- Empty list: return None (the dict holds only `None`, so `old_to_new[head]` is None).
- `random` is None, points to itself, or points backward or forward.
- Repeated values with different random targets (the value-keyed version fails here).
- All random pointers point to the same node.

**Follow-ups:**
- O(1) extra space? Interleave each copy after its original, set `copy.random = original.random.next`, then split the two lists apart and restore the original. That is the separate question later in this part.
- Recursive version with the dict as a memo? Works, but the depth equals the list length, so see Q26 in this part for the recursion limit.
- How do you test it? Compare structure by position index, and assert that no node of the copy is a node of the original.

**Common mistakes:**
- Keying by value.
- Setting `random` in the same pass that creates nodes, so a forward target has no copy yet.
- Forgetting to map None.
- Making the copy's `random` point back into the original list.

### Q12 ⭐⭐⭐ 🔴 Merge k sorted linked lists. Nodes are `ListNode(val, next)`. `lists` holds k sorted lists (0 <= k <= 100, total nodes N <= 10^4, a list may be empty). Return one sorted list reusing the nodes; ties keep the lower list index first (stable). Give three solutions and their costs: merging one list into an accumulated result (O(kN)), a `heapq` of (value, list index, node) used only as the merge tool (O(N log k); heap theory itself is Part 8; say why the list index must be in the tuple, since two ListNode objects are not orderable), and pairwise divide and conquer (O(N log k)). Explain how the heap holds at most k nodes. Example: [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]; [] -> []; [[]] -> []; [[],[2],[]] -> [2].

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Merge of sorted sequences. The two-list merge (Q3 in this part) is the building block. Either keep "the smallest front node" with a heap, or reduce k lists to one by merging pairs.

**Say this first (1 line):** "k lists, N nodes in total. Merging one at a time into a result is O(kN). A heap of the k front nodes, or merging pairs in rounds, is O(N log k). Ties go to the lower list index."

**Brute force:** Merge one list at a time into an accumulated result: `result = merge2(result, list_i)`. The result grows, and each merge re-walks it, so the cost is O(kN) in the worst case (for k lists of N/k nodes each, the accumulated sizes are N/k, 2N/k, ... , N, so about kN/2 node steps in total). Another baseline: dump all values into a Python list, sort, rebuild (O(N log N) time, O(N) space, new nodes), which does not reuse the nodes.

**Optimal:**
- Heap: put `(val, list_index, node)` for each non-empty list head in a `heapq` min-heap. Pop the smallest, append that node to the output, push the popped node's successor if it exists.
- Why the heap holds at most k nodes: it has one entry per list (a list is represented by its current front node). Each pop is followed by at most one push from the same list.
- Why `list_index` is in the tuple: tuples compare element by element. If two values tie, Python compares the next element. `ListNode` objects are not orderable, so `(1, nodeA) < (1, nodeB)` raises `TypeError` (the output shows it). The index breaks ties, and it is also what makes the merge stable: equal values come out in list order. `(val, i)` is always unique inside the heap (one entry per list), so the node itself is never compared.
- Heap theory (sift up/down, why `heapify` is O(k)) is Part 8; here it is only a tool.
- Divide and conquer: merge lists 0+1, 2+3, ... in a round, then merge the results in the next round. There are about log2(k) rounds, and each round touches every node once, so O(N log k). It uses `merge2` from Q3, which is stable (first list wins ties), and merging neighbours keeps list order, so the whole thing is stable. It needs O(1) extra space (a Python list of heads in each round is O(k)).

**Complexity:**
- Accumulate: O(kN) time worst case, O(1) extra space.
- Heap: O(N log k) time (each of N nodes is popped and pushed once at O(log k)), O(k) space for the heap.
- Divide and conquer: O(N log k) time, O(1) extra for the merging, O(k) for the list of heads (the recursion version would use O(log k) stack).

**Dry run:** [[1,4,5],[1,3,4],[2,6]].
- Heap starts with (1,0,A1), (1,1,B1), (2,2,C2). Pop (1,0): output 1 (from list 0), push (4,0). Pop (1,1): output 1 (from list 1), push (3,1). Pop (2,2): push (6,2). Pop (3,1): push (4,1). Pop (4,0): push (5,0). Pop (4,1). Pop (5,0). Pop (6,2).
- Output: 1,1,2,3,4,4,5,6. The first 1 is from list 0 because the index 0 < 1.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

import heapq

def merge2(a, b):
    """Stable merge: on a tie the node from a comes first. Reuses nodes."""
    dummy = tail = ListNode()
    while a and b:
        if b.val < a.val:
            tail.next = b; b = b.next
        else:
            tail.next = a; a = a.next
        tail = tail.next
    tail.next = a or b
    return dummy.next

def merge_accumulate(lists):           # O(k * N): the result is re-walked on every merge
    result = None
    for head in lists:
        result = merge2(result, head)  # result first, so ties keep the lower list index first
    return result

def merge_heap(lists):                 # O(N log k)
    heap = [(h.val, i, h) for i, h in enumerate(lists) if h]
    heapq.heapify(heap)                # at most k entries: one node per list
    peak = len(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node; tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
        peak = max(peak, len(heap))
    tail.next = None
    merge_heap.peak = peak
    return dummy.next

def merge_dc(lists):                   # O(N log k): merge neighbours pairwise, round by round
    if not lists:
        return None
    while len(lists) > 1:
        lists = [merge2(lists[i], lists[i + 1]) if i + 1 < len(lists) else lists[i]
                 for i in range(0, len(lists), 2)]
    return lists[0]

def build_all(arrays):
    heads, all_nodes = [], []
    for arr in arrays:
        h, ns = from_array(arr)
        heads.append(h); all_nodes.append(ns)
    return heads, all_nodes

def expected_ids(all_nodes):
    """Stable order: by value, then list index, then position inside the list."""
    flat = [(n.val, li, pos, id(n)) for li, ns in enumerate(all_nodes) for pos, n in enumerate(ns)]
    return [t[3] for t in sorted(flat)]

# the four examples
for arrays, want in (([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]), ([], []), ([[]], []), ([[], [2], []], [2])):
    for f in (merge_accumulate, merge_heap, merge_dc):
        heads, ns = build_all(arrays)
        r = f(heads)
        assert to_array(r) == want, (f.__name__, arrays)
        assert node_ids(r) == expected_ids(ns)          # same nodes, stable order
    print(arrays, '->', want)

# ListNode objects cannot be compared, so a (val, node) heap entry breaks on a tie
a, b = ListNode(1), ListNode(1)
try:
    heapq.heappush([(1, a)], (1, b))
    raise SystemExit('expected TypeError')
except TypeError as e:
    print('without the list index:', e)

# seeded random cross-check on shapes with many ties
random.seed(12)
for _ in range(500):
    k = random.randint(0, 8)
    arrays = [sorted(random.randint(0, 5) for _ in range(random.randint(0, 6))) for _ in range(k)]
    want = sorted(v for arr in arrays for v in arr)
    for f in (merge_accumulate, merge_heap, merge_dc):
        heads, ns = build_all(arrays)
        r = f(heads)
        assert to_array(r) == want
        assert node_ids(r) == expected_ids(ns)
# the heap never holds more than k nodes
heads, _ = build_all([[i, i + 100, i + 200] for i in range(7)])
merge_heap(heads)
assert merge_heap.peak <= 7
print('heap peak size for k = 7:', merge_heap.peak)
# max-ish size: k = 100, N = 10^4
arrays = [sorted(random.randint(0, 50) for _ in range(100)) for _ in range(100)]
for f in (merge_accumulate, merge_heap, merge_dc):
    heads, ns = build_all(arrays)
    r = f(heads)
    assert node_ids(r) == expected_ids(ns) and len(node_ids(r)) == 10**4
print('random cross-check ok (500 cases + k=100, N=10^4)')
```

**Output (my run):**
```
[[1, 4, 5], [1, 3, 4], [2, 6]] -> [1, 1, 2, 3, 4, 4, 5, 6]
[] -> []
[[]] -> []
[[], [2], []] -> [2]
without the list index: '<' not supported between instances of 'ListNode' and 'ListNode'
heap peak size for k = 7: 7
random cross-check ok (500 cases + k=100, N=10^4)
```

**Edge cases:**
- `lists = []` (k = 0): return None. The heap version returns None because the heap is empty; the pairwise version needs the explicit check.
- Lists that are empty (`[[]]`, `[[], [2], []]`): skip empty lists when building the heap.
- All equal values: ties everywhere, so stability and the index matter.
- One list: the heap loop just copies it.

**Follow-ups:**
- Why not a heap of all N nodes? Heap size N makes each operation O(log N); using one front node per list keeps it at O(log k).
- Which is better in Python? The heap is simpler to write. Divide and conquer needs no heap and does O(1) extra pointer work, but both have the same big-O.
- Can the heap version be written with `(val, i)` only? You need the node too, because the heap has to give you the node to link.

**Common mistakes:**
- Pushing `(val, node)` without the index: TypeError on ties.
- Pushing all nodes of all lists up front (O(N) heap, defeats the purpose).
- Leaving stale links when you reuse nodes. In the heap code the last popped node's `next` is already None, so `tail.next = None` is a harmless safety line; in other rearrangements a missing final `= None` makes a cycle.
- Merging with `<=` on the wrong side and breaking stability.

### Q13 ⭐⭐⭐ 🔴 Reverse nodes in k-groups. Nodes are `ListNode(val, next)`. Given a list (1 <= len <= 5000) and an integer k with 1 <= k <= len, reverse the nodes k at a time and return the new head; if fewer than k nodes remain at the end, leave that last group as it is. Only links may change, not values (tests check identity). Use a dummy head, a `group_prev` pointer, a check that k nodes remain before reversing, and a reversal of exactly k nodes that reconnects both ends. O(n) time, O(1) space; mention the recursive version and its O(n/k) stack. Example: [1,2,3,4,5], k=2 -> [2,1,4,3,5]; [1,2,3,4,5], k=3 -> [3,2,1,4,5]; [1,2,3], k=1 -> [1,2,3]; [1,2,3,4], k=4 -> [4,3,2,1].

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Reverse a fixed-size window of a linked list, repeated. The pieces are: a dummy head, a `group_prev` pointer that sits just before each group, a "do k nodes remain?" check, and the three-pointer reversal of exactly k nodes (Q1 in this part).

**Say this first (1 line):** "For each group: check that k nodes remain, reverse exactly k nodes with the first node of the next group as the starting `prev`, then reconnect `group_prev` to the new head and move it to the old head."

**Brute force:** Copy the values to a Python list, reverse each full block of k with a slice, and rebuild. O(n) time, O(n) space, and it changes values or builds new nodes, which the question forbids. (The code uses this version only as the checker.)

**Optimal:**
- `dummy -> head`; `group_prev = dummy`.
- Loop: walk `kth = group_prev` forward k times. If you fall off the end, fewer than k nodes remain: return `dummy.next`. The tail group is left alone.
- `group_next = kth.next` is the first node after the group.
- Reverse k nodes with `prev = group_next` as the starting value instead of None. Then the old first node's `next` already points at `group_next`, so the tail end reconnects with no extra line.
- After the loop `prev` is the old k-th node, now the new first node. Set `group_prev.next = prev`. The old first node (`first = group_prev.next`, saved before) is now the group's tail, so it becomes the new `group_prev`.
- Invariant: everything up to `group_prev` is finished and linked; everything after it is untouched.
- Recursive version: reverse the first k nodes, call itself on the rest, and attach the result. There is one call per group, so the stack depth is about n/k. For k = 1 that is n, which overflows Python's default limit of 1000 (see Q26 in this part; the output shows the failure).

**Complexity:** Time O(n): the check walks k nodes and the reversal walks k nodes per group, so about 2n steps. Space O(1) for the iterative version. Recursive: O(n/k) stack.

**Dry run:** [1,2,3,4,5], k = 3. `group_prev` = dummy. `kth` reaches 3, `group_next` = 4. Reverse 1,2,3 with `prev` starting at node 4: 1.next = 4, 2.next = 1, 3.next = 2; `prev` = node 3. `dummy.next` = 3. `group_prev` = node 1. List so far: 3 -> 2 -> 1 -> 4 -> 5. Next round: from node 1 walk 3 steps: 4, 5, then None, so stop. Result [3,2,1,4,5].

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def brute(arr, k):                     # on a Python list: reverse each full block of k
    out = []
    for i in range(0, len(arr), k):
        block = arr[i:i + k]
        out += block[::-1] if len(block) == k else block
    return out

def reverse_k_group(head, k):          # iterative: O(n) time, O(1) space
    dummy = ListNode(0, head)
    group_prev = dummy                 # last node of the already-finished part
    while True:
        kth = group_prev
        for _ in range(k):             # are there k nodes left?
            kth = kth.next
            if kth is None:
                return dummy.next      # fewer than k left: leave them as they are
        group_next = kth.next          # first node after this group
        prev, cur = group_next, group_prev.next      # start 'prev' at group_next so the tail reconnects
        for _ in range(k):             # reverse exactly k nodes
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        first = group_prev.next        # the old first node is now the group's tail
        group_prev.next = prev         # prev = old kth = new first node of the group
        group_prev = first

depth = [0, 0]                         # [current depth, max depth] for the recursive version
def reverse_k_group_rec(head, k):
    depth[0] += 1; depth[1] = max(depth[1], depth[0])
    node, count = head, 0
    while node and count < k:          # find the start of the next group
        node = node.next; count += 1
    if count < k:
        depth[0] -= 1
        return head                    # short tail: unchanged
    new_tail_next = reverse_k_group_rec(node, k)     # solve the rest first
    prev, cur = new_tail_next, head
    for _ in range(k):                 # reverse this group, ending on the solved rest
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    depth[0] -= 1
    return prev

def run(f, arr, k):
    head, nodes = from_array(arr)
    r = f(head, k)
    ids = node_ids(r)
    assert sorted(ids) == sorted(id(n) for n in nodes)      # same node objects, none lost, none repeated
    return to_array(r), ids

for arr, k, want in (([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]), ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),
                     ([1, 2, 3], 1, [1, 2, 3]), ([1, 2, 3, 4], 4, [4, 3, 2, 1])):
    for f in (reverse_k_group, reverse_k_group_rec):
        assert run(f, arr, k)[0] == want == brute(arr, k)
    print(arr, 'k =', k, '->', want)

# exhaustive: every length 1..14 and every k in 1..len, values all distinct
for n in range(1, 15):
    for k in range(1, n + 1):
        arr = list(range(n))
        depth[1] = 0
        a, ids_a = run(reverse_k_group, arr, k)
        b, _ = run(reverse_k_group_rec, arr, k)
        assert a == b == brute(arr, k)
        assert depth[1] <= n // k + 1                       # recursion depth ~ n / k
print('exhaustive n=1..14, all k ok')

# identity: the k nodes of a group are the same objects in reverse order
head, nodes = from_array(list(range(6)))
r = reverse_k_group(head, 3)
assert node_ids(r) == [id(n) for n in (nodes[2], nodes[1], nodes[0], nodes[5], nodes[4], nodes[3])]

# seeded random cross-check with repeated values
random.seed(13)
for _ in range(500):
    n = random.randint(1, 40); k = random.randint(1, n)
    arr = [random.randint(0, 3) for _ in range(n)]
    assert run(reverse_k_group, arr, k)[0] == brute(arr, k)
# max size, iterative only: no recursion trouble
arr = list(range(5000))
assert run(reverse_k_group, arr, 7)[0] == brute(arr, 7)
depth[1] = 0
assert run(reverse_k_group_rec, arr, 7)[0] == brute(arr, 7)
print('recursive depth for n=5000, k=7:', depth[1], '(about n/k =', 5000 // 7, ')')
print('random cross-check ok (500 cases + n=5000)')
# k = 1 makes the recursive depth n, so 5000 nodes overflow the default recursion limit of 1000
try:
    run(reverse_k_group_rec, arr, 1)
    print('unexpected: no error')
except RecursionError:
    print('recursive version, n=5000, k=1: RecursionError (depth ~ n / k = 5000)')
assert run(reverse_k_group, arr, 1)[0] == arr
```

**Output (my run):**
```
[1, 2, 3, 4, 5] k = 2 -> [2, 1, 4, 3, 5]
[1, 2, 3, 4, 5] k = 3 -> [3, 2, 1, 4, 5]
[1, 2, 3] k = 1 -> [1, 2, 3]
[1, 2, 3, 4] k = 4 -> [4, 3, 2, 1]
exhaustive n=1..14, all k ok
recursive depth for n=5000, k=7: 715 (about n/k = 714 )
random cross-check ok (500 cases + n=5000)
recursive version, n=5000, k=1: RecursionError (depth ~ n / k = 5000)
```

**Edge cases:**
- k = 1: nothing changes (every group is one node).
- k = len: the whole list is reversed.
- len is a multiple of k: no leftover group.
- Leftover group of fewer than k nodes stays in the original order.
- Single node (k = 1 is the only legal k).

**Follow-ups:**
- Reverse the leftover group too (or alternate groups)? Drop the "k nodes remain" check and count how many you actually have, or flip a flag per group.
- Reverse in groups counted from the END? Reverse the whole list, apply this, reverse again, or compute the length and skip n % k nodes first.
- Why is it still O(1) space with a dummy? The dummy is one node, not a function of n.

**Common mistakes:**
- Reversing first and checking length later, which leaves a short tail reversed.
- Starting `prev = None` and forgetting to reconnect the group tail to `group_next`.
- Moving `group_prev` to the new first node instead of the old first node (now the group's tail).
- Losing the old head of the group before `group_prev.next` is reassigned.

### Q14 ⭐⭐ 🟢 Delete a node when you are given only that node. Nodes are `ListNode(val, next)`. You get a reference `node` that is in a singly linked list but is NOT the tail (the list has at least 2 nodes), and no head. Delete it from the list in O(1). The trick is to copy the next node's value into this node and bypass the next node; explain why this is not a true deletion of the given node object, what it breaks (other references to the next node, identity checks) and why it cannot work for the tail. Example: [4,5,1,9] deleting the node with value 5 -> [4,1,9]; [4,5,1,9] deleting the node with value 1 -> [4,5,9]; [1,2] deleting the node with value 1 -> [2]; [0,1,2,3] deleting the node with value 0 -> [1,2,3].

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Pointer rewiring with a trick: when you cannot reach the previous node, you cannot unlink the given node, so you make the given node BECOME its successor and unlink the successor instead.

**Say this first (1 line):** "I cannot get to the previous node, so I copy the next node's value into this node and skip the next node. It is O(1), but it only works if the node is not the tail, and what really leaves the list is the successor object."

**Brute force:** Without the head you cannot walk to the previous node, so the "normal" delete (find `prev`, set `prev.next = node.next`) is impossible. If you did have the head, it would be an O(n) walk. With only the node, the one trick below is the intended answer.

**Optimal:**
- `node.val = node.next.val`
- `node.next = node.next.next`
- Two lines, O(1) time and space.
- The list now reads as if the given value had been removed, but the object you were handed is still in the list (holding the successor's value), and the SUCCESSOR object is the one that left.
- What it breaks:
  - A reference someone else keeps to the successor now points at a node that is no longer in the list (it still has its old `next`, so it looks fine but is detached). Later changes through that reference do not affect the list.
  - Identity checks: code that remembers `node` expecting it to be gone finds it still in the list with a different value.
  - A node that holds heavy data or has side effects on deletion (for example, a destructor or a hash map entry pointing to the node) is not cleaned up.
- Why not the tail: `node.next` is None, so `node.next.val` raises `AttributeError` (the output shows it). There is no successor to copy from, and you cannot make a node "become" None.

**Complexity:** Time O(1), space O(1).

**Dry run:** [4,5,1,9], delete the node holding 5. `node.val = node.next.val` sets it to 1: 4 -> 1 -> 1 -> 9. `node.next = node.next.next`: 4 -> 1 -> 9. The old node holding 1 (the successor) is out; the node we were given now holds 1.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def delete_node(node):
    """O(1). node is not the tail. Copy the successor's value in, then bypass the successor."""
    node.val = node.next.val
    node.next = node.next.next

def brute(arr, idx):                   # delete by index in a Python list
    return arr[:idx] + arr[idx + 1:]

# the four examples: the node to delete is chosen by its value
for arr, v, want in (([4, 5, 1, 9], 5, [4, 1, 9]), ([4, 5, 1, 9], 1, [4, 5, 9]),
                     ([1, 2], 1, [2]), ([0, 1, 2, 3], 0, [1, 2, 3])):
    head, nodes = from_array(arr)
    target = next(n for n in nodes if n.val == v)
    delete_node(target)
    assert to_array(head) == want == brute(arr, arr.index(v))
    print(arr, 'delete value', v, '->', want)

# what really happened: the given NODE OBJECT survives, the SUCCESSOR object is the one that left the list
head, nodes = from_array([4, 5, 1, 9])
node, successor = nodes[1], nodes[2]
other_ref = successor                  # someone else holds the successor
delete_node(node)
ids = node_ids(head)
assert id(node) in ids                 # the node we were given is still in the list (now holding 1)
assert id(successor) not in ids        # the successor object is gone from the list
assert other_ref.val == 1 and other_ref.next is nodes[3]   # but the stale reference still looks like a list node
print('given node still in list:', id(node) in ids, '| successor still in list:', id(successor) in ids,
      '| given node value now:', node.val)

# the tail cannot be deleted this way
head, nodes = from_array([1, 2, 3])
try:
    delete_node(nodes[-1])
except AttributeError as e:
    print('tail:', type(e).__name__, '-', e)
else:
    raise SystemExit('expected failure')

# seeded random cross-check: delete every non-tail position of random lists
random.seed(14)
for _ in range(300):
    n = random.randint(2, 15)
    arr = [random.randint(0, 4) for _ in range(n)]
    idx = random.randint(0, n - 2)
    head, nodes = from_array(arr)
    before = node_ids(head)
    delete_node(nodes[idx])
    assert to_array(head) == brute(arr, idx)
    assert node_ids(head) == before[:idx + 1] + before[idx + 2:]    # exactly one node object left: the successor
print('random cross-check ok (300 cases)')
```

**Output (my run):**
```
[4, 5, 1, 9] delete value 5 -> [4, 1, 9]
[4, 5, 1, 9] delete value 1 -> [4, 5, 9]
[1, 2] delete value 1 -> [2]
[0, 1, 2, 3] delete value 0 -> [1, 2, 3]
given node still in list: True | successor still in list: False | given node value now: 1
tail: AttributeError - 'NoneType' object has no attribute 'val'
random cross-check ok (300 cases)
```

**Edge cases:**
- Node is the second-to-last: after the call it becomes the new tail (its `next` is None).
- Node is the head (the head reference the caller holds stays valid; it now holds the second value).
- List of exactly 2 nodes, deleting the first.
- Tail: not supported; state the precondition and say what you would do (return an error or use a different API).

**Follow-ups:**
- Why does the problem guarantee a non-tail node? Because of exactly the failure shown above.
- Can you delete the tail with only the node? No. You need the previous node. A doubly linked list (Q29 in this part) can, because `node.prev` exists.
- Is it a "real" delete in a language with manual memory? No: the freed object is the successor, not the node you passed in, which matters in C++ with raw pointers.

**Common mistakes:**
- Setting only `node.next = node.next.next` (that removes the successor and keeps the node's own value).
- Trying to use it on the tail.
- Claiming other references to the given node are invalidated; it is the references to the successor that go stale.

### Q15 ⭐⭐ 🟢 Remove duplicates from a sorted linked list. Nodes are `ListNode(val, next)`. The list is sorted ascending (0 <= len <= 300). Delete nodes so each value appears once (keep the FIRST node of each run) and return the head, in place. Explain why you only need to compare a node with its successor, why you do not advance when you delete, and why no dummy is needed here (the head never changes) while it is needed for the 'remove all duplicated values' variant that is a separate question. Example: [1,1,2] -> [1,2]; [1,1,2,3,3] -> [1,2,3]; [5,5,5] -> [5]; [] -> []; [1,2,3] -> [1,2,3].

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** One pointer walking a sorted list and comparing a node with its successor. Because the list is sorted, equal values sit in one run, so duplicates are always adjacent.

**Say this first (1 line):** "Sorted means duplicates are neighbours. I compare `cur` with `cur.next`; if equal I unlink the successor and stay put, otherwise I advance."

**Brute force:** Copy values into a Python list, build `[k for k, _ in groupby(arr)]`, and make a new list. O(n) time, O(n) space, new nodes. For an unsorted list you would need a set (Q27 in this part).

**Optimal:**
- `cur = head`. While `cur and cur.next`:
  - if `cur.val == cur.next.val`: `cur.next = cur.next.next` (delete the successor, keep the FIRST node of the run). Do not advance: the new successor may be another copy.
  - else `cur = cur.next`.
- Why only the successor: sorted order means any later copy of `cur.val` is in the same run right after `cur`.
- Why no dummy: the first node of the first run is never deleted, so the head never changes. For "remove all duplicated values" (Q24 in this part) the head itself may go, so a dummy is needed.
- Not advancing after a delete matters: with [5,5,5], advancing after the first delete leaves [5,5] (the output shows this bug).

**Complexity:** Time O(n): each step either advances `cur` or removes a node, so at most 2n steps. Space O(1).

**Dry run:** [1,1,2,3,3]. cur=1, next=1 equal: unlink, list 1,2,3,3. cur=1, next=2 differ: advance. cur=2, next=3: advance. cur=3, next=3 equal: unlink. cur=3, next None: stop. Result [1,2,3].

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

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
```

**Output (my run):**
```
[1, 1, 2] -> [1, 2]
[1, 1, 2, 3, 3] -> [1, 2, 3]
[5, 5, 5] -> [5]
[] -> []
[1, 2, 3] -> [1, 2, 3]
exhaustive sorted lists ok: 330
buggy version on [5, 5, 5]: [5, 5]
random cross-check ok (300 cases + 300 equal values)
```

**Edge cases:**
- Empty list and single node: loop does not run.
- All equal (one long run): one node survives, and it is the first one.
- No duplicates: nothing changes.
- Duplicates at the end: `cur.next` becomes None and the loop ends.

**Follow-ups:**
- Keep none of the duplicated values? Q24 in this part: dummy plus `prev` that trails the last kept node.
- Unsorted input? Use a set of seen values, or O(n^2) scanning (Q27 in this part).
- Keep the LAST of each run? Skip forward through the run and keep the last node, relinking the previous kept node to it; the head may change, so use a dummy.

**Common mistakes:**
- Advancing after deleting.
- Writing `while cur.next` without checking `cur` (crash on an empty list).
- Comparing nodes with `==`; compare `.val`.
- Calling it "O(1) time" because no extra structure is used; it is O(n) time.

### Q16 ⭐⭐ 🟢 The dummy (sentinel) node technique: remove all nodes with a given value. Nodes are `ListNode(val, next)`. Given a list (0 <= len <= 10^4) and an integer `val`, delete every node whose value equals `val` and return the head, in place. Write it with a dummy node in front, and then without one (a head-skipping loop followed by the main loop) and compare how much special-case code each needs. State what a dummy node costs (one extra node, O(1)) and name two other list problems where it removes a head case. Example: [1,2,6,3,4,5,6], val=6 -> [1,2,3,4,5]; [], val=1 -> []; [7,7,7], val=7 -> []; [1,2], val=3 -> [1,2]; [6,1], val=6 -> [1].

**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Dummy (sentinel) node. A fake node in front of the head turns "delete the head" into the same operation as "delete any other node".

**Say this first (1 line):** "I put a dummy before the head, keep `prev` on the node before the one I am testing, and return `dummy.next`. The head case disappears."

**Brute force:** Collect the values that are not `val` into a Python list and rebuild: O(n) time, O(n) space, new nodes. Or the no-dummy in-place version below, which is correct but needs a special loop.

**Optimal (dummy):**
- `dummy = ListNode(0, head)`, `prev = dummy`.
- While `prev.next`: if `prev.next.val == val`, set `prev.next = prev.next.next` (do not advance); else `prev = prev.next`.
- Return `dummy.next`. If the head was removed, `dummy.next` already points to the new head.

**Without a dummy:**
- Loop 1: `while head and head.val == val: head = head.next` (skip matching heads).
- Loop 2: `cur = head`; `while cur and cur.next:` same test on `cur.next`.
- It is two loops, and the empty result needs the `cur and` guard. The dummy version is one loop and one return.

**Cost of the dummy:** one extra node, so O(1) space. It is created once and is not part of the result.

**Complexity:** Time O(n), one pass. Space O(1). Both versions reuse the nodes (the code checks identity).

**Dry run:** [6,1], val=6. dummy -> 6 -> 1. prev=dummy, prev.next is 6: match, dummy.next = 1. prev.next is 1: no match, prev = node 1. prev.next is None: stop. Return dummy.next = node 1. Result [1].

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def remove_with_dummy(head, val):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next     # delete; do not advance prev
        else:
            prev = prev.next
    return dummy.next

def remove_without_dummy(head, val):
    while head and head.val == val:        # special case: skip matching heads
        head = head.next
    cur = head
    while cur and cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head

def brute(arr, val):
    return [v for v in arr if v != val]

def run(f, arr, val):
    head, nodes = from_array(arr)
    r = f(head, val)
    ids = node_ids(r)
    kept = [id(n) for n in nodes if n.val != val]
    assert ids == kept                      # same node objects, same order, no new nodes
    return to_array(r)

for arr, val, want in (([1, 2, 6, 3, 4, 5, 6], 6, [1, 2, 3, 4, 5]), ([], 1, []), ([7, 7, 7], 7, []),
                       ([1, 2], 3, [1, 2]), ([6, 1], 6, [1])):
    for f in (remove_with_dummy, remove_without_dummy):
        assert run(f, arr, val) == want == brute(arr, val)
    print(arr, 'remove', val, '->', want)

random.seed(16)
for _ in range(500):
    arr = [random.randint(0, 3) for _ in range(random.randint(0, 20))]
    val = random.randint(0, 4)
    for f in (remove_with_dummy, remove_without_dummy):
        assert run(f, arr, val) == brute(arr, val)
assert run(remove_with_dummy, [9] * 10**4, 9) == [] and run(remove_without_dummy, [9] * 10**4, 9) == []
print('random cross-check ok (500 cases + 10^4 equal values)')
```

**Output (my run):**
```
[1, 2, 6, 3, 4, 5, 6] remove 6 -> [1, 2, 3, 4, 5]
[] remove 1 -> []
[7, 7, 7] remove 7 -> []
[1, 2] remove 3 -> [1, 2]
[6, 1] remove 6 -> [1]
random cross-check ok (500 cases + 10^4 equal values)
```

**Edge cases:**
- Empty list: return None.
- Every node matches: result is empty (`dummy.next` is None).
- Matches at the head, in the middle, at the tail.
- No match.
- Long run of matches (10^4): iteration, not recursion, so no stack trouble.

**Follow-ups:**
- Other problems where a dummy removes a head case? Merge two sorted lists (Q3), remove the n-th from the end (Q5), remove all duplicated values (Q24), partition (Q21), all in this part.
- Recursive version? `head.next = f(head.next, val); return head.next if head.val == val else head`; neat, but depth n (see Q26 in this part).
- Is the dummy always worth it? If the head can never change (Q15), you can skip it.

**Common mistakes:**
- Advancing `prev` after a delete, which skips the next node when matches are adjacent.
- Returning `head` instead of `dummy.next`.
- Forgetting the dummy when the head can be deleted.
- In the no-dummy version, testing `cur.val` instead of `cur.next.val` in loop 2, so you cannot unlink.

### Q17 ⭐⭐ 🟢 Python specifics: the node class, identity versus equality, building and printing lists. Write `ListNode` with `__slots__ = ('val', 'next')` and helper functions `from_array(arr)` (returns the head, building from the back or with a dummy), `to_array(head)` and a cycle-safe `show(head)`. Explain what `__slots__` removes (the per-instance `__dict__`, so no new attributes can be added) and why it saves memory; show that `a == b` is False for two nodes with equal values (default equality is identity) and say what `is` tests; explain why a `show` that loops `while node:` hangs on a cyclic list and how a set of visited ids or a step cap fixes it. `show` must print values joined by ' -> ' and end with ' -> None' for a normal list, 'None' for an empty list, and for a cycle stop at the repeated node and end with ' -> (cycle to index k)' where k is the index of the repeated node. Example: show of [1,2,3] -> '1 -> 2 -> 3 -> None'; show of [] -> 'None'; show of [1,2,3] with the tail pointing back to index 1 -> '1 -> 2 -> 3 -> (cycle to index 1)'; to_array(from_array([4,5])) -> [4,5].

**Asked at:** Python recursion-limit explainers (note.nkmk.me, educative.io, DEV Community recursion-limit posts; snippets only, not opened: default limit 1000, raising it risks crashes, iteration preferred); __slots__ behaviour not found in any snippet and was verified by running Python 3.13 in the sandbox | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Python housekeeping for list problems: a lean node class, identity versus equality, and test helpers that cannot hang. This is the toolkit every other question in this part uses.

**Say this first (1 line):** "`__slots__` drops the per-instance dict, `==` on plain objects is identity, and any print or compare on a list that might have a cycle needs a visited set or a step cap."

**Brute force:** A plain class (`self.val = val; self.next = next`) with a `show` that loops `while node:`. It works for normal lists and hangs forever on a cycle. Wrong for test helpers.

**Optimal:**
- `ListNode` with `__slots__ = ('val', 'next')`. Each instance has fixed storage for those two fields and no `__dict__`, so instances are smaller and a typo such as `node.nxt = x` raises `AttributeError` instead of silently creating an attribute.
- `from_array(arr)`: build from the back (`head = ListNode(v, head)` for v in reversed order), so there is no dummy and no tail pointer.
- `to_array(head)`: walk and collect, with a length cap so a cycle fails loudly instead of hanging.
- `show(head)`: walk with a dict `id(node) -> index`. When a node repeats, stop and print `-> (cycle to index k)` with k from the dict. Otherwise end with `-> None`. Empty list prints `None`.
- Equality: a class without `__eq__` inherits identity equality, so two nodes with the same value are not `==`. `is` tests whether two names refer to the same object. `a == a` is True. That is why tests for in-place algorithms compare `id(node)` (or `is`), and compare values separately.
- A step cap works too (stop after a known maximum length), but it needs a bound you trust. The visited dict needs no bound and also gives the index. An O(1)-space alternative uses Floyd's algorithm to find the cycle start index (Q6 in this part), shown in the code as `show_o1`.
- Memory numbers in the output are from this sandbox and include the int object and the list slot. Use them as a rough comparison, not as a guarantee.

**Complexity:** `from_array`, `to_array`, `show`: O(n) time. `show` uses O(n) space for the dict; `show_o1` uses O(1).

**Dry run:** `show` on 1 -> 2 -> 3 with 3 pointing back to 2 (index 1). Visit 1 (index 0), 2 (index 1), 3 (index 2), then the next node is node 2, which is in the dict with index 1. Output `1 -> 2 -> 3 -> (cycle to index 1)`.

**Code:**
```python
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
```

**Output (my run):**
```
1 -> 2 -> 3 -> None
None
1 -> 2 -> 3 -> (cycle to index 1)
[4, 5]
a == b: False | a is b: False | a == a: True
slots node has __dict__: False | plain node has __dict__: True
new attribute on slots node: AttributeError
bytes per node incl. its int and list slot (sandbox only): slots 89, plain 129
naive while node: still walking after 10000 steps
random cross-check ok (500 cases)
```

**Edge cases:**
- Empty list: `from_array([])` is None and `show` prints `None`.
- Self-loop (single node pointing to itself): prints `1 -> (cycle to index 0)`.
- Cycle that returns to the head (index 0).
- Equal values everywhere: only identity can detect the cycle, never values.

**Follow-ups:**
- Why not `str(node)` for printing? The default repr is an address; write `show`.
- Does `__slots__` help with subclasses or weak references? A subclass without its own `__slots__` gets a `__dict__` again; weak references need `'__weakref__'` in the slots.
- Why does equality matter for tests? To assert "in place" you compare node identities before and after; comparing values would pass even when the algorithm built a new list.

**Common mistakes:**
- `while node:` printing with no guard.
- Using `==` on nodes and expecting value equality.
- Detecting a cycle by comparing values.
- Building the list front-to-back with `head.next.next...` chains instead of a tail pointer or building from the back.

### Q18 ⭐⭐ 🟡 Reverse a sublist between positions. Nodes are `ListNode(val, next)`. Given a list (1 <= len <= 500) and 1-based positions left <= right <= len, reverse only the nodes from position left to position right, in place, in one pass, and return the head. Use a dummy node, walk to the node before position left, then repeatedly move the node after the current tail of the reversed part to the front of that part ('head insertion'); explain why it is one pass and O(1) space, and why left == right is a no-op. Also say how the node-VALUES variant of the same problem (a candidate-reported Flipkart variant) changes the first step. Example: [1,2,3,4,5], left=2, right=4 -> [1,4,3,2,5]; [5], 1, 1 -> [5]; [3,5], 1, 2 -> [5,3]; [1,2,3], 1, 3 -> [3,2,1]; [1,2,3], 2, 2 -> [1,2,3].

**Asked at:** Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice) | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr, pos=-1):
    """Build a list from an array. Returns (head, nodes). pos >= 0 links the tail back to nodes[pos]."""
    dummy = tail = ListNode()
    nodes = []
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next, nodes

def to_array(head, cap=10**5):
    """Values from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**5):
    """Identities of the nodes from head; the cap guards against a cycle."""
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out


def brute(arr, left, right):           # slice reversal on a Python list
    return arr[:left - 1] + arr[left - 1:right][::-1] + arr[right:]

def reverse_between(head, left, right):    # one pass, O(1) space, in place
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):          # stop on the node just before position left
        before = before.next
    tail = before.next                 # the node at position left; it ends up at the END of the reversed part
    for _ in range(right - left):      # head insertion: move tail.next to the front of the part
        moved = tail.next
        tail.next = moved.next         # unlink moved
        moved.next = before.next       # put it in front of the reversed part
        before.next = moved
    return dummy.next

def reverse_between_values(head, a, b):
    """Variant: reverse from the node holding value a to the node holding value b (values distinct, a before b).
    Only the first step changes: find the positions by walking, then reuse the same function."""
    pos, left, right, p = 1, None, None, head
    while p:
        if p.val == a and left is None:
            left = pos
        if p.val == b:
            right = pos
            break
        p, pos = p.next, pos + 1
    return reverse_between(head, left, right)

def run(arr, left, right):
    head, nodes = from_array(arr)
    r = reverse_between(head, left, right)
    ids = node_ids(r)
    want_nodes = nodes[:left - 1] + nodes[left - 1:right][::-1] + nodes[right:]
    assert ids == [id(n) for n in want_nodes]           # same objects, exactly this order
    return to_array(r)

for arr, l, r, want in (([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5]), ([5], 1, 1, [5]), ([3, 5], 1, 2, [5, 3]),
                        ([1, 2, 3], 1, 3, [3, 2, 1]), ([1, 2, 3], 2, 2, [1, 2, 3])):
    assert run(arr, l, r) == want == brute(arr, l, r)
    print(arr, l, r, '->', want)

# exhaustive: every length 1..9 and every 1 <= left <= right <= len
count = 0
for n in range(1, 10):
    arr = list(range(10, 10 + n))
    for l in range(1, n + 1):
        for r in range(l, n + 1):
            assert run(arr, l, r) == brute(arr, l, r)
            count += 1
print('exhaustive (length, left, right) triples ok:', count)

# no-op when left == right: the very same list comes back
head, nodes = from_array([1, 2, 3])
assert reverse_between(head, 2, 2) is head and node_ids(head) == [id(n) for n in nodes]

# value variant: [1,2,3,4,5], from value 2 to value 4
head, _ = from_array([1, 2, 3, 4, 5])
assert to_array(reverse_between_values(head, 2, 4)) == [1, 4, 3, 2, 5]
random.seed(18)
for _ in range(300):
    n = random.randint(1, 30)
    arr = random.sample(range(100), n)
    i = random.randint(0, n - 1); j = random.randint(i, n - 1)
    head, _ = from_array(arr)
    assert to_array(reverse_between_values(head, arr[i], arr[j])) == brute(arr, i + 1, j + 1)
    l = random.randint(1, n); r = random.randint(l, n)
    dup = [random.randint(0, 3) for _ in range(n)]
    assert run(dup, l, r) == brute(dup, l, r)
print('value variant and random cross-check ok (300 cases)')
head, _ = from_array(list(range(500)))
assert to_array(reverse_between(head, 1, 500)) == list(range(499, -1, -1))
print('n = 500, whole list ok')[1, 2, 3, 4, 5] 2 4 -> [1, 4, 3, 2, 5]
[5] 1 1 -> [5]
[3, 5] 1 2 -> [5, 3]
[1, 2, 3] 1 3 -> [3, 2, 1]
[1, 2, 3] 2 2 -> [1, 2, 3]
exhaustive (length, left, right) triples ok: 165
value variant and random cross-check ok (300 cases)
n = 500, whole list ok
