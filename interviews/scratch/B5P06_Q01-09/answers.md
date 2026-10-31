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

**Complexity:** Time O(mu + lambda) = O(n): phase 1 takes t < mu + lambda steps (t is the first multiple of lambda that is at least mu, at most mu + lambda - 1), phase 2 takes mu steps. Space O(1).

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
