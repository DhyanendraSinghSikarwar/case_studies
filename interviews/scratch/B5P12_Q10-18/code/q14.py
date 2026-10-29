import random

random.seed(1214)

def build_trie(roots):
    root = {}
    for w in roots:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
        nd['$'] = True                               # end-of-root flag ('$' can never be a lowercase letter)
    return root

def replace_words(roots, sentence):
    trie = build_trie(roots)
    out = []
    for word in sentence.split(' '):
        nd, k = trie, 0
        while k < len(word) and '$' not in nd and word[k] in nd:   # stop at the FIRST flag: it is the shortest root
            nd = nd[word[k]]
            k += 1
        out.append(word[:k] if '$' in nd else word)
    return ' '.join(out)

def brute(roots, sentence):
    out = []
    for word in sentence.split(' '):
        c = [r for r in roots if word.startswith(r)]
        out.append(min(c, key=len) if c else word)
    return ' '.join(out)

for roots, s, want in [(['to', 'tra', 'a'], 'tomorrow a train travels to tokyo', 'to a tra tra to to'),
                       (['ab'], 'cab ab abc', 'cab ab ab'), (['b', 'be'], 'best bee ace', 'b b ace')]:
    assert replace_words(roots, s) == brute(roots, s) == want, (roots, s)
print("3 prompt examples ok")

# dry run: roots = ['to','tra','a'], word 'train'
t = build_trie(['to', 'tra', 'a'])
print("trie top level:", sorted(k for k in t), "| under 't':", sorted(k for k in t['t']), "| under 'tr':", sorted(t['t']['r']))
w = 'train'; nd = t; path = ''
for ch in w:
    if '$' in nd or ch not in nd: break
    nd = nd[ch]; path += ch
    print("  read %r -> node for %r, end flag here: %s" % (ch, path, '$' in nd))
print("  result:", path if '$' in nd else w)

for _ in range(500):
    roots = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(random.randint(1, 6))]
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(random.randint(1, 8))]
    s = ' '.join(words)
    assert replace_words(roots, s) == brute(roots, s), (roots, s)
print("500 seeded random cases agree with scanning every root for every word")

# duplicate roots and ordering do not matter; a longer root never wins over a shorter prefix root
assert replace_words(['ab', 'ab', 'a'], 'abc') == 'a' == replace_words(['a', 'ab', 'ab'], 'abc')
assert replace_words(['abc'], 'ab') == 'ab'              # root longer than the word: no replacement
assert replace_words(['a'], 'a') == 'a'                  # word equal to a root
assert replace_words(['z'], 'a') == 'a'                  # no root matches
assert replace_words(['a'], 'aaa a aa') == 'a a a'
print("edge asserts ok")

# max-size shape: 1000 roots of length 100 and a 1000-word sentence of length-100 words
roots = [''.join(random.choice('ab') for _ in range(100)) for _ in range(1000)]
sent = ' '.join(''.join(random.choice('ab') for _ in range(100)) for _ in range(1000))
assert replace_words(roots, sent) == brute(roots, sent)
print("max-size shape ok (1000 roots x 100 letters, 1000 words x 100 letters)")
