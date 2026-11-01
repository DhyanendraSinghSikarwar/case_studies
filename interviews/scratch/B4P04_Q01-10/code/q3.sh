set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); cp proj/* $W/; cd $W
git init -q; git config user.email a@b.c; git config user.name demo
dvc init -q; git add -A; git commit -qm init
echo "--- repro #1"; dvc repro 2>&1 | grep -v -i 'warn'
echo "--- dvc.lock (train stage)"; sed -n '/^  train:/,/^  evaluate:/p' dvc.lock | head -30
echo "--- dag"; dvc dag
echo "--- repro #2 (nothing changed)"; dvc repro
echo "--- edit only evaluate.py (comment)"; echo "# tweak" >> evaluate.py
dvc repro
echo "--- change train.C only"; sed -i 's/C: 1.0/C: 0.1/' params.yaml
dvc repro
echo "--- dvc status after changing prepare.seed"; sed -i "s/seed: 7/seed: 8/" params.yaml
dvc status
cat metrics.json
