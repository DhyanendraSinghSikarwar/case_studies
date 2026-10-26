D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q27.XXXX); cd $W
timeout 90 python3 -I "$D/q27.py" 2>&1 | tail -30
