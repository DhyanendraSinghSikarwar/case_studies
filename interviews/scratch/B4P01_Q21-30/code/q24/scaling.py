def scale(x, lo, hi, clip=False):
    out = (x - lo) / hi              # BUG: should divide by (hi - lo)
    if clip:
        out = min(max(out, 0.0), 1.0)
    return out
