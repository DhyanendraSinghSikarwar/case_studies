SETTINGS = {  # starting points to tune on an eval set, not universal values
    "code_completion": dict(temperature=0.0, top_p=1.0, max_tokens=64,  stop=["\n\n", "\ndef ", "\nclass "]),
    "support_chat":    dict(temperature=0.4, top_p=0.9, max_tokens=400, stop=["\nUser:"]),
    "creative":        dict(temperature=1.0, top_p=0.95, max_tokens=1200, stop=[]),   # or min_p ~0.05 instead of top_p
    "extraction":      dict(temperature=0.0, top_p=1.0, max_tokens=300, stop=[]),     # + schema-constrained output (Part 3)
}
for name, s in SETTINGS.items():
    assert 0 <= s["temperature"] <= 2 and 0 < s["top_p"] <= 1 and s["max_tokens"] > 0
    print(f"{name:16s} {s}")
