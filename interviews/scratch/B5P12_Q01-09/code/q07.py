import itertools
import math
import random

random.seed(1207)

def gen_parens(n):
    """Returns (sorted list, number of calls, list of every prefix visited)."""
    out, cur, calls, prefixes = [], [], [0], []
    def go(o, c):
        calls[0] += 1
        prefixes.append(''.join(cur))
        if len(cur) == 2 * n:
            out.append(''.join(cur)); return
        if o < n:                           # rule 1: may open while fewer than n opens used
            cur.append('('); go(o + 1, c); cur.pop()
        if c < o:                           # rule 2: may close only if an unmatched '(' exists
            cur.append(')'); go(o, c + 1); cur.pop()
    go(0, 0)
    return sorted(out), calls[0], prefixes

def gen_unpruned_calls(n):
    """Try '(' and ')' at every position, test balance at the leaves: calls = 2^(2n+1) - 1."""
    return 2 ** (2 * n + 1) - 1

def brute(n):
    def ok(s):
        bal = 0
        for ch in s:
            bal += 1 if ch == '(' else -1
            if bal < 0:
                return False
        return bal == 0
    return sorted(''.join(t) for t in itertools.product('()', repeat=2 * n) if ok(t))

examples = [(1, ['()']), (2, ['(())', '()()']), (3, ['((()))', '(()())', '(())()', '()(())', '()()()'])]
for n, want in examples:
    assert gen_parens(n)[0] == want == brute(n)
    print(n, '->', gen_parens(n)[0])

# decision tree for n = 2: which branches the two rules allow
def tree(n, s='', o=0, c=0, d=0):
    if len(s) == 2 * n:
        print('  ' * d + f'{s}  (answer)'); return
    print('  ' * d + f'{s or "(empty)"}  open={o} close={c}')
    if o < n: tree(n, s + '(', o + 1, c, d + 1)
    else: print('  ' * (d + 1) + "'(' blocked: open == n")
    if c < o: tree(n, s + ')', o, c + 1, d + 1)
    else: print('  ' * (d + 1) + "')' blocked: close == open")
tree(2)

# Catalan counts, calls pruned vs unpruned, and the claim 'no dead branch': every visited prefix begins some answer
for n in range(1, 9):
    res, calls, prefixes = gen_parens(n)
    assert len(res) == math.comb(2 * n, n) // (n + 1)
    assert all(any(r.startswith(p) for r in res) for p in prefixes), 'dead branch found'
    print(f'n={n} results={len(res):5} pruned calls={calls:6} unpruned calls={gen_unpruned_calls(n):7}')
    if n <= 6:
        assert res == brute(n)

# seeded cross-check (n up to 5, plus random ids)
for _ in range(100):
    n = random.randint(1, 5)
    assert gen_parens(n)[0] == brute(n)
print('random cross-check ok: 100 cases (n in 1..5; the oracle is exhaustive)')
# edge: n = 1, n = 8 (1430 = Catalan(8)), first and last strings
r = gen_parens(8)[0]
assert len(r) == 1430 and r[0] == '(' * 8 + ')' * 8 and r[-1] == '()' * 8
assert gen_parens(1)[0] == ['()']
print('edge asserts ok')
