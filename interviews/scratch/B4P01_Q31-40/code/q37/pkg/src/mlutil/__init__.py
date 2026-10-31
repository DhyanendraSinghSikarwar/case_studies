def scale(xs):
    lo, hi = min(xs), max(xs)
    return [(x - lo) / (hi - lo) for x in xs]
