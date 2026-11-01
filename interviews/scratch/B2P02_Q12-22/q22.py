def stream_with_stop(chunks, stops):
    """Yield safe text; hold back the longest suffix that could still start a stop sequence."""
    buf, out = "", []
    hold = max(map(len, stops)) - 1
    for ch in chunks:
        buf += ch
        hits = [buf.find(s) for s in stops if s in buf]
        if hits:
            out.append(buf[:min(hits)]); return "".join(out), "stop"
        # keep a tail that is a prefix of some stop
        k = 0
        for n in range(min(hold, len(buf)), 0, -1):
            if any(s.startswith(buf[-n:]) for s in stops): k = n; break
        out.append(buf[:len(buf)-k]); buf = buf[len(buf)-k:]
    out.append(buf); return "".join(out), "eos"
chunks = ["Answer: 42\n", "\nUs", "er: next", " question"]
print(stream_with_stop(chunks, ["\nUser:"]))
print(stream_with_stop(["Hi\nUs","ing it"], ["\nUser:"]))
def generate(tokens, max_tokens, eos="<eos>"):
    out=[]
    for t in tokens:
        if t==eos: return out,"stop"
        out.append(t)
        if len(out)>=max_tokens: return out,"length"
    return out,"length"
print(generate(["a","b","<eos>","c"], 10)); print(generate(["a","b","c","d"], 3))
