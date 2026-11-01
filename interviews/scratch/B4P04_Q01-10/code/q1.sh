set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); cd $W
git init -q; git config user.email a@b.c; git config user.name demo
python3 -I - <<'PY'
import random
random.seed(0)
with open("train.csv","w") as f:
    f.write("x,y\n")
    for i in range(1000): f.write(f"{random.random():.4f},{i%2}\n")
PY
dvc init -q
git commit -qm "dvc init"
dvc add train.csv
echo "--- train.csv.dvc"; cat train.csv.dvc
echo "--- .gitignore"; cat .gitignore
echo "--- git status"; git status --short
git add train.csv.dvc .gitignore
git commit -qm "track train.csv"
echo "--- cache layout"; find .dvc/cache -type f | sed 's#.dvc/cache/##'
echo "--- silent edit"; echo "0.5,1" >> train.csv
dvc status
echo "--- md5 now"; md5sum train.csv
