import itertools, random, string
from collections import deque, defaultdict
random.seed(15)
INF = float('inf')

def ladder_letters(begin, end, word_list):      # try all 26 letters at each position
    words = set(word_list)
    if end not in words:
        return 0
    seen = {begin}
    q = deque([(begin, 1)])
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for c in string.ascii_lowercase:
                x = w[:i] + c + w[i + 1:]
                if x in words and x not in seen:
                    seen.add(x)
                    q.append((x, d + 1))
    return 0

def ladder_buckets(begin, end, word_list):      # wildcard buckets: 'h*t' -> words matching it
    words = list(dict.fromkeys(word_list))
    if end not in words:
        return 0
    bucket = defaultdict(list)
    for w in words + [begin]:
        for i in range(len(w)):
            bucket[w[:i] + '*' + w[i + 1:]].append(w)
    seen = {begin}
    q = deque([(begin, 1)])
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for x in bucket[w[:i] + '*' + w[i + 1:]]:
                if x not in seen:
                    seen.add(x)
                    q.append((x, d + 1))
    return 0

def brute(begin, end, word_list):               # explicit all-pairs graph, then relax to a fixed point
    nodes = [begin] + [w for w in dict.fromkeys(word_list) if w != begin]
    if end not in word_list:
        return 0
    adj = {w: [x for x in nodes if sum(a != b for a, b in zip(w, x)) == 1] for w in nodes}
    d = {w: INF for w in nodes}; d[begin] = 1
    changed = True
    while changed:
        changed = False
        for w in nodes:
            for x in adj[w]:
                if d[w] + 1 < d[x]:
                    d[x] = d[w] + 1; changed = True
    return 0 if d[end] == INF else d[end]

wl = ['hot', 'dot', 'dog', 'lot', 'log', 'cog']
assert ladder_letters('hit', 'cog', wl) == ladder_buckets('hit', 'cog', wl) == brute('hit', 'cog', wl) == 5
assert ladder_letters('hit', 'cog', wl[:-1]) == ladder_buckets('hit', 'cog', wl[:-1]) == 0
assert ladder_letters('a', 'c', ['a', 'b', 'c']) == ladder_buckets('a', 'c', ['a', 'b', 'c']) == 2
print("examples ok: 5 0 2")

# convention when begin == end and it is in the list: one word, length 1 (the prompt does not say; all three methods agree)
assert ladder_letters('a', 'a', ['a']) == ladder_buckets('a', 'a', ['a']) == brute('a', 'a', ['a']) == 1

# exhaustive: alphabet abc, length 2 -> 9 words, every subset as word_list, every begin and end
allw = [''.join(p) for p in itertools.product('abc', repeat=2)]
cnt = 0
for mask in range(1, 1 << 9):
    wl = [w for i, w in enumerate(allw) if mask >> i & 1]
    for b in allw:
        for e in allw:
            r = ladder_letters(b, e, wl)
            assert r == ladder_buckets(b, e, wl) == brute(b, e, wl), (b, e, wl)
            cnt += 1
print("exhaustive abc/length 2: %d cases, all three methods agree" % cnt)

for _ in range(300):
    L = random.randint(1, 4)
    ws = list({''.join(random.choice('abc') for _ in range(L)) for _ in range(random.randint(1, 12))})
    b = ''.join(random.choice('abc') for _ in range(L)); e = random.choice(ws)
    assert ladder_letters(b, e, ws) == ladder_buckets(b, e, ws) == brute(b, e, ws)
print("300 random cases ok")

# edge cases
assert ladder_letters('abc', 'xyz', ['xyz']) == 0          # no one-letter path
assert ladder_letters('abc', 'abd', ['abd']) == 2          # begin not in the list
assert ladder_letters('abc', 'abd', ['abc']) == 0          # end not in the list
print("edge cases ok")

# scale: 5000 words of length 10 (complexity depends on neighbour structure, not only the pair count)
ws = list({''.join(random.choice(string.ascii_lowercase) for _ in range(10)) for _ in range(5000)})
r1 = ladder_letters(ws[0], ws[1], ws); r2 = ladder_buckets(ws[0], ws[1], ws)
assert r1 == r2
print("5000 random 10-letter words: both give", r1, "(random words are rarely 1 letter apart)")
dense = [''.join(p) for p in itertools.product('abcde', repeat=4)][:625]
assert ladder_letters('aaaa', 'eeee', dense) == ladder_buckets('aaaa', 'eeee', dense) == 5
print("625 dense 4-letter words over 'abcde': shortest ladder aaaa -> eeee has", ladder_letters('aaaa', 'eeee', dense), "words")
