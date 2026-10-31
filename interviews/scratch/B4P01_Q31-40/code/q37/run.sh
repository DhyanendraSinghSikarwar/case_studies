set -e
W=$(mktemp -d); cp -r "/home/user/case_studies/interviews/scratch/B4P01_Q31-40/code/q37/pkg" $W/pkg; cd $W/pkg
python3 -m build --wheel --no-isolation -o ../dist . 2>&1 | tail -1
cd ..; ls dist
echo "--- name-version-python-abi-platform: py3-none-any = pure Python, any OS ---"
echo "--- contents ---"; python3 -m zipfile -l dist/*.whl | awk '{print $1}' | tail -n +2
echo "--- METADATA (header part) ---"; python3 -m zipfile -e dist/*.whl x >/dev/null; cat x/mlutil-0.3.0.dist-info/METADATA | sed -n 1,14p
echo "--- WHEEL file ---"; cat x/mlutil-0.3.0.dist-info/WHEEL
echo "--- clean venv: install base vs extra (offline for the base; torch not downloaded) ---"
python3 -m venv v; ./v/bin/pip -q install --no-index --no-deps dist/*.whl
./v/bin/python -c "import mlutil; print(mlutil.scale([2,4,6]))"
./v/bin/python -c "import mlutil.gpu as g; g.to_device([1])" 2>&1 | tail -1
