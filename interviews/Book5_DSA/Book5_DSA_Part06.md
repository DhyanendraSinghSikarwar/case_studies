# Book 5 — Part 6: Linked lists

**Topic:** Python DSA for product-company interviews: the node class (ListNode with __slots__) and the test harness, identity versus equality, building lists from arrays and printing safely on cycles, the dummy (sentinel) node technique, reversing a list (iterative and recursive), reversing between positions and in k-groups, Floyd cycle detection with the cycle start and its proof, cycle and tail length, removing a cycle, the middle node, palindrome list in O(1) space, merging two sorted lists and k sorted lists (a heap only as the merge tool), removing the n-th node from the end, removing duplicates (sorted, all-duplicated, unsorted), partition, rotate, reorder, odd-even, swap in pairs, adding two numbers (reverse and forward digit order), intersection of two lists, deleting a node given only that node, copying a list with random pointers (hash map and O(1) extra space), flattening a multilevel doubly linked list, sorting a list (top-down and O(1)-space bottom-up merge sort, insertion sort), doubly linked list operations with sentinels, the LRU cache idea at concept level, and why recursion on long lists fails in Python

**Target:** 35  |  **Actual:** 35 (⭐⭐⭐ 13, ⭐⭐ 13, ⭐ 9)  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns pointer manipulation on singly and doubly linked lists. Fast and slow pointers on ARRAYS belong to Part 2 (the circular array loop is cross-referenced only as 'Part 2 Q44', checked against its heading), and the value-range plus Floyd solution of find the duplicate number is Part 1 ('Part 1 Q28', checked against its heading; here Floyd is on node pointers). Part 4 owns stacks and queues, Part 5 binary search, Part 7 trees, Part 8 heaps, intervals and greedy (the merge-k question uses `heapq` only as a merge tool and heap theory is left to Part 8), Part 9 graphs (cycle detection in graphs), and Part 14 owns design problems (the LRU cache here is concept level only: why a doubly linked list plus a dict gives O(1), not the class design). Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Conventions: every prompt states its list as a Python array in the examples and uses `class ListNode: __slots__ = ('val', 'next')` with constructor `ListNode(val, next)`; cyclic examples are written as an array plus `pos` (the index the tail points back to, -1 for none); random-pointer nodes are written [val, random_index]; the multilevel list is written as a nested array in which a list item is the child list of the node before it. Questions that say 'in place' require the result to consist of the same node objects, which the tests verify by node identity, together with an acyclicity check and a step cap so a broken solution fails instead of hanging. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example was run against node-based reference solutions and independent brute-force code on Python lists (scratch/B5P06_wavea/check_examples.py, python3 -I) before freezing, together with randomised cross-checks (500 random lists for most operations, 300 for the sorts' stability, doubly linked list and LRU checks) and exhaustive checks of claims: Floyd's slow and fast pointers meet after exactly t steps, where t is the smallest positive multiple of the cycle length lambda that is at least the tail length mu, for every mu in 0..15 and lambda in 1..15 (240 pairs), the restart step returns the cycle start for all of them, and t <= mu + lambda (equality only at mu = 0), which bounds the moves in the cycle-length question; merge-k tie order (lower list index first) in both the heap and the divide-and-conquer versions; stability of both merge sorts and insertion sort by node identity; the recursive reverse raising RecursionError at 2000 nodes under the default limit of 1000 while the iterative one handles 10^5; that a ListNode has no __dict__ and rejects new attributes; that equal-valued nodes compare unequal; and that a value-set cycle check would be wrong (a list [1,1,1] has repeated values but no cycle). The prompts state their uniqueness assumptions: the middle of an even list is the second middle, sorts and partitions are stable, merge ties favour the first list, intersection means shared node objects, and remove-n-th, rotate, reorder and the like have exactly one result list. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for docs.python.org) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part06_sources.md). Searches returned linked-list pattern guides and question roundups, candidate-reported Naukri Code360 entries (Amazon on-campus March 2021 flatten of a multilevel list and December 2021 with adding two numbers; Flipkart 2020 and 2021 reverse linked list, one with an O(n) time O(1) space follow-up; one LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant), Floyd explanations (partial proof sketches only) and Python recursion-limit explainers; nothing was found for reverse in k-groups, merge k sorted lists or LRU cache at a named company, so 'Asked at' tags name source types (pattern guides, practice lists, candidate-reported snippets, editor knowledge of standard lists), not verified company reports. The Floyd proof and the __slots__ behaviour were checked by running code (Python 3.13), not taken from a page. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---

### Q1 ⭐⭐⭐ 🟢 Reverse a linked list. Nodes are `ListNode(val, next)`. Given the head of a singly linked list (0 <= len <= 5000), return the head of the reversed list. Write the iterative three-pointer version (`prev`, `cur`, and a saved `nxt`) in O(n) time and O(1) space, then the recursive version, and say why the recursive one uses O(n) stack. Reverse in place: the result must be made of the same node objects (no new nodes), which the tests check by identity. Example: [1,2,3,4,5] -> [5,4,3,2,1]; [1,2] -> [2,1]; [7] -> [7]; [] -> [].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Pointer reversal with a saved next pointer. Flip each link as you walk, so no new nodes are needed.

**Say this first (1 line):** "I walk once, saving `cur.next` before I overwrite it, pointing each node at the previous one. O(n) time, O(1) space, same nodes."

**Brute force:** Copy the values into an array, then build a new list from the reversed array. O(n) time, O(n) space, and it creates new nodes, so it fails the in-place requirement.

**Optimal:**
- Iterative: `prev = None`, `cur = head`. Each round: `nxt = cur.next`, `cur.next = prev`, `prev = cur`, `cur = nxt`.
- Invariant: `prev` is the head of the already-reversed part, `cur` is the head of the untouched part. The two parts never share a node.
- Why the saved `nxt`: after `cur.next = prev` the rest of the list is unreachable unless you kept it.
- When `cur` is None, `prev` is the old tail, which is the new head.
- Recursive: reverse everything after `head`, then make `head.next.next = head` and cut `head.next = None`. The recursive call returns the new head unchanged all the way up.
- Why the recursion uses O(n) stack: each node has a pending call frame (it still has to do `head.next.next = head` after the call returns), so n frames are live at the deepest point.

**Complexity:** Iterative: time O(n), one visit per node; space O(1), three pointers. Recursive: time O(n), space O(n) for the call stack. Python's default recursion limit is 1000, so the recursive version fails on a 5000-node list unless you raise the limit.

**Dry run:** `[1,2,3]`. Start `prev=None, cur=1`.
- Round 1: `nxt=2`, `1.next=None`, `prev=1`, `cur=2`.
- Round 2: `nxt=3`, `2.next=1`, `prev=2`, `cur=3`.
- Round 3: `nxt=None`, `3.next=2`, `prev=3`, `cur=None`. Return 3: `3 -> 2 -> 1 -> None`.

**Code:**
```python
import random
import sys

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

# ---------- brute force: copy values out, build NEW nodes (not in place) ----------
def reverse_brute(head):
    vals = to_list(head)
    new_head = None
    for v in vals:                      # pushing each value on the front reverses the order
        new_head = ListNode(v, new_head)
    return new_head

# ---------- optimal 1: iterative three pointers ----------
def reverse_iter(head):
    prev, cur = None, head
    while cur is not None:
        nxt = cur.next                  # save the rest before we cut the link
        cur.next = prev                 # flip one link
        prev = cur                      # advance prev
        cur = nxt                       # advance cur
    return prev                         # prev is the old tail = new head

# ---------- optimal 2: recursive ----------
def reverse_rec(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_rec(head.next)   # reverses everything after head
    head.next.next = head               # the node after head now points back to head
    head.next = None                    # head becomes the tail
    return new_head

def check_inplace(fn, arr):
    head, nodes = build(arr)
    out = fn(head)
    assert to_list(out) == arr[::-1]
    assert node_ids(out) == [id(n) for n in reversed(nodes)]   # same objects, reversed order
    return to_list(out)

# ---- examples from the prompt ----
for arr, exp in [([1,2,3,4,5],[5,4,3,2,1]), ([1,2],[2,1]), ([7],[7]), ([],[])]:
    assert check_inplace(reverse_iter, arr) == exp
    assert check_inplace(reverse_rec, arr) == exp
    print(arr, "->", exp)

# ---- randomised cross-check (seeded) ----
random.seed(1)
for _ in range(500):
    arr = [random.randint(-5, 5) for _ in range(random.randint(0, 30))]
    head, _n = build(arr)
    assert to_list(reverse_brute(head)) == arr[::-1]       # brute is non-destructive
    assert check_inplace(reverse_iter, arr) == arr[::-1]
    assert check_inplace(reverse_rec, arr) == arr[::-1]
print("cross-check ok (500 random lists, identity checked)")

# ---- recursion depth: the prompt allows 5000 nodes ----
big, _n = build(list(range(5000)))
print("default recursion limit:", sys.getrecursionlimit())
try:
    reverse_rec(big)
    print("recursive on 5000 nodes: no error")
except RecursionError:
    print("recursive on 5000 nodes: RecursionError")
big, nodes = build(list(range(5000)))                      # fresh list (the failed call cut links)
out = reverse_iter(big)
assert to_list(out) == list(range(4999, -1, -1))
print("iterative on 5000 nodes: ok")
old = sys.getrecursionlimit()
sys.setrecursionlimit(20000)
big, nodes = build(list(range(5000)))
assert to_list(reverse_rec(big)) == list(range(4999, -1, -1))
sys.setrecursionlimit(old)
print("recursive on 5000 nodes with the limit raised to 20000: ok")
```

**Output (my run):**
```
[1, 2, 3, 4, 5] -> [5, 4, 3, 2, 1]
[1, 2] -> [2, 1]
[7] -> [7]
[] -> []
cross-check ok (500 random lists, identity checked)
default recursion limit: 1000
recursive on 5000 nodes: RecursionError
iterative on 5000 nodes: ok
recursive on 5000 nodes with the limit raised to 20000: ok
```

**Edge cases:**
- Empty list: the loop never runs, return `prev = None`.
- One node: becomes `None <- 1`, so it returns itself.
- Two nodes: the smallest case that actually flips a link.
- 5000 nodes: use the iterative version, or raise the recursion limit.

**Follow-ups:**
- Why not just swap values? It is not a pointer reversal, and with big payloads or shared references the node identity matters. The prompt also asks for the same nodes in reverse order.
- Reverse a part of the list only? Same loop on a window with a dummy head (see the "reverse between positions" question in this part).
- Print safely? Always cap the walk, as `to_list` does, in case a bug made a cycle.

**Common mistakes:**
- Overwriting `cur.next` before saving it, which loses the rest of the list.
- Forgetting `head.next = None` in the recursive version, which leaves a two-node cycle at the old head.
- Returning `head` instead of `prev`.
- Trusting recursion on a long list in Python.

### Q2 ⭐⭐⭐ 🟢 Middle of a linked list. Nodes are `ListNode(val, next)`. Return the middle node of a singly linked list with 1 <= len <= 100, using one pass with a slow and a fast pointer. When the length is even there are two middles; return the SECOND one. Show that the loop condition `while fast and fast.next` yields the second middle, and say what changes to get the first middle. Return the node itself (the tests compare node identity, and print the values from that node onward). Example: [1,2,3,4,5] -> [3,4,5]; [1,2,3,4,5,6] -> [4,5,6]; [1] -> [1]; [1,2] -> [2].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Floyd cycle-detection explanations (arXiv note on Pollard rho, Wikipedia cycle detection, VisuAlgo cycle finding, an Isabelle formalisation; snippets only, not opened: they give the mu + k = lambda*M relation, finding mu by restarting one pointer, finding lambda by looping once; none gives a complete written proof, so the proof here is the editor's own and is tested exhaustively)

**Pattern:** Slow and fast pointers. Fast moves twice as far, so when it finishes, slow is at the middle.

**Say this first (1 line):** "One pass: slow steps 1, fast steps 2, and when fast runs out, slow is in the middle. The loop `while fast and fast.next` gives the second middle."

**Brute force:** Walk once to put all nodes in an array, then return `nodes[n // 2]`. O(n) time, O(n) space. Or walk once to count, then walk n // 2 steps: O(n) time, O(1) space, two passes.

**Optimal:**
- `slow = fast = head`. While `fast` and `fast.next` exist: `slow = slow.next`, `fast = fast.next.next`.
- Invariant: slow has moved k steps and fast has moved 2k steps from the head.
- Odd length n = 2m + 1: fast lands on the last node after m rounds, and slow is at index m, the exact middle.
- Even length n = 2m: fast reaches None after m rounds, so slow is at index m, the second middle (indices are 0-based, the middles are m - 1 and m).
- The condition: the loop runs again only if fast can still jump two (`fast.next` exists). For even n, fast is at index 2m - 2 with `fast.next` present, so it runs one more round and slow moves to index m.
- For the FIRST middle use `while fast.next and fast.next.next`. The loop stops one round earlier, slow is at index m - 1 for even n. Odd n is unchanged. This version needs a non-empty list (it reads `fast.next`).

**Complexity:** Time O(n): fast visits about n nodes, slow n/2. Space O(1).

**Dry run:** `[1,2,3,4]`. Round 1: slow=2, fast=3 (`fast.next` is 4, still exists). Round 2: slow=3, fast=None. Loop ends (fast is None). Return node 3, the second middle. With the first-middle condition: round 1 slow=2, fast=3; now `fast.next.next` is None, stop. Return 2.

**Code:**
```python
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
# ---------- brute force: collect nodes in a Python list, index into it ----------
def middle_brute(head, first=False):
    nodes = []
    while head is not None:
        nodes.append(head)
        head = head.next
    n = len(nodes)
    return nodes[(n - 1) // 2] if first else nodes[n // 2]

# ---------- optimal: slow moves 1, fast moves 2, one pass ----------
def middle(head):                       # SECOND middle on even length
    slow = fast = head
    while fast and fast.next:           # fast can still jump two
        slow = slow.next
        fast = fast.next.next
    return slow

def middle_first(head):                 # FIRST middle on even length
    slow = fast = head
    while fast.next and fast.next.next: # stop one step earlier
        slow = slow.next
        fast = fast.next.next
    return slow

for arr, exp in [([1,2,3,4,5],[3,4,5]), ([1,2,3,4,5,6],[4,5,6]), ([1],[1]), ([1,2],[2])]:
    head, nodes = build(arr)
    m = middle(head)
    assert m is nodes[len(arr) // 2]    # identity, not just value
    assert to_list(m) == exp
    print(arr, "->", to_list(m))

random.seed(2)
for _ in range(500):
    arr = [random.randint(0, 3) for _ in range(random.randint(1, 100))]   # many repeats on purpose
    head, nodes = build(arr)
    assert middle(head) is middle_brute(head) is nodes[len(arr) // 2]
    assert middle_first(head) is middle_brute(head, first=True) is nodes[(len(arr) - 1) // 2]
print("cross-check ok (500 random lists, identity checked, both variants)")
head, nodes = build([1, 2, 3, 4])
print("first middle of [1,2,3,4]:", to_list(middle_first(head)), "| second middle:", to_list(middle(head)))
```

**Output (my run):**
```
[1, 2, 3, 4, 5] -> [3, 4, 5]
[1, 2, 3, 4, 5, 6] -> [4, 5, 6]
[1] -> [1]
[1, 2] -> [2]
cross-check ok (500 random lists, identity checked, both variants)
first middle of [1,2,3,4]: [2, 3, 4] | second middle: [3, 4]
```

**Edge cases:**
- One node: loop does not run, return head.
- Two nodes: returns the second node (first-middle version returns the first).
- Empty list is excluded by the prompt (the first-middle version would crash on it).
- Repeated values: compare nodes with `is`, not values, which the tests do.

**Follow-ups:**
- Why is this the basis of many problems? Palindrome list, reorder list, and sort list (merge sort) all split at the middle with this loop.
- Merge sort wants the node BEFORE the middle? Use a `prev` pointer, or the first-middle variant to cut after it.
- Third node from the end? Different technique: a gap of k between two pointers (see remove n-th from end).

**Common mistakes:**
- Writing `while fast.next and fast.next.next` and expecting the second middle.
- Checking `fast.next` before `fast`, which crashes when fast is None.
- Returning an index or a value instead of the node.

### Q3 ⭐⭐⭐ 🟢 Merge two sorted linked lists. Nodes are `ListNode(val, next)`. Given the heads of two lists, each sorted ascending (0 <= len <= 50 each), splice them into one sorted list and return its head, reusing the existing nodes (no new nodes; the tests check identity). Use a dummy head node and a tail pointer, and make the merge stable: on equal values the node from the FIRST list comes first. Explain what the dummy removes (the empty-result and first-node special cases) and why this is O(m + n) time and O(1) extra space. Example: [1,2,4] and [1,3,4] -> [1,1,2,3,4,4] (the first 1 is from the first list); [] and [] -> []; [] and [0] -> [0]; [2,5] and [1] -> [1,2,5].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Two-pointer merge with a dummy head and a tail pointer. The dummy removes the "which node is first" special case.

**Say this first (1 line):** "Dummy head, tail pointer, always splice the smaller front node, `<` strict so ties take list one, and attach the leftover run at the end."

**Brute force:** Put all nodes into an array, stable-sort by value, relink. O((m + n) log(m + n)) time, O(m + n) space. It ignores that both lists are already sorted.

**Optimal:**
- `dummy = tail = ListNode()`. While both lists are non-empty compare the two fronts. If `b.val < a.val` take b, otherwise take a.
- Stability: on a tie the condition is false, so `a` (the first list) goes first. Using `<=` for b would break it.
- After the loop at most one list remains and it is already sorted: `tail.next = a or b` (the code spells it with `is not None`).
- Invariant: everything from `dummy.next` to `tail` is sorted and no larger than any remaining front node.
- What the dummy removes: without it you must decide the head separately, and an empty result (both lists empty) needs its own branch. With it `tail` always exists and the answer is `dummy.next`, which is None when the result is empty.

**Complexity:** Time O(m + n): each iteration consumes one node. Space O(1) extra: only pointers, the nodes are reused (the dummy is one temporary node).

**Dry run:** `[2,5]` and `[1]`. a=2, b=1: 1 < 2, take b. b is None, loop ends. `tail.next = a` splices the whole `2 -> 5`. Result `1 -> 2 -> 5`.

**Code:**
```python
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
```

**Output (my run):**
```
[1, 2, 4] [1, 3, 4] -> [1, 1, 2, 3, 4, 4]
[] [] -> []
[] [0] -> [0]
[2, 5] [1] -> [1, 2, 5]
tie check: first 1 is from list 1 -> ok
cross-check ok (1000 random pairs with many ties, stability and identity checked)
```

**Edge cases:**
- Both empty: the loop is skipped, `tail.next = None`, return None.
- One empty: the whole other list is spliced.
- All of one list smaller than the other: one splice of the leftover.
- Many equal values: first list's nodes stay ahead of second list's.

**Follow-ups:**
- Merge k lists? Repeat this merge pairwise (divide and conquer), or use a heap (heaps are Part 8). 
- Recursive version? Shorter, but O(m + n) stack, which fails on long lists in Python.
- Merge into new nodes instead? Allocate a node per step. O(m + n) space.

**Common mistakes:**
- Forgetting to attach the leftover run.
- Using `<=` for the second list and breaking stability.
- Returning `dummy` instead of `dummy.next`.
- Leaving the last node's `next` pointing into the old list. Here the leftover splice and the tail of the other list keep it ending in None.

### Q4 ⭐⭐⭐ 🟢 Detect a cycle in a linked list. Nodes are `ListNode(val, next)`. Return True if following `next` from the head ever revisits a node, else False (0 <= len <= 10^4). Examples describe a cycle as an array plus `pos`, the index the tail's `next` points back to (-1 means no cycle). Give the O(n) time, O(n) space version with a set of node identities (`id(node)` or the node itself, since the default hash is identity), then Floyd's tortoise and hare in O(1) space. Explain why a fast pointer that moves 2 per step must catch a slow one inside a cycle and why it can never skip over it, and why a hash set of node VALUES would be wrong when values repeat. Example: [3,2,0,-4], pos=1 -> True; [1,2], pos=0 -> True; [1], pos=-1 -> False; [1,1,1], pos=-1 -> False; [], pos=-1 -> False.
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Floyd cycle-detection explanations (arXiv note on Pollard rho, Wikipedia cycle detection, VisuAlgo cycle finding, an Isabelle formalisation; snippets only, not opened: they give the mu + k = lambda*M relation, finding mu by restarting one pointer, finding lambda by looping once; none gives a complete written proof, so the proof here is the editor's own and is tested exhaustively)

**Pattern:** Visited-set, then Floyd's tortoise and hare (fast and slow pointers) for O(1) space.

**Say this first (1 line):** "Set of node identities is O(n) space. For O(1) space, slow moves 1 and fast moves 2; if they ever meet there is a cycle, if fast hits None there is not."

**Brute force:** Walk the list and store each node in a set. If you see a node again, there is a cycle; if you reach None, there is none. O(n) time, O(n) space. A node without `__eq__` or `__hash__` hashes by identity, so `node in seen` is an identity check. Storing `node.val` is wrong: `[1,1,1]` has no cycle, but the value set reports one on the second node (the code shows this).

**Optimal:**
- `slow = fast = head`. Loop while `fast` and `fast.next` exist: `slow = slow.next`, `fast = fast.next.next`, and return True if `slow is fast`. Falling out of the loop means fast reached the end: False.
- Why they meet if there is a cycle: once both are inside the cycle, fast gains exactly one node on slow per step (fast moves 2, slow moves 1). The gap, measured around the cycle of length lambda, shrinks by 1 each step.
- Why fast cannot skip over slow: the gap goes lambda-1, ..., 2, 1, 0. It changes by exactly 1, so it must hit 0 before it could go negative. A gap of 1 means fast is one node behind slow, and the next step lands them on the same node.
- Why no cycle means fast ends: the list is finite, so fast reaches None.
- Compare with `is`, never values.

**Complexity:** Time O(n): slow enters the cycle after mu steps and then fast closes a gap smaller than lambda, so under mu + lambda steps in total, and mu + lambda is at most n. Space O(1).

**Dry run:** `[3,2,0,-4]`, tail points to index 1. Positions: slow=3, fast=3. Step 1: slow=2, fast=0. Step 2: slow=0, fast=2 (fast went -4 then back to 2). Step 3: slow=-4, fast=-4. Same node: True.

**Code:**
```python
import itertools

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
# ---------- O(n) space: set of node identities ----------
def has_cycle_set(head):
    seen = set()
    while head is not None:
        if head in seen:                # ListNode has no __eq__/__hash__, so this is identity
            return True
        seen.add(head)
        head = head.next
    return False

# ---------- WRONG: set of VALUES ----------
def has_cycle_values_wrong(head, limit=10**5):
    seen = set()
    steps = 0
    while head is not None and steps < limit:
        if head.val in seen:
            return True
        seen.add(head.val)
        head = head.next
        steps += 1
    return False

# ---------- O(1) space: Floyd tortoise and hare ----------
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:                # compare identity, never values
            return True
    return False

for arr, pos, exp in [([3,2,0,-4],1,True), ([1,2],0,True), ([1],-1,False), ([1,1,1],-1,False), ([],-1,False)]:
    head, _n = build(arr, pos)
    assert has_cycle(head) is has_cycle_set(head) is exp
    print(arr, "pos =", pos, "->", has_cycle(head))
head, _n = build([1, 1, 1])
print("values-set on [1,1,1] (no cycle):", has_cycle_values_wrong(head), "<- wrong")
assert has_cycle_values_wrong(head) is True

# exhaustive: every length 0..9, every pos -1..n-1, small value alphabets (repeats included)
count = 0
for n in range(0, 10):
    for pos in range(-1, n):
        for vals in ([0] * n, list(range(n)), [i % 2 for i in range(n)]):
            head, _nodes = build(vals, pos)
            expect = pos != -1
            assert has_cycle(head) is has_cycle_set(head) is expect
            count += 1
print("exhaustive ok:", count, "lists (all lengths 0..9, all pos)")

# the gap closes by exactly 1 per step once both are inside the cycle, so fast cannot jump over slow
head, nodes = build(list(range(5)) + list(range(5, 12)), 5)      # mu = 5, lambda = 7
slow = fast = head
steps = 0
while True:
    slow, fast = slow.next, fast.next.next
    steps += 1
    if slow is fast:
        break
print("mu=5, lambda=7: slow and fast first meet after", steps, "steps")
```

**Output (my run):**
```
[3, 2, 0, -4] pos = 1 -> True
[1, 2] pos = 0 -> True
[1] pos = -1 -> False
[1, 1, 1] pos = -1 -> False
[] pos = -1 -> False
values-set on [1,1,1] (no cycle): True <- wrong
exhaustive ok: 165 lists (all lengths 0..9, all pos)
mu=5, lambda=7: slow and fast first meet after 7 steps
```

**Edge cases:**
- Empty list: the loop is skipped, False.
- One node with no cycle: `fast.next` is None, False. One node pointing to itself: step 1 puts both on it, True.
- Repeated values with no cycle (`[1,1,1]`): must be False.
- The code checked every length 0 to 9 and every `pos`.

**Follow-ups:**
- Where does the cycle start? Floyd's second phase, the next questions in this part.
- Cycle length? After they meet, walk one pointer around until it returns: count the steps.
- Why not fast moving 3? The gap would shrink by 2 per step. If the cycle length is even and the gap is odd, it hops over 0 forever and they never meet. Step 2 changes the gap by exactly 1, so it cannot miss.

**Common mistakes:**
- Loop condition `while fast.next` without checking `fast`.
- Comparing values (`slow.val == fast.val`).
- Starting `slow` and `fast` at different nodes and checking before moving, so the first check is trivially true.
- Printing the list to debug: it can loop forever, cap the walk.

### Q5 ⭐⭐⭐ 🟡 Remove the n-th node from the end. Nodes are `ListNode(val, next)`. Given the head of a list with 1 <= len <= 30 and an integer n with 1 <= n <= len, delete the n-th node counted from the END and return the head, in ONE pass. Use a dummy node and two pointers kept n nodes apart, and explain why the dummy lets you delete the head node without a special case and why the gap is n (not n - 1 or n + 1) when you want the node BEFORE the one to delete. Also give the two-pass version (count, then walk) and compare. Example: [1,2,3,4,5], n=2 -> [1,2,3,5]; [1], n=1 -> []; [1,2], n=1 -> [1]; [1,2], n=2 -> [2].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Two pointers with a fixed gap, plus a dummy head so deleting the first node is not a special case.

**Say this first (1 line):** "Dummy before the head, fast goes n steps ahead, then both move until fast is on the last node. Slow is then just before the target."

**Brute force:** Two passes. Count the length L, then walk L - n steps from a dummy head to reach the node before the target, and unlink. O(L) time, O(1) space, but it reads the list twice.

**Optimal:**
- `dummy -> head`, `slow = fast = dummy`.
- Move `fast` n steps. Now fast and slow are n nodes apart.
- Move both while `fast.next` exists. Fast stops ON the last node.
- Why the gap is n: let the last node be at position L (dummy is position 0). Fast ends at L, so slow ends at L - n. The target (n-th from the end) is at position L - n + 1, exactly `slow.next`. A gap of n - 1 would stop slow ON the target, and a gap of n + 1 would stop it one node too early.
- Then `slow.next = slow.next.next`.
- Why the dummy: if n = L the target is the head, and "the node before the head" does not exist. With the dummy, slow ends at the dummy and `dummy.next` is updated normally. Return `dummy.next`.

**Complexity:** One-pass: time O(L), space O(1). Two-pass: time O(L) too (about 2L steps against about L), space O(1). Both are linear. The one-pass version matters if the list is a stream or reading is expensive, and interviewers like it as a two-pointer test.

**Dry run:** `[1,2,3,4,5]`, n = 2. `dummy,1,2,3,4,5`. Fast moves 2: at node 2. Now move together while `fast.next`: fast 3 (slow 1), fast 4 (slow 2), fast 5 (slow 3). `fast.next` is None, stop. slow is node 3, `slow.next` is 4, delete it: `1,2,3,5`.

**Code:**
```python
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
# ---------- two-pass: count, then walk ----------
def remove_nth_two_pass(head, n):
    length = 0
    p = head
    while p is not None:
        length += 1
        p = p.next
    dummy = ListNode(0, head)
    p = dummy
    for _ in range(length - n):         # stop on the node BEFORE the target
        p = p.next
    p.next = p.next.next
    return dummy.next

# ---------- one-pass: dummy + two pointers with a gap of n ----------
def remove_nth(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):                  # fast gets a head start of n nodes
        fast = fast.next
    while fast.next is not None:        # fast stops ON the last node, so slow stops BEFORE the target
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next

def check(fn, arr, n):
    head, nodes = build(arr)
    out = fn(head, n)
    removed = nodes[len(arr) - n]
    assert node_ids(out) == [id(x) for x in nodes if x is not removed]   # same objects minus one
    return to_list(out)

for arr, n, exp in [([1,2,3,4,5],2,[1,2,3,5]), ([1],1,[]), ([1,2],1,[1]), ([1,2],2,[2])]:
    assert check(remove_nth, arr, n) == check(remove_nth_two_pass, arr, n) == exp
    print(arr, "n =", n, "->", exp)

# exhaustive: every length 1..30, every n 1..len, all values equal (so only identity can tell nodes apart)
count = 0
for L in range(1, 31):
    for n in range(1, L + 1):
        arr = [7] * L
        assert check(remove_nth, arr, n) == check(remove_nth_two_pass, arr, n) == arr[:L - n] + arr[L - n + 1:]
        count += 1
print("exhaustive ok:", count, "(length, n) pairs")

random.seed(5)
for _ in range(500):
    L = random.randint(1, 30)
    arr = [random.randint(0, 9) for _ in range(L)]
    n = random.randint(1, L)
    assert check(remove_nth, arr, n) == arr[:L - n] + arr[L - n + 1:]
print("cross-check ok (500 random lists vs list slicing)")
```

**Output (my run):**
```
[1, 2, 3, 4, 5] n = 2 -> [1, 2, 3, 5]
[1] n = 1 -> []
[1, 2] n = 1 -> [1]
[1, 2] n = 2 -> [2]
exhaustive ok: 465 (length, n) pairs
cross-check ok (500 random lists vs list slicing)
```

**Edge cases:**
- n = L: removes the head (handled by the dummy).
- n = 1: removes the tail; `slow.next.next` is None.
- Single node with n = 1: result is empty (None).
- All values equal: only identity shows the right node was removed, and the code checks that.

**Follow-ups:**
- n larger than L? Not allowed here. If it is, the fast pointer hits None during the head start: check and return the head unchanged.
- Find the middle or the k-th from the end without deleting? Same gap trick.
- Is it really one pass? Fast makes one pass and slow follows it, total about L steps for fast.

**Common mistakes:**
- Gap of n - 1 or n + 1, deleting the wrong node.
- No dummy, so the head case crashes or needs a special branch.
- Returning `head` instead of `dummy.next` (breaks when the head is deleted).
- Looping `while fast` instead of `while fast.next`.

### Q6 ⭐⭐⭐ 🟡 Find where a cycle begins. Nodes are `ListNode(val, next)`. Given a list that may contain a cycle (examples give the array plus `pos`, the index the tail points back to, -1 for none), return the node where the cycle begins, or None. Use Floyd's two phases: find a meeting point with slow and fast, then restart one pointer at the head and move both one step at a time. PROVE why they meet exactly at the cycle start, with the tail length mu, the cycle length lambda and the distance k from the cycle start to the meeting point: state that the two pointers first meet after exactly t steps where t is the smallest POSITIVE multiple of lambda with t >= mu, derive mu + k = a multiple of lambda, and conclude. The same trick on an array of values is Part 1 Q28; here it is on node pointers. Example: [3,2,0,-4], pos=1 -> the node at index 1 (value 2); [1,2], pos=0 -> index 0; [1], pos=0 -> index 0 (a self-loop); [1,2,3], pos=-1 -> None.
**Asked at:** Floyd cycle-detection explanations (arXiv note on Pollard rho, Wikipedia cycle detection, VisuAlgo cycle finding, an Isabelle formalisation; snippets only, not opened: they give the mu + k = lambda*M relation, finding mu by restarting one pointer, finding lambda by looping once; none gives a complete written proof, so the proof here is the editor's own and is tested exhaustively) | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Floyd's cycle detection, phase 2: restart one pointer at the head and move both one step at a time. They meet at the cycle start.

**Say this first (1 line):** "Find the meeting point, then put one pointer back at the head. Both move one step at a time and meet exactly at the cycle start, because the head-to-start distance and the meeting-point-to-start distance differ by whole laps."

**Brute force:** Walk with a set of nodes. The first node seen twice is the cycle start. O(n) time, O(n) space.

**Optimal:**
- Phase 1: slow moves 1, fast moves 2 from the head. If fast reaches None, there is no cycle, return None. Otherwise they meet at some node M.
- Notation: mu = nodes before the cycle (tail length), lambda = cycle length, k = distance from the cycle start forward to M, 0 <= k < lambda.
- Meeting time. Slow has walked t steps, fast 2t. Both stand on the same node only when both are in the cycle, i.e. t >= mu (while slow is on the tail, fast is either on a different tail node, since 2t != t for t > 0, or already in the cycle, and a tail node is never a cycle node). Once both are in the cycle, they are on the same node exactly when their step counts differ by a multiple of lambda: 2t - t = t. So the first meeting is at the smallest POSITIVE multiple of lambda with t >= mu. For mu = 0 that is lambda, not 0.
- Position of M: slow has walked t steps, so M is t - mu steps past the cycle start, and k = (t - mu) mod lambda. Because t is a multiple of lambda, mu + k is a multiple of lambda, i.e. mu + k = c * lambda.
- Phase 2: pointer P at the head and pointer S at M, both one step at a time. After mu steps P is at the cycle start. S has walked mu steps from M, which is k + mu steps past the cycle start, and k + mu is a multiple of lambda, so S is also at the cycle start. They are on the same node after mu steps.
- First meeting is exactly there: before mu steps P is on the tail, and S is on the cycle, different nodes. So P and S first meet after exactly mu steps, at the cycle start.

**Complexity:** Time O(mu + lambda) = O(n): phase 1 takes t <= mu + lambda steps (t is the smallest positive multiple of lambda that is at least mu; it is below mu + lambda for mu >= 1 and equals lambda at mu = 0), phase 2 takes mu steps. Space O(1).

**Dry run:** `[3,2,0,-4]`, pos = 1: tail node -4 points to node 2. mu = 1, lambda = 3. Phase 1 meets at -4 after t = 3 steps (smallest multiple of 3 that is at least 1), so k = (3 - 1) mod 3 = 2: M = -4 is 2 steps past the start node 2 (2 -> 0 -> -4). Check mu + k = 3 = lambda. Phase 2: P = 3, S = -4. One step: P = 2, S = 2 (-4 points back to 2). They meet at node 2: the cycle start.

**Code:**
```python
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
```

**Output (my run):**
```
[3, 2, 0, -4] pos = 1 -> index 1 (value 2)
[1, 2] pos = 0 -> index 0 (value 1)
[1] pos = 0 -> index 0 (value 1)
[1, 2, 3] pos = -1 -> None
exhaustive ok: 240 (mu, lambda) pairs: t = smallest positive multiple of lambda >= mu; mu + k = 0 mod lambda; phase 2 takes mu steps
cross-check ok (1000 random lists, repeated values, identity compared)
```

**Edge cases:**
- No cycle: phase 1 ends with fast None, return None.
- Self-loop (`[1]`, pos = 0): mu = 0, lambda = 1; they meet at the head and phase 2 takes 0 steps.
- Cycle includes the head (mu = 0): they meet at a node at distance k = 0 from the head, so phase 2 is empty and returns the head. That is also why the first meeting is lambda and not 0.
- Repeated values: compare nodes by identity.

**Follow-ups:**
- Remove the cycle? Walk from the start to the node whose `next` is the start and set its `next` to None.
- Find mu and lambda? mu = phase 2 steps; lambda = walk once around from M until you return to M.
- The array version? "Find the duplicate number" is the same idea on indices (Part 1 Q28).

**Common mistakes:**
- Moving fast two steps in phase 2.
- Saying they meet at the start of the cycle in phase 1 (they meet at distance k from it, not necessarily at the start).
- Returning the meeting point.
- Claiming t is "the smallest multiple": it must be positive, so mu = 0 gives lambda, not 0.

### Q7 ⭐⭐⭐ 🟡 Palindrome linked list. Nodes are `ListNode(val, next)`. Return True if the sequence of values reads the same forward and backward (1 <= len <= 10^5), using O(n) time and O(1) EXTRA space: find the middle with slow and fast pointers, reverse the second half in place, compare, and restore the list afterwards (so the input is unchanged, which the tests check by identity and by values). Explain why the O(n) space copy-to-array version is the baseline, how odd lengths are handled (skip the middle), and what goes wrong if you do not restore the list. Example: [1,2,2,1] -> True; [1,2,3,2,1] -> True; [1,2] -> False; [1] -> True; [1,0,0] -> False.
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Middle by slow and fast pointers, in-place reversal of the second half, then a two-pointer compare. Restore at the end.

**Say this first (1 line):** "Copy to an array is the easy O(n) space answer. For O(1) space I find the middle, reverse the second half in place, compare it to the first half, and reverse it back."

**Brute force:** Copy the values into an array and compare it with its reverse. O(n) time, O(n) space. This is the baseline to mention first.

**Optimal:**
- Slow and fast: slow ends at the second middle for even n, the exact middle for odd n.
- Reverse from `slow` onward. The reversed half starts at the old tail. The node before `slow` still points at `slow`, which is now the end of the reversed half.
- Compare `p` from the head and `q` from the reversed half while `q` is not None. `q` covers n - n // 2 nodes. For odd n that includes the middle, which just compares with itself, so the middle is effectively skipped.
- Even n: both halves have n / 2 nodes and are compared fully.
- Restore: reverse the second half again so the input is unchanged. Do it even if a mismatch was found early (the code breaks out, then restores).

**Complexity:** Time O(n): find middle n/2, reverse n/2, compare n/2, restore n/2. Space O(1).

**Dry run:** `[1,2,3,2,1]`. Slow ends at 3 (index 2). Reverse from 3: the second half becomes `1 -> 2 -> 3` (the last 1 first, ending at the middle node 3). Compare p=1 vs q=1, p=2 vs q=2, p=3 vs q=3, q is None. True. Reverse the second half back to restore.

**Code:**
```python
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
def reverse(head):
    prev = None
    while head is not None:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

# ---------- baseline: copy values to an array, O(n) space ----------
def is_pal_array(head):
    vals = to_list(head)
    return vals == vals[::-1]

# ---------- optimal: middle, reverse second half, compare, restore ----------
def is_pal(head):
    slow = fast = head
    while fast and fast.next:           # slow ends at the second middle (even) or the exact middle (odd)
        slow = slow.next
        fast = fast.next.next
    second = reverse(slow)              # reversed second half; for odd n it starts at the last node and ends at the middle
    p, q = head, second
    ok = True
    while q is not None:                # q covers n - n//2 nodes; for odd n the middle compares with itself
        if p.val != q.val:
            ok = False
            break
        p, q = p.next, q.next
    reverse(second)                     # restore: reverse the second half back (the first half still points at slow)
    return ok

def is_pal_no_restore(head):            # shows the damage of forgetting to restore
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    reverse(slow)
    return None

for arr, exp in [([1,2,2,1],True), ([1,2,3,2,1],True), ([1,2],False), ([1],True), ([1,0,0],False)]:
    head, nodes = build(arr)
    before = node_ids(head)
    assert is_pal(head) is is_pal_array(head) is exp
    assert node_ids(head) == before and to_list(head) == arr          # list unchanged, same node order
    print(arr, "->", exp)

head, _n = build([1, 2, 3, 2, 1])
is_pal_no_restore(head)
print("[1,2,3,2,1] after forgetting to restore, head onward:", to_list(head))

random.seed(7)
for _ in range(2000):
    n = random.randint(1, 12)
    half = [random.randint(0, 2) for _ in range(n // 2)]
    mid = [random.randint(0, 2)] if n % 2 else []
    arr = half + mid + (half[::-1] if random.random() < 0.7 else [random.randint(0, 2) for _ in half])
    head, nodes = build(arr)
    assert is_pal(head) is (arr == arr[::-1])
    assert [id(x) for x in nodes] == node_ids(head) and to_list(head) == arr
print("cross-check ok (2000 random lists, odd and even, input restored by identity)")

big = [i % 7 for i in range(50000)]
big = big + big[::-1]                   # length 100000 palindrome
head, nodes = build(big)
assert is_pal(head) and node_ids(head) == [id(x) for x in nodes]
print("palindrome of length", len(big), "ok, restored")
```

**Output (my run):**
```
[1, 2, 2, 1] -> True
[1, 2, 3, 2, 1] -> True
[1, 2] -> False
[1] -> True
[1, 0, 0] -> False
[1,2,3,2,1] after forgetting to restore, head onward: [1, 2, 3]
cross-check ok (2000 random lists, odd and even, input restored by identity)
palindrome of length 100000 ok, restored
```

**Edge cases:**
- One node: slow is the head, reversal of one node, compare with itself, True.
- Two equal nodes: slow is the second node, compares 1 node, True.
- Odd length: middle compares with itself, no special code needed.
- Length 100000: iterative reversal, no recursion.

**Follow-ups:**
- Can we modify the list? If the caller does not mind, skip the restore. Otherwise restore, especially in a shared or concurrent setting.
- Doubly linked list? Two pointers from both ends, no reversal needed.
- Recursive version? Uses O(n) stack, and fails on 10^5 nodes in Python.

**Common mistakes:**
- Not restoring. The first half's last node still points at the old middle, which is now the tail of the reversed half, so the list reads as a shorter list (the code shows `[1,2,3,2,1]` becoming `[1, 2, 3]`).
- Using the first middle for even n and mis-sizing the halves.
- Returning early on a mismatch before restoring.

### Q8 ⭐⭐⭐ 🟡 Add two numbers stored in reverse order. Nodes are `ListNode(val, next)`. Two non-empty lists (1 <= len <= 100, digits 0-9, no leading zeros except the number 0 itself) hold non-negative integers with the LEAST significant digit first. Return a new list for their sum in the same order. Walk both lists with a carry and a dummy head, and loop while either list or the carry is non-zero. Explain why a final carry can add a node and why you must not convert to an int (state what the int route costs and when it is fine in Python). Example: [2,4,3] and [5,6,4] -> [7,0,8] (342 + 465 = 807); [0] and [0] -> [0]; [9,9,9,9] and [1] -> [0,0,0,0,1]; [5] and [5] -> [0,1].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Digit-by-digit addition with a carry, building the result behind a dummy head. The reversed storage means the least significant digit comes first, which is the order addition needs.

**Say this first (1 line):** "Walk both lists together, add the digits plus the carry, write `sum % 10`, carry `sum // 10`, and keep looping while either list or the carry is non-zero."

**Brute force:** Convert each list to an int, add, convert the sum back to a list. Simple, and fine in Python for the sizes here (at most 100 digits), because Python integers have no overflow.

**Optimal:**
- `dummy = tail = ListNode()`, `carry = 0`.
- Loop while `a`, `b` or `carry`. Each round `s = carry + (a.val if a) + (b.val if b)`, then `carry, digit = divmod(s, 10)`, append `ListNode(digit)`, advance both lists if they are not None.
- Different lengths: the shorter list contributes 0 once it is exhausted.
- Final carry: 999 + 1: the last round ends with carry 1 and both lists empty. Without `or carry` the leading 1 is lost. The carry is at most 1 because 9 + 9 + 1 = 19.
- The sum is built in new nodes. The inputs are not modified.

**Complexity:** Time O(max(m, n)) rounds, plus one for the final carry. Space O(1) extra besides the output list, which needs O(max(m, n)) nodes.

**Why not int in general:** Building the int and the digit string costs O(n) extra memory, and converting a very long digit string to an int can be slow. Python 3.11+ also refuses `int()` on strings of more than 4300 digits by default (the code shows the ValueError). So it is fine for 100 digits, but it skips the point of the exercise, and interviewers often ask you not to use it. The pointer walk uses no big-number arithmetic and works the same in languages with fixed-size ints.

**Dry run:** `[2,4,3]` + `[5,6,4]`. Round 1: 2 + 5 = 7, digit 7, carry 0. Round 2: 4 + 6 = 10, digit 0, carry 1. Round 3: 3 + 4 + 1 = 8, digit 8, carry 0. Done: `7 -> 0 -> 8` (342 + 465 = 807).

**Code:**
```python
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
```

**Output (my run):**
```
[2, 4, 3] [5, 6, 4] -> [7, 0, 8]
[0] [0] -> [0]
[9, 9, 9, 9] [1] -> [0, 0, 0, 0, 1]
[5] [5] -> [0, 1]
cross-check ok (2000 random pairs up to 100 digits, many 9s, vs int addition)
int() of a 5000-digit string raises ValueError under the default limit
```

**Edge cases:**
- Zero plus zero: one round, digit 0, no carry, result `[0]`.
- Different lengths: `[9,9,9,9]` + `[1]`.
- Both numbers end with a carry: `[5]` + `[5]` gives `[0, 1]`.
- Inputs must be unchanged (the code checks values and node identity).

**Follow-ups:**
- Digits stored most significant first? Reverse both lists, or push digits on stacks and add from the stack tops, building the result by prepending nodes.
- Subtract or multiply? Same digit-wise idea with borrow or a convolution.
- Do it recursively? Possible with the carry returned up the stack, O(n) stack.

**Common mistakes:**
- Loop condition `while a and b`, which drops the longer tail.
- Forgetting the final carry.
- Reading `.val` of a None list.
- Returning `dummy` instead of `dummy.next`.

### Q9 ⭐⭐⭐ 🟡 Reorder list. Nodes are `ListNode(val, next)`. Rearrange a list L0 -> L1 -> ... -> Ln-1 IN PLACE (1 <= len <= 5*10^4, node values may repeat; do not modify values, only links) into L0 -> Ln-1 -> L1 -> Ln-2 -> L2 -> ... Use three steps: find the middle, reverse the second half, interleave the two halves; state exactly where the list is cut so odd lengths put the extra node in the first half. O(n) time, O(1) space; the tests check node identity. Example: [1,2,3,4] -> [1,4,2,3]; [1,2,3,4,5] -> [1,5,2,4,3]; [1] -> [1]; [1,2] -> [1,2].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Find the middle, reverse the second half, merge the two halves alternately. Three small list routines in sequence.

**Say this first (1 line):** "Cut after the first half, reverse the second half, then weave one node from each. O(n) time, O(1) space, links only."

**Brute force:** Put the nodes in an array and rewire them with two indices `i` and `j` (first, last, second, second-to-last, ...). O(n) time, O(n) space.

**Optimal:**
- Find the cut with `slow = fast = head` and `while fast.next and fast.next.next`. Slow stops on the LAST node of the first half.
- Odd n = 2m + 1: slow at index m, first half has m + 1 nodes (the extra middle node stays in the first half). Even n = 2m: slow at index m - 1, first half has m nodes.
- `second = reverse(slow.next)`, then `slow.next = None` to cut. Now the first half has ceil(n / 2) nodes and the second half has floor(n / 2).
- Interleave: while `second` is not None, take `first.next` and `second.next` into temporaries, set `first.next = second`, `second.next = old first.next`, advance both. The second half is never longer than the first, so looping on `second` is enough; the leftover extra node (odd n) is already in place at the end.
- Invariant: the woven prefix is correct and `first`/`second` are the unwoven fronts.

**Complexity:** Time O(n): find middle, reverse and weave are each linear. Space O(1).

**Dry run:** `[1,2,3,4,5]`. Start slow = fast = 1. Round 1: slow = 2, fast = 3 (`fast.next.next` is 5, so go on). Round 2: slow = 3, fast = 5. Now `fast.next` is None, stop. slow = 3. Second = reverse(`4 -> 5`) = `5 -> 4`; cut: first = `1,2,3`. Weave: 1 -> 5 -> 2 -> 4 -> 3. Result `[1,5,2,4,3]`.

**Code:**
```python
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
def reverse(head):
    prev = None
    while head is not None:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

# ---------- brute force: node array and two indices (O(n) space) ----------
def reorder_order_brute(nodes):
    order, i, j = [], 0, len(nodes) - 1
    while i <= j:
        order.append(nodes[i])
        if i != j:
            order.append(nodes[j])
        i += 1
        j -= 1
    return order

# ---------- optimal: middle, reverse second half, interleave ----------
def reorder(head):
    if head is None or head.next is None:
        return head
    slow = fast = head
    while fast.next and fast.next.next: # slow stops at the LAST node of the first half
        slow = slow.next
        fast = fast.next.next
    second = reverse(slow.next)         # second half starts after slow
    slow.next = None                    # the cut: first half has ceil(n/2) nodes
    first = head
    while second is not None:           # second half is never longer than the first
        f_next, s_next = first.next, second.next
        first.next = second
        second.next = f_next
        first, second = f_next, s_next
    return head

for arr, exp in [([1,2,3,4],[1,4,2,3]), ([1,2,3,4,5],[1,5,2,4,3]), ([1],[1]), ([1,2],[1,2])]:
    head, nodes = build(arr)
    out = reorder(head)
    assert out is head and to_list(out) == exp
    assert node_ids(out) == [id(n) for n in reorder_order_brute(nodes)]
    print(arr, "->", to_list(out))

count = 0
for n in range(1, 61):                  # exhaustive over lengths, distinct values
    arr = list(range(n))
    head, nodes = build(arr)
    out = reorder(head)
    assert node_ids(out) == [id(x) for x in reorder_order_brute(nodes)]
    assert len(set(node_ids(out))) == n # no node lost or repeated, so no cycle either
    count += 1
print("exhaustive ok: lengths 1..60 (", count, "lists ), identity order matches the index pattern 0, n-1, 1, n-2, ...")

random.seed(9)
for _ in range(500):
    arr = [random.randint(0, 3) for _ in range(random.randint(1, 200))]   # repeats on purpose
    head, nodes = build(arr)
    out = reorder(head)
    assert node_ids(out) == [id(x) for x in reorder_order_brute(nodes)]
    assert to_list(out) == [x.val for x in reorder_order_brute(nodes)]
print("cross-check ok (500 random lists, repeated values, identity compared)")
head, nodes = build(list(range(50000)))
out = reorder(head)
assert node_ids(out) == [id(x) for x in reorder_order_brute(nodes)]
print("length 50000 ok")
```

**Output (my run):**
```
[1, 2, 3, 4] -> [1, 4, 2, 3]
[1, 2, 3, 4, 5] -> [1, 5, 2, 4, 3]
[1] -> [1]
[1, 2] -> [1, 2]
exhaustive ok: lengths 1..60 ( 60 lists ), identity order matches the index pattern 0, n-1, 1, n-2, ...
cross-check ok (500 random lists, repeated values, identity compared)
length 50000 ok
```

**Edge cases:**
- One node: return at once (nothing to do).
- Two nodes: slow stays at the head, second = `2`, weave gives the same order `[1,2]`.
- Odd length: the middle ends up last.
- Repeated values: the identity order check proves only links changed.
- 50000 nodes: all loops are iterative.

**Follow-ups:**
- Why not recursion? Depth n stack: the default limit of 1000 breaks at 50000 nodes.
- Variant that swaps adjacent pairs, or odd/even grouping? Different pointer patterns, other questions in this part.
- Can you skip the cut? No: without `slow.next = None` the first half still links into the second half and the weave makes a cycle.

**Common mistakes:**
- Not cutting the list at the middle.
- Using `while fast and fast.next`, which makes the first half too short for even n or puts the middle in the wrong half.
- Losing `first.next` or `second.next` before relinking.
- Changing values instead of links (the prompt forbids it).

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

**Pattern:** In-place sublist reversal with head insertion. A dummy node guarantees a node exists before position `left`, even when `left` is 1.

**Say this first (1 line):** "Walk to the node before `left`. Then `right - left` times, take the node after the current tail of the reversed part and insert it right after that 'before' node. One pass, O(1) space."

**Brute force:** Copy values to a Python list, reverse the slice `arr[left-1:right]`, rebuild. O(n) time, O(n) space, new nodes (or overwriting values). Another baseline: cut the sublist out, reverse it with Q1's function, and splice it back; that works but needs more pointers to save and reconnect.

**Optimal:**
- `dummy -> head`. Move `before` forward `left - 1` times, so `before.next` is the node at position `left`.
- `tail = before.next`. This node starts the reversed part at the front and ends up at its back, because everything is inserted in front of it.
- Repeat `right - left` times:
  - `moved = tail.next`
  - `tail.next = moved.next` (unlink `moved`)
  - `moved.next = before.next` (point it at the current front of the reversed part)
  - `before.next = moved` (make it the new front)
- Why it is one pass: you only walk to `left`, then do `right - left` constant-time moves, so the work is `right` steps. Why O(1): pointers only. There is no recursion and no list copy.
- Why the end reconnects by itself: `tail` is never moved, and its `next` is always the node after the part (the node at `right + 1`, or None). So the tail of the part is linked to the rest of the list at every step.
- `left == right`: the loop runs zero times, so nothing changes and the original head is returned.
- Values variant (candidate-reported Flipkart variant: the two boundaries are given as node values instead of positions): the reversal is the same. Only the first step changes: instead of counting `left - 1` steps, walk the list until you find the node holding the first value, and stop on the node before it; the end is found when the second value is seen (or you count `right - left` by walking to it first). The code finds the two positions by one walk and reuses the same function, assuming the values are distinct.

**Complexity:** Time O(right) which is at most O(n), one pass. Space O(1).

**Dry run:** [1,2,3,4,5], left=2, right=4. `before` = node 1, `tail` = node 2.
- Step 1: moved = 3. tail.next = 4. 3.next = 2 (before.next). before.next = 3. List: 1 -> 3 -> 2 -> 4 -> 5.
- Step 2: moved = 4. tail.next = 5. 4.next = 3. before.next = 4. List: 1 -> 4 -> 3 -> 2 -> 5.
- Done after right - left = 2 steps.

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
print('n = 500, whole list ok')
```

**Output (my run):**
```
[1, 2, 3, 4, 5] 2 4 -> [1, 4, 3, 2, 5]
[5] 1 1 -> [5]
[3, 5] 1 2 -> [5, 3]
[1, 2, 3] 1 3 -> [3, 2, 1]
[1, 2, 3] 2 2 -> [1, 2, 3]
exhaustive (length, left, right) triples ok: 165
value variant and random cross-check ok (300 cases)
n = 500, whole list ok
```

**Edge cases:**
- `left == right`: no-op.
- `left == 1`: the head changes; the dummy handles it.
- `right == len`: `tail.next` becomes None at the end; no special case.
- Single node.
- Whole list (`left = 1`, `right = len`): same as a full reverse.

**Follow-ups:**
- Why not the standard three-pointer reversal? You can: reverse the part and then reconnect `before` and the node after. It needs two extra saved pointers. Head insertion keeps the invariant simple.
- Recursive version? Possible, but depth is about `right`, so it hits the recursion limit on long lists (Q26 in this part).
- k-group reversal? That is Q13 in this part; it applies this idea repeatedly.

**Common mistakes:**
- Walking `left` steps instead of `left - 1`, so `before` lands on the first node of the part.
- Inserting after `tail` instead of after `before` (that does not reverse).
- Updating `before.next` before saving `moved.next`.
- Forgetting the dummy and special-casing `left == 1`.

### Q19 ⭐⭐ 🟡 Swap nodes in pairs. Nodes are `ListNode(val, next)`. Given a list (0 <= len <= 100), swap every two adjacent nodes by changing LINKS, not values (tests check identity: the node objects themselves must move), and return the new head. A last unpaired node stays. Write it iteratively with a dummy and three pointers per pair, and recursively, and say what each rewires and why the order of the three assignments matters. Example: [1,2,3,4] -> [2,1,4,3]; [1,2,3] -> [2,1,3]; [1] -> [1]; [] -> []; [1,2] -> [2,1].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Pointer rewiring with a dummy head. Each pair needs three link changes, and the node before the pair must be remembered.

**Say this first (1 line):** "I keep a `prev` before each pair, rewire three links in a safe order, then move `prev` to the old first node of the pair."

**Brute force:** Copy values to a Python list, swap pairs, write them back (or build new nodes). O(n) time, O(n) space if you copy, or O(1) if you swap values in place. It fails this question: the node objects must move, so a value swap is rejected by the identity check.

**Optimal:**
- Dummy head, `prev = dummy`. While `prev.next` and `prev.next.next` both exist, there is a full pair.
- Name the pair `a = prev.next`, `b = a.next`.
- Three assignments, in this order:
  1. `a.next = b.next` (a now skips b and keeps the rest of the list)
  2. `b.next = a` (b points back at a)
  3. `prev.next = b` (the earlier part enters the pair at b)
- Then `prev = a`, because a is now the second node of the pair and the tail of the finished part.
- Why the order matters: `b.next` is the only pointer to the rest of the list. If you overwrite it first (`b.next = a`), the rest is lost and `a.next = b.next` makes `a` point at itself.
- Recursive version: swap the rest first, `head.next = swap(b.next)`, then `b.next = head`, return `b`. Same three rewires, no dummy needed.
- Invariant: everything before `prev` (inclusive) is already swapped and linked to `prev.next`.

**Complexity:** Iterative: time O(n), each node is touched once; space O(1). Recursive: time O(n), stack depth n/2 pairs, so O(n) space (Q26 shows why that is a risk at about 1000 frames; at 100 nodes it is fine).

**Dry run:** [1,2,3] with dummy D. prev = D, a = 1, b = 2.
- a.next = b.next gives 1 -> 3. b.next = a gives 2 -> 1. D.next = 2. prev = node 1.
- List now: D -> 2 -> 1 -> 3. prev.next is 3 and prev.next.next is None, so no full pair. Return 2 -> 1 -> 3.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def brute(arr):                          # on a Python list: swap values pairwise
    a = list(arr)
    for i in range(0, len(a) - 1, 2):
        a[i], a[i + 1] = a[i + 1], a[i]
    return a

def swap_iter(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a = prev.next
        b = a.next
        a.next = b.next                  # 1: a skips b, keeps the rest of the list
        b.next = a                       # 2: b points back at a
        prev.next = b                    # 3: the previous part now enters at b
        prev = a                         # a is the new tail of the finished part
    return dummy.next

def swap_rec(head):
    if head is None or head.next is None:
        return head
    b = head.next
    head.next = swap_rec(b.next)         # a points at the already-swapped rest
    b.next = head
    return b

def swap_values(head):                   # the WRONG answer for this question: moves values, not nodes
    p = head
    while p and p.next:
        p.val, p.next.val = p.next.val, p.val
        p = p.next.next
    return head

def wrong_order(head):                   # step 2 before step 1: loses the rest of the list
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(10):                  # step cap: the bug would loop forever
        if not (prev.next and prev.next.next):
            break
        a = prev.next
        b = a.next
        b.next = a                       # b's old next (the rest) is gone
        a.next = b.next                  # now a.next is b.next is a: a self-loop
        prev.next = b
        prev = a
    return dummy.next

def run(fn, arr):
    head = from_array(arr)
    before = node_ids(head)
    res = fn(head)
    assert is_acyclic(res)
    expect_ids = list(before)            # nodes must be the same objects, pairs swapped
    for i in range(0, len(expect_ids) - 1, 2):
        expect_ids[i], expect_ids[i + 1] = expect_ids[i + 1], expect_ids[i]
    assert node_ids(res) == expect_ids, "node objects did not move as required"
    return to_array(res)

# examples from the prompt
for arr in ([1, 2, 3, 4], [1, 2, 3], [1], [], [1, 2]):
    assert run(swap_iter, arr) == run(swap_rec, arr) == brute(arr)
    print(arr, "->", run(swap_iter, arr))

# exhaustive over lengths 0..10 plus 500 seeded random lists with repeated values
for n in range(11):
    arr = list(range(n))
    assert run(swap_iter, arr) == run(swap_rec, arr) == brute(arr)
random.seed(19)
for _ in range(500):
    arr = [random.randint(-3, 3) for _ in range(random.randint(0, 100))]
    assert run(swap_iter, arr) == run(swap_rec, arr) == brute(arr)
print("cross-check ok")

# value swapping gives the right values but fails the identity check
try:
    run(swap_values, [1, 2, 3, 4])
    print("value swap passed identity (unexpected)")
except AssertionError:
    print("value swap: right values, fails identity check")

# wrong assignment order creates a cycle (caught by the Floyd check, no hang)
h = wrong_order(from_array([1, 2, 3, 4]))
print("wrong order acyclic?", is_acyclic(h))
assert not is_acyclic(h)
```

**Output (my run):**
```
[1, 2, 3, 4] -> [2, 1, 4, 3]
[1, 2, 3] -> [2, 1, 3]
[1] -> [1]
[] -> []
[1, 2] -> [2, 1]
cross-check ok
value swap: right values, fails identity check
wrong order acyclic? False
```

**Edge cases:**
- Empty list and single node: the loop does not run, the dummy returns the head unchanged.
- Odd length: the last node stays where it is.
- Repeated values: only the identity check proves that nodes moved, not values.
- Length 2: new head is the old second node, and the old first node must end with `next = None` (it does: `a.next = b.next`).

**Follow-ups:**
- Swap in groups of k? That is Q13 (reverse in k-groups); k = 2 is this problem.
- Why not just swap `val`? When values are the whole payload it is accepted in some settings, but if nodes carry other fields or outside references, swapping values changes what those references see.
- Can the recursion be removed? Yes, the iterative version is the same thing with `prev` carrying the context.

**Common mistakes:**
- Doing `b.next = a` first and losing the rest (the code block shows the resulting cycle).
- Forgetting the dummy and special-casing the head.
- Checking only `prev.next` and crashing on `prev.next.next` for odd lengths.
- Setting `prev = b` instead of `prev = a`.

### Q20 ⭐⭐ 🟡 Odd-even list. Nodes are `ListNode(val, next)`. Group all nodes at ODD positions (1-based) first, then those at EVEN positions, keeping the relative order inside each group; this is about positions, not values. Do it in place in O(n) time and O(1) extra space (nodes are reused, so the tests check identity) with two chains and a joining step. Explain the loop condition `even and even.next` and what is wrong with testing odd instead, and where the odd tail connects to the even head. Example: [1,2,3,4,5] -> [1,3,5,2,4]; [2,1,3,5,6,4,7] -> [2,3,6,7,1,5,4]; [1] -> [1]; [1,2] -> [1,2]; [] -> [].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Two chains built in place by pointer splitting (odd-position chain and even-position chain), then one join. It is a positions problem, not a values problem.

**Say this first (1 line):** "Odd runs along the odd positions, even along the even ones, I skip each over the other, and at the end I hang the even chain behind the odd tail."

**Brute force:** Read the nodes into a Python list, take `nodes[0::2] + nodes[1::2]`, relink them. O(n) time, O(n) space for the list of node references.

**Optimal:**
- `odd = head`, `even = head.next`, and remember `even_head = even` (you lose it otherwise).
- Loop `while even and even.next`:
  - `odd.next = even.next; odd = odd.next` (odd jumps to the next odd position)
  - `even.next = odd.next; even = even.next` (even jumps to the next even position)
- After the loop: `odd.next = even_head`.
- Why test `even`: even is always ahead of odd. `even and even.next` means "there is another odd node after this even node", so both jumps are legal. Length 1 gives `even = None`, loop skipped, join with `None` is harmless.
- Why not test `odd`: for an even length, `odd.next` still exists (it is the last even node), so the loop runs once more, makes `odd = None` and then reads `odd.next`. The code shows an AttributeError for lengths 2, 4, 6, 8.
- The even chain already ends in None: for an odd length the last step set `even.next = odd.next = None`; for an even length the last even node was already the tail.
- Invariant: before each iteration, `odd` is the last node of the odd chain so far, `even` the last of the even chain, and the unprocessed rest starts at `even.next`.

**Complexity:** Time O(n), each node visited once. Extra space O(1): four pointers, no new nodes.

**Dry run:** [1,2,3,4,5]. odd = 1, even = 2, even_head = 2.
- Iteration 1: 1.next = 3, odd = 3; 2.next = 3.next = 4, even = 4.
- Iteration 2: even.next = 5 exists. 3.next = 5, odd = 5; 4.next = 5.next = None, even = None.
- Loop ends (even is None). odd.next = even_head: 5 -> 2. Result 1 -> 3 -> 5 -> 2 -> 4.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def brute_ids(ids):                      # on a Python list: positions 1,3,5,... then 2,4,6,...
    return ids[0::2] + ids[1::2]

def odd_even(head):
    if head is None:
        return None
    odd = head
    even = head.next
    even_head = even
    while even and even.next:            # even runs ahead of odd, so test even
        odd.next = even.next             # odd skips over an even node
        odd = odd.next
        even.next = odd.next             # even skips over the new odd node
        even = even.next
    odd.next = even_head                 # join: odd tail -> even head
    return head

def odd_even_wrong(head):                # tests odd instead of even
    if head is None:
        return None
    odd = head
    even = head.next
    even_head = even
    while odd and odd.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next             # odd can be None here for even lengths
        even = even.next
    odd.next = even_head
    return head

def run(arr):
    head = from_array(arr)
    before = node_ids(head)
    res = odd_even(head)
    assert is_acyclic(res)
    assert node_ids(res) == brute_ids(before), "same nodes, odd positions then even positions"
    assert to_array(res) == arr[0::2] + arr[1::2]
    return to_array(res)

for arr in ([1, 2, 3, 4, 5], [2, 1, 3, 5, 6, 4, 7], [1], [1, 2], []):
    print(arr, "->", run(arr))

for n in range(0, 12):                   # every length 0..11
    run(list(range(n)))
random.seed(20)
for _ in range(500):
    run([random.randint(-5, 5) for _ in range(random.randint(0, 60))])
print("cross-check ok")

# testing odd instead of even breaks on even lengths
bad = []
for n in range(1, 9):
    try:
        odd_even_wrong(from_array(list(range(n))))
    except AttributeError:
        bad.append(n)
print("wrong loop condition raises for lengths:", bad)
assert bad == [2, 4, 6, 8]
```

**Output (my run):**
```
[1, 2, 3, 4, 5] -> [1, 3, 5, 2, 4]
[2, 1, 3, 5, 6, 4, 7] -> [2, 3, 6, 7, 1, 5, 4]
[1] -> [1]
[1, 2] -> [1, 2]
[] -> []
cross-check ok
wrong loop condition raises for lengths: [2, 4, 6, 8]
```

**Edge cases:**
- Empty list: return `None` before touching `head.next`.
- One node and two nodes: nothing to rearrange.
- Values are irrelevant (the second example has odd and even values mixed); only positions matter.
- Odd length vs even length end differently; both are covered by the loop condition.

**Follow-ups:**
- Group by value parity instead? Different problem: two dummy chains and a stable partition (Q21).
- Stable? Yes, relative order inside each group is kept.
- Singly vs doubly linked: no change in the idea, but `prev` pointers need fixing too.

**Common mistakes:**
- Not saving `even_head`.
- Looping on `odd` and crashing on even lengths.
- Forgetting the final join, or joining before the loop ends.
- Reading "odd" as odd values instead of odd positions.

### Q21 ⭐⭐ 🟡 Partition a list around a value. Nodes are `ListNode(val, next)`. Given a list (0 <= len <= 200) and an integer x, rearrange so that all nodes with value < x come before all nodes with value >= x, preserving the original relative order inside each part (a stable partition), reusing the nodes. Build two chains with two dummy heads, then join them and terminate the second chain with None; explain why forgetting that last step can create a cycle. O(n) time, O(1) extra space. Example: [1,4,3,2,5,2], x=3 -> [1,2,2,4,3,5]; [2,1], x=2 -> [1,2]; [], x=0 -> []; [3,3], x=3 -> [3,3]; [1,2,3], x=4 -> [1,2,3].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Stable two-way partition with two dummy-headed chains, appended in place, then joined.

**Say this first (1 line):** "Walk once, append each node to a 'small' chain or a 'large' chain, then join small to large and cut the large tail."

**Brute force:** Copy values to a Python list, build `[v for v in a if v < x] + [v for v in a if v >= x]`, write back or rebuild. O(n) time, O(n) space, and it creates new nodes or rewrites values.

**Optimal:**
- Two dummies: `small_d`, `large_d`; tails `s`, `l` start at the dummies.
- For each node: if `val < x` append to the small chain, else to the large chain. Appending reuses the node, so order inside each chain is the original order (stable).
- After the loop: `l.next = None`, then `s.next = large_d.next`, return `small_d.next`.
- Why the dummies: either chain may stay empty, and the dummy means no special case for the first append and for an empty small part (the head of the answer is then `large_d.next`, which `s.next = large_d.next` gives for free).
- Why `l.next = None` is essential: the last node of the large chain still carries its ORIGINAL `next`. If the original tail went to the small chain, that old pointer leads back into the list. After the join the large tail points into the small chain, and the small chain leads to the large chain: a cycle. The code block builds exactly that.
- Order of the last two lines: any, as long as both happen after the loop.
- Invariant: each chain contains the nodes seen so far with the right property, in original order; the unseen suffix starts at `head`.

**Complexity:** Time O(n), one pass. Extra space O(1) (two dummies and two tails), no new data nodes.

**Dry run:** [1,4,3,2,5,2], x = 3.
- 1 small, 4 large, 3 large, 2 small, 5 large, 2 small. small: 1,2,2. large: 4,3,5.
- `l.next = None` cuts the 5 away from the last 2. Join 2 -> 4. Result 1 -> 2 -> 2 -> 4 -> 3 -> 5.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def brute_ids(ids, vals, x):             # stable partition on Python lists
    idx = [i for i in range(len(vals)) if vals[i] < x] + [i for i in range(len(vals)) if vals[i] >= x]
    return [ids[i] for i in idx], [vals[i] for i in idx]

def partition(head, x):
    small_d = ListNode()
    large_d = ListNode()
    s, l = small_d, large_d
    while head:
        if head.val < x:
            s.next = head
            s = head
        else:
            l.next = head
            l = head
        head = head.next
    l.next = None                        # terminate: l may still point into the small part
    s.next = large_d.next                # join small chain to large chain
    return small_d.next

def partition_no_terminate(head, x):     # the classic bug: forgets l.next = None
    small_d = ListNode()
    large_d = ListNode()
    s, l = small_d, large_d
    while head:
        nxt = head.next
        if head.val < x:
            s.next = head
            s = head
        else:
            l.next = head
            l = head
        head = nxt
    s.next = large_d.next                # no l.next = None
    return small_d.next

def run(arr, x):
    head = from_array(arr)
    before = node_ids(head)
    res = partition(head, x)
    assert is_acyclic(res)
    ids, vals = brute_ids(before, arr, x)
    assert node_ids(res) == ids and to_array(res) == vals
    return to_array(res)

for arr, x in (([1, 4, 3, 2, 5, 2], 3), ([2, 1], 2), ([], 0), ([3, 3], 3), ([1, 2, 3], 4)):
    print(arr, "x =", x, "->", run(arr, x))

random.seed(21)
for _ in range(600):
    arr = [random.randint(-4, 6) for _ in range(random.randint(0, 40))]
    run(arr, random.randint(-5, 7))
for n in range(7):                       # all 0/1/2 lists up to length 6 with every x in 0..3
    for t in range(3 ** n):
        arr = [(t // 3 ** i) % 3 for i in range(n)]
        for x in range(4):
            run(arr, x)
print("cross-check ok")

h = partition_no_terminate(from_array([1, 4, 3, 2, 5, 2]), 3)
print("without l.next = None, acyclic?", is_acyclic(h))
assert not is_acyclic(h)
```

**Output (my run):**
```
[1, 4, 3, 2, 5, 2] x = 3 -> [1, 2, 2, 4, 3, 5]
[2, 1] x = 2 -> [1, 2]
[] x = 0 -> []
[3, 3] x = 3 -> [3, 3]
[1, 2, 3] x = 4 -> [1, 2, 3]
cross-check ok
without l.next = None, acyclic? False
```

**Edge cases:**
- Empty list: both chains empty, `s.next = None`, returns `None`.
- All nodes small or all large: one chain empty, the join still works.
- `x` equal to existing values: `val >= x` goes to the large side, so `[3,3], x=3` stays `[3,3]`.
- Negative values and repeats: handled by plain comparison.

**Follow-ups:**
- Three-way partition (less, equal, greater)? Three chains and two joins; same termination rule on the last chain.
- Do the nodes keep their order inside each part? Yes, this is the stable property the answer must say out loud.
- Can you do it with one chain only? Moving nodes around a single pointer is possible but easier to break; two chains are the safe version.

**Common mistakes:**
- Forgetting `l.next = None` (cycle, or an infinite print).
- Appending a node and then reading `head.next` after something changed it: here `head = head.next` runs right after the append and only the previous tail's `next` was changed, so it is safe; the unsafe one is the missing cut above.
- Using `<=` instead of `<`.
- Returning `head` instead of `small_d.next`.

### Q22 ⭐⭐ 🟡 Rotate a list to the right. Nodes are `ListNode(val, next)`. Rotate a list (0 <= len <= 500) to the right by k places, 0 <= k <= 2*10^9, and return the head: the last k nodes (k taken modulo the length) move to the front. Find the length and the tail in one pass, reduce k % n, then cut at position n - k % n; you may close the list into a ring temporarily. O(n) time, O(1) space; explain why k can be huge but the work cannot depend on k, and handle empty lists, single nodes and k % n == 0. Example: [1,2,3,4,5], k=2 -> [4,5,1,2,3]; [0,1,2], k=4 -> [2,0,1]; [1], k=99 -> [1]; [1,2], k=2 -> [1,2]; [] , k=3 -> []; [1,2,3], k=2000000000 -> [2,3,1].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Modular arithmetic plus a temporary ring: find length and tail, reduce `k % n`, cut at position `n - k % n`.

**Say this first (1 line):** "k only matters modulo n, so I measure the list, reduce k, close the list into a ring and cut it at the right spot."

**Brute force:** Rotate by one k times: find the second-to-last node, move the tail to the front. O(n) per step, O(n * k) total; with k up to 2*10^9 it never finishes. Also a Python-list version `a[-k:] + a[:-k]` is O(n) time and space (after `k %= n`).

**Optimal:**
- Empty list or one node: return `head`.
- One pass for the length `n` and the `tail`.
- `k %= n`. If `k == 0`, nothing to do, return `head`.
- Join `tail.next = head` (a ring). The new tail is the node at 1-based position `n - k`; walk `n - k - 1` steps from `head`. The new head is `new_tail.next`. Set `new_tail.next = None`.
- Why the work does not depend on k: `k` enters only through `k % n`, which is O(1) on a Python int; walking is at most n steps.
- Without the ring: walk to position `n - k`, set `new_head = new_tail.next`, `new_tail.next = None`, `tail.next = head`. Same thing.
- Invariant: the ring contains all n nodes, so cutting after any node yields a valid rotation.

**Complexity:** Time O(n): one pass for the length and at most one more walk. Space O(1).

**Dry run:** [1,2,3,4,5], k = 2. n = 5, tail = 5, k % 5 = 2. Ring: 5 -> 1. Walk n - k - 1 = 2 steps from 1: reach 3. New head = 4. Cut 3.next. Result 4 -> 5 -> 1 -> 2 -> 3.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def brute(arr, k):                       # simulate k single right-rotations (small k only)
    a = list(arr)
    for _ in range(k):
        if a:
            a.insert(0, a.pop())
    return a

def rotate_right(head, k):
    if head is None or head.next is None:
        return head
    n, tail = 1, head
    while tail.next:                     # length and tail in one pass
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head                     # close the ring
    new_tail = head
    for _ in range(n - k - 1):           # new tail is the node at position n - k
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None                 # open the ring
    return new_head

def run(arr, k):
    head = from_array(arr)
    before = node_ids(head)
    res = rotate_right(head, k)
    assert is_acyclic(res)
    n = len(arr)
    s = (n - k % n) % n if n else 0      # rotation as a left shift of ids
    assert node_ids(res) == before[s:] + before[:s], "same nodes, rotated"
    return to_array(res)

for arr, k in (([1, 2, 3, 4, 5], 2), ([0, 1, 2], 4), ([1], 99), ([1, 2], 2), ([], 3), ([1, 2, 3], 2000000000)):
    print(arr, "k =", k, "->", run(arr, k))
    if k <= 100:
        assert run(arr, k) == brute(arr, k)
assert 2000000000 % 3 == 2

random.seed(22)
for _ in range(600):
    arr = [random.randint(-5, 5) for _ in range(random.randint(0, 25))]
    k = random.randint(0, 60)
    assert run(arr, k) == brute(arr, k)
for n in range(0, 9):                    # every k in 0..3n for each length
    for k in range(3 * n + 1):
        assert run(list(range(n)), k) == brute(list(range(n)), k)
big = list(range(500))
r = (2 * 10**9 + 7) % 500
assert run(big, 2 * 10**9 + 7) == big[-r:] + big[:-r]
print("cross-check ok")
```

**Output (my run):**
```
[1, 2, 3, 4, 5] k = 2 -> [4, 5, 1, 2, 3]
[0, 1, 2] k = 4 -> [2, 0, 1]
[1] k = 99 -> [1]
[1, 2] k = 2 -> [1, 2]
[] k = 3 -> []
[1, 2, 3] k = 2000000000 -> [2, 3, 1]
cross-check ok
```

**Edge cases:**
- Empty list: return `None` before reading `head.next`.
- `k % n == 0` (k = 0, or k a multiple of n): return the original head and do not make a ring (a ring left open would be a cycle).
- Single node with huge k: the early return.
- k bigger than n and k = 2*10^9: the reduction handles both.

**Follow-ups:**
- Rotate left? Rotate right by `n - k % n`, or cut at position `k % n`.
- Why is the answer to "rotate right by k" the last k nodes in front? The last `k % n` nodes are exactly the ones that wrap around.
- Doubly linked version? Same plan, plus fix the `prev` pointers at the two cut ends.

**Common mistakes:**
- Forgetting `k %= n` (a loop to k, or walking off the end).
- Off-by-one in the walk: `n - k - 1` steps from the head, not `n - k`.
- Leaving the ring closed when `k % n == 0`.
- On a Python list, `a[-k:] + a[:-k]` with `k = 0` gives `a[-0:]` (the whole list) plus `a[:-0]` (empty), which happens to be right here, but with `k == n` after reduction you must still reduce first; handle `k % n == 0` explicitly.

### Q23 ⭐⭐ 🟡 Add two numbers stored in forward order. Nodes are `ListNode(val, next)`. Two non-empty lists (1 <= len <= 100, digits 0-9, no leading zeros except 0 itself) hold non-negative integers with the MOST significant digit first. Return their sum as a new list in the same order WITHOUT reversing the inputs. Give two ways: push the digits on two stacks (Python lists) and add from the end building the result by head insertion, and reverse-add-reverse (which mutates the inputs unless you restore them); say which preserves the inputs and what each costs in space. Example: [7,2,4,3] and [5,6,4] -> [7,8,0,7] (7243 + 564 = 7807); [2,4,3] and [5,6,4] -> [8,0,7]; [0] and [0] -> [0]; [9,9] and [1] -> [1,0,0].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Candidate-reported rounds on Naukri Code360 (an Amazon on-campus March 2021 entry listing flatten of a multilevel list with child pointers; an Amazon December 2021 entry tied to adding two numbers held as lists; Flipkart 2020 and 2021 entries naming reverse linked list, one with an O(n) time O(1) space follow-up and one solved first with a stack; plus a LeetCode discuss Flipkart SDE-1 June 2024 report of a Reverse Linked List II variant given node values instead of positions; snippets only, not opened; candidate-reported, unverified, not evidence of current practice)

**Pattern:** Digit addition with a carry, from the least significant end of a forward-order list. The stack (or a double reversal) gives access to that end; the result is built by head insertion.

**Say this first (1 line):** "Push both lists on stacks, pop from the end adding with a carry, and put each new digit node in FRONT of the result."

**Brute force:** Convert both lists to integers (`v = v * 10 + d`), add, convert the sum back to nodes. O(m + n) digit steps for a 100-digit number, easy in Python since ints do not overflow. It works here, but it is a trick the interviewer usually forbids, and converting a huge int to a string is not linear time.

**Optimal (stacks):**
- Walk each list once, appending values to a Python list used as a stack.
- Loop while a stack is non-empty or `carry` is non-zero: `s = carry + pop_a + pop_b`, `carry, d = divmod(s, 10)`, `result = ListNode(d, result)`.
- The final carry becomes a leading node ([9,9] + [1] gives [1,0,0]).
- Inputs are never touched.

**Optimal (reverse-add-reverse):**
- Reverse both lists in place, add as in the reverse-order problem (Q8), reverse the sum.
- Mutates the inputs: after the first reversal the old head is the tail. Reverse them again before returning to leave the caller's lists as they were.
- Extra space: only the output nodes (O(1) besides them), versus O(m + n) for the stacks.

**Complexity:** Both are O(m + n) time. Stacks: O(m + n) extra space. Reverse version: O(1) extra besides the output, but four reversals plus the add.

**Dry run:** [7,2,4,3] + [5,6,4]. Stacks: [7,2,4,3] and [5,6,4].
- pop 3 + 4 = 7, carry 0, result 7. pop 4 + 6 = 10, digit 0, carry 1, result 0 -> 7.
- pop 2 + 5 + carry 1 = 8, result 8 -> 0 -> 7. pop 7 + 0 = 7, result 7 -> 8 -> 0 -> 7. Stacks empty, carry 0. Answer 7807.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


def to_int(head):
    v = 0
    for d in to_array(head):
        v = v * 10 + d
    return v

def digits(n):
    return [int(c) for c in str(n)]

def rev(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

def add_stacks(a, b):                    # inputs are only read
    sa, sb = [], []
    while a:
        sa.append(a.val)
        a = a.next
    while b:
        sb.append(b.val)
        b = b.next
    result, carry = None, 0
    while sa or sb or carry:
        s = carry + (sa.pop() if sa else 0) + (sb.pop() if sb else 0)
        carry, d = divmod(s, 10)
        result = ListNode(d, result)     # head insertion: new node in front
    return result

def add_reverse(a, b, restore=True):     # reverse both, add LSD first, reverse the sum
    ra, rb = rev(a), rev(b)
    dummy = tail = ListNode()
    carry = 0
    p, q = ra, rb
    while p or q or carry:
        s = carry + (p.val if p else 0) + (q.val if q else 0)
        carry, d = divmod(s, 10)
        tail.next = ListNode(d)
        tail = tail.next
        p = p.next if p else None
        q = q.next if q else None
    if restore:
        rev(ra)
        rev(rb)
    return rev(dummy.next)

def run(x, y, fn, **kw):
    a, b = from_array(digits(x)), from_array(digits(y))
    ia, ib = node_ids(a), node_ids(b)
    res = fn(a, b, **kw)
    assert is_acyclic(res)
    assert to_int(res) == x + y and to_array(res) == digits(x + y)
    assert node_ids(res) and not (set(node_ids(res)) & (set(ia) | set(ib))), "sum has its own nodes"
    assert node_ids(a) == ia and node_ids(b) == ib and to_array(a) == digits(x), "inputs restored"
    return to_array(res)

for arr1, arr2 in (([7, 2, 4, 3], [5, 6, 4]), ([2, 4, 3], [5, 6, 4]), ([0], [0]), ([9, 9], [1])):
    x, y = to_int(from_array(arr1)), to_int(from_array(arr2))
    r1, r2 = run(x, y, add_stacks), run(x, y, add_reverse)
    assert r1 == r2
    print(arr1, "+", arr2, "->", r1)

random.seed(23)
for _ in range(800):
    x = random.randint(0, 10 ** random.randint(0, 25))
    y = random.randint(0, 10 ** random.randint(0, 25))
    assert run(x, y, add_stacks) == run(x, y, add_reverse) == digits(x + y)
for x in range(0, 120):                  # all pairs below 120 (carry chains, 99 + 1, ...)
    for y in range(0, 120):
        assert run(x, y, add_stacks) == digits(x + y)
big = 10 ** 99 - 1
assert run(big, 1, add_stacks) == [1] + [0] * 99
print("cross-check ok")

# reverse-add-reverse WITHOUT restoring leaves the inputs reversed
a, b = from_array([7, 2, 4, 3]), from_array([5, 6, 4])
add_reverse(a, b, restore=False)
print("inputs after no-restore: a head now", a.val, "with next", a.next, "| a node is now the tail")
assert a.next is None
```

**Output (my run):**
```
[7, 2, 4, 3] + [5, 6, 4] -> [7, 8, 0, 7]
[2, 4, 3] + [5, 6, 4] -> [8, 0, 7]
[0] + [0] -> [0]
[9, 9] + [1] -> [1, 0, 0]
cross-check ok
inputs after no-restore: a head now 7 with next None | a node is now the tail
```

**Edge cases:**
- Different lengths: a drained stack contributes 0.
- Final carry: 99 + 1, and 9...9 + 1.
- [0] + [0]: the loop runs once and gives one node 0.
- Inputs must be unchanged: the identity check in the code verifies it for both methods.

**Follow-ups:**
- Recursion without stacks? Pad the shorter list with leading zeros, recurse to the end, add on the way back; the stack depth is the length (Q26).
- Subtract or multiply? Same digit-wise loop with borrow or schoolbook products; a typical extension.
- When is the int route fine? For quick scripts and small inputs; Python ints are exact, but it hides the algorithm being asked about.

**Common mistakes:**
- Building the result by appending (gives the digits reversed).
- Dropping the final carry.
- Reversing the inputs and returning without restoring them.
- Stopping when one list ends.

### Q24 ⭐⭐ 🟡 Remove ALL values that are duplicated in a sorted list. Nodes are `ListNode(val, next)`. The list is sorted ascending (0 <= len <= 300). Delete every node whose value appears more than once so that only values that occur exactly once remain; return the head, in place. Use a dummy head, a `prev` pointer that trails the last kept node, and skip each run of equal values entirely; explain why the dummy is required here and how this differs from keeping one copy of each value. Example: [1,2,3,3,4,4,5] -> [1,2,5]; [1,1,1,2,3] -> [2,3]; [1,1] -> []; [1,2,3] -> [1,2,3]; [] -> [].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Run skipping on a sorted list with a dummy head and a trailing `prev` that points at the last kept node.

**Say this first (1 line):** "Equal values sit in runs, so for each node I look at its successor; if they match I skip the whole run, and `prev` only moves when I keep a node."

**Brute force:** Count values with a `Counter` (or dict), then walk and unlink nodes whose count is above 1. O(n) time, O(n) space; it ignores the sorted property.

**Optimal:**
- Sortedness means duplicates are adjacent, so one pass and O(1) space are enough.
- `dummy -> head`, `prev = dummy`, `cur = head`.
- If `cur.next` exists and has the same value, remember `v = cur.val`, advance `cur` while `cur.val == v` (this removes the first copy too), then `prev.next = cur`. Do NOT move `prev`: `cur` has not been judged yet.
- Otherwise `cur` is a single: `prev = cur; cur = cur.next`.
- Why the dummy is required: the head itself can be removed ([1,1,2,3] -> [2,3]), and then there is no node whose `next` can be updated. The dummy gives `prev.next = cur` a home. In the keep-one version (Q15) the first node of a run always survives, so the head never changes and no dummy is needed.
- Invariant: everything up to `prev` is final and contains only values that occur once; `cur` starts an unjudged suffix.

**Complexity:** Time O(n), each node visited once (the inner loop advances `cur` too). Space O(1).

**Dry run:** [1,1,1,2,3]. prev = D, cur = 1 (first).
- cur.next.val == 1: skip the run, cur = 2. D.next = 2. prev stays D.
- cur = 2, next is 3 (different): keep, prev = 2, cur = 3. cur = 3, no next: keep. Result 2 -> 3.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True

import itertools
from collections import Counter

def brute(arr):                          # keep only values that occur exactly once
    c = Counter(arr)
    return [i for i, v in enumerate(arr) if c[v] == 1]

def remove_all_dups(head):
    dummy = ListNode(0, head)
    prev = dummy                         # last node known to be kept
    cur = head
    while cur:
        if cur.next and cur.next.val == cur.val:
            v = cur.val
            while cur and cur.val == v:  # skip the whole run
                cur = cur.next
            prev.next = cur              # prev stays; the next node is not yet judged
        else:
            prev = cur
            cur = cur.next
    return dummy.next

def keep_one(head):                      # contrast: keep first of each run (Q15)
    cur = head
    while cur and cur.next:
        if cur.next.val == cur.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head

def run(arr):
    head = from_array(arr)
    before = node_ids(head)
    res = remove_all_dups(head)
    assert is_acyclic(res)
    keep = brute(arr)
    assert node_ids(res) == [before[i] for i in keep], "same node objects, only singles"
    assert to_array(res) == [arr[i] for i in keep]
    return to_array(res)

for arr in ([1, 2, 3, 3, 4, 4, 5], [1, 1, 1, 2, 3], [1, 1], [1, 2, 3], []):
    print(arr, "->", run(arr))

# exhaustive: every sorted list of length 0..7 over values 0..3 (multisets)
count = 0
for n in range(8):
    for combo in itertools.combinations_with_replacement(range(4), n):
        run(list(combo)); count += 1
random.seed(24)
for _ in range(500):
    run(sorted(random.randint(-6, 6) for _ in range(random.randint(0, 40))))
print("cross-check ok, exhaustive lists:", count)

print("keep one copy  :", to_array(keep_one(from_array([1, 1, 1, 2, 3]))))
print("remove all dups:", to_array(remove_all_dups(from_array([1, 1, 1, 2, 3]))))
```

**Output (my run):**
```
[1, 2, 3, 3, 4, 4, 5] -> [1, 2, 5]
[1, 1, 1, 2, 3] -> [2, 3]
[1, 1] -> []
[1, 2, 3] -> [1, 2, 3]
[] -> []
cross-check ok, exhaustive lists: 330
keep one copy  : [1, 2, 3]
remove all dups: [2, 3]
```

**Edge cases:**
- Duplicates at the head or the tail: [1,1,2] and [1,2,2] -> [2] and [1].
- Whole list is one run: result is empty (the dummy's `next` becomes `None`).
- Runs longer than 2, and a run of 2 right after a single.
- Empty list and single node.

**Follow-ups:**
- Same for an unsorted list? Count first with a dict, or sort; with O(1) space it is O(n^2).
- Keep one copy of each? Q15: compare `cur` with `cur.next`, no dummy.
- Allow at most two copies? Compare with the node two back; a dummy is useful again.

**Common mistakes:**
- Moving `prev` after a skip (it may then point at a deleted node).
- Skipping only the later copies and keeping the first.
- No dummy, and crashing when the head is deleted.
- Forgetting the `cur and` guard in the inner loop.

### Q25 ⭐⭐ 🟡 Sort a list with merge sort in O(1) extra space. Nodes are `ListNode(val, next)`. Sort a list (0 <= len <= 5*10^4) ascending, stably (equal values keep their original order, tests check by identity), in O(n log n) time. Give the top-down merge sort (find the middle with slow and fast, cut, sort both halves, merge) and state its stack depth; then the BOTTOM-UP version with O(1) extra space: merge runs of size 1, 2, 4, ... using a `split(head, size)` helper that cuts off `size` nodes and a merge that returns head and tail. Say why arrays-style quicksort and index-based heap sort do not fit a list and why sorting a Python list copy is a valid but different answer (O(n) space). Example: [4,2,1,3] -> [1,2,3,4]; [-1,5,3,4,0] -> [-1,0,3,4,5]; [] -> []; [2,2,1,1] -> [1,1,2,2]; [1] -> [1].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Merge sort on a linked list: split by slow/fast pointers (or by run size), merge two sorted lists (Q3). Lists do merge for free, no shifting and no auxiliary array.

**Say this first (1 line):** "Merge sort: cut in the middle, sort both halves, merge them stably; for O(1) extra space I do it bottom-up with run sizes 1, 2, 4, and so on."

**Brute force:** Copy values into a Python list, `sorted()`, write back or rebuild. O(n log n) time, O(n) space. Valid, but a different answer: it does not rearrange the nodes unless you also sort node references (`sorted(nodes, key=...)`, still O(n) extra).

**Optimal (top-down):**
- Base case: 0 or 1 node.
- Find the middle with `slow = head`, `fast = head.next`; the loop leaves `slow` on the FIRST middle. Using `fast = head` would put `slow` on the second middle for even lengths and a 2-node list could split into 2 and 0, which recurses forever.
- Cut with `slow.next = None`, sort both halves, merge.
- Stability: the merge takes the left node unless the right value is strictly smaller.
- Stack depth: the recursion halves the list each time, so depth is about log2 n (the code prints 17 for 50000 nodes). Extra space is O(log n), not O(1).

**Optimal (bottom-up, O(1) extra):**
- Measure the length n. For `size = 1, 2, 4, ...` while `size < n`: walk the list once, repeatedly taking two runs of `size` nodes.
- `split(head, size)` keeps `size` nodes in the part starting at `head`, cuts, and returns the start of the rest.
- `merge(a, b)` returns the merged head AND tail, so the next merged run can be attached to `prev`.
- Why a tail is returned: re-walking to find it each time would be fine for the total (each merge costs its length anyway) but returning it is cleaner.
- Invariant after the pass with `size`: every block of `2 * size` consecutive nodes (the last one may be shorter) is sorted.

**Complexity:** Time O(n log n) for both: log n levels, each level merges n nodes in total. Space: bottom-up O(1); top-down O(log n) stack. The 50000-node bound is far below the recursion limit for top-down, since depth is about 17.

**Why not the array algorithms:** Heap sort needs index arithmetic (`2i + 1`) and O(1) random access. Quicksort's swap-based partition needs two-ended index access; a stable list partition exists (Q21) but picking a good pivot needs a walk, and the worst case is O(n^2). Merge sort needs only sequential access.

**Dry run:** [4,2,1,3], n = 4, bottom-up.
- size 1: runs (4)(2) -> 2,4; (1)(3) -> 1,3. List 2,4,1,3.
- size 2: runs (2,4)(1,3) -> 1,2,3,4. size 4 is not less than n: stop.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True

import sys

def merge(a, b):                         # stable: ties take a (the earlier part) first; returns (head, tail)
    dummy = tail = ListNode()
    while a and b:
        if b.val < a.val:
            tail.next = b; b = b.next
        else:
            tail.next = a; a = a.next
        tail = tail.next
    tail.next = a or b
    while tail.next:                     # walk to the true tail (needed by the bottom-up caller)
        tail = tail.next
    return dummy.next, tail

depth_seen = 0
def sort_top_down(head, depth=1):
    global depth_seen
    depth_seen = max(depth_seen, depth)
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next         # slow ends on the FIRST middle, so both halves shrink
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    right = slow.next
    slow.next = None                     # cut
    return merge(sort_top_down(head, depth + 1), sort_top_down(right, depth + 1))[0]

def split(head, size):                   # keep `size` nodes in head's part, return the rest
    for _ in range(size - 1):
        if head is None:
            break
        head = head.next
    if head is None:
        return None
    rest = head.next
    head.next = None
    return rest

def sort_bottom_up(head):
    n, p = 0, head
    while p:
        n += 1
        p = p.next
    dummy = ListNode(0, head)
    size = 1
    while size < n:
        prev, cur = dummy, dummy.next
        while cur:
            left = cur
            right = split(left, size)
            cur = split(right, size)     # split(None, size) is None
            h, t = merge(left, right)
            prev.next = h
            prev = t
        size *= 2
    return dummy.next

def run(fn, arr):
    head = from_array(arr)
    before = node_ids(head)
    res = fn(head)
    assert is_acyclic(res)
    order = sorted(range(len(arr)), key=lambda i: arr[i])      # Python's sort is stable
    assert node_ids(res) == [before[i] for i in order], "stable and in place"
    assert to_array(res) == sorted(arr)
    return to_array(res)

for arr in ([4, 2, 1, 3], [-1, 5, 3, 4, 0], [], [2, 2, 1, 1], [1]):
    assert run(sort_top_down, arr) == run(sort_bottom_up, arr)
    print(arr, "->", run(sort_bottom_up, arr))

random.seed(25)
for _ in range(600):
    arr = [random.randint(-5, 5) for _ in range(random.randint(0, 70))]   # many ties
    run(sort_top_down, arr); run(sort_bottom_up, arr)
for n in range(0, 9):                    # all 0/1/2 lists up to length 8
    for t in range(3 ** n):
        arr = [(t // 3 ** i) % 3 for i in range(n)]
        run(sort_bottom_up, arr); run(sort_top_down, arr)
print("cross-check ok")

big = [random.randint(0, 10**6) for _ in range(50000)]
depth_seen = 0
run(sort_top_down, big)
print("top-down recursion depth on 50000 nodes:", depth_seen, "(about log2 n + 1)")
run(sort_bottom_up, big)
print("bottom-up on 50000 nodes ok, no recursion")
print("default recursion limit:", sys.getrecursionlimit())
```

**Output (my run):**
```
[4, 2, 1, 3] -> [1, 2, 3, 4]
[-1, 5, 3, 4, 0] -> [-1, 0, 3, 4, 5]
[] -> []
[2, 2, 1, 1] -> [1, 1, 2, 2]
[1] -> [1]
cross-check ok
top-down recursion depth on 50000 nodes: 17 (about log2 n + 1)
bottom-up on 50000 nodes ok, no recursion
default recursion limit: 1000
```

**Edge cases:**
- Empty list and single node: `n < 2`, the loop is skipped.
- Already sorted or reversed input: same cost.
- All equal values: the identity check confirms stability (nodes keep order).
- A last run shorter than `size`: `split` returns `None` for the missing partner and `merge` just returns the single run.

**Follow-ups:**
- Why is the merge stable? On a tie it takes the left node; left nodes came earlier in the original list.
- Natural merge sort? Start from existing ascending runs; O(n) on sorted input.
- Sort a list of 10^6 nodes? Bottom-up avoids the recursion question (Q26).

**Common mistakes:**
- `fast = head` in top-down: infinite recursion on a 2-node list.
- Forgetting `slow.next = None`, so the left half still contains everything.
- Not reconnecting `prev.next` in the bottom-up passes.
- Using `<=` in the merge test (`b.val <= a.val` takes the right node on ties and breaks stability).
- Calling top-down "O(1) space".

### Q26 ⭐⭐ 🟡 Why a recursive list algorithm fails on long lists in Python. The recursive reverse `def rev(h): ... rev(h.next) ...` works on a list of 100 nodes but raises `RecursionError` on a list of 2000 nodes under the default recursion limit, while the iterative version handles 10^5 nodes. Write both, demonstrate the failure, and explain: Python's default limit (1000 frames; read it with `sys.getrecursionlimit()`), that the depth equals the list length here, why raising it with `sys.setrecursionlimit` is a risk to weigh (stack use, crashes) rather than a fix to rely on, and why the same applies to recursive printing, recursive length and recursive merge. State which common list algorithms are naturally recursive-friendly only for short inputs. Example: recursive reverse of [1,2,3,4,5] -> [5,4,3,2,1]; recursive reverse of a 100-node list works; recursive reverse of a 2000-node list under the default limit -> RecursionError; iterative reverse of a 2000-node list -> works.
**Asked at:** Python recursion-limit explainers (note.nkmk.me, educative.io, DEV Community recursion-limit posts; snippets only, not opened: default limit 1000, raising it risks crashes, iteration preferred); __slots__ behaviour not found in any snippet and was verified by running Python 3.13 in the sandbox | Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports

**Pattern:** Recursion depth equals list length. Python does not optimise tail calls, so each node costs one stack frame; the iterative loop costs none.

**Say this first (1 line):** "Recursive reverse needs one frame per node, and Python stops at about 1000 frames, so for long lists I use the loop."

**Brute force / baseline:** Recursive reverse: base case on `None` or the last node, `new_head = rev(h.next)`, then `h.next.next = h; h.next = None`. Time O(n), stack space O(n). Correct and short, and works for 100 nodes.

**Optimal:**
- Iterative reverse with `prev`, `cur`, `nxt`: time O(n), space O(1), no depth limit. The code runs it on 100,000 nodes.
- Why the recursive one fails: `sys.getrecursionlimit()` is 1000 by default (the code prints it). Depth reached is n plus the frames already in use, so a 2000-node list raises `RecursionError`. The code finds the smallest failing length in this sandbox; that number is environment-specific, not a constant.
- The failure happens on the way down, before any link is changed, so the list is left intact (the code checks).
- `sys.setrecursionlimit(n)`: it only raises the interpreter's own guard. The risks: memory for every frame, and in older or C-heavy paths a real stack overflow that crashes the process with no exception. It is a tuning knob you must justify, not a fix. (The code raises it to 10000 for a 5000-node demo and restores it.)
- Other recursive list code has the same wall: recursive printing, recursive length, recursive merge (code shows length and merge failing at 2000), recursive swap in pairs, recursive palindrome check, recursive k-group reverse (depth n/k), recursive list copy.
- Recursion-friendly only for short inputs: reverse, length, print, merge two lists, swap pairs, remove duplicates, and similar one-frame-per-node designs. Depth is fine when it is O(log n), as in top-down merge sort (Q25) and balanced tree recursion (Part 7).

**Complexity:** Recursive: O(n) time, O(n) stack. Iterative: O(n) time, O(1) space. Sizes in the demo are tests, not proof; the proof is the one-frame-per-node argument.

**Dry run:** rev([1,2,3]) calls rev([2,3]) calls rev([3]) which returns 3. Back in rev([2,3]): 3.next = 2, 2.next = None, return 3. Back in rev([1,2,3]): 2.next = 1, 1.next = None, return 3. Result 3 -> 2 -> 1; three frames deep. For 2000 nodes, frame 1001 raises.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True

import sys

def rev_it(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

def rev_rec(head):
    if head is None or head.next is None:
        return head
    new_head = rev_rec(head.next)        # one frame per node on the way down
    head.next.next = head
    head.next = None
    return new_head

def length_rec(head):
    return 0 if head is None else 1 + length_rec(head.next)

def merge_rec(a, b):                     # recursive merge of two sorted lists
    if a is None: return b
    if b is None: return a
    if b.val < a.val:
        b.next = merge_rec(a, b.next); return b
    a.next = merge_rec(a.next, b); return a

def fails(fn, n):
    try:
        fn(from_array(list(range(n))))
        return False
    except RecursionError:
        return True

print("default recursion limit:", sys.getrecursionlimit())

# correctness first, with identity, on short lists
random.seed(26)
for _ in range(400):
    arr = [random.randint(-9, 9) for _ in range(random.randint(0, 60))]
    h = from_array(arr); before = node_ids(h)
    r1 = rev_rec(h)
    assert to_array(r1) == arr[::-1] and node_ids(r1) == before[::-1]
    h = from_array(arr); before = node_ids(h)
    r2 = rev_it(h)
    assert to_array(r2) == arr[::-1] and node_ids(r2) == before[::-1]
print("recursive reverse of [1,2,3,4,5] ->", to_array(rev_rec(from_array([1, 2, 3, 4, 5]))))
print("recursive reverse, 100 nodes works:", not fails(rev_rec, 100))
print("recursive reverse, 2000 nodes RecursionError:", fails(rev_rec, 2000))
big = from_array(list(range(100000)))
print("iterative reverse, 100000 nodes ok:", to_array(rev_it(big))[:3], "...")
print("iterative reverse, 2000 nodes ok:", to_array(rev_it(from_array(list(range(2000)))))[:3], "...")

# the same wall for other recursive list code (2000 nodes)
print("recursive length, 2000 nodes fails:", fails(length_rec, 2000))
print("recursive merge, 2000 vs 2000 fails:", end=" ")
try:
    merge_rec(from_array(list(range(0, 4000, 2))), from_array(list(range(1, 4000, 2))))
    print(False)
except RecursionError:
    print(True)

# a failed descent changes nothing: the mutation happens on the way back
h = from_array(list(range(2000)))
try:
    rev_rec(h)
except RecursionError:
    pass
print("list unchanged after the failed call:", to_array(h) == list(range(2000)))

# where the wall is (sandbox, Python 3.13, called from module level; varies with caller depth)
n = 900
while not fails(rev_rec, n):
    n += 1
print("smallest failing length here:", n, "(limit", sys.getrecursionlimit(), "minus frames already in use)")

# raising the limit works but is a risk to weigh
old = sys.getrecursionlimit()
sys.setrecursionlimit(10000)
print("limit 10000, 5000 nodes works:", not fails(rev_rec, 5000))
sys.setrecursionlimit(old)
print("limit restored to", sys.getrecursionlimit())
```

**Output (my run):**
```
default recursion limit: 1000
recursive reverse of [1,2,3,4,5] -> [5, 4, 3, 2, 1]
recursive reverse, 100 nodes works: True
recursive reverse, 2000 nodes RecursionError: True
iterative reverse, 100000 nodes ok: [99999, 99998, 99997] ...
iterative reverse, 2000 nodes ok: [1999, 1998, 1997] ...
recursive length, 2000 nodes fails: True
recursive merge, 2000 vs 2000 fails: True
list unchanged after the failed call: True
smallest failing length here: 999 (limit 1000 minus frames already in use)
limit 10000, 5000 nodes works: True
limit restored to 1000
```

**Edge cases:**
- Empty list and single node: both versions return at once.
- Exactly at the limit: the failing length depends on how deep the caller already is (a test runner adds frames).
- Catching `RecursionError` leaves a recoverable program; a hard stack overflow does not.
- Cyclic list: the recursive versions never reach the base case and fail on any limit.

**Follow-ups:**
- Convert any recursion to a loop? Use an explicit stack (a Python list), or find the pointer-rewiring form as in reverse.
- Does tail recursion help? Not in CPython; there is no tail-call elimination.
- What about a thread with a bigger stack? `threading.stack_size` plus a higher limit is possible but fragile; prefer iteration.

**Common mistakes:**
- Raising the recursion limit as the first move.
- Claiming that 1000 is a hard constant: it is the default and can be read or set.
- Testing only on 5-node lists, so the depth failure is never seen.
- Writing the recursive version when the question says "up to 10^5 nodes".

### Q27 ⭐ 🟡 Remove duplicates from an UNSORTED list. Nodes are `ListNode(val, next)`. Given a list of integers (0 <= len <= 2000, unsorted, values may repeat), keep only the FIRST occurrence of each value and return the head, in place. Give the O(n) time, O(n) space version with a `set` of seen values, and the O(1)-space O(n^2) version that for each node scans the rest of the list to unlink later copies; explain the trade-off and why sorting first changes the surviving order. Example: [1,2,1,3,2,4] -> [1,2,3,4]; [5,5,5] -> [5]; [] -> []; [3,1,2] -> [3,1,2]; [2,1,2,1] -> [2,1].
**Asked at:** Linked-list pattern guides and question roundups (techinterview.org linked-list patterns page covering reverse, merge, cycle detection, fast-slow pointers and dummy nodes; a Substack linked-list prep post; techiedelight linked-list question list; a Questions100 linked-list category; DEV Community linked-list posts; search snippets only, not opened; WebFetch failed with getaddrinfo ENOTFOUND); tutorial content, not verified company reports | Standard-problem lists known to the editor (not found as an opened page; included on the editor's knowledge of widely circulated problem sets; indicative only, no company attribution)

**Pattern:** Dedupe in place with a `seen` set (time for space), or with a nested scan (space for time). The first occurrence survives.

**Say this first (1 line):** "With a set of seen values it is one pass and O(n) space; without extra space I scan the rest for each node, which is O(n^2)."

**Brute force:** For each node, scan the rest of the list and unlink later copies of its value. O(n^2) time, O(1) space. This is also the no-extra-memory answer.

**Optimal (time):**
- One pass with `prev` (last kept node) and `cur`. If `cur.val` is in `seen`, set `prev.next = cur.next` (do not move `prev`); else add it to `seen` and set `prev = cur`.
- No dummy is needed: the head is never a repeat, so `prev` is not `None` when an unlink happens.
- Expected O(n) time (hash lookups are O(1) on average), O(n) space for the set.
- The first occurrence is kept because the walk goes front to back.

**Optimal (space), nested scan:**
- For each `cur`, a `runner` starts at `cur` and checks `runner.next`: on a match, unlink it and do NOT advance the runner; otherwise advance.
- O(n^2) time, O(1) space; at 2000 nodes that is about 2 million steps, fine.

**Trade-off:** Set version: faster, more memory, values must be hashable (ints here). Nested version: no extra memory, works with only equality comparison, slow for large n.

**Why sorting first changes the order:** Sorting makes duplicates adjacent so you can use the sorted-list dedupe (Q15) in O(n log n) time and O(1) extra space for a merge-sorted list. But the result is in sorted order, not in the original first-occurrence order ([2,1,2,1] gives [1,2], but the required answer is [2,1]). To keep the original order you would have to sort pairs with the original index and sort back, which costs O(n) extra space again.

**Complexity:** Set: O(n) expected time, O(n) space. Nested scan: O(n^2) time, O(1) space.

**Dry run:** [2,1,2,1]. seen = {}. 2: new, keep, seen {2}. 1: new, keep, seen {1,2}. Second 2: in seen, prev (the 1) points past it to the last 1. Second 1: in seen, prev (the 1 at position 2) skips it. Result 2 -> 1.

**Code:**
```python
import random

class ListNode:
    __slots__ = ('val', 'next')
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def from_array(arr):
    dummy = tail = ListNode()
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_array(head, cap=10**6):          # cap: a bug that makes a cycle fails instead of hanging
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def node_ids(head, cap=10**6):          # identities of the nodes, in list order
    out = []
    while head is not None:
        out.append(id(head))
        head = head.next
        assert len(out) <= cap, "cycle or runaway list"
    return out

def is_acyclic(head):                   # Floyd, O(1) space
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return False
    return True


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
```

**Output (my run):**
```
[1, 2, 1, 3, 2, 4] -> [1, 2, 3, 4]
[5, 5, 5] -> [5]
[] -> []
[3, 1, 2] -> [3, 1, 2]
[2, 1, 2, 1] -> [2, 1]
cross-check ok
first-occurrence order: [2, 1] | sort first, then dedupe: [1, 2]
```

**Edge cases:**
- Empty list and a single node.
- All equal ([5,5,5]): every node after the first is unlinked.
- No duplicates: the list is unchanged.
- Negative values and zero: valid set members.

**Follow-ups:**
- Keep the LAST occurrence? Reverse first (or use a count pass, then keep when the remaining count hits 0).
- Remove all values that repeat (unsorted)? Count with a dict, then drop any node with count above 1; contrast with Q24 for the sorted case.
- Values that are not hashable? Use the O(n^2) scan, or key by a hashable form.

**Common mistakes:**
- Advancing the runner after an unlink and skipping a node.
- Moving `prev` after unlinking, so it points at a removed node.
- Using a set of nodes rather than values (every node is distinct, nothing is removed).
- Deduplicating by sorting and claiming the original order is preserved.

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

