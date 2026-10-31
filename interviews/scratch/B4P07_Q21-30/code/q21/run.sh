PY=/tmp/claude-0/b7p07/v/bin/python
D=$(dirname "$(readlink -f "$0")")
bash $D/make_trees.sh /tmp/claude-0/b7_q21_30/q21
echo '$ python3 -I repo_lint.py good/'; $PY -I $D/repo_lint.py /tmp/claude-0/b7_q21_30/q21/good; echo "exit=$?"
echo '$ python3 -I repo_lint.py bad/'; $PY -I $D/repo_lint.py /tmp/claude-0/b7_q21_30/q21/bad; echo "exit=$?"
