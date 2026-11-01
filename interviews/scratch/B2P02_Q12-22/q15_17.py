for s in ["hello", "café", "नमस्ते", "日本", "😀"]:
    b = s.encode("utf-8")
    print(repr(s), "chars", len(s), "bytes", len(b), list(b))
    assert b.decode("utf-8") == s
# a lone byte of a multi-byte char is not valid UTF-8
b = "नमस्ते".encode("utf-8")
try: b[:2].decode("utf-8")
except UnicodeDecodeError as e: print("partial:", e.reason)
print(b[:2].decode("utf-8", errors="replace"))
# Q17: bytes per char
en, hi = "Hello how are you", "आप कैसे हैं"
for name, s in [("english", en), ("hindi", hi)]:
    print(name, len(s), "chars", len(s.encode()), "bytes", round(len(s.encode())/len(s),2), "bytes/char")
print({c: len(c.encode()) for c in "aअ ा"})
