# HyDE with a MOCK generator (canned text, no LLM) and a TOY hashed bag-of-words embedder (not a real encoder).
import re, zlib
import numpy as np
def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
STOP = {"the", "a", "an", "of", "to", "is", "my", "and", "in", "when", "why", "does", "get", "it", "on", "or", "that", "can"}
def emb(text, d=128):
    v = np.zeros(d)
    for w in toks(text):
        if w not in STOP: v[zlib.crc32(w.encode()) % d] += 1
    n = np.linalg.norm(v); return v / n if n else v
corpus = {
 "thermal": "Thermal throttling reduces CPU clock speed when die temperature exceeds the safe limit; clean fans and replace thermal paste",
 "battery": "Battery wear lowers capacity after many charge cycles; calibrate the battery and check cycle count",
 "driver":  "A faulty graphics driver can cause crashes; reinstall the driver from the vendor",
 "wifi":    "Wifi disconnects often come from channel congestion; change the router channel",
 "storage": "Low disk space slows the system; delete temporary files and move media to external storage",
}
ids = list(corpus); E = np.stack([emb(corpus[i]) for i in ids])
def search(vec): return [ids[j] for j in np.argsort(-(E @ vec))]
# MOCK generator: canned hypothetical answers. Note the deliberate FALSE detail (a made-up 95 C limit)
# and the one case where the "LLM" lacks domain knowledge and writes an off-topic passage.
HYP = {
 "why is my laptop so hot": "Laptops get hot because of thermal throttling when the CPU temperature exceeds 95 C; dust in the fans and old thermal paste make it worse.",
 "laptop dies fast": "Laptops with a heavy graphics driver load crash when the router channel is congested.",   # unknowledgeable/drifting mock
}
tests = [("why is my laptop so hot", "thermal"), ("laptop dies fast", "battery")]
for q, gold in tests:
    plain = search(emb(q)); hyde = search(emb(HYP[q]))
    print(f"{q!r:28} gold={gold:8} plain top1={plain[0]:8} HyDE top1={hyde[0]:8} | hypothetical text contains a false detail: {'95 C' in HYP[q]}")
# The retrieved item is always a REAL corpus passage; the hypothetical text is never shown to the answerer as evidence.
print("returned passage for query 1:", corpus[search(emb(HYP[tests[0][0]]))[0]][:60], "...")
