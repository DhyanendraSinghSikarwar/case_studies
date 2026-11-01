V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
export MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1 PYTHONDONTWRITEBYTECODE=1
rm -rf /tmp/claude-0/b7_q21_30/q24; mkdir -p /tmp/claude-0/b7_q21_30/q24
cd $D
echo '$ pytest -q -p no:cacheprovider test_approve.py'; $V/pytest -q -p no:cacheprovider test_approve.py 2>&1 | tail -5
echo '$ python3 -I demo.py'; $V/python -I demo.py 2>&1 | grep -v -i "alembic\|INFO\|warn"
