#!/usr/bin/env bash
# Q7: notebook diffs: raw vs nbstripout vs jupytext
set -e
. "$(dirname "$0")/env.sh"
W=$(mktemp -d); cd "$W"; git init -q -b main r; cd r
python3 -I - <<'PY'
import json, base64
def nb(count, value):
    fake_png = base64.b64encode(bytes(range(256)) * 40).decode()      # ~13 KB fake plot
    cells = [
      {"cell_type":"code","id":"cell0001","execution_count":count,"metadata":{},"source":["import numpy as np\n","x = np.arange(5)\n","x.mean()"],
       "outputs":[{"output_type":"execute_result","execution_count":count,"data":{"text/plain":[str(value)]},"metadata":{}}]},
      {"cell_type":"code","id":"cell0002","execution_count":count+1,"metadata":{},"source":["plot()"],
       "outputs":[{"output_type":"display_data","data":{"image/png":fake_png,"text/plain":["<Figure>"]},"metadata":{}}]},
    ]
    return {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
            "language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":5}
json.dump(nb(1, 2.0), open("a.ipynb","w"), indent=1)
json.dump(nb(7, 2.0), open("b.ipynb","w"), indent=1)   # same code, re-run: only counts differ (+ image bytes re-rendered)
PY
cp a.ipynb eda.ipynb; git add eda.ipynb; c -m "notebook v1 (raw, with outputs)"
# teammate re-runs everything: new execution counts and a re-rendered image
python3 -I - <<'PY'
import json, base64
d = json.load(open("b.ipynb")); d["cells"][1]["outputs"][0]["data"]["image/png"] = base64.b64encode(bytes(range(255,-1,-1))*40).decode()
json.dump(d, open("eda.ipynb","w"), indent=1)
PY
echo "=== RAW notebook: diff after a plain re-run (no code change)"
git diff --stat; echo "diff lines: $(git diff | wc -l), diff bytes: $(git diff | wc -c)"
git add eda.ipynb; c -m "notebook v2 (raw re-run)"
echo; echo "=== STRIPPED: nbstripout on both versions"
git show HEAD~1:eda.ipynb | nbstripout > s1.ipynb
nbstripout < eda.ipynb > s2.ipynb
echo "size raw=$(wc -c < eda.ipynb) bytes, stripped=$(wc -c < s2.ipynb) bytes"
echo "diff lines between stripped v1 and stripped v2: $(diff s1.ipynb s2.ipynb | wc -l)  (re-run noise gone)"
echo; echo "=== install as a git filter so you cannot forget (writes .git/config + .git/info/attributes)"
nbstripout --install >/dev/null; grep -A3 'filter "nbstripout"' .git/config | head -4; cat .git/info/attributes   # per-clone; commit a .gitattributes line too so teammates get it
echo; echo "=== JUPYTEXT: pair with a .py file, review the .py"
jupytext --set-formats ipynb,py:percent eda.ipynb 2>&1 | tail -1   # pair them
jupytext --sync eda.ipynb 2>&1 | tail -1                           # keeps both files in step
git status --short
cat eda.py
echo "py size=$(wc -c < eda.py) bytes vs ipynb=$(wc -c < eda.ipynb) bytes"
rm -rf "$W"
