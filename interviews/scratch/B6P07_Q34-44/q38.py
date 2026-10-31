import re

# Illustrative numbers from the prompt (time to first token ignored)
TOK, TPS, CHECK, CHUNK = 400, 40, 0.1, 50

buffered = TOK / TPS + CHECK
chunked_first = CHUNK / TPS + CHECK
print(f"buffered: first text at {buffered:.2f} s; chunked: first text at {chunked_first:.2f} s")
assert buffered == 10.1 and chunked_first == 1.35 and round(buffered - chunked_first, 2) == 8.75

# Chunked, checks run alongside generation: when does each chunk become visible, and when does the last one?
n_chunks = TOK // CHUNK
visible = [(k * CHUNK) / TPS + CHECK for k in range(1, n_chunks + 1)]
print("chunks:", n_chunks, "| visible at (s):", [round(v, 2) for v in visible])
assert n_chunks == 8 and visible[0] == 1.35 and round(visible[-1], 2) == 10.1   # same finish time as buffered

# If checks were serial and paused generation instead: 8 x 0.1 s added
serial_total = TOK / TPS + n_chunks * CHECK
print("if each check paused generation, last text at", serial_total, "s")
assert round(serial_total, 2) == 10.8

# The risk with chunking: a fake 10-digit number split across a chunk boundary (invented data)
pii = re.compile(r"\b\d{5} ?\d{5}\b")
chunk1 = "Please call me on 98765"
chunk2 = " 43210 tomorrow morning."
per_chunk_hits = [bool(pii.search(c)) for c in (chunk1, chunk2)]
rolling_hit = bool(pii.search(chunk1 + chunk2))
print("per-chunk check finds it:", any(per_chunk_hits), "| check with held-back overlap finds it:", rolling_hit)
assert not any(per_chunk_hits) and rolling_hit

# Cost of the fix: check a rolling window (previous tail + new chunk) and show everything except the last H tokens
H = 10
first_release_tokens = CHUNK - H
tail_lag = CHUNK / TPS   # the held-back tail waits for the next chunk to arrive and be checked
print(f"first text at {chunked_first:.2f} s still, showing {first_release_tokens} tokens; the held tail lags by {tail_lag:.2f} s")
assert first_release_tokens == 40 and tail_lag == 1.25
assert TOK // 10 == 40   # checks needed with 10-token chunks (follow-up)
