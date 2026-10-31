set -e
export PATH=/tmp/claude-0/ven/v/bin:$PATH
W=$(mktemp -d); R=$(mktemp -d); cp proj/* $W/; cd $W
git init -q -b main; git config user.email a@b.c; git config user.name demo
dvc init -q; dvc remote add -d store $R/store -q; git add -A; git commit -qm init
dvc repro -q >/dev/null; dvc push -q
git add -A; git commit -qm "model v1"; git tag v1
echo "v1 model md5 from dvc.lock:"; grep -A3 'path: model.joblib' dvc.lock | grep md5: | head -1
echo "--- experiment moves on: C=0.01 -> model v2"
sed -i 's/C: 1.0/C: 0.01/' params.yaml; dvc repro -q >/dev/null; dvc push -q
git add -A; git commit -qm "model v2"
echo "v2 model md5:"; md5sum model.joblib | cut -c1-32
echo "--- go back to v1"
git -c advice.detachedHead=false checkout -q v1
dvc status
dvc checkout
echo "md5 of model.joblib on disk now:"; md5sum model.joblib | cut -c1-32
echo "--- repro dry-run check (is v1 reproducible without retraining?)"
dvc status
echo "--- fresh clone, pull from remote"
cd $(mktemp -d); git -c advice.detachedHead=false clone -q $W fresh; cd fresh; git -c advice.detachedHead=false checkout -q v1
cp $W/.dvc/config.local .dvc/ 2>/dev/null || true
ls
dvc pull
md5sum model.joblib | cut -c1-32
echo "--- remote garbage collected (gc keeps only workspace=v2)"
cd $W; git checkout -q main
dvc gc -w -c -f
cd $(mktemp -d); git -c advice.detachedHead=false clone -q $W fresh2; cd fresh2; git -c advice.detachedHead=false checkout -q v1
dvc pull 2>&1 | tail -6 || true
