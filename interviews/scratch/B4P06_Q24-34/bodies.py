def q24(h):
    return f"""**Say this first (1 line):** Cache only when the model is deterministic and a slightly old answer is fine, key the cache on the model version plus a canonical hash of the features, and never let a new model read an old model's answers.

**Then explain:**
- **Safe when:** same input always gives the same output (no sampling, no clock, no random), inputs repeat (popular items, retries, dashboards), and you can live with staleness up to the TTL.
- **Key design:** `sha256(model_version | canonical features)`. Canonical means fixed order, fixed rounding, fixed JSON format. A version bump changes every key, so the old entries simply never match and age out.
- **In-process LRU vs Redis:** in-process is fastest and has no network hop, but every replica has its own copy, so hit rate drops as you add replicas and a restart empties it. Redis is shared and survives restarts, but adds a network call and a new thing to run (not executed here).
- **TTL and negatives:** TTL bounds staleness. Cache only successes. Cache a "no result" only briefly, and never cache a 5xx or a timeout.
- **Stampede:** a hot key expires and 500 requests all compute it at once. Fix with a per-key lock or single-flight, jittered TTLs, or serving the stale value while one request refreshes.
- **Danger:** caching on request features is fine; caching on an ID whose features change behind the scenes (a user's last-hour spend) serves stale scores. Key on the feature values, or put the feature freshness in the TTL.

**Example:** Request `[6.7, 3.0, 5.2, 2.3]` on model `v1`: first call computes (miss), second call returns the stored label (hit). Bump to `v2`: same features, new key, miss again. Also `6.7000001` rounds to `6.7` at 6 decimals, so it hits the same entry. 20 distinct inputs sent 10 times each should give 20 misses and 180 hits, a 90 percent hit rate. You can check that by hand.

**Code:** an in-process LRU (`OrderedDict`) inside a FastAPI app with an ONNX iris model, a pytest file that proves the version bump misses, and a runner that measures hit rate. `make_model.py` (shared by several answers) builds the ONNX file; it is in `code/`. Redis is not run; the swap is `GET key` / `SETEX key ttl value` with the same key function.
{h['code']('make_model.py','q24_cache_app.py','q24_run.py','test_q24.py')}
```bash
python make_model.py /tmp/work            # writes /tmp/work/iris.onnx
python q24_run.py /tmp/work/iris.onnx
IRIS_ONNX=/tmp/work/iris.onnx python -m pytest -q test_q24.py
```

**Output (my run):** real run, Python 3.13, fastapi 0.162, onnxruntime 1.31, TestClient. Redis not executed (no Redis here); the cache logic and key function did run. Timings are this sandbox only, not a benchmark.
{h['out']('q24.txt')}
Reading the timing: the model is tiny and TestClient overhead dominates, so a hit saves almost nothing here. A cache pays when the model call is slow, not when it is a 20-microsecond logistic regression.

**Follow-ups:**
- *How do you stop a stampede?* One lock per key (single-flight), jittered TTLs, or serve stale while one worker refreshes.
- *Why not key on a user id?* The features behind that id change. You would serve a score computed from old data, with no sign it is old.
- *Cache in the model server or the gateway?* Gateway or app cache is simpler and shared across model versions; keep the version in the key either way.

**Common mistakes:**
- Leaving the model version out of the key, so a rollout keeps serving the old model's answers for a TTL.
- Hashing the raw JSON string: `{{"a":1,"b":2}}` and `{{"b":2,"a":1}}` become two keys. Canonicalise first.
- Caching non-deterministic models (sampling, dropout left on) or error responses.
- Unbounded dict as a cache: memory grows until the pod is killed. Always set a size.
"""

def q25(h):
    return f"""**Say this first (1 line):** I scale on requests in flight per replica (or queue depth), not CPU, and I size for start-up time, because a replica that takes 90 seconds to become ready does not help the spike that already happened.

**Then explain:**
- **Signals:** CPU is fine for simple CPU-bound APIs. For batching or GPU services CPU stays low while the queue grows, so it misleads. Better: in-flight requests per replica, queue depth, p95 latency, GPU utilisation or GPU memory (check what your platform can read).
- **Tools at concept level:** HPA scales on CPU, memory or custom metrics; KEDA adds event sources such as queue length; Knative scales on request concurrency and can scale to zero. Details are Part 3. Check current docs for exact behaviour.
- **Maths (Little's law):** in flight = requests per second x seconds per request. Replicas = ceil(in flight / target per replica). Set the target below real capacity to leave headroom.
- **Scale-up lag:** pod scheduling, image pull, model download and load. If that is 90 seconds, the spike is over before the new pods help. Fixes: minimum replicas, smaller images, model baked in or cached on a volume, scale earlier on a leading signal.
- **Scale-down:** use a stabilisation window and drain in-flight requests (terminationGracePeriod, readiness off first). Flapping (up, down, up) wastes start-ups; slow scale-down prevents it.
- **Failure mode:** with no headroom, backlog never drains even after scaling (shown below).

**Example:** 200 req/s at 0.1 s each is 20 in flight. A replica handles 4 at once (capacity), target 3 for headroom: ceil(20/3) = 7 replicas, capacity 7 x 4 / 0.1 = 280 req/s. At target 4 you would get 5 replicas, capacity exactly 200, and the queue built during the lag would never drain.

**Code:** the function and a per-second spike simulation. Traffic is 20 rps for 60 s, then 200 rps. Latency budget 500 ms. A request is late if queue wait plus service time exceeds it. Everything is an input; no cluster.
{h['code']('q25_autoscale.py')}

**Output (my run):** real run with `python -I`. The spike result is a model of the inputs above, not a measurement of any system. Kubernetes, HPA, KEDA and Knative are not executed.
{h['out']('q25.txt')}
Read it: with 90 s start-up and one warm replica, almost every request in the window is late, because the backlog built during the lag drains slowly. With a 10 s start-up it is 11 percent. With 7 warm replicas it is zero, at the price of paying for idle pods.

**Follow-ups:**
- *Why not scale to zero?* Cold start of image plus model hits the first user. Fine for batch or rare internal tools, bad for latency-sensitive APIs.
- *What stops flapping?* Stabilisation window on scale-down, a rate limit on scale-down steps, and a metric that is not noisy.
- *CPU 30 percent but latency high?* Queueing or GPU bound; look at in-flight and queue depth.

**Common mistakes:**
- Autoscaling GPU services on CPU.
- Setting target equal to max capacity, so there is no headroom.
- Ignoring start-up time in the plan.
- Scaling down while requests are in flight, which drops them.
"""

def q26(h):
    return f"""**Say this first (1 line):** A GPU pays off when the model is big and I can batch enough work to keep it busy; for small tree models or low traffic a CPU is cheaper and simpler, and I always verify which provider the session really got.

**Then explain:**
- **GPU wins:** large transformers or CNNs, big batches, heavy matrix maths. **CPU wins:** small tree or linear models, tiny inputs, low or bursty traffic.
- **Idle without batching:** one request at a time uses a sliver of the GPU. Dynamic batching and several model instances per GPU raise utilisation.
- **Memory:** weights plus activations plus batch must fit. Too big a batch or too many instances gives out-of-memory errors, so set a batch cap and test with the largest input.
- **Concept only:** mixed precision (FP16 or BF16) cuts memory and time with a small accuracy check needed; MIG splits a supported GPU into isolated slices, time slicing shares it without memory isolation. Check vendor docs for supported cards.
- **Boundary:** the container image, CUDA version and driver must be compatible (Part 2 owns GPU Docker).
- **Cost per prediction:** hourly price divided by predictions per hour at your real utilisation. An idle GPU is the expensive failure.
- **Silent fallback trap:** ONNX Runtime may fall back to CPU if CUDA is not usable. Print `session.get_providers()` and alert if it is not what you expected.

**Example:** Asking for `["CUDAExecutionProvider", "CPUExecutionProvider"]` on a machine with no GPU should end up on CPU. The helper below filters the wish list by what is available, so the list order is the priority and CPU is always last.

**Code:**
{h['code']('q26_providers.py')}

**Output (my run):** real run on a CPU-only sandbox, onnxruntime 1.31. GPU execution is not executed (no GPU here); only provider selection ran.
{h['out']('q26.txt')}
Notice the last line: asking for CUDA only did not fail, it warned and ran on CPU. In production that is a latency incident waiting to happen, so check `get_providers()` at startup.

**Follow-ups:**
- *How do you know the GPU is worth it?* Measure cost per 1000 predictions at realistic batch and traffic on both. Not done here.
- *Several instances per GPU?* Good when one instance cannot fill the GPU; bad when memory is tight.
- *OOM at runtime?* Cap batch size and input length, restart the instance, and alert.

**Common mistakes:**
- Assuming a GPU is faster for a small model.
- Not checking the active provider.
- Mismatched CUDA, driver and runtime versions.
- Benchmarking with batch 1 and concluding the GPU is useless, or with huge batches and ignoring latency.
"""

def q27(h):
    return f"""**Say this first (1 line):** I read the input in chunks, load the model once, predict in vectorised batches, write each output part to a temp file then rename it, and skip finished parts on restart, so a crash at part 6 costs me parts 6 onward, not the whole night.

**Then explain:**
- **Chunking:** never load 50 million rows into memory. Read fixed-size chunks or partition files.
- **Load once:** one model session per worker, not per chunk or per row.
- **Vectorise:** one `run` call per chunk, not a Python loop over rows.
- **Idempotent output:** write `part-00003.csv.tmp`, then `os.replace` to the final name (atomic on the same filesystem). Output goes in a date partition (`dt=2026-10-26`) so a re-run replaces that day only.
- **Checkpoint:** a part that exists is done. No fancy state file is needed when part names are deterministic. Chunk boundaries must be deterministic too.
- **Parallelism (concept):** multiprocessing per partition file, or Spark/Ray at scale (Part 9 owns Spark). Each worker loads its own model copy.
- **Validate:** output rows equal input rows, ids are unique, no stray `.tmp` files, then publish (flip a pointer or write a `_SUCCESS` marker).
- **Failure modes:** crash between write and rename leaves only a `.tmp`, ignored on resume; a changed chunk size between runs breaks part numbering, so fix it in config.

**Example:** 100,000 rows, chunk 10,000: 10 parts. Crash after 4 parts. Resume scores 60,000 rows and skips 40,000. Run again: skips all 100,000. Output rows must equal 100,000 with 100,000 unique ids.

**Code:** the scorer (input CSV is generated on first run) and the shell steps.
{h['code']('q27_batch.py')}
```bash
python make_model.py /tmp/work
python q27_batch.py /tmp/work/iris.onnx /tmp/work/q27 --crash-after 4   # exits 3
python q27_batch.py /tmp/work/iris.onnx /tmp/work/q27                   # resumes
python q27_batch.py /tmp/work/iris.onnx /tmp/work/q27                   # nothing to do
```

**Output (my run):** real run on 100,000 generated rows with the iris ONNX model. Elapsed times are this sandbox only. Spark and cloud batch services are not executed.
{h['out']('q27.txt')}

**Follow-ups:**
- *Why rename instead of writing the final file directly?* A crash mid-write would leave a half file that looks finished.
- *Join scores to keys how?* Write the id with each score (done here), then join on id downstream.
- *Duplicates if two jobs run at once?* Use a lock or a run id; same part names mean the last rename wins with identical content.

**Common mistakes:**
- Loading the model inside the loop.
- Appending to one big output file, so re-runs duplicate rows.
- Not validating counts before publishing.
- Treating `.tmp` files as output.
"""

def q28(h):
    return f"""**Say this first (1 line):** Streaming inference is at-least-once, so I make the write idempotent by event id, score in micro-batches, watch consumer lag, and send events that keep failing to a dead-letter queue instead of blocking the partition.

**Then explain:**
- **At-least-once:** the broker may redeliver after a crash or rebalance. Duplicates are normal. Dedupe by event id, or make the write an upsert keyed by id.
- **Order and partitions:** order is kept only within a partition. Key by entity id (user, device) if scores depend on order.
- **Micro-batching:** poll up to N events or wait T ms, then one model call. Better throughput than one by one, bounded added latency.
- **Backpressure and lag:** if the consumer is slower than the producer, lag grows. Lag (messages or seconds behind) is the key signal; scale consumers up to the partition count.
- **Poison events:** a bad payload throws on every retry. Retry a limited number of times, then dead-letter it with the error, and carry on.
- **Simpler alternative:** if the caller waits for the answer, a request-response API is simpler than a queue.
- **Failure mode:** marking an id as seen before the result is written loses the event if the write fails. In real code, record "seen" in the same transaction as the output (the simulation keeps it in memory, so it ignores this).

**Example:** 40 events, one poison (id 10), and 5 redeliveries (ids 3, 3, 17, 25, 25). Queue has 45 messages. Expected: 39 scored, 5 duplicates skipped, 1 dead-lettered, 39 + 1 = 40 unique ids.

**Code:**
{h['code']('q28_stream_sim.py')}

**Output (my run):** real run with `python -I`. Kafka is not executed (no broker here); the logic (dedupe, micro-batch, dead letter) ran in memory.
{h['out']('q28.txt')}

**Follow-ups:**
- *Exactly-once?* Mostly means at-least-once plus idempotent writes; check your platform's transaction support.
- *What do you alert on?* Consumer lag trend, dead-letter rate, and scoring error rate.
- *Why retry one by one after a batch fails?* To isolate the poison event so the other seven still get scored.

**Common mistakes:**
- Dead-lettering a whole batch for one bad event.
- Unbounded retries that block the partition.
- Dedupe set in memory only, lost on restart (use the output store as the source of truth).
- Ignoring lag until users complain.
"""

def q29(h):
    return f"""**Say this first (1 line):** I quantise with ONNX Runtime dynamic int8 to cut size and often CPU time, then I decide by accuracy on a held-out set and by latency at my real batch size, not by a few sample rows.

**Then explain:**
- **Graph optimisation:** ONNX Runtime has optimisation levels (basic, extended, all) that fold constants and fuse operators; they are on by default at a high level, and you can save the optimised model. Check current docs for names.
- **Dynamic int8:** weights are stored as int8, activations are quantised on the fly. Good for matmul-heavy models (MLPs, transformers on CPU). Little help for tiny linear or tree models.
- **Other levers:** smaller or distilled model (concept: a small student learns from a big teacher), batching, thread settings (intra-op threads match the cores you were given).
- **Check the trade-off:** accuracy on a validation set (thousands of rows), how many predictions flip versus fp32, file size, latency at batch 1 and at the real batch, and memory.
- **Failure modes:** accuracy drop on rare classes hidden by overall accuracy; speed-up that disappears at batch 1; quantiser errors on unsupported operators (the tool then raises, so read the message).

**Example:** A 64-feature, two hidden layer (256, 256) MLP, 3 classes, 6,000 synthetic rows. Compare fp32 and int8 on 1,800 held-out rows: size, accuracy, flipped labels, latency.

**Code:**
{h['code']('q29_quantize.py')}
```bash
python q29_quantize.py /tmp/work/q29
```

**Output (my run):** real run, onnxruntime 1.31 CPU, a quantiser warning about pre-processing was printed and is harmless here. The quantiser did not reject the model. Latency is machine-specific, not a benchmark. GPU and TensorRT are not executed.
{h['out']('q29.txt')}
Read it: the file is about a quarter of the size; accuracy moved from 0.9444 to 0.9439 (10 of 1800 labels flipped); at batch 1 there is no speed-up (the call overhead dominates), at batch 256 it was about twice as fast on this machine. Your model and CPU will differ.

**Follow-ups:**
- *Dynamic vs static quantisation?* Static uses a calibration set to fix activation scales ahead of time; usually faster, more work.
- *Why not trust 5 sample rows?* Rare flips would not show.
- *When not to quantise?* When accuracy is tight, or the model is already tiny.

**Common mistakes:**
- Judging by file size only.
- Measuring latency at batch 1 and claiming a general speed-up.
- Skipping the accuracy check per class or slice.
- Forgetting to re-run the golden and parity tests (Q33) on the quantised artifact.
"""

def q30(h):
    return f"""**Say this first (1 line):** For a 40-second model I do not hold the connection: POST returns 202 with a job id, a worker does the job from a queue, and the client polls GET /jobs/id or gets a callback.

**Then explain:**
- **Why not wait:** proxies, gateways and browsers time out (often 30 to 60 seconds, check yours), and a held connection pins a worker and breaks on any retry.
- **Flow:** `POST /jobs` returns 202, a `Location` header and a job id; `GET /jobs/{{id}}` returns `queued`, `running`, `done` or `failed` with the result or error.
- **Queue plus workers:** in production Celery, RQ or a cloud queue with Redis or a broker; here an in-process queue and a thread stand in. A real queue survives an API restart; this does not.
- **Idempotency key:** the client sends `Idempotency-Key`; a retried POST returns the same job instead of running the model twice.
- **Result expiry:** keep results for a TTL, then return 404 or 410. Store big results in object storage and return a link.
- **Timeouts at each hop:** client, gateway, API, queue visibility timeout and worker timeout, with the inner ones shorter than the outer.
- **Alternatives:** webhook or a message when done, to avoid polling.

**Example:** `POST /jobs {{"n": 7}}` returns 202 `{{"job_id": "...", "state": "queued"}}`. Polling shows `queued` or `running`, then `{{"state": "done", "result": 49}}`. The same POST with the same `Idempotency-Key` returns the same job id.

**Code:** app and tests (TestClient).
{h['code']('q30_async_jobs.py','test_q30.py')}

**Output (my run):** real pytest run with TestClient. Celery and Redis are not executed.
{h['out']('q30.txt')}

**Follow-ups:**
- *Poll or push?* Polling is simple and works through any proxy; webhooks cut load but need a reachable receiver and retries.
- *Worker dies mid-job?* A real queue redelivers after a visibility timeout, so jobs must be idempotent.
- *Why 202 not 200?* The work is accepted, not finished.

**Common mistakes:**
- In-memory job state with multiple API replicas (replica A cannot see replica B's jobs): use a shared store.
- No expiry, so results pile up.
- Retrying POST without an idempotency key, running the model twice.
- Polling in a tight loop with no backoff.
"""

def q31(h):
    return f"""**Say this first (1 line):** I put a hard cap on requests in flight per replica and answer 503 with Retry-After when it is full, because failing fast early is better than a queue that grows until everything times out.

**Then explain:**
- **Timeouts:** the client's timeout is shorter than the server's, so the client gives up first and the server does not keep working for nobody. Set a timeout at every hop.
- **Retries:** only for idempotent calls (a prediction is, a "charge the card" is not). Exponential backoff with jitter, a retry budget, and honour Retry-After.
- **Retry storm:** when a service slows, every client retries, load multiplies, the service dies. Backoff, jitter and a retry budget stop it.
- **Load shedding:** limit concurrency (here N in flight). Over the limit return 503 (or 429 for per-client limits) at once.
- **Circuit breaker:** after many failures, stop calling for a while, then probe. **Bulkhead:** separate pools per dependency or route so one slow part cannot eat all capacity.
- **Degraded modes:** a cheaper model, cached answer or default score, labelled as such.
- **Failure mode:** shedding on liveness probes or counting shed requests as healthy latency hides the problem; export the shed count (Q32).

**Example:** limit 4, a 0.3 s handler, 10 simultaneous requests: 4 are served, 6 are rejected with 503 and `Retry-After: 1`, peak in flight is 4. After the burst, a new request gets 200.

**Code:** middleware, plus a full-jitter backoff helper, plus tests.
{h['code']('q31_limiter.py','test_q31.py')}

**Output (my run):** real pytest run with httpx and an in-process ASGI transport. Printed lines are from `-s`.
{h['out']('q31.txt')}

**Follow-ups:**
- *503 or 429?* 429 says "you sent too many"; 503 says "I am overloaded". Per-client limits use 429.
- *Why not a bigger queue?* A long queue only converts overload into latency, then timeouts.
- *Where do you set the limit?* From measured capacity per replica (load test), a bit below the knee.

**Common mistakes:**
- Retrying without jitter (all clients retry together).
- Retrying non-idempotent calls.
- Limit counted per process while running several workers (each has its own count).
- Client timeout longer than the server's.
"""

def q32(h):
    return f"""**Say this first (1 line):** Inside the serving layer I want structured logs with a request id and model version, request, error and latency metrics on /metrics, and alerts on error rate, p99 and saturation; drift and data quality belong to Part 8.

**Then explain:**
- **Logs:** one JSON line per request: request id, route, status, model version, duration. Pass the id back in a header and forward it to downstream calls (trace id).
- **Metrics:** a counter for requests by route and status, a histogram for latency, a gauge for in-flight. Histograms let Prometheus compute p99 across replicas; averages hide tails.
- **Labels:** keep values bounded (route template, not the raw URL with ids). Unbounded labels blow up memory in Prometheus.
- **Alert on:** error rate, p99 versus the budget, saturation (in-flight at the limit, shed count), and readiness flapping. Alert on symptoms users feel.
- **Logging inputs and predictions for later drift analysis:** sample (for example 1 percent), hash or drop identifiers, never log PII, keep a retention limit. Store features and predictions with the model version.
- **Failure mode:** a metric registered twice (two app instances in tests) raises an error; use your own registry per app or create once.

**Example:** Two POST /predict and one unknown URL: the counter shows `/predict` 200 = 2 and `unmatched` 404 = 1; the histogram count for `/predict` is 2; the log line for the first request has the id `abc123` we sent.

**Code:**
{h['code']('q32_metrics_app.py','q32_run.py')}

**Output (my run):** real run with prometheus_client 0.26 and TestClient. Log lines and /metrics text are the actual output (trimmed to the key lines). Prometheus and Grafana servers are not executed. The in-flight gauge reads 1 because the /metrics request itself was in flight.
{h['out']('q32.txt')}

**Follow-ups:**
- *Histogram buckets?* Pick them around your latency budget; check current prometheus_client defaults.
- *Multiple uvicorn workers?* Each process has its own metrics; use prometheus_client's multiprocess mode or scrape per pod (check docs).
- *Health endpoints in metrics?* Count them separately or exclude them, so probes do not hide real error rates.

**Common mistakes:**
- Raw path as a label (`/items/123`).
- Averages instead of percentiles.
- Logging full request bodies with personal data.
- No model version in logs, so you cannot tell which model made a bad call.
"""

def q33(h):
    return f"""**Say this first (1 line):** I test the API in layers: schema contract, golden predictions, parity with the training pipeline, a startup test, and a batch-equals-singles property, all in pytest with TestClient so CI runs them in seconds.

**Then explain:**
- **TestClient:** use `with TestClient(app)` so the lifespan runs and the model loads; without `with` the model is not loaded (shown: /readyz gives 503).
- **Contract test:** response keys and types, and 422 for bad input. This catches an accidental rename.
- **Golden file:** fixed inputs with expected outputs and a tolerance (`atol`). Generate it once from a reviewed artifact, commit it, and a model change that moves outputs fails the test and forces a human look. Do not regenerate it blindly.
- **Parity:** the served artifact (ONNX) must match the original (sklearn) on labels and, within tolerance, on probabilities. This catches export bugs and dtype mistakes (float64 vs float32).
- **Property:** a batch of N rows gives the same labels as N single calls.
- **Smoke load test:** a few hundred requests in CI checking no errors and a loose latency ceiling (CI wiring is Part 7; not run here).
- **Failure modes:** exact float equality (flaky), goldens regenerated on every change (test proves nothing), testing only the happy path.

**Example:** Iris, three golden rows (setosa, versicolor, virginica), parity on all 150 rows, and 15 rows sent as one batch and as 15 single calls.

**Code:** the app under test, the pytest suite, and the golden file (made once from the reviewed artifact, then committed). A mutation check (editing one golden number) should make the golden test fail, and it did.
{h['code']('iris_app.py','test_q33.py')}
```bash
python make_model.py /tmp/work
IRIS_ONNX=/tmp/work/iris.onnx python -m pytest -v test_q33.py
```
```json
{h['golden']}
```

**Output (my run):** real run, pytest 9.1, fastapi 0.162. The second part is the mutation check (one golden probability changed to 0.5, then restored).
{h['out']('q33.txt')}

**Follow-ups:**
- *Why tolerance?* Different libraries and CPUs give tiny float differences.
- *When do you update the golden file?* On an intended model change, in the same pull request, with a reviewer comparing old and new.
- *Where does the load test run?* A small smoke in CI, the real one on a staging environment (locust or k6 not executed here).

**Common mistakes:**
- Forgetting `with TestClient(...)`, so the lifespan never runs.
- Comparing floats with `==`.
- Golden file made from the model it tests, never reviewed.
- Testing the Python model but not the exported artifact that really ships.
"""

def q34(h):
    return f"""**Say this first (1 line):** For LLMs the serving layer streams tokens over Server-Sent Events, I measure time to first token and tokens per second separately, and I cancel generation when the client disconnects, while the engine does the continuous batching.

**Then explain:**
- **Streaming (SSE):** the response is `text/event-stream`, each chunk is `data: ...` and a blank line, ending with a `[DONE]` marker. Turn off proxy buffering, or users see nothing until the end.
- **Metrics:** time to first token (TTFT) is prefill plus queueing, which users feel as "did it start". Tokens per second is decode speed, which sets how fast it reads. Track both, plus total time.
- **Cancellation:** if the client closes the tab, stop generating. Otherwise you pay for tokens nobody reads. Check `request.is_disconnected()` or handle `CancelledError`.
- **Timeouts:** a total request timeout and an idle timeout between chunks, at gateway and server.
- **OpenAI-compatible interface:** many servers and clients speak `/v1/chat/completions`, so clients can swap backends. Check current docs for the exact fields.
- **Gateway in front:** auth, rate limits, quotas, routing between models, logging, retries. Streaming must pass through it unbuffered.
- **Continuous batching:** requests finish at different lengths, so fixed-size batches waste slots waiting for the longest one. The engine adds and removes sequences every step. Internals belong to Book 2.

**Example:** 20 tokens, a fake 0.30 s prefill and 0.05 s per token: first token near 0.3 s, total near 1.3 s, about 20 tokens per second after the first. Disconnect after 3 tokens: the server should record a cancel.

**Code:** a FastAPI endpoint with a fake generator, and an httpx client. Run with `python -m uvicorn q34_stream_app:app --port 8341`, then the client.
{h['code']('q34_stream_app.py','q34_client.py')}

**Output (my run):** real local uvicorn server on port 8341, stopped afterwards. No real LLM or GPU server is executed; the generator is fake. Timings are this sandbox only.
{h['out']('q34.txt')}

**Follow-ups:**
- *SSE or WebSocket?* SSE is simpler for one-way token streams and works over normal HTTP; WebSocket for two-way.
- *What breaks streaming?* Proxy or CDN buffering and gzip on the stream.
- *Rate limit by what?* Tokens, not just requests; one request can be 10 or 10,000 tokens.

**Common mistakes:**
- Measuring only total latency.
- Not cancelling on disconnect.
- Buffering proxies.
- Setting a total timeout shorter than a long answer needs.
"""

BODIES = {24: q24, 25: q25, 26: q26, 27: q27, 28: q28, 29: q29, 30: q30, 31: q31, 32: q32, 33: q33, 34: q34}
