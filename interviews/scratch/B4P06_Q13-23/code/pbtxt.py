# pbtxt.py: tiny parser for the protobuf TEXT format subset used in Triton config.pbtxt.
# It is NOT Triton's schema check. It only proves the file is well-formed text and lets us assert on fields.
import re
TOK = re.compile(r'\s*(#[^\n]*|"(?:[^"\\]|\\.)*"|[A-Za-z_][A-Za-z_0-9]*|-?\d+\.?\d*|[{}\[\]:,])')
def tokens(s):
    pos, out = 0, []
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m:
            if s[pos:].strip() == "": break
            raise ValueError(f"bad text near: {s[pos:pos+20]!r}")
        pos = m.end()
        if not m.group(1).startswith("#"): out.append(m.group(1))
    return out
def val(t):
    if t.startswith('"'): return t[1:-1]
    if re.fullmatch(r"-?\d+", t): return int(t)
    if re.fullmatch(r"-?\d+\.\d*", t): return float(t)
    return t                                   # enum such as TYPE_FP32 or KIND_CPU
def parse_msg(t, i, closer=None):
    d = {}
    def add(k, v): d.setdefault(k, []).append(v)
    while i < len(t) and t[i] != closer:
        if t[i] == ",": i += 1; continue          # commas between fields are allowed
        k = t[i]; i += 1
        if t[i] == ":": i += 1
        if t[i] == "{":
            v, i = parse_msg(t, i + 1, "}"); i += 1; add(k, v)
        elif t[i] == "[":
            i += 1
            while t[i] != "]":
                if t[i] == ",": i += 1; continue
                if t[i] == "{":
                    v, i = parse_msg(t, i + 1, "}"); i += 1; add(k, v)
                else: add(k, val(t[i])); i += 1
            i += 1
        else: add(k, val(t[i])); i += 1
    return d, i
def parse(s):
    d, i = parse_msg(tokens(s), 0)
    return d
