### Q41 ⭐⭐ 🟡 How do you monitor and debug a RAG system in production (retrieved chunk IDs and scores, per-stage latency, feedback loops)?
**Asked at:** product, GCC, platform teams
**Say this first (1 line):** I log one structured record per request, with the query, retrieved chunk ids and scores, prompt tokens, citations, answer, per-stage latency and any feedback. I then watch retrieval health, latency per stage, cost and user feedback on a dashboard, sample traces for human review, and turn bad cases into eval cases.

**Then explain:**
- **What I log per request** (one record, one request id, so any bad answer can be replayed):

| Field | Why |
|---|---|
| query (after redaction, see Q42), rewritten query | reproduce the case; spot query drift |
| retrieved chunk ids, scores, rank | the first thing I read when debugging (Q11) |
| index version, embedder version, prompt version | tells me if a deploy caused the change |
| prompt tokens, completion tokens | cost and truncation (context overflow) |
| citations and the final answer | check that cited ids were really retrieved |
| latency per stage: embed, search, rerank, generate | find which stage got slow |
| feedback: thumbs, copy, retry, escalation | the cheapest quality signal |

- **Dashboards and alerts:**
  - Latency: p50 and p95 per stage, not only end to end. A p95 jump in one stage points straight at the cause.
  - Retrieval health: distribution of top-1 score, share of queries with no chunk above the threshold (abstention rate), share of answers with zero citations.
  - Cost: prompt tokens per request, tokens per day.
  - Quality proxies: thumbs-down rate, retry rate, escalation-to-human rate, citation validity (every cited id is in the retrieved set).
  - Alert on a change against a baseline (for example p95 up more than 25 percent for 15 minutes), not only on fixed numbers.
- **Sampling for human review:** review a small random slice every week, plus all thumbs-down, plus low top-1 score, plus no-citation answers. Random alone misses rare failures; failure-biased alone gives a skewed picture of overall quality. I use both.
- **Drift:** query drift means users start asking about new things (new product, new topic), so my golden set (Q40) no longer represents traffic. I watch the mix of query clusters and the share of low-score queries. Embedding drift means the stored vectors and the live query vectors stop matching, usually after a silent embedder or preprocessing change (Q21). Fix by versioning the embedder and comparing score distributions before and after a deploy.
- **Feedback to eval cases:** every thumbs-down is a candidate. A human reads the retrieved chunks, labels the right chunk (or marks that the corpus has no answer), and the case enters the golden set with the label (Q40). Never add an unlabelled thumbs-down as ground truth, since users also downvote for tone or speed. LLMOps depth, tracing tools and online evals are in Part 11.
- **Privacy:** logs hold user text, so redact, set a retention period and restrict access (Q42).

**Example:** on Monday the support bot gets slower and nobody changed the prompt. End-to-end p95 says only "slower". The per-stage table shows search p95 going 44 to 80 ms in my synthetic run while generate is flat, so I look at the vector index (a rebuild left an unoptimised index, or a new filter) and not at the LLM. Without per-stage logs I would have wasted a day on the model.

**Code:** (executed, standalone, standard library; SYNTHETIC log records, so numbers are illustrative, timings are generated not measured)
```python
# Standalone, standard library only. SYNTHETIC logs (generated here), not real traffic.
import random, statistics
from dataclasses import dataclass, field

@dataclass
class RagLog:
    request_id: str
    query: str
    chunk_ids: list           # retrieved chunk ids, in rank order
    scores: list              # similarity scores, same order
    prompt_tokens: int
    answer: str
    citations: list           # chunk ids the answer cites
    latency_ms: dict          # per stage: embed, search, rerank, generate
    index_version: str = "v1"
    feedback: str = None      # "up", "down" or None

random.seed(7)
def make_logs(n, search_scale=1.0):
    logs = []
    for i in range(n):
        lat = {"embed": random.lognormvariate(3.0, 0.25),
               "search": random.lognormvariate(3.2, 0.35) * search_scale,
               "rerank": random.lognormvariate(4.2, 0.30),
               "generate": random.lognormvariate(6.3, 0.40)}
        logs.append(RagLog(f"r{i}", "toy query", [f"c{i}a", f"c{i}b"], [0.8, 0.6],
                           900, "toy answer", [f"c{i}a"], lat))
    return logs

def pct(vals, q):                       # nearest-rank percentile
    s = sorted(vals); return s[min(len(s) - 1, max(0, int(round(q / 100 * len(s) + 0.5)) - 1))]

def stage_table(logs):
    return {st: (pct([l.latency_ms[st] for l in logs], 50), pct([l.latency_ms[st] for l in logs], 95))
            for st in logs[0].latency_ms}

def regressions(base, cur, tol=1.25):
    out = []
    for st in base:
        b95, c95 = base[st][1], cur[st][1]
        if c95 > tol * b95: out.append((st, b95, c95, c95 / b95))
    return out

base = stage_table(make_logs(5000))                      # last week (synthetic)
cur = stage_table(make_logs(5000, search_scale=1.8))     # today: search stage made 1.8x slower on purpose
print("stage      base p50/p95 (ms)   today p50/p95 (ms)")
for st in base:
    print(f"{st:9s}  {base[st][0]:7.1f} /{base[st][1]:7.1f}   {cur[st][0]:7.1f} /{cur[st][1]:7.1f}")
for st, b, c, r in regressions(base, cur):
    print(f"ALERT: {st} p95 {b:.1f} -> {c:.1f} ms ({r:.2f}x, threshold 1.25x)")

# thumbs-down -> eval case (cross-ref Q40): keep query, retrieved ids, and a slot for a human label
logs = make_logs(3); logs[1].feedback = "down"
cases = [{"query": l.query, "retrieved": l.chunk_ids, "expected_chunk_ids": None, "note": "label me"}
         for l in logs if l.feedback == "down"]
print("eval cases from thumbs-down:", cases)
```

**Follow-ups:**
- *How do you know an answer was wrong without labels?* I cannot fully. I use proxies (thumbs, retries, no citation, low scores) to choose what humans review, and an LLM judge for broad sampling with a human check on a subset (Part 9).
- *What do you alert on first?* Errors and timeouts, then p95 per stage against baseline, then abstention rate and thumbs-down rate. Quality metrics are noisy, so I alert on trends over a window.
- *Can you log the full prompt?* Only if the privacy policy allows; otherwise log ids and token counts and rebuild the prompt from stored chunks and the prompt version.

**Common mistakes:** logging only the final answer (cannot debug retrieval); watching only end-to-end latency; averaging latency instead of using percentiles; treating all thumbs-down as ground truth; logging raw PII with no retention limit; no version fields, so a regression cannot be tied to a deploy.

### Q42 ⭐⭐ 🟡 What are the security and privacy risks in enterprise RAG (access control at retrieval, tenant isolation, PII in the index, logging)?
**Asked at:** product, GCC, regulated-industry and enterprise teams
**Say this first (1 line):** The retriever is a new data path to every document, so I enforce permissions inside retrieval (before ranking), derive the tenant from the authenticated session and never from the prompt, keep PII and secrets out of the index and logs, and test for leaks automatically. The model must never be the thing that decides who sees what.

**Then explain:**
- **Access control at retrieval (Q15):** store tenant, group or ACL on every chunk. Apply the predicate inside the search (pre-filter), not after top-k, or you leak less but also lose recall (Q44). Do not rely on "the prompt says only answer from this user's data": anything that reaches the prompt can be shown to the user.
- **Tenant isolation, three options:**

| Option | Strength | Cost |
|---|---|---|
| Filter on a tenant field in one shared index | simple, cheap, one index to run | one missing filter in one code path leaks; filtered ANN can be slow or lossy (Q44) |
| Namespace or partition per tenant (same cluster) | no query can cross unless the code picks the wrong namespace | many small indexes, more overhead |
| Separate index or cluster per tenant | strongest blast-radius limit, per-tenant keys and deletion | most expensive; for strict or regulated customers |

  I pick filters for many small tenants with low sensitivity, and separate namespaces or indexes for large or regulated tenants. Product support for these differs; check current docs.
- **Source of identity:** the filter value comes from the verified token on the server. If it comes from a request field the user can edit, the user chooses their own tenant.
- **PII and secrets in the index:** vectors and chunk text are copies of the source data. Redact or exclude what should not be searchable (national ids, card numbers, health data) before embedding, and keep the index under the same access, encryption and retention rules as the source. Embeddings are not anonymous (Q53).
- **PII in logs (Q41):** query text, retrieved text and answers all contain user data. Redact, set short retention, restrict who can read traces, and keep audit logs of who queried and which chunk ids were returned (ids, not text).
- **Deletion requests:** a delete must remove the vectors, the chunk text, caches and backups on a schedule, and the index must really drop them (tombstones and compaction, Q20). I verify it with a test that queries for the deleted text. This is engineering, not legal advice; compliance rules differ by country and contract.
- **Encryption:** in transit (TLS) and at rest, with keys managed by the cloud or your KMS; per-tenant keys where the contract needs it.
- **Injection:** a retrieved document can carry instructions and try to get data out. Least-privilege tools, no secrets in the prompt, output checks (Q36, Part 11).
- **Embedding inversion:** a stolen vector store may leak part of the text (Q53), so treat the store as sensitive.

**Example:** a SaaS support bot serves 3 companies from one index. A developer forgets the tenant filter on a new "similar tickets" endpoint, and company A starts seeing company B's refund notes. I add a test that, for every caller and every test query, asserts each returned chunk's tenant equals the caller. In my toy run the unfiltered search leaked 36 chunks over 16 caller-query pairs, and the pre-filter and the namespace versions leaked 0, including for an unknown caller (which gets nothing).

**Code:** (executed, standalone, numpy; TOY hashed bag-of-words vectors on synthetic tenants. It proves the harness idea, not a real vector DB)
```python
# Standalone, numpy only. TOY store: hashed bag-of-words "embeddings" (no semantic quality), synthetic tenants.
import zlib, numpy as np
D = 256
def embed(text):                                   # TOY hashed bag-of-words, L2-normalised
    v = np.zeros(D)
    for w in text.lower().split(): v[zlib.crc32(w.encode()) % D] += 1
    n = np.linalg.norm(v); return v / n if n else v

DOCS = [("t1", "refund policy for tenant one orders"), ("t1", "shipping times for tenant one"),
        ("t2", "refund policy for tenant two secret pricing"), ("t2", "tenant two internal roadmap refund notes"),
        ("t3", "refund policy tenant three")]
chunks = [{"id": f"c{i}", "tenant": t, "text": x, "vec": embed(x)} for i, (t, x) in enumerate(DOCS)]

def search_no_filter(caller, q, k=3):              # BUG: nothing ties results to the caller
    qv = embed(q); s = sorted(chunks, key=lambda c: -float(c["vec"] @ qv)); return s[:k]

def search_filter(caller, q, k=3):                 # tenant predicate applied BEFORE ranking (pre-filter)
    qv = embed(q); pool = [c for c in chunks if c["tenant"] == caller]
    return sorted(pool, key=lambda c: -float(c["vec"] @ qv))[:k]

NAMESPACES = {}                                    # one index per tenant: no cross-tenant path exists
for c in chunks: NAMESPACES.setdefault(c["tenant"], []).append(c)
def search_namespace(caller, q, k=3):
    qv = embed(q); return sorted(NAMESPACES.get(caller, []), key=lambda c: -float(c["vec"] @ qv))[:k]

def assert_no_leak(search_fn, queries, callers):    # the test harness
    leaks = []
    for caller in callers:
        for q in queries:
            for c in search_fn(caller, q):
                if c["tenant"] != caller: leaks.append((caller, q, c["id"], c["tenant"]))
    return leaks

QUERIES = ["refund policy", "tenant two internal roadmap", "secret pricing", "shipping"]
for name, fn in [("no filter (buggy)", search_no_filter), ("pre-filter", search_filter), ("namespace", search_namespace)]:
    leaks = assert_no_leak(fn, QUERIES, ["t1", "t2", "t3", "unknown"])
    print(f"{name:18s} leaks={len(leaks)}", leaks[:2])
assert assert_no_leak(search_filter, QUERIES, ["t1", "t2", "t3", "unknown"]) == []
assert assert_no_leak(search_namespace, QUERIES, ["t1", "t2", "t3", "unknown"]) == []
print("tests passed for pre-filter and namespace")
```

**Follow-ups:**
- *Filter or separate index?* Filters until tenant count, size or contracts make one mistake too costly; then namespaces or indexes. Mixed designs are normal.
- *Can the LLM enforce permissions?* No. It can be talked out of rules, and it sees whatever you retrieved. Enforce before the prompt.
- *Documents lose access after ingestion (user removed from a group)?* Store group ids, not user ids, on the chunk and resolve groups at query time, or re-sync ACLs on change events; test that revocation takes effect within the agreed delay.

**Common mistakes:** filtering after top-k; taking the tenant from the request body; one shared cache across tenants (the cache key must include the tenant or ACL scope); logging full prompts with PII; assuming vectors are safe to share; no automated leak test; deleting from the metadata table but not the index.

### Q43 ⭐ 🟡 AI code review: this LLM-written RAG ingestion and retrieval code has bugs (embedding-model mismatch, missing normalisation, filtering after top-k, deletes that leave vectors, off-by-one chunk overlap). Find and fix them.
**Asked at:** product, big tech, AI-era code-review rounds
**Say this first (1 line):** I review RAG code against a checklist (same embedder and dimension on both sides, normalised vectors for cosine, filter before ranking, deletes that reach the index, overlap and boundary arithmetic, tokens not characters), and I prove each bug on a tiny store by its symptom before I fix it and add a test.

**Then explain:**

| # | Bug in the LLM-written code | Symptom from my toy run |
|---|---|---|
| 1 | Ingest embeds with one model, query with another (or another dimension) | Different dimension: a shape error. Same dimension, different model: recall@1 fell from 1.0 to 0.2 with no error at all (the silent, dangerous case) |
| 2 | `dot` on unnormalised vectors while assuming cosine | A long off-topic chunk scored dot 18.0 against 3.0 for the short relevant one, while cosine said 0.61 vs 1.00. Long chunks win |
| 3 | Filter applied after top-k | 1 result instead of 10 for a 5 percent tenant (2000 random vectors); filtering before ranking gave 10 (Q44) |
| 4 | Delete updates the metadata table only | Top hit for the deleted document's own query is still that document; after a real delete it is gone (Q20) |
| 5 | Off-by-one in the chunk step (`size - overlap + 1`) | Overlap 2 became 1; with overlap 0, tokens 8 and 17 were silently dropped, so facts at chunk edges vanish |
| 6 | Chunks cut by characters while the budget is in tokens | A 600-character chunk was 175 toy tokens for prose and 600 for numbers and code, against a budget of 150 |

- **Fixes:** store embedder name and dimension with the index and assert on every call; L2-normalise at ingest and query so dot equals cosine (Q9); put the predicate inside the search; delete by id from the vector index and the metadata, then test that the text is no longer retrievable; write the chunk loop as `step = size - overlap` with an end check, and test coverage and overlap; count with the real tokenizer of the model that will read the text (Q16).
- **How I review LLM-written code:** do not trust that it runs. A wrong RAG pipeline usually runs fine and returns plausible text, so I check the numbers: print embedding shapes and norms, assert the tenant of every returned chunk, assert recall on 5 known queries, assert deleted ids are gone.
- **What this toy cannot show:** it uses hashed bag-of-words vectors and a toy tokenizer (so no real embedder behaviour or real token counts). The symptoms are directional, not what a production index would print.

**Example:** a teammate's LLM generated ingest code with `model="embed-v1"` and the query service with a newer default. Everything ran, and the retrieval quality quietly dropped. In my toy the same-dimension mismatch took recall@1 from 1.0 to 0.2 with no error. The fix was a version tag stored with the index and an assertion on query, not "be careful".

**Code:** (executed, standalone, numpy; TOY hashed vectors and toy tokenizer; every bug printed in isolation, then the fix asserted)
```python
# Standalone, numpy only. TOY store and TOY hashed embeddings; each bug is shown in isolation, then the fixed version is tested.
import zlib, re, numpy as np

def embed_a(text, d=64):                       # "model A" (toy hashed bag-of-words), NOT normalised
    v = np.zeros(d)
    for w in re.findall(r"\w+", text.lower()): v[zlib.crc32(w.encode()) % d] += 1
    return v
def embed_b(text, d=64):                       # "model B": same dimension, different hash salt = different space
    v = np.zeros(d)
    for w in re.findall(r"\w+", text.lower()): v[zlib.crc32(b"salt" + w.encode()) % d] += 1
    return v
def unit(v): n = np.linalg.norm(v); return v / n if n else v

DOCS = {"d1": "refund policy for damaged items", "d2": "shipping times and carriers for international orders",
        "d3": "password reset steps for the mobile app", "d4": "invoice and tax details for business customers",
        "d5": "warranty claim process and repair centres"}
Q = {"d1": "refund damaged items", "d2": "international shipping carriers", "d3": "reset password mobile",
     "d4": "business tax invoice", "d5": "warranty repair claim"}

# ---------------- Bug 1: embedder mismatch between ingest and query ----------------
M = np.stack([embed_a(t) for t in DOCS.values()]); ids = list(DOCS)
def hit1(qfn, m=M):
    return np.mean([ids[int(np.argmax(m @ qfn(q)))] == d for d, q in Q.items()])
print("BUG1 same model recall@1:", hit1(embed_a), "| ingest A, query B (same dim):", hit1(embed_b))
try: M @ embed_a("x", d=32)
except ValueError as e: print("BUG1 dimension mismatch raises:", str(e)[:40], "...")
# FIX: store embedder name + dim next to the index and assert on every query
class Index:
    def __init__(self, name, dim): self.name, self.dim, self.vecs, self.ids = name, dim, [], []
    def add(self, i, v, name): assert name == self.name and len(v) == self.dim; self.ids.append(i); self.vecs.append(unit(v))
    def search(self, v, name, k=3):
        assert name == self.name and len(v) == self.dim, "embedder mismatch"
        s = np.stack(self.vecs) @ unit(v); o = np.argsort(-s)[:k]; return [(self.ids[j], float(s[j])) for j in o]
idx = Index("A-64", 64)
for d, t in DOCS.items(): idx.add(d, embed_a(t), "A-64")
try: idx.search(embed_b("refund"), "B-64")
except AssertionError as e: print("FIX1 rejects:", e)

# ---------------- Bug 2: dot product on unnormalised vectors, assumed cosine ----------------
short = "refund damaged items"; long_ = ("refund damaged items " + "warranty repair claim process centres ") * 6
cands = {"short_relevant": embed_a(short), "long_offtopic": embed_a(long_)}
q = embed_a("refund damaged items")
print("BUG2 dot:", {k: round(float(v @ q), 2) for k, v in cands.items()},
      "| cosine:", {k: round(float(unit(v) @ unit(q)), 2) for k, v in cands.items()})

# ---------------- Bug 3: filter applied after top-k ----------------
rng = np.random.default_rng(0); N = 2000
V = np.stack([unit(rng.normal(size=32)) for _ in range(N)]); tenant = rng.integers(0, 20, N)   # 5% of chunks per tenant
qv = unit(rng.normal(size=32)); k = 10
top = np.argsort(-(V @ qv))[:k]; post = [i for i in top if tenant[i] == 3]
s = V @ qv; s[tenant != 3] = -9; pre = np.argsort(-s)[:k]
print(f"BUG3 filter after top-{k}: {len(post)} results | filter before ranking: {len(pre)} results")

# ---------------- Bug 4: delete updates metadata table only ----------------
class Store:
    def __init__(self): self.meta, self.vecs, self.ids = {}, [], []
    def add(self, i, text, deleted_ok=False): self.meta[i] = {"text": text, "deleted": False}; self.ids.append(i); self.vecs.append(unit(embed_a(text)))
    def delete_buggy(self, i): self.meta[i]["deleted"] = True             # vector stays in the index
    def delete_fixed(self, i):
        j = self.ids.index(i); self.ids.pop(j); self.vecs.pop(j); self.meta.pop(i)
    def search(self, text): s = np.stack(self.vecs) @ unit(embed_a(text)); return self.ids[int(np.argmax(s))]
st = Store(); [st.add(d, t) for d, t in DOCS.items()]
st.delete_buggy("d1"); print("BUG4 after metadata-only delete, top hit for 'refund damaged items':", st.search("refund damaged items"))
st2 = Store(); [st2.add(d, t) for d, t in DOCS.items()]
st2.delete_fixed("d1"); print("FIX4 after real delete, top hit:", st2.search("refund damaged items"))

# ---------------- Bug 5: off-by-one overlap ----------------
def chunk_buggy(tokens, size, overlap):
    out, s = [], 0
    while s < len(tokens): out.append(tokens[s:s + size]); s += size - overlap + 1   # BUG: step too big by 1
    return out
def chunk_fixed(tokens, size, overlap):
    assert 0 <= overlap < size
    out, s = [], 0
    while True:
        out.append(tokens[s:s + size])
        if s + size >= len(tokens): break
        s += size - overlap
    return out
toks = list(range(20)); size = 8
for name, fn, ov in [("buggy ov=2", chunk_buggy, 2), ("fixed ov=2", chunk_fixed, 2), ("buggy ov=0", chunk_buggy, 0), ("fixed ov=0", chunk_fixed, 0)]:
    ch = fn(toks, size, ov); covered = set(t for c in ch for t in c)
    ovl = [len(set(a) & set(b)) for a, b in zip(ch, ch[1:])]
    print(f"BUG5 {name}: chunks={len(ch)} missing tokens={sorted(set(toks) - covered)} overlaps={ovl}")
f = chunk_fixed(toks, size, 2); assert set(t for c in f for t in c) == set(toks) and all(len(set(a) & set(b)) == 2 for a, b in zip(f, f[1:]))

# ---------------- Bug 6: chunk by characters, budget in tokens ----------------
def toy_tokens(s): return re.findall(r"[A-Za-z]{1,4}|\d|[^\sA-Za-z\d]", s)   # TOY tokenizer: <=4 letters, single digits, symbols
prose = "the cat sat on the mat. " * 40
code_ = "x=[1,2,3];y={'a':42};" * 40
for name, text in [("prose", prose), ("numbers/code", code_)]:
    c = text[:600]; print(f"BUG6 {name}: 600-char chunk = {len(toy_tokens(c))} toy tokens (budget 150)")
def chunk_by_tokens(text, budget): t = toy_tokens(text); return ["".join(t[i:i + budget]) for i in range(0, len(t), budget)]
assert all(len(toy_tokens(c)) <= 150 for c in chunk_by_tokens(code_, 150)); print("FIX6 token-based chunks all <= 150 toy tokens")
```

**Follow-ups:**
- *Which bug is the most dangerous?* The silent same-dimension model mismatch and the post-filter leak or recall loss, since nothing crashes.
- *Cosine or dot after normalisation?* Identical ranking for unit vectors; dot is faster and many indexes use it for normalised vectors. Check the index metric setting (Q9).
- *How do you stop this in CI?* A small golden set with a recall threshold, a leak test, a delete test and a chunker property test (coverage and overlap).

**Common mistakes:** approving code because it ran; testing only the happy path; fixing the symptom (more top-k) and not the cause; normalising only the query or only the chunks; deleting from the metadata table only; measuring chunk size in characters and promising a token budget.

### Q44 ⭐ 🔴 A strict metadata filter returns only 2 results when the user wanted 10. Why does it happen, and how do you fix it (pre-filtering, post-filtering, filter-aware ANN)?
**Asked at:** platform teams, product, GenAI startups, senior roles
**Say this first (1 line):** The filter is probably applied after the ANN search: the index returns its top 10 nearest vectors, most fail the filter, and only 2 survive. The fix is to make the filter part of the search (filter-aware ANN, or a predicate inside the scanned IVF cells), or over-fetch, or give very selective filters their own partition.

**Then explain:**
- **Why post-filtering fails:** if only 20 percent of chunks pass the filter, a top-10 list holds about 2 passing items on average. The other 8 were nearer but not allowed. The survivors are also not the true best 10 among allowed chunks. With a 1 percent filter you often get zero.
- **Why pre-filtering is not free:** apply the filter first and then search a plain HNSW graph. The graph was built over all vectors, so removing most nodes breaks the paths the search walks. The reported effect (from the HNSW and IVF guide I read, not measured by me) is latency spikes or too few results. Filter-aware implementations handle this in different ways; check your engine's docs.
- **Remedies, with trade-offs:**

| Remedy | How it helps | Cost |
|---|---|---|
| Filter-aware search inside the index (the engine checks the predicate during traversal, or switches to an exact scan when the filter is very selective) | right count and good recall | depends on the engine; test on your filters |
| IVF with the predicate applied inside the scanned cells, and a larger nprobe | scans only allowed vectors in the probed cells | more cells means more latency |
| Partition or separate index for high-selectivity values (a big tenant, a language) | the search space is already small | many indexes to operate (Q42) |
| Over-fetch `k / selectivity`, with a cap, then filter | works with any index | still can fall short when selectivity is tiny; cost grows as the filter gets stricter |
| Exact scan of the filtered subset | perfect recall when the subset is small (say thousands) | slow if the subset is large |

- **Decision I would make:** use the engine's filter-aware mode, measure results-per-query and recall against an exact filtered search on real filters, and put the few extreme filters (the 1 percent ones) on a partition or an exact scan.
- **Security:** access-control filters must never be post-filters that sometimes return fewer results by luck; they need to be pre-filters or partitions (Q15, Q42).

**Example:** results from my synthetic run (20000 random clustered vectors, IVF with 64 cells, nprobe 4, recall against an exact search on the filtered set). At 20 percent selectivity: post-filter gave 1.87 results per query (recall@10 0.19); over-fetch gave 8.70 results (0.87); predicate inside the cells gave 10 (1.00). At 1 percent selectivity: post-filter 0.13 results, over-fetch with a cap of 200 only 2.10, predicate inside the cells 9.37 results with recall 0.71, and with nprobe 16 it gave 10 results and recall 0.96. So the stricter the filter, the more the search budget must move inside the filter.

**Code:** (executed, standalone, numpy; SYNTHETIC data with a random flag; a toy IVF, not HNSW, so it shows the post-filter effect and in-cell predicates, not HNSW graph fragmentation)
```python
# Standalone, numpy only. SYNTHETIC clustered vectors and a random metadata flag; recall is vs exact filtered search.
import numpy as np
rng = np.random.default_rng(0)
N, D, NLIST, K = 20000, 32, 64, 10
centers = rng.normal(size=(NLIST, D)) * 2
X = centers[rng.integers(0, NLIST, N)] + rng.normal(size=(N, D))
X /= np.linalg.norm(X, axis=1, keepdims=True)
# tiny k-means for an IVF index
C = X[rng.choice(N, NLIST, replace=False)].copy()
for _ in range(8):
    a = np.argmax(X @ C.T, 1)
    for j in range(NLIST):
        m = X[a == j]
        if len(m): C[j] = m.mean(0)
    C /= np.linalg.norm(C, axis=1, keepdims=True)
assign = np.argmax(X @ C.T, 1); cells = [np.where(assign == j)[0] for j in range(NLIST)]
Q = X[rng.choice(N, 200, replace=False)] + 0.1 * rng.normal(size=(200, D)); Q /= np.linalg.norm(Q, axis=1, keepdims=True)

def top(ids, q, k): s = X[ids] @ q; return ids[np.argsort(-s)[:k]]
def ivf_candidates(q, nprobe): return np.concatenate([cells[j] for j in np.argsort(-(C @ q))[:nprobe]])

def run(sel, nprobe=4):
    flag = rng.random(N) < sel                                    # metadata predicate passes for fraction `sel`
    res = {m: [] for m in ["post-filter ANN, k=10", "post-filter, over-fetch k/sel (cap 200)", "pre-filter inside IVF cells", "pre-filter, nprobe x4"]}
    rec = {m: [] for m in res}
    for q in Q:
        truth = set(top(np.where(flag)[0], q, K))                 # exact search on the filtered subset
        cand = ivf_candidates(q, nprobe)
        outs = {"post-filter ANN, k=10": [i for i in top(cand, q, K) if flag[i]],
                "post-filter, over-fetch k/sel (cap 200)": [i for i in top(cand, q, min(200, int(K / sel))) if flag[i]][:K],
                "pre-filter inside IVF cells": list(top(cand[flag[cand]], q, K)),
                "pre-filter, nprobe x4": list(top((c4 := ivf_candidates(q, nprobe * 4))[flag[c4]], q, K))}
        for m, o in outs.items(): res[m].append(len(o)); rec[m].append(len(set(o) & truth) / K)
    print(f"selectivity {sel:.0%} (about {int(N*sel)} eligible vectors), nprobe={nprobe} of {NLIST}")
    for m in res: print(f"  {m:42s} results/query={np.mean(res[m]):5.2f}  recall@10 vs exact-filtered={np.mean(rec[m]):.2f}")
run(0.20); run(0.01)
```

**Follow-ups:**
- *Why not always raise k?* Cost grows with k, and for a 0.1 percent filter you would need k in the thousands. At that point partition or scan.
- *Does a strict filter break HNSW recall?* It can, since the nodes that remain may not be connected well; this is reported in the guide and engine-specific, so test it.
- *Where do you check the result count?* Log results-per-query and the filter selectivity (Q41); fewer than k results is an alert.

**Common mistakes:** filtering after top-k and calling it fixed because the answer looked fine; only measuring recall for unfiltered queries; over-fetching with no cap; treating the access-control filter like a ranking hint; forgetting that selectivity differs by tenant, so a design that works for the big tenant fails for the small one.

### Q45 ⭐ 🔴 Design question: 800 million vectors and a 200 GB RAM budget. Which index do you choose, and how do you recover recall?
**Asked at:** platform teams, senior roles at product companies
**Say this first (1 line):** 800 million 768-dim fp32 vectors are about 2.46 TB raw, 12 times the RAM, so I use IVF-PQ: compressed codes (for example 96 bytes per vector, about 77 GB) plus ids and centroids in RAM, the full vectors on SSD, and I rerank a shortlist with the full vectors to win back recall. If one machine is not enough, I shard.

**Then explain:**
- **Size first:** 800e6 x 768 x 4 bytes = 2.46 TB. fp16 is 1.23 TB and int8 is 614 GB, still too big. So I must compress or spread the data.
- **Index choice (per the HNSW/IVF guide, as reported):** flat under about 1M vectors, HNSW when latency matters and RAM allows, IVF-Flat for tens of millions, IVF-PQ for hundreds of millions to billions. At 800M, IVF-PQ is the match. HNSW needs full vectors for its distance computations plus a graph (about 205 GB of links alone for M=32 under my assumption), so it does not fit here.
- **How IVF-PQ works:** IVF splits the space into cells (nlist) and searches only the nprobe nearest cells. PQ cuts each vector into 96 pieces and stores one byte per piece (a pointer to the nearest of 256 small centroids), so 3,072 bytes become 96 bytes (32x). Distances are approximate.
- **Memory (assumed nlist of 2^20, 8-byte ids):** codes 76.8 GB + ids 6.4 GB + centroids 3.2 GB = about 86 GB, which fits in 200 GB with room for the OS, caches and the rerank pipeline. 32 bytes per vector would be about 35 GB total (lower recall).
- **Recover recall:**
  - raise nprobe (more cells searched; latency goes up);
  - fetch a bigger shortlist from PQ (say 100 to 500) and rerank it with the exact full-precision vectors read from SSD; this fixes most of the PQ error;
  - more bytes per vector (more sub-vectors, or more bits per sub-vector);
  - OPQ-style rotation before PQ (from memory, not verified: it often helps by balancing variance across sub-vectors; test on your data);
  - more cells (nlist) with a matching nprobe.
- **Sharding:** if QPS or latency needs more than one box, split by id range or by cluster, query all shards in parallel and merge top-k. Cost is fan-out latency (the slowest shard sets p99) and more machines. Keeping full fp32 in RAM would need about 18 machines under my 70 percent usable-RAM assumption, which is why compression plus SSD rerank is usually cheaper.
- **Check the SSD:** a shortlist of 100 at 1000 QPS is 100,000 random reads per second (307 MB/s), a sensible load for NVMe drives but check the drive spec. Many engines offer a disk-based index mode; check current docs.

**Example:** I answer in order: (1) raw 2.46 TB, does not fit; (2) IVF-PQ at 96 B per vector gives about 86 GB in RAM; (3) full vectors on SSD, rerank top 100 to 200; (4) measure recall@10 against exact search on a 1M sample of real queries and tune nprobe and shortlist until recall and p95 meet the target; (5) shard if QPS demands it. Then I say what I would not trust without a test: the recall the compression gives on my data.

**Code:** (executed, standalone, standard library; arithmetic only; decimal GB; nlist, id size, HNSW links and QPS are ASSUMED)
```python
# Standalone, standard library only. Pure arithmetic; decimal units (1 GB = 1e9 bytes). ASSUMED parameters are labelled.
N, D, RAM = 800_000_000, 768, 200e9
GB = lambda b: b / 1e9
raw32 = N * D * 4
print(f"raw fp32: {GB(raw32):,.0f} GB = {raw32/1e12:.2f} TB  -> {raw32/RAM:.1f}x the 200 GB budget (does not fit)")
print(f"raw fp16: {GB(N*D*2):,.0f} GB | int8: {GB(N*D):,.0f} GB (still too big)")
IDS = N * 8                                                   # 8-byte id per vector
NLIST = 1_048_576                                             # ASSUMED coarse cells (2^20; tune on your data)
cent = NLIST * D * 4
print(f"\nASSUMED IVF with nlist={NLIST:,}: centroids {GB(cent):.1f} GB, ids {GB(IDS):.1f} GB")
print(f"{'PQ bytes/vec':>12} {'codes GB':>9} {'+ids+centroids GB':>18} {'fits 200 GB?':>13} {'compression':>12}")
for m in (16, 32, 64, 96, 128):                               # m sub-vectors, 8 bits (1 byte) each
    codes = N * m; tot = codes + IDS + cent + m * 256 * (D // m) * 4
    print(f"{m:>12} {GB(codes):>9.1f} {GB(tot):>18.1f} {'yes' if tot < RAM*0.8 else 'tight/no':>13} {D*4/m:>11.0f}x")
print("\nIn-RAM HNSW is the wrong tool: graph links alone for M=32 (ASSUMED, ~2*M links x 4 B per vector on layer 0):",
      f"{GB(N*2*32*4):.0f} GB, and it still needs full vectors for distances ({GB(raw32):,.0f} GB).")
# SSD rerank cost, ASSUMED workload
qps, shortlist = 1000, 100
print(f"\nSSD rerank (ASSUMED {qps} QPS, shortlist {shortlist}): {qps*shortlist:,} random 3 KB reads/s, {qps*shortlist*D*4/1e6:,.0f} MB/s;"
      " NVMe drives are commonly rated for hundreds of thousands of IOPS (check the drive spec).")
for per_machine in (200e9,):
    print(f"Alternative: shard full fp32 vectors in RAM: {raw32/(per_machine*0.7):.0f} machines at 70% usable RAM each (ASSUMED)")
print(f"Sharded IVF-PQ(96) over 4 machines: {GB(N*96+IDS+cent)/4:.1f} GB per machine for codes+ids+centroids")
```

**Follow-ups:**
- *Why not just int8 quantisation?* 614 GB is still 3 times the RAM; scalar quantisation gives 4x, PQ gives 30x or more.
- *What if the corpus keeps growing?* IVF-PQ needs retraining when the data distribution moves a lot; plan periodic rebuilds and a delta index for new data (Q20).
- *What will you measure?* recall@k against an exact search on a sample, p95 latency, SSD reads per query, memory per shard.

**Common mistakes:** forgetting ids and centroids in the memory count; quoting 100M x 768 as "low terabytes" (it is about 307 GB) or mixing GB with GiB; choosing HNSW for 800M with 200 GB; skipping the rerank and blaming the embedder for PQ loss; sizing memory and ignoring the p99 fan-out of shards.

### Q46 ⭐ 🔴 Recall is 0.90 and you need 0.97 without changing the embedding model. What do you change, and what does it cost?
**Asked at:** platform teams, product, senior roles
**Say this first (1 line):** First I confirm the 0.90 is ANN recall against exact search (index quality), then I spend a little latency: raise efSearch or nprobe, rerank a bigger shortlist with full-precision vectors, and if that is not enough, rebuild with a larger M and efConstruction or less aggressive compression. Each step costs latency, memory or a rebuild, so I measure the curve.

**Then explain:**
- **Which recall?** There are two different numbers. ANN recall = how many of the true nearest neighbours the index returned (index quality). End-to-end relevance = whether the right chunk is found for the user (embedder and chunking quality). Raising ANN recall from 0.90 to 0.97 cannot fix an embedder that ranks the right chunk 40th. I check the ANN recall on sampled production queries against a flat (exact) search (Q34).
- **Levers, cheapest first:**

| Lever | Cost |
|---|---|
| Raise efSearch (HNSW) or nprobe (IVF) | more latency per query; no rebuild; the only knob you can change on a live index per the guide |
| Rerank a bigger shortlist with full-precision vectors (when the index stores compressed codes) | more reads and compute; recovers PQ or quantisation loss |
| Less aggressive PQ (more bytes per vector), or none | more memory |
| Raise M and efConstruction (HNSW) | rebuild, more memory, slower indexing |
| More cells (nlist) with a matching nprobe (IVF) | rebuild and retrain |
| Flat (exact) search for small shards | linear cost, fine under about 1M vectors per the guide |
| Hybrid retrieval (add BM25) to rescue misses the dense vector never finds (Q29) | extra index and fusion; it fixes retrieval misses, not ANN error |

- **Diminishing returns:** the guide reports that going 0.80 to 0.95 costs modestly while 0.95 to 0.99 can cost several times the latency (reported, illustrative, not a law). My synthetic sweep shows the same shape.
- **Order of work:** measure the baseline curve, pick the smallest efSearch/nprobe that reaches 0.97 at the p95 latency budget, and only if the latency is too high change the index build.

**Example:** my synthetic IVF (50,000 vectors, 128 cells, run on one machine) gave recall@10 of 0.915 at nprobe 8 (0.13 ms/query), 0.963 at nprobe 16 (0.28 ms), 0.986 at nprobe 32 (0.53 ms) and 1.000 at nprobe 64 (1.48 ms). So 0.97 sits between nprobe 16 and 32, at roughly 2 to 4 times the latency of the 0.915 setting. In a real system I would run the same sweep on my own data and queries and choose the point that fits the latency budget.

**Code:** (executed, standalone, numpy; SYNTHETIC clustered vectors, a toy IVF built from scratch; timings are machine-specific and only the shape of the curve matters)
```python
# Standalone, numpy only. SYNTHETIC vectors; recall is ANN vs exact search (index quality, not end-to-end relevance). Timings are machine-specific.
import time, numpy as np
rng = np.random.default_rng(1)
N, D, NLIST, K, NQ = 50000, 32, 128, 10, 200
centers = rng.normal(size=(NLIST, D))
X = (centers[rng.integers(0, NLIST, N)] + 1.2 * rng.normal(size=(N, D))).astype(np.float32)   # overlapping clusters: not trivial
X /= np.linalg.norm(X, axis=1, keepdims=True)
C = X[rng.choice(N, NLIST, replace=False)].copy()
for _ in range(6):
    a = np.argmax(X @ C.T, 1)
    for j in range(NLIST):
        m = X[a == j]
        if len(m): C[j] = m.mean(0)
    C /= np.linalg.norm(C, axis=1, keepdims=True)
a = np.argmax(X @ C.T, 1); cells = [np.where(a == j)[0] for j in range(NLIST)]
Q = X[rng.choice(N, NQ, replace=False)] + 0.5 * rng.normal(size=(NQ, D)).astype(np.float32) / np.sqrt(D); Q = Q.astype(np.float32); Q /= np.linalg.norm(Q, axis=1, keepdims=True)
truth = [set(np.argsort(-(X @ q))[:K]) for q in Q]

def ivf(q, nprobe):
    cand = np.concatenate([cells[j] for j in np.argsort(-(C @ q))[:nprobe]])
    return cand[np.argsort(-(X[cand] @ q))[:K]]
print("IVF nprobe sweep (recall@10 vs exact):")
for nprobe in (1, 2, 4, 8, 16, 32, 64, 128):
    t = time.perf_counter(); res = [ivf(q, nprobe) for q in Q]; ms = (time.perf_counter() - t) / NQ * 1000
    rec = np.mean([len(set(r) & t_) / K for r, t_ in zip(res, truth)])
    print(f"  nprobe={nprobe:3d}  recall@10={rec:.3f}  {ms:6.2f} ms/query (this machine)")
```

**Follow-ups:**
- *Will rerank help an HNSW index that stores full vectors?* No, it already scores with full vectors; reranking helps a compressed or two-stage index and, with a cross-encoder, relevance (Q30), which is a different problem.
- *efSearch vs efConstruction?* efSearch is a query-time knob; efConstruction and M are build-time and need a rebuild (reported in the guide and general HNSW practice).
- *How do you know 0.97 is enough?* Link it to the end-to-end metric: does answer quality (Q39) improve when ANN recall goes from 0.90 to 0.97? If not, the bottleneck is elsewhere.

**Common mistakes:** tuning ANN recall when the embedder or chunking is the problem; quoting recall without k; measuring on random queries instead of real ones; raising efSearch without checking p95 and p99; rebuilding the index first when a query-time knob would do; forgetting that filters change recall (Q44).

### Q47 ⭐ 🔴 How do you evaluate chunking strategies empirically (experiment design, retrieval metrics, ablations, confounders)?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** I fix the corpus, golden set, embedder, retriever and k, change one chunking setting at a time, score at the answer-span or document level (because chunk counts differ), track context tokens and end-to-end faithfulness too, and use a paired bootstrap over queries to see whether a difference is real.

**Then explain:**
- **Setup:** a golden set of real queries (Q40) with the answer evidence marked as a text span or a document, not as a chunk id (chunk ids change with every chunker). Same embedder, same index type, same retriever and reranker. Only chunk size, overlap or strategy changes.
- **Hold what constant? Say it out loud.** Two valid designs: (a) constant k, which means bigger chunks put more tokens in the prompt, so the comparison is confounded with context size; (b) constant token budget in the prompt (for example 2,000 tokens), so small chunks get a larger k. I prefer (b) for the final decision because the prompt budget is what you really pay for; (a) is useful to understand the mechanism. Report context tokens used either way.
- **Metrics:**
  - span-hit or recall@k: does any retrieved chunk contain the answer span?
  - MRR (rank of the first useful chunk), context precision (share of retrieved tokens that are useful), context tokens used;
  - end-to-end faithfulness and answer correctness on the final answers (Q39), since a chunk that is retrieved but too short to answer wins on retrieval and loses on generation.
- **The pitfall:** if the gold label is "all chunks of the right document", recall depends on the number of chunks, which depends on chunk size. Small chunks create many gold chunks and look bad at k=3; large chunks look better. In my toy run this naive chunk recall went up with chunk size (0.074, 0.113, 0.149) while the real answer-span hit went down (0.82, 0.53, 0.41). Opposite conclusions from the same runs. Judge on answer span or document.
- **Significance:** the same queries are scored under both settings, so the differences are paired. A paired bootstrap resamples queries (keeping each query's two outcomes together) and gives a confidence interval for the difference. With a few hundred queries, small differences are often noise.
- **Confounders:** different token budgets; the parser or cleaning changed at the same time; golden set built from text near chunk boundaries of one chunker (bias, Q40); overlap duplicates inflating hit rate; tuning on the same queries you report; query types that behave differently (lookup vs summary, so report by segment).

**Example:** I compare 256, 512 and 1024-token chunks on 300 real support queries, with a fixed 3,000-token prompt budget. Result: 512 has the best span-hit and answer correctness, 256 is slightly better on lookup questions and worse on how-to questions. The bootstrap CI for 512 vs 256 on span-hit is wide on lookup-only queries (few of them) and I say so instead of declaring a winner. In my toy below (SYNTHETIC, keyword-matching, so small chunks win there; it says nothing about real corpora) the difference between 60-word and 20-word chunks was -0.293 with a 95% CI of [-0.387, -0.200], and with a fixed k the 20-word chunks also used far fewer context words (60 vs 164), which is exactly the confounder I would control in a real study.

**Code:** (executed, standalone, numpy; SYNTHETIC documents and a TOY hashed bag-of-words retriever)
```python
# Standalone, numpy only. SYNTHETIC corpus, TOY hashed bag-of-words retrieval; shows experiment design and metric pitfalls, not real chunking quality.
import zlib, numpy as np
rng = np.random.default_rng(3)
D, NDOC, DOCLEN, K = 4096, 150, 240, 3
filler = [f"f{i}" for i in range(400)]
def emb(ws):
    v = np.zeros(D)
    for w in ws: v[zlib.crc32(w.encode()) % D] += 1
    n = np.linalg.norm(v); return v / n if n else v
docs, queries = [], []                                   # each doc hides one answer sentence containing 3 rare words; the query uses 2 of them
for d in range(NDOC):
    ws = list(rng.choice(filler, DOCLEN)); rare = [f"r{d}_{j}" for j in range(3)]
    pos = int(rng.integers(0, DOCLEN - 6)); ws[pos:pos + 3] = rare
    docs.append((ws, pos)); queries.append((d, [rare[0], rare[1]] + list(rng.choice(filler, 1))))

def evaluate(size, overlap):
    step = size - overlap; chunks = []                   # (doc, start, end, vec)
    for d, (ws, _) in enumerate(docs):
        for s in range(0, max(1, len(ws) - overlap), step): chunks.append((d, s, min(len(ws), s + size), emb(ws[s:s + size])))
    M = np.stack([c[3] for c in chunks]); span_hit, doc_hit, chunk_recall, ctx = [], [], [], []
    for d, q in queries:
        top = np.argsort(-(M @ emb(q)))[:K]; pos = docs[d][1]
        span_hit.append(float(any(chunks[i][0] == d and chunks[i][1] <= pos and pos + 3 <= chunks[i][2] for i in top)))
        doc_hit.append(float(any(chunks[i][0] == d for i in top)))
        gold = [i for i, c in enumerate(chunks) if c[0] == d]                      # NAIVE gold: every chunk of the gold doc
        chunk_recall.append(len(set(top) & set(gold)) / len(gold))
        ctx.append(sum(chunks[i][2] - chunks[i][1] for i in top))
    return np.array(span_hit), np.array(doc_hit), np.array(chunk_recall), np.mean(ctx), len(chunks)

print(f"{'size/overlap':>12} {'#chunks':>8} {'span-hit@3':>10} {'doc-hit@3':>10} {'naive chunk-recall@3':>21} {'ctx words':>10}")
R = {}
for size, ov in [(20, 0), (60, 10), (120, 20)]:
    sh, dh, cr, ctx, n = evaluate(size, ov); R[size] = sh
    print(f"{size:>6}/{ov:<5} {n:>8} {sh.mean():>10.3f} {dh.mean():>10.3f} {cr.mean():>21.3f} {ctx:>10.0f}")

def paired_bootstrap(a, b, n=5000, seed=0):             # resample QUERIES, keep each query's pair together
    r = np.random.default_rng(seed); idx = r.integers(0, len(a), (n, len(a)))
    diffs = (a[idx] - b[idx]).mean(1); return (a - b).mean(), np.percentile(diffs, [2.5, 97.5])
for x, y in [(60, 20), (120, 60)]:
    d, ci = paired_bootstrap(R[x], R[y]); print(f"span-hit {x}-word vs {y}-word chunks: diff {d:+.3f}, 95% paired-bootstrap CI [{ci[0]:+.3f}, {ci[1]:+.3f}]")
```

**Follow-ups:**
- *Do you need a separate golden set per chunker?* No. Mark answer spans in the source text once, then map to whichever chunks contain them.
- *Is the best chunk size universal?* No. It depends on the corpus, the query types and the embedder; the usual 256 to 512 token starting range is a starting point, not a result.
- *How many queries?* Enough that the bootstrap interval on the difference you care about excludes zero; a few hundred is typical for a first read, with the caveat that rare query types need their own samples.

**Common mistakes:** comparing chunk-id recall across chunkers; changing chunk size and k and the embedder together; not reporting context tokens; judging on retrieval only; reporting one number without a CI; tuning on the test queries; using LLM-generated questions that copy chunk wording (Q40).

### Q48 ⭐ 🔴 How does semantic chunking work (similarity breakpoints), and what does the evidence say about when it beats simpler chunking?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** Semantic chunking embeds each sentence (or a small window of sentences), measures the similarity between neighbours, and starts a new chunk where similarity drops below a threshold or percentile, so chunks follow topic shifts instead of a fixed length. The evidence that it beats simple recursive or structure-aware chunking is mixed, so I test it on my own golden set before paying for it.

**Then explain:**
- **Steps:**
  1. Split the text into sentences.
  2. Embed each sentence (often with neighbours as a small window, to reduce noise).
  3. Compute similarity between consecutive sentences or windows.
  4. Mark a breakpoint where similarity falls under a threshold, or in the lowest N percent of the document's similarities.
  5. Merge sentences between breakpoints; usually also enforce a minimum and maximum size.
- **Trade-offs:**
  - Ingest cost: you embed every sentence, then embed the chunks again. For big corpora this is a large extra bill and extra time (Q32).
  - Unstable sizes: chunks can be 1 sentence or 40. Tiny chunks lack context, huge ones dilute the embedding; so add min and max limits (Q16).
  - Threshold sensitivity: a percentile always creates breaks even in a document with one topic; a fixed threshold depends on the embedder.
  - Embedder dependence: breakpoints come from the same kind of model that you later retrieve with, so errors correlate.
  - Structure ignored: headings, tables and lists already give cleaner boundaries for free (Q4, Q17).
- **Evidence:** I have seen mixed reports: some experiments show gains on certain datasets and others show no gain or a loss against simple fixed or recursive splitting once cost is counted. I quote no numbers here. The honest answer is "it can help for long, unstructured, multi-topic text, and I would A/B it with the method in Q47".
- **My default:** structure-aware or recursive chunking with sensible size and overlap, and parent-document retrieval (Q18). I try semantic chunking when documents are long unstructured transcripts or emails, and keep it only if span-hit and answer quality improve on the golden set at acceptable cost.

**Example:** a 35-sentence synthetic support text with 4 uneven topic sections (7, 12, 5 and 9 sentences). Fixed 7-sentence chunks cut it at sentences 7, 14, 21, 28: it gets the first boundary right, then slices the 12-sentence section in the middle (F1 0.29, tolerance one sentence). Semantic breakpoints on 3-sentence windows found boundaries 8, 23 and 24 (F1 0.80), and on single sentences 7, 19 and 22 (F1 0.67). Look at the weakness too: the windowed version produced a 1-sentence chunk, which is the unstable-size problem. This is a TOY on bag-of-words vectors with very clean topics; real text is messier.

**Code:** (executed, standalone, numpy; TOY bag-of-words sentence vectors on synthetic text; no real embedding model)
```python
# Standalone, numpy only. TOY: synthetic multi-topic text, bag-of-words sentence vectors (no real embeddings, no semantic quality claims).
import numpy as np
rng = np.random.default_rng(5)
topics = {t: [f"{t}{i}" for i in range(25)] for t in ["billing", "shipping", "login", "warranty"]}
common = ["the", "a", "is", "to", "and", "for"]
sent_per_topic = [7, 12, 5, 9]                      # uneven section lengths on purpose
sents, truth = [], []                               # truth = sentence indices where a new topic starts
for t, n in zip(topics, sent_per_topic):
    truth.append(len(sents))
    for _ in range(n): sents.append(list(rng.choice(topics[t], 7)) + list(rng.choice(common, 3)))
truth = set(truth[1:]); vocab = {w: i for i, w in enumerate(sorted({w for s in sents for w in s}))}
def vec(ws):
    v = np.zeros(len(vocab))
    for w in ws: v[vocab[w]] += 1
    return v / np.linalg.norm(v)
V = np.stack([vec(s) for s in sents])
W = np.stack([vec(sum(sents[max(0, i - 1):i + 2], [])) for i in range(len(sents))])      # window of 3 sentences smooths noise
def breakpoints(M, pct=15):
    sim = np.array([M[i] @ M[i + 1] for i in range(len(M) - 1)])    # similarity between neighbours i and i+1
    thr = np.percentile(sim, pct); return {i + 1 for i, s in enumerate(sim) if s <= thr}, sim
def f1(pred, truth, tol=1):
    tp = sum(any(abs(p - t) <= tol for p in pred) for t in truth); pr = sum(any(abs(p - t) <= tol for t in truth) for p in pred)
    P, R = pr / max(1, len(pred)), tp / len(truth); return 2 * P * R / (P + R) if P + R else 0
def sizes(bps, n): b = [0] + sorted(bps) + [n]; return [b[i + 1] - b[i] for i in range(len(b) - 1)]
print("true topic starts at sentences:", sorted(truth), "| sentences per topic:", sent_per_topic)
for name, M in [("sentence vectors", V), ("3-sentence windows", W)]:
    bp, _ = breakpoints(M, 8); print(f"semantic ({name}, 8th percentile): boundaries {sorted(bp)} F1(tol=1)={f1(bp, truth):.2f} chunk sizes {sizes(bp, len(sents))}")
fixed = set(range(7, len(sents), 7)); print(f"fixed 7-sentence chunks: boundaries {sorted(fixed)} F1(tol=1)={f1(fixed, truth):.2f} chunk sizes {sizes(fixed, len(sents))}")
```

**Follow-ups:**
- *How do you set the threshold?* Tune a percentile or threshold on the golden set, together with min and max chunk sizes, and check the chunk-size distribution (Q47).
- *What if the embedder is multilingual?* Similarity levels differ per language, so use per-document percentiles, not a global threshold.
- *Alternatives?* Use the document's own structure (headings), a recursive splitter, or an LLM to propose boundaries (expensive).

**Common mistakes:** assuming semantic means better; no min and max chunk size; one global threshold across documents; ignoring ingest cost; comparing on chunk-level metrics that favour whatever creates fewer chunks (Q47); sentence splitting on dots that break abbreviations and numbers.
