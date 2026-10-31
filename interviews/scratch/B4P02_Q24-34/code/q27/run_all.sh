cd "$(dirname "$0")"
python3 -I drive.py
echo "--- bash -n docker_run.sh"; bash -n docker_run.sh && echo OK
