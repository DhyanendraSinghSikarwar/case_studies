#!/usr/bin/env bash
# Q1: what goes in Git, .gitignore, LFS, and removing a pushed secret
set -e
. "$(dirname "$0")/env.sh"
W=$(mktemp -d); cd "$W"; git init -q -b main proj; cd proj
mkdir -p src data models notebooks
echo 'def train(): pass' > src/train.py
echo 'numpy==2.5.3' > requirements.txt
echo 'seed: 42' > params.yaml
head -c 400000 /dev/urandom > data/train.parquet      # stand-in for the 400 MB file
head -c 1200000 /dev/urandom > models/model.pkl        # stand-in for the 1.2 GB file
echo 'AWS_SECRET_ACCESS_KEY=FAKEKEY123' > .env
echo '{"cells":[]}' > notebooks/eda.ipynb
mkdir -p __pycache__ .ipynb_checkpoints; echo x > __pycache__/a.pyc
cat > .gitignore <<'G'
# secrets
.env
.env.*
!.env.example
# data and models (tracked by DVC or LFS instead)
data/
models/
*.pkl
*.parquet
# python and notebook noise
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
G
echo 'AWS_SECRET_ACCESS_KEY=' > .env.example
echo '--- git status --short (what Git sees)'; git status --short
echo '--- git check-ignore -v (which rule hides each file)'
git check-ignore -v .env data/train.parquet models/model.pkl __pycache__/a.pyc
echo '--- commit, then show tracked files'
git add -A; c -m "initial: code, params, gitignore"; git ls-files
echo '--- the Git LFS alternative: track patterns, writes .gitattributes'
git lfs install --local >/dev/null; git lfs track "*.parquet" "*.pkl"; cat .gitattributes
echo '--- secret already committed: simulate the mistake'
echo 'AWS_SECRET_ACCESS_KEY=FAKEKEY123' > config.env; git add -f config.env; c -m "oops add key"
git log --oneline --all -- config.env
echo '--- rewrite history with git filter-repo (on a fresh clone, as the tool requires)'
cd "$W"; git clone -q proj clean; cd clean
git filter-repo --invert-paths --path config.env --force 2>&1 | tail -2
echo 'file in history after rewrite:'; git log --oneline --all -- config.env | wc -l
echo '(rotate the key anyway: anyone who pulled earlier still has it)'
rm -rf "$W"
