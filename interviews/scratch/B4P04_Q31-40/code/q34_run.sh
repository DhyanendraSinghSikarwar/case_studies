set -u; W=$1; rm -rf $W; mkdir -p $W/repo $W/remote; cd $W/repo
git init -q -b main; git config user.email a@b.c; git config user.name t; dvc init -q; git commit -qm init
dvc remote add -d loc $W/remote >/dev/null
echo v1 > data.csv; dvc add data.csv >/dev/null; git add -A; git commit -qm v1; git tag v1
git checkout -qb feature; echo v2-feature > data.csv; dvc add data.csv >/dev/null; git add -A; git commit -qm feature; git tag feat
git checkout -q main; echo v3 > data.csv; dvc add data.csv >/dev/null; git add -A; git commit -qm v3
dvc push 2>&1 | tail -1; git checkout -q feature; dvc push 2>&1 | tail -1; git checkout -q main
echo "--- report: main only"; python -I $2 . main
echo; echo "--- report: main + feature branch"; python -I $2 . main feature
echo; echo "--- dvc gc dry run, workspace only (keeps just what main HEAD needs), cloud remote"
dvc gc -w -c -f --dry 2>&1 | tail -6
echo "--- dvc gc dry run, all branches and tags"
dvc gc -A -c -f --dry 2>&1 | tail -4
