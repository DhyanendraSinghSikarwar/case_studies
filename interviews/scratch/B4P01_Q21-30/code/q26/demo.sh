set -e
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
cp "$1/pre-commit-config.yaml" .pre-commit-config.yaml; cp -r "$1/tools" tools
git add -A; git commit -qm "add hooks" --no-verify
pre-commit install | sed "s#$D#<repo>#"
# a notebook with an output, a 6 MB file, a fake key, and a lint error
python3 -I - <<'PY'
import json
nb = {"cells":[{"cell_type":"code","execution_count":1,"metadata":{},"source":["print(1)"],
       "outputs":[{"output_type":"stream","name":"stdout","text":["1\n"]}]}],
      "metadata":{},"nbformat":4,"nbformat_minor":5}
json.dump(nb, open("eda.ipynb","w"))
open("big.bin","wb").write(b"0"*(6*1024*1024))
open("config.py","w").write('API_KEY = "sk_live_abcdef123456"\n')
open("train.py","w").write("import os\nprint('hi')\n")      # unused import -> ruff F401
PY
git add -A
echo '$ git commit -m "add eda"      # should be BLOCKED'
git commit -m "add eda" 2>&1 | sed -E 's/^(.{0,100}).*/\1/' | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
echo; echo "--- fix each problem ---"
git rm -q --cached big.bin; rm big.bin
printf 'import os\nAPI_KEY = os.environ["API_KEY"]\n' > config.py
printf 'print("hi")\n' > train.py
git add -A            # nbstripout already cleaned eda.ipynb in the working tree during the failed run
echo '$ git commit -m "add eda"      # second try'
git commit -m "add eda" 2>&1 | sed -E 's/^(.{0,100}).*/\1/' | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
echo; echo '--- bypass is possible: git commit --no-verify. So CI runs the same hooks: ---'
echo '$ pre-commit run --all-files   # same config, run in CI'
pre-commit run --all-files 2>&1 | grep -v -e '^$' -e 'MissingIDField' -e '_validate(nbdict' || true
git log --oneline | cat
git show --stat --format=%s HEAD | head -5
python3 -I -c "import json,subprocess; nb=json.loads(subprocess.check_output(['git','show','HEAD:eda.ipynb'])); print('outputs in the committed notebook:', nb['cells'][0]['outputs'])"
