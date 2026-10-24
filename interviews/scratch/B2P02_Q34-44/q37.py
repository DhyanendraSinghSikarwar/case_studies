texts = {"English": "The weather is nice today", "Hindi": "आज मौसम अच्छा है", "number": "1234567"}
for k, t in texts.items():
    print(f"{k:8s} chars={len(t):3d} utf8 bytes={len(t.encode('utf-8')):3d}")
# attention cost grows ~ L^2: bytes/char ratio r -> r^2 more attention pairs vs same text at char level
hi = "आज मौसम अच्छा है"
r = len(hi.encode()) / len(hi)
print("Hindi bytes per char %.2f; attention pairs x%.1f vs char-level" % (r, r**2))
# 4x longer sequences (typical bytes-per-subword-token is ~4 for English, assumed): attention x16, per-token MLP cost x4
print("if bytes are 4x more positions than subword tokens: attention pairs x", 4**2, ", linear cost x", 4)
