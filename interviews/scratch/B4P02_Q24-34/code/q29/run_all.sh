cd "$(dirname "$0")"
python3 -I triage.py inspect_sample.json
echo; bash crlf_demo.sh 2>&1
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
