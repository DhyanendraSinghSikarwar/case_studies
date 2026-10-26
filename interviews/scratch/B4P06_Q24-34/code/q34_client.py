import sys, time, httpx
base = sys.argv[1]
with httpx.Client(timeout=10) as c:
    t0 = time.perf_counter(); first = None; n = 0
    with c.stream("POST", base + "/v1/chat/stream", json={"prompt": "hi", "max_tokens": 20}) as r:
        print("status", r.status_code, r.headers["content-type"])
        for line in r.iter_lines():
            if line.startswith("data: ") and line != "data: [DONE]":
                n += 1
                if first is None: first = time.perf_counter() - t0
    total = time.perf_counter() - t0
    print(f"tokens {n}; time to first token {first*1000:.0f} ms; total {total*1000:.0f} ms; tokens/s after first {(n-1)/(total-first):.1f} (this sandbox, fake generator)")
    # client disconnects after 3 tokens
    with c.stream("POST", base + "/v1/chat/stream", json={"prompt": "hi", "max_tokens": 100}) as r:
        k = 0
        for line in r.iter_lines():
            if line.startswith("data: "):
                k += 1
                if k == 3: break
    time.sleep(0.6)
    print("stats after one full stream and one early disconnect:", c.get(base + "/stats").json())
