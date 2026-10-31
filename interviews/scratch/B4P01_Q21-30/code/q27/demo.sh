set -e
export GIT_AUTHOR_DATE="2026-01-01T00:00:00+0000" GIT_COMMITTER_DATE="2026-01-01T00:00:00+0000"
D=$(mktemp -d); cd "$D"
git init -q -b main; git config user.email a@b.c; git config user.name demo
mkdir -p src/credit_model
pyproject() { cat > pyproject.toml <<T
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "credit-model"
version = "$1"
dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["src/credit_model"]
T
}
code() { cat > src/credit_model/__init__.py <<P
from importlib.metadata import version

__version__ = version("credit-model")   # single source of truth: the installed package metadata

def score(income$1):
    """Risk score in $2."""
    return $3

def model_card():
    return {"code_version": __version__, "data_version": "loans-2026-01", "output_scale": "$4"}
P
}
release() { git add -A; git commit -qm "release $1"; git tag -a "v$1" -m "credit-model $1 $2"; }

pyproject 1.0.0; code "" "[0, 1]" "min(income / 100.0, 1.0)" "0-1"
printf '# Changelog\n\n## 1.0.0\n- First release. score() returns a value in [0, 1].\n' > CHANGELOG.md
release 1.0.0 "(data loans-2026-01)"

pyproject 1.1.0; code ", tenure_years=0" "[0, 1]" "min(income / 100.0, 1.0)" "0-1"          # new optional arg: MINOR
printf '# Changelog\n\n## 1.1.0\n- Added optional tenure_years argument (backward compatible).\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 1.1.0 ""

pyproject 1.1.1; code ", tenure_years=0" "[0, 1]" "max(min(income / 100.0, 1.0), 0.0)" "0-1"   # clamp negatives: PATCH
printf '# Changelog\n\n## 1.1.1\n- Fix: negative income no longer gives a negative score.\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 1.1.1 ""

pyproject 2.0.0; code ", tenure_years=0" "[0, 100]" "max(min(income, 100.0), 0.0)" "0-100"        # scale change: MAJOR
printf '# Changelog\n\n## 2.0.0 (BREAKING)\n- score() now returns 0-100 instead of 0-1. Update your thresholds.\n%s\n' "$(tail -n +3 CHANGELOG.md)" > C.tmp; mv C.tmp CHANGELOG.md
release 2.0.0 "(output scale 0-100)"

echo '$ git tag -n1'; git tag -n1
echo; echo '$ head -9 CHANGELOG.md'; head -9 CHANGELOG.md

python3 -m venv --system-site-packages "$D/.venv" >/dev/null
PIP="$D/.venv/bin/pip install -q --no-build-isolation --no-deps --disable-pip-version-check"
echo; echo "--- install the latest tag, read version at runtime ---"
git checkout -q v2.0.0; $PIP .
"$D/.venv/bin/python" -I -c "import credit_model as m; print(m.__version__, m.score(40), m.model_card())"
echo "--- rollback: check out the previous good tag and reinstall ---"
git checkout -q v1.1.1; $PIP --force-reinstall .
"$D/.venv/bin/python" -I -c "import credit_model as m; print(m.__version__, m.score(40), m.model_card())"
echo; echo '$ git describe --tags   # one commit after v2.0.0'
git checkout -q main; echo "" >> CHANGELOG.md; git commit -qam "docs"; git describe --tags | sed -E 's/g[0-9a-f]+$/g<sha>/'
