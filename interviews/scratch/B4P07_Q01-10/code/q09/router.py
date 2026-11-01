from fnmatch import fnmatch

# path pattern -> pipelines it triggers (first column of the table in the answer)
RULES = [
    ("docs/*",              set()),                                 # docs only: nothing
    ("*.md",                set()),
    ("src/serving/*",       {"code_ci", "serving_rebuild"}),        # API code: test + rebuild image
    ("Dockerfile",          {"code_ci", "serving_rebuild"}),
    ("requirements*.txt",   {"code_ci", "serving_rebuild", "model_ct"}),  # deps change both
    ("src/training/*",      {"code_ci", "model_ct"}),               # training code: retrain
    ("configs/train*.yaml", {"code_ci", "model_ct"}),
    ("data/*.dvc",          {"model_ct"}),                          # new data pointer: retrain, no code CI
    ("deploy/alias.yaml",   {"promote_pointer"}),                   # pointer move: no build at all
    ("src/*",               {"code_ci"}),
    ("tests/*",             {"code_ci"}),
]

def route(changed_paths):
    out = set()
    for p in changed_paths:
        for pattern, pipes in RULES:
            if fnmatch(p, pattern):
                out |= pipes
                break
        else:
            out.add("code_ci")          # unknown path: fail safe, run the cheap CI
    return sorted(out)

if __name__ == "__main__":
    import sys
    print(route(sys.argv[1:]))
