#!/usr/bin/env bash
# Q10: sys.path hack -> installable src-layout package; build wheel + sdist; install in a clean venv
set -e
W=$(mktemp -d); cd "$W"; mkdir -p churnkit/src/churnkit churnkit/tests; cd churnkit
cat > pyproject.toml <<'T'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "churnkit"
version = "0.1.0"
description = "Shared feature helpers for the churn team"
requires-python = ">=3.10"
dependencies = ["pandas>=2.0"]

[project.optional-dependencies]
dev = ["pytest"]

[tool.hatch.build.targets.wheel]
packages = ["src/churnkit"]
T
cat > src/churnkit/__init__.py <<'T'
from churnkit.features import add_ratio

__version__ = "0.1.0"
__all__ = ["add_ratio"]
T
cat > src/churnkit/features.py <<'T'
import pandas as pd


def add_ratio(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ratio"] = out["spend"] / out["tenure"].clip(lower=1)
    return out
T
cat > tests/test_features.py <<'T'
import pandas as pd
from churnkit import add_ratio


def test_add_ratio():
    out = add_ratio(pd.DataFrame({"spend": [100.0], "tenure": [4]}))
    assert out["ratio"].iloc[0] == 25.0
T
echo "--- layout"; find . -type f | sort
echo "--- build wheel + sdist (isolated build env pulls hatchling from the index)"
python3 -m build 2>&1 | tail -2
ls dist
echo "--- wheel contents (src/ is NOT in the wheel; the package sits at the top level)"
python3 -c "import zipfile,sys; print('\n'.join(zipfile.ZipFile(sys.argv[1]).namelist()))" dist/*.whl
echo "--- sdist contents"
python3 -c "import tarfile,sys; print('\n'.join(tarfile.open(sys.argv[1]).getnames()))" dist/*.tar.gz
echo "--- fresh venv, install the WHEEL only, run from another folder (so the source tree cannot leak in)"
python3 -m venv "$W/v1" >/dev/null; mkdir "$W/elsewhere"; cd "$W/elsewhere"
"$W/v1/bin/pip" -q install "$W"/churnkit/dist/*.whl 2>&1 | tail -2
"$W/v1/bin/python" -I -c "import churnkit, pandas; print('imported from', churnkit.__file__.replace('$W','<tmp>')); print('version', churnkit.__version__)"
"$W/v1/bin/pip" list 2>/dev/null | grep -iE "churnkit|pandas"
echo "--- editable install in a second venv: edit the source, no reinstall needed"
python3 -m venv "$W/v2" >/dev/null
"$W/v2/bin/pip" -q install -e "$W/churnkit[dev]" 2>&1 | tail -2
cd "$W/churnkit"
sed -i 's/clip(lower=1)/clip(lower=2)/' src/churnkit/features.py
cd "$W/elsewhere"; "$W/v2/bin/python" -c "
import pandas as pd, churnkit
print('after editing source, ratio =', churnkit.add_ratio(pd.DataFrame({'spend':[100.0],'tenure':[1]})).ratio[0], '(clip(lower=2) is live)')"
sed -i 's/clip(lower=2)/clip(lower=1)/' "$W/churnkit/src/churnkit/features.py"
echo "--- run tests against the installed package"
cd "$W/churnkit"; "$W/v2/bin/python" -m pytest -q -p no:cacheprovider 2>&1 | tail -2
rm -rf "$W"
