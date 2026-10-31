set -u; W=$1; rm -rf $W; mkdir -p $W/remote; cd $W; export PATH=/tmp/claude-0/ven/v/bin:$PATH
git init -q -b main; git config user.email a@b.c; git config user.name t
git lfs install --local >/dev/null 2>&1
git lfs track "*.csv" >/dev/null; printf 'a,b\n1,2\n' > big.csv
git add -A; git commit -qm "with lfs"
echo "--- before: what git stores in the commit for big.csv"; git show HEAD:big.csv; git lfs ls-files
echo "--- step 1: make sure the real file is in the workspace (git lfs pull); step 2: stop tracking it in LFS"
git lfs untrack "*.csv" >/dev/null; git rm -q --cached big.csv
echo "--- step 3: hand it to DVC"
dvc init -q; dvc remote add -d loc $W/remote >/dev/null; dvc add big.csv 2>&1 | tail -2
git add -A; git commit -qm "move big.csv to DVC"
echo "--- after: what git stores now"; git show HEAD:big.csv.dvc | head -4; git ls-files
dvc push 2>&1 | tail -1
echo "--- old history still holds the LFS pointer:"; git show HEAD~1:big.csv | head -3
