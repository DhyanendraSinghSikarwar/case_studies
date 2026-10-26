set -e
D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q22.XXXX); cd $W
python3 -I "$D/q22.py" 2>&1 | sed "s/\x1b\[[0-9;]*m//g" | grep -v "INFO\|Downloading\|color_warning"
