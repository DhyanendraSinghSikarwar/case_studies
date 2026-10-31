V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
export PYTHONDONTWRITEBYTECODE=1; cd $D
echo '$ pytest -q -p no:cacheprovider test_rollout.py'; $V/pytest -q -p no:cacheprovider test_rollout.py
echo '$ python3 -I demo.py'; $V/python -I demo.py
