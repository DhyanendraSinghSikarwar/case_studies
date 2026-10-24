# Standalone, stdlib only. TOY pipeline: word-overlap "retriever", mock "LLM". Shows lineage (chunk id + char offsets) surviving every step.
import re
from collections import defaultdict

DOCS = {"policy_v3": "Refunds are allowed within 30 days of delivery. Damaged items are refunded in full. "
                     "Shipping fees are not refunded. Gift cards cannot be refunded.",
        "faq_v1":    "Delivery takes 3 to 5 days in metros. Refund requests are answered within 2 days. "
                     "Track your parcel in the app."}

def chunk(doc_id, text, size=2):                      # chunk = group of `size` sentences; keep absolute char offsets in the DOCUMENT
    sents = [(m.start(), m.end()) for m in re.finditer(r"[^.]+\.", text)]
    out = []
    for i in range(0, len(sents), size):
        grp = sents[i:i + size]
        out.append({"chunk_id": f"{doc_id}#{i // size}", "doc": doc_id, "start": grp[0][0], "end": grp[-1][1]})
    return out
CHUNKS = {c["chunk_id"]: c for d, t in DOCS.items() for c in chunk(d, t)}
def ctext(c): return DOCS[c["doc"]][c["start"]:c["end"]]
words = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))

def retrieve(q, k=3):                                  # toy lexical retriever; returns (chunk_id, rank) lineage, not just text
    sc = sorted(((len(words(q) & words(ctext(c))), cid) for cid, c in CHUNKS.items()), reverse=True)
    return [cid for s, cid in sc[:k] if s > 0]
def rrf(lists, k=60):                                  # fusion keeps ids; no text is copied or changed here
    s = defaultdict(float)
    for L in lists:
        for r, cid in enumerate(L, 1): s[cid] += 1 / (k + r)
    return sorted(s, key=lambda c: -s[c])
def rerank(q, ids): return sorted(ids, key=lambda c: -len(words(q) & words(ctext(CHUNKS[c]))))
def compress(q, ids):                                  # keep only query-relevant sentences; each keeps ABSOLUTE doc offsets
    keep = []
    for cid in ids:
        c = CHUNKS[cid]
        for m in re.finditer(r"[^.]+\.", ctext(c)):
            a, b = c["start"] + m.start(), c["start"] + m.end()
            if words(q) & words(DOCS[c["doc"]][a:b]):
                keep.append({"sid": f"S{len(keep)+1}", "chunk_id": cid, "doc": c["doc"], "start": a, "end": b,
                             "text": DOCS[c["doc"]][a:b].strip()})
    return keep
def mock_llm(sentences): return [(f"Per policy: {s['text']}", [s["sid"]]) for s in sentences[:2]]   # MOCK: cites sentence ids

def verify(answer_sents, kept):                        # every cited sentence must equal the source span it claims
    by = {s["sid"]: s for s in kept}; problems = []
    for text, cites in answer_sents:
        for sid in cites:
            s = by.get(sid)
            if s is None: problems.append((sid, "unknown sentence id")); continue
            if DOCS[s["doc"]][s["start"]:s["end"]].strip() != s["text"]: problems.append((sid, "span does not match text"))
            elif s["text"] not in text: problems.append((sid, "answer does not contain the cited sentence"))
    return problems

q, q_rewritten = "can damaged items be refunded", "refund policy damaged items"
lists = [retrieve(q), retrieve(q_rewritten)]           # original query kept alongside the rewrite
fused = rrf(lists); ranked = rerank(q, fused); kept = compress(q, ranked[:2]); ans = mock_llm(kept)
lineage = {"query": q, "rewrite": q_rewritten, "retrieved": lists, "fused": fused, "reranked": ranked,
           "kept": [(s["sid"], s["chunk_id"], s["start"], s["end"]) for s in kept]}
print("lineage log:", lineage)
print("answer:", ans)
print("verify (clean):", verify(ans, kept))
assert verify(ans, kept) == []

bad = [dict(s, text=s["text"].replace("in full", "in part")) for s in kept]          # a compressor that paraphrases / edits
ans_bad = mock_llm(bad)
print("verify (edited compressor):", verify(ans_bad, bad))
assert verify(ans_bad, bad) != []
DOCS["policy_v3"] = "NEW. " + DOCS["policy_v3"]                                       # source edited after indexing: offsets drift
print("verify (source changed after indexing):", verify(ans, kept))
assert verify(ans, kept) != []
