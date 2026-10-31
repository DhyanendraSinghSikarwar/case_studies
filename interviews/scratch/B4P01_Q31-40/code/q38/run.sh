set -e -o pipefail
Q=/home/user/case_studies/interviews/scratch/B4P01_Q31-40/code/q38
W=$(mktemp -d); cp -r $Q/pkg $W/src; cp -r $Q/tests $W/tests; cd $W
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@x GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@x
cd src; git init -q -b main; git add .; git commit -qm "teamlib 1.2.0"; git tag v1.2.0; cd ..
python3 -m build --wheel --no-isolation -o shared_dir src >/dev/null 2>&1
python3 -m venv v; PIP="./v/bin/pip -q install --disable-pip-version-check"
echo "--- form 1: git URL pinned to a tag (local path used here instead of a hosted remote) ---"
$PIP "teamlib @ git+file://$W/src@v1.2.0" 2>&1 | tail -2
./v/bin/pip list --disable-pip-version-check 2>/dev/null | grep -i teamlib
./v/bin/pip uninstall -y -q teamlib
echo "--- form 3: shared directory of wheels, no network, no index ---"
$PIP --no-index --find-links shared_dir teamlib==1.2.0
./v/bin/pip list --disable-pip-version-check 2>/dev/null | grep -i teamlib
echo "--- tests (pytest.warns) ---"
$PIP pytest 2>&1 | tail -1
./v/bin/python -m pytest -q tests 2>&1 | tail -3
echo "--- how the old call looks to a user ---"
./v/bin/python -W default -c "import teamlib; teamlib.build_features([1,None])" 2>&1 | cut -c1-200 | sed "s#$W#<tmp>#"
