D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q29.XXXX); cd $W
python3 -I "$D/q29.py" 2>&1 | grep -v "INFO\|Downloading\|WARNING\|Registered model\|Created version"
