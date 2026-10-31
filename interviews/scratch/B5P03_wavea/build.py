import os, sys, re
os.chdir('/home/user/case_studies/interviews')
sys.path.insert(0,'scratch/B5P03_wavea')
from qs import QS
order={'🟢':0,'🟡':1,'🔴':2}
QS=sorted(QS,key=lambda q:(-q[0],order[q[1]]))   # stable: stars 3,2,1; easy to hard inside a star
N=40
n=len(QS)
c=[sum(1 for q in QS if q[0]==s) for s in (3,2,1)]
print(n,c)
assert n==N, n
assert [q[0] for q in QS]==sorted([q[0] for q in QS],reverse=True)
assert sum(c)==N and all(q[1] in order for q in QS)
assert len({q[2] for q in QS})==N
for s in (3,2,1):
    d=[order[q[1]] for q in QS if q[0]==s]
    assert d==sorted(d),(s,d)
for s,d,q,a in QS:
    assert 'Example' in q and '->' in q, q[:40]
    assert 'Asked' not in q and a.strip()
# resolve every 'Part N Qn' reference against the built part files, by checked heading keyword
KW={(1,3):'Valid anagram',(1,24):'Encode and decode a list of strings',(2,1):'Valid palindrome. ',(2,20):'Valid palindrome II'}
refs=set()
for s,d,q,a in QS:
    for m in re.finditer(r'Part (\d+) Q(\d+)',q): refs.add((int(m.group(1)),int(m.group(2))))
print('refs',sorted(refs))
files={p:open(f'Book5_DSA/Book5_DSA_Part0{p}.md',encoding='utf-8').read() for p in (1,2)}
for (p,qn) in refs:
    assert (p,qn) in KW, (p,qn)
    m=re.search(rf'^### Q{qn} \S+ \S+ (.*)$',files[p],re.M)
    assert m and m.group(1).startswith(KW[(p,qn)]), (p,qn, m and m.group(1)[:50])
hdr=f"""# Book 5 — Part 3: Strings

**Topic:** Python DSA for product-company interviews: palindromes (longest palindromic substring and counting by expand-around-center, shortest palindrome, Manacher at concept level, rearrangement counting), string building and immutability (join versus +=, StringIO), parsing and tokenising in one left-to-right pass (atoi, valid number, version comparison, basic calculator without a stack design), reverse words and in-place character-list work, run-length compression, encode and decode with escaping, longest common prefix, numeric-string arithmetic (add, add binary, multiply) and Roman numerals both ways, zigzag, pattern matching (naive search, KMP prefix function, Z-function, Rabin-Karp with collision handling, longest happy prefix, longest repeated substring with rolling hash plus binary search), repeated-substring and rotation problems (rotated string, lexicographically smallest rotation), Unicode versus bytes versus code points versus graphemes, normalisation and case-folding with unicodedata, UTF-8 validation, regex versus manual matching and catastrophic backtracking, wildcard matching, and edit distance, LCS and tries at concept level only

**Target:** 40  |  **Actual:** {n} (⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})  |  **Date:** 2026-10-27  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns string algorithms and string-specific Python behaviour (palindromic substrings, parsing, numeric strings, pattern matching, Unicode). Part 1 already owns hashing and anagram grouping, valid anagram, isomorphic strings and word pattern, ransom note and the length-prefix list codec (cross-referenced here only as 'Part 1 Q3, Q24', each checked against its heading; isomorphic and word-pattern problems are not repeated). Part 2 owns sliding-window string problems (longest substring without repeats, minimum window substring, permutation in string, anagram start positions, character replacement) and the two-pointer valid palindrome and valid palindrome II (cross-referenced only as 'Part 2 Q1, Q20', checked against headings); none of those is repeated. Part 4 owns stacks and queues (the calculator question here is a single-pass parse with no stack design); Part 11 owns edit distance, LCS and regex matching as DP (concept level only here, with memoised recursion on tiny inputs); Part 12 owns backtracking (palindrome partitioning), tries and bit manipulation (the prefix-query question here is a sorted-list plus bisect answer with the trie described only); Part 13 owns number theory and sorting internals. Book 3 owns SQL, Book 4 systems, Book 1 ML maths. Each question is a frozen, self-contained prompt with a precise statement, constraints and at least one input/output example; every example in every prompt was run against brute-force or reference code (scratch/B5P03_wavea/check_examples.py, python3 -I) before freezing; one example was found wrong during that run (a ligature does not separate casefold from compatibility normalisation because casefold already expands it) and was replaced. Questions are paraphrased from well-known problems and named by common names only.

Evidence limits: WebFetch failed (getaddrinfo ENOTFOUND for neetcode.io) so no page was opened; every external source is a WebSearch snippet only (see research_notes/Book5_Part03_sources.md). Searches for TCS, Infosys and Amazon string rounds returned generic aggregator and candidate-reported pages, and nothing for Google, so 'Asked at' tags name source types (public pattern lists, community roundups, Indian placement-style prep, pattern-matching tutorials, Unicode docs and tutorials, editor knowledge of standard lists), not verified company reports; company tags on community pages are unverified. The Unicode searches did not return the official Python docs, so the casefold and grapheme claims rest on editor knowledge and on the sandbox run. Star ratings are an editorial judgement from how consistently a problem appears across these lists. No salary figures are used. Wave B code runs as Python 3.13 with the standard library only.

---
"""
out=[hdr]
for i,(s,d,q,a) in enumerate(QS,1):
    out.append(f"\n### Q{i} {'⭐'*s} {d} {q.strip()}\n**Asked at:** {a}\n<!-- ANSWER_PENDING -->\n")
txt=''.join(out)
assert txt.count('<!-- ANSWER_PENDING -->')==N and txt.count('**Asked at:**')==N
assert f"(⭐⭐⭐ {c[0]}, ⭐⭐ {c[1]}, ⭐ {c[2]})" in txt and f"**Actual:** {N} " in txt
assert txt.count('\n### Q')==N
os.makedirs('Book5_DSA',exist_ok=True)
open('Book5_DSA/Book5_DSA_Part03.md','w',encoding='utf-8',newline='\n').write(txt)
rows_i=''.join(f"| B5P03-Q{i} | 3 | {q.strip()} |\n" for i,(s,d,q,a) in enumerate(QS,1))
open('scratch/B5P03_wavea/index_rows.txt','w',encoding='utf-8',newline='\n').write(rows_i)
idx=open('question_index.md',encoding='utf-8').read()
if 'B5P03-Q1 ' not in idx:
    if not idx.endswith('\n'): idx+='\n'
    open('question_index.md','w',encoding='utf-8',newline='\n').write(idx+rows_i)
print('built',n,c)
