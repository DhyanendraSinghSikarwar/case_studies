word = "strawberry"
pieces = ["str", "aw", "berry"]            # HYPOTHETICAL split, not from a real tokenizer
ids = {p: i for i, p in enumerate(pieces)}
print("model input ids:", [ids[p] for p in pieces], "-> no letters visible")
print("true r count:", word.count("r"), "| per-piece r counts:", [p.count("r") for p in pieces])
print("reverse of ids:", [ids[p] for p in pieces][::-1], "vs true reversal:", word[::-1],
      "| reversed pieces then reversed letters:", "".join(p[::-1] for p in pieces[::-1]))
def chunk_ltr(s, n=3): return [s[i:i+n] for i in range(0, len(s), n)]
def chunk_rtl(s, n=3):
    r = len(s) % n; head = [s[:r]] if r else []
    return head + [s[i:i+n] for i in range(r, len(s), n)]
for a, b in [("1234567", "89")]:
    print(a, "ltr:", chunk_ltr(a), "rtl:", chunk_rtl(a))
print("1234567 +", "89 ltr chunks align ones place?", chunk_ltr("1234567")[-1], "(this chunk is the ones, but has", len(chunk_ltr("1234567")[-1]), "digit(s))")
