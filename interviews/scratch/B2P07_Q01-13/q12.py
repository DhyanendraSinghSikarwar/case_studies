# TOY GraphRAG-style flow on hand-labelled triples (invented, harmless). No LLM: extraction is replaced by the triples,
# community detection is connected components (real GraphRAG uses hierarchical Leiden clustering per its docs),
# and "summaries" are templates standing in for LLM-written community reports.
from collections import defaultdict
triples = [
 ("Lumen Farms", "grows", "oats"), ("Lumen Farms", "sells_to", "Harbor Mills"), ("Harbor Mills", "produces", "porridge"),
 ("Quill Labs", "builds", "SkyMapper"), ("SkyMapper", "uses", "satellite imagery"), ("Quill Labs", "partners_with", "Orbit Co"),
 ("Marsh Council", "funds", "Reed Park"), ("Reed Park", "hosts", "bird census"), ("Marsh Council", "regulates", "wetland drainage"),
]
theme_of = {"Lumen Farms": "food supply chain", "Quill Labs": "geospatial software", "Marsh Council": "local wetlands policy"}
# union-find communities
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
for s, _, o in triples: parent[find(s)] = find(o)
groups = defaultdict(list)
for s, r, o in triples: groups[find(s)].append((s, r, o))
comms = list(groups.values())
def summarize(trs):       # MOCK summary: template, not an LLM
    ents = sorted({e for s, _, o in trs for e in (s, o)})
    anchor = next(e for e in ents if e in theme_of)
    return {"theme": theme_of[anchor], "entities": ents, "text": "; ".join(f"{s} {r.replace('_',' ')} {o}" for s, r, o in trs)}
summaries = [summarize(c) for c in comms]
print("communities found:", len(comms), "->", [s["theme"] for s in summaries])
# GLOBAL question: "What are the main themes in this collection?"
# MAP: one partial answer per community summary (mock: its theme + size). REDUCE: merge partials.
partials = [f"{s['theme']} ({len(s['entities'])} entities)" for s in summaries]
print("map-reduce global answer: the collection covers", "; ".join(partials), "| LLM calls (mock count): map =", len(summaries), "+ reduce = 1")
# LOCAL question: "Who does Lumen Farms sell to?" needs one passage; a plain lookup is enough, no graph needed
print("local lookup:", [f"{s} {r} {o}" for s, r, o in triples if s == "Lumen Farms" and r == "sells_to"])
