D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q26.XXXX); cd $W; cp $D/sweep.yaml .
python3 -I "$D/validate_sweep.py"
echo "--- wandb.sweep with no account (WANDB_MODE=offline) ---"
timeout 60 python3 -I "$D/try_sweep.py" 2>&1 | tail -3
