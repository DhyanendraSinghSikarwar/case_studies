# Q30 serving-layer review: a FastAPI-STYLE handler (plain asyncio, no framework) with the 8 listed bugs, a fixed version, and tests.
# Everything is a mock: embedding, vector store, LLM. Run: python3 -I q30.py
import asyncio, time, logging, io, hashlib, inspect
API_KEY = "sk-test-FAKE-123456"
CORPUS = [dict(id=f"{t}-{i}", tenant=t, text=f"{t} policy {i} refund", ) for t in ("a", "b") for i in range(6)]
CORPUS += [dict(id=f"b-secret-{i}", tenant="b", text="tenant b confidential refund secret") for i in range(3)]
EMBED_MODEL = "embed-v1"                                    # BUG 2: mutable global
def embed_blocking(text, model):                            # mock embedding call that blocks (CPU / sync HTTP client)
    time.sleep(0.15); return model + ":" + text
def search(query_vec, k, tenant=None):                      # mock store: ranking puts tenant b's secret first for 'refund secret'
    ranked = sorted(CORPUS, key=lambda d: -("secret" in d["text"]))
    if tenant: ranked = [d for d in ranked if d["tenant"] == tenant]
    return ranked[:k]
async def fake_llm_stream(prompt, state):
    state["ctx"] = prompt
    for i in range(50):
        await asyncio.sleep(0.001); state["generated"] += 1; yield f"tok{i} "
async def slow_store(*a, **k): await asyncio.sleep(2.0); return []
# ---------------- BUGGY ----------------
CACHE_BAD = {}
async def handle_buggy(tenant, q, log, state, disconnect=None, store=search):
    log.info("request key=%s q=%s", API_KEY, q)                                   # BUG 7: secret logged
    if q in CACHE_BAD: return CACHE_BAD[q]                                       # BUG 5: key without tenant
    vec = embed_blocking(q, EMBED_MODEL)                                         # BUG 8 (blocks loop) and BUG 2
    hits = [d for d in search(vec, 3) if d["tenant"] == tenant]                  # BUG 1: filter AFTER top-k
    ctx = " ".join(d["text"] for d in hits)                                      # BUG 4: unbounded context
    out = ""
    async for t in fake_llm_stream(ctx, state):                                  # BUG 6: ignores disconnect
        out += t
    cites = [w for w in out.split() if w.startswith("tok")]                      # BUG 3: citations from model text (here: whatever it says)
    CACHE_BAD[q] = dict(answer=out, cites=cites); return CACHE_BAD[q]
# ---------------- FIXED ----------------
CACHE = {}; MAX_CTX_CHARS = 200
async def handle_fixed(tenant, q, log, state, disconnect=None, store=search, model="embed-v1", timeout=0.5):
    log.info("request tenant=%s q_hash=%s", tenant, hashlib.sha256(q.encode()).hexdigest()[:8])
    key = (tenant, model, hashlib.sha256(q.encode()).hexdigest())               # tenant + model in key
    if key in CACHE: return CACHE[key]
    async def work():
        vec = await asyncio.to_thread(embed_blocking, q, model)                  # off the event loop
        call = store(vec, 3, tenant) if inspect.iscoroutinefunction(store) else asyncio.to_thread(store, vec, 3, tenant)
        hits = await asyncio.wait_for(call, timeout)                              # per-dependency timeout
        ctx = ""
        for d in hits:                                                           # budgeted context
            if len(ctx) + len(d["text"]) > MAX_CTX_CHARS: break
            ctx += d["text"] + " "
        out = ""
        async for t in fake_llm_stream(ctx, state):
            if disconnect is not None and disconnect.is_set(): break             # stop paying for tokens
            out += t
        return dict(answer=out, cites=[d["id"] for d in hits if d["text"] in ctx])   # citations from chunk IDs we retrieved
    res = await asyncio.wait_for(work(), timeout=timeout + 2)
    CACHE[key] = res; return res
# ---------------- TESTS ----------------
def mklog():
    buf = io.StringIO(); lg = logging.getLogger("t" + str(id(buf))); lg.setLevel(logging.INFO); lg.addHandler(logging.StreamHandler(buf)); return lg, buf
async def heartbeat(n, ticks):
    for _ in range(n): await asyncio.sleep(0.01); ticks.append(time.perf_counter())
async def main():
    res = {}
    # T1 tenant filter before top-k: tenant a asks a question whose global top-3 belong to tenant b
    for name, h in (("buggy", handle_buggy), ("fixed", handle_fixed)):
        CACHE_BAD.clear(); CACHE.clear(); lg, _ = mklog()
        st = dict(generated=0); await h("a", "refund secret", lg, st); res[("T1 tenant a still gets its own context (ctx %d chars)" % len(st["ctx"].strip()), name)] = len(st["ctx"].strip()) > 0
    # T5 cache key must include tenant: b asks first, a asks the same question
    CACHE_BAD.clear(); CACHE.clear(); lg, _ = mklog()
    await handle_buggy("b", "refund", lg, dict(generated=0)); await handle_buggy("a", "refund", lg, dict(generated=0)); res[("T5 cache keyed by tenant", "buggy")] = len(CACHE_BAD) == 2
    await handle_fixed("b", "refund", lg, dict(generated=0)); await handle_fixed("a", "refund", lg, dict(generated=0)); res[("T5 cache keyed by tenant", "fixed")] = len(CACHE) == 2
    # T7 key not in logs
    for name, h in (("buggy", handle_buggy), ("fixed", handle_fixed)):
        CACHE_BAD.clear(); CACHE.clear(); lg, buf = mklog(); await h("a", "q7", lg, dict(generated=0)); res[("T7 api key not logged", name)] = API_KEY not in buf.getvalue()
    # T6 disconnect stops generation
    for name, h in (("buggy", handle_buggy), ("fixed", handle_fixed)):
        CACHE_BAD.clear(); CACHE.clear(); lg, _ = mklog(); ev = asyncio.Event(); st = dict(generated=0); ev.set()
        await h("a", "q6", lg, st, disconnect=ev); res[("T6 stops generating after disconnect (tokens made: %d)" % st["generated"], name)] = st["generated"] < 5
    # T8 event loop not blocked: heartbeat ticks while embedding runs
    for name, h in (("buggy", handle_buggy), ("fixed", handle_fixed)):
        CACHE_BAD.clear(); CACHE.clear(); lg, _ = mklog(); ticks = []; t0 = time.perf_counter()
        await asyncio.gather(h("a", "q8", lg, dict(generated=0)), heartbeat(10, ticks))
        gap = max(b - a for a, b in zip([t0] + ticks, ticks)); res[("T8 loop stays responsive (max gap %.2fs)" % gap, name)] = gap < 0.1
    # T2 request timeout on slow store: fixed raises TimeoutError quickly, buggy has no timeout parameter use at all
    lg, _ = mklog(); CACHE.clear(); t0 = time.perf_counter()
    try: await handle_fixed("a", "q2", lg, dict(generated=0), store=slow_store, timeout=0.3); ok = False
    except asyncio.TimeoutError: ok = (time.perf_counter() - t0) < 1.0
    res[("T2 slow dependency times out in <1s", "fixed")] = ok
    # T4 context bounded
    CACHE.clear(); big = [dict(id=f"a-{i}", tenant="a", text=str(i) * 150) for i in range(3)]
    async def bigstore(v, k, t): return big
    r = await handle_fixed("a", "q4", lg, dict(generated=0), store=bigstore); res[("T4 context bounded (cites %d of 3)" % len(r["cites"]), "fixed")] = len(r["cites"]) < 3
    # T3 citations come from chunk IDs
    CACHE.clear(); r = await handle_fixed("a", "refund", lg, dict(generated=0)); res[("T3 citations are retrieved chunk ids", "fixed")] = all(c.startswith("a-") for c in r["cites"]) and len(r["cites"]) > 0
    # T2b model name is a parameter, not a mutable global
    res[("T2b model passed per request (cache key includes it)", "fixed")] = "embed-v1" in str(list(CACHE.keys())[0]) if CACHE else True
    CACHE_BAD.clear(); lg, _ = mklog(); r = await handle_buggy("a", "refund", lg, dict(generated=0)); res[("T3 citations are retrieved chunk ids", "buggy")] = all(c.startswith("a-") for c in r["cites"]) and len(r["cites"]) > 0
    for (n, v), ok in res.items(): print(f"{'PASS' if ok else 'FAIL'}  {v:6s} {n}")
asyncio.run(main())
