import math
bikes, rec_bytes, every_s, cap = 500, 200, 5, 2_000_000
readings = 24 * 3600 // every_s
raw = readings * rec_bytes
factor = raw / cap
print("readings/day", readings, "raw bytes/bike/day", raw, "reduction factor", round(factor, 3))
assert readings == 17_280 and raw == 3_456_000 and round(factor, 3) == 1.728
print("fleet raw GB/day", bikes * raw / 1e9)
assert bikes * raw == 1_728_000_000
# options to fit the cap (each must be >= 1.728x); sums are illustrative
send_every = math.ceil(every_s * factor)          # slower fixed rate
print("fixed-rate option: one reading every", send_every, "s ->", 86400 // send_every * rec_bytes, "bytes/day")
assert send_every == 9 and 86400 // 9 * 200 <= cap
# on-bike summary: 1 summary of 400 bytes per minute + event uploads
summary = 24 * 60 * 400
print("1-minute 400-byte summaries", summary, "bytes/day, factor", round(raw / summary, 2))
assert summary == 576_000 and round(raw / summary, 2) == 6.0
spare = cap - summary
print("spare for event windows (bytes/day)", spare, "= windows of 60 readings (12,000 B):", spare // 12_000)
assert spare // 12_000 == 118
