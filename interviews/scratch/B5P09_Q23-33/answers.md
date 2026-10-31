### Q23 ⭐⭐ 🟡 Accounts merge (union-find on emails). `accounts` is a list of accounts, each `[name, email1, email2, ...]` (1 <= len(accounts) <= 1000, each with at least one email, emails lowercase). Two accounts belong to the same person if they share at least one email (directly or through a chain of accounts); different people may have the same name, and one email always maps to a single name. Return the merged accounts as `[name, sorted unique emails...]`, with the returned list sorted ascending as ordinary Python lists, so the answer is unique. Say what the union-find nodes are and the complexity. Example: accounts=[['john', 'a@x', 'b@x'], ['john', 'c@x'], ['john', 'b@x', 'd@x'], ['mary', 'e@x']] -> [['john', 'a@x', 'b@x', 'd@x'], ['john', 'c@x'], ['mary', 'e@x']]; accounts=[['sam', 's@x'], ['sam', 't@x']] -> [['sam', 's@x'], ['sam', 't@x']]; accounts=[['kim', 'k@x', 'k@x']] -> [['kim', 'k@x']].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Union-find (disjoint sets) for grouping by shared keys. The shared email is the link, so the emails are the nodes.

**Say this first (1 line):** "Names are not identities, emails are. I union all emails inside one account, then group emails by root, attach the name, sort."

**Brute force:** Keep a list of (name, email set). Find any two sets that intersect, merge them, restart. Repeat until no pair intersects. Each pass is O(A^2) set intersections and there can be O(A) passes, so O(A^2 * rounds) with big constants. It is the checker in the code.

**Optimal:**
- Nodes: every distinct email string. Not accounts (two accounts can be linked only through a third) and not names (two different people can be called "sam").
- For each account, `union(email_j, first_email)` for the other emails. Also record `name[email] = account name` (one email maps to one name, so overwriting is safe).
- After all unions, bucket every email by `find(email)`. Each bucket is one person. Output `[name, *sorted(bucket)]`, then sort the outer list.
- Chains work for free: A shares with B, B shares with C, so A and C end in one set although they share nothing directly.
- `find` is iterative with path halving, so no recursion limit problem on a chain of 1000 accounts.

**Complexity:** Let N be the total number of emails over all accounts (at most about 1000 times the longest account). Unions and finds: O(N * alpha(N)) with union by rank, and about O(N log N) worst case with path halving alone (what the code does; either is tiny). Sorting: O(N log N) for the emails inside buckets plus the sort of the result lists. Space O(N) for the parent map and groups.

**Dry run:** `[['john','a@x','b@x'], ['john','c@x'], ['john','b@x','d@x'], ['mary','e@x']]`.
- Account 1: parent has a, b. Union b into a's set: {a, b}.
- Account 2: c alone: {c}.
- Account 3: b already exists; d is new; union d with b's root: {a, b, d}.
- Account 4: {e}.
- Buckets: {a, b, d} named john, {c} named john, {e} named mary. Sorted: `[['john','a@x','b@x','d@x'], ['john','c@x'], ['mary','e@x']]`.

**Code:**
```python
import random
from collections import defaultdict

random.seed(23)

def accounts_merge(accounts):
    """Union-find over EMAILS (not accounts, not names). Iterative find with path halving."""
    parent, name = {}, {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for acc in accounts:
        for e in acc[1:]:
            parent.setdefault(e, e)
            name[e] = acc[0]
        for e in acc[2:]:                       # chain every email of the account to its first one
            ra, rb = find(e), find(acc[1])
            if ra != rb:
                parent[ra] = rb
    groups = defaultdict(list)
    for e in parent:
        groups[find(e)].append(e)
    return sorted([name[r], *sorted(es)] for r, es in groups.items())

def accounts_merge_brute(accounts):
    """Keep merging any two sets that share an email until nothing changes. O(A^2 * rounds)."""
    sets = [(a[0], set(a[1:])) for a in accounts]
    changed = True
    while changed:
        changed = False
        for i in range(len(sets)):
            for j in range(i + 1, len(sets)):
                if sets[i][1] & sets[j][1]:
                    sets[i] = (sets[i][0], sets[i][1] | sets[j][1])
                    del sets[j]
                    changed = True
                    break
            if changed:
                break
    return sorted([nm, *sorted(es)] for nm, es in sets)

def merge_by_name_wrong(accounts):
    """Common bug: treat the name as the identity."""
    by = defaultdict(set)
    for a in accounts:
        by[a[0]] |= set(a[1:])
    return sorted([n, *sorted(s)] for n, s in by.items())

# ---- examples from the prompt
ex = [
    ([['john', 'a@x', 'b@x'], ['john', 'c@x'], ['john', 'b@x', 'd@x'], ['mary', 'e@x']],
     [['john', 'a@x', 'b@x', 'd@x'], ['john', 'c@x'], ['mary', 'e@x']]),
    ([['sam', 's@x'], ['sam', 't@x']], [['sam', 's@x'], ['sam', 't@x']]),
    ([['kim', 'k@x', 'k@x']], [['kim', 'k@x']]),
]
for acc, want in ex:
    got = accounts_merge(acc)
    assert got == want == accounts_merge_brute(acc), (acc, got, want)
    print(acc, '->', got)

# ---- the name-as-identity bug
acc = ex[1][0]
print('merge by name (wrong) on the two sams ->', merge_by_name_wrong(acc))

# ---- chain: A-B share, B-C share, so A and C merge through B even though they share nothing directly
chain = [['z', 'e1', 'e2'], ['z', 'e3', 'e4'], ['z', 'e2', 'e3']]
print('chain ->', accounts_merge(chain))
assert accounts_merge(chain) == [['z', 'e1', 'e2', 'e3', 'e4']]

# ---- random cross-check, small email pool so merges and chains are frequent
def rand_accounts():
    k = random.randint(1, 8)
    emails = [f'{random.choice("abcdefgh")}{i}@x' for i in range(random.randint(1, 10))]
    emails = sorted(set(emails))
    owner = {e: random.choice(['ann', 'bob', 'cy']) for e in emails}      # one email -> one name
    accts = []
    for _ in range(k):
        sub = [random.choice(emails) for _ in range(random.randint(1, 4))]  # duplicates inside an account allowed
        # keep names consistent: the account name is the owner of its first email; all its emails must share that owner
        nm = owner[sub[0]]
        sub = [x for x in sub if owner[x] == nm]
        accts.append([nm, *sub])
    return accts
for _ in range(1000):
    acc = rand_accounts()
    assert accounts_merge(acc) == accounts_merge_brute(acc), acc
print('1000 seeded random inputs: union-find on emails == repeated set merging')

# ---- size: 1000 accounts forming one long chain (worst case for a naive recursive find)
n = 1000
big = [['w', f'm{i}@x', f'm{i+1}@x'] for i in range(n)]
res = accounts_merge(big)
assert len(res) == 1 and len(res[0]) == n + 2
print('1000-account chain merges into one account with', len(res[0]) - 1, 'emails')

# ---- edge cases
assert accounts_merge([['a', 'x@x']]) == [['a', 'x@x']]
assert accounts_merge([['a', 'x@x'], ['a', 'x@x']]) == [['a', 'x@x']]
assert accounts_merge([['b', 'p@x'], ['a', 'q@x']]) == [['a', 'q@x'], ['b', 'p@x']]
print('edge asserts passed')
```

**Output (my run):**
```
[['john', 'a@x', 'b@x'], ['john', 'c@x'], ['john', 'b@x', 'd@x'], ['mary', 'e@x']] -> [['john', 'a@x', 'b@x', 'd@x'], ['john', 'c@x'], ['mary', 'e@x']]
[['sam', 's@x'], ['sam', 't@x']] -> [['sam', 's@x'], ['sam', 't@x']]
[['kim', 'k@x', 'k@x']] -> [['kim', 'k@x']]
merge by name (wrong) on the two sams -> [['sam', 's@x', 't@x']]
chain -> [['z', 'e1', 'e2', 'e3', 'e4']]
1000 seeded random inputs: union-find on emails == repeated set merging
1000-account chain merges into one account with 1001 emails
edge asserts passed
```

**Edge cases:**
- Duplicate email inside one account (`['kim','k@x','k@x']`): union of a node with itself is a no-op, and the output has one copy.
- Same name, no shared email: stay separate (the second example).
- Same email in two accounts with the same name only: merges; one email maps to one name, so there is no name conflict to resolve.
- One account, one email: trivial group.
- Output ordering: sorting `[name, emails...]` lists compares the name first, then the first email, so ties between two people with the same name are broken by their smallest email. That is why the answer is unique.

**Follow-ups:**
- Why not nodes = accounts? You would need a map from email to the first account that owned it, then union accounts. It works too, but the email version has fewer moving parts.
- Why not DFS on an email graph? Also O(N), but you must build adjacency lists first, and with 1000 accounts you can still hit deep recursion; union-find does not.
- Online version (accounts arrive one at a time)? Union-find handles it directly; the group lists are rebuilt only when queried.

**Common mistakes:**
- Merging by name (the code prints the wrong answer for two sams).
- Forgetting to sort the emails or the final list.
- Recursive `find` without a depth guard on a long chain.
- Using the root's account name when roots are emails: fine, but only because one email has one name; do not take the name from an arbitrary account of the group if the statement allowed conflicts.

### Q24 ⭐⭐ 🟡 Parallel courses: minimum number of semesters. Courses are labelled 1..n (1 <= n <= 5000) and `relations` is a list of [prev, next] meaning prev must be finished in an earlier semester than next (0 <= len <= 5000). In each semester you may take any number of courses whose prerequisites were all completed in earlier semesters. Return the minimum number of semesters to finish all courses, or -1 if a cycle makes it impossible. Use Kahn's algorithm one level at a time and say what the answer is in terms of a longest path. Example: n=3, relations=[[1, 3], [2, 3]] -> 2; n=3, relations=[[1, 2], [2, 3], [3, 1]] -> -1; n=4, relations=[[1, 2], [2, 3], [3, 4]] -> 4; n=2, relations=[] -> 1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort by Kahn's algorithm, processed level by level. The number of levels is the length of the longest prerequisite chain.

**Say this first (1 line):** "Each semester I take everything with no unfinished prerequisite. That is one BFS level of Kahn's algorithm, so the answer is the number of levels, or -1 if some course never reaches in-degree zero."

**Brute force:** Longest-chain by relaxation: `d[c] = 1` for all courses, then repeat n times `d[next] = max(d[next], d[prev] + 1)` over every relation. If an edge can still improve after n rounds there is a cycle, so -1. Otherwise the answer is `max(d)`. O(n * E), about 25 million steps at the limits. It is the checker in the code.

**Optimal:**
- Build adjacency lists and in-degrees for courses 1..n.
- `cur` = all courses with in-degree 0. Each loop iteration is one semester: count it, add `len(cur)` to `done`, and for every course in `cur` decrement its neighbours' in-degrees; a neighbour that hits 0 goes into `nxt`.
- Stop when `cur` is empty. If `done == n` return the semester count, else a cycle blocked some courses: return -1.
- Why the number of levels is the longest path: a course can be taken no earlier than one semester after its latest prerequisite, and Kahn takes it exactly then. So the semester of a course is 1 + max(semester of prerequisites), which is the length (counted in courses) of the longest chain ending there. The answer is the maximum, the longest path in the DAG.
- Taking courses as early as possible never hurts, because finishing a course earlier only unlocks more.
- Duplicate relations are fine: the in-degree counts the edge twice and it is decremented twice.

**Complexity:** Time O(n + E): each course enters `cur` once, each relation is touched once. Space O(n + E) for the adjacency lists, in-degrees and level lists.

**Dry run:** `n=3, relations=[[1,3],[2,3]]`.
- In-degrees: 1 -> 0, 2 -> 0, 3 -> 2.
- Semester 1: `cur=[1,2]`, done = 2. Course 1 drops 3 to 1; course 2 drops 3 to 0, so `nxt=[3]`.
- Semester 2: `cur=[3]`, done = 3. No neighbours.
- `cur` empty, done == 3 == n, answer 2.
- Cycle case `[[1,2],[2,3],[3,1]]`: every in-degree is 1, `cur` is empty at the start, semesters 0, done 0 < 3, so -1.

**Code:**
```python
import itertools
import random

random.seed(24)

def min_semesters(n, relations):
    """Kahn's algorithm one level (= one semester) at a time."""
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        adj[a].append(b)
        indeg[b] += 1
    cur = [i for i in range(1, n + 1) if indeg[i] == 0]
    semesters = done = 0
    while cur:
        semesters += 1
        done += len(cur)
        nxt = []
        for u in cur:
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        cur = nxt
    return semesters if done == n else -1

def min_semesters_brute(n, relations):
    """Longest chain (in courses) by n rounds of relaxation; a cycle never settles, so any still-improving edge means -1."""
    d = [1] * (n + 1)
    for _ in range(n):
        for a, b in relations:
            if d[a] + 1 > d[b]:
                d[b] = d[a] + 1
    if any(d[a] + 1 > d[b] for a, b in relations):
        return -1
    return max(d[1:])

for n, rel, want in [(3, [[1, 3], [2, 3]], 2), (3, [[1, 2], [2, 3], [3, 1]], -1),
                     (4, [[1, 2], [2, 3], [3, 4]], 4), (2, [], 1)]:
    got = min_semesters(n, rel)
    assert got == want == min_semesters_brute(n, rel), (n, rel, got, want)
    print(n, rel, '->', got)

# ---- exhaustive: EVERY relation set on n <= 3 including self loops (2^9 sets for n=3), and every set without self loops on n = 4 (2^12)
cnt = 0
for n, loops in [(1, True), (2, True), (3, True), (4, False)]:
    pairs = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if loops or a != b]
    for mask in range(1 << len(pairs)):
        rel = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        assert min_semesters(n, rel) == min_semesters_brute(n, rel), (n, rel)
        cnt += 1
print('exhaustive check on', cnt, 'relation sets (all graphs on n<=3 with self loops, n=4 without): longest chain == Kahn levels')

# ---- seeded random larger cases, with duplicate relations allowed
for _ in range(500):
    n = random.randint(1, 9)
    rel = [[random.randint(1, n), random.randint(1, n)] for _ in range(random.randint(0, 12))]
    assert min_semesters(n, rel) == min_semesters_brute(n, rel), (n, rel)
print('500 seeded random cases agree')

# ---- the answer is a longest path: a DAG that is a single chain has n semesters, a star has 2
n = 5000
chain = [[i, i + 1] for i in range(1, n)]
assert min_semesters(n, chain) == n
assert min_semesters(n, [[1, i] for i in range(2, n + 1)]) == 2
assert min_semesters(n, []) == 1
assert min_semesters(n, chain + [[n, 1]]) == -1                    # one back edge makes a cycle
assert min_semesters(1, [[1, 1]]) == -1                            # self loop
print('n=5000 chain ->', min_semesters(n, chain), 'semesters; star ->', 2, '; no relations ->', 1)

# ---- a partial cycle: courses before the cycle finish, but done < n exposes the cycle
assert min_semesters(4, [[1, 2], [2, 3], [3, 2]]) == -1
print('cycle hidden behind a valid prefix is still caught by done < n')
```

**Output (my run):**
```
3 [[1, 3], [2, 3]] -> 2
3 [[1, 2], [2, 3], [3, 1]] -> -1
4 [[1, 2], [2, 3], [3, 4]] -> 4
2 [] -> 1
exhaustive check on 4626 relation sets (all graphs on n<=3 with self loops, n=4 without): longest chain == Kahn levels
500 seeded random cases agree
n=5000 chain -> 5000 semesters; star -> 2 ; no relations -> 1
cycle hidden behind a valid prefix is still caught by done < n
```

**Edge cases:**
- No relations: all courses in one semester (answer 1, not 0; n >= 1 so there is always at least one course).
- Self loop `[a, a]`: a course that needs itself; in-degree never reaches 0, so -1. The code asserts it.
- A cycle behind a valid prefix (`1 -> 2`, `2 <-> 3`): course 1 is taken, then nothing, so `done < n` and -1. Checking only "did we process something" is not enough.
- Single chain of 5000 courses: 5000 semesters. The loop is iterative, so there is no recursion issue.

**Follow-ups:**
- At most k courses per semester (Parallel courses II)? The level trick breaks: you must choose which k of the ready courses, and that choice is NP-hard in general; the usual interview version uses bitmask DP for n <= 15.
- Return the schedule, not the count? Keep each `cur` list: it is the semester's courses.
- Why not DFS longest path? Works with memoisation on a DAG plus a three-colour cycle check; Kahn does both in one pass.

**Common mistakes:**
- Counting semesters as the number of edges on the longest path (off by one: a single course is 1 semester).
- Returning the semester count without checking `done == n`.
- Using 0-based arrays for courses labelled 1..n and silently dropping course n.
- Processing one course at a time with a single queue and losing the level boundaries.

### Q25 ⭐⭐ 🟡 Dijkstra with lazy deletion: count pushes and stale pops. `n` nodes 0..n-1 (1 <= n <= 10^5), `edges` a list of directed [u, v, w] with 0 <= w <= 100 (up to 2*10^5, repeats allowed) and `src`. Run this exact algorithm: dist[src] = 0; the heap holds (distance, node) tuples and starts with (0, src); pop the smallest entry (d, u); if d > dist[u] the entry is stale, so count it and skip it; otherwise, for each edge (u, v, w) in input order, if d + w < dist[v] (strictly) set dist[v] = d + w and push (d + w, v). Return `[dist, pushes, stale_pops]` where dist has None for unreachable nodes, `pushes` counts every heappush including the first one, and `stale_pops` counts skipped entries. Python's heapq has no decrease-key, so duplicates are pushed instead (see Part 8 Q38); explain why the (distance, node) tuples never hit the unorderable-tie TypeError seen with payload objects (Part 8 Q29), why pushes is at most E + 1, and that stale_pops always equals pushes minus the number of reached nodes. Example: n=4, edges=[[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]], src=0 -> [[0, 3, 1, 4], 5, 1]; n=3, edges=[[0, 1, 1]], src=2 -> [[null, null, 0], 1, 0]; n=3, edges=[[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]], src=0 -> [[0, 5, 5], 3, 0].
**Asked at:** Dijkstra and lazy-deletion write-ups (a PracHub guide on Dijkstra stale heap entries and negative edges, Codeforces lazy-deletion tutorials, a python-dev heapq thread; search snippets only, not opened; docs.python.org was unreachable) | Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened)

**Pattern:** Single-source shortest paths with non-negative weights: Dijkstra on a `heapq` min-heap, using lazy deletion because `heapq` has no decrease-key.

**Say this first (1 line):** "Pop the closest entry; if its distance is worse than what I already know, it is stale, skip it. Otherwise relax its edges and push every improvement as a new entry. Duplicates are cheap, a decrease-key is not available."

**Brute force:** Bellman-Ford style: n rounds of relaxing every edge, O(n * E). Too slow at 10^5 by 2*10^5, and it does not give the push and stale counts. It is the checker for the distances.

**Optimal:**
- `dist[src] = 0`, heap `[(0, src)]`, `pushes = 1`, `stale = 0`.
- Pop `(d, u)`. If `d > dist[u]`: count it as stale, `continue`. Else for each edge `(u, v, w)` in input order: if `d + w < dist[v]` (strict), set it and push `(d + w, v)`.
- Why it is right: with weights >= 0 the first time a node is popped with `d == dist[u]` that distance is final (any other route goes through an entry that is at least as large). Stale entries are exactly the entries for a node that were beaten after being pushed.
- Why `(distance, node)` never raises `TypeError`: both items are ints, so tuples always compare. If two entries tie on distance the node number decides, and if both are equal the tuples are equal, which `heapq` does not mind. The `TypeError` in Part 8 Q29 came from tied priorities followed by an unorderable payload object (the code shows it). Part 8 Q38 is the same trick, push a new entry and ignore the old one.
- Why `pushes <= E + 1`: every push after the first happens while relaxing an edge. A node's edges are relaxed only when its non-stale entry is popped, and each node has exactly one non-stale pop, so each edge is relaxed at most once. So at most E pushes from edges plus the initial one.
- Why `stale == pushes - reached`: every entry pushed is popped eventually. A reached node has exactly one entry whose distance equals its final `dist` (equal distances are never pushed twice because the comparison is strict, and weights are >= 0 so the final value is never lowered after its pop). That entry is the one non-stale pop; every other entry is stale. The source's first entry counts as its non-stale one.

**Complexity:** Time O((V + E) log E) which is O((V + E) log V) because E <= V^2 only changes the log by a factor of 2: at most E + 1 pushes, each push and pop O(log heap size). Space O(V + E) (adjacency lists, plus a heap of at most E + 1 entries).

**Dry run:** `n=4, edges=[[0,1,4],[0,2,1],[2,1,2],[1,3,1]], src=0`.
- Pop (0,0). Relax 0->1: dist[1]=4, push (4,1). Relax 0->2: dist[2]=1, push (1,2). Pushes 3.
- Pop (1,2). Relax 2->1: 1+2=3 < 4, dist[1]=3, push (3,1). Pushes 4.
- Pop (3,1). Relax 1->3: dist[3]=4, push (4,3). Pushes 5.
- Pop (4,1): 4 > dist[1]=3, stale (count 1). Pop (4,3): fine.
- Result `[[0,3,1,4], 5, 1]`; reached = 4, and 5 - 4 = 1 = stale.

**Code:**
```python
import heapq
import itertools
import random

random.seed(25)
INF = float('inf')

def dijkstra_lazy(n, edges, src):
    """Lazy deletion: push duplicates, skip a popped entry whose distance is worse than the best known."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    heap = [(0, src)]
    pushes, stale = 1, 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                       # a better entry for u was already processed
            stale += 1
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:               # strict: equal distance does not push
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                pushes += 1
    return [[None if x == INF else x for x in dist], pushes, stale]

def bellman_ford_dist(n, edges, src):
    """Independent checker for the distances only (weights are >= 0 so no negative cycles)."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return [None if x == INF else x for x in d]

examples = [
    (4, [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]], 0, [[0, 3, 1, 4], 5, 1]),
    (3, [[0, 1, 1]], 2, [[None, None, 0], 1, 0]),
    (3, [[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]], 0, [[0, 5, 5], 3, 0]),
]
for n, e, s, want in examples:
    got = dijkstra_lazy(n, e, s)
    assert got == want, (got, want)
    print(n, e, 'src', s, '->', got)

# ---- why (distance, node) tuples never raise TypeError: ints always compare, and equal pairs are fully equal
heap = []
for item in [(3, 1), (3, 1), (3, 0), (2, 5)]:
    heapq.heappush(heap, item)
print('tied distances pop in node order:', [heapq.heappop(heap) for _ in range(4)])
class Payload:                               # what goes wrong if you push objects (Part 8 Q29)
    pass
h = [(1, Payload())]
try:
    heapq.heappush(h, (1, Payload()))
except TypeError as err:
    print('(dist, object) with tied dist ->', err)

# ---- exhaustive: every multigraph on 3 nodes with up to 3 edges, weights 0..2, every source
opts = [(u, v, w) for u in range(3) for v in range(3) for w in range(3)]     # 27 possible edges (self loops included)
cnt = 0
for k in range(4):
    for combo in itertools.product(opts, repeat=k):                           # ordered, so repeats and input orders are covered
        edges = [list(x) for x in combo]
        for src in range(3):
            dist, pushes, stale = dijkstra_lazy(3, edges, src)
            reached = sum(x is not None for x in dist)
            assert dist == bellman_ford_dist(3, edges, src)
            assert pushes <= len(edges) + 1
            assert stale == pushes - reached
            cnt += 1
print('exhaustive on', cnt, '(graph, source) cases: distances right, pushes <= E + 1, stale == pushes - reached')

# ---- seeded random bigger graphs
for _ in range(500):
    n = random.randint(1, 12)
    edges = [[random.randrange(n), random.randrange(n), random.randint(0, 6)] for _ in range(random.randint(0, 40))]
    src = random.randrange(n)
    dist, pushes, stale = dijkstra_lazy(n, edges, src)
    reached = sum(x is not None for x in dist)
    assert dist == bellman_ford_dist(n, edges, src) and pushes <= len(edges) + 1 and stale == pushes - reached
print('500 seeded random graphs agree')

# ---- the stale check saves work: count edge scans with and without it on a graph with many improvable nodes
def scans(n, edges, src, skip_stale):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [INF] * n
    dist[src] = 0
    heap, work = [(0, src)], 0
    while heap:
        d, u = heapq.heappop(heap)
        if skip_stale and d > dist[u]:
            continue
        for v, w in adj[u]:
            work += 1
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return work
# layer graph: node i reaches every later node; the first path found is the worst, later ones improve it
m = 60
edges = [[i, j, (j - i) ** 2] for i in range(m) for j in range(i + 1, m)]
edges.sort(key=lambda e: -e[2])
print('edge scans, 60-node graph: with stale check', scans(m, edges, 0, True), '| without', scans(m, edges, 0, False))

# ---- edge case and size: n=1; n = 10^5, E = 2*10^5 with repeated edges
assert dijkstra_lazy(1, [], 0) == [[0], 1, 0]
n, E = 10 ** 5, 2 * 10 ** 5
edges = [[random.randrange(n), random.randrange(n), random.randint(0, 100)] for _ in range(E)]
dist, pushes, stale = dijkstra_lazy(n, edges, 0)
reached = sum(x is not None for x in dist)
assert pushes <= E + 1 and stale == pushes - reached
print('n=10^5, E=2*10^5: reached', reached, 'pushes', pushes, '<= E + 1 =', E + 1, '| stale', stale, '== pushes - reached =', pushes - reached)
```

**Output (my run):**
```
4 [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]] src 0 -> [[0, 3, 1, 4], 5, 1]
3 [[0, 1, 1]] src 2 -> [[None, None, 0], 1, 0]
3 [[0, 1, 5], [0, 2, 5], [1, 2, 0], [2, 1, 0]] src 0 -> [[0, 5, 5], 3, 0]
tied distances pop in node order: [(2, 5), (3, 0), (3, 1), (3, 1)]
(dist, object) with tied dist -> '<' not supported between instances of 'Payload' and 'Payload'
exhaustive on 61320 (graph, source) cases: distances right, pushes <= E + 1, stale == pushes - reached
500 seeded random graphs agree
edge scans, 60-node graph: with stale check 1770 | without 34279
n=10^5, E=2*10^5: reached 79852 pushes 85195 <= E + 1 = 200001 | stale 5343 == pushes - reached = 5343
```

**Edge cases:**
- Unreachable nodes stay `None`; their entries never exist, so they add nothing to the counts (second example: `[[None, None, 0], 1, 0]`).
- Zero-weight edges and zero-weight cycles (third example): the strict `<` stops infinite pushing, the count stays 3.
- Parallel edges and self loops: a self loop never improves anything with weight >= 0.
- `n = 1`: `[[0], 1, 0]`.
- Negative weights break the "first pop is final" claim and the counting argument (Q28 and Q42 in this part).

**Follow-ups:**
- Why not skip the stale check? The result stays correct for non-negative weights, but each stale entry re-scans its edges. The code counts 34279 edge scans against 1770 on a 60-node graph.
- Can you avoid duplicates? An indexed heap with decrease-key (or a Fibonacci heap) does, at the cost of much more code; in Python the lazy version is nearly always faster.
- Early exit when only one target matters? Return when the target is popped non-stale.

**Common mistakes:**
- Pushing the node first, `(node, d)`, so the heap orders by node.
- Using `<=` in the relaxation: equal distances get pushed again and the push bound breaks (zero-weight cycles can loop forever).
- Marking nodes done on push instead of on pop.
- Counting `reached` as the number of finite distances but forgetting the source.

### Q26 ⭐⭐ 🟡 Path with minimum effort. `heights` is an m x n grid of integers (1 <= m, n <= 100, 0 <= value <= 10^6). Moving up, down, left or right between adjacent cells costs |difference of heights|, and the effort of a route is the largest single step cost on it. Return the minimum possible effort over all routes from the top-left to the bottom-right cell. Solve it with Dijkstra where the path 'length' is the maximum edge instead of the sum, and say why that still works; mention the binary-search-on-answer alternative. Example: heights=[[1, 2, 2], [3, 8, 2], [5, 3, 5]] -> 2; heights=[[1, 2, 3], [3, 8, 4], [5, 3, 5]] -> 1; heights=[[7]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Dijkstra and lazy-deletion write-ups (a PracHub guide on Dijkstra stale heap entries and negative edges, Codeforces lazy-deletion tutorials, a python-dev heapq thread; search snippets only, not opened; docs.python.org was unreachable)

**Pattern:** Minimax path (bottleneck shortest path) on a grid: Dijkstra with `max` in place of `+`. Binary search on the answer plus a DFS/BFS reachability test is the alternative.

**Say this first (1 line):** "It is Dijkstra, but a route's cost is its largest step so far. Extending a route can never make that smaller, and a cheaper prefix never gives a worse result, so the greedy pop order is still correct."

**Brute force:** Enumerate every simple path from corner to corner and take the one with the smallest maximum step. Exponential in the number of cells; fine only on 3 x 3 grids. It is one checker in the code.

**Optimal:**
- Heap entries `(effort, row, col)`, `best[r][c] = INF` except `best[0][0] = 0`.
- Pop the smallest. If `effort > best[r][c]` it is stale, skip. If it is the bottom-right cell, return it.
- For each of the 4 neighbours: `ne = max(effort, abs(h[nb] - h[cell]))`; if `ne < best[nb]`, update and push.
- Why `max` still works. Dijkstra needs two properties of the path cost:
  - Extending a path never lowers its cost: `max(e, w) >= e`.
  - The extension is monotone in the prefix: if `e1 <= e2` then `max(e1, w) <= max(e2, w)`.
  - With these, when a cell is popped with effort `e`, any other route reaches it through a cell not yet popped, whose effort is already `>= e`, so that route costs at least `e`. So the first pop of a cell is final. Sum satisfies both properties for non-negative steps, and so does max.
- Binary search alternative: for a threshold T, flood fill only through steps `<= T`; feasibility is monotone in T, so binary search T in `[0, max - min]`. Cost O(mn * log(10^6)), about 20 floods. The code runs both and they agree.
- The two answers are not the same as the sum version: on example 1 the sum-of-steps answer is 4 but the minimum effort is 2 (code prints it).

**Complexity:** Dijkstra: each cell pushes at most one entry per improvement, at most 4mn pushes, each O(log(mn)), so O(mn log(mn)) time, O(mn) space. Binary search: O(mn log(range)) time, O(mn) space; at 100 x 100 and range 10^6 that is about 20 * 10^4 cell visits. Both are fine at this size; the binary search has no heap.

**Dry run:** `[[1,2,2],[3,8,2],[5,3,5]]`.
- Start (0,0) effort 0. Push right (0,1): max(0,1) = 1; push down (1,0): max(0,2) = 2.
- Pop (0,1) effort 1: right (0,2) step 0, effort 1; down (1,1) step 6, effort 6.
- Pop (0,2) effort 1: down (1,2) step 0, effort 1. Pop (1,2) effort 1: down (2,2) step 3, effort 3.
- Pop (1,0) effort 2: down (2,0) step 2, effort 2. Pop (2,0) effort 2: right (2,1) step 2, effort 2. Pop (2,1) effort 2: right (2,2) step 2, effort max(2,2) = 2 < 3, update.
- Pop (2,2) with effort 2. Answer 2.

**Code:**
```python
import heapq
import itertools
import random

random.seed(26)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
INF = float('inf')

def min_effort(h):
    """Dijkstra where a path's cost is the MAX step so far instead of the sum."""
    m, n = len(h), len(h[0])
    best = [[INF] * n for _ in range(m)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, x, y = heapq.heappop(heap)
        if e > best[x][y]:                         # stale entry (lazy deletion)
            continue
        if (x, y) == (m - 1, n - 1):
            return e
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                ne = max(e, abs(h[a][b] - h[x][y]))    # the only change from ordinary Dijkstra
                if ne < best[a][b]:
                    best[a][b] = ne
                    heapq.heappush(heap, (ne, a, b))

def min_effort_bsearch(h):
    """Binary search on the answer T; feasibility = reachable using only steps <= T (iterative DFS). O(mn log(maxdiff))."""
    m, n = len(h), len(h[0])
    def ok(T):
        seen = {(0, 0)}
        st = [(0, 0)]
        while st:
            x, y = st.pop()
            if (x, y) == (m - 1, n - 1):
                return True
            for dx, dy in D4:
                a, b = x + dx, y + dy
                if 0 <= a < m and 0 <= b < n and (a, b) not in seen and abs(h[a][b] - h[x][y]) <= T:
                    seen.add((a, b))
                    st.append((a, b))
        return False
    lo, hi = 0, max(map(max, h)) - min(map(min, h))
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def min_effort_paths(h):
    """Brute force: enumerate every simple path (tiny grids only) and take the best max step."""
    m, n = len(h), len(h[0])
    best = [INF]
    def go(x, y, seen, cur):
        if (x, y) == (m - 1, n - 1):
            best[0] = min(best[0], cur)
            return
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and (a, b) not in seen:
                seen.add((a, b))
                go(a, b, seen, max(cur, abs(h[a][b] - h[x][y])))
                seen.discard((a, b))
    go(0, 0, {(0, 0)}, 0)
    return best[0]

def min_sum_wrong(h):
    """Ordinary Dijkstra (sum of step costs): answers a different question."""
    m, n = len(h), len(h[0])
    best = [[INF] * n for _ in range(m)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, x, y = heapq.heappop(heap)
        if e > best[x][y]:
            continue
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and e + abs(h[a][b] - h[x][y]) < best[a][b]:
                best[a][b] = e + abs(h[a][b] - h[x][y])
                heapq.heappush(heap, (best[a][b], a, b))
    return best[m - 1][n - 1]

for g, want in [([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2), ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1), ([[7]], 0)]:
    got = min_effort(g)
    assert got == want == min_effort_bsearch(g) == min_effort_paths(g), (g, got, want)
    print(g, '->', got)

# ---- sum-Dijkstra is a different problem: same grids, different answers
g = [[1, 2, 2], [3, 8, 2], [5, 3, 5]]
print('example 1: max-step answer', min_effort(g), '| sum-of-steps answer (different question)', min_sum_wrong(g))
g = [[0, 5, 5, 5], [1, 9, 9, 5], [2, 3, 4, 5]]
print('another grid: max-step', min_effort(g), '| sum of steps', min_sum_wrong(g))

# ---- exhaustive: every 2x3 grid with values 0..3 and every 3x3 grid with values 0..2
cnt = 0
for m, n, V in [(1, 1, 4), (1, 4, 3), (2, 2, 4), (2, 3, 4), (3, 3, 3)]:
    for vals in itertools.product(range(V), repeat=m * n):
        g = [list(vals[i * n:(i + 1) * n]) for i in range(m)]
        r = min_effort(g)
        assert r == min_effort_bsearch(g) == min_effort_paths(g), g
        cnt += 1
print('exhaustive on', cnt, 'small grids: Dijkstra(max) == binary search on answer == all simple paths')

# ---- seeded random larger grids (no path enumeration, two independent methods)
for _ in range(300):
    m, n = random.randint(1, 7), random.randint(1, 7)
    g = [[random.randint(0, 20) for _ in range(n)] for _ in range(m)]
    assert min_effort(g) == min_effort_bsearch(g), g
print('300 seeded random grids up to 7x7 agree')

# ---- size: 100 x 100 with values up to 10^6, and a snake that forces a long route
m = n = 100
g = [[random.randint(0, 10 ** 6) for _ in range(n)] for _ in range(m)]
assert min_effort(g) == min_effort_bsearch(g)
print('100x100 random, values <= 10^6 ->', min_effort(g))
m = 99                                    # odd number of rows would end on a wall row, so use 99 rows
snake = [[0 if (i % 2 == 0 or (i % 4 == 1 and j == n - 1) or (i % 4 == 3 and j == 0)) else 10 ** 6 for j in range(n)] for i in range(m)]
assert min_effort(snake) == min_effort_bsearch(snake) == 0
print('99x100 snake corridor of equal heights -> 0 (a route of about 5000 cells, no recursion used)')
```

**Output (my run):**
```
[[1, 2, 2], [3, 8, 2], [5, 3, 5]] -> 2
[[1, 2, 3], [3, 8, 4], [5, 3, 5]] -> 1
[[7]] -> 0
example 1: max-step answer 2 | sum-of-steps answer (different question) 4
another grid: max-step 1 | sum of steps 5
exhaustive on 24120 small grids: Dijkstra(max) == binary search on answer == all simple paths
300 seeded random grids up to 7x7 agree
100x100 random, values <= 10^6 -> 335144
99x100 snake corridor of equal heights -> 0 (a route of about 5000 cells, no recursion used)
```

**Edge cases:**
- 1 x 1 grid: start is the goal, effort 0.
- Equal heights everywhere: 0.
- Going away from the goal is allowed and sometimes necessary (the snake corridor winds through about 5000 cells).
- Huge heights (10^6): ints, no overflow in Python.
- Return when the target is popped, not when it is first pushed (a later, better push can still arrive).

**Follow-ups:**
- Why not BFS or DFS with a visited set directly? The best route to a cell depends on its effort, not on who arrived first, so a plain visited set can lock in a worse effort.
- Union-find version? Sort all adjacent-cell edges by step cost and add them until top-left and bottom-right join: the last edge added is the answer (Kruskal-style bottleneck), O(mn log(mn)).
- Why is the maximum spanning-path idea related to MST? The minimax path between two nodes lies on the minimum spanning tree; that is the Q29 connection.

**Common mistakes:**
- Summing the steps (Dijkstra by habit).
- Taking `abs` of the wrong pair, or using the neighbour's height only.
- Returning at the first push of the target.
- Marking cells visited when pushed.

### Q27 ⭐⭐ 🟡 0-1 BFS: minimum obstacles to remove. `grid` is an m x n grid (1 <= m*n <= 10^5) of 0 (empty) and 1 (obstacle) with grid[0][0] = grid[m-1][n-1] = 0. You move up, down, left or right, and stepping onto an obstacle cell costs 1 (you remove it) while stepping onto an empty cell costs 0. Return the minimum number of obstacles removed to get from the top-left to the bottom-right cell. Solve it in O(m*n) with a deque (push 0-cost neighbours to the front, 1-cost to the back) and explain why an ordinary BFS that marks a cell visited the first time it is enqueued gives wrong answers here, and why this beats Dijkstra's log factor. Example: grid=[[0, 1, 1], [1, 1, 0], [1, 1, 0]] -> 2; grid=[[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]] -> 0; grid=[[0]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Shortest path with edge weights only 0 or 1: 0-1 BFS on a deque. Stepping into an obstacle cell costs 1, into an empty cell costs 0.

**Say this first (1 line):** "It is Dijkstra where the heap only ever holds two distances, d and d+1, so a deque replaces it: free moves go to the front, paid moves to the back."

**Brute force:** Bellman-Ford over the grid: sweep every cell and neighbour, relax, and repeat until nothing changes. Up to O((mn)^2) in the worst case. Plain Dijkstra with `heapq` is the middle option, O(mn log(mn)). Both are checkers in the code.

**Optimal:**
- `dist[0][0] = 0`, deque `[(0,0)]`. Pop from the left. For each neighbour with cost `w = grid[nb]` (cost of stepping INTO it): if `dist[cell] + w < dist[nb]`, update; `w == 0` -> `appendleft`, `w == 1` -> `append`.
- Invariant: the deque is always sorted by distance and holds at most two different values, d and d+1. Popping from the left takes the smallest. A 0-move produces distance d, which belongs in front of the d+1 entries; a 1-move produces d+1, which belongs at the back. The code asserts the invariant before every pop on all small grids.
- Why a cell can be queued more than once: it may first be reached with d+1 and later with d. The strict `<` allows that improvement. Since only two values exist at a time, a cell improves at most about twice, so total work stays O(mn). A stale copy is harmless: when popped, its relaxations all fail.
- Why ordinary BFS fails: BFS finalises a cell when it is first enqueued and assumes every edge costs one step. With costs 0 and 1 the first route found (fewest steps) is not the cheapest route (fewest obstacles). The code counts the plain version wrong on 12914 of the 17557 exhaustively tested grids; example 1 gives 3 instead of 2.
- Versus Dijkstra: same relaxations, but a heap push/pop costs O(log) and the deque costs O(1), because the "priority" only takes two consecutive values.

**Complexity:** Time O(mn): each cell is queued a constant number of times (at most twice per improvement level) and scans 4 neighbours. Space O(mn) for `dist` and the deque. The log factor of Dijkstra disappears.

**Dry run:** `[[0,1,1],[1,1,0],[1,1,0]]`.
- Start (0,0), dist 0. Right (0,1): cost 1, dist 1, append. Down (1,0): cost 1, dist 1, append. Deque: (0,1), (1,0).
- Pop (0,1) (dist 1): right (0,2) cost 1 -> 2, append; down (1,1) cost 1 -> 2, append.
- Pop (1,0) (dist 1): down (2,0) -> 2, append; right (1,1) 2 is not less than 2, no change.
- Pop (0,2) dist 2: down (1,2) cost 0 -> 2, appendleft. Pop (1,2): down (2,2) cost 0 -> 2, appendleft. Pop (2,2).
- dist[2][2] = 2.

**Code:**
```python
import heapq
import itertools
import random
from collections import deque

random.seed(27)
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
INF = float('inf')

def min_obstacles(grid, check_invariant=False):
    """0-1 BFS: relax like Dijkstra, but a 0-cost move goes to the FRONT of the deque and a 1-cost move to the BACK."""
    m, n = len(grid), len(grid[0])
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    dq = deque([(0, 0)])
    while dq:
        if check_invariant:                                  # deque distances are non-decreasing and span at most two values
            ds = [dist[x][y] for x, y in dq]
            assert ds == sorted(ds) and ds[-1] - ds[0] <= 1, ds
        x, y = dq.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n:
                w = grid[a][b]                               # cost of stepping INTO (a, b)
                if dist[x][y] + w < dist[a][b]:              # strict: a cell can be re-queued when a cheaper route appears
                    dist[a][b] = dist[x][y] + w
                    if w:
                        dq.append((a, b))
                    else:
                        dq.appendleft((a, b))
    return dist[m - 1][n - 1]

def dijkstra_obstacles(grid):
    m, n = len(grid), len(grid[0])
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    h = [(0, 0, 0)]
    while h:
        d, x, y = heapq.heappop(h)
        if d > dist[x][y]:
            continue
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and d + grid[a][b] < dist[a][b]:
                dist[a][b] = d + grid[a][b]
                heapq.heappush(h, (dist[a][b], a, b))
    return dist[m - 1][n - 1]

def fixpoint_brute(grid):
    """Independent brute force: keep relaxing every cell pair until nothing changes (Bellman-Ford over the grid)."""
    m, n = len(grid), len(grid[0])
    d = [[INF] * n for _ in range(m)]
    d[0][0] = 0
    changed = True
    while changed:
        changed = False
        for x in range(m):
            for y in range(n):
                for dx, dy in D4:
                    a, b = x + dx, y + dy
                    if 0 <= a < m and 0 <= b < n and d[x][y] + grid[a][b] < d[a][b]:
                        d[a][b] = d[x][y] + grid[a][b]
                        changed = True
    return d[m - 1][n - 1]

def plain_bfs_wrong(grid):
    """The tempting bug: ordinary BFS, a cell is finalised the first time it is enqueued, obstacle cost added on the way."""
    m, n = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        for dx, dy in D4:
            a, b = x + dx, y + dy
            if 0 <= a < m and 0 <= b < n and (a, b) not in dist:
                dist[(a, b)] = dist[(x, y)] + grid[a][b]
                q.append((a, b))
    return dist[(m - 1, n - 1)]

for g, want in [([[0, 1, 1], [1, 1, 0], [1, 1, 0]], 2), ([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0), ([[0]], 0)]:
    got = min_obstacles(g, check_invariant=True)
    assert got == want == dijkstra_obstacles(g) == fixpoint_brute(g), (g, got, want)
    print(g, '->', got, '| plain BFS says', plain_bfs_wrong(g))

# ---- exhaustive over every grid with free corners: 2x3, 3x3, 3x4, 4x4
total = bad_bfs = 0
for m, n in [(1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]:
    inner = [(i, j) for i in range(m) for j in range(n) if (i, j) not in ((0, 0), (m - 1, n - 1))]
    for bits in itertools.product((0, 1), repeat=len(inner)):
        g = [[0] * n for _ in range(m)]
        for (i, j), b in zip(inner, bits):
            g[i][j] = b
        r = min_obstacles(g, check_invariant=True)
        assert r == dijkstra_obstacles(g) == fixpoint_brute(g), g
        total += 1
        bad_bfs += plain_bfs_wrong(g) != r
print('exhaustive on', total, 'grids: 0-1 BFS == Dijkstra == fixpoint, deque stays sorted with span <= 1')
print('plain visited-on-enqueue BFS is wrong on', bad_bfs, 'of those grids')

# ---- seeded random cross-check on bigger grids
for _ in range(300):
    m, n = random.randint(1, 8), random.randint(1, 8)
    g = [[int(random.random() < 0.45) for _ in range(n)] for _ in range(m)]
    g[0][0] = 0
    g[m - 1][n - 1] = 0
    assert min_obstacles(g) == dijkstra_obstacles(g) == fixpoint_brute(g), g
print('300 seeded random grids up to 8x8 agree')

# ---- sizes: m*n = 10^5 (a single row, a single column, 316x316), iterative so no recursion limit
row = [[0] + [1] * (10 ** 5 - 2) + [0]]
assert min_obstacles(row) == 10 ** 5 - 2
col = [[v] for v in row[0]]
assert min_obstacles(col) == 10 ** 5 - 2
big = [[int(random.random() < 0.4) for _ in range(316)] for _ in range(316)]
big[0][0] = big[315][315] = 0
assert min_obstacles(big) == dijkstra_obstacles(big)
print('10^5-cell row and column ->', min_obstacles(row), '; 316x316 random ->', min_obstacles(big))
```

**Output (my run):**
```
[[0, 1, 1], [1, 1, 0], [1, 1, 0]] -> 2 | plain BFS says 3
[[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]] -> 0 | plain BFS says 1
[[0]] -> 0 | plain BFS says 0
exhaustive on 17557 grids: 0-1 BFS == Dijkstra == fixpoint, deque stays sorted with span <= 1
plain visited-on-enqueue BFS is wrong on 12914 of those grids
300 seeded random grids up to 8x8 agree
10^5-cell row and column -> 99998 ; 316x316 random -> 4
```

**Edge cases:**
- 1 x 1 grid: 0.
- Start and end are guaranteed free, so the start cell's own value is never paid.
- A grid that is one long row or column of obstacles: answer is the number of obstacles in the middle; sizes up to 10^5 cells are fine because the loop is iterative.
- A free corridor that is longer than a path through one obstacle: still the corridor wins (cost 0). Example 2 shows it.

**Follow-ups:**
- Cost on edges rather than cells (a weight 0 or 1 per edge)? Same algorithm; the cost is read from the edge.
- Weights 0..K? Dial's algorithm: K + 1 buckets instead of a deque.
- Why not a visited set instead of the strict distance check? With a visited-on-pop set it also works (skip a cell that was already finalised), but then you must set it on pop, never on push.

**Common mistakes:**
- Marking a cell visited when it is enqueued (the BFS bug above).
- Pushing the 0-cost neighbour to the back, which breaks the sorted invariant.
- Adding the cost of the cell you leave instead of the one you enter (the start would be charged).
- Using `<=` in the relaxation and re-queueing forever on zero-cost cycles.

### Q28 ⭐⭐ 🟡 Bellman-Ford with negative edges and negative cycles. `n` nodes 0..n-1 (1 <= n <= 500), `edges` a list of directed [u, v, w] with -100 <= w <= 100 (up to 5000) and `src`. If a negative-weight cycle is reachable from `src`, return None. Otherwise return the list of shortest distances from `src` (None for unreachable nodes). Use n-1 rounds of relaxing every edge, then one extra round to detect a cycle; explain why n-1 rounds suffice, why the check must only consider cycles reachable from src (not just any negative edge), and the O(V*E) cost. Example: n=4, edges=[[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]], src=0 -> [0, 2, 5, 4]; n=3, edges=[[0, 1, 1], [1, 2, -3], [2, 1, 1]], src=0 -> null; n=3, edges=[[1, 2, -1], [2, 1, -1]], src=0 -> [0, null, null].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Single-source shortest paths with negative edge weights: Bellman-Ford (relax every edge V-1 times), plus one more round as a negative-cycle detector.

**Say this first (1 line):** "Dijkstra is out because of the negative edges. Bellman-Ford relaxes every edge n-1 times, since a shortest path has at most n-1 edges; if an edge still improves in round n, a negative cycle reachable from the source exists."

**Brute force:** Floyd-Warshall on all pairs, O(n^3) (125 million steps at n = 500, too slow in Python), then declare a cycle if some node k reachable from `src` has `f[k][k] < 0`. It is the independent checker in the code.

**Optimal:**
- `d = [INF]*n`, `d[src] = 0`.
- Repeat n-1 times: for every edge `(u, v, w)`, if `d[u] != INF and d[u] + w < d[v]`, set `d[v] = d[u] + w`. Stop early if a whole round changes nothing.
- One more round: if any edge with `d[u] != INF` still improves, return `None`.
- Why n-1 rounds suffice: with no negative cycle, some shortest path to each node is simple, so it has at most n-1 edges. By induction, after round k every node whose shortest path has at most k edges holds its correct distance, because round k relaxes the k-th edge of that path after the (k-1)-th was fixed. The worst case is edges listed against the path direction: each round then advances one edge, and the code shows n-2 rounds are not enough on a path of 8 nodes (the check round fires although there is no cycle).
- Why the detector only counts reachable cycles: a negative cycle that `src` cannot reach never gets finite distances, and the answer for the reachable part is still well defined. The guard `d[u] != INF` keeps unreached nodes out of the arithmetic. If you represent INF by a big integer and skip the guard, `INF - 1 < INF` is true for the unreachable cycle in example 3, and the code returns `None` wrongly (the code prints it, and counts 110 of 1000 random graphs wrong).
- Why one extra round finds a reachable negative cycle: going around such a cycle lowers some distance on every lap, so after any number of rounds at least one edge of the cycle can still relax. Conversely, if no negative cycle is reachable, all distances are final after n-1 rounds and nothing improves.
- With `float('inf')`, `inf + w < inf` is already false, so the guard is implicit; with an integer sentinel it is mandatory. The explicit test is the safe habit.

**Complexity:** Time O(V * E) worst case (500 * 5000 = 2.5 million relaxations at the limits, fine); early exit often makes it much faster. Space O(V) for `d` plus the edge list. Dijkstra's O((V + E) log V) needs non-negative weights.

**Dry run:** `n=3, edges=[[0,1,1],[1,2,-3],[2,1,1]], src=0`.
- Start `d = [0, INF, INF]`.
- Round 1: 0->1 gives d1 = 1. 1->2: 1 - 3 = -2, d2 = -2. 2->1: -2 + 1 = -1 < 1, d1 = -1.
- Round 2 (n-1 = 2): 1->2: -1 - 3 = -4, d2 = -4. 2->1: -4 + 1 = -3, d1 = -3.
- Check round: 1->2 would give -6 < -4. An edge still improves, so return `None`.
- Example 1 for contrast: `[0, 2, 5, 4]` settles in 2 rounds with no improvement in the check round (the path 0 -> 2 -> 1 uses the negative edge 2 -> 1 and beats the direct edge).

**Code:**
```python
import itertools
import random

random.seed(28)
INF = float('inf')

def bellman_ford(n, edges, src, rounds=None, guard=True):
    """n-1 rounds of relaxing every edge, then one more round: any improvement means a reachable negative cycle."""
    d = [INF] * n
    d[src] = 0
    for _ in range(n - 1 if rounds is None else rounds):
        changed = False
        for u, v, w in edges:
            if d[u] != INF and d[u] + w < d[v]:          # never relax out of an unreached node
                d[v] = d[u] + w
                changed = True
        if not changed:                                  # early exit: distances are final
            break
    for u, v, w in edges:
        if d[u] != INF and d[u] + w < d[v]:
            return None
    return [None if x == INF else x for x in d]

def bellman_ford_unguarded(n, edges, src, big=10 ** 9):
    """Bug: unreached nodes get a large finite number and are relaxed like real ones."""
    d = [big] * n
    d[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in edges:
        if d[u] + w < d[v]:
            return None
    return [None if x >= big // 2 else x for x in d]

def floyd_brute(n, edges, src):
    """Independent brute force: all-pairs Floyd-Warshall; a negative cycle shows up as f[k][k] < 0 for a k reachable from src."""
    f = [[INF] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 0
    for u, v, w in edges:
        f[u][v] = min(f[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if f[i][k] + f[k][j] < f[i][j]:
                    f[i][j] = f[i][k] + f[k][j]
    if any(f[src][k] < INF and f[k][k] < 0 for k in range(n)):
        return None
    return [None if x == INF else x for x in f[src]]

for n, e, s, want in [(4, [[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]], 0, [0, 2, 5, 4]),
                      (3, [[0, 1, 1], [1, 2, -3], [2, 1, 1]], 0, None),
                      (3, [[1, 2, -1], [2, 1, -1]], 0, [0, None, None])]:
    got = bellman_ford(n, e, s)
    assert got == want == floyd_brute(n, e, s), (got, want)
    print(n, e, 'src', s, '->', got)

# ---- the two classic bugs on example 3: a negative cycle that is NOT reachable from src
e3 = [[1, 2, -1], [2, 1, -1]]
print('unguarded INF arithmetic on example 3 ->', bellman_ford_unguarded(3, e3, 0), '(false alarm: that cycle is unreachable)')

# ---- why n-1 rounds suffice: a shortest path without a negative cycle has at most n-1 edges, and round k fixes the k-th edge of every
# shortest path. Worst case = path edges listed in REVERSE order, so each round advances only one edge.
n = 8
path = [[i, i + 1, 1] for i in range(n - 1)][::-1]
full = bellman_ford(n, path, 0)
short = bellman_ford(n, path, 0, rounds=n - 2)            # one round too few: distances are not final, so the check round fires
print('reverse-ordered path, n=8: n-1 rounds ->', full, '| n-2 rounds ->', short)
assert full == list(range(n)) and short is None

# ---- exhaustive: every ordered list of up to 3 edges on 3 nodes with weights -2..2 (self loops included), every source
opts = [(u, v, w) for u in range(3) for v in range(3) for w in range(-2, 3)]    # 45 edge options
cnt = neg = 0
for k in range(4):
    for combo in itertools.product(opts, repeat=k):
        edges = [list(x) for x in combo]
        for src in range(3):
            a = bellman_ford(3, edges, src)
            assert a == floyd_brute(3, edges, src), (edges, src)
            neg += a is None
            cnt += 1
print('exhaustive on', cnt, '(graph, source) cases, of which', neg, 'have a reachable negative cycle: Bellman-Ford == Floyd-Warshall')

# ---- seeded random graphs up to n = 7 with a mix of negative edges
for _ in range(1000):
    n = random.randint(1, 7)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-5, 8)] for _ in range(random.randint(0, 14))]
    src = random.randrange(n)
    assert bellman_ford(n, edges, src) == floyd_brute(n, edges, src), (n, edges, src)
print('1000 seeded random graphs agree')

# ---- the unguarded bug versus the correct code over the same random graphs
wrong = 0
for _ in range(1000):
    n = random.randint(1, 7)
    edges = [[random.randrange(n), random.randrange(n), random.randint(-5, 8)] for _ in range(random.randint(0, 14))]
    src = random.randrange(n)
    wrong += bellman_ford_unguarded(n, edges, src) != floyd_brute(n, edges, src)
print('unguarded variant disagrees with the checker on', wrong, 'of 1000 random graphs')

# ---- max size: n = 500, E = 5000, worst-case O(V*E) = about 2.5 * 10^6 relaxations
n, E = 500, 5000
pot = [random.randint(0, 50) for _ in range(n)]
edges = []
for _ in range(E):
    u, v = random.randrange(n), random.randrange(n)
    edges.append([u, v, random.randint(0, 50) + pot[u] - pot[v]])              # reduced-cost form: negative edges, but no negative cycle
assert min(w for _, _, w in edges) < 0
r = bellman_ford(n, edges, 0)
assert r is not None and r[0] == 0
edges += [[0, 1, -100], [1, 0, -100]]                                            # a reachable negative 2-cycle
assert bellman_ford(n, edges, 0) is None
print('n=500, E=5000 with negative edges but no negative cycle: reached', sum(x is not None for x in r),
      'nodes; adding a 2-cycle of weight -200 -> None')
assert bellman_ford(1, [], 0) == [0]
assert bellman_ford(1, [[0, 0, -1]], 0) is None and bellman_ford(1, [[0, 0, 1]], 0) == [0]
print('edge asserts passed (n=1, negative and positive self loops)')
```

**Output (my run):**
```
4 [[0, 1, 4], [0, 2, 5], [2, 1, -3], [1, 3, 2]] src 0 -> [0, 2, 5, 4]
3 [[0, 1, 1], [1, 2, -3], [2, 1, 1]] src 0 -> None
3 [[1, 2, -1], [2, 1, -1]] src 0 -> [0, None, None]
unguarded INF arithmetic on example 3 -> None (false alarm: that cycle is unreachable)
reverse-ordered path, n=8: n-1 rounds -> [0, 1, 2, 3, 4, 5, 6, 7] | n-2 rounds -> None
exhaustive on 279588 (graph, source) cases, of which 69036 have a reachable negative cycle: Bellman-Ford == Floyd-Warshall
1000 seeded random graphs agree
unguarded variant disagrees with the checker on 110 of 1000 random graphs
n=500, E=5000 with negative edges but no negative cycle: reached 500 nodes; adding a 2-cycle of weight -200 -> None
edge asserts passed (n=1, negative and positive self loops)
```

**Edge cases:**
- Negative cycle not reachable from `src` (example 3): distances for the reachable part (just `src`) are returned, unreachable nodes `None`, no error.
- Negative self loop (`[0,0,-1]`): a one-edge negative cycle, `None`; a positive self loop is ignored.
- A negative edge that is not on a cycle is fine (example 1).
- A zero-weight cycle does not improve anything: no detection, correct distances.
- `n = 1`, no edges: `[0]`.
- Undirected graph with a negative edge is itself a negative cycle (go back and forth); treat each undirected edge as two directed ones and Bellman-Ford returns `None`.

**Follow-ups:**
- Which nodes are on the cycle, or which distances are -infinity? Run one more n rounds, mark every node that still improves, and propagate the mark along edges (everything reachable from a marked node is -infinity).
- Cheapest flights within K stops: Bellman-Ford with exactly K+1 rounds, but each round must read the previous round's array (a copy), or the in-place version lets a path use more edges than allowed (Q34 in this part).
- Faster in practice? SPFA (queue-based) often wins, but its worst case is still O(V * E) and it can be attacked.

**Common mistakes:**
- Running too few rounds (n-2), or checking for a cycle before the n-1 rounds are done.
- Dropping the `d[u] != INF` guard with an integer sentinel (false negative-cycle alarms).
- Reporting a cycle if any edge is negative.
- Forgetting the early exit, or using it before the detection round.

### Q29 ⭐⭐ 🟡 Minimum spanning tree weight with Kruskal. `n` nodes 0..n-1 (1 <= n <= 10^4) and `edges` a list of undirected [u, v, w] with 1 <= w <= 10^5 (up to 10^5 edges; repeats and self loops possible). Return the total weight of a minimum spanning tree, or -1 if the graph is disconnected. Several different trees can tie, but their total weight is the same, and the checker accepts only that number. Sort edges by weight and join components with union-find; state the complexity (O(E log E)) and name Prim's algorithm as the heap-based alternative (cut property, Borůvka and second-best trees belong to Part 14). Example: n=4, edges=[[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]] -> 7; n=3, edges=[[0, 1, 2]] -> -1; n=1, edges=[] -> 0; n=3, edges=[[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]] -> 4.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Minimum spanning tree by Kruskal's greedy algorithm, with union-find to test "does this edge close a cycle?".

**Say this first (1 line):** "Sort edges by weight, take an edge if it joins two different components, skip it otherwise. If I end with fewer than n-1 edges, the graph is disconnected, so -1."

**Brute force:** Try every subset of n-1 edges, keep the ones that are acyclic (n-1 edges with no cycle on n nodes is a spanning tree), take the cheapest. That is C(E, n-1) subsets, only usable on tiny graphs. It is a checker in the code.

**Optimal:**
- Sort edges by weight (`sorted(..., key=...)`; ties in any order).
- Union-find with an iterative `find` (path halving) and union by size. For each edge: if `find(u) == find(v)` skip it (a cycle, and this also skips self loops and repeated edges); else union, add `w`, count it.
- Stop early at n-1 edges. At the end, `used == n-1` means connected: return the total, else -1. For n = 1 there is nothing to add: 0.
- Why greedy works (cut property, informally): the cheapest edge crossing any cut between two parts of the nodes belongs to some MST. When Kruskal looks at an edge that joins two components, it is the cheapest edge leaving one of them that has not been considered, so it is safe to take. Skipped edges would close a cycle in which they are the heaviest edge seen so far, so they are safe to drop. The full proof, Borůvka and second-best trees belong to Part 14.
- Ties: several different trees can have the same minimum weight, and which one Kruskal returns depends on the order of equal-weight edges. The code counts 3 minimum trees in the all-equal triangle. The checker only accepts the total, which is unique.
- Prim's algorithm is the heap-based alternative: start from one node, repeatedly pop the cheapest edge leaving the current tree from a heap (lazy deletion of edges to already-visited nodes). Total cost is O(E log V). It wins on dense graphs and when the graph is given as adjacency lists; Kruskal wins when edges are already a list or easy to sort. The code runs both and they agree on every case.

**Complexity:** Sorting: O(E log E). Union-find: O(E * alpha(V)) with path compression and union by size (alpha is the inverse Ackermann function, at most 4 or so here). Total O(E log E), which equals O(E log V) since E <= V^2. Space O(V + E): parent and size arrays, plus the sorted copy of the edges.

**Dry run:** `n=4, edges=[[0,1,1],[1,2,2],[0,2,3],[2,3,4],[1,3,5]]`.
- Sorted by weight: (0,1,1), (1,2,2), (0,2,3), (2,3,4), (1,3,5).
- (0,1,1): different components, take it, total 1.
- (1,2,2): take, total 3. Now {0,1,2}.
- (0,2,3): both in {0,1,2}, skip (cycle).
- (2,3,4): 3 is alone, take, total 7, used = 3 = n-1: stop.
- Answer 7.

**Code:**
```python
import heapq
import itertools
import random

random.seed(29)

def kruskal(n, edges):
    """Sort by weight, add an edge iff it joins two different components. Iterative find, path halving, union by size."""
    parent = list(range(n))
    size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    total = used = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a == b:                                  # self loops and cycle-forming edges are skipped here
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        total += w
        used += 1
        if used == n - 1:
            break
    return total if used == n - 1 else -1

def prim(n, edges):
    """Heap-based alternative: grow one tree from node 0 by the cheapest edge leaving it (lazy heap)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            adj[u].append((w, v))
            adj[v].append((w, u))
    seen = [False] * n
    seen[0] = True
    heap = list(adj[0])
    heapq.heapify(heap)
    total, cnt = 0, 1
    while heap and cnt < n:
        w, v = heapq.heappop(heap)
        if seen[v]:
            continue
        seen[v] = True
        total += w
        cnt += 1
        for item in adj[v]:
            if not seen[item[1]]:
                heapq.heappush(heap, item)
    return total if cnt == n else -1

def mst_brute(n, edges):
    """Try every (n-1)-edge subset: it is a spanning tree iff it has no cycle. Take the cheapest."""
    if n == 1:
        return 0
    best = None
    for sub in itertools.combinations(edges, n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x:
                x = p[x]
            return x
        ok = True
        for u, v, w in sub:
            a, b = find(u), find(v)
            if a == b:
                ok = False
                break
            p[a] = b
        if ok:
            t = sum(e[2] for e in sub)
            best = t if best is None or t < best else best
    return -1 if best is None else best

def count_min_trees(n, edges):
    """How many distinct (n-1)-edge spanning trees have the optimal weight? (tiny graphs; shows that the tree is not unique)"""
    best, cnt = None, 0
    for sub in itertools.combinations(range(len(edges)), n - 1):
        p = list(range(n))
        def find(x):
            while p[x] != x:
                x = p[x]
            return x
        ok = True
        for i in sub:
            u, v, _ = edges[i]
            a, b = find(u), find(v)
            if a == b:
                ok = False
                break
            p[a] = b
        if ok:
            t = sum(edges[i][2] for i in sub)
            if best is None or t < best:
                best, cnt = t, 1
            elif t == best:
                cnt += 1
    return best, cnt

for n, e, want in [(4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]], 7), (3, [[0, 1, 2]], -1), (1, [], 0),
                   (3, [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]], 4)]:
    got = kruskal(n, e)
    assert got == want == prim(n, e) == mst_brute(n, e), (n, e, got, want)
    print(n, e, '->', got)

# ---- ties: several different trees, one weight
n, e = 3, [[0, 1, 2], [1, 2, 2], [0, 2, 2]]
print('triangle with all weights 2: (weight, number of minimum trees) =', count_min_trees(n, e), '-> only the weight is unique')
n, e = 3, [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]]
print('example 4: (weight, number of minimum trees) =', count_min_trees(n, e), '; the weight-1 self loop is never usable')

# ---- exhaustive: all multisets of up to 4 edges on 3 nodes (weights 1..3, self loops included), and up to 4 edges on 4 nodes (weights 1..2)
cnt = 0
for n, W, K in [(3, 3, 4), (4, 2, 4)]:
    opts = [(u, v, w) for u in range(n) for v in range(n) for w in range(1, W + 1)]
    for k in range(K + 1):
        for combo in itertools.combinations_with_replacement(opts, k):
            edges = [list(x) for x in combo]
            r = kruskal(n, edges)
            assert r == prim(n, edges) == mst_brute(n, edges), (n, edges)
            cnt += 1
print('exhaustive on', cnt, 'multigraphs: Kruskal == Prim == best spanning subset')

for _ in range(500):
    n = random.randint(1, 8)
    edges = [[random.randrange(n), random.randrange(n), random.randint(1, 9)] for _ in range(random.randint(0, 12))]
    assert kruskal(n, edges) == prim(n, edges), (n, edges)
print('500 seeded random graphs: Kruskal == Prim (n up to 8)')

# ---- max size: n = 10^4, E = 10^5 with repeats and self loops; connected by a spine so the answer is not -1
n = 10 ** 4
edges = [[i, i + 1, random.randint(1, 10 ** 5)] for i in range(n - 1)]
edges += [[random.randrange(n), random.randrange(n), random.randint(1, 10 ** 5)] for _ in range(10 ** 5 - len(edges))]
k, p = kruskal(n, edges), prim(n, edges)
assert k == p and k != -1
print('n=10^4, E=10^5: Kruskal', k, '== Prim', p)
assert kruskal(n, [e for e in edges if e[0] != 5000 and e[1] != 5000]) == -1    # isolating one node disconnects the graph
print('removing every edge at node 5000 -> -1 (disconnected)')
assert kruskal(1, [[0, 0, 5]]) == 0
print('edge asserts passed')
```

**Output (my run):**
```
4 [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]] -> 7
3 [[0, 1, 2]] -> -1
1 [] -> 0
3 [[0, 0, 1], [0, 1, 2], [1, 2, 2], [0, 2, 2]] -> 4
triangle with all weights 2: (weight, number of minimum trees) = (4, 3) -> only the weight is unique
example 4: (weight, number of minimum trees) = (4, 3) ; the weight-1 self loop is never usable
exhaustive on 90370 multigraphs: Kruskal == Prim == best spanning subset
500 seeded random graphs: Kruskal == Prim (n up to 8)
n=10^4, E=10^5: Kruskal 58934380 == Prim 58934380
removing every edge at node 5000 -> -1 (disconnected)
edge asserts passed
```

**Edge cases:**
- Disconnected graph: fewer than n-1 usable edges, return -1 (example 2). Do not return a spanning forest weight.
- `n = 1` and no edges: 0.
- Self loops: `find(u) == find(u)`, always skipped (the weight-1 self loop in example 4 is never counted).
- Repeated edges between the same pair: the cheaper one is processed first; the second then closes a cycle and is skipped.
- Many equal weights: any order gives the same total (checked exhaustively against the brute force).

**Follow-ups:**
- Maximum spanning tree? Sort descending, or negate the weights.
- Is the MST path also the minimax (bottleneck) path between two nodes? Yes. That is the idea behind the minimum-effort grid question (Q26 in this part), where union-find over sorted edges is the alternative solution.
- Kruskal or Prim for 10^4 nodes and 10^5 edges? Either; the sort in Kruskal runs in C and is fast in Python. For a complete graph given as points (about n^2/2 edges), Prim with an O(n^2) array avoids materialising the edges (Q37).

**Common mistakes:**
- Not handling disconnected graphs (returning the sum of what was joined).
- Comparing `u != v` instead of components (misses cycles of length 3 and more).
- Recursive `find` without compression on a path-shaped union order.
- Claiming the MST itself is unique: only the weight is, unless all weights are distinct.

### Q30 ⭐⭐ 🟡 Open the lock (BFS over an implicit graph). A lock has four wheels, each showing a digit 0-9; one move turns one wheel one step up or down and 9 and 0 wrap around. It starts at '0000'. `deadends` is a list of up to 500 four-digit strings that jam the lock (if you reach one you cannot continue from it) and `target` is a four-digit string. Return the minimum number of moves to reach `target`, or -1 if impossible (also -1 if '0000' itself is a dead end; if `target` is a dead end it is unreachable). Describe the implicit graph (10^4 states, 8 neighbours each) and why you do not build it up front. Example: deadends=['0201', '0101', '0102', '1212', '2002'], target='0202' -> 6; deadends=['8888'], target='0009' -> 1; deadends=['0000'], target='8888' -> -1; deadends=['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'], target='8888' -> -1.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Shortest path in an unweighted implicit graph: BFS where a state is a string and neighbours are computed on demand.

**Say this first (1 line):** "Each four-digit combination is a node, each single-wheel turn is an edge, every edge costs one move, so BFS from '0000' gives the fewest moves. Dead ends are nodes I refuse to enter."

**Brute force:** DFS or enumerating all move sequences is exponential and finds a path, not the shortest. A level-by-level BFS using sets (no queue, no distance dictionary) is a second, independent implementation, and is used as the checker in the code, together with a bidirectional BFS.

**Optimal:**
- Nodes: the 10^4 strings `'0000'..'9999'`. Edges: 4 wheels times 2 directions, so exactly 8 neighbours per state; for example `'0000'` goes to `'1000'`, `'9000'`, `'0100'`, `'0900'` and so on. The code checks that all 10^4 states have 8 distinct neighbours (so 40000 undirected edges) and that all are reachable.
- Why not build it up front: the neighbours follow from a rule in two lines, so a generator function is shorter than an adjacency table, needs no memory for edges, and generalises to states where the graph is too large to store (sliding puzzle, Q32 in this part). With only 10^4 states, building it would also work here; the habit is the point.
- Algorithm: if `'0000'` is a dead end, return -1. Queue of `(state, moves)`, `seen = {'0000'}`. Pop; if it is the target, return its moves; for each neighbour not dead and not seen, mark seen and push (mark on push, so a state is queued once).
- Dead ends are simply never entered. The target being a dead end means it is never reached, so the answer is -1 without a special case, but the start being dead needs the explicit check (the start is added to `seen` before any dead-end test; the code shows the bug returning 8 instead of -1).
- BFS correctness: all edges cost 1, so the first time a state is popped its distance is minimal.
- Without dead ends the answer is the sum over wheels of `min(digit, 10 - digit)`; the code confirms it on 1429 sampled targets, and the farthest state `5555` is 20 moves away.

**Complexity:** Time O(S * 8) with S = 10^4 states, so at most 80000 neighbour visits; each costs O(1) string building (4 characters) and set lookups. Space O(S) for `seen` and the queue. With the 500 dead ends of the prompt only fewer states are visited.

**Dry run:** `deadends=['8888'], target='0009'`.
- Start `'0000'`, 0 moves. Neighbours: `'1000'`, `'9000'`, `'0100'`, `'0900'`, `'0010'`, `'0090'`, `'0001'`, `'0009'` (all 1 move).
- The target `'0009'` is one of them (the last wheel turned down from 0 to 9 by wrap-around). Pop it at 1 move: answer 1.
- Example 1 (answer 6): each of the six 4-move routes to `'0202'` hits a dead end (`'0101'`, `'0102'` or `'0201'`). One shortest route found by BFS is 0000, 1000, 1100, 1200, 1201, 1202, 0202: six moves.

**Code:**
```python
import random
from collections import deque

random.seed(30)

def neighbours(s):
    """The implicit graph: 8 neighbours computed on demand (4 wheels x up/down, with wrap-around)."""
    for i in range(4):
        d = int(s[i])
        for step in (1, 9):                               # +1 and -1 mod 10
            yield s[:i] + str((d + step) % 10) + s[i + 1:]

def open_lock(deadends, target):
    dead = set(deadends)
    if '0000' in dead:
        return -1
    seen = {'0000'}
    q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for t in neighbours(s):
            if t not in dead and t not in seen:           # mark on PUSH so no state is queued twice
                seen.add(t)
                q.append((t, d + 1))
    return -1

def open_lock_levels(deadends, target):
    """Independent brute force: expand one whole level at a time with sets (no queue, no per-node distance)."""
    dead = set(deadends)
    if '0000' in dead:
        return -1
    level, seen, d = {'0000'}, {'0000'}, 0
    while level:
        if target in level:
            return d
        nxt = set()
        for s in level:
            for t in neighbours(s):
                if t not in dead and t not in seen:
                    nxt.add(t)
        seen |= nxt
        level, d = nxt, d + 1
    return -1

def open_lock_bidirectional(deadends, target):
    """Follow-up: grow the smaller frontier from each end; meet in the middle."""
    dead = set(deadends)
    if '0000' in dead or target in dead:
        return -1
    if target == '0000':
        return 0
    a, b, seen_a, seen_b, d = {'0000'}, {target}, {'0000'}, {target}, 0
    while a and b:
        if len(a) > len(b):
            a, b, seen_a, seen_b = b, a, seen_b, seen_a
        nxt = set()
        d += 1
        for s in a:
            for t in neighbours(s):
                if t in seen_b:
                    return d
                if t not in dead and t not in seen_a:
                    seen_a.add(t)
                    nxt.add(t)
        a = nxt
    return -1

def open_lock_no_start_check(deadends, target):
    """Bug: forget that '0000' itself may be jammed."""
    dead = set(deadends)
    seen = {'0000'}
    q = deque([('0000', 0)])
    while q:
        s, d = q.popleft()
        if s == target:
            return d
        for t in neighbours(s):
            if t not in dead and t not in seen:
                seen.add(t)
                q.append((t, d + 1))
    return -1

for de, tg, want in [(['0201', '0101', '0102', '1212', '2002'], '0202', 6), (['8888'], '0009', 1),
                     (['0000'], '8888', -1), (['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'], '8888', -1)]:
    got = open_lock(de, tg)
    assert got == want == open_lock_levels(de, tg) == open_lock_bidirectional(de, tg), (de, tg, got, want)
    print(de, tg, '->', got)
print("forgetting the '0000' dead-end check on example 3 ->", open_lock_no_start_check(['0000'], '8888'), '(should be -1)')

# ---- the graph itself: 10^4 states, every state has exactly 8 distinct neighbours, all reachable, distance = sum of wheel distances
states = [f'{i:04d}' for i in range(10 ** 4)]
assert all(len(set(neighbours(s))) == 8 for s in states)
dist = {'0000': 0}
q = deque(['0000'])
while q:
    s = q.popleft()
    for t in neighbours(s):
        if t not in dist:
            dist[t] = dist[s] + 1
            q.append(t)
assert len(dist) == 10 ** 4
assert all(dist[s] == sum(min(int(c), 10 - int(c)) for c in s) for s in states)
print('states', len(states), '| neighbours each 8 | edges', 8 * len(states) // 2, '| farthest state', max(dist, key=dist.get), 'at', max(dist.values()), 'moves')

# ---- every possible target with no dead ends equals the wheel-distance formula
for s in states[::7]:
    assert open_lock([], s) == dist[s]
print('open_lock([], target) == sum of per-wheel distances on', len(states[::7]), 'sampled targets')

# ---- seeded random cross-check with up to 500 dead ends
def rnd():
    return f'{random.randrange(10 ** 4):04d}'
for _ in range(300):
    de = [rnd() for _ in range(random.choice([0, 5, 50, 500, 2000]))]
    tg = rnd()
    r = open_lock(de, tg)
    assert r == open_lock_levels(de, tg) == open_lock_bidirectional(de, tg), (de[:5], tg)
print('300 seeded random cases: queue BFS == level-set BFS == bidirectional BFS')

# ---- edge cases
assert open_lock([], '0000') == 0
assert open_lock(['0000'], '0000') == -1
assert open_lock(['0001'], '0001') == -1                  # target is a dead end
assert open_lock(['1000', '9000', '0100', '0900', '0010', '0090', '0001', '0009'], '5555') == -1   # all 8 neighbours of the start jammed
print('edge asserts passed')
```

**Output (my run):**
```
['0201', '0101', '0102', '1212', '2002'] 0202 -> 6
['8888'] 0009 -> 1
['0000'] 8888 -> -1
['8887', '8889', '8878', '8898', '8788', '8988', '7888', '9888'] 8888 -> -1
forgetting the '0000' dead-end check on example 3 -> 8 (should be -1)
states 10000 | neighbours each 8 | edges 40000 | farthest state 5555 at 20 moves
open_lock([], target) == sum of per-wheel distances on 1429 sampled targets
300 seeded random cases: queue BFS == level-set BFS == bidirectional BFS
edge asserts passed
```

**Edge cases:**
- Target `'0000'` and not dead: 0 moves.
- `'0000'` dead: -1 at once, even if the target is `'0000'`.
- Target dead: -1.
- Start enclosed by 8 dead neighbours: BFS exhausts and returns -1 (the last example, and the 4th prompt example).
- Duplicate dead ends in the list: a set handles them.
- 9 to 0 and 0 to 9 wrap, so `'0009'` is one move away.

**Follow-ups:**
- Faster in the worst case? Bidirectional BFS (in the code) searches from both ends and cuts the work from about b^d to 2 * b^(d/2); here the graph is small, so the gain is modest.
- Return the actual sequence? Store a parent dictionary and walk it back from the target.
- Many targets from one start? One BFS gives all distances; the code builds the full distance table that way.

**Common mistakes:**
- Marking states visited when popped (queues duplicates, up to 8 times more work).
- Forgetting the wrap-around (`(d + 1) % 10`, `(d + 9) % 10`).
- Not checking the start against the dead ends.
- Using a list for `deadends` lookups (O(500) per check instead of O(1)); convert to a set once.

### Q31 ⭐⭐ 🟡 Topological sort by DFS (reverse postorder). `n` nodes 0..n-1 (1 <= n <= 10^5) and `edges` a list of directed [u, v] (0 <= len <= 2*10^5; self loops possible). Run an iterative three-colour DFS: loop over start nodes 0, 1, ..., n-1 in ascending order, explore each node's out-edges in input order, append a node to `post` when it finishes, and return `post` reversed. If any edge reaches a node currently on the DFS path, return []. This order is deterministic, and the checker accepts exactly this list. Explain why reverse postorder puts every edge u -> v with u before v, and why the order generally differs from Kahn's. Sizes are chosen so that a recursive DFS would exceed CPython's default recursion limit of 1000, so an iterative method (queue or explicit stack) is required. Example: n=4, edges=[[0, 1], [0, 2], [1, 3], [2, 3]] -> [0, 2, 1, 3]; n=3, edges=[[0, 1], [1, 2], [2, 0]] -> []; n=3, edges=[] -> [2, 1, 0]; n=5, edges=[[3, 1], [4, 1], [4, 0], [2, 3]] -> [4, 2, 3, 1, 0].
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort by depth-first search: reverse postorder, with three colours (new, on the path, finished) for cycle detection. Iterative, because the input is deep.

**Say this first (1 line):** "A node is appended after everything reachable from it has finished, so reversing that finish order puts every node before its successors. An edge into a node still on the current path is a cycle. The DFS must be iterative: a 10^5-node chain breaks CPython's recursion limit of 1000."

**Brute force:** The textbook recursive DFS gives the same list (it is the specification in the code), but a path of 5000 nodes already raises `RecursionError`, so it fails the stated sizes. Another brute force is to try every permutation of the nodes and check all edges, O(n! * E), used mentally for n <= 8. For the cycle test the code also compares with Kahn's algorithm.

**Optimal:**
- `color`: 0 new, 1 on the current DFS path, 2 finished. `post` is the list of finished nodes.
- For each start node `s` in ascending order: if new, mark 1 and push a frame `(s, iterator over adj[s])`.
- Loop on the top frame. Take the next out-neighbour `v` from its iterator:
  - `color[v] == 1`: back edge, so there is a cycle: return `[]`. This includes a self loop.
  - `color[v] == 0`: mark 1, push a frame for `v`, `break` out of the `for` (go deeper). The iterator keeps its position, so when `v` finishes we continue with the next edge.
  - `color[v] == 2`: already finished, ignore.
- If the iterator is exhausted (the `for ... else` branch), `u` is finished: mark 2, append to `post`, pop the frame.
- Return `post[::-1]`.
- Why reverse postorder is topological: take an edge `u -> v` in an acyclic graph. When DFS first examines the edge, `v` is either new (then `v` finishes before `u` does, since `u` is still open), or already finished (so `v` finished before `u`). A third possibility, `v` on the path, is a cycle and has been excluded. So in every case `v` is finished before `u`, and in the reversed list `u` comes before `v`.
- Why the order generally differs from Kahn's: Kahn emits nodes as their in-degrees reach 0, which is a breadth-first flavour, ascending by label here; DFS order depends on the visiting order and ends with the last start node first (the empty graph gives `[2, 1, 0]`, Kahn gives `[0, 1, 2]`). Both are valid topological orders. The code counts the graphs where they differ (364 of the 572 acyclic graphs tested).
- The checker accepts exactly this list, so the deterministic rules matter: start nodes ascending, out-edges in input order, post appended on finish, final reversal.

**Complexity:** Time O(V + E): each node gets one frame and each edge is examined once through the iterator. Space O(V + E) for the adjacency lists, colours, the explicit stack (up to V frames) and `post`.

**Dry run:** `n=4, edges=[[0,1],[0,2],[1,3],[2,3]]`.
- Start 0: colour 1. Edges of 0: 1, then 2. Go to 1 (colour 1).
- Node 1: edge to 3, new, go to 3. Node 3 has no edges: finish, `post=[3]`.
- Back in 1: no more edges, finish, `post=[3,1]`.
- Back in 0: next edge to 2, new, go to 2. Edge 2->3: 3 is finished, ignore. Finish 2: `post=[3,1,2]`. Finish 0: `post=[3,1,2,0]`.
- Starts 1, 2, 3 are already done. Reverse: `[0,2,1,3]`, the prompt's answer. Kahn would give `[0,1,2,3]`.

**Code:**
```python
import itertools
import random
import sys
from collections import deque

random.seed(31)

def dfs_topo(n, edges):
    """Iterative three-colour DFS. 0 = new, 1 = on the current path, 2 = finished. Returns reverse postorder or [] on a cycle."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    post = []
    for s in range(n):                                   # start nodes in ascending order
        if color[s]:
            continue
        color[s] = 1
        stack = [(s, iter(adj[s]))]                      # each frame remembers how far we got in its edge list
        while stack:
            u, it = stack[-1]
            for v in it:                                 # resumes where it left off
                if color[v] == 1:                        # edge to a node on the path: cycle (also catches self loops)
                    return []
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, iter(adj[v])))
                    break                                # go deeper; come back to this frame later
            else:                                        # edge list exhausted: u is finished
                color[u] = 2
                post.append(u)
                stack.pop()
    return post[::-1]

def dfs_topo_recursive(n, edges):
    """Textbook recursive version: the specification for the order (small n only, or it hits the recursion limit)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    color = [0] * n
    post = []
    cyc = [False]
    def go(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1:
                cyc[0] = True
            elif color[v] == 0:
                go(v)
        color[u] = 2
        post.append(u)
    for s in range(n):
        if color[s] == 0:
            go(s)
    return [] if cyc[0] else post[::-1]

def kahn(n, edges):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == n else []

def is_topological(n, edges, order):
    pos = {x: i for i, x in enumerate(order)}
    return len(order) == n and len(pos) == n and all(pos[u] < pos[v] for u, v in edges)

for n, e, want in [(4, [[0, 1], [0, 2], [1, 3], [2, 3]], [0, 2, 1, 3]), (3, [[0, 1], [1, 2], [2, 0]], []),
                   (3, [], [2, 1, 0]), (5, [[3, 1], [4, 1], [4, 0], [2, 3]], [4, 2, 3, 1, 0])]:
    got = dfs_topo(n, e)
    assert got == want == dfs_topo_recursive(n, e), (n, e, got, want)
    print(n, e, '->', got, '| Kahn gives', kahn(n, e))

# ---- the recursion limit: a 5000-node path
n = 5000
path = [[i, i + 1] for i in range(n - 1)]
try:
    dfs_topo_recursive(n, path)
except RecursionError:
    print('recursive DFS on a', n, 'node path -> RecursionError (limit', sys.getrecursionlimit(), ')')
assert dfs_topo(n, path) == list(range(n))
n = 2 * 10 ** 5
path = [[i, i + 1] for i in range(n - 1)]
assert dfs_topo(n, path) == list(range(n))
assert dfs_topo(n, [[i + 1, i] for i in range(n - 1)]) == list(range(n - 1, -1, -1))
assert dfs_topo(n, path + [[n - 1, 0]]) == []                           # one back edge closes the cycle
print('iterative: 2*10^5-node path, its reverse, and the path closed into a cycle all handled')

# ---- exhaustive: every edge SET on n <= 4 (self loops included for n <= 3), plus ordered edge lists with repeats on n = 3
cnt = cyc = differs = 0
for n, loops in [(1, True), (2, True), (3, True), (4, False)]:
    pairs = [(a, b) for a in range(n) for b in range(n) if loops or a != b]
    for mask in range(1 << len(pairs)):
        e = [list(p) for i, p in enumerate(pairs) if mask >> i & 1]
        r = dfs_topo(n, e)
        assert r == dfs_topo_recursive(n, e), (n, e)
        k = kahn(n, e)
        assert (r == []) == (k == []), (n, e)                           # both detect exactly the cyclic graphs
        if r:
            assert is_topological(n, e, r) and is_topological(n, e, k)
            differs += r != k
        else:
            cyc += 1
        cnt += 1
print('exhaustive on', cnt, 'graphs:', cyc, 'cyclic ->', '[]; every acyclic one gives a valid order equal to the recursive DFS;',
      'DFS order differs from Kahn order on', differs)
opts = [(a, b) for a in range(3) for b in range(3)]
for k in range(4):
    for combo in itertools.product(opts, repeat=k):
        e = [list(p) for p in combo]
        assert dfs_topo(3, e) == dfs_topo_recursive(3, e)
print('ordered edge lists with repeats on 3 nodes also match the recursive version')

# ---- seeded random DAGs and cyclic graphs
for _ in range(500):
    n = random.randint(1, 9)
    perm = list(range(n))
    random.shuffle(perm)
    e = [[perm[min(a, b)], perm[max(a, b)]] for a, b in ((random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 14))) if a != b]
    r = dfs_topo(n, e)
    assert r == dfs_topo_recursive(n, e) and is_topological(n, e, r)
print('500 seeded random DAGs: valid order, equal to the recursive DFS')

# ---- big: 10^5 nodes, 2*10^5 edges, random DAG over a shuffled labelling
n, E = 10 ** 5, 2 * 10 ** 5
perm = list(range(n))
random.shuffle(perm)
e = []
while len(e) < E:
    a, b = random.randrange(n), random.randrange(n)
    if a != b:
        e.append([perm[min(a, b)], perm[max(a, b)]])
r = dfs_topo(n, e)
assert is_topological(n, e, r)
print('n=10^5, E=2*10^5 random DAG: valid topological order of length', len(r))
assert dfs_topo(1, [[0, 0]]) == []
print('self loop -> []')
```

**Output (my run):**
```
4 [[0, 1], [0, 2], [1, 3], [2, 3]] -> [0, 2, 1, 3] | Kahn gives [0, 1, 2, 3]
3 [[0, 1], [1, 2], [2, 0]] -> [] | Kahn gives []
3 [] -> [2, 1, 0] | Kahn gives [0, 1, 2]
5 [[3, 1], [4, 1], [4, 0], [2, 3]] -> [4, 2, 3, 1, 0] | Kahn gives [2, 4, 3, 0, 1]
recursive DFS on a 5000 node path -> RecursionError (limit 1000 )
iterative: 2*10^5-node path, its reverse, and the path closed into a cycle all handled
exhaustive on 4626 graphs: 4054 cyclic -> []; every acyclic one gives a valid order equal to the recursive DFS; DFS order differs from Kahn order on 364
ordered edge lists with repeats on 3 nodes also match the recursive version
500 seeded random DAGs: valid order, equal to the recursive DFS
n=10^5, E=2*10^5 random DAG: valid topological order of length 100000
self loop -> []
```

**Edge cases:**
- Self loop: the neighbour is the node itself with colour 1, so `[]`.
- No edges: all nodes isolated, order `[n-1, ..., 0]` (reverse of the start order).
- A cycle that is only reachable from a later start node is still found, since every unvisited node becomes a start.
- A cycle that sits next to a valid part (the 3-cycle example) returns `[]`, not a partial order.
- Repeated edges: the second one sees colour 2 or 1 and behaves correctly (tested with repeats on 3 nodes).
- Deep chains (2 * 10^5 nodes, both directions) run without recursion.

**Follow-ups:**
- Can I raise the recursion limit instead? `sys.setrecursionlimit` lets the interpreter try deeper, but each frame still uses C stack and a very deep chain can crash the process; the explicit stack is the safe fix. Part 7 Q35 covers the same trap for skewed trees.
- Why two colours are not enough: a visited flag cannot tell a back edge (cycle) from an edge to an already finished node (harmless cross or forward edge). Both look "visited".
- DFS or Kahn? Kahn gives levels (used in Q24) and the cycle check is a count; DFS gives a canonical order and generalises to strongly connected components (Part 14).

**Common mistakes:**
- Appending to `post` when a node is pushed instead of when it finishes.
- Forgetting to reverse.
- A single `visited` set for cycle detection (false cycles on diamonds like 0->1, 0->2, 1->3, 2->3).
- Processing the stack as plain "pop and push all neighbours": that gives a different order and does not know when a node finishes.

### Q32 ⭐⭐ 🔴 Sliding puzzle (state-space BFS). The board is a 2 x 3 grid holding the numbers 0-5 once each, where 0 is the blank. One move slides a tile that is up, down, left or right of the blank into it. Return the minimum number of moves to reach [[1,2,3],[4,5,0]], or -1 if it is unreachable. Treat each board as one node (flatten it to a tuple) and BFS; state the number of states (720), why exactly half of them are unreachable, and why the same code on a bigger board needs a smarter search. Example: board=[[1, 2, 3], [4, 0, 5]] -> 1; board=[[1, 2, 3], [5, 4, 0]] -> -1; board=[[4, 1, 2], [5, 0, 3]] -> 5; board=[[1, 2, 3], [4, 5, 0]] -> 0.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** State-space BFS: each configuration is a node, each legal move is an edge, all edges cost one move.

**Say this first (1 line):** "Flatten the board to a tuple so it is hashable, BFS from the start to the goal with a visited set. There are only 720 boards, so it is instant, and exactly half of them cannot reach the goal."

**Brute force:** DFS or random walks do not give the minimum and can loop forever without a visited set. A second exact method is one BFS backwards from the goal over all boards: moves are reversible, so the distance from the goal to a board equals the distance from the board to the goal. That gives the whole answer table at once, and it is the checker in the code (all 720 boards agree).

**Optimal:**
- State: the board read row by row as a 6-tuple, for example `(4, 1, 2, 5, 0, 3)`. Goal: `(1, 2, 3, 4, 5, 0)`.
- Neighbours of the blank: a precomputed table of adjacent positions for the 2 x 3 shape (position 0 touches 1 and 3, position 1 touches 0, 2 and 4, and so on). Swap the blank with each neighbour to get the next board.
- BFS with a `deque` of `(state, moves)` and a `seen` set. First time the goal appears, its move count is the minimum, because every move costs 1. If the queue empties without the goal, return -1.
- Why 720 states: the 6 cells hold 6 distinct values, so 6! = 720 boards.
- Why exactly half are unreachable: look at the 5 numbered tiles read row by row and count inversions (pairs in the wrong order). Sliding a tile horizontally does not change the reading order. Sliding a tile vertically jumps it over exactly 2 other tiles on a 3-wide board, which changes the inversion count by 0 or +-2, so the parity never changes. The goal has 0 inversions (even), so only even-inversion boards are reachable. The code verifies on all 720 boards that "reachable" and "even inversions" are the same set: 360 and 360. Example 2 (`1 2 3 5 4`, one inversion) is therefore -1.
- Bigger boards: 3 x 3 has 9! = 362,880 boards (181,440 reachable); BFS still fits in memory (the code runs it, hardest board 31 moves). 4 x 4 has 16! = about 2 * 10^13 boards, so plain BFS is hopeless: use A* or IDA* with the Manhattan-distance heuristic (or pattern databases), which explores only promising boards.

**Complexity:** Time O(S * b) with S <= 720 states and branching factor b <= 3, so at most 2160 successor checks; each builds a 6-tuple, O(6). Space O(S) for `seen` and the queue. For an n x m board: S = (nm)!, so factorial growth.

**Dry run:** `[[4,1,2],[5,0,3]]` -> flat `(4,1,2,5,0,3)`, answer 5.
- Blank at position 4. One shortest route (found by the BFS): slide 5 right -> `(4,1,2,0,5,3)`; slide 4 down -> `(0,1,2,4,5,3)`; slide 1 left -> `(1,0,2,4,5,3)`; slide 2 left -> `(1,2,0,4,5,3)`; slide 3 up -> `(1,2,3,4,5,0)`.
- That is 5 moves. BFS tries all boards at distance 1, 2, ..., and the goal first appears at level 5.

**Code:**
```python
import itertools
import math
from collections import Counter, deque

GOAL = (1, 2, 3, 4, 5, 0)
# neighbours of each flat position on a 2 x 3 board: index = 3 * row + col
NB = {0: (1, 3), 1: (0, 2, 4), 2: (1, 5), 3: (0, 4), 4: (1, 3, 5), 5: (2, 4)}

def sliding_puzzle(board):
    """BFS over boards. A node is the whole board flattened to a tuple (hashable, so it can live in a set)."""
    start = tuple(x for row in board for x in row)
    if start == GOAL:
        return 0
    seen = {start}
    q = deque([(start, 0)])
    while q:
        s, d = q.popleft()
        z = s.index(0)
        for j in NB[z]:                                   # slide the tile at j into the blank
            l = list(s)
            l[z], l[j] = l[j], l[z]
            t = tuple(l)
            if t not in seen:
                if t == GOAL:
                    return d + 1
                seen.add(t)
                q.append((t, d + 1))
    return -1

def distance_table():
    """Independent method: one BFS BACKWARDS from the goal over all boards. Moves are reversible, so distance is symmetric."""
    dist = {GOAL: 0}
    frontier = [GOAL]
    while frontier:
        nxt = []
        for s in frontier:
            z = s.index(0)
            for j in NB[z]:
                l = list(s)
                l[z], l[j] = l[j], l[z]
                t = tuple(l)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    nxt.append(t)
        frontier = nxt
    return dist

def inversions_even(flat):
    tiles = [x for x in flat if x]
    inv = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inv % 2 == 0

for b, want in [([[1, 2, 3], [4, 0, 5]], 1), ([[1, 2, 3], [5, 4, 0]], -1), ([[4, 1, 2], [5, 0, 3]], 5), ([[1, 2, 3], [4, 5, 0]], 0)]:
    got = sliding_puzzle(b)
    assert got == want, (b, got, want)
    print(b, '->', got)

# ---- all 720 boards: forward BFS equals the backward table, and exactly half are unreachable
table = distance_table()
boards = list(itertools.permutations(range(6)))
assert len(boards) == 720
res = {}
for p in boards:
    b = [list(p[:3]), list(p[3:])]
    res[p] = sliding_puzzle(b)
    assert res[p] == table.get(p, -1), p
reach = sum(v >= 0 for v in res.values())
print('boards', len(boards), '| reachable', reach, '| unreachable', len(boards) - reach, '| hardest board needs', max(res.values()), 'moves')
print('boards per distance:', sorted(Counter(v for v in res.values() if v >= 0).items()))

# ---- why exactly half: a move never changes the parity of inversions among the 5 tiles (read row by row), and the goal has 0 inversions
assert all((res[p] >= 0) == inversions_even(p) for p in boards)
print('reachable  <=>  even number of inversions among tiles 1..5: holds for all 720 boards')
# a horizontal slide keeps the reading order of the tiles; a vertical slide jumps one tile over exactly 2 others (3-wide board), an even change
unsolvable = [[1, 2, 3], [5, 4, 0]]
print('example 2 has tiles read 1 2 3 5 4: one inversion (odd) ->', sliding_puzzle(unsolvable))

# ---- the state space grows too fast for the same code on bigger boards
print('states: 2x3', math.factorial(6), 'reachable', math.factorial(6) // 2, '| 3x3', math.factorial(9), 'reachable', math.factorial(9) // 2,
      '| 4x4', math.factorial(16), 'reachable', math.factorial(16) // 2)

# ---- the same BFS code does handle the 3x3 (8-puzzle) in memory, to show where the limit starts
def bfs_count_3x3():
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    seen = {goal}
    fr = [goal]
    depth = 0
    while True:
        nxt = []
        for s in fr:
            z = s.index(0)
            r, c = divmod(z, 3)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = r + dr, c + dc
                if 0 <= a < 3 and 0 <= b < 3:
                    j = 3 * a + b
                    l = list(s)
                    l[z], l[j] = l[j], l[z]
                    t = tuple(l)
                    if t not in seen:
                        seen.add(t)
                        nxt.append(t)
        if not nxt:
            return len(seen), depth
        fr, depth = nxt, depth + 1
n3, depth3 = bfs_count_3x3()
assert n3 == math.factorial(9) // 2
print('3x3 BFS from the goal visits', n3, 'boards, hardest needs', depth3, 'moves; 4x4 would need about 10^13 (use A* or IDA* with a heuristic)')

# ---- edge asserts
assert sliding_puzzle([[1, 2, 3], [4, 5, 0]]) == 0
assert sliding_puzzle([[1, 2, 3], [4, 0, 5]]) == 1
assert sliding_puzzle([[0, 1, 2], [3, 4, 5]]) == table[(0, 1, 2, 3, 4, 5)] == 15
print('edge asserts passed')
```

**Output (my run):**
```
[[1, 2, 3], [4, 0, 5]] -> 1
[[1, 2, 3], [5, 4, 0]] -> -1
[[4, 1, 2], [5, 0, 3]] -> 5
[[1, 2, 3], [4, 5, 0]] -> 0
boards 720 | reachable 360 | unreachable 360 | hardest board needs 21 moves
boards per distance: [(0, 1), (1, 2), (2, 3), (3, 5), (4, 6), (5, 7), (6, 10), (7, 12), (8, 12), (9, 16), (10, 23), (11, 25), (12, 28), (13, 39), (14, 44), (15, 40), (16, 29), (17, 21), (18, 18), (19, 12), (20, 6), (21, 1)]
reachable  <=>  even number of inversions among tiles 1..5: holds for all 720 boards
example 2 has tiles read 1 2 3 5 4: one inversion (odd) -> -1
states: 2x3 720 reachable 360 | 3x3 362880 reachable 181440 | 4x4 20922789888000 reachable 10461394944000
3x3 BFS from the goal visits 181440 boards, hardest needs 31 moves; 4x4 would need about 10^13 (use A* or IDA* with a heuristic)
edge asserts passed
```

**Edge cases:**
- Already solved: 0 moves (checked before the loop, so no queue work).
- One move away: 1.
- Unsolvable (odd inversions): the search exhausts all 360 reachable boards and returns -1.
- Hardest solvable board: 21 moves. The code lists how many boards sit at each distance.
- Input as lists of lists: convert to a tuple, lists are not hashable and cannot go in a set.

**Follow-ups:**
- Print the moves? Store a parent pointer per state and walk it back from the goal.
- Test solvability without search? The inversion parity rule for odd width (this 2 x 3 board and the 3 x 3 puzzle); for even width the blank's row also matters.
- Bidirectional BFS? Meets in the middle and cuts nodes explored; on 720 states it is not needed, on larger ones it helps.

**Common mistakes:**
- Using a list as the state (unhashable) or mutating a shared list between neighbours (copy before swapping).
- Marking states seen when popped, which queues duplicates.
- Swapping the wrong pair: the blank swaps with a neighbour, never two tiles with each other.
- Forgetting the start-equals-goal case (answer 0), or returning from the loop before the goal check on the first board.

### Q33 ⭐⭐ 🔴 Alien dictionary (topological order from constraints). `words` is a list of 1 to 100 non-empty lowercase words (length <= 100) claimed to be sorted in an alien alphabet's lexicographic order (a proper prefix comes before the longer word). Return a string containing each distinct letter that appears in `words` exactly once, in an order under which `words` is sorted, or '' if no such order exists (a cycle among the constraints, or a longer word placed before its own prefix). Many alphabets can be valid: the checker accepts any string that contains each letter once and under which the list is sorted, and accepts '' only if no ordering of the letters works; the example shows one accepted answer. Explain how the first differing letters of adjacent words give edges, and why only adjacent pairs are needed. Example: words=['wrt', 'wrf', 'er', 'ett', 'rftt'] -> 'wertf'; words=['z', 'x', 'z'] -> ''; words=['abc', 'ab'] -> ''; words=['a', 'b', 'a'] -> ''; words=['ab'] -> 'ab'.
**Asked at:** Graph pattern guides and lists (techinterview.org graph interview patterns and comprehensive graph guides, DesignGurus common graph-traversal questions, Techie Delight graph practice list; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Topological sort on a graph built from constraints: letters are nodes, "this letter comes before that letter" is an edge.

**Say this first (1 line):** "Compare each adjacent pair of words, find the first position where they differ, and that gives one edge: the letter in the first word comes before the letter in the second. Then topologically sort the letters; a cycle, or a longer word before its own prefix, means there is no valid alphabet."

**Brute force:** Try every permutation of the distinct letters and test whether the word list is sorted under it. That is up to 26! orders, so it only works for at most 7 or 8 letters. It is the checker in the code: it decides when `''` is a correct answer.

**Optimal:**
- Nodes: every distinct letter in any word (including letters that get no constraint: they must still appear exactly once in the answer).
- For each adjacent pair `(a, b)`: scan for the first index where `a[i] != b[i]`. If found, add the edge `a[i] -> b[i]` (once per distinct pair; a repeated edge must not double-count the in-degree) and stop looking at this pair. If no difference is found, one word is a prefix of the other: fine if `a` is the shorter or they are equal, impossible if `len(a) > len(b)` (for example `abc` before `ab`): return `''`.
- Kahn's algorithm: queue of in-degree-0 letters, pop, output, decrease the successors. If the output has fewer letters than the alphabet, there is a cycle: return `''`.
- Why only adjacent pairs: the list is sorted, so for `i < j` the order of `words[i]` and `words[j]` follows from the chain `words[i] <= words[i+1] <= ... <= words[j]` by transitivity. Any constraint from a non-adjacent pair is implied by the adjacent ones. Using all pairs would add up to 4950 candidate pairs and the same answer. The code checks it: on all 22,620 small word lists plus 400 random ones, the all-pairs version is impossible exactly when the adjacent-only version is.
- Why only the first difference counts: after the first differing letters the rest of the words says nothing about the order.
- Many answers are valid when the constraints leave letters unordered. The code's validator accepts any string containing each letter once under which the list is sorted, and accepts `''` only when the exhaustive permutation search finds no order. The prompt's `'wertf'` is accepted and so is our output.

**Complexity:** Let L be the total length of all words (up to 100 * 100 = 10^4) and K the alphabet size (up to 26). Building edges: O(L) (each adjacent pair is scanned once, up to the shorter length). Kahn: O(K + number of edges), and the edges are at most min(99, K^2). Total O(L + K). Space O(K + edges).

**Dry run:** `['wrt','wrf','er','ett','rftt']`.
- wrt vs wrf: first difference at index 2, t vs f: edge t -> f.
- wrf vs er: index 0, w vs e: edge w -> e.
- er vs ett: index 1, r vs t: edge r -> t.
- ett vs rftt: index 0, e vs r: edge e -> r.
- Graph: w -> e -> r -> t -> f. In-degrees: only w is 0. Kahn outputs w, e, r, t, f: `'wertf'`.
- Example `['z','x','z']`: z -> x, x -> z: a cycle, nothing has in-degree 0, output empty, so `''`.

**Code:**
```python
import itertools
import random
from collections import deque

random.seed(33)

def alien_order(words):
    """Edges from the first differing letters of ADJACENT words, then Kahn's algorithm. '' if impossible."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:                       # one edge per distinct ordered pair
                    adj[x].add(y)
                    indeg[y] += 1
                break
        else:                                             # no differing letter: one word is a prefix of the other
            if len(a) > len(b):                           # longer word first is impossible
                return ''
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''   # fewer than all letters: a cycle

def sorted_under(words, order):
    rank = {c: i for i, c in enumerate(order)}
    key = lambda w: [rank[c] for c in w]                  # list comparison: a proper prefix is smaller
    return all(key(a) <= key(b) for a, b in zip(words, words[1:]))

def valid(words, got):
    """The checker the prompt states: each letter exactly once and the list sorted under it; '' only if NO ordering works."""
    letters = sorted({c for w in words for c in w})
    if got == '':
        return not any(sorted_under(words, p) for p in itertools.permutations(letters))
    return sorted(got) == letters and sorted_under(words, got)

def alien_brute(words):
    letters = sorted({c for w in words for c in w})
    for p in itertools.permutations(letters):
        if sorted_under(words, p):
            return ''.join(p)
    return ''

def alien_all_pairs(words):
    """Same algorithm but with constraints from EVERY pair i < j: shows adjacent pairs already imply all of them."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = words[i], words[j]
            for x, y in zip(a, b):
                if x != y:
                    adj[x].add(y)
                    break
            else:
                if len(a) > len(b):
                    return ''
    indeg = {c: 0 for c in letters}
    for u in letters:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''

def alien_no_prefix_check(words):
    """Bug: ignore the 'longer word before its own prefix' case."""
    letters = sorted({c for w in words for c in w})
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:
                    adj[x].add(y)
                    indeg[y] += 1
                break
    q = deque(c for c in letters if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ''.join(out) if len(out) == len(letters) else ''

for w, shown in [(['wrt', 'wrf', 'er', 'ett', 'rftt'], 'wertf'), (['z', 'x', 'z'], ''), (['abc', 'ab'], ''), (['a', 'b', 'a'], ''), (['ab'], 'ab')]:
    got = alien_order(w)
    assert valid(w, got) and valid(w, shown), (w, got, shown)
    print(w, '->', repr(got), '| prompt shows', repr(shown), '| both accepted')

print("no prefix check on ['abc','ab'] ->", repr(alien_no_prefix_check(['abc', 'ab'])), '(wrongly accepted: no differing letter, so no edge)')

# ---- exhaustive: every list of 1..4 words over {a,b,c}, lengths 1..2 (12 possible words): our answer is accepted by the validator,
# '' appears exactly when no permutation works, and adjacent-pair edges agree with all-pair edges
words_all = [''.join(p) for L in (1, 2) for p in itertools.product('abc', repeat=L)]
cnt = empties = 0
for k in range(1, 5):
    for combo in itertools.product(words_all, repeat=k):
        w = list(combo)
        got = alien_order(w)
        assert valid(w, got), (w, got)
        assert (got == '') == (alien_brute(w) == ''), w
        assert (alien_all_pairs(w) == '') == (got == ''), w
        empties += got == ''
        cnt += 1
print('exhaustive on', cnt, 'word lists:', empties, 'impossible; all answers accepted by the validator, adjacent pairs == all pairs')

# ---- seeded random lists over 5 letters: sample from a hidden alphabet order so most are solvable, then corrupt some
for t in range(400):
    alpha = random.sample('abcde', 5)
    rank = {c: i for i, c in enumerate(alpha)}
    ws = [''.join(random.choice('abcde') for _ in range(random.randint(1, 4))) for _ in range(random.randint(1, 8))]
    ws.sort(key=lambda s: [rank[c] for c in s])
    if t % 3 == 0 and len(ws) > 1:
        i, j = random.sample(range(len(ws)), 2)
        ws[i], ws[j] = ws[j], ws[i]                      # may break sortedness
    got = alien_order(ws)
    assert valid(ws, got), (ws, got)
    assert (alien_all_pairs(ws) == '') == (got == '')
print('400 seeded random lists (5 letters): accepted by the validator; adjacent == all pairs')

# ---- letters with no constraint must still appear exactly once
r = alien_order(['x', 'y', 'q'])
assert sorted(alien_order(['ab', 'cd'])) == list('abcd') and sorted(r) == list('qxy') and valid(['x', 'y', 'q'], r)
print("unconstrained letters: ['ab','cd'] ->", alien_order(['ab', 'cd']))

# ---- max size: 100 words of length 100 over 26 letters in one hidden order; plus a 26-letter chain
alpha = random.sample('abcdefghijklmnopqrstuvwxyz', 26)
rank = {c: i for i, c in enumerate(alpha)}
ws = sorted((''.join(random.choice(alpha) for _ in range(100)) for _ in range(100)), key=lambda s: [rank[c] for c in s])
got = alien_order(ws)
assert got != '' and sorted(got) == sorted(set(''.join(ws))) and sorted_under(ws, got)
print('100 words of length 100: letters', len(got), 'ordering accepted')
chain = [alpha[i] for i in range(26)]
assert alien_order(chain) == ''.join(alpha) and alien_order(['a']) == 'a'
print('edge asserts passed')
```

**Output (my run):**
```
['wrt', 'wrf', 'er', 'ett', 'rftt'] -> 'wertf' | prompt shows 'wertf' | both accepted
['z', 'x', 'z'] -> '' | prompt shows '' | both accepted
['abc', 'ab'] -> '' | prompt shows '' | both accepted
['a', 'b', 'a'] -> '' | prompt shows '' | both accepted
['ab'] -> 'ab' | prompt shows 'ab' | both accepted
no prefix check on ['abc','ab'] -> 'abc' (wrongly accepted: no differing letter, so no edge)
exhaustive on 22620 word lists: 16140 impossible; all answers accepted by the validator, adjacent pairs == all pairs
400 seeded random lists (5 letters): accepted by the validator; adjacent == all pairs
unconstrained letters: ['ab','cd'] -> abdc
100 words of length 100: letters 26 ordering accepted
edge asserts passed
```

**Edge cases:**
- One word: the letters of the word, in any order that keeps each once; there are no constraints (the prompt shows `'ab'`, but `'ba'` is equally valid, and the validator accepts both).
- Prefix cases: `['ab','abc']` is fine (no edge); `['abc','ab']` is impossible. Missing this check is the most common bug: the code shows it returning `'abc'`.
- Identical adjacent words: no difference, lengths equal, no constraint.
- A cycle across non-adjacent words (`['a','b','a']`): transitive through adjacent edges, found as the cycle a -> b -> a.
- Letters that never get an edge still count: they must be in the output once. Compare the output's sorted letters with the alphabet.
- Deduplicate edges: two adjacent pairs giving the same letter pair must not add 2 to the in-degree and then decrement once.

**Follow-ups:**
- Return all valid orders or count them? That is counting topological orders, exponential in general; for ties, Kahn with a lexicographic-smallest heap gives a unique canonical answer.
- Is the order unique? Only if the Kahn queue never holds two letters at once (a Hamiltonian path in the constraint DAG). The code's `['ab','cd']` example has several.
- DFS version? Same edges, reverse postorder with a three-colour cycle check (Q31 in this part).

**Common mistakes:**
- Adding edges for every differing position instead of only the first.
- Omitting the prefix check.
- Counting a duplicate edge twice in the in-degree.
- Building the graph only from letters that appear in an edge, so unconstrained letters vanish from the answer.
- Comparing with the example string and expecting `'wertf'`: other valid answers exist when constraints do not pin the order.
