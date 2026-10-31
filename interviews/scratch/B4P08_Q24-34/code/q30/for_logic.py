# Re-implementation of the `for:` idea: inactive -> pending -> firing; one good sample resets.
def evaluate(values, threshold, for_steps):
    state, pending, log = "inactive", 0, []
    for v in values:
        if v > threshold:
            pending += 1
            state = "firing" if pending >= for_steps else "pending"
        else:
            pending, state = 0, "inactive"
        log.append(state)
    return log

# one sample per 30 minutes, drift score, rule: > 0.3 for 2h  (= 4 consecutive samples)
series = [0.1, 0.35, 0.4, 0.2, 0.31, 0.33, 0.36, 0.34, 0.35, 0.1]
log = evaluate(series, 0.3, 4)
for i, (v, s) in enumerate(zip(series, log)):
    print(f"t={i*30:3d}min value={v:.2f} {s}")
print("first firing at sample:", log.index("firing"), "| a single spike never fires:", "firing" not in evaluate([0.1, 0.9, 0.1, 0.1], 0.3, 4))
