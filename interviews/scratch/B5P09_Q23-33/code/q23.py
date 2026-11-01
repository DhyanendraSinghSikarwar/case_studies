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
