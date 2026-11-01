"""Q39: build a tiny 'repo' with four planted debts and find them with ~40 lines of ast/regex.
Not a real tool: it shows that each smell is mechanically visible, so you can count it and track it."""
import ast, re, tempfile, textwrap
from pathlib import Path

FILES = {
 "features.py": '''
    USE_OLD_FEATURES = False          # flag nobody has flipped since 2023
    def build(df):
        if USE_OLD_FEATURES:
            return old_build(df)      # dead experimental path
        return new_build(df)
    def old_build(df): return df
    def new_build(df): return df
 ''',
 "glue.py": '''
    import numpy as np, pandas as pd
    def to_api(df):                   # glue: only converts shapes between two packages
        arr = np.asarray(df); df2 = pd.DataFrame(arr); return df2.to_numpy().tolist()
 ''',
 "train.py": '''
    import json
    cfg = json.load(open("config.json"))
    def run():
        return cfg["lr"], cfg["depth"]         # reads only lr and depth
 ''',
 "config.json": '{"lr": 0.1, "depth": 4, "dropout": 0.3, "legacy_mode": true, "tmp_fix_2022": 1}',
 "job_a.py": "from features import build\nbuild(None)\n",
 "step1_clean.py": "pass\n", "step2_clean_v2.py": "pass\n", "step3_clean_final.py": "pass\n",
 "step4_clean_final2.py": "pass\n", "step5_join_tmp.py": "pass\n",
}
root = Path(tempfile.mkdtemp())
for n, t in FILES.items(): (root / n).write_text(textwrap.dedent(t).lstrip())
py = {p.name: ast.parse(p.read_text()) for p in root.glob("*.py")}
text = {p.name: p.read_text() for p in root.glob("*.py")}

# 1 glue code: modules that import both numpy and pandas and define no logic beyond conversions
for n, t in py.items():
    src = text[n]
    if "asarray" in src and "to_numpy" in src and "DataFrame(" in src:
        print(f"glue code            : {n} converts np<->pandas back and forth with no real logic")
# 2 pipeline jungle: many step files with version-ish names
jungle = sorted(n for n in py if re.match(r"step\d+_.*(v\d|final|tmp)", n))
print(f"pipeline jungle      : {len(jungle)} step files with v2/final/tmp style names -> {jungle[:3]} ...")
# 3 dead experimental path: module-level flag that is constant False/True and guards a branch
for n, t in py.items():
    for node in t.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, bool) \
           and node.targets[0].id.isupper():
            print(f"dead experimental    : {n}: constant flag {node.targets[0].id} = {node.value.value} guards a branch")
# 4 config debt: keys in config.json never read via cfg["key"] in code
import json
keys = json.loads((root / "config.json").read_text())
used = set(re.findall(r'cfg\["(\w+)"\]', "".join(text.values())))
print(f"configuration debt   : {sorted(set(keys) - used)} are in config.json but never read")
