D=$(cd "$(dirname "$0")"; pwd)
source "$D/../env.sh"
rm -rf /tmp/claude-0/b4q24_art_root
W=$(mktemp -d /tmp/claude-0/b4q24.XXXX); cd $W
python3 -I "$D/q24.py" 2>&1 | grep -v "INFO\|Downloading"
