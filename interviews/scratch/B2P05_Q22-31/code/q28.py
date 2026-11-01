import numpy as np
rng = np.random.default_rng(4)
# ASSUMED per-rail latencies in ms (not measured on any real system).
rails = {"regex": 1, "small_classifier": 25, "llm_judge": 400}
LLM_MAIN = 1200      # assumed main model latency
block_rate = {"regex": 0.02, "small_classifier": 0.03, "llm_judge": 0.01}  # assumed fraction blocked at each
N = 100000
# closed-form expectations per request
def serial_all():            return sum(rails.values()) + LLM_MAIN
def parallel_all():          return max(rails.values()) + LLM_MAIN
def tiered():
    # cheap first; later rails only run if earlier did not block; blocked requests skip main LLM
    t = 0.0; alive = 1.0
    for name in ["regex", "small_classifier", "llm_judge"]:
        t += alive * rails[name]
        alive *= 1 - block_rate[name]
    return t + alive * LLM_MAIN
print("expected ms per request (assumed numbers):")
print(f"  serial, all rails then LLM : {serial_all():7.1f}")
print(f"  parallel rails then LLM    : {parallel_all():7.1f}")
print(f"  tiered + short-circuit     : {tiered():7.1f}")
# hybrid: run the LLM judge only on 5% of traffic flagged 'uncertain' by the small classifier
p_uncertain = 0.05
hyb = 1 + 25 + p_uncertain*400 + LLM_MAIN
print(f"  tiered, judge on 5% only   : {hyb:7.1f}")
# streaming: check output in 200-char chunks, stop on first flagged chunk
print("streaming: with a 25 ms check per chunk, a flagged chunk at position 3 stops after", 3*25, "ms of checks")
