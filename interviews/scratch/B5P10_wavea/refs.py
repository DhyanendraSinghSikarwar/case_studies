# Reference solutions (s_*) and independent brute-force / plain-recursion oracles (b_*) for Book 5 Part 10 (DP I).
import bisect, itertools, functools, sys
from functools import cache
INF = float('inf')
M = 10**9 + 7

# ---------------- 3 stars, easy
def s_climb(n):
    if n < 2: return 1
    a, b = 1, 1
    for _ in range(2, n + 1): a, b = b, (a + b) % M
    return b
def b_climb(n):
    def f(k): return 1 if k < 2 else f(k - 1) + f(k - 2)
    return f(n) % M
def s_min_cost_stairs(cost):
    n = len(cost); a = b = 0
    for i in range(2, n + 1): a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b
def b_min_cost_stairs(cost):
    n = len(cost)
    def g(i): return 0 if i >= n else cost[i] + min(g(i + 1), g(i + 2))
    return min(g(0), g(1))
def s_kadane(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x); best = max(best, cur)
    return best
def b_kadane(nums):
    return max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))
def s_stock_once(prices):
    hold, sold = -INF, 0
    for p in prices:
        hold = max(hold, -p); sold = max(sold, hold + p)
    return sold
def b_stock_once(prices):
    return max([0] + [prices[j] - prices[i] for i in range(len(prices)) for j in range(i + 1, len(prices))])

# ---------------- 3 stars, medium
def s_house_robber(nums):
    a = b = 0
    for x in nums: a, b = b, max(b, a + x)
    return b
def b_house_robber(nums):
    n = len(nums); best = 0
    for mask in range(1 << n):
        if mask & (mask >> 1): continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best
def s_coin_min(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]: dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]
def b_coin_min(coins, amount):
    def f(a):
        if a == 0: return 0
        best = INF
        for c in coins:
            if c <= a: best = min(best, 1 + f(a - c))
        return best
    r = f(amount); return -1 if r == INF else r
def s_lis_length(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return [len(tails), tails]
def b_lis_length(nums):
    best = {}
    n = len(nums)
    for L in range(1, n + 1):
        for comb in itertools.combinations(range(n), L):
            vals = [nums[i] for i in comb]
            if all(vals[i] < vals[i + 1] for i in range(L - 1)):
                best[L] = min(best.get(L, INF), vals[-1])
    ks = sorted(best)
    return [len(ks), [best[k] for k in ks]]
def s_word_break(s, word_dict):
    ws = set(word_dict); lens = sorted({len(w) for w in ws}); n = len(s)
    dp = [True] + [False] * n
    for i in range(1, n + 1):
        for L in lens:
            if L <= i and dp[i - L] and s[i - L:i] in ws: dp[i] = True; break
    return dp[n]
def b_word_break(s, word_dict):
    def f(i):
        if i == len(s): return True
        return any(s.startswith(w, i) and f(i + len(w)) for w in word_dict)
    return f(0)
def s_decode_ways(s):
    a, b = 1, 0 if s[0] == '0' else 1   # ways(0 chars), ways(1 char)
    for i in range(2, len(s) + 1):
        c = 0
        if s[i - 1] != '0': c += b
        if 10 <= int(s[i - 2:i]) <= 26: c += a
        a, b = b, c
    return b
def b_decode_ways(s):
    def f(i):
        if i == len(s): return 1
        if s[i] == '0': return 0
        r = f(i + 1)
        if i + 1 < len(s) and int(s[i:i + 2]) <= 26: r += f(i + 2)
        return r
    return f(0)
def s_coin_ways(coins, amount):
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1): dp[a] += dp[a - c]
    return dp[amount]
def b_coin_ways(coins, amount):
    def f(i, rem):
        if rem == 0: return 1
        if i == len(coins) or rem < 0: return 0
        return f(i, rem - coins[i]) + f(i + 1, rem)
    return f(0, amount)
def s_partition_equal(nums):
    t = sum(nums)
    if t % 2: return False
    bits = 1
    for x in nums: bits |= bits << x
    return bool(bits >> (t // 2) & 1)
def b_partition_equal(nums):
    t = sum(nums); n = len(nums)
    return any(2 * sum(nums[i] for i in range(n) if m >> i & 1) == t for m in range(1 << n))
def s_house_robber2(nums):
    if len(nums) == 1: return nums[0]
    return max(s_house_robber(nums[1:]), s_house_robber(nums[:-1]))
def b_house_robber2(nums):
    n = len(nums); best = 0
    for mask in range(1 << n):
        ok = all(not (mask >> i & 1 and mask >> ((i + 1) % n) & 1) for i in range(n) if (i + 1) % n != i)
        if ok: best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best
def s_max_product(nums):
    best = mx = mn = nums[0]
    for x in nums[1:]:
        c = (x, mx * x, mn * x); mx, mn = max(c), min(c); best = max(best, mx)
    return best
def b_max_product(nums):
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)): p *= nums[j]; best = max(best, p)
    return best

# ---------------- 2 stars
def s_fib_three(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    fib = a
    f1 = 1; f2 = 1   # naive calls: c(0)=c(1)=1, c(k)=1+c(k-1)+c(k-2)
    c0, c1 = 1, 1
    for _ in range(n - 1): c0, c1 = c1, 1 + c0 + c1
    naive = 1 if n < 2 else c1
    memo = 1 if n == 0 else 2 * n - 1
    return [fib, naive, memo]
def b_fib_three(n):
    cnt = [0]
    def f(k):
        cnt[0] += 1
        return k if k < 2 else f(k - 1) + f(k - 2)
    v = f(n); naive = cnt[0]
    cnt[0] = 0; memo = {}
    def g(k):
        cnt[0] += 1
        if k < 2: return k
        if k in memo: return memo[k]
        memo[k] = g(k - 1) + g(k - 2); return memo[k]
    g(n)
    return [v, naive, cnt[0]]
def s_paint_fence(n, k):
    same, diff = 0, k
    for _ in range(2, n + 1): same, diff = diff, (same + diff) * (k - 1) % M
    return (same + diff) % M
def b_paint_fence(n, k):
    c = 0
    for col in itertools.product(range(k), repeat=n):
        if all(not (col[i] == col[i + 1] == col[i + 2]) for i in range(n - 2)): c += 1
    return c % M
def s_perfect_squares(n):
    dp = [0] + [INF] * n
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            if dp[i - j * j] + 1 < dp[i]: dp[i] = dp[i - j * j] + 1
            j += 1
    return dp[n]
def b_perfect_squares(n):
    def f(m):
        if m == 0: return 0
        return 1 + min(f(m - j * j) for j in range(1, int(m ** .5) + 1))
    return f(n)
def s_knapsack01(weights, values, cap):
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1): dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]
def b_knapsack01(weights, values, cap):
    n = len(weights); best = 0
    for m in range(1 << n):
        if sum(weights[i] for i in range(n) if m >> i & 1) <= cap: best = max(best, sum(values[i] for i in range(n) if m >> i & 1))
    return best
def knapsack_forward(weights, values, cap):   # the buggy upward loop
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1): dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]
def s_subset_sum(nums, target):
    dp = [True] + [False] * target
    for x in nums:
        for t in range(target, x - 1, -1):
            if dp[t - x]: dp[t] = True
    return dp[target]
def subset_sum_bitset(nums, target):
    bits = 1
    for x in nums: bits |= bits << x
    return bool(bits >> target & 1)
def b_subset_sum(nums, target):
    n = len(nums); return any(sum(nums[i] for i in range(n) if m >> i & 1) == target for m in range(1 << n))
def s_target_sum(nums, target):
    t = sum(nums)
    if abs(target) > t or (t + target) % 2: return 0
    need = (t + target) // 2; dp = [1] + [0] * need
    for x in nums:
        for w in range(need, x - 1, -1): dp[w] += dp[w - x]
    return dp[need]
def b_target_sum(nums, target):
    return sum(1 for signs in itertools.product((1, -1), repeat=len(nums)) if sum(s * x for s, x in zip(signs, nums)) == target)
def s_unbounded_knapsack(weights, values, cap):
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        for w, v in zip(weights, values):
            if w <= c and dp[c - w] + v > dp[c]: dp[c] = dp[c - w] + v
    return dp[cap]
def b_unbounded_knapsack(weights, values, cap):
    def f(c): return max([0] + [f(c - w) + v for w, v in zip(weights, values) if w <= c])
    return f(cap)
def s_comb_sum4(nums, target):
    o = [1] + [0] * target
    for t in range(1, target + 1):
        for x in nums:
            if x <= t: o[t] += o[t - x]
    u = [1] + [0] * target
    for x in nums:
        for t in range(x, target + 1): u[t] += u[t - x]
    return [o[target], u[target]]
def b_comb_sum4(nums, target):
    def seqs(rem):
        if rem == 0: return 1
        return sum(seqs(rem - x) for x in nums if x <= rem)
    def combos(i, rem):
        if rem == 0: return 1
        if i == len(nums) or rem < 0: return 0
        return combos(i, rem - nums[i]) + combos(i + 1, rem)
    return [seqs(target), combos(0, target)]
def comb_wrong_order(nums, target):   # coin loop outer for ordered count (counts combinations) -- the classic swap
    dp = [1] + [0] * target
    for x in nums:
        for t in range(x, target + 1): dp[t] += dp[t - x]
    return dp[target]
def s_kadane_idx(nums):
    P = [0]
    for x in nums: P.append(P[-1] + x)
    best = None; mn = INF; mn_i = 0
    for r in range(len(nums)):
        if P[r] < mn: mn, mn_i = P[r], r
        s = P[r + 1] - mn
        if best is None or s > best[0] or (s == best[0] and mn_i < best[1]): best = (s, mn_i, r)
    return list(best)
def b_kadane_idx(nums):
    c = [(-sum(nums[l:r + 1]), l, r) for l in range(len(nums)) for r in range(l, len(nums))]
    s, l, r = min(c); return [-s, l, r]
def s_coin_recon(coins, amount):
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]: dp[a] = dp[a - c] + 1
    if dp[amount] == INF: return None
    out = []; a = amount; cs = sorted(coins)
    while a:
        for c in cs:
            if c <= a and dp[a - c] == dp[a] - 1: out.append(c); a -= c; break
    return out
def b_coin_recon(coins, amount):
    best = []
    def rec(i, rem, cur):
        if rem == 0: best.append(list(cur)); return
        if i == len(coins) or rem < 0: return
        k = 0
        while k * coins[i] <= rem:
            rec(i + 1, rem - k * coins[i], cur + [coins[i]] * k); k += 1
    cs = sorted(coins); coins_ = cs
    def rec2(i, rem, cur):
        if rem == 0: best.append(list(cur)); return
        if i == len(cs): return
        k = 0
        while k * cs[i] <= rem:
            rec2(i + 1, rem - k * cs[i], cur + [cs[i]] * k); k += 1
    rec2(0, amount, [])
    if not best: return None
    m = min(len(b) for b in best); return min(b for b in best if len(b) == m)
def s_jump_dp(nums):
    n = len(nums); R = 0; i = 0
    while i <= R and i < n:
        R = max(R, i + nums[i]); i += 1
    return [R >= n - 1, min(R, n - 1) + 1]
def b_jump_dp(nums):
    n = len(nums); seen = {0}; st = [0]
    while st:
        i = st.pop()
        for j in range(i + 1, min(n - 1, i + nums[i]) + 1):
            if j not in seen: seen.add(j); st.append(j)
    return [n - 1 in seen, len(seen)]
def s_stock_cooldown(prices):
    hold, sold, rest = -INF, -INF, 0
    for p in prices: hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)
def b_stock_cooldown(prices):
    n = len(prices)
    def f(i, holding):
        if i >= n: return 0
        best = f(i + 1, holding)
        if holding: best = max(best, prices[i] + f(i + 2, False))   # day i + 1 is the cooldown day
        else: best = max(best, -prices[i] + f(i + 1, True))
        return best
    return f(0, False)
def s_circular_kadane(nums):
    mx = cur = nums[0]; mn = curm = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x); mx = max(mx, cur); curm = min(x, curm + x); mn = min(mn, curm)
    return mx if mx < 0 else max(mx, sum(nums) - mn)
def b_circular_kadane(nums):
    n = len(nums); best = -INF
    for s in range(n):
        for L in range(1, n + 1): best = max(best, sum(nums[(s + k) % n] for k in range(L)))
    return best
def s_delete_earn(nums):
    if not nums: return 0
    tot = [0] * (max(nums) + 1)
    for x in nums: tot[x] += x
    a = b = 0
    for v in tot: a, b = b, max(b, a + v)
    return b
def b_delete_earn(nums):
    from collections import Counter
    c = Counter(nums); vals = sorted(c); best = 0
    for m in range(1 << len(vals)):
        ch = [vals[i] for i in range(len(vals)) if m >> i & 1]
        if all(ch[i + 1] - ch[i] > 1 for i in range(len(ch) - 1)): best = max(best, sum(v * c[v] for v in ch))
    return best

# ---------------- 2 stars, hard
def s_count_lis(nums):
    n = len(nums)
    if n == 0: return [0, 0]
    ln = [1] * n; ct = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if ln[j] + 1 > ln[i]: ln[i], ct[i] = ln[j] + 1, ct[j]
                elif ln[j] + 1 == ln[i]: ct[i] += ct[j]
    L = max(ln); return [L, sum(c for l, c in zip(ln, ct) if l == L)]
def b_count_lis(nums):
    n = len(nums); best = 0; cnt = 0
    for m in range(1 << n):
        v = [nums[i] for i in range(n) if m >> i & 1]
        if all(v[i] < v[i + 1] for i in range(len(v) - 1)):
            if len(v) > best: best, cnt = len(v), 1
            elif len(v) == best: cnt += 1
    return [best, cnt] if n else [0, 0]
def s_stock_k(k, prices):
    n = len(prices)
    if n < 2 or k == 0: return 0
    if k >= n // 2: return sum(max(0, prices[i + 1] - prices[i]) for i in range(n - 1))
    buy = [-INF] * (k + 1); sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p); sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
def stock_k_dp_full(k, prices):   # no shortcut, k capped only by n (memory O(k)) for the equivalence claim
    n = len(prices); k = min(k, n)
    if n < 2 or k == 0: return 0
    buy = [-INF] * (k + 1); sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p); sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
def b_stock_k(k, prices):
    n = len(prices)
    def f(i, t, hold):
        if i == n: return 0
        best = f(i + 1, t, hold)
        if hold: best = max(best, prices[i] + f(i + 1, t, 0))
        elif t > 0: best = max(best, -prices[i] + f(i + 1, t - 1, 1))
        return best
    return f(0, k, 0)
def s_last_stone2(stones):
    t = sum(stones); bits = 1
    for x in stones: bits |= bits << x
    h = t // 2
    while not bits >> h & 1: h -= 1
    return t - 2 * h
def b_last_stone2(stones):
    @cache
    def f(state):
        if len(state) <= 1: return state[0] if state else 0
        best = INF
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                rest = list(state[:i] + state[i + 1:j] + state[j + 1:]); d = state[j] - state[i]
                if d: rest.append(d)
                best = min(best, f(tuple(sorted(rest))))
        return best
    return f(tuple(sorted(stones)))

# ---------------- 1 star
def s_ones_zeroes(strs, m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for s in strs:
        z = s.count('0'); o = len(s) - z
        for a in range(m, z - 1, -1):
            for b in range(n, o - 1, -1): dp[a][b] = max(dp[a][b], dp[a - z][b - o] + 1)
    return dp[m][n]
def b_ones_zeroes(strs, m, n):
    k = len(strs); best = 0
    for mask in range(1 << k):
        ch = [strs[i] for i in range(k) if mask >> i & 1]
        if sum(s.count('0') for s in ch) <= m and sum(s.count('1') for s in ch) <= n: best = max(best, len(ch))
    return best
def s_alias_trap(m, n, ops):
    bug = [[0] * n] * m; ok = [[0] * n for _ in range(m)]
    for r, c, v in ops: bug[r][c] = v; ok[r][c] = v
    return [bug, ok, len({id(r) for r in bug}), len({id(r) for r in ok})]
def b_alias_trap(m, n, ops):
    bug = [[0] * n] * m; ok = [[0] * n for _ in range(m)]
    for r, c, v in ops:
        for rr in range(m): bug[rr][c] = v   # every row is the same object: writing one cell writes the column in all rows
        ok[r][c] = v
    return [bug, ok, 1, m]
def s_lru_mutable(nums, target):
    ns = tuple(nums); n = len(ns)
    @cache
    def f(i, rem):
        if i == n: return 1 if rem == 0 else 0
        return f(i + 1, rem) + f(i + 1, rem - ns[i])
    a = f(0, target); info = f.cache_info(); f.cache_clear()
    return [a, info.hits, info.misses, f.cache_info().currsize]
def b_lru_mutable(nums, target):
    n = len(nums); memo = {}; hits = misses = 0
    def f(i, rem):
        nonlocal hits, misses
        if (i, rem) in memo: hits += 1; return memo[(i, rem)]
        misses += 1
        v = (1 if rem == 0 else 0) if i == n else f(i + 1, rem) + f(i + 1, rem - nums[i])
        memo[(i, rem)] = v; return v
    a = f(0, target); return [a, hits, misses, 0]
def s_recursion_limit(n):
    a, b, c = 1, 1, 2
    if n == 0: v = 1
    elif n == 1: v = 1
    elif n == 2: v = 2
    else:
        w = [1, 1, 2]
        for _ in range(3, n + 1): w = [w[1], w[2], (w[0] + w[1] + w[2]) % M]
        v = w[2]
    return [v, 'ok' if n <= 500 else 'RecursionError']
def b_recursion_limit(n):
    @cache
    def f(k):
        if k < 0: return 0
        if k == 0: return 1
        return (f(k - 1) + f(k - 2) + f(k - 3)) % M
    try: return [f(n), 'ok']
    except RecursionError: return [None, 'RecursionError']
def b_recursion_limit_cmp(got, b):   # the oracle only knows the value when it did not raise
    return got[1] == b[1] and (b[0] is None or got[0] == b[0])
def lis_len_dp(nums):
    n = len(nums); f = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] > nums[i]: f[i] = max(f[i], 1 + f[j])
    return f
def s_lis_recon(nums):
    n = len(nums)
    if not n: return []
    f = lis_len_dp(nums); L = max(f); out = []; need = L; last = None
    for i in range(n):
        if f[i] == need and (last is None or nums[i] > last): out.append(nums[i]); last = nums[i]; need -= 1
        if need == 0: break
    return out
def b_lis_recon(nums):
    n = len(nums); best = []
    for L in range(n, 0, -1):
        cand = [c for c in itertools.combinations(range(n), L) if all(nums[c[i]] < nums[c[i + 1]] for i in range(L - 1))]
        if cand: return [nums[i] for i in min(cand)]
    return []
def s_lnds_tails(nums):
    t = []; s = []
    for x in nums:
        i = bisect.bisect_right(t, x)
        if i == len(t): t.append(x)
        else: t[i] = x
        j = bisect.bisect_left(s, x)
        if j == len(s): s.append(x)
        else: s[j] = x
    return [len(t), t, len(s)]
def lnds_wrong(nums):   # bisect_left used for the non-decreasing variant
    t = []
    for x in nums:
        i = bisect.bisect_left(t, x)
        if i == len(t): t.append(x)
        else: t[i] = x
    return len(t)
def b_lnds_tails(nums):
    n = len(nums); bn = {}; bs = {}
    for L in range(1, n + 1):
        for c in itertools.combinations(range(n), L):
            v = [nums[i] for i in c]
            if all(v[i] <= v[i + 1] for i in range(L - 1)): bn[L] = min(bn.get(L, INF), v[-1])
            if all(v[i] < v[i + 1] for i in range(L - 1)): bs[L] = min(bs.get(L, INF), v[-1])
    return [len(bn), [bn[k] for k in sorted(bn)], len(bs)]
def s_russian_doll(envelopes):
    es = sorted(envelopes, key=lambda e: (e[0], -e[1])); t = []
    for _, h in es:
        i = bisect.bisect_left(t, h)
        if i == len(t): t.append(h)
        else: t[i] = h
    return len(t)
def b_russian_doll(envelopes):
    es = sorted(envelopes); n = len(es); dp = [1] * n
    for i in range(n):
        for j in range(i):
            if es[j][0] < es[i][0] and es[j][1] < es[i][1]: dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)
def s_dice_rolls(n, k, target):
    dp = [1] + [0] * target
    for _ in range(n):
        nd = [0] * (target + 1)
        for t in range(target + 1):
            if dp[t]:
                for f in range(1, k + 1):
                    if t + f <= target: nd[t + f] = (nd[t + f] + dp[t]) % M
        dp = nd
    return dp[target]
def b_dice_rolls(n, k, target):
    return sum(1 for r in itertools.product(range(1, k + 1), repeat=n) if sum(r) == target) % M
def s_knapsack_recon(weights, values, cap):
    n = len(weights)
    f = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for w in range(cap + 1):
            f[i][w] = f[i + 1][w]
            if weights[i] <= w: f[i][w] = max(f[i][w], values[i] + f[i + 1][w - weights[i]])
    out = []; w = cap
    for i in range(n):
        if f[i][w] == 0: break
        if weights[i] <= w and values[i] + f[i + 1][w - weights[i]] == f[i][w]: out.append(i); w -= weights[i]
    return [f[0][cap], out]
def b_knapsack_recon(weights, values, cap):
    n = len(weights); best = (-1, None)
    cands = []
    for L in range(n + 1):
        for c in itertools.combinations(range(n), L):
            if sum(weights[i] for i in c) <= cap: cands.append((sum(values[i] for i in c), list(c)))
    mv = max(v for v, _ in cands)
    return [mv, min(c for v, c in cands if v == mv)]
def s_min_cost_tickets(days, costs):
    ds = set(days); last = days[-1] if days else 0; dp = [0] * (last + 1)
    for d in range(1, last + 1):
        if d not in ds: dp[d] = dp[d - 1]
        else: dp[d] = min(dp[max(0, d - 1)] + costs[0], dp[max(0, d - 7)] + costs[1], dp[max(0, d - 30)] + costs[2])
    return dp[last]
def b_min_cost_tickets(days, costs):
    n = len(days)
    def f(i):
        if i >= n: return 0
        best = INF
        for span, c in zip((1, 7, 30), costs):
            j = i
            while j < n and days[j] < days[i] + span: j += 1
            best = min(best, c + f(j))
        return best
    return f(0)

S = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('s_')}
B = {k[2:]: v for k, v in dict(globals()).items() if k.startswith('b_') and not k.endswith('_cmp')}
CMP = {'recursion_limit': b_recursion_limit_cmp}
