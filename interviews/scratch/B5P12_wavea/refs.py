# Reference solutions (S) and independent oracles (B) for Book 5 Part 12 (backtracking, tries, bit manipulation, DS-flavoured).
import itertools, functools, sys, re, math, random, collections
sys.setrecursionlimit(1000)
S = {}; B = {}
def reg(d, name):
    def deco(f): d[name] = f; return f
    return deco
M32 = 0xFFFFFFFF

# ============ bit manipulation
@reg(S, 'single_number')
def _(nums):
    r = 0
    for x in nums: r ^= x
    return r
@reg(B, 'single_number')
def _(nums): return [k for k, v in collections.Counter(nums).items() if v == 1][0]

@reg(S, 'count_set_bits')
def _(n):
    c = 0; naive = 0; m = n
    while m: naive += 1; m >>= 1
    m = n
    while m: m &= m - 1; c += 1
    return [c, naive, c]
@reg(B, 'count_set_bits')
def _(n): return [bin(n).count('1'), len(bin(n)) - 2 if n else 0, bin(n).count('1')]

@reg(S, 'power_two_four')
def _(n):
    p2 = n > 0 and n & (n - 1) == 0
    return [p2, p2 and (n & 0x55555555) != 0]
@reg(B, 'power_two_four')
def _(n): return [n in {2 ** i for i in range(31)}, n in {4 ** i for i in range(16)}]

@reg(S, 'hamming')
def _(x, y, nums):
    d = bin(x ^ y).count('1'); tot = 0; m = len(nums)
    for b in range(31):
        ones = sum((v >> b) & 1 for v in nums); tot += ones * (m - ones)
    return [d, tot]
@reg(B, 'hamming')
def _(x, y, nums):
    h = lambda a, b: sum(1 for i in range(31) if ((a >> i) & 1) != ((b >> i) & 1))
    return [h(x, y), sum(h(a, b) for a, b in itertools.combinations(nums, 2))]

@reg(S, 'dup_missing')
def _(nums):
    x = 0
    for i, v in enumerate(nums, 1): x ^= i ^ v          # x = dup ^ missing
    low = x & -x; a = 0; b = 0
    for i, v in enumerate(nums, 1):
        if i & low: a ^= i
        else: b ^= i
        if v & low: a ^= v
        else: b ^= v
    return [a, b] if a in nums and nums.count(a) == 2 else [b, a]
@reg(B, 'dup_missing')
def _(nums):
    c = collections.Counter(nums); n = len(nums)
    return [[k for k, v in c.items() if v == 2][0], [i for i in range(1, n + 1) if i not in c][0]]

@reg(S, 'single_number_iii')
def _(nums):
    x = 0
    for v in nums: x ^= v
    low = x & -x; a = 0
    for v in nums:
        if v & low: a ^= v
    return sorted([a, x ^ a])
@reg(B, 'single_number_iii')
def _(nums): return sorted(k for k, v in collections.Counter(nums).items() if v == 1)

@reg(S, 'reverse_bits')
def _(n):
    n &= M32; r = 0
    for _i in range(32): r = (r << 1) | (n & 1); n >>= 1
    return r
@reg(B, 'reverse_bits')
def _(n): return int(format(n & M32, '032b')[::-1], 2)

@reg(S, 'single_number_ii')
def _(nums):
    r = 0
    for b in range(32):
        if sum((v >> b) & 1 for v in nums) % 3: r |= 1 << b
    return r - (1 << 32) if r >= 1 << 31 else r
@reg(B, 'single_number_ii')
def _(nums): return [k for k, v in collections.Counter(nums).items() if v == 1][0]

@reg(S, 'sum_two')
def _(a, b):
    a &= M32; b &= M32; rounds = 0
    while b:
        a, b = (a ^ b) & M32, ((a & b) << 1) & M32; rounds += 1
    return [a if a <= 0x7FFFFFFF else ~(a ^ M32), rounds]
@reg(B, 'sum_two')
def _(a, b):
    # independent: simulate with explicit 32-bit two's complement digits (ripple carry adder)
    ba = [(a >> i) & 1 for i in range(32)]; bb = [(b >> i) & 1 for i in range(32)]; c = 0; out = 0
    for i in range(32):
        s = ba[i] ^ bb[i] ^ c; c = (ba[i] & bb[i]) | (c & (ba[i] ^ bb[i])); out |= s << i
    return [out - (1 << 32) if out >> 31 else out, None]

@reg(S, 'bitmask_enum')
def _(items, target):
    n = len(items); res = []
    for mask in range(1 << n):
        if sum(items[i] for i in range(n) if mask >> i & 1) == target:
            res.append([items[i] for i in range(n) if mask >> i & 1])
    pairs = 0
    for mask in range(1 << n):
        sub = mask
        while sub: pairs += 1; sub = (sub - 1) & mask
    return [res, pairs]
@reg(B, 'bitmask_enum')
def _(items, target):
    n = len(items); res = []
    for mask in range(1 << n):
        sel = [items[i] for i in range(n) if (mask >> i) % 2 == 1]
        if sum(sel) == target: res.append(sel)
    pairs = sum(1 for m in range(1 << n) for s in range(1, 1 << n) if s & m == s)
    return [res, pairs]

# ============ backtracking
@reg(S, 'subsets')
def _(nums):
    out = []; cur = []
    def go(i):
        if i == len(nums): out.append(cur[:]); return
        go(i + 1); cur.append(nums[i]); go(i + 1); cur.pop()
    go(0); return sorted(out)
@reg(B, 'subsets')
def _(nums):
    n = len(nums); return sorted([nums[i] for i in range(n) if m >> i & 1] for m in range(1 << n))

@reg(S, 'subsets_dup')
def _(nums):
    a = sorted(nums); out = []; cur = []
    def go(start):
        out.append(cur[:])
        for i in range(start, len(a)):
            if i > start and a[i] == a[i - 1]: continue
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0); return sorted(out)
@reg(B, 'subsets_dup')
def _(nums):
    n = len(nums); return sorted(map(list, {tuple(sorted(nums[i] for i in range(n) if m >> i & 1)) for m in range(1 << n)}))

@reg(S, 'permutations')
def _(nums):
    out = []; used = [False] * len(nums); cur = []
    a = sorted(nums)
    def go():
        if len(cur) == len(a): out.append(cur[:]); return
        for i in range(len(a)):
            if used[i]: continue
            used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go(); return out
@reg(B, 'permutations')
def _(nums): return sorted(map(list, itertools.permutations(nums)))

@reg(S, 'permutations_dup')
def _(nums):
    a = sorted(nums); out = []; used = [False] * len(a); cur = []
    def go():
        if len(cur) == len(a): out.append(cur[:]); return
        for i in range(len(a)):
            if used[i] or (i and a[i] == a[i - 1] and not used[i - 1]): continue
            used[i] = True; cur.append(a[i]); go(); cur.pop(); used[i] = False
    go(); return out
@reg(B, 'permutations_dup')
def _(nums): return sorted(map(list, set(itertools.permutations(nums))))

@reg(S, 'combinations')
def _(n, k):
    out = []; cur = []
    def go(start):
        if len(cur) == k: out.append(cur[:]); return
        for v in range(start, n - (k - len(cur)) + 2):
            cur.append(v); go(v + 1); cur.pop()
    go(1); return out
@reg(B, 'combinations')
def _(n, k): return sorted(map(list, itertools.combinations(range(1, n + 1), k)))

@reg(S, 'comb_sum')
def _(candidates, target):
    c = sorted(candidates); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            cur.append(c[j]); go(j, rem - c[j]); cur.pop()
    go(0, target); return sorted(out)
@reg(B, 'comb_sum')
def _(candidates, target):
    res = set()
    for L in range(1, target // min(candidates) + 1):
        for t in itertools.combinations_with_replacement(sorted(candidates), L):
            if sum(t) == target: res.add(t)
    return sorted(map(list, res))

@reg(S, 'comb_sum2')
def _(candidates, target):
    c = sorted(candidates); out = []; cur = []
    def go(start, rem):
        if rem == 0: out.append(cur[:]); return
        for j in range(start, len(c)):
            if c[j] > rem: break
            if j > start and c[j] == c[j - 1]: continue
            cur.append(c[j]); go(j + 1, rem - c[j]); cur.pop()
    go(0, target); return sorted(out)
@reg(B, 'comb_sum2')
def _(candidates, target):
    n = len(candidates)
    return sorted(map(list, {tuple(sorted(candidates[i] for i in range(n) if m >> i & 1)) for m in range(1, 1 << n)
                             if sum(candidates[i] for i in range(n) if m >> i & 1) == target}))

@reg(S, 'gen_parens')
def _(n):
    out = []
    def go(cur, o, c):
        if len(cur) == 2 * n: out.append(''.join(cur)); return
        if o < n: cur.append('('); go(cur, o + 1, c); cur.pop()
        if c < o: cur.append(')'); go(cur, o, c + 1); cur.pop()
    go([], 0, 0); return sorted(out)
@reg(B, 'gen_parens')
def _(n):
    def ok(s):
        d = 0
        for ch in s:
            d += 1 if ch == '(' else -1
            if d < 0: return False
        return d == 0
    return sorted(s for s in map(''.join, itertools.product('()', repeat=2 * n)) if ok(s))

KEYS = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
@reg(S, 'letter_combos')
def _(digits):
    if not digits: return []
    out = []; cur = []
    def go(i):
        if i == len(digits): out.append(''.join(cur)); return
        for ch in KEYS[digits[i]]: cur.append(ch); go(i + 1); cur.pop()
    go(0); return out
@reg(B, 'letter_combos')
def _(digits):
    if not digits: return []
    return sorted(''.join(t) for t in itertools.product(*[KEYS[d] for d in digits]))

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
@reg(S, 'word_search')
def _(board, word):
    R, C = len(board), len(board[0]); g = [list(r) for r in board]
    def go(r, c, k):
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1): g[r][c] = word[k]; return True
        g[r][c] = word[k]; return False
    return any(go(r, c, 0) for r in range(R) for c in range(C))
@reg(B, 'word_search')
def _(board, word):
    R, C = len(board), len(board[0])
    def paths(path):   # immutable visited tuple
        k = len(path)
        if k == len(word): return True
        r, c = path[-1]
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in path and board[nr][nc] == word[k] and paths(path + ((nr, nc),)): return True
        return False
    return any(board[r][c] == word[0] and paths(((r, c),)) for r in range(R) for c in range(C))

@reg(S, 'nqueens')
def _(n):
    out = []; cols = []; cs = set(); d1 = set(); d2 = set()
    def go(r):
        if r == n: out.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in cols]); return
        for c in range(n):
            if c in cs or r - c in d1 or r + c in d2: continue
            cs.add(c); d1.add(r - c); d2.add(r + c); cols.append(c)
            go(r + 1)
            cols.pop(); cs.discard(c); d1.discard(r - c); d2.discard(r + c)
    go(0); return out
@reg(B, 'nqueens')
def _(n):
    res = []
    for p in itertools.permutations(range(n)):
        if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            res.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in p])
    return res   # permutations come in lexicographic order of the column tuple

@reg(S, 'word_search2')
def _(board, words):
    R, C = len(board), len(board[0]); root = {}
    for w in words:
        nd = root
        for ch in w: nd = nd.setdefault(ch, {})
        nd['$'] = w
    found = set(); g = [list(r) for r in board]
    def go(r, c, nd):
        ch = g[r][c]
        nxt = nd.get(ch)
        if nxt is None: return
        if '$' in nxt: found.add(nxt['$'])
        g[r][c] = '#'
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] != '#': go(nr, nc, nxt)
        g[r][c] = ch
    for r in range(R):
        for c in range(C): go(r, c, root)
    return sorted(found)
@reg(B, 'word_search2')
def _(board, words): return sorted(w for w in words if B['word_search'](board, w))

def _sud_ok(board):
    for i in range(9):
        for grp in ([board[i][j] for j in range(9)], [board[j][i] for j in range(9)],
                    [board[3 * (i // 3) + j // 3][3 * (i % 3) + j % 3] for j in range(9)]):
            d = [x for x in grp if x != '.']
            if len(d) != len(set(d)): return False
    return True
@reg(S, 'sudoku')
def _(board):
    g = [[0 if ch == '.' else int(ch) for ch in row] for row in board]
    rows = [0] * 9; cols = [0] * 9; box = [0] * 9; empties = []
    for r in range(9):
        for c in range(9):
            if g[r][c]:
                b = 1 << g[r][c]; rows[r] |= b; cols[c] |= b; box[r // 3 * 3 + c // 3] |= b
            else: empties.append((r, c))
    def solve():
        if not empties: return True
        best = -1; bm = 0; bc = 99
        for idx, (r, c) in enumerate(empties):           # most constrained cell first
            m = ~(rows[r] | cols[c] | box[r // 3 * 3 + c // 3]) & 0x3FE
            k = bin(m).count('1')
            if k < bc: best, bm, bc = idx, m, k
            if k == 0: return False
        empties[best], empties[-1] = empties[-1], empties[best]
        r, c = empties.pop(); bi = r // 3 * 3 + c // 3
        while bm:
            low = bm & -bm; bm ^= low; v = low.bit_length() - 1
            g[r][c] = v; rows[r] |= low; cols[c] |= low; box[bi] |= low
            if solve(): return True
            rows[r] ^= low; cols[c] ^= low; box[bi] ^= low; g[r][c] = 0
        empties.append((r, c)); empties[best], empties[-1] = empties[-1], empties[best]
        return False
    assert solve()
    return [''.join(map(str, row)) for row in g]
def sudoku_count(board, limit=2):
    """plain cell-by-cell solver counting solutions (independent of the MRV/bitmask reference)."""
    g = [list(r) for r in board]; cnt = 0
    def ok(r, c, ch):
        for k in range(9):
            if g[r][k] == ch or g[k][c] == ch: return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        nonlocal cnt
        if cnt >= limit: return
        while pos < 81 and g[pos // 9][pos % 9] != '.': pos += 1
        if pos == 81: cnt += 1; return
        r, c = divmod(pos, 9)
        for ch in '123456789':
            if ok(r, c, ch): g[r][c] = ch; go(pos + 1); g[r][c] = '.'
    go(0); return cnt
@reg(B, 'sudoku')
def _(board):
    g = [list(r) for r in board]
    def ok(r, c, ch):
        for k in range(9):
            if g[r][k] == ch or g[k][c] == ch: return False
        br, bc = r // 3 * 3, c // 3 * 3
        return all(g[br + i][bc + j] != ch for i in range(3) for j in range(3))
    def go(pos):
        while pos < 81 and g[pos // 9][pos % 9] != '.': pos += 1
        if pos == 81: return True
        r, c = divmod(pos, 9)
        for ch in '123456789':
            if ok(r, c, ch):
                g[r][c] = ch
                if go(pos + 1): return True
                g[r][c] = '.'
        return False
    assert go(0); return [''.join(r) for r in g]

@reg(S, 'palin_partition')
def _(s):
    out = []; cur = []
    def go(i):
        if i == len(s): out.append(cur[:]); return
        for j in range(i + 1, len(s) + 1):
            t = s[i:j]
            if t == t[::-1]: cur.append(t); go(j); cur.pop()
    go(0); return sorted(out)
@reg(B, 'palin_partition')
def _(s):
    n = len(s); out = []
    for m in range(1 << (n - 1)):
        cuts = [i + 1 for i in range(n - 1) if m >> i & 1]; ed = [0] + cuts + [n]
        parts = [s[ed[i]:ed[i + 1]] for i in range(len(ed) - 1)]
        if all(p == p[::-1] for p in parts): out.append(parts)
    return sorted(out)

@reg(S, 'restore_ip')
def _(s):
    out = []
    def go(i, parts):
        if len(parts) == 4:
            if i == len(s): out.append('.'.join(parts))
            return
        for L in (1, 2, 3):
            t = s[i:i + L]
            if len(t) < L or (L > 1 and t[0] == '0') or int(t) > 255: continue
            go(i + L, parts + [t])
    go(0, []); return sorted(out)
@reg(B, 'restore_ip')
def _(s):
    n = len(s); out = []
    for cuts in itertools.combinations(range(1, n), 3) if n >= 4 else []:
        ps = [s[a:b] for a, b in zip((0,) + cuts, cuts + (n,))]
        if all(str(int(p)) == p and int(p) <= 255 for p in ps): out.append('.'.join(ps))
    return sorted(out)

@reg(S, 'comb_nodes')
def _(candidates, target):
    def run(c, brk):
        calls = 0; found = 0
        def go(start, rem):
            nonlocal calls, found
            calls += 1
            if rem < 0: return
            if rem == 0: found += 1; return
            for j in range(start, len(c)):
                if brk and c[j] > rem: break
                go(j, rem - c[j])
        go(0, target); return calls, found
    a, fa = run(list(candidates), False); b, fb = run(sorted(candidates), True)
    assert fa == fb
    return [a, b, fa]
@reg(B, 'comb_nodes')
def _(candidates, target):
    def run(c, brk):    # explicit stack, same rules
        calls = 0; found = 0; st = [(0, target)]
        while st:
            start, rem = st.pop(); calls += 1
            if rem < 0: continue
            if rem == 0: found += 1; continue
            for j in range(len(c) - 1, start - 1, -1):
                if brk and c[j] > rem: continue
                st.append((j, rem - c[j]))
        return calls, found
    a, fa = run(list(candidates), False); b, fb = run(sorted(candidates), True)
    return [a, b, fa]

@reg(S, 'iter_ws')
def _(board, word):
    R, C = len(board), len(board[0]); L = len(word)
    if L > R * C: return False
    for sr in range(R):
        for sc in range(C):
            if board[sr][sc] != word[0]: continue
            path = [(sr, sc)]; nxt = [0]; seen = {(sr, sc)}
            while path:
                if len(path) == L: return True
                r, c = path[-1]; d = nxt[-1]
                if d == 4: path.pop(); nxt.pop(); seen.discard((r, c)); continue
                nxt[-1] += 1; dr, dc = DIRS[d]; nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen and board[nr][nc] == word[len(path)]:
                    path.append((nr, nc)); nxt.append(0); seen.add((nr, nc))
    return False
@reg(B, 'iter_ws')
def _(board, word): return B['word_search'](board, word)
def recursive_ws(board, word):   # plain recursion, used to demonstrate RecursionError
    R, C = len(board), len(board[0]); seen = set()
    def go(r, c, k):
        if board[r][c] != word[k] or (r, c) in seen: return False
        if k == len(word) - 1: return True
        seen.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1): return True
        seen.discard((r, c)); return False
    return any(go(r, c, 0) for r in range(R) for c in range(C))

@reg(S, 'expr_ops')
def _(num, target):
    n = len(num); out = []
    def go(i, expr, val, last):
        if i == n:
            if val == target: out.append(expr)
            return
        for j in range(i + 1, n + 1):
            t = num[i:j]
            if len(t) > 1 and t[0] == '0': break
            v = int(t)
            if i == 0: go(j, t, v, v)
            else:
                go(j, expr + '+' + t, val + v, v)
                go(j, expr + '-' + t, val - v, -v)
                go(j, expr + '*' + t, val - last + last * v, last * v)
    go(0, '', 0, 0); return sorted(out)
@reg(B, 'expr_ops')
def _(num, target):
    n = len(num); out = []
    for ops in itertools.product(['', '+', '-', '*'], repeat=n - 1):
        e = num[0] + ''.join(o + d for o, d in zip(ops, num[1:]))
        toks = re.split(r'[+*-]', e)
        if any(len(t) > 1 and t[0] == '0' for t in toks): continue
        if eval(e) == target: out.append(e)
    return sorted(out)

# ============ tries
@reg(S, 'trie_ops')
def _(ops):
    root = {}; res = []
    def walk(w):
        nd = root
        for ch in w:
            nd = nd.get(ch)
            if nd is None: return None
        return nd
    for name, arg in ops:
        if name == 'insert':
            nd = root
            for ch in arg: nd = nd.setdefault(ch, {})
            nd['$'] = True; res.append(None)
        elif name == 'search':
            nd = walk(arg); res.append(nd is not None and '$' in nd)
        else:
            res.append(walk(arg) is not None)
    return res
@reg(B, 'trie_ops')
def _(ops):
    ws = set(); res = []
    for name, arg in ops:
        if name == 'insert': ws.add(arg); res.append(None)
        elif name == 'search': res.append(arg in ws)
        else: res.append(any(w.startswith(arg) for w in ws))
    return res

@reg(S, 'replace_words')
def _(roots, sentence):
    root = {}
    for w in roots:
        nd = root
        for ch in w: nd = nd.setdefault(ch, {})
        nd['$'] = True
    out = []
    for word in sentence.split(' '):
        nd = root; k = 0
        while k < len(word) and '$' not in nd and word[k] in nd: nd = nd[word[k]]; k += 1
        out.append(word[:k] if '$' in nd else word)
    return ' '.join(out)
@reg(B, 'replace_words')
def _(roots, sentence):
    out = []
    for word in sentence.split(' '):
        c = [r for r in roots if word.startswith(r)]
        out.append(min(c, key=len) if c else word)
    return ' '.join(out)

@reg(S, 'autocomplete')
def _(entries, queries):
    root = {}
    for w, cnt in entries:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
            top = nd.setdefault('#', [])
            top.append((-cnt, w)); top.sort(); del top[3:]
    res = []
    for p in queries:
        nd = root
        for ch in p:
            nd = nd.get(ch)
            if nd is None: break
        res.append([] if nd is None else [w for _, w in nd['#']])
    return res
@reg(B, 'autocomplete')
def _(entries, queries):
    return [[w for c, w in sorted((-c, w) for w, c in entries if w.startswith(p))[:3]] for p in queries]

@reg(S, 'map_sum')
def _(ops):
    root = {}; vals = {}; res = []
    for op in ops:
        if op[0] == 'insert':
            _, key, v = op; delta = v - vals.get(key, 0); vals[key] = v; nd = root
            for ch in key:
                nd = nd.setdefault(ch, {'s': 0}) if False else nd.setdefault(ch, {})
                nd['s'] = nd.get('s', 0) + delta
            res.append(None)
        else:
            nd = root
            for ch in op[1]:
                nd = nd.get(ch)
                if nd is None: break
            res.append(0 if nd is None else nd['s'])
    return res
@reg(B, 'map_sum')
def _(ops):
    d = {}; res = []
    for op in ops:
        if op[0] == 'insert': d[op[1]] = op[2]; res.append(None)
        else: res.append(sum(v for k, v in d.items() if k.startswith(op[1])))
    return res

@reg(S, 'max_xor')
def _(nums):
    root = [None, None]; best = 0
    def ins(x):
        nd = root
        for b in range(30, -1, -1):
            bit = x >> b & 1
            if nd[bit] is None: nd[bit] = [None, None]
            nd = nd[bit]
    ins(nums[0])
    for x in nums[1:]:
        nd = root; cur = 0
        for b in range(30, -1, -1):
            bit = x >> b & 1
            if nd[bit ^ 1] is not None: cur |= 1 << b; nd = nd[bit ^ 1]
            else: nd = nd[bit]
        best = max(best, cur); ins(x)
    return best
@reg(B, 'max_xor')
def _(nums): return max(a ^ b for a, b in itertools.combinations(nums, 2))

@reg(S, 'trie_memory')
def _(words):
    root = {}; nodes = 0
    for w in set(words):
        nd = root
        for ch in w:
            if ch not in nd: nd[ch] = {}; nodes += 1
            nd = nd[ch]
    d = set(words)
    return [nodes, 26 * (nodes + 1), sum(len(w) for w in d), len(d)]
@reg(B, 'trie_memory')
def _(words):
    d = set(words); pre = {w[:i] for w in d for i in range(1, len(w) + 1)}
    return [len(pre), 26 * (len(pre) + 1), sum(len(w) for w in d), len(d)]

# ============ skip list
class SkipList:
    MAXL = 16
    def __init__(self, seed=0): self.rng = random.Random(seed); self.head = [None] * self.MAXL; self.lvl = 1   # node = [key, next0, next1, ...]
    def _level(self):
        l = 1
        while l < self.MAXL and self.rng.random() < 0.5: l += 1
        return l
    def _find(self, x):
        upd = [None] * self.MAXL; cur = None   # cur None = head
        for i in range(self.lvl - 1, -1, -1):
            while True:
                nx = self._nxt(cur, i)
                if nx is not None and nx[0] < x: cur = nx
                else: break
            upd[i] = cur
        nx = self._nxt(cur, 0)
        return upd, nx
    def _nxt(self, node, i): return self.head[i] if node is None else node[1 + i]
    def contains(self, x):
        _, nx = self._find(x); return nx is not None and nx[0] == x
    def insert(self, x):
        upd, nx = self._find(x)
        if nx is not None and nx[0] == x: return False
        l = self._level()
        if l > self.lvl:
            for i in range(self.lvl, l): upd[i] = None
            self.lvl = l
        node = [x] + [None] * l
        for i in range(l):
            node[1 + i] = self._nxt(upd[i], i)
            if upd[i] is None: self.head[i] = node
            else: upd[i][1 + i] = node
        return True
    def remove(self, x):
        upd, nx = self._find(x)
        if nx is None or nx[0] != x: return False
        for i in range(self.lvl):
            if self._nxt(upd[i], i) is nx:
                if upd[i] is None: self.head[i] = nx[1 + i]
                else: upd[i][1 + i] = nx[1 + i]
        while self.lvl > 1 and self.head[self.lvl - 1] is None: self.lvl -= 1
        return True
    def items(self):
        out = []; nd = self.head[0]
        while nd is not None: out.append(nd[0]); nd = nd[1]
        return out
@reg(S, 'skip_list')
def _(ops, seed=0):
    sl = SkipList(seed); res = []
    for name, x in ops: res.append(getattr(sl, name)(x))
    return res
@reg(B, 'skip_list')
def _(ops, seed=0):
    s = set(); res = []
    for name, x in ops:
        if name == 'insert': res.append(x not in s); s.add(x)
        elif name == 'contains': res.append(x in s)
        else: res.append(x in s); s.discard(x)
    return res
