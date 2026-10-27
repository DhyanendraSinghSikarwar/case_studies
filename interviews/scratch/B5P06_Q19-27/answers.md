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
assert run(big, 2 * 10**9) == big[-(2 * 10**9 % 500):] + big[:-(2 * 10**9 % 500)] if 2 * 10**9 % 500 else True
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
- Using `a[-k:]` with `k = 0` on a Python list (returns the whole list at the front: still correct by luck for `a[-0:] + a[:-0]`? It gives `a + []`; fine here, but `a[:-0]` is empty, so the tail part vanishes: handle `k == 0` explicitly).

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
