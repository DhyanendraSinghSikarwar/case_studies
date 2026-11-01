# Reference solutions (S) and independent brute force / validators for Book 5 Part 8. Imported by check_examples.py.
import heapq, itertools, random
from collections import Counter, deque
from functools import lru_cache

# ---------- 3 stars
def s_heapq_layout(vals):
    h = []
    for v in vals: heapq.heappush(h, v)
    pushed = list(h)
    h2 = list(vals); heapq.heapify(h2)
    h3 = list(pushed); pops = [heapq.heappop(h3) for _ in range(min(3, len(h3)))]
    m = []
    for v in vals: heapq.heappush(m, -v)
    top = [-heapq.heappop(m) for _ in range(min(3, len(m)))]
    return [pushed, h2, pops, top]

def s_kth_stream(k, nums, adds):
    h = list(nums); heapq.heapify(h)
    while len(h) > k: heapq.heappop(h)
    out = []
    for a in adds:
        if len(h) < k: heapq.heappush(h, a)
        elif a > h[0]: heapq.heapreplace(h, a)
        out.append(h[0])
    return out
def b_kth_stream(k, nums, adds):
    cur = list(nums); out = []
    for a in adds:
        cur.append(a); out.append(sorted(cur)[-k])
    return out

def s_meeting_rooms1(intervals):
    iv = sorted(intervals)
    return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))
def b_meeting_rooms1(intervals):
    return not any(a[0] < b[1] and b[0] < a[1] for a, b in itertools.combinations(intervals, 2))

def s_kth_largest(nums, k):
    h = []
    for x in nums:
        if len(h) < k: heapq.heappush(h, x)
        elif x > h[0]: heapq.heapreplace(h, x)
    return h[0]
def b_kth_largest(nums, k): return sorted(nums, reverse=True)[k - 1]

def s_merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out
def b_merge_intervals(intervals):
    pts = set()
    for s, e in intervals: pts.update(range(2 * s, 2 * e + 1))
    out = []; cur = None
    for p in sorted(pts):
        if cur and p == cur[1] + 1: cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[a // 2, b // 2] for a, b in out]

def s_insert_interval(intervals, new):
    out = []; i = 0; n = len(intervals); s, e = new
    while i < n and intervals[i][1] < s: out.append(list(intervals[i])); i += 1
    while i < n and intervals[i][0] <= e:
        s = min(s, intervals[i][0]); e = max(e, intervals[i][1]); i += 1
    out.append([s, e])
    while i < n: out.append(list(intervals[i])); i += 1
    return out
def b_insert_interval(intervals, new): return b_merge_intervals(list(map(list, intervals)) + [list(new)])

def s_meeting_rooms2(intervals):
    h = []; best = 0
    for s, e in sorted(intervals):
        if h and h[0] <= s: heapq.heapreplace(h, e)
        else: heapq.heappush(h, e)
    return len(h)
def s_meeting_rooms2_sweep(intervals):
    ev = sorted([(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals])   # -1 sorts before +1 at equal time
    cur = best = 0
    for t, d in ev: cur += d; best = max(best, cur)
    return best
def b_meeting_rooms2(intervals):
    ts = {s for s, e in intervals}
    return max((sum(s <= t < e for s, e in intervals) for t in ts), default=0)

def s_top_k_words(words, k):
    c = Counter(words)
    h = [(-n, w) for w, n in c.items()]; heapq.heapify(h)
    return [heapq.heappop(h)[1] for _ in range(k)]
def b_top_k_words(words, k):
    c = Counter(words)
    return sorted(c, key=lambda w: (-c[w], w))[:k]

def d2(p): return p[0] * p[0] + p[1] * p[1]
def s_k_closest(points, k):
    return [list(p) for p in heapq.nsmallest(k, points, key=d2)]
def ok_k_closest(kw, got):
    pts = kw['points']; k = kw['k']
    if len(got) != k: return False
    if Counter(map(tuple, got)) - Counter(map(tuple, pts)): return False
    return sorted(map(d2, got)) == sorted(map(d2, pts))[:k]

def s_merge_k_arrays(lists):
    h = [(l[0], i, 0) for i, l in enumerate(lists) if l]; heapq.heapify(h)
    out = []; peak = len(h)
    while h:
        v, i, j = heapq.heappop(h); out.append(v)
        if j + 1 < len(lists[i]): heapq.heappush(h, (lists[i][j + 1], i, j + 1))
        peak = max(peak, len(h))
    assert peak <= len(lists)
    return out
def b_merge_k_arrays(lists): return sorted(x for l in lists for x in l)

def s_task_scheduler(tasks, n):
    c = sorted(Counter(tasks).values(), reverse=True)
    mx = c[0]; cnt = c.count(mx)
    return max(len(tasks), (mx - 1) * (n + 1) + cnt)
def s_task_scheduler_heap(tasks, n):
    h = [-v for v in Counter(tasks).values()]; heapq.heapify(h)
    t = 0; q = deque()
    while h or q:
        t += 1
        while q and q[0][0] <= t: heapq.heappush(h, q.popleft()[1])
        if h:
            v = heapq.heappop(h) + 1
            if v: q.append((t + n + 1, v))
    return t
def b_task_scheduler(tasks, n):
    letters = sorted(set(tasks)); cnt = tuple(tasks.count(l) for l in letters)
    start = (cnt, tuple(0 for _ in letters)); seen = {start}; dq = deque([(start, 0)])
    while dq:
        (c, cool), t = dq.popleft()
        if not any(c): return t
        base = tuple(max(x - 1, 0) for x in cool)
        nxt = [(c, base)]
        for i in range(len(c)):
            if c[i] and cool[i] == 0:
                c2 = list(c); c2[i] -= 1; cl = list(base); cl[i] = n
                nxt.append((tuple(c2), tuple(cl)))
        for s in nxt:
            if s not in seen: seen.add(s); dq.append((s, t + 1))

def s_jump1(nums):
    far = 0
    for i, x in enumerate(nums):
        if i > far: return False
        far = max(far, i + x)
    return True
def b_jump1(nums):
    n = len(nums); ok = [False] * n; ok[0] = True
    for i in range(n):
        if ok[i]:
            for j in range(i + 1, min(n, i + nums[i] + 1)): ok[j] = True
    return ok[-1]

def s_jump2(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end: jumps += 1; end = far
    return jumps
def b_jump2(nums):
    n = len(nums); INF = 10 ** 9; d = [INF] * n; d[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)): d[j] = min(d[j], d[i] + 1)
    return d[-1]

def s_gas(gas, cost):
    if sum(gas) < sum(cost): return -1
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0: start = i + 1; tank = 0
    return start
def b_gas(gas, cost):
    n = len(gas)
    for s in range(n):
        t = 0; ok = True
        for k in range(n):
            i = (s + k) % n; t += gas[i] - cost[i]
            if t < 0: ok = False; break
        if ok: return s
    return -1

def s_reorganize(s):
    c = Counter(s); h = [(-v, ch) for ch, v in c.items()]; heapq.heapify(h)
    out = []; prev = None
    while h:
        v, ch = heapq.heappop(h); out.append(ch); v += 1
        if prev: heapq.heappush(h, prev); prev = None
        if v: prev = (v, ch)
    return ''.join(out) if len(out) == len(s) else ''
def ok_reorganize(kw, got):
    s = kw['s']
    if got == '': return not any(all(p[i] != p[i + 1] for i in range(len(p) - 1)) for p in set(itertools.permutations(s))) if len(s) <= 7 else max(Counter(s).values()) > (len(s) + 1) // 2
    return sorted(got) == sorted(s) and all(got[i] != got[i + 1] for i in range(len(got) - 1))

def s_non_overlap(intervals):
    cnt = 0; end = -10 ** 18
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if s >= end: end = e
        else: cnt += 1
    return cnt
def b_non_overlap(intervals):
    n = len(intervals); best = 0
    for m in range(1 << n):
        sel = [intervals[i] for i in range(n) if m >> i & 1]
        if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(sel, 2)): best = max(best, len(sel))
    return n - best

def s_median_stream(adds):
    lo = []; hi = []; out = []   # lo = max-heap (negated), hi = min-heap; len(lo) in (len(hi), len(hi)+1)
    for x in adds:
        heapq.heappush(lo, -x); heapq.heappush(hi, -heapq.heappop(lo))
        if len(hi) > len(lo): heapq.heappush(lo, -heapq.heappop(hi))
        assert len(lo) - len(hi) in (0, 1)
        out.append(float(-lo[0]) if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2)
    return out
def b_median_stream(adds):
    out = []
    for i in range(1, len(adds) + 1):
        a = sorted(adds[:i]); m = len(a)
        out.append(float(a[m // 2]) if m % 2 else (a[m // 2 - 1] + a[m // 2]) / 2)
    return out

# ---------- 2 stars
def s_last_stone(stones):
    h = [-x for x in stones]; heapq.heapify(h)
    while len(h) > 1:
        a = -heapq.heappop(h); b = -heapq.heappop(h)
        if a != b: heapq.heappush(h, -(a - b))
    return -h[0] if h else 0
def b_last_stone(stones):
    a = sorted(stones)
    while len(a) > 1:
        x = a.pop(); y = a.pop()
        if x != y: a.append(x - y); a.sort()
    return a[0] if a else 0

def s_cookies(g, s):
    g = sorted(g); s = sorted(s); i = 0
    for c in s:
        if i < len(g) and g[i] <= c: i += 1
    return i
def b_cookies(g, s):
    @lru_cache(None)
    def f(i, used):
        if i == len(g): return 0
        best = f(i + 1, used)
        for j in range(len(s)):
            if not used >> j & 1 and s[j] >= g[i]: best = max(best, 1 + f(i + 1, used | 1 << j))
        return best
    return f(0, 0)

def s_sticks(sticks):
    h = list(sticks); heapq.heapify(h); tot = 0
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h); tot += a + b; heapq.heappush(h, a + b)
    return tot
def b_sticks(sticks):
    @lru_cache(None)
    def f(t):
        if len(t) == 1: return 0
        best = 10 ** 18
        for i, j in itertools.combinations(range(len(t)), 2):
            r = [t[k] for k in range(len(t)) if k not in (i, j)] + [t[i] + t[j]]
            best = min(best, t[i] + t[j] + f(tuple(sorted(r))))
        return best
    return f(tuple(sorted(sticks)))

def s_balloons(points):
    cnt = 0; end = None
    for s, e in sorted(points, key=lambda p: p[1]):
        if end is None or s > end: cnt += 1; end = e
    return cnt
def b_balloons(points):
    lo = min(p[0] for p in points); hi = max(p[1] for p in points); xs = range(lo, hi + 1)
    for r in range(1, len(points) + 1):
        for comb in itertools.combinations(xs, r):
            if all(any(s <= x <= e for x in comb) for s, e in points): return r

def s_partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}; out = []; start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        if i == end: out.append(end - start + 1); start = i + 1
    return out
def b_partition_labels(s):
    n = len(s); best = None
    for m in range(1 << max(n - 1, 0)):
        cuts = [i + 1 for i in range(n - 1) if m >> i & 1]
        parts = [s[a:b] for a, b in zip([0] + cuts, cuts + [n])]
        if len({ch for p in parts for ch in p}) == sum(len(set(p)) for p in parts):
            if best is None or len(parts) > len(best): best = parts
    return [len(p) for p in best]

def s_queue(people):
    out = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])): out.insert(k, [h, k])
    return out
def pairs_of(queue):
    return [[h, sum(1 for x in queue[:i] if x >= h)] for i, h in enumerate(queue)]

def s_intersections(a, b):
    i = j = 0; out = []
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0]); hi = min(a[i][1], b[j][1])
        if lo <= hi: out.append([lo, hi])
        if a[i][1] < b[j][1]: i += 1
        else: j += 1
    return out
def b_intersections(a, b):
    pa = set(); pb = set()
    for s, e in a: pa.update(range(2 * s, 2 * e + 1))
    for s, e in b: pb.update(range(2 * s, 2 * e + 1))
    pts = sorted(pa & pb); out = []; cur = None
    for p in pts:
        if cur and p == cur[1] + 1: cur[1] = p
        else:
            if cur: out.append(cur)
            cur = [p, p]
    if cur: out.append(cur)
    return [[x // 2, y // 2] for x, y in out]

def s_max_events(events):
    ev = sorted(events); h = []; i = 0; day = 0; cnt = 0; n = len(ev)
    while i < n or h:
        if not h: day = max(day, ev[i][0])
        while i < n and ev[i][0] <= day: heapq.heappush(h, ev[i][1]); i += 1
        while h and h[0] < day: heapq.heappop(h)
        if h: heapq.heappop(h); cnt += 1; day += 1
    return cnt
def b_max_events(events):
    days = sorted({d for s, e in events for d in range(s, e + 1)})
    match = {}
    def try_(i, seen):
        for d in range(events[i][0], events[i][1] + 1):
            if d in seen: continue
            seen.add(d)
            if d not in match or try_(match[d], seen): match[d] = i; return True
        return False
    return sum(try_(i, set()) for i in range(len(events)))

def s_furthest(heights, bricks, ladders):
    h = []
    for i in range(len(heights) - 1):
        d = heights[i + 1] - heights[i]
        if d > 0:
            heapq.heappush(h, d)
            if len(h) > ladders:
                bricks -= heapq.heappop(h)
                if bricks < 0: return i
    return len(heights) - 1
def b_furthest(heights, bricks, ladders):
    best = 0
    def go(i, b, l):
        nonlocal best
        best = max(best, i)
        if i == len(heights) - 1: return
        d = heights[i + 1] - heights[i]
        if d <= 0: go(i + 1, b, l); return
        if b >= d: go(i + 1, b - d, l)
        if l > 0: go(i + 1, b, l - 1)
    go(0, bricks, ladders); return best

def s_k_pairs(nums1, nums2, k):
    if not nums1 or not nums2: return []
    h = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]; heapq.heapify(h); out = []
    while h and len(out) < k:
        _, i, j = heapq.heappop(h); out.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2): heapq.heappush(h, (nums1[i] + nums2[j + 1], i, j + 1))
    return out
def ok_k_pairs(kw, got):
    a, b, k = kw['nums1'], kw['nums2'], kw['k']
    allp = [(x, y) for x in a for y in b]
    if len(got) != k: return False
    if Counter(map(tuple, got)) - Counter(allp): return False
    return sorted(x + y for x, y in got) == sorted(x + y for x, y in allp)[:k]

def textbook_down(a, i, n, cnt):
    while True:
        l, r = 2 * i + 1, 2 * i + 2; m = i
        if l < n and a[l] < a[m]: m = l
        if r < n and a[r] < a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; cnt[0] += 1; i = m
def s_build_heap(vals):
    a = list(vals); n = len(a); c = [0]
    for i in range(n // 2 - 1, -1, -1): textbook_down(a, i, n, c)
    p = []; c2 = 0
    for v in vals:
        p.append(v); i = len(p) - 1
        while i > 0 and p[(i - 1) // 2] > p[i]:
            p[(i - 1) // 2], p[i] = p[i], p[(i - 1) // 2]; i = (i - 1) // 2; c2 += 1
    return [a, c[0], p, c2]
def is_heap(a): return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

def s_tie_break(tasks):
    h = []
    for cnt, (p, payload) in enumerate(tasks): heapq.heappush(h, (p, cnt, payload))
    return [heapq.heappop(h)[2]['id'] for _ in range(len(h))]
def b_tie_break(tasks):
    return [t[1]['id'] for t in sorted(tasks, key=lambda t: t[0])]   # sorted is stable

def s_custom_order(words, order):
    class Rev:
        __slots__ = ('w',)
        def __init__(s, w): s.w = w
        def __lt__(s, o): return s.w > o.w
    class LenRev:
        __slots__ = ('w',)
        def __init__(s, w): s.w = w
        def __lt__(s, o): return (len(s.w), s.w) > (len(o.w), o.w)
    C = Rev if order == 'lex_desc' else LenRev
    h = [C(w) for w in words]; heapq.heapify(h)
    return [heapq.heappop(h).w for _ in range(len(words))]
def b_custom_order(words, order):
    return sorted(words, reverse=True) if order == 'lex_desc' else sorted(words, key=lambda w: (len(w), w), reverse=True)

def s_lazy_pq(ops):
    h = []; dead = Counter(); live = 0; out = []; pushes = 0; pops = 0
    def clean():
        nonlocal pops
        while h and dead[h[0]]:
            dead[h[0]] -= 1; heapq.heappop(h); pops += 1
    present = Counter()
    for op in ops:
        if op[0] == 'push': heapq.heappush(h, op[1]); present[op[1]] += 1; live += 1; pushes += 1
        elif op[0] == 'remove':
            if present[op[1]] > 0: present[op[1]] -= 1; dead[op[1]] += 1; live -= 1; out.append(True)
            else: out.append(False)
        elif op[0] == 'pop':
            clean()
            if h: v = heapq.heappop(h); pops += 1; present[v] -= 1; live -= 1; out.append(v)
            else: out.append(None)
        elif op[0] == 'top':
            clean(); out.append(h[0] if h else None)
        else: out.append(live)
        assert len(h) <= pushes
    assert pops <= pushes
    return out
def b_lazy_pq(ops):
    a = []; out = []
    for op in ops:
        if op[0] == 'push': a.append(op[1])
        elif op[0] == 'remove':
            if op[1] in a: a.remove(op[1]); out.append(True)
            else: out.append(False)
        elif op[0] == 'pop':
            if a: m = min(a); a.remove(m); out.append(m)
            else: out.append(None)
        elif op[0] == 'top': out.append(min(a) if a else None)
        else: out.append(len(a))
    return out

def s_activity(activities):
    cnt = 0; end = -10 ** 18
    for s, e in sorted(activities, key=lambda a: a[1]):
        if s >= end: cnt += 1; end = e
    return cnt
def b_activity(activities):
    n = len(activities); best = 0
    for m in range(1 << n):
        sel = [activities[i] for i in range(n) if m >> i & 1]
        if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(sel, 2)): best = max(best, len(sel))
    return best
def greedy_by(activities, keyf):
    chosen = []
    for s, e in sorted(activities, key=keyf):
        if all(e <= c[0] or c[1] <= s for c in chosen): chosen.append([s, e])
    return len(chosen)

def coin_tables(coins, limit):
    INF = 10 ** 9; opt = [0] + [INF] * limit; gr = [0] * (limit + 1)
    for a in range(1, limit + 1):
        opt[a] = min(opt[a - c] + 1 for c in coins if c <= a)
        r = a; g = 0
        for c in reversed(coins): g += r // c; r %= c
        gr[a] = g
    return opt, gr
def s_coin_greedy(coins):
    limit = coins[-1] + (coins[-2] if len(coins) > 1 else 0)
    opt, gr = coin_tables(coins, limit)
    for a in range(1, limit + 1):
        if gr[a] > opt[a]: return a
    return -1
def b_coin_greedy(coins):
    opt, gr = coin_tables(coins, 200)
    for a in range(1, 201):
        if gr[a] > opt[a]: return a
    return -1

def s_candy(ratings):
    n = len(ratings); c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]: c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]: c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)
def b_candy(ratings):
    n = len(ratings); best = 10 ** 9
    for c in itertools.product(range(1, n + 1), repeat=n):
        if all((ratings[i + 1] <= ratings[i] or c[i + 1] > c[i]) and (ratings[i] <= ratings[i + 1] or c[i] > c[i + 1]) for i in range(n - 1)):
            best = min(best, sum(c))
    return best

def s_free_time(schedule):
    iv = sorted(x for emp in schedule for x in emp); out = []; end = iv[0][1]
    for s, e in iv[1:]:
        if s > end: out.append([end, s])
        end = max(end, e)
    return out
def b_free_time(schedule):
    iv = [x for emp in schedule for x in emp]
    lo = min(s for s, e in iv); hi = max(e for s, e in iv)
    free = [not any(s <= t and t + 1 <= e for s, e in iv) for t in range(lo, hi)]
    out = []; t = 0
    while t < len(free):
        if free[t]:
            u = t
            while u < len(free) and free[u]: u += 1
            out.append([lo + t, lo + u]); t = u
        else: t += 1
    return out

# ---------- 1 star
def s_quickselect(nums, k):
    seg = list(nums); rounds = 0
    while True:
        p = seg[0]; rounds += 1
        gt = [x for x in seg if x > p]; eq = [x for x in seg if x == p]; lt = [x for x in seg if x < p]
        if k <= len(gt): seg = gt
        elif k <= len(gt) + len(eq): return [p, rounds]
        else: k -= len(gt) + len(eq); seg = lt
def b_quickselect(nums, k): return sorted(nums, reverse=True)[k - 1]

def s_nlargest(records, k):
    return [r[0] for r in heapq.nlargest(k, records, key=lambda r: r[1])]
def b_nlargest(records, k):
    idx = sorted(range(len(records)), key=lambda i: (-records[i][1], i))
    return [records[i][0] for i in idx[:k]]

def s_pq_update(ops):
    h = []; cur = {}; stamp = 0; out = []; pushes = 0
    for op in ops:
        if op[0] in ('add', 'update'):
            stamp += 1; cur[op[1]] = (op[2], stamp); heapq.heappush(h, (op[2], stamp, op[1])); pushes += 1
        elif op[0] == 'remove':
            out.append(cur.pop(op[1], None) is not None)
        elif op[0] == 'pop':
            r = None
            while h:
                p, st, t = heapq.heappop(h)
                if cur.get(t) == (p, st): del cur[t]; r = t; break
            out.append(r)
        else: out.append(len(cur))
        assert len(h) <= pushes
    return out
def b_pq_update(ops):
    cur = {}; stamp = 0; out = []
    for op in ops:
        if op[0] in ('add', 'update'): stamp += 1; cur[op[1]] = (op[2], stamp)
        elif op[0] == 'remove': out.append(cur.pop(op[1], None) is not None)
        elif op[0] == 'pop':
            if cur: t = min(cur, key=lambda x: cur[x]); del cur[t]; out.append(t)
            else: out.append(None)
        else: out.append(len(cur))
    return out

def s_greedy_days(weights, cap):
    if max(weights) > cap: return -1
    days = 1; cur = 0
    for w in weights:
        if cur + w > cap: days += 1; cur = 0
        cur += w
    return days
def b_greedy_days(weights, cap):
    if max(weights) > cap: return -1
    n = len(weights); INF = 10 ** 9; d = [INF] * (n + 1); d[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            if sum(weights[j:i]) <= cap: d[i] = min(d[i], d[j] + 1)
    return d[n]

def s_huffman(freqs):
    n = len(freqs)
    if n == 1: return [0]
    h = [(f, i, [i]) for i, f in enumerate(freqs)]; heapq.heapify(h); L = [0] * n; nxt = n
    while len(h) > 1:
        f1, _, a = heapq.heappop(h); f2, _, b = heapq.heappop(h)
        for i in a + b: L[i] += 1
        heapq.heappush(h, (f1 + f2, nxt, a + b)); nxt += 1
    return L
def opt_cost(freqs):
    n = len(freqs); tot = [0] * (1 << n)
    for m in range(1, 1 << n): tot[m] = sum(freqs[i] for i in range(n) if m >> i & 1)
    @lru_cache(None)
    def f(m):
        if m & (m - 1) == 0: return 0
        best = 10 ** 18; sub = (m - 1) & m
        while sub:
            if sub < (m ^ sub) or True: best = min(best, f(sub) + f(m ^ sub) + tot[m])
            sub = (sub - 1) & m
        return best
    return f((1 << n) - 1)
def ok_huffman(kw, got):
    fr = kw['freqs']
    if len(got) != len(fr): return False
    if sum(2.0 ** -l for l in got) != 1.0: return False
    return sum(f * l for f, l in zip(fr, got)) == opt_cost(fr)

def s_sliding_median(nums, k):
    lo = []; hi = []; side = {}; dead = set(); lsz = hsz = 0; out = []
    def prune(h):
        while h and h[0][1] in dead: dead.discard(h[0][1]); heapq.heappop(h)
    for i, x in enumerate(nums):
        prune(lo)
        if lo and x <= -lo[0][0]: heapq.heappush(lo, (-x, i)); side[i] = 'lo'; lsz += 1
        else: heapq.heappush(hi, (x, i)); side[i] = 'hi'; hsz += 1
        if i >= k:
            j = i - k; dead.add(j)
            if side.pop(j) == 'lo': lsz -= 1
            else: hsz -= 1
        while lsz > (lsz + hsz + 1) // 2:
            prune(lo); v, j = heapq.heappop(lo); heapq.heappush(hi, (-v, j)); side[j] = 'hi'; lsz -= 1; hsz += 1
        while lsz < (lsz + hsz + 1) // 2:
            prune(hi); v, j = heapq.heappop(hi); heapq.heappush(lo, (-v, j)); side[j] = 'lo'; hsz -= 1; lsz += 1
        prune(lo); prune(hi)
        if i >= k - 1:
            out.append(float(-lo[0][0]) if k % 2 else (-lo[0][0] + hi[0][0]) / 2)
    return out
def b_sliding_median(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        a = sorted(nums[i:i + k]); out.append(float(a[k // 2]) if k % 2 else (a[k // 2 - 1] + a[k // 2]) / 2)
    return out

def s_rooms3(n, meetings):
    free = list(range(n)); heapq.heapify(free); busy = []; cnt = [0] * n
    for s, e in sorted(meetings):
        while busy and busy[0][0] <= s: heapq.heappush(free, heapq.heappop(busy)[1])
        if free: r = heapq.heappop(free); heapq.heappush(busy, (e, r))
        else:
            t, r = heapq.heappop(busy); heapq.heappush(busy, (t + e - s, r))
        cnt[r] += 1
    return cnt.index(max(cnt))
def b_rooms3(n, meetings):
    avail = [0] * n; cnt = [0] * n
    for s, e in sorted(meetings):
        free = [r for r in range(n) if avail[r] <= s]
        if free: r = free[0]; avail[r] = e
        else:
            t = min(avail); r = avail.index(t); avail[r] = t + e - s
        cnt[r] += 1
    return cnt.index(max(cnt))

def s_smallest_range(lists):
    h = [(l[0], i, 0) for i, l in enumerate(lists)]; heapq.heapify(h); hi = max(x[0] for x in h)
    best = [h[0][0], hi]
    while True:
        v, i, j = h[0]
        if hi - v < best[1] - best[0] or (hi - v == best[1] - best[0] and v < best[0]): best = [v, hi]
        if j + 1 == len(lists[i]): return best
        nv = lists[i][j + 1]; heapq.heapreplace(h, (nv, i, j + 1)); hi = max(hi, nv)
def b_smallest_range(lists):
    vals = sorted({x for l in lists for x in l}); best = None
    for a in vals:
        for b in vals:
            if b >= a and all(any(a <= x <= b for x in l) for l in lists):
                if best is None or (b - a, a) < (best[1] - best[0], best[0]): best = [a, b]
    return best

def s_ipo(k, w, profits, capital):
    ps = sorted(zip(capital, profits)); h = []; i = 0
    for _ in range(k):
        while i < len(ps) and ps[i][0] <= w: heapq.heappush(h, -ps[i][1]); i += 1
        if not h: break
        w -= heapq.heappop(h)
    return w
def b_ipo(k, w, profits, capital):
    best = w
    def go(w, used, left):
        nonlocal best
        best = max(best, w)
        if left == 0: return
        for i in range(len(profits)):
            if not used >> i & 1 and capital[i] <= w: go(w + profits[i], used | 1 << i, left - 1)
    go(w, 0, k); return best

def s_rearrange_k(s, k):
    if k <= 1: return s
    h = [(-v, ch) for ch, v in Counter(s).items()]; heapq.heapify(h); q = deque(); out = []
    while h:
        v, ch = heapq.heappop(h); out.append(ch); q.append((v + 1, ch))
        if len(q) >= k:
            v2, c2 = q.popleft()
            if v2: heapq.heappush(h, (v2, c2))
    return ''.join(out) if len(out) == len(s) else ''
def ok_rearrange_k(kw, got):
    s, k = kw['s'], kw['k']
    if got == '' and s != '':
        return not any(all(p[i] != p[j] for i in range(len(p)) for j in range(i + 1, min(len(p), i + k))) for p in set(itertools.permutations(s)))
    if sorted(got) != sorted(s): return False
    return all(got[i] != got[j] for i in range(len(got)) for j in range(i + 1, min(len(got), i + k)))

S = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('s_')}
OK = {'k_closest': ok_k_closest, 'reorganize': ok_reorganize, 'k_pairs': ok_k_pairs, 'huffman': ok_huffman, 'rearrange_k': ok_rearrange_k}
ALIAS = {'jump_game1': 'jump1', 'jump_game2': 'jump2', 'gas_station': 'gas', 'queue_reconstruct': 'queue', 'furthest_building': 'furthest',
         'activity_selection': 'activity', 'candy': 'candy'}
for _k, _v in ALIAS.items(): S[_k] = S[_v]
B = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('b_')}
for _k, _v in ALIAS.items():
    if _v in B: B[_k] = B[_v]
