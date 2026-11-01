### Q27 ⭐⭐ 🟡 What is RAPTOR (hierarchical summary trees)? How is the tree built, how is it queried, and how does it compare with GraphRAG?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** RAPTOR builds a tree over your chunks: it embeds and clusters them, has an LLM summarise each cluster, then repeats on the summaries, so retrieval can pull from detailed leaves or high-level summaries depending on the question.
**Then explain:**
- **What the paper says (abstract):** recursively embed, cluster and summarise chunks into a tree with several levels of summary; at query time retrieve across those levels of abstraction. Paired with GPT-4 it reports a 20% absolute accuracy gain on the QuALITY benchmark. That is the authors' own claim on one benchmark, not something I would promise on your data.
- **Build loop:** chunk, embed, cluster, summarise each cluster, embed the summaries, repeat until one root (or few nodes) remain. Cost is index-time LLM calls, one per cluster per level, plus re-running parts of it when documents change.
- **Query options (from memory, not verified against the paper):** "collapsed tree" puts all nodes from all levels in one pool and takes top-k by similarity under a token budget; "tree traversal" starts at the top and descends into the best children. I would start with the collapsed version because it is just normal vector search over more nodes.
- **Why it helps:** a question like "what is the overall argument of this book?" has no single chunk answering it, but a high-level summary node may. Detail questions still hit leaves.
- **Versus GraphRAG:** RAPTOR gives a tree of summaries grouped by embedding similarity. GraphRAG extracts an entity-relationship graph, clusters it into communities and summarises those (Q28), so it keeps explicit entities and relationships. Tree: simpler, no extraction step. Graph: better when the question is about how entities connect.

**Example:** A 300-page report is about 600 chunks. Level 1 might have about 60 summaries and level 2 about 6 (assumed ratios, they depend on the clusterer). Index cost is about 66 summarisation calls plus embeddings, a small fraction of one call per chunk for entity extraction in GraphRAG. "What are the three main risks the report highlights?" now matches a level-2 node instead of needing 40 leaf chunks.

**Code:** (run; TOY: hashed bag-of-words embeddings, farthest-first k-means from scratch, a MOCK summariser that keeps frequent words. It shows tree shape, call count and cross-level retrieval, not semantic quality or real RAPTOR output)
```python
import re, zlib
import numpy as np

# TOY RAPTOR-style tree. Embeddings = hashed bag-of-words (toy, no semantic quality).
# The "summariser" is a mock (keeps the most frequent words); a real build calls an LLM per cluster.
def toks(t): return re.findall(r"[a-z]+", t.lower())
def embed(text, d=128):
    v = np.zeros(d)
    for w in toks(text): v[zlib.crc32(w.encode()) % d] += 1
    n = np.linalg.norm(v); return v / n if n else v

def kmeans(X, k, iters=20, seed=0):
    rng = np.random.default_rng(seed)
    idx = [int(rng.integers(len(X)))]                 # farthest-first init
    while len(idx) < k:
        idx.append(int(np.argmin((X @ X[idx].T).max(1))))
    C = X[idx].copy()
    for _ in range(iters):
        lab = np.argmax(X @ C.T, axis=1)          # cosine (unit vectors)
        for j in range(k):
            if (lab == j).any():
                c = X[lab == j].mean(0); C[j] = c / (np.linalg.norm(c) + 1e-9)
    return lab

calls = 0
def mock_summarise(texts):
    global calls; calls += 1                       # one LLM call per cluster in a real build
    from collections import Counter
    cnt = Counter(w for t in texts for w in toks(t) if len(w) > 3)
    return "SUMMARY: " + " ".join(w for w, _ in cnt.most_common(6))

chunks = [
 "the river bank flooded after heavy monsoon rain in july",
 "flood barriers along the river were raised before the monsoon",
 "rain gauges recorded record monsoon rainfall near the river",
 "the central bank raised interest rates to curb inflation",
 "inflation expectations rose and the bank signalled more rate hikes",
 "bond yields climbed as interest rates and inflation stayed high",
 "the chess club met on friday to analyse the opening moves",
 "a grandmaster explained endgame technique to the chess club",
 "club members practised opening theory and endgame puzzles",
]
nodes = [dict(level=0, text=t, vec=embed(t)) for t in chunks]
level_nodes = nodes
for level, k in [(1, 3), (2, 1)]:
    X = np.stack([n["vec"] for n in level_nodes])
    lab = kmeans(X, k)
    new = []
    for j in range(k):
        members = [n["text"] for n, l in zip(level_nodes, lab) if l == j]
        if not members: continue
        s = mock_summarise(members)
        new.append(dict(level=level, text=s, vec=embed(" ".join(members))))
    nodes += new; level_nodes = new
print("nodes per level:", {l: sum(n['level']==l for n in nodes) for l in (0,1,2)}, "| mock summariser calls:", calls)

def collapsed_search(q, top=3):          # search ALL nodes of ALL levels together
    qv = embed(q); sc = [(float(n["vec"] @ qv), n) for n in nodes]
    return sorted(sc, key=lambda x: -x[0])[:top]
for q in ["what did the river flood barriers do in the monsoon", "which theme covers inflation, interest rates and the bank"]:
    print("\nQ:", q)
    for s, n in collapsed_search(q):
        print(f"  L{n['level']} {s:.2f} {n['text'][:70]}")
```
Output (my run):
```
nodes per level: {0: 9, 1: 3, 2: 1} | mock summariser calls: 4

Q: what did the river flood barriers do in the monsoon
  L1 0.76 SUMMARY: river monsoon rain bank flooded after
  L0 0.71 flood barriers along the river were raised before the monsoon
  L0 0.59 the river bank flooded after heavy monsoon rain in july

Q: which theme covers inflation, interest rates and the bank
  L1 0.72 SUMMARY: inflation bank interest rates central raised
  L0 0.60 the central bank raised interest rates to curb inflation
  L0 0.48 inflation expectations rose and the bank signalled more rate hikes
```
Four mock summariser calls built a 3-cluster level and a root. In the run, a summary node ranked first for each query. The level-1 clusters are not perfectly pure (the first summary mixes river and bank words) because hashed vectors and mock summaries are crude, which is itself a lesson: summary quality limits the tree.

**Follow-ups:**
- *Stale data?* Summaries go stale when leaves change; re-cluster and re-summarise the affected branches, or rebuild on a schedule.
- *Collapsed tree or traversal?* Collapsed is simpler and lets each query pick its own level; traversal is cheaper per query but an early wrong branch cannot be recovered (my reasoning, from memory of the paper's comparison).
- *Why not just a plain summary of each document?* One summary per document loses the middle levels; for hybrid and contextual enrichment see Q26.

**Common mistakes:** quoting the 20% as a general gain; saying RAPTOR extracts entities (it clusters text); ignoring index-time LLM cost; trusting summaries as ground truth with no citation back to leaves; confusing it with GraphRAG.


### Q28 ⭐⭐ 🟡 Walk through the GraphRAG indexing pipeline (text units, entity and relationship extraction, community detection, community summaries) and its cost.
**Asked at:** product, GenAI startups, enterprise teams
**Say this first (1 line):** GraphRAG indexing splits documents into text units, has an LLM extract entities, relationships and claims from each, clusters the graph into hierarchical communities with Leiden, and pre-writes a summary for each community, so global questions can be answered later from those summaries.
**Then explain:**
- **Pipeline (per the Microsoft GraphRAG docs):** (1) text units: chunks of the source; (2) extraction of entities, relationships and key claims from each unit; (3) hierarchical clustering with the Leiden technique, so you get communities at several granularities; (4) bottom-up community summaries, where the lower levels feed the higher ones.
- **Why this shape:** the paper's point is that plain vector RAG fails on "global" questions over a whole corpus (query-focused summarisation). Pre-built summaries give something to read for those (query modes: Q29).
- **Cost driver:** the extraction step needs an LLM call over every chunk, so cost scales with corpus size. This is reported by explainers; the docs page does not discuss cost, so I would measure it on a sample. Community summaries add calls on top.
- **Staleness:** new or edited documents change entities and possibly communities, so summaries go stale. Refresh cost is a reported concern: re-extract changed chunks, then re-cluster and re-summarise affected communities, or rebuild on a schedule.
- **Tuning:** the docs recommend prompt tuning on your own data, because the default extraction prompts will miss your domain's entity types.

**Example:** 100,000 chunks means on the order of 100,000 extraction calls before any summary. At an assumed 1,000 input and 300 output tokens each, that is around 100M input and 30M output tokens just for extraction. Run it on 1,000 chunks first, look at the extracted entities, tune the prompt, then scale.

**Code:** (run; TOY: dictionary extractor in place of the LLM, label propagation written from scratch in place of Leiden, 7 invented chunks; token counts are ASSUMED, not measured)
```python
import re
from collections import defaultdict

# TOY GraphRAG-style indexing. Extractor = hand-written dictionary (stands in for an LLM call per chunk).
# Communities = label propagation written from scratch (the real system uses hierarchical Leiden).
chunks = [
 "Asha leads Project Falcon at Acme.",
 "Project Falcon uses the Orion database.",
 "Ravi maintains the Orion database for Acme.",
 "Meera runs Project Lotus at Zenith.",
 "Project Lotus depends on the Pearl service.",
 "Zenith operates the Pearl service.",
 "Ravi once advised Zenith on security.",
]
ENTITIES = ["Asha","Ravi","Meera","Acme","Zenith","Project Falcon","Project Lotus","Orion database","Pearl service"]

def extract(chunk):                      # mock "LLM extraction": entities co-mentioned in a chunk are linked
    found = [e for e in ENTITIES if e in chunk]
    return found, [(a, b) for i, a in enumerate(found) for b in found[i+1:]]

edges = set(); mentions = defaultdict(list)
for ci, c in enumerate(chunks):
    ents, rels = extract(c)
    for e in ents: mentions[e].append(ci)
    for a, b in rels: edges.add((a, b))
adj = defaultdict(set)
for a, b in edges: adj[a].add(b); adj[b].add(a)

def label_propagation(adj, rounds=10):
    lab = {n: n for n in sorted(adj)}
    for _ in range(rounds):
        changed = False
        for n in sorted(adj):                                   # deterministic order
            cnt = defaultdict(int)
            for m in adj[n]: cnt[lab[m]] += 1
            best = max(sorted(cnt), key=lambda l: cnt[l])       # ties: alphabetical
            if cnt[best] > cnt.get(lab[n], 0): lab[n] = best; changed = True
        if not changed: break
    return lab
lab = label_propagation(adj)
comms = defaultdict(list)
for n, l in lab.items(): comms[l].append(n)
print("entities:", len(adj), "edges:", len(edges), "communities:", len(comms))
for i, (l, ms) in enumerate(sorted(comms.items())):
    print(f"  community {i}: {sorted(ms)}")

# LLM-call estimate. ALL numbers below are ASSUMED, not measured.
def estimate(N, chunk_tok=600, extract_out=300, comm_ratio=0.05, summ_in=3000, summ_out=500):
    ext_calls = N                                   # one extraction call per chunk
    comm_calls = int(N * comm_ratio)                # assumed: communities ~ 5% of chunk count
    tin = ext_calls * (chunk_tok + 400) + comm_calls * summ_in   # +400 assumed prompt overhead
    tout = ext_calls * extract_out + comm_calls * summ_out
    return ext_calls + comm_calls, tin, tout
print("\nASSUMED tokens: 600-token chunks, 400 prompt overhead, 300 out/extraction, 5% communities")
for N in (1_000, 10_000, 100_000):
    c, ti, to = estimate(N)
    print(f"N={N:>7,} chunks -> {c:>7,} LLM calls, ~{ti/1e6:6.1f}M input tok, ~{to/1e6:5.1f}M output tok")
```
Output (my run):
```
entities: 9 edges: 13 communities: 2
  community 0: ['Acme', 'Asha', 'Orion database', 'Project Falcon', 'Ravi']
  community 1: ['Meera', 'Pearl service', 'Project Lotus', 'Zenith']

ASSUMED tokens: 600-token chunks, 400 prompt overhead, 300 out/extraction, 5% communities
N=  1,000 chunks ->   1,050 LLM calls, ~   1.1M input tok, ~  0.3M output tok
N= 10,000 chunks ->  10,500 LLM calls, ~  11.5M input tok, ~  3.2M output tok
N=100,000 chunks -> 105,000 LLM calls, ~ 115.0M input tok, ~ 32.5M output tok
```
The estimate shows the shape: calls grow linearly with chunks. The assumptions (chunk size, prompt overhead, community ratio) are placeholders, so replace them with measured values. Label propagation here is a simple stand-in; Leiden optimises modularity and gives a hierarchy.

**Follow-ups:**
- *Why a hierarchy of communities?* Different questions need different zoom levels: a top community for "themes", a small one for a specific project.
- *Can you cut the cost?* Cheaper model for extraction, fewer or larger chunks, skip claim extraction, incremental updates. Check quality loss each time.
- *Is the graph accurate?* It is LLM-extracted, so noisy: duplicated entities ("Acme" vs "Acme Corp"), missed or invented relations. Sample and review (curated graphs: Q30).

**Common mistakes:** saying the graph is built by an algorithm without an LLM; forgetting that the cost is per chunk; ignoring updates; skipping prompt tuning; claiming GraphRAG beats vector RAG on all questions (the docs recommend basic search where vector search already works).


### Q29 ⭐⭐ 🟡 What are GraphRAG's query modes (global, local, DRIFT, basic), and which question types suit each?
**Asked at:** product, GenAI startups, enterprise teams
**Say this first (1 line):** Global search answers whole-corpus "what are the themes" questions from community summaries, local search answers questions about specific entities using their neighbours, DRIFT is local search enriched with community context, and basic is ordinary top-k vector search.
**Then explain:**
- **Global (per the docs):** holistic questions over the whole collection. Each community summary produces a partial answer, then the partials are combined into the final answer (map-reduce). Expensive: many LLM calls per query.
- **Local:** questions about particular entities ("who maintains X, what does X depend on"). Starts from the entity and pulls in its related entities, relationships and text units.
- **DRIFT:** local search plus community information, for questions that start at an entity but need broader context. Details of how it iterates are beyond what I verified; check the current docs.
- **Basic:** standard vector top-k. The docs themselves point to it for questions vector search already handles, so GraphRAG does not replace it.
- **Routing:** a small classifier or rules choose the mode; wrong routing is a failure mode of its own, so log the choice and evaluate it.

| Question | Mode |
|---|---|
| "What are the main themes across these 5,000 emails?" | Global |
| "Who maintains the Orion database?" | Local |
| "How does Project Falcon relate to the wider platform work?" | DRIFT |
| "What is the refund window for annual plans?" | Basic |

**Example:** "What are the main risks across the archive?" has no single chunk answering it. A global pass reads each community summary, extracts that community's risks, and a final step merges them. The same question to basic top-5 would return 5 chunks about risk and miss the rest.

**Code:** (run; TOY: keyword-rule router and mock summaries, no LLM and no GraphRAG library; the 6/6 only means the rules agree with six cases I wrote myself)
```python
import re

# TOY dispatcher + map-reduce global answer over MOCK community summaries. No LLM is called.
KNOWN_ENTITIES = ["Asha", "Ravi", "Project Falcon", "Project Lotus", "Orion database"]
GLOBAL_CUES = ["main themes", "overall", "across the", "summarise the whole", "big picture", "trends in"]
MULTI_CUES = ["how does", "relate", "connected to", "and also what else"]

def route(q):
    ql = q.lower()
    if any(c in ql for c in GLOBAL_CUES): return "global"
    ents = [e for e in KNOWN_ENTITIES if e.lower() in ql]
    if ents and any(c in ql for c in MULTI_CUES): return "drift"   # entity + open-ended exploration
    if ents: return "local"
    return "basic"

tests = [
 ("What are the main themes across the whole archive?", "global"),
 ("Who maintains the Orion database?", "local"),
 ("How does Project Falcon relate to the wider platform work?", "drift"),
 ("What is the refund window for annual plans?", "basic"),
 ("Summarise the big picture of engineering risks", "global"),
 ("Tell me about Ravi", "local"),
]
ok = 0
for q, want in tests:
    got = route(q); ok += got == want
    print(f"{got:6} (want {want:6}) <- {q}")
print("router agreement on 6 hand-written cases:", ok, "/", len(tests))

# MAP-REDUCE over mock community summaries
communities = {
 "C0": "Acme engineering: Project Falcon on Orion database; risk: single maintainer (Ravi).",
 "C1": "Zenith operations: Project Lotus depends on Pearl service; risk: vendor dependency.",
 "C2": "Hiring: three open roles; risk: attrition in platform team.",
}
def map_step(question, summary):           # mock partial answer with a helpfulness score (an LLM would write+score)
    risks = re.findall(r"risk: ([^.;]+)", summary)
    return {"score": 80 if risks else 10, "partial": risks}
def reduce_step(partials, budget=2):       # keep best partials, then (mock) combine
    best = sorted(partials, key=lambda p: -p["score"])[:budget]
    return "Main risks: " + "; ".join(r for p in best for r in p["partial"])
q = "What are the main risks across the archive?"
partials = [map_step(q, s) for s in communities.values()]
print("\nmap calls:", len(partials), "| reduce calls: 1")
print(reduce_step(partials))
```
Output (my run):
```
global (want global) <- What are the main themes across the whole archive?
local  (want local ) <- Who maintains the Orion database?
drift  (want drift ) <- How does Project Falcon relate to the wider platform work?
basic  (want basic ) <- What is the refund window for annual plans?
global (want global) <- Summarise the big picture of engineering risks
local  (want local ) <- Tell me about Ravi
router agreement on 6 hand-written cases: 6 / 6

map calls: 3 | reduce calls: 1
Main risks: single maintainer (Ravi); vendor dependency
```

**Follow-ups:**
- *Global cost?* Calls scale with the number of communities at the chosen level; a higher (coarser) level is cheaper but less detailed. Cap the number of partials passed to the reduce step.
- *Can you skip the router and run all modes?* You can, but it multiplies cost; route first, fall back to basic.
- *How do you evaluate global answers?* No single gold chunk, so use rubric or pairwise LLM judging (the paper uses comprehensiveness and diversity, judged by an LLM, reported by the authors); Part 9 covers judging.

**Common mistakes:** using global search for factual lookups; treating GraphRAG as always better than vector RAG; forgetting global-mode cost; keyword routers with no evaluation; assuming DRIFT details without reading the docs.


### Q30 ⭐⭐ 🟡 Knowledge-graph retrieval vs GraphRAG-style summaries: when do graph databases, entity linking and text-to-Cypher help, and what are the risks?
**Asked at:** product, enterprise teams, search teams
**Say this first (1 line):** If you already have a curated graph with a clean schema, query it directly (entity linking, then a graph query for multi-hop traversal); GraphRAG-style indexing is for turning unstructured text into a graph and summaries when no graph exists.
**Then explain:**
- **Curated graph + graph DB:** products, org charts, supply chains, ontologies. Facts are structured and verified, so multi-hop questions ("which suppliers of X are located in Y?") are exact graph queries in Cypher or SPARQL, not similarity guesses.
- **Entity linking is the weak joint:** the user says "Asha"; which node is that? A wrong link gives a confident, wrong answer with a clean-looking trace. Return top candidates with scores, ask when ambiguous, and add context (company, date).
- **Text-to-Cypher risks:** the LLM can invent relationship types or labels that are not in the schema, write an expensive query, or be steered by user text into a query it should not run (injection). Controls: give the schema in the prompt, validate the query against it, run with a read-only role, enforce row-level permissions in the database and not in the prompt, set limits and timeouts.
- **Hybrid:** use vector retrieval to find the entry nodes or relevant passages, then the graph to expand to neighbours; or attach text chunks to nodes and return both.
- **Versus LLM-extracted graphs (Q28):** extracted graphs are noisy and costly to build and refresh; a curated one is only as good as its upkeep but each edge was put there on purpose.

**Example:** Query "Where is the company that employs Asha located?" is a 2-hop path person -> company -> city. Answer by traversal, with a source for every edge. A question like "what are the recurring complaints in these 10,000 tickets?" has no graph; that is where summaries over text (Q28, Q29) fit.

**Code:** (run; TOY in-memory triple store with invented names; difflib string similarity stands in for a real entity linker; no graph database used)
```python
import difflib
from collections import defaultdict

# TOY in-memory triple store, 2-hop query, fuzzy entity linking. Invented data.
triples = [
 ("Asha Rao", "WORKS_AT", "Acme"),
 ("Asha Kumar", "WORKS_AT", "Zenith"),
 ("Acme", "LOCATED_IN", "Pune"),
 ("Zenith", "LOCATED_IN", "Chennai"),
 ("Ravi", "WORKS_AT", "Acme"),
]
out = defaultdict(list)
for s, p, o in triples: out[(s, p)].append(o)
names = sorted({t[0] for t in triples} | {t[2] for t in triples})

def link(mention, cutoff=0.5):
    # fuzzy linking by string similarity; returns (entity, score) candidates, best first
    sc = [(difflib.SequenceMatcher(None, mention.lower(), n.lower()).ratio(), n) for n in names]
    return [(n, round(s, 2)) for s, n in sorted(sc, reverse=True) if s >= cutoff]

def two_hop(entity, p1, p2):
    return [o2 for o1 in out[(entity, p1)] for o2 in out[(o1, p2)]]

mention = "Asha"
cands = link(mention)
print("candidates for 'Asha':", cands)
top = cands[0][0]
print("naive: take top candidate ->", top, "->", two_hop(top, "WORKS_AT", "LOCATED_IN"), "(confident but may be the wrong person)")
if len(cands) > 1 and cands[0][1] - cands[1][1] < 0.15:
    print("guard: scores within 0.15 -> ambiguous, ask the user which one")
print("\nresolved 'Asha Kumar':", two_hop(link("Asha Kumar")[0][0], "WORKS_AT", "LOCATED_IN"))

# text-to-query risk: validate a generated query against the schema before running it
SCHEMA = {"WORKS_AT", "LOCATED_IN"}
def validate(rel_types):
    bad = [r for r in rel_types if r not in SCHEMA]
    return "ok" if not bad else f"reject: unknown relationship {bad}"
print("\nschema check, LLM-proposed rels ['WORKS_AT','EMPLOYED_BY']:", validate(["WORKS_AT", "EMPLOYED_BY"]))
```
Output (my run):
```
candidates for 'Asha': [('Asha Rao', 0.67), ('Asha Kumar', 0.57)]
naive: take top candidate -> Asha Rao -> ['Pune'] (confident but may be the wrong person)
guard: scores within 0.15 -> ambiguous, ask the user which one

resolved 'Asha Kumar': ['Chennai']

schema check, LLM-proposed rels ['WORKS_AT','EMPLOYED_BY']: reject: unknown relationship ['EMPLOYED_BY']
```
The naive linker silently picked Asha Rao and gave Pune. The guard noticed two close candidates. The schema check rejects a made-up relationship type before anything runs, which is the cheapest defence against hallucinated labels.

**Follow-ups:**
- *Which is better, graph DB or vector DB?* Different jobs: graph for exact relational queries, vector for fuzzy text. Many systems use both.
- *Permissions?* Filter in the database layer by the caller's identity; never rely on the LLM to hide nodes.
- *Evaluation?* Check entity-linking accuracy and query execution accuracy separately, since either can fail alone.

**Common mistakes:** trusting the top fuzzy match; letting generated Cypher run with write access; putting the whole schema into every prompt without validation; building an LLM-extracted graph when a clean database already exists; treating graph retrieval as a replacement for vector search.


### Q31 ⭐⭐ 🟡 Multi-hop retrieval strategies: iterative retrieval that interleaves reasoning and search, stopping conditions, and how to avoid drifting off-topic.
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** For multi-hop questions one search is not enough, so you loop: reason about what you have, form the next query from the new evidence, search again, and stop when a separate check says the evidence is sufficient or a budget runs out.
**Then explain:**
- **Why single-shot fails:** "Which city has the institute where the Falcon project leader studied?" needs person, then institute, then city. The last fact shares almost no words with the question, so one query will not find it.
- **Interleaving (IRCoT-style, from memory, not verified):** alternate a reasoning step with a retrieval step, using each reasoning step as the next query. Agent frameworks (Part 8) generalise this.
- **Stopping conditions:** (1) sufficiency judged by an independent check (not the same generator saying "I'm done"; self-judgement is unreliable, per agentic-RAG explainers); (2) max hops; (3) no new documents; (4) optionally a token or time budget.
- **Drift:** each hop can wander because the query is built from the last document, not the question. Fixes: keep the original question in every query or in the reasoning prompt, exclude documents already seen so only new evidence is added, cap hops, and have the sufficiency check compare evidence with the original question.
- **Cost:** each hop is an LLM call plus a search, so latency grows with hops. Route simple questions to single-shot (Q7, Q38).

**Example:** Falcon question above: hop 1 finds the project leader, hop 2 the institute, hop 3 the city; stop. Without the stop rule the loop keeps following "Patna" into ghats and tourism timings: more tokens, a more distracting context, no benefit.

**Code:** (run; MOCK: word-overlap retriever over a 7-document toy KB, rule-based next query and sufficiency check, no LLM; this shows the control flow only)
```python
import re

# MOCK multi-hop loop over a tiny knowledge base. Retriever = word overlap (toy); the "reasoner" just
# builds the next query from the newest evidence; sufficiency = a rule. No LLM, no real embeddings.
KB = {
 1: "Asha led the Falcon project.",
 2: "Asha studied at Nalanda Institute.",
 3: "Nalanda Institute is located in Patna.",
 4: "Patna is known for its river ghats.",
 5: "River ghats host evening aarti tourism.",
 6: "Aarti tourism timings change in winter.",
 7: "Falcon is also the name of a bird of prey.",
}
STOP = {"the","was","by","is","in","of","a","at","for","its","also","name","which","where","who","led"}
def toks(t): return set(re.findall(r"[a-z]+", t.lower())) - STOP
def search(q, exclude):
    sc = sorted(((len(toks(q) & toks(d)), -i) for i, d in KB.items() if i not in exclude), reverse=True)
    return [-i for s, i in sc[:1] if s > 0]

def sufficient(seen):                      # mock independent check: do we hold a "located in" fact for the institute?
    return any("located in" in KB[i] for i in seen)

def run(question, max_hops=5, keep_question=True, check=True):
    seen, q, trace = [], question, []
    for hop in range(1, max_hops + 1):
        new = search(q, exclude=seen)
        if not new:
            trace.append(f"hop {hop}: no new documents -> stop"); break
        seen += new; trace.append(f"hop {hop}: doc {new[0]}: {KB[new[0]]}")
        if check and sufficient(seen):
            trace.append("sufficiency check passed -> stop"); break
        q = (question + " " if keep_question else "") + KB[new[0]]     # next query from the newest evidence
    else:
        trace.append(f"hop limit {max_hops} reached -> stop")
    return seen, trace

Q = "Which city has the institute where the Falcon project leader studied?"
for name, kw in [("guarded: keep question, sufficiency check, hop limit 5", dict()),
                 ("drift: query = newest doc only, no sufficiency check", dict(keep_question=False, check=False))]:
    seen, tr = run(Q, **kw); print("==", name); print("\n".join("  " + t for t in tr))
```
Output (my run):
```
== guarded: keep question, sufficiency check, hop limit 5
  hop 1: doc 1: Asha led the Falcon project.
  hop 2: doc 2: Asha studied at Nalanda Institute.
  hop 3: doc 3: Nalanda Institute is located in Patna.
  sufficiency check passed -> stop
== drift: query = newest doc only, no sufficiency check
  hop 1: doc 1: Asha led the Falcon project.
  hop 2: doc 2: Asha studied at Nalanda Institute.
  hop 3: doc 3: Nalanda Institute is located in Patna.
  hop 4: doc 4: Patna is known for its river ghats.
  hop 5: doc 5: River ghats host evening aarti tourism.
  hop limit 5 reached -> stop
```
The guarded loop stopped at hop 3 once a "located in" fact was held. The unguarded one ran to the hop limit and added two irrelevant documents. A real drift failure is subtler (a plausible but wrong bridge entity), which is why you also log the hop trace and evaluate it.

**Follow-ups:**
- *Decomposition up front vs iterating?* Decomposing into sub-questions works when the steps are independent; iterating is needed when step 2 depends on the answer to step 1.
- *How do you evaluate?* Check that each gold supporting document is retrieved (recall per hop) and the final answer; see Part 9.
- *What if hop 1 is wrong?* Errors compound, so keep the top 2-3 candidates per hop or let the checker trigger a re-query.

**Common mistakes:** no max-hop limit; letting the generator grade its own sufficiency; dropping the original question from later queries; re-retrieving the same documents; using loops for questions that one search answers.


### Q32 ⭐⭐ 🟡 What are adaptive and self-reflective retrieval (Self-RAG, reflection tokens), and what simpler prompt-based alternatives exist?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** Adaptive retrieval means the system decides whether and when to retrieve instead of always fetching a fixed top-k; Self-RAG trains one language model to do that and to critique its own output using special reflection tokens, and prompt-based gates give a cheaper approximation.
**Then explain:**
- **Self-RAG (per the abstract):** one LM trained to retrieve on demand, and to generate and critique both its passages and its own output with reflection tokens. This contrasts with fixed top-k retrieval, which fetches whether or not it helps and can drag in irrelevant passages.
- **Reported results (authors' claims):** the 7B and 13B models are reported to beat ChatGPT and retrieval-augmented Llama2-chat on open-domain QA, reasoning and fact verification, with better factuality and citation accuracy. Treat these as the paper's setting, not a guarantee for your task.
- **The catch:** it needs training with the special tokens (a critic or labelled data and fine-tuning your own generator). If you call a hosted model through an API you cannot do that.
- **Prompt-based alternatives:** (1) a retrieval gate: classify the query (chit-chat, task on supplied text, private or time-sensitive, general knowledge) and use model confidence; (2) relevance grading of retrieved chunks before they enter the prompt; (3) a groundedness check on the draft answer against its chunks, with a re-retrieve or "not found" on failure.
- **Trade-off:** every gate is another LLM call or classifier and can be wrong. A wrong "no retrieval" on a private fact causes a confident hallucination, so bias the gate toward retrieving when unsure, and log decisions.

**Example:** "Thanks!" needs no retrieval. "What is our refund policy?" must retrieve because the model cannot know it. "Capital of France?" can skip it. Sending all three through top-5 retrieval wastes a search and adds noisy context for the first and last.

**Code:** (run; MOCK gate with hand-written rules and an invented confidence number, no model and no training; it illustrates the decision logic only)
```python
import re

# MOCK retrieval gate: decide whether to retrieve, from query type and a (mock) model-confidence number.
# Rules and thresholds are hand-written assumptions, not a trained model.
def gate(query, model_conf, retrieval_top_score=None, conf_threshold=0.8):
    q = query.lower()
    if re.search(r"\b(hi|hello|thanks|thank you)\b", q): return "no_retrieve", "chit-chat"
    if re.search(r"\b(translate|rewrite|rephrase|summari[sz]e this)\b", q): return "no_retrieve", "task on supplied text"
    if re.search(r"\b(policy|our|latest|current|202\d|price|order|ticket)\b", q): return "retrieve", "private or time-sensitive"
    if model_conf >= conf_threshold: return "no_retrieve", f"confident ({model_conf:.2f} >= {conf_threshold})"
    return "retrieve", f"low confidence ({model_conf:.2f})"

def relevance_grade(score, keep=0.5):        # mock relevance grader on a retriever score
    return "relevant" if score >= keep else "irrelevant"

cases = [("Hello, thanks!", 0.9), ("Translate this paragraph to Hindi", 0.9),
         ("What is our refund policy?", 0.9), ("What is the capital of France?", 0.97),
         ("What is the half-life of isotope X-7?", 0.35)]
for q, c in cases:
    d, why = gate(q, c); print(f"{d:12} {why:28} <- {q}")
print("grade scores 0.8, 0.3 ->", relevance_grade(0.8), relevance_grade(0.3), "(irrelevant top hit => answer without it or say not found)")
```
Output (my run):
```
no_retrieve  chit-chat                    <- Hello, thanks!
no_retrieve  task on supplied text        <- Translate this paragraph to Hindi
retrieve     private or time-sensitive    <- What is our refund policy?
no_retrieve  confident (0.97 >= 0.8)      <- What is the capital of France?
retrieve     low confidence (0.35)        <- What is the half-life of isotope X-7?
grade scores 0.8, 0.3 -> relevant irrelevant (irrelevant top hit => answer without it or say not found)
```
Self-reported confidence from an LLM is often poorly calibrated, so the 0.8 threshold must be tuned on labelled queries (retrieval helped vs not), and it should be set to favour retrieval.

**Follow-ups:**
- *Self-RAG vs a prompt-based gate?* Self-RAG integrates the decision into the model through training; a gate is a separate component you can build today and change without retraining.
- *How do you measure a gate?* Answer quality and cost, with and without it, split by gate decision; check false "no retrieve" on private-fact queries.
- *Relation to CRAG?* Self-RAG judges before and during generation; corrective RAG reacts to bad retrieval (Q33).

**Common mistakes:** saying Self-RAG is a prompt technique; quoting the paper's wins as general; skipping retrieval for questions about private data; trusting the model's stated confidence without calibration; no logging of gate decisions.


### Q33 ⭐⭐ 🟡 What is corrective RAG (CRAG)? Explain the retrieval evaluator, the fallback actions, and how production systems approximate it.
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Corrective RAG adds a retrieval evaluator that scores the retrieved documents and, depending on confidence, uses them (refined), throws them away and falls back to web search, or combines both, so bad retrieval does not silently poison the answer.
**Then explain:**
- **Evaluator:** a lightweight model that judges whether the retrieved documents fit the query. In the paper it is a fine-tuned T5-large (reported via a glossary snippet; I did not open the paper). It outputs one of three verdicts.
- **Actions (as described in explainers):** Correct: keep the documents and refine them (strip irrelevant parts, Q34). Incorrect: discard them and search the web instead. Ambiguous: combine refined documents with web results.
- **Production approximation (reported):** many teams skip training an evaluator and use the reranker's top score, or an LLM relevance grader, as a confidence signal. Above a high threshold: answer. Below a low one: fallback (another index, query rewrite, web search, or "I don't know"). In between: do both.
- **Fallback risks:** web content is untrusted (it can be wrong, spammy or carry injected instructions: see Part 6 Q36 and Part 11); it adds latency and per-call cost; for private enterprise questions the right fallback is often "not found" plus a rewrite, not the open web.
- **Tuning:** pick thresholds on labelled queries by the cost of a wrong "trust" vs a wasted fallback. Reranker scores are not calibrated across queries or models, so calibrate them.

**Example:** Query "What is our parental leave policy?" returns chunks about travel policy, with a top reranker score of 0.2. A fixed top-5 pipeline would still stuff them in and the model might invent an answer. The controller sees 0.2 below the low threshold and rewrites the query or says the policy was not found.

**Code:** (run; SYNTHETIC: 5,000 queries with assumed score distributions, 70% good retrievals; thresholds scanned; this is not a real reranker and the accuracies are not expected on real data)
```python
import numpy as np

# SYNTHETIC data: top reranker score per query, drawn from assumed distributions.
# 70% of queries have good retrieval (gold chunk present), 30% bad. Scores are NOT from a real reranker.
rng = np.random.default_rng(0)
n = 5000
good = rng.random(n) < 0.70
score = np.where(good, rng.normal(0.70, 0.15, n), rng.normal(0.35, 0.15, n)).clip(0, 1)

def controller(s, hi, lo):
    return np.where(s >= hi, "correct", np.where(s <= lo, "incorrect", "ambiguous"))

print("thresholds (hi, lo) | correct / ambiguous / incorrect | acc of trigger | bad slipped through | good sent to fallback")
for hi, lo in [(0.5, 0.5), (0.6, 0.4), (0.65, 0.3), (0.75, 0.25)]:
    act = controller(score, hi, lo)
    frac = {a: float((act == a).mean()) for a in ("correct", "ambiguous", "incorrect")}
    # decision "trust retrieval" = correct; "distrust" = incorrect; ambiguous counts as extra work (both sources)
    decided = act != "ambiguous"
    acc = float(((act == "correct") == good)[decided].mean())
    slipped = float(((act == "correct") & ~good).sum() / (~good).sum())
    wasted = float(((act == "incorrect") & good).sum() / good.sum())
    print(f"({hi:.2f},{lo:.2f})        | {frac['correct']:.2f} / {frac['ambiguous']:.2f} / {frac['incorrect']:.2f}"
          f"             | {acc:.3f}          | {slipped:.3f}               | {wasted:.3f}")
```
Output (my run):
```
thresholds (hi, lo) | correct / ambiguous / incorrect | acc of trigger | bad slipped through | good sent to fallback
(0.50,0.50)        | 0.69 / 0.00 / 0.31             | 0.888          | 0.165               | 0.089
(0.60,0.40)        | 0.54 / 0.25 / 0.21             | 0.956          | 0.050               | 0.026
(0.65,0.30)        | 0.46 / 0.42 / 0.12             | 0.981          | 0.025               | 0.005
(0.75,0.25)        | 0.27 / 0.65 / 0.08             | 0.994          | 0.004               | 0.001
```
The accuracy column only counts queries where the controller committed to correct or incorrect, so widening the ambiguous band "improves" it by deferring decisions. Read it with the ambiguous fraction, because ambiguous means extra cost (both paths run). That trade-off is the point: tighter thresholds miss fewer bad retrievals but send more traffic down the expensive path.

**Follow-ups:**
- *Why not always do web search?* Cost, latency, and untrusted content; also it may not contain private facts.
- *How do you choose thresholds?* Plot trigger precision and recall against the labelled "retrieval was good" flag and choose from the cost of each error.
- *Evaluator vs LLM judge?* A small trained evaluator is cheap and fast but needs data; an LLM grader is flexible but costs a call each.

**Common mistakes:** treating raw reranker scores as probabilities; one global threshold for all query types; no cap on fallback calls; trusting web results as much as the internal index; not logging how often each action fires.


### Q34 ⭐⭐ 🟡 How do you compress or filter retrieved context (extractive compression, LLM filtering, token budgets), and what is the risk of dropping evidence?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Compression shrinks the retrieved text before generation, by selecting the sentences that matter (extractive) or having an LLM filter or summarise (abstractive), to save tokens and cut noise, at the risk of deleting the one sentence the answer needs or changing its meaning.
**Then explain:**
- **Extractive:** score each sentence against the query (a reranker or cross-encoder, embedding similarity, or overlap) and keep the top ones in original order. Cheap, no rewriting, so wording stays faithful.
- **LLM-based:** ask a model to extract only the relevant parts or write a short summary. More flexible (it can resolve "it" or merge facts) but costs a call per query, adds latency, and can paraphrase numbers or negations wrongly. Ask it to quote spans, then verify the quotes exist in the source.
- **Token budget:** fix a context budget (say N tokens) and fill it by score, not by "top-k chunks". Keep chunk ids so citations still work.
- **Main risk:** the supporting sentence often does not look relevant on its own ("It was founded in 1998."). Sentence scoring against the query drops it. Mitigate by keeping neighbouring sentences, scoring chunks and sentences together, or compressing less when the retrieval confidence is low.
- **Evaluate:** measure supporting-span retention against compression ratio on a labelled set, and end-to-end answer correctness. Pick the ratio where retention starts to fall off.

**Example:** 5 chunks of 400 tokens is 2,000 tokens. Keeping the best 30% of sentences gives about 600 tokens, a 70% cut in generator input. If the gold sentence is retained 95% of the time you would take that; if it is 70%, you have traded accuracy for cost.

**Code:** (run; SYNTHETIC: 2,000 invented documents of 10 sentences, toy overlap scoring; 30% of the supporting sentences are written as indirect, so they share no words with the query by construction)
```python
import random, re
import numpy as np

# SYNTHETIC test of sentence-level extractive compression. Toy scoring = query-word overlap.
random.seed(0)
vocab = [f"w{i}" for i in range(200)]
def make_example():
    q = random.sample(vocab, 3)
    sents = [" ".join(random.choices(vocab, k=8)) + "." for _ in range(10)]
    # some distractors share one query word
    for i in random.sample(range(10), 3):
        s = sents[i].split(); s[random.randrange(len(s))] = random.choice(q); sents[i] = " ".join(s)
    sup = random.randrange(10)
    direct = random.random() < 0.7                 # 70% of supports mention query words; 30% are indirect ("It was ...")
    if direct: sents[sup] = " ".join(random.choices(vocab, k=4) + q[:2] + ["ANSWER"]) + "."
    else:      sents[sup] = " ".join(["it", "was"] + random.choices(vocab, k=4) + ["ANSWER"]) + "."
    return q, sents, sup, direct

def score(q, s): return len(set(q) & set(re.findall(r"[a-z0-9]+", s.lower())))

data = [make_example() for _ in range(2000)]
print("ratio kept | support retained (all) | direct | indirect | mean tokens kept")
for keep in (1.0, 0.5, 0.3, 0.2, 0.1):
    k = max(1, round(10 * keep)); ret = {"all": [], True: [], False: []}; toks = []
    for q, sents, sup, direct in data:
        order = sorted(range(10), key=lambda i: (-score(q, sents[i]), i))[:k]      # ties: earlier sentence first
        hit = sup in order; ret["all"].append(hit); ret[direct].append(hit)
        toks.append(sum(len(sents[i].split()) for i in order))
    print(f"{keep:>9.1f}  | {np.mean(ret['all']):.3f}                  | {np.mean(ret[True]):.3f}  | {np.mean(ret[False]):.3f}    | {np.mean(toks):.0f}")
```
Output (my run):
```
ratio kept | support retained (all) | direct | indirect | mean tokens kept
      1.0  | 1.000                  | 1.000  | 1.000    | 79
      0.5  | 0.779                  | 1.000  | 0.264    | 39
      0.3  | 0.717                  | 1.000  | 0.055    | 23
      0.2  | 0.704                  | 0.993  | 0.028    | 15
      0.1  | 0.630                  | 0.893  | 0.017    | 7
```
Direct support survives down to keeping 20% of sentences, while indirect support is lost as soon as compression starts (chance level: around the keep ratio). The 30% indirect share is my assumption; the lesson is that overlap-based compression is blind to context-dependent sentences, so a real system needs a better scorer, neighbour expansion, or a retained-evidence check.

**Follow-ups:**
- *Compress before or after reranking?* After: the reranker picks the chunks, then compression trims inside them.
- *Is compression worth it with long-context models?* Cost and noise still matter; also "lost in the middle" (Part 1 Q19) means shorter, cleaner context can help.
- *How do you catch meaning changes?* A faithfulness check of the compressed text against the source, and a sample of human review.

**Common mistakes:** compressing aggressively with no retention metric; dropping context needed for pronouns, dates or negations; letting the LLM paraphrase numbers; losing chunk ids so citations break; applying one ratio to every query.


### Q35 ⭐⭐ 🟡 How do you answer questions over very long documents or many documents (hierarchical retrieval, map-reduce, iterative refinement)?
**Asked at:** product, GenAI startups, enterprise teams
**Say this first (1 line):** Narrow the search in stages (document, then section, then chunk) for specific questions, use map-reduce or refine only when the answer needs the whole text, add summary indexes for broad questions, and consider a long-context model when the material fits.
**Then explain:**
- **Hierarchical retrieval:** stage 1 picks the right documents (or sections) using document-level vectors, titles or summaries; stage 2 searches chunks only inside them. It cuts the candidate pool and removes look-alike chunks from unrelated documents. Ceiling: if stage 1 misses the document, stage 2 cannot recover (the same shortlist ceiling as reranking).
- **Map-reduce:** run a question over every part and combine the partial answers. Right for "summarise all" or "list all risks", costly (one call per part). **Refine:** go through parts in order and update a running answer. Cheaper in parallelism terms but sequential and order-sensitive. Skeleton for both: Part 6 Q49, not repeated here.
- **Summary indexes:** pre-built summaries at several levels (RAPTOR in Q27, communities in Q28) let broad questions hit one node instead of many chunks.
- **Long-context models:** if the relevant documents fit, sending them whole is simpler, but cost grows per query and quality can degrade for evidence in the middle (Part 1 Q19, Q36 here).
- **Pick by question type:** lookup goes to hierarchical or flat retrieval; "across all documents" goes to map-reduce or summary indexes; "compare two contracts" goes to fetching both documents in full.

**Example:** 5,000 contracts, each about 40 chunks (200,000 chunks). "What is the notice period in the Acme contract?" Stage 1 finds the Acme contract by title and entity metadata; stage 2 searches its 40 chunks. Flat search over 200,000 chunks might return the notice clause of a different company's near-identical contract.

**Code:** (run; TOY: hashed bag-of-words vectors, 60 documents x 15 chunks, 3 look-alike decoy chunks per query; recall values are properties of this synthetic setup only)
```python
import random, zlib
import numpy as np

# TOY corpus: 60 documents x 15 chunks. Hashed bag-of-words embeddings (toy, not semantic).
random.seed(1); np.random.seed(1)
D = 256
vocab = [f"f{i}" for i in range(500)]
def embed(words):
    v = np.zeros(D)
    for w in words: v[zlib.crc32(w.encode()) % D] += 1
    n = np.linalg.norm(v); return v / n if n else v

n_docs, n_chunks = 60, 15
topics = [[f"topic{d}a", f"topic{d}b"] for d in range(n_docs)]
chunks, doc_of = [], []
queries = []                                   # (query words, target chunk index)
for d in range(n_docs):
    for c in range(n_chunks):
        w = random.choices(vocab, k=25)
        if random.random() < 0.4: w += topics[d]            # topic words appear in ~40% of a document's chunks
        chunks.append(w); doc_of.append(d)
for d in range(n_docs):                         # one query per doc: 2 topic words + 2 detail words
    detail = [f"detail{d}x", f"detail{d}y"]
    tgt = d * n_chunks + random.randrange(n_chunks)
    chunks[tgt] = chunks[tgt][:25] + detail                 # target chunk has details but NOT necessarily topic words
    for _ in range(3):                                      # decoys in other docs share exactly the detail words
        o = random.randrange(len(chunks))
        if doc_of[o] != d: chunks[o] = chunks[o] + detail
    queries.append((topics[d] + detail, tgt))
C = np.stack([embed(w) for w in chunks])
doc_vec = np.stack([C[d*n_chunks:(d+1)*n_chunks].mean(0) for d in range(n_docs)])
doc_vec /= np.linalg.norm(doc_vec, axis=1, keepdims=True)

def flat(q, k):  return list(np.argsort(-(C @ embed(q)))[:k])
def hier(q, k, n_top_docs=3):
    top_docs = np.argsort(-(doc_vec @ embed(q)))[:n_top_docs]          # stage 1: documents
    cand = [i for d in top_docs for i in range(d*n_chunks, (d+1)*n_chunks)]
    return sorted(cand, key=lambda i: -(C[i] @ embed(q)))[:k]           # stage 2: chunks inside them

for k in (1, 5):
    rf = np.mean([t in flat(q, k) for q, t in queries]); rh = np.mean([t in hier(q, k) for q, t in queries])
    print(f"recall@{k}: flat {rf:.3f} | hierarchical (top-3 docs then chunks) {rh:.3f}")
cand_flat = len(chunks); cand_h = 3 * n_chunks
print("chunks scored per query: flat", cand_flat, "| stage 2 of hierarchical", cand_h, "(+", n_docs, "document scores)")
dr = np.mean([doc_of[t] in list(np.argsort(-(doc_vec @ embed(q)))[:3]) for q, t in queries])
print(f"stage-1 ceiling: target document in top-3 documents for {dr:.3f} of queries")
```
Output (my run):
```
recall@1: flat 0.000 | hierarchical (top-3 docs then chunks) 0.117
recall@5: flat 0.200 | hierarchical (top-3 docs then chunks) 0.467
chunks scored per query: flat 900 | stage 2 of hierarchical 45 (+ 60 document scores)
stage-1 ceiling: target document in top-3 documents for 0.983 of queries
```
The hierarchical path beats flat here because the decoys carry the same detail words but live in other documents. It is far from perfect: stage 1 reaches the right document for 98% of queries, yet recall@5 is only 0.47, because within the chosen documents the chunks carrying the topic words outrank the detail chunk. That is a stage-2 scoring problem, so it needs a reranker or hybrid scoring (Q2, Q5).

**Follow-ups:**
- *How many documents should stage 1 keep?* Enough to cover the stage-1 miss rate you can tolerate; measure document recall@n and the cost of larger n.
- *Where does metadata fit?* Filter by entity, date or type before or during stage 1 (Part 6 Q44).
- *Map-reduce vs hierarchical?* Hierarchical finds a needle; map-reduce answers aggregate questions.

**Common mistakes:** flat search over everything with no document context; map-reduce for simple lookups; no safeguard when stage 1 misses; building summaries and trusting them without links back to the source; ignoring that every map call costs money.


### Q36 ⭐⭐ 🟡 When is RAG unnecessary because the corpus fits in the context window? Work through the cost and quality trade-off at scale.
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** If the whole knowledge base is small (the Contextual Retrieval post suggests under about 200,000 tokens), is mostly static and has no per-user permissions, putting it all in the prompt with prompt caching can beat building RAG; as corpus size, query volume, update rate or access control grow, RAG wins.
**Then explain:**
- **The reported guidance:** Anthropic's Contextual Retrieval post suggests skipping RAG and including the entire knowledge base in the prompt when it is under about 200,000 tokens. That is a vendor suggestion at the time of writing; context limits and prices change, so check current numbers.
- **Cost:** full-prompt cost per query is about (corpus tokens + question) x input price. RAG cost is about (k chunks x chunk size + question) x price, plus the retrieval stack. Caching a static prefix can cut the repeat cost of the corpus (reported; the discount and cache lifetime depend on the provider, so check terms).
- **Quality:** more context is not free. Models can miss evidence buried in the middle of a long prompt (Part 1 Q19), and latency rises with prompt length even when cached. Retrieval can give a cleaner, shorter context, though retrieval itself can miss.
- **Things that favour RAG:** the corpus is large or grows; documents change often (cache invalidates on any change to the prefix); different users may see different documents (permissions and per-user filtering are easier with a retrieval filter than by building one prompt per user); you need citations to specific passages; high query volume.
- **Things that favour full prompt:** small stable corpus, low to moderate volume, fast build, and questions needing the whole document.

**Example:** A 60-page internal handbook (about 40,000 tokens), updated quarterly, same for all staff, 500 questions a day: full prompt with caching is a sensible first version. A 5M-token policy library with team-level access rules and daily edits is RAG territory.

**Code:** (run; every price, discount and hit rate is an ASSUMED placeholder in abstract cost units, so only the ratios mean anything; it ignores vector DB and reranker cost, so RAG's true cost is somewhat higher)
```python
# Cost model: whole-corpus-in-prompt vs RAG. ALL numbers are ASSUMED placeholders, not real prices.
PRICE_IN = 1.0            # ASSUMED: 1 cost unit per 1M input tokens (only ratios matter)
CACHE_READ_FRAC = 0.10    # ASSUMED: cached prefix tokens cost 10% of normal input price (check provider terms)
CACHE_HIT = 0.90          # ASSUMED: share of queries that hit a warm cache
RAG_TOKENS = 5 * 500 + 300  # ASSUMED: 5 chunks x 500 tokens + 300 prompt/question tokens
SHORT = 200               # ASSUMED question + instruction tokens on the full-context path
DAYS = 30

def full_ctx(corpus, q, cached):
    per = corpus + SHORT
    if cached:
        eff = CACHE_HIT * (corpus * CACHE_READ_FRAC + SHORT) + (1 - CACHE_HIT) * per
    else: eff = per
    return eff * q * PRICE_IN / 1e6
def rag(q): return RAG_TOKENS * q * PRICE_IN / 1e6          # ignores embedding/vector-DB/rerank cost

print("monthly cost units (ASSUMED prices) | corpus tokens | queries/day | full prompt | full + cache | RAG (tokens only)")
for corpus in (20_000, 100_000, 190_000):
    for qpd in (100, 10_000, 1_000_000):
        q = qpd * DAYS
        print(f"{corpus:>12,} | {qpd:>10,} | {full_ctx(corpus,q,False):>11,.1f} | {full_ctx(corpus,q,True):>11,.1f} | {rag(q):>9,.1f}")
# break-even corpus size where cached full-context per-query tokens equal RAG tokens
for hit in (0.9,):
    eff_per_corpus_token = hit * CACHE_READ_FRAC + (1 - hit)
    be = (RAG_TOKENS - hit * SHORT - (1 - hit) * SHORT) / eff_per_corpus_token
    print(f"\nbreak-even corpus size (cached, hit rate {hit}): about {be:,.0f} tokens (below this, full prompt is no costlier per query in token terms)")
```
Output (my run):
```
monthly cost units (ASSUMED prices) | corpus tokens | queries/day | full prompt | full + cache | RAG (tokens only)
      20,000 |        100 |        60.6 |        12.0 |       8.4
      20,000 |     10,000 |     6,060.0 |     1,200.0 |     840.0
      20,000 |  1,000,000 |   606,000.0 |   120,000.0 |  84,000.0
     100,000 |        100 |       300.6 |        57.6 |       8.4
     100,000 |     10,000 |    30,060.0 |     5,760.0 |     840.0
     100,000 |  1,000,000 | 3,006,000.0 |   576,000.0 |  84,000.0
     190,000 |        100 |       570.6 |       108.9 |       8.4
     190,000 |     10,000 |    57,060.0 |    10,890.0 |     840.0
     190,000 |  1,000,000 | 5,706,000.0 | 1,089,000.0 |  84,000.0

break-even corpus size (cached, hit rate 0.9): about 13,684 tokens (below this, full prompt is no costlier per query in token terms)
```
Under these assumptions a cached full prompt costs roughly 7 to 13 times the RAG token bill at 100,000 to 190,000 corpus tokens, but at 100 queries a day all the absolute numbers are tiny, so build effort and simplicity dominate. At a million queries a day the ratio decides. Plug in your provider's real prices, cache rules and your measured hit rate.

**Follow-ups:**
- *Does cache hit rate matter?* A lot: it only helps if the same prefix recurs within the cache lifetime, and any edit to the prefix invalidates it.
- *Middle ground?* Retrieve large chunks or whole documents (document-level RAG) rather than tiny chunks, or use full prompt per department corpus.
- *Quality test?* Run the golden set through both designs and compare accuracy, latency and cost per correct answer.

**Common mistakes:** quoting "200K tokens" as a law; ignoring query volume; assuming cache savings without checking terms; forgetting permissions; assuming long context removes the lost-in-the-middle problem.


### Q37 ⭐⭐ 🟡 Build a failure taxonomy for an advanced RAG pipeline: where does each component help, where can it hurt, and how do you attribute an error to a stage?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** List the stages in order, write down how each one can lose the right evidence or add noise, then attribute errors by oracle experiments: inject the gold evidence at a stage and see whether the answer is fixed.
**Then explain:**

| Stage | Helps with | Can hurt by |
|---|---|---|
| Parse | text, tables, structure | garbled tables, lost headers, OCR errors |
| Chunk | context-sized units | splitting the answer from its context (Q26 helps) |
| Rewrite / HyDE / multi-query | vocabulary mismatch, vague queries | drifting from intent, extra cost (Q7, Q8) |
| Embed / retrieve | recall over the corpus | misses exact terms, ids; gold not in candidates |
| Fuse (hybrid, RRF) | covers both lexical and semantic | a bad weight or one weak list dilutes the other (Q3, Q4) |
| Rerank | precise order of the shortlist | drops gold from the shortlist, adds latency (Q5) |
| Compress | fewer, cleaner tokens | deletes the supporting sentence or changes meaning (Q34) |
| Generate | writes the answer | ignores or misreads context, hallucinates beyond it |

- **Order matters:** an early loss (gold never retrieved) cannot be fixed later, so measure retrieval recall first, then precision after rerank, then generation.
- **Attribution by oracle:** for failed questions with known gold evidence, (1) give the generator the gold chunk directly: if answers are still wrong, the generator or prompt is at fault; (2) inject gold after retrieval, after rerank, after compression to see where it was lost; (3) use the original query instead of the rewritten one to test the rewriter.
- **Caveat:** several stages can fail on one query, so oracle gains depend on order and overlap. Report the share of queries with more than one failing stage and prefer logging each stage's intermediate output (gold present or not).
- **Link to evaluation:** labelled gold evidence per question is the prerequisite; Part 9 covers building that set.

**Example:** Of 100 wrong answers, 40 fail already at "gold in top-50 candidates" (a retrieval problem: embeddings, chunking, query), 25 more lose gold at rerank, 10 lose it in compression, and 25 have gold in context but wrong answers (generation). Fix retrieval first; tuning the prompt would help at most 25 of them.

**Code:** (run; SYNTHETIC: 20,000 simulated queries, 7 stages with ASSUMED independent failure rates, to show the method and its pitfall; not data from a real system)
```python
import numpy as np

# SYNTHETIC oracle-ablation harness. Per-stage failure rates are ASSUMED, chosen only to show the method.
rng = np.random.default_rng(0)
stages = ["parse", "chunk", "rewrite", "retrieve", "rerank", "compress", "generate"]
p_fail = dict(parse=0.03, chunk=0.05, rewrite=0.04, retrieve=0.14, rerank=0.08, compress=0.04, generate=0.07)
N = 20000
fail = {s: rng.random(N) < p_fail[s] for s in stages}   # did stage s break this query (given earlier stages were fine)?

def run(oracle_at=None):
    """Answer is right only if no stage fails. Oracle at stage X = inject the gold evidence right after X,
    which removes failures of X and every stage before it (the generator sees gold)."""
    ok = np.ones(N, bool)
    cut = stages.index(oracle_at) + 1 if oracle_at else 0
    for s in stages[cut:]: ok &= ~fail[s]
    return ok

base = run().mean()
print(f"baseline answer accuracy: {base:.3f}")
print("oracle after stage | accuracy | gain over previous | share of all errors")
prev, total_err = base, 1 - base
rows = {}
for s in stages[:-1]:
    acc = run(s).mean(); rows[s] = acc - prev
    print(f"{s:18} | {acc:.3f}    | {acc - prev:+.3f}             | {(acc - prev) / total_err:5.1%}")
    prev = acc
last = (1 - prev)
print(f"{'generate (rest)':18} | {1.0:.3f}    | {last:+.3f}             | {last / total_err:5.1%}   <- errors left even with gold evidence")

# cross-check against the true first failing stage per query (known only because the data is synthetic)
first = np.full(N, -1)
for i, s in reversed(list(enumerate(stages))): first = np.where(fail[s], i, first)
print("\ntrue first-failure share:", {s: round(float((first == i).sum() / (first >= 0).sum()), 3) for i, s in enumerate(stages)})
nfail = sum(fail[s].astype(int) for s in stages)
print(f"queries with exactly one failing stage: {(nfail==1).mean():.3f} | two or more: {(nfail>=2).mean():.3f}")
print("single-stage oracle (only that stage fixed) accuracy gain:")
for s in stages:
    ok = np.ones(N, bool)
    for t in stages:
        if t != s: ok &= ~fail[t]
    print(f"  fix {s:9}: {ok.mean() - base:+.3f}", end=";")
print()
```
Output (my run):
```
baseline answer accuracy: 0.624
oracle after stage | accuracy | gain over previous | share of all errors
parse              | 0.642    | +0.019             |  4.9%
chunk              | 0.675    | +0.033             |  8.8%
rewrite            | 0.702    | +0.027             |  7.1%
retrieve           | 0.818    | +0.116             | 30.8%
rerank             | 0.892    | +0.075             | 19.8%
compress           | 0.930    | +0.037             |  9.9%
generate (rest)    | 1.000    | +0.070             | 18.7%   <- errors left even with gold evidence

true first-failure share: {'parse': 0.078, 'chunk': 0.128, 'rewrite': 0.096, 'retrieve': 0.335, 'rerank': 0.168, 'compress': 0.074, 'generate': 0.12}
queries with exactly one failing stage: 0.306 | two or more: 0.070
single-stage oracle (only that stage fixed) accuracy gain:
  fix parse    : +0.019;  fix chunk    : +0.032;  fix rewrite  : +0.025;  fix retrieve : +0.102;  fix rerank   : +0.057;  fix compress : +0.026;  fix generate : +0.045;
```
Retrieval is the biggest slice by construction (I set 14% fail rate). The useful lesson is the second half: nested-oracle shares differ from the first-failure shares, because about 7% of queries break in two or more stages, and a query counts as fixed only when all its failing stages are repaired. So the share depends on ordering and on overlap; treat the numbers as guidance on where to look, not an exact split.

**Follow-ups:**
- *Do you need gold chunks for everything?* For a diagnostic sample, yes; label 50-100 failures by hand, since LLM judges are weaker for this.
- *Does a better retriever always fix the answer?* No: if generation is the problem, answers stay wrong with gold context.
- *How do you monitor in production?* Log stage outputs and scores, then sample and label failures by stage (Part 11).

**Common mistakes:** tuning the prompt for retrieval failures; measuring only final-answer accuracy; assuming one cause per failure; adding stages with no ablation showing they help; skipping a "no rewriter" baseline.


### Q38 ⭐⭐ 🟡 What is the latency and cost budget of an advanced RAG pipeline (rewriting, multiple searches, reranking, contextualisation, agent loops), and how do you control it?
**Asked at:** product, GCC, platform teams
**Say this first (1 line):** Every advanced stage adds a call or a pass, so you write a per-stage budget, run the expensive stages only for queries that need them (gating and routing), cache what repeats, and track p95 and not just the average.
**Then explain:**
- **Where the extra work comes from:** rewrite is 1 LLM call; multi-query is N searches (parallel latency, N times the search cost) plus fusion; reranking scores n query-document pairs; an agent loop repeats LLM call plus search k times (reported at 5-10x more LLM calls per query than single-pass, in agentic-RAG explainers); contextualisation (Q26) is an index-time LLM call per chunk, paid once per re-index, not per query.
- **Budget table (ASSUMED milliseconds, for illustration only; measure yours):**

| Stage | Assumed latency | Run when |
|---|---|---|
| Rewrite (LLM) | 400 ms | ambiguous or follow-up queries |
| Search (per query) | 80 ms | always |
| Multi-query (N=4 parallel) | about 80 ms, 4x search cost | recall-critical or hard queries |
| Rerank 50 pairs | 120 ms | always, or when stage-1 scores are ambiguous |
| Generate | 1,500 ms | always |
| Agent loop (each) | 600 ms | multi-hop questions only |

- **Gating and routing:** a cheap classifier or rules decide the path (simple lookup, needs rewrite, multi-hop). Most traffic should take the short path (Q7, Q32).
- **Caching:** cache embeddings of repeated queries, rerank results for hot queries, and the static prompt prefix (reported provider feature, check terms). Semantic caches risk returning answers for slightly different questions.
- **Percentiles:** users feel the slow tail. A pipeline with a retry or loop path has a heavy p95 even if the mean is fine; set timeouts and max hops, and return a degraded answer when a stage times out.

**Example:** Sequential stages add up: rewrite 400 + search 80 + rerank 120 + generate 1,500 = 2,100 ms (assumed). Adding 3 agent loops adds 1,800 ms more. If only 10% of queries need loops, gating keeps the other 90% at about 2 seconds.

**Code:** (run; SIMULATION with ASSUMED latencies, cost units, 60/30/10 query mix, lognormal jitter and fan-out; the output is not a benchmark of any system)
```python
import numpy as np

# SIMULATION with ASSUMED numbers: milliseconds, cost units and the query mix are placeholders, not measurements.
rng = np.random.default_rng(0)
# stage: (mean ms, cost units). Cost unit 1.0 = one generator-sized LLM call (ASSUMED).
ST = dict(rewrite=(400, 0.3), search=(80, 0.02), rerank=(120, 0.1), generate=(1500, 1.0), loop=(600, 0.5))
MQ_N = 4          # ASSUMED: multi-query fan-out, searches run in parallel (latency of one, cost of N)
LOOP_K = 3        # ASSUMED: agent loop iterations for hard queries
MIX = dict(simple=0.6, medium=0.3, hard=0.1)    # ASSUMED query mix

def plan(kind, gated):
    if not gated: kind = "hard"                  # ungated: everything runs the full pipeline
    base = ["search", "rerank", "generate"]
    if kind == "simple": return base
    if kind == "medium": return ["rewrite"] + base
    return ["rewrite", "multi", "rerank", "generate"] + ["loop"] * LOOP_K

def run_query(kind, gated):
    lat = cost = 0.0
    for s in plan(kind, gated):
        if s == "multi": ms, c = ST["search"][0], ST["search"][1] * MQ_N
        else: ms, c = ST[s]
        lat += ms * rng.lognormal(0, 0.35)       # jitter: heavy right tail (ASSUMED sigma)
        cost += c
    return lat, cost

N = 20000
kinds = rng.choice(list(MIX), size=N, p=list(MIX.values()))
for gated in (False, True):
    res = np.array([run_query(k, gated) for k in kinds])
    lat, cost = res[:, 0], res[:, 1]
    print(f"{'gated  ' if gated else 'ungated'}: mean latency {lat.mean():6.0f} ms | p95 {np.percentile(lat, 95):6.0f} ms | mean cost {cost.mean():.2f} units/query")
print("\nper-stage cost of a hard query path:", {s: ST[s] for s in ST})
```
Output (my run):
```
ungated: mean latency   4145 ms | p95   5429 ms | mean cost 2.98 units/query
gated  : mean latency   2166 ms | p95   4138 ms | mean cost 1.39 units/query

per-stage cost of a hard query path: {'rewrite': (400, 0.3), 'search': (80, 0.02), 'rerank': (120, 0.1), 'generate': (1500, 1.0), 'loop': (600, 0.5)}
```
Gating cut the mean latency by about half and the mean cost by more than half in this setup. Note p95 fell much less: the hard queries still take the long path and set the tail. So report p95 per route and decide what the hard path may cost, not only the blended average.

**Follow-ups:**
- *How do you know the gate is not hurting quality?* Compare answer quality per route against the ungated pipeline on the golden set, and watch for hard queries misrouted to the short path.
- *What do you cut first?* The stage with the lowest measured quality gain per millisecond or unit of cost, found by ablation (Q37).
- *Streaming?* Streaming the answer improves perceived latency, but time to first token still includes all the pre-generation stages.

**Common mistakes:** quoting only mean latency; running every technique on every query; sequential calls that could run in parallel; no timeout or hop limit; forgetting that index-time costs recur on re-indexing; copying another team's millisecond numbers.
