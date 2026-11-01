set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); cp proj/* $W/; cd $W
git init -q; git config user.email a@b.c; git config user.name demo
dvc init -q; git add -A; git commit -qm init
dvc repro -q; git add -A; git commit -qm "baseline C=1.0"
echo "--- unrelated edit: add an unused key to params.yaml"
printf "notes:\n  owner: team-a\n" >> params.yaml
dvc status
echo "--- change train.C"
sed -i 's/C: 1.0/C: 0.01/' params.yaml
dvc repro -q
echo "--- params diff (workspace vs HEAD)"; dvc params diff
echo "--- metrics diff (workspace vs HEAD)"; dvc metrics diff
echo "--- metrics show"; dvc metrics show
git add -A; git commit -qm "C=0.01"
echo "--- metrics diff HEAD~1 HEAD"; dvc metrics diff HEAD~1 HEAD
echo "--- plots diff --json (head)"; dvc plots diff HEAD~1 HEAD -o plots_out >/dev/null 2>&1 && ls plots_out || echo "plots diff failed"
echo "--- misspelled param key"
sed -i 's/- train.C$/- train.Cc/' dvc.yaml
dvc repro 2>&1 | tail -4 || true
sed -i 's/- train.Cc$/- train.C/' dvc.yaml
echo "--- metrics file missing"
rm metrics.json
dvc metrics show 2>&1 | tail -3 || true
