# Book 4 Part 6 review (Wave C)

Date: 2026-10-26. Reviewer: lead session (independent of the four answer agents). Scope: 45 questions, Q1-Q45 (model serving: FastAPI, batch vs real-time, ONNX, Triton, BentoML, rollout, load, security). Band per plan.md: Rs 30-80 LPA; no salary figures.

## Process
Four agents answered Q1-12, Q13-23, Q24-34, Q35-45; merged by heading: 45 of 45 merged, 0 skipped, 0 pending. Wave A was interrupted once by a spend limit and resumed with SendMessage after the reset; no Wave B stops. Each agent used its own port range (81xx to 84xx) and temp dirs; no servers were left running.

## Structure checks (scripted by the lead)
| Check | Result |
|---|---|
| ANSWER_PENDING | 0 |
| Numbering continuous Q1-Q45; star order and counts 17 / 18 / 10 | pass |
| All 7 template labels present and in order (a few Example labels carry a suffix such as "Example (hand check)"); code fences balanced | pass for all 45 |

The lead did not re-run the servers and load demos: they need the shared venv, ports and per-question temp dirs; pasted outputs come from each agent's real runs (code and raw outputs in each agent's `code/` folder). All latency and throughput figures are this-sandbox-only demos (client and server on one machine) and differ on a re-run.

## What really ran (fastapi 0.162, uvicorn 0.54, onnx 1.23, onnxruntime 1.31 CPU, skl2onnx 1.20, bentoml 1.4.40, tritonclient 2.73, prometheus_client, torch 2.14 CPU path, Python 3.13)
FastAPI TestClient and real uvicorn with ONNX models loaded in lifespan; probes (live/ready) with blocking vs background load; skl2onnx export with parity on all 150 iris rows; TorchScript and torch.onnx exports with eight failure cases; dynamic quantisation; ONNX Runtime threads, optimisation levels, provider fallback; dynamic batching in a service; canary, shadow and gateway servers with sticky hashing; graceful SIGTERM; auth, size and rate limits (8 tests); closed vs open loop load generator; `bentoml serve` and `bentoml build`; tritonclient against a FastAPI mock of the v2 routes; a Triton-style repository and config.pbtxt checked by a hand-written parser; protobuf compile with protoc; pickle and skops/weights_only safety demos; caching, resumable batch scoring, queue simulation, async job pattern, metrics middleware.

## Findings kept in the text (observed)
- Loading a model blocking inside `lifespan` means uvicorn does not open the port: probes get connection refused, not 503; a background load gives a live /livez and a 503 /readyz.
- Exporting a model without its scaler agreed with the training pipeline on only 52% of rows; whole-pipeline export 100%.
- Asking ONNX Runtime for CUDA only does not fail without a GPU: it warns and runs on CPU (check `get_providers()`).
- Batched model call 9.6x faster; end to end over HTTP only about 10-20% gain, and a longer wait made p50 worse; runs noisy, cause not profiled.
- Quantisation: 326 KB to 87 KB, 10 of 1800 labels flipped; speed-up only at large batch.
- Open-loop load generation shows a tail (p99 278 ms) that closed-loop hid (6.9 ms).
- Torch weights_only blocked a pickled checkpoint; skops refused an untrusted type.
- The server collapsed at concurrency 64 in the load demo; throughput peaked near concurrency 4.

## Not executed
Triton server, perf_analyzer, GPU/CUDA/TensorRT/OpenVINO providers, Docker and containerize, Kubernetes, KServe, Seldon, TorchServe, Istio/mesh canary, Redis, Kafka, Celery, Prometheus/Grafana servers, locust, k6, real LLM servers, cloud endpoints, BentoCloud, pen tests, WAF, mTLS, JWT. Cost and decision questions use invented inputs (no real prices).

## Hedged
Triton config.pbtxt details (my parser is not Triton's schema check), TorchServe maintenance status, Seldon licence, registry names and sunset dates (made-up examples), ONNX exporter versions, `dims: [1]` with reshape ("check current docs"). Weak numbers from two REST-vs-gRPC pages were flagged in the sources note and not used.

## Evidence limits
No candidate-reported questions found; every WebFetch failed, so sources are snippet-only guides and job postings (Triton, BentoML and Seldon each appeared in one posting, KServe in none). See research_notes/Book4_Part06_sources.md.

## Housekeeping
Agents added skops, safetensors, onnxscript and grpcio-tools to the shared venv (outside the repo). One agent left a `_build/` folder inside its scratch folder (working files only).
