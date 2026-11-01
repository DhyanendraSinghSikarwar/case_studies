### Q15 ⭐⭐⭐ 🟡 How do metadata filtering and access control work in RAG? Why does post-filtering fail, and how do you guarantee users never see documents they lack permission for?
**Asked at:** product, GCC, regulated-industry and enterprise teams
**Say this first (1 line):** Store the tenant or ACL metadata on every chunk and apply the filter inside the vector query (pre-filter), never after retrieval, because post-filtering can return too few results and a permission bug there is a data leak.

**Then explain:**
- **How it works:** at ingestion each chunk gets metadata such as `tenant_id`, `allowed_groups`, `doc_id`, `source`, `date`. At query time the server adds the user's identity to the filter. The user never sends their own permissions; the backend derives them from the auth token.
- **Post-filter:** take the global top-k, then drop what the user cannot see. If most of the corpus belongs to other tenants, you may keep 2 of 10. The model then answers from thin context or says "not found" when the answer existed.
- **Pre-filter:** restrict the candidate set first, then rank. You always get k results the user may see. Cost: on a plain ANN graph, a very selective filter can slow the search or hurt recall, so use the store's filter-aware search or partition by tenant (check current docs of your store; behaviour differs).
- **Why it is also a security issue:** anything outside the filter that reaches the app, the reranker, logs or the prompt has already leaked, even if you hide it later. Rankings and scores can also reveal that a restricted document exists.
- **Guarantees:** deny by default, filter in the database not the app, sync ACL changes (a revoked user must lose access at once, so keep the ACL as a filter on live metadata or re-sync fast), test with a canary user who must never see canary documents.

**Example:** SYNTHETIC: 2,000 random unit vectors over 4 tenants, k=10. For one query the global top-10 had only 3 chunks of the user's tenant (post-filter), while the pre-filter returned 10 of 10 with 0 leaks. Over 500 random queries the post-filter returned fewer than 10 every time, with a mean of 2.4 results.

**Code:** (run, numpy, synthetic vectors; no real embeddings)
```python
import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: 2000 chunks, 4 tenants; random unit vectors (toy, no semantics)
N, d, K = 2000, 32, 10
X = rng.standard_normal((N, d)); X /= np.linalg.norm(X, axis=1, keepdims=True)
tenant = rng.integers(0, 4, N)            # ACL metadata stored on every chunk
q = rng.standard_normal(d); q /= np.linalg.norm(q)
user_tenant = 0

def search(q, k, allowed=None, candidates=None):
    s = X @ q
    mask = np.ones(N, bool) if allowed is None else allowed
    idx = np.where(mask)[0]
    return idx[np.argsort(-s[idx])[:k]]

# post-filter: take global top-K, then drop chunks the user may not see
top = search(q, K)
post = [i for i in top if tenant[i] == user_tenant]
# pre-filter: apply the ACL inside the query, then take top-K
pre = search(q, K, allowed=(tenant == user_tenant))
print("post-filter returned", len(post), "of", K, "| pre-filter returned", len(pre), "of", K)
print("pre-filter leaks:", int(np.sum(tenant[pre] != user_tenant)))

# leak check over 500 random queries
short, counts, leaks = [], [], 0
for _ in range(500):
    qq = rng.standard_normal(d); qq /= np.linalg.norm(qq)
    p = [i for i in search(qq, K) if tenant[i] == user_tenant]
    short.append(len(p) < K); counts.append(len(p))
    r = search(qq, K, allowed=(tenant == user_tenant))
    leaks += int(np.sum(tenant[r] != user_tenant))
print("queries where post-filter returned fewer than K:", f"{np.mean(short):.0%}", "| pre-filter leaks over 500 queries:", leaks)
print("mean post-filter results:", np.mean(counts))
```
Output (my run):
```
post-filter returned 3 of 10 | pre-filter returned 10 of 10
pre-filter leaks: 0
queries where post-filter returned fewer than K: 100% | pre-filter leaks over 500 queries: 0
mean post-filter results: 2.422
```

**Follow-ups:**
- *What if the filter is very selective (one user has 50 documents)?* Use a per-tenant partition or namespace, or a filter-aware index; a brute-force scan over the allowed subset is also fine at that size.
- *Do you also filter in the reranker and cache?* Yes: a semantic cache keyed only on the query can serve one user's answer to another, so key it by permission scope (Part 11 covers RAG security in depth).
- *Document-level vs chunk-level ACLs?* Copy the document's ACL onto each chunk at ingestion and re-write it when permissions change (see Q20).

**Common mistakes:** filtering after top-k; letting the client send the filter; checking permissions only when displaying sources while the text already went into the prompt; forgetting that revoked access must propagate; assuming filtering is free for the index.

### Q16 ⭐⭐ 🟡 What pitfalls come with chunk size and overlap in practice (tokens vs characters, boundaries, chunk metadata, duplicated text)?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Chunk size must be measured in the embedder's and generator's tokens, not characters; the usual bugs are cutting sentences or tables in half, off-by-one overlap, duplicates from overlap, and chunks that carry no doc id or position so you cannot cite or debug them.

**Then explain:**
- **Tokens vs characters:** model limits are in tokens, and a token is not a fixed number of characters (it varies by language and content; Hindi or code often costs more tokens per word). Count with the actual tokenizer. My demo uses a word count as a labelled proxy only.
- **Boundaries:** fixed splits cut sentences, list items, code and tables. Prefer splitting at paragraph or sentence boundaries, keep a table whole or split by rows with the header repeated (Q17), and keep headings with their text (see Q4 for the strategies).
- **Overlap:** overlap protects facts that sit on a boundary. It costs index size, and the same sentence then appears in two chunks, so top-k can fill up with near-identical hits. Dedupe at retrieval by merging overlapping offset ranges of the same document.
- **Overlap bugs:** the step is `size - overlap`. Writing `size - overlap + 1` silently shrinks the overlap by one (or drops a word when overlap is 0).
- **Chunk metadata:** `doc_id`, section title, page, start and end offsets, chunk index, version, source URL. This enables citations (Q26), deletion by document (Q20), parent lookup (Q18) and ACL filtering (Q15).

**Example:** In my run with 20 words, size 8 and overlap 2, the buggy step gave starts 0, 7, 14 and an actual overlap of 1; the fixed step gave 0, 6, 12 and overlap 2. With overlap 0 the buggy version never indexed words 8 and 17; the fixed one covered every word. In the made-up retrieval list, two overlapping chunks of the same document (spans 0-8 and 6-14) collapsed to the higher-scored one.

**Code:** (run; word-count proxy for tokens, made-up hits)
```python
# Word-count proxy: 1 "token" ~ 1 word here (real tokenisers differ; count with your model's tokenizer).
def chunk_buggy(words, size, overlap):
    out, start = [], 0
    while start < len(words):
        out.append((start, words[start:start+size]))
        start += size - overlap + 1       # BUG: off-by-one, skips one word between chunks
    return out

def chunk_fixed(words, size, overlap):
    assert 0 <= overlap < size
    out, start = [], 0
    while start < len(words):
        out.append((start, words[start:start+size]))
        if start + size >= len(words): break
        start += size - overlap
    return out

words = [f"w{i}" for i in range(20)]
for ov in (2, 0):
    for name, fn in [("buggy", chunk_buggy), ("fixed", chunk_fixed)]:
        ch = fn(words, 8, ov)
        covered = set(i for s, c in ch for i in range(s, s+len(c)))
        missing = sorted(set(range(20)) - covered)
        actual = len(set(ch[0][1]) & set(ch[1][1]))
        print(f"requested overlap={ov} {name}: starts={[s for s, _ in ch]} actual overlap={actual} words never indexed={missing}")

# overlap creates duplicates: dedupe at retrieval by offset range, keep best-scored
hits = [  # (doc, start, end, score) -- made-up retrieval results
    ("docA", 0, 8, 0.91), ("docA", 6, 14, 0.89), ("docA", 12, 20, 0.40), ("docB", 0, 8, 0.70)]
def dedupe(hits):
    kept = []
    for h in sorted(hits, key=lambda x: -x[3]):
        if all(not (h[0] == k[0] and h[1] < k[2] and k[1] < h[2]) for k in kept):
            kept.append(h)
    return kept
print("before:", len(hits), "after dedupe of overlapping spans:", dedupe(hits))
```
Output (my run):
```
requested overlap=2 buggy: starts=[0, 7, 14] actual overlap=1 words never indexed=[]
requested overlap=2 fixed: starts=[0, 6, 12] actual overlap=2 words never indexed=[]
requested overlap=0 buggy: starts=[0, 9, 18] actual overlap=0 words never indexed=[8, 17]
requested overlap=0 fixed: starts=[0, 8, 16] actual overlap=0 words never indexed=[]
before: 4 after dedupe of overlapping spans: [('docA', 0, 8, 0.91), ('docB', 0, 8, 0.7), ('docA', 12, 20, 0.4)]
```

**Follow-ups:**
- *How much overlap?* Reported starting points are around 10-20 percent of the chunk size; tune on a golden set (Q10), not by habit.
- *Is overlap always worth it?* Not for structure-aware chunks that already split at natural boundaries.

**Common mistakes:** counting characters when the limit is tokens; one chunk size for all content types; no offsets stored, so citations and dedupe are impossible; testing the chunker only on clean prose; never printing a few real chunks to read them.

### Q17 ⭐⭐ 🟡 How do you ingest PDFs, tables, scans and HTML for RAG (parsing, OCR, layout-aware extraction, tables as text)?
**Asked at:** product, GCC, finance and enterprise teams
**Say this first (1 line):** Plain text extraction destroys tables and reading order, so use layout-aware extraction (OCR for scans), turn tables into text that keeps caption, headers and units, strip repeated headers and footers, keep page and section metadata, and evaluate the extraction itself before blaming the retriever.

**Then explain:**
- **PDF with a text layer:** simple extraction can interleave columns, glue table cells together and mix in page headers. A layout-aware parser detects blocks, columns and tables. Look at the output yourself on a sample.
- **Scans:** no text layer, so run OCR (optical character recognition, image to text). Expect errors on poor scans, stamps and handwriting; keep a confidence score and flag low-confidence pages for review.
- **HTML:** drop navigation, cookie banners and footers; keep headings, lists and tables as structure.
- **Tables:** options are markdown or CSV text, or one sentence per row ("Services segment revenue was Rs 640 crore in FY23..."). Always attach the caption, column names and units to each piece, otherwise a chunk of bare numbers matches nothing. Very wide tables may be better queried through a structured tool than retrieved.
- **Headers and footers:** repeated page strings pollute many chunks; detect lines repeated across pages and remove them. Keep `page`, `section`, `doc_id` as metadata.
- **Evaluate extraction:** spot-check 20-50 pages, compare table cells with the source, and measure retrieval on questions whose answers sit in tables.

**Example:** TOY test (hashed bag-of-words, lexical only, not a semantic model): a synthetic 6-row revenue table, query "Services segment revenue FY24 Rs crore". Markdown rows split without header or caption ranked the correct row 2nd, behind an unrelated sentence mentioning services; row sentences with caption and units ranked it 1st. The toy shows the mechanism only; a real embedder behaves differently, so test on your own documents. (I first tried a longer natural-language query; hash collisions in the toy embedder reordered results, which is itself a reminder not to read much into toy scores.)

**Code:** (run; toy embedder, synthetic table)
```python
import numpy as np, re, hashlib
# TOY embedder: hashed bag of words, 1024 dims. Lexical only; NOT a semantic model.
def emb(text, D=1024):
    v = np.zeros(D)
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % D] += 1
    return v / (np.linalg.norm(v) + 1e-9)

caption = "Table 3: Segment revenue by year (Rs crore)"   # synthetic table
header = ["Segment", "FY23", "FY24"]
rows = [["Retail", "1200", "1350"], ["Cloud", "800", "1010"], ["Services", "640", "700"],
        ["Hardware", "300", "250"], ["Licensing", "150", "170"], ["Other", "60", "55"]]

def to_markdown(caption, header, rows):
    lines = [caption, "| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)

def to_row_sentences(caption, header, rows, unit="Rs crore"):
    return [f"{caption}. {r[0]} segment revenue was Rs {r[1]} crore in {header[1]} and Rs {r[2]} crore in {header[2]}." for r in rows]

md = to_markdown(caption, header, rows)
sents = to_row_sentences(caption, header, rows)
print(md); print(sents[2]); print()

# Naive pipeline: split the markdown table by lines, so a row loses caption and header
naive_rows = md.split("\n")[3:]
corpus = {"markdown row (no header/caption)": naive_rows, "row sentence (caption+units)": sents}
# distractor chunks from the same toy document
others = ["Hardware margins fell because of component costs.", "The services team opened two new offices in FY24.",
          "Revenue recognition policy for cloud contracts is described in note 2."]
q = "Services segment revenue FY24 Rs crore"
qv = emb(q)
for name, chunks in corpus.items():
    allc = chunks + others
    sc = [float(emb(c) @ qv) for c in allc]
    order = np.argsort(sc)[::-1]
    target = [i for i, c in enumerate(allc) if "Services" in c and "640" in c][0]
    print(name, "top-3:", [allc[i][:48] for i in order[:3]])
    print(f"{name}: rank of the correct row = {list(order).index(target)+1}, top-1 = {allc[order[0]][:60]!r}")
```
Output (my run):
```
Table 3: Segment revenue by year (Rs crore)
| Segment | FY23 | FY24 |
|---|---|---|
| Retail | 1200 | 1350 |
| Cloud | 800 | 1010 |
| Services | 640 | 700 |
| Hardware | 300 | 250 |
| Licensing | 150 | 170 |
| Other | 60 | 55 |
Table 3: Segment revenue by year (Rs crore). Services segment revenue was Rs 640 crore in FY23 and Rs 700 crore in FY24.

markdown row (no header/caption) top-3: ['The services team opened two new offices in FY24', '| Services | 640 | 700 |', 'Revenue recognition policy for cloud contracts i']
markdown row (no header/caption): rank of the correct row = 2, top-1 = 'The services team opened two new offices in FY24.'
row sentence (caption+units) top-3: ['Table 3: Segment revenue by year (Rs crore). Ser', 'Table 3: Segment revenue by year (Rs crore). Clo', 'Table 3: Segment revenue by year (Rs crore). Lic']
row sentence (caption+units): rank of the correct row = 1, top-1 = 'Table 3: Segment revenue by year (Rs crore). Services segmen'
```

**Follow-ups:**
- *Numbers in tables, exact lookups?* Dense retrieval is weak at exact numbers; add keyword search (Part 7) or structured queries.
- *Images and charts?* Caption them, or use a vision model to describe them, and store the description with the page.

**Common mistakes:** never inspecting parser output; dropping the table header from chunks after row splitting; keeping page footers; assuming OCR text is clean; losing page numbers so citations cannot point to a page.

### Q18 ⭐⭐ 🟡 What is parent-document (small-to-big) retrieval, and when does returning a larger context around a hit help?
**Asked at:** product, GenAI startups
**Say this first (1 line):** Parent-document or small-to-big retrieval indexes small child chunks for precise matching, keeps a map from each child to its parent section, and returns the parent (or a window around the hit) to the LLM so it gets enough context.

**Then explain:**
- **Why:** small chunks (one or two sentences) embed one idea and match precisely; big chunks give the model the surrounding conditions, definitions and exceptions. You get both.
- **Mechanics:** at ingestion store `child_id -> parent_id` and keep parents in a document store. At query time search children, map hits to parents, dedupe parents (three hits in one section should send that section once), then apply the token budget (Q25).
- **Variants:** return a sentence window (the hit plus n neighbours) or the whole section.
- **Trade-offs:** more tokens per hit, so a smaller k of parents; large parents can bring in noise and push the answer into the middle of the prompt; two stores to keep in sync (delete children and parents together, Q20).
- **When it helps:** policy and legal text, manuals, anything where the answer depends on the sentence before or after. It helps little when each chunk is already self-contained, such as FAQ entries.

**Example:** TOY (hashed bag-of-words, synthetic 3-section policy; each section split into sentences). For "refunds processing takes how many days" the top-3 children came from refund#1, ship#1 and refund#1 again; mapping to parents and deduping returned refund#1 and ship#1. The matched child was 7 words; its parent was 22 words with the neighbouring facts (payment method, gift cards).

**Code:** (run; toy embedder)
```python
import numpy as np, re, hashlib
# TOY embedder: hashed bag of words (lexical only, not semantic)
def emb(t, D=1024):
    v = np.zeros(D)
    for w in re.findall(r"[a-z0-9]+", t.lower()):
        v[int(hashlib.md5(w.encode()).hexdigest(), 16) % D] += 1
    return v / (np.linalg.norm(v) + 1e-9)

# synthetic parent sections (each has 3 sentences)
parents = {
 "refund#1": "Refunds are issued to the original payment method. Processing takes 5 to 7 business days. Gift cards are refunded as store credit.",
 "ship#1":   "Standard shipping takes 3 to 5 business days. Express shipping is available for an extra fee. Orders over 999 rupees ship free.",
 "warr#1":   "All laptops carry a one year warranty. The warranty covers battery defects. Accidental damage is not covered.",
}
# children = single sentences, with a child -> parent map
children, child2parent = [], {}
for pid, text in parents.items():
    for j, s in enumerate([x.strip() + "." for x in text.split(".") if x.strip()]):
        cid = f"{pid}/s{j}"; children.append((cid, s)); child2parent[cid] = pid
CV = np.stack([emb(s) for _, s in children])

def small_to_big(q, k_children=3, max_parents=2):
    sc = CV @ emb(q)
    top = np.argsort(-sc)[:k_children]
    seen, out = [], []
    for i in top:
        pid = child2parent[children[i][0]]
        if pid not in seen:                    # dedupe parents
            seen.append(pid); out.append(pid)
    return [children[i][0] for i in top], out[:max_parents]

q = "refunds processing takes how many days"
hit_children, ps = small_to_big(q)
print("child hits:", hit_children)
print("parents returned (deduped):", ps)
print("context words, child only:", len(children[[c for c, _ in children].index(hit_children[0])][1].split()),
      "| parent:", len(parents[ps[0]].split()))
```
Output (my run):
```
child hits: ['refund#1/s1', 'ship#1/s0', 'refund#1/s0']
parents returned (deduped): ['refund#1', 'ship#1']
context words, child only: 7 | parent: 22
```

**Follow-ups:**
- *How is it different from just bigger chunks?* Retrieval is scored on small units, so the match is sharper, and the context size is decoupled from the embedding size.
- *How do you know it helps?* Compare recall and answer quality with and without it on the golden set (Q10).

**Common mistakes:** forgetting to dedupe parents so one section fills the whole context; returning parents far larger than the budget; no child-to-parent map persisted, so a re-ingest breaks links; using it where chunks are already self-contained.

### Q19 ⭐⭐ 🟡 What does a good ingestion pipeline do (cleaning, boilerplate removal, deduplication, versioning, stable chunk IDs)?
**Asked at:** product, GCC, platform teams
**Say this first (1 line):** A good ingestion pipeline is parse, clean, remove boilerplate, dedupe (exact and near), chunk, and write chunks with stable ids and version metadata, so re-running it never creates duplicates and updates can be applied cleanly.

**Then explain:**
- **Clean and strip boilerplate:** nav bars, cookie text, page numbers, repeated legal footers. They add noise and false matches.
- **Exact dedupe:** hash the cleaned text (SHA-256) and skip documents already seen.
- **Near-duplicate dedupe:** split into word shingles and compare Jaccard similarity (intersection over union); above a threshold keep one. The threshold is a tuning choice; check what you drop.
- **Stable chunk ids:** `doc_id` plus a hash of the chunk content (or doc id plus offset and version). The same input then gives the same ids, so re-running is idempotent and updates are targeted.
- **Metadata:** `doc_id`, source, section, page, version, doc hash, ingest time, ACL (Q15).
- **Operations:** log counts of added and skipped, keep a manifest of doc hashes, make the job resumable and safe to run twice.

**Example:** SYNTHETIC: four documents: an HR policy with a header and footer, an exact copy, a mirror with two small edits, and an IT guide. Run 1 added 6 chunks and skipped 2 documents (the copy and the mirror, whose shingle Jaccard was 0.68 against a demo threshold of 0.6). Run 2 on the same input added 0 and skipped 4, and the ids were unchanged.

**Code:** (run; standard library only)
```python
import hashlib, re
def sha(t): return hashlib.sha256(t.encode()).hexdigest()
def clean(raw):
    lines = [l.strip() for l in raw.splitlines()]
    boiler = {"Home | Products | Contact", "Copyright 2026 Acme Ltd. All rights reserved."}  # synthetic boilerplate
    lines = [l for l in lines if l and l not in boiler and not re.fullmatch(r"Page \d+", l)]
    return " ".join(lines)
def shingles(t, n=3):
    w = t.lower().split(); return {" ".join(w[i:i+n]) for i in range(max(1, len(w)-n+1))}
def jaccard(a, b): return len(a & b) / len(a | b)
def chunks(text, size=12):
    w = text.split(); return [" ".join(w[i:i+size]) for i in range(0, len(w), size)]

def ingest(docs, index, seen_hashes, version="v1", near_dup=0.6):
    added = skipped = 0
    kept_shingles = [s for s in index.get("_sh", [])]
    for doc_id, raw in docs.items():
        text = clean(raw); h = sha(text)
        if h in seen_hashes:                      # exact duplicate (or unchanged re-run)
            skipped += 1; continue
        sh = shingles(text)
        if any(jaccard(sh, o) >= near_dup for o in kept_shingles):  # near-duplicate
            skipped += 1; continue
        seen_hashes.add(h); kept_shingles.append(sh)
        for j, c in enumerate(chunks(text)):
            cid = f"{doc_id}:{sha(c)[:8]}"       # stable id: doc id + content hash
            index[cid] = {"text": c, "doc": doc_id, "pos": j, "version": version, "doc_hash": h[:8]}
            added += 1
    index["_sh"] = kept_shingles
    return added, skipped

body = "Employees may carry over five unused leave days into the next calendar year. Carry over requests must be approved by the manager before March. Unused days beyond five lapse on the last day of December."
docs = {
  "hr-policy": "Home | Products | Contact\nPage 1\n" + body + "\nCopyright 2026 Acme Ltd. All rights reserved.",
  "hr-policy-copy": body,                                           # exact duplicate after cleaning
  "hr-policy-mirror": body.replace("five", "5", 1).replace("March", "March 31"),  # near duplicate
  "it-guide": "Reset your password from the self service portal. Passwords expire every ninety days. Contact the service desk if you are locked out of your account after three attempts.",
}
index, seen = {}, set()
print("run 1 (added, skipped):", ingest(docs, index, seen))
ids1 = sorted(k for k in index if k != "_sh")
print("run 2 same input (added, skipped):", ingest(docs, index, seen), "| ids unchanged:", ids1 == sorted(k for k in index if k != "_sh"))
print("chunk count:", len(ids1), "| docs indexed:", sorted({index[i]["doc"] for i in ids1})); print("sample id:", ids1[0])
print("jaccard(original, mirror) =", round(jaccard(shingles(clean(docs["hr-policy"])), shingles(clean(docs["hr-policy-mirror"]))), 2))
```
Output (my run):
```
run 1 (added, skipped): (6, 2)
run 2 same input (added, skipped): (0, 4) | ids unchanged: True
chunk count: 6 | docs indexed: ['hr-policy', 'it-guide']
sample id: hr-policy:43e73bc4
jaccard(original, mirror) = 0.68
```

**Follow-ups:**
- *Why not random UUIDs for chunks?* Re-running would create new ids and duplicates, and you could not find the old chunks of a document to replace.
- *At scale, near-dup detection?* Pairwise Jaccard is quadratic; MinHash with locality-sensitive hashing is the usual approach (from memory, standard technique).

**Common mistakes:** dedupe thresholds picked without looking at what is dropped (a mirror with a different effective date is not a duplicate); content-only hashes that merge identical text from different documents with different ACLs; no version field; non-idempotent jobs.

### Q20 ⭐⭐ 🟡 How do you keep a RAG index fresh (incremental updates, deletes, tombstones), and what happens when deleted documents still surface?
**Asked at:** product, GCC, platform teams
**Say this first (1 line):** Tie every chunk to its document id and version, update a document by deleting its old chunks and inserting the new ones, and handle removals with deletes or tombstones; otherwise old chunks stay in the index and outdated or deleted text keeps surfacing.

**Then explain:**
- **Why stale chunks survive:** if chunk ids come from content hashes, an edited paragraph gets a new id and the old chunk stays. Upserting by id replaces nothing. This is the failure mode the prep articles flag: deleted or updated documents still surface.
- **Update:** delete by `doc_id` (or by filter), then insert the new chunks; or insert the new version and switch a `current_version` flag atomically, then clean up the old.
- **Delete:** hard delete by doc id, or a tombstone (a marker saying "deleted") that the query filter excludes, with a background job that removes the data later. Some ANN stores mark deletes lazily, so check how your store handles them.
- **TTL:** an expiry timestamp on chunks (news, prices); a filter excludes expired chunks, a job removes them.
- **Reindex:** schedule full rebuilds for chunking or model changes (Q21); a periodic reconciliation compares doc ids in the source against the index and fixes drift.
- **Compliance:** deletions for legal reasons need proof, so log them and verify that no chunk with that doc id remains, including caches and backups.

**Example:** Toy store (word overlap, not embeddings). A 13-word policy changed "30 days" to "60 days". With upsert-only and content-hash ids the store held 4 chunks and the query "notice period days" returned both the 30-day and 60-day chunks. With delete-then-insert by doc id the store held 3 chunks and only the 60-day chunk came back; deleting the document left 0 chunks.

**Code:** (run; toy store, no vector DB)
```python
import hashlib
# Toy in-memory "vector store": dict id -> {text, doc}; search by word overlap (toy, lexical).
def make_chunks(doc_id, text, size=6):
    w = text.split()
    return {f"{doc_id}:{hashlib.sha256(' '.join(w[i:i+size]).encode()).hexdigest()[:6]}": {"text": " ".join(w[i:i+size]), "doc": doc_id}
            for i in range(0, len(w), size)}
def search(store, q):
    qs = set(q.lower().split())
    sc = {i: len(qs & set(v["text"].lower().split())) for i, v in store.items()}
    return [(i, store[i]["text"]) for i in sorted(sc, key=sc.get, reverse=True) if sc[i] > 0][:3]

v1 = "Notice period is 30 days for all staff. Bonus is paid in April each year."
v2 = "Notice period is 60 days for all staff. Bonus is paid in April each year."

# A) upsert-only: ids are content hashes, so changed chunks get NEW ids and old ones stay
store = {}; store.update(make_chunks("hr", v1)); store.update(make_chunks("hr", v2))
print("upsert only -> chunks in store:", len(store))
print(" notice-period hits:", [t for _, t in search(store, "notice period days")][:2])

# B) delete-then-insert by doc id, then reindex
store = {}; store.update(make_chunks("hr", v1))
def update_doc(store, doc_id, new_text):
    for i in [i for i, v in store.items() if v["doc"] == doc_id]:
        del store[i]                             # real DBs: delete by metadata filter or tombstone
    store.update(make_chunks(doc_id, new_text))
update_doc(store, "hr", v2)
print("delete-then-insert -> chunks in store:", len(store))
print(" notice-period hits:", [t for _, t in search(store, "notice period days")][:2])
# delete a whole document
update_doc(store, "hr", "")
print("after deleting doc 'hr', chunks left:", len(store))
```
Output (my run):
```
upsert only -> chunks in store: 4
 notice-period hits: ['Notice period is 30 days for', 'Notice period is 60 days for']
delete-then-insert -> chunks in store: 3
 notice-period hits: ['Notice period is 60 days for']
after deleting doc 'hr', chunks left: 0
```

**Follow-ups:**
- *How do you notice stale answers?* Add a doc-id and version to every citation, and run a canary test: edit a fact, re-ingest, and query it.
- *Deletes in the middle of a query?* Eventually consistent stores can still return a doc for a short time; use the filter, not only physical deletion, for hard guarantees.

**Common mistakes:** upsert-only updates; chunk ids unrelated to doc ids; deleting from the vector index but not from the cache, parent store or keyword index; no reconciliation job.

### Q21 ⭐⭐ 🟡 What happens when you change the embedding model? How do you migrate an index safely?
**Asked at:** product, platform teams, GenAI startups
**Say this first (1 line):** Vectors from different embedding models live in different spaces (often with different dimensions), so you cannot mix them; you migrate by building a second index with the new model, backfilling, shadow-evaluating on the golden set, cutting over, and keeping the old index for rollback.

**Then explain:**
- **Why incompatible:** each model learns its own coordinate system. Even with the same dimension, cosine between a vector from model A and one from model B is meaningless. Different dimensions fail with a shape error or, worse, a silent truncation. See B1P07-Q49 for embedding operations in general.
- **Safe migration:** (1) create a new index or collection; (2) re-embed all documents with the new model (backfill), and dual-write new or changed documents to both; (3) shadow queries: send live traffic to both and compare recall and answer quality on the golden set (Q10); (4) switch queries atomically (blue-green); (5) keep the old index until the new one has proven stable; then delete.
- **Query side:** the query encoder must switch at the same moment as the index you point it at; a config flag naming the model per index prevents mismatches.
- **Cost:** re-embedding the whole corpus is a real compute and time bill; estimate chunks times tokens first.
- **Record the model name and version** in index metadata, so a mismatch can be detected.

**Example:** SYNTHETIC unit vectors (d=64, 3,000 docs, 300 queries): with one model recall@10 was 1.0; after rotating only the document vectors by a random orthogonal matrix (standing in for a different model) it fell to 0.0 (chance is about 0.003); rotating both restored 1.0. A 48-dim query against the 64-dim index raised a ValueError. A rotation of both is just a change of axes, which is why consistency is what matters, not the direction of the axes.

**Code:** (run, numpy, synthetic)
```python
import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: documents and queries are noisy views of "topics"; unit vectors in d=64
N, d, K = 3000, 64, 10
docs = rng.standard_normal((N, d)); docs /= np.linalg.norm(docs, axis=1, keepdims=True)
target = rng.integers(0, N, 300)                       # each query's one relevant doc
Q = docs[target] + 0.8 * rng.standard_normal((300, d)) / np.sqrt(d)
Q /= np.linalg.norm(Q, axis=1, keepdims=True)
def recall(D, Qm):
    top = np.argsort(-(Qm @ D.T), axis=1)[:, :K]
    return np.mean([t in row for t, row in zip(target, top)])
R, _ = np.linalg.qr(rng.standard_normal((d, d)))        # random orthogonal matrix = a "different model"
print("same model for both          recall@10:", round(recall(docs, Q), 3))
print("docs rotated, queries not    recall@10:", round(recall(docs @ R, Q), 3), "(old queries vs new doc vectors)")
print("both rotated (consistent)    recall@10:", round(recall(docs @ R, Q @ R), 3))
print("random chance level:", K / N)
try:
    Q_new_dim = rng.standard_normal((1, 48)) @ docs.T      # a 48-dim query against a 64-dim index
except ValueError as e:
    print("dimension mismatch ->", type(e).__name__, str(e)[:70])
```
Output (my run):
```
same model for both          recall@10: 1.0
docs rotated, queries not    recall@10: 0.0 (old queries vs new doc vectors)
both rotated (consistent)    recall@10: 1.0
random chance level: 0.0033333333333333335
dimension mismatch -> ValueError matmul: Input operand 1 has a mismatch in its core dimension 0, with g
```

**Follow-ups:**
- *Can you learn a mapping between the two spaces?* It is a research-style shortcut with quality loss; for production, re-embed.
- *How do you avoid downtime?* Blue-green: the old index serves while the new one fills.

**Common mistakes:** upgrading the query encoder only; mixing old and new vectors in one index; no model version in metadata; cutting over without evaluating; deleting the old index immediately.

### Q22 ⭐⭐ 🟡 What are asymmetric query and document embeddings (instruction prefixes, query length, normalisation), and why do they matter?
**Asked at:** product, GenAI startups
**Say this first (1 line):** Queries are short questions and documents are long passages, so many embedding models are trained asymmetrically (query and document prefixes or separate encoders); follow the model card, and apply the same normalisation to both sides so the similarity score does not depend on vector length.

**Then explain:**
- **Asymmetry:** a query like "refund time" and a passage about refunds are different kinds of text. Some models expect an instruction or prefix on the query, on the document, or on both; some use two encoders. Which ones, and the exact strings, differ by model: check the model card and test with and without.
- **Same preprocessing:** use the same tokenizer, truncation and max length rules at index and query time, and do not skip the prefix for one side. A forgotten prefix usually degrades quality quietly with no error.
- **Normalisation:** if the index uses dot product, vectors with a large norm win regardless of meaning. L2-normalise both sides (then dot product equals cosine) unless the model card says otherwise. See B1P07-Q16 on metrics.
- **Query length:** very short or vague queries embed poorly; query rewriting or expansion (Part 7) can help.
- **Long documents:** the embedder truncates at its max input length, so text beyond it is invisible; chunk to fit.

**Example:** SYNTHETIC vectors: 1,000 docs, 20 of them with a 5x larger norm (2 percent of the corpus). Raw dot product put a big-norm doc at top-1 for 95 percent of queries and found the true neighbour only 4 percent of the time; cosine got 100 percent with 0 percent big-norm top-1. Scaling only the query changed no ranking, since the query norm multiplies every score equally.

**Code:** (run, numpy, synthetic)
```python
import numpy as np
rng = np.random.default_rng(1)
# SYNTHETIC vectors, no real model. 1000 docs, 20 of them have a 5x larger norm (think: long docs, or a model that does not normalise).
N, d = 1000, 32
D = rng.standard_normal((N, d)); D /= np.linalg.norm(D, axis=1, keepdims=True)
big = rng.choice(N, 20, replace=False)
D[big] *= 5.0
# 200 queries; each query's true neighbour is a random doc that is NOT a big one
others = np.setdiff1d(np.arange(N), big)
tgt = rng.choice(others, 200)
Dn = D / np.linalg.norm(D, axis=1, keepdims=True)
Q = Dn[tgt] + 0.5 * rng.standard_normal((200, d)) / np.sqrt(d); Q /= np.linalg.norm(Q, axis=1, keepdims=True)
for name, S in [("raw dot product", Q @ D.T), ("cosine", Q @ Dn.T)]:
    top1 = S.argmax(1)
    print(f"{name:16s} top-1 correct: {np.mean(top1 == tgt):.2f} | top-1 is a big-norm doc: {np.mean(np.isin(top1, big)):.2f}")
print("big-norm docs are 2% of the corpus")
# normalising only the documents but not the queries is harmless for ranking (query norm scales all scores equally)
S2 = (3.0 * Q) @ Dn.T
print("same ranking when only the query is scaled:", bool((S2.argmax(1) == (Q @ Dn.T).argmax(1)).all()))
```
Output (my run):
```
raw dot product  top-1 correct: 0.04 | top-1 is a big-norm doc: 0.95
cosine           top-1 correct: 1.00 | top-1 is a big-norm doc: 0.00
big-norm docs are 2% of the corpus
same ranking when only the query is scaled: True
```

**Follow-ups:**
- *Does this matter for cosine indexes?* If the store normalises internally, usually not, but still check how it treats vectors.
- *How would you detect a missing prefix?* Compare recall on the golden set with and without; the drop shows.

**Common mistakes:** assuming all models want the same prefixes (or none); normalising documents but not queries in a dot-product index; truncating silently at the max length; mixing prefixed and unprefixed vectors in one index.

### Q23 ⭐⭐ 🟡 How do embedding dimension, truncation and quantisation affect quality and storage? Work through the storage maths.
**Asked at:** product, platform teams, GenAI startups
**Say this first (1 line):** Memory is N x d x bytes per vector, so dimension and precision set your cost; you can shrink with fewer dimensions, int8 or binary quantisation, or PQ, usually at some recall cost that you must measure against exact search on your own data.

**Then explain:**
- **Maths:** fp32 = 4 B, fp16 = 2 B, int8 = 1 B, 1-bit = d/8 B, PQ = number of codes (one byte each in the usual setup). For d=768 that is 3,072, 1,536, 768, 96 and (for 96 codes) 96 bytes per vector.
- **Scale:** 100M x 768 x 4 B is about 307 GB raw (not "low terabytes", as one prep article says); 10M is about 31 GB. HNSW graph links and metadata add on top, so budget more than the raw figure.
- **Truncating dimensions:** only safe if the model was trained for it (Matryoshka-style training, from memory, packs the most information in the leading coordinates; check the model card). Cutting arbitrary models naively can hurt a lot.
- **Quantisation:** int8 usually costs little recall; binary and PQ cost more and are often followed by reranking a shortlist with full vectors.
- **Always measure** recall@k against exact search on sampled production queries; the same compression behaves differently on different data.

**Example:** SYNTHETIC data (20,000 vectors of 256 dims, built to have low intrinsic dimension; real data may differ). Recall@10 versus exact fp32 search: naive truncation to 128 dims 0.46, to 64 dims 0.26; PCA to 64 dims 0.99, to 32 dims 0.54; int8 0.98; 1-bit sign 0.41. The contrast between naive truncation and PCA shows why you cannot cut dimensions blindly.

**Code:** (run, numpy; storage numbers are exact arithmetic, recall numbers are synthetic)
```python
import numpy as np
# Storage maths (decimal GB = 1e9 bytes). Raw vectors only; indexes (HNSW graph etc.) add overhead.
def gb(n, bytes_per_vec): return n * bytes_per_vec / 1e9
d = 768
sizes = {"fp32": d*4, "fp16": d*2, "int8": d*1, "1-bit": d/8, "PQ 96 codes x 1 B": 96}
print(f"{'format':20s}{'B/vec':>8s}{'10M (GB)':>11s}{'100M (GB)':>11s}")
for k, b in sizes.items():
    print(f"{k:20s}{b:8.0f}{gb(10e6, b):11.1f}{gb(100e6, b):11.1f}")

# SYNTHETIC recall@10 vs exact fp32 search. Data has low intrinsic dimension (like many real embeddings, an assumption) 
rng = np.random.default_rng(0)
N, d, r, K = 20000, 256, 48, 10
Z = rng.standard_normal((N, r)) @ rng.standard_normal((r, d))
X = Z + 0.2 * rng.standard_normal((N, d)); X /= np.linalg.norm(X, axis=1, keepdims=True)
Q = X[rng.choice(N, 100, replace=False)] + 0.3 * rng.standard_normal((100, d)) / np.sqrt(d)
Q /= np.linalg.norm(Q, axis=1, keepdims=True)
exact = np.argsort(-(Q @ X.T), axis=1)[:, :K]
def rec(Xa, Qa):
    top = np.argsort(-(Qa @ Xa.T), axis=1)[:, :K]
    return np.mean([len(set(a) & set(b)) / K for a, b in zip(exact, top)])
for m in (256, 128, 64, 32):                      # naive truncation of leading coordinates
    print(f"truncate to first {m:3d} dims: recall@10 = {rec(X[:, :m], Q[:, :m]):.2f}")
# PCA to m dims (fit on the corpus)
mu = X.mean(0); U, S, Vt = np.linalg.svd(X - mu, full_matrices=False)
for m in (64, 32):
    P = Vt[:m].T
    print(f"PCA to {m:3d} dims:             recall@10 = {rec((X-mu)@P, (Q-mu)@P):.2f}")
def int8(A, scale):  return np.clip(np.round(A / scale * 127), -127, 127).astype(np.int8)
scale = np.abs(X).max()
Xq, Qq = int8(X, scale).astype(np.float32), int8(Q, scale).astype(np.float32)
print(f"int8 (scalar quantised):       recall@10 = {rec(Xq, Qq):.2f}")
sign = lambda A: (A > 0).astype(np.float32) * 2 - 1
print(f"1-bit (sign) dot product:      recall@10 = {rec(sign(X), sign(Q)):.2f}")
```
Output (my run):
```
format                 B/vec   10M (GB)  100M (GB)
fp32                    3072       30.7      307.2
fp16                    1536       15.4      153.6
int8                     768        7.7       76.8
1-bit                     96        1.0        9.6
PQ 96 codes x 1 B         96        1.0        9.6
truncate to first 256 dims: recall@10 = 1.00
truncate to first 128 dims: recall@10 = 0.46
truncate to first  64 dims: recall@10 = 0.26
truncate to first  32 dims: recall@10 = 0.17
PCA to  64 dims:             recall@10 = 0.99
PCA to  32 dims:             recall@10 = 0.54
int8 (scalar quantised):       recall@10 = 0.98
1-bit (sign) dot product:      recall@10 = 0.41
```

**Follow-ups:**
- *Does lower recall in the index mean worse answers?* Not one-for-one; check end-to-end on the golden set, and note a reranker can recover some loss.
- *When is PQ worth it?* Hundreds of millions of vectors where RAM is the constraint (Q8).

**Common mistakes:** forgetting index overhead; copying "low terabytes" figures; truncating dimensions on a model not trained for it; judging compression by memory saved without measuring recall; mixing fp32 queries with quantised vectors without scaling.

### Q24 ⭐⭐ 🟡 How do you tune top-k: fixed vs adaptive k, similarity thresholds, deduplicating near-identical chunks, and MMR diversification?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Fixed k is a simple starting point; better is to retrieve a few more than you need, drop low scores and near-duplicates, optionally diversify with MMR, and cut at a score gap, then let the token budget have the final say.

**Then explain:**
- **Fixed k:** easy and predictable, but too many chunks on easy queries add noise and cost, and too few on hard ones miss evidence.
- **Threshold:** drop chunks below a similarity score. The scale depends on the embedder, so calibrate on a golden set (Q27, Q9); do not copy a threshold from a blog.
- **Adaptive k (elbow):** sort scores and cut at the largest drop; use a minimum gap and a fall-back to a fixed k when the tail is flat.
- **Near-duplicates:** overlap, mirrors and repeated boilerplate fill the top-k with the same text; dedupe (Q16, Q19).
- **MMR (maximal marginal relevance):** pick the chunk that maximises lambda x sim(query, chunk) - (1 - lambda) x max sim(chunk, already selected). lambda=1 is plain top-k; lower values trade relevance for diversity.
- **Tune k by** retrieval recall@k and answer quality on the golden set (Q10), plus latency and cost.

**Example:** SYNTHETIC: 14 vectors in 3 topics (8 near-duplicates of topic 0, 3 each of topics 1 and 2). For k=4, lambda 1.0 picked four chunks from topic 0 (mean pairwise similarity 0.98); lambda 0.7 got 2 topics; lambda 0.5 got all 3 topics (mean pairwise similarity 0.15). On made-up sorted scores, an elbow rule with minimum gap 0.15 chose k=3 for [0.82, 0.79, 0.77, 0.41, ...] and fell back to 5 for a flat tail.

**Code:** (run, numpy, synthetic)
```python
import numpy as np
rng = np.random.default_rng(3)
# SYNTHETIC: 3 topics; topic 0 has 8 near-duplicate chunks, topics 1 and 2 have 3 each. Query is closest to topic 0.
d = 24
centres = rng.standard_normal((3, d)); centres /= np.linalg.norm(centres, axis=1, keepdims=True)
def pts(c, n, noise):
    p = c + noise * rng.standard_normal((n, d)) / np.sqrt(d); return p / np.linalg.norm(p, axis=1, keepdims=True)
X = np.vstack([pts(centres[0], 8, 0.15), pts(centres[1], 3, 0.15), pts(centres[2], 3, 0.15)])
topic = np.array([0]*8 + [1]*3 + [2]*3)
q = 0.7*centres[0] + 0.5*centres[1] + 0.4*centres[2]; q /= np.linalg.norm(q)

def mmr(q, X, k, lam):
    sim_q = X @ q; sel = []
    cand = list(range(len(X)))
    while len(sel) < k:
        def score(i):
            red = max((X[i] @ X[j] for j in sel), default=0.0)
            return lam * sim_q[i] - (1 - lam) * red
        best = max(cand, key=score); sel.append(best); cand.remove(best)
    return sel
for lam in (1.0, 0.7, 0.5):
    sel = mmr(q, X, 4, lam)
    print(f"lambda={lam}: picked topics {topic[sel].tolist()} | distinct topics {len(set(topic[sel]))} | mean pairwise sim {np.mean([X[a]@X[b] for i,a in enumerate(sel) for b in sel[i+1:]]):.2f}")

# adaptive k by largest score gap, on made-up sorted scores for two queries
for name, sc in [("query with a clear elbow", [0.82, 0.79, 0.77, 0.41, 0.39, 0.38, 0.37]),
                 ("query with a flat tail  ", [0.52, 0.51, 0.50, 0.49, 0.48, 0.47, 0.46])]:
    sc = np.array(sc); gaps = sc[:-1] - sc[1:]
    k = int(np.argmax(gaps)) + 1 if gaps.max() > 0.15 else 5     # min gap 0.15 (made up); else fall back to fixed k=5
    print(name, "-> k =", k)
```
Output (my run):
```
lambda=1.0: picked topics [0, 0, 0, 0] | distinct topics 1 | mean pairwise sim 0.98
lambda=0.7: picked topics [0, 1, 0, 0] | distinct topics 2 | mean pairwise sim 0.56
lambda=0.5: picked topics [0, 2, 1, 0] | distinct topics 3 | mean pairwise sim 0.15
query with a clear elbow -> k = 3
query with a flat tail   -> k = 5
```

**Follow-ups:**
- *Is MMR always good?* Not for a question with one precise answer; diversity then pushes the right chunk out. Use it for broad or multi-aspect questions.
- *Reranking?* Retrieve more, rerank to a small k (Part 7).

**Common mistakes:** one global threshold copied from another model; ignoring duplicates; MMR with lambda too low; tuning k only on retrieval metrics and not on answer quality.

### Q25 ⭐⭐ 🟡 How do you assemble the context for the prompt (ordering, token budget, truncation, the lost-in-the-middle effect)?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Assemble the prompt under a token budget: rank chunks, pack greedily by score within the budget left after the system prompt, question and answer room, drop whole chunks rather than cutting them silently, and place the strongest evidence at the start or end because long contexts under-use the middle.

**Then explain:**
- **Budget:** context window minus system prompt, question, chat history and answer room. Count tokens with the model's tokenizer; larger contexts cost more and add latency.
- **Packing:** sort by score and add chunks while they fit; a chunk that does not fit may be skipped in favour of a smaller one that does. Dedupe first (Q24).
- **Truncation policy:** drop lowest-scored whole chunks first; if you must cut a chunk, cut at a sentence boundary and mark it as truncated; never cut a table row or a number.
- **Ordering:** lost-in-the-middle (Part 1 Q19) is a reported effect where models use information in the middle of a long context less well; so put the best chunks first and last, keep k small, and do not rely on it as a law for every model.
- **Format:** label each chunk with an id and source (needed for citations, Q26), and separate chunks clearly from instructions.
- **Compress** only if needed (summarise or extract), as it can lose details.

**Example:** Made-up chunks: lengths 60, 50, 45, 30, 20 words and scores 0.91, 0.85, 0.80, 0.74, 0.60; a 200-token budget with 40 reserved (word-count proxy). The packer took c1, c2, c3 (155 words, 5 left) and dropped c4 and c5 because they did not fit. The ordering helper gave c1, c3, c2: best chunk first, second-best last, weakest in the middle.

**Code:** (run; word-count proxy for tokens)
```python
# Word-count proxy for tokens (real systems count with the model's tokenizer).
def n_tokens(text): return len(text.split())

def pack(chunks, budget, reserve=40, min_score=0.0):
    """chunks: list of (id, score, text). Greedy by score under a budget; reserve covers system prompt + question + answer room."""
    room = budget - reserve; picked, dropped = [], []
    for cid, sc, text in sorted(chunks, key=lambda c: -c[1]):
        if sc < min_score: dropped.append((cid, "below threshold")); continue
        t = n_tokens(text)
        if t <= room: picked.append((cid, sc, text)); room -= t
        else: dropped.append((cid, f"needs {t}, only {room} left"))
    return picked, dropped, room

def order_for_prompt(picked):
    """Best evidence at the start and second-best at the end; weakest in the middle (lost-in-the-middle mitigation)."""
    by = sorted(picked, key=lambda c: -c[1]); front, back = [], []
    for i, c in enumerate(by): (front if i % 2 == 0 else back).append(c)
    return front + back[::-1]

chunks = [("c1", 0.91, "w " * 60), ("c2", 0.85, "w " * 50), ("c3", 0.80, "w " * 45),
          ("c4", 0.74, "w " * 30), ("c5", 0.60, "w " * 20)]   # made-up scores and lengths
picked, dropped, room = pack(chunks, budget=200)
print("picked:", [(c, s) for c, s, _ in picked], "| tokens left:", room)
print("dropped:", dropped)
print("prompt order:", [c for c, _, _ in order_for_prompt(picked)])
# truncation policy: never cut a chunk silently mid-sentence; drop whole chunks, or cut at a sentence boundary and mark it
def truncate_to(text, limit):
    out = []
    for s in text.split(". "):
        if n_tokens(" ".join(out + [s])) > limit: break
        out.append(s)
    return ". ".join(out) + (" [...truncated]" if len(out) < len(text.split(". ")) else "")
print(truncate_to("Alpha beta gamma. Delta epsilon zeta eta. Theta iota kappa lambda mu.", 8))
```
Output (my run):
```
picked: [('c1', 0.91), ('c2', 0.85), ('c3', 0.8)] | tokens left: 5
dropped: [('c4', 'needs 30, only 5 left'), ('c5', 'needs 20, only 5 left')]
prompt order: ['c1', 'c3', 'c2']
Alpha beta gamma. Delta epsilon zeta eta [...truncated]
```

**Follow-ups:**
- *Why not just fill the window?* Cost, latency, and more distracting text; quality can fall with irrelevant chunks.
- *What if the top chunk alone exceeds the budget?* Use parent or window logic in reverse: trim to the matching section (Q18).

**Common mistakes:** counting words or characters as tokens; ignoring the answer room; silent mid-sentence cuts; burying the best evidence in the middle; no chunk ids in the prompt.

### Q26 ⭐⭐ 🟡 How do you produce reliable citations and attribution in RAG (chunk IDs, span-level citations, verifying that a citation supports the claim)?
**Asked at:** product, GCC, regulated-industry teams
**Say this first (1 line):** Number the retrieved chunks in the prompt, require an [id] after each claim, then verify after generation that every cited id exists and that the chunk actually supports the claim, because models can cite a real chunk that does not say what they claim.

**Then explain:**
- **Prompt side:** give each chunk a short id with its source, instruct "cite chunk ids for every factual statement; if the context does not contain the answer, say so" (see Q12).
- **Validity check:** parse the citations; reject ids that were not in the prompt.
- **Support check:** for each claim and cited chunk, test entailment. Real systems use an NLI model (natural language inference: does the text imply the claim?) or an LLM judge; Part 9 covers faithfulness evaluation. A lexical overlap check is only a weak proxy.
- **Span-level citations:** store chunk offsets (Q16) so you can highlight the exact sentence, or ask the model to quote a short supporting phrase and check that the quote appears verbatim in the chunk.
- **UI:** show the doc title, page and version; link to the source. Citing a deleted or outdated document is a freshness bug (Q20).
- **Limits:** a citation shows where the claim came from, not that the claim is true; verifying also costs latency.

**Example:** TOY check on a mock answer with three cited claims. Claims one and two matched their chunks (overlap 0.86 and 0.67); the third, "unused days are paid out in cash at year end [2]", was cited to chunk 2 but shared no content words with it (overlap 0.00) and was flagged UNSUPPORTED. The 0.5 threshold is arbitrary; a paraphrase would fool this checker, which is why real systems use NLI or an LLM judge.

**Code:** (run; toy lexical checker, mock LLM output)
```python
import re
# TOY citation checker: lexical overlap is a weak proxy. Real systems use an NLI model or an LLM judge.
STOP = set("the a an is are was were of to in and or for on by with at it this that be as from".split())
def content(t): return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP}

chunks = {  # numbered chunks as they appear in the prompt (synthetic)
 1: ("policy.pdf#p3", "Employees may carry over five unused leave days into the next year."),
 2: ("policy.pdf#p4", "Carry over requests must be approved by the manager before March."),
 3: ("it.pdf#p1", "Passwords expire every ninety days and must be reset on the portal."),
}
answer = ("Employees can carry over five leave days [1]. Requests need manager approval before March [2]. "
          "Unused days are paid out in cash at year end [2].")          # last claim is NOT in chunk 2 (mock LLM output)

def check(answer, chunks, min_overlap=0.5):
    results = []
    for sent in re.split(r"(?<=[.])\s+", answer):
        ids = [int(x) for x in re.findall(r"\[(\d+)\]", sent)]
        claim = content(re.sub(r"\[\d+\]", "", sent))
        for i in ids:
            if i not in chunks: results.append((sent, i, "INVALID ID (not in prompt)")); continue
            ov = len(claim & content(chunks[i][1])) / max(1, len(claim))
            results.append((sent, i, f"{'supported' if ov >= min_overlap else 'UNSUPPORTED'} (overlap {ov:.2f})"))
        if not ids: results.append((sent, None, "NO CITATION"))
    return results
for s, i, verdict in check(answer, chunks): print(f"[{i}] {verdict:34s} <- {s[:55]}")
```
Output (my run):
```
[1] supported (overlap 0.86)           <- Employees can carry over five leave days [1].
[2] supported (overlap 0.67)           <- Requests need manager approval before March [2].
[2] UNSUPPORTED (overlap 0.00)         <- Unused days are paid out in cash at year end [2].
```

**Follow-ups:**
- *What if the model cites nothing?* Treat it as a failure case: retry, or fall back to an abstain answer.
- *Citations for multi-chunk claims?* Allow several ids per claim and check them jointly.

**Common mistakes:** trusting the model's citations without verification; citing by document rather than chunk or span; not storing offsets; using overlap as if it were entailment; showing citations for stale documents.

### Q27 ⭐⭐ 🟡 What should a RAG system do when retrieval finds nothing relevant (abstaining, score thresholds, fallbacks)?
**Asked at:** product, GCC, customer-facing teams
**Say this first (1 line):** When retrieval finds nothing relevant, the system should say so (abstain) instead of letting the LLM guess; set a score threshold calibrated on a golden set that includes unanswerable queries, and give fallbacks such as a broader search, a clarifying question or a human handoff.

**Then explain:**
- **Detect:** low top-1 score, a flat score profile, or no chunk passing the threshold. A second signal is the generator's own "I cannot find it" under a prompt that allows it (Q12).
- **Calibrate:** the threshold depends on the embedder and data. Build a golden set with answerable and unanswerable queries (Q10), sweep the threshold, and pick it by the cost of a wrong answer versus a wrong refusal.
- **Abstain template:** short and useful: "I could not find this in the documents I can access", the closest topics found, and how to get help. Do not invent a partial answer.
- **Fallbacks:** (1) one broader retry (drop filters you added, rewrite the query, add keyword search, Part 7); (2) a clarifying question if the query is ambiguous; (3) human handoff or ticket for customer-facing flows.
- **Check permissions too:** "nothing found" may mean nothing the user is allowed to see (Q15); do not reveal that a restricted document exists.
- **Monitor** the abstain rate in production; a jump often means a broken index or a data change.

**Example:** SYNTHETIC scores: 400 answerable queries (top-1 score about N(0.62, 0.10)) and 400 unanswerable (about N(0.42, 0.10)). At threshold 0.50, 89 percent of answerable queries were answered but 22 percent of unanswerable ones also were; at 0.60, 55 percent and 3 percent. Choosing the lowest threshold with at most 10 percent wrongly answered gave 0.56: 71 percent of answerable answered, 8 percent of unanswerable wrongly answered. That 10 percent target is a policy choice, not a law.

**Code:** (run, numpy, synthetic scores)
```python
import numpy as np
rng = np.random.default_rng(5)
# SYNTHETIC top-1 retrieval scores (cosine-like). Answerable queries tend to score higher, but the distributions overlap.
ans = np.clip(rng.normal(0.62, 0.10, 400), 0, 1)      # 400 answerable queries
una = np.clip(rng.normal(0.42, 0.10, 400), 0, 1)      # 400 unanswerable queries (golden set must include these)
print(f"{'threshold':>9s} {'answerable answered':>24s} {'wrongly answered (unanswerable)':>33s}")
for t in (0.30, 0.40, 0.50, 0.55, 0.60, 0.70):
    print(f"{t:9.2f} {np.mean(ans >= t):24.2f} {np.mean(una >= t):33.2f}")
# pick the lowest threshold that keeps wrongly-answered <= 10% (a policy choice, not a law)
ts = np.linspace(0.2, 0.9, 71)
t_star = next(t for t in ts if np.mean(una >= t) <= 0.10)
print(f"chosen threshold {t_star:.2f}: answers {np.mean(ans >= t_star):.0%} of answerable, wrongly answers {np.mean(una >= t_star):.0%} of unanswerable")

def respond(top_score, t=t_star):
    if top_score >= t: return "ANSWER from retrieved context"
    if top_score >= t - 0.10: return "ASK a clarifying question / broaden search once"
    return "ABSTAIN: 'I could not find this in the documents' + handoff"
for s in (0.70, 0.52, 0.30): print(s, "->", respond(s))
```
Output (my run):
```
threshold      answerable answered   wrongly answered (unanswerable)
     0.30                     1.00                              0.90
     0.40                     0.98                              0.59
     0.50                     0.89                              0.22
     0.55                     0.75                              0.10
     0.60                     0.55                              0.03
     0.70                     0.20                              0.00
chosen threshold 0.56: answers 71% of answerable, wrongly answers 8% of unanswerable
0.7 -> ANSWER from retrieved context
0.52 -> ASK a clarifying question / broaden search once
0.3 -> ABSTAIN: 'I could not find this in the documents' + handoff
```

**Follow-ups:**
- *Why not rely on the LLM to say "I don't know"?* It sometimes answers anyway from its own knowledge; combine a retrieval-side gate with the prompt.
- *Scores near the threshold?* Use a grey zone: ask a clarifying question or broaden search once.

**Common mistakes:** a threshold copied from another embedder; a golden set with no unanswerable queries; letting the model guess; refusing so often that users stop trusting the product; not logging abstentions.
