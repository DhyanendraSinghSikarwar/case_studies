V=/tmp/claude-0/b7p07/v/bin
D=$(dirname "$(readlink -f "$0")")
for w in fair unfair; do echo "\$ python3 -I fairness_gate.py $w"; $V/python -I $D/fairness_gate.py $w; echo "exit=$?"; done
