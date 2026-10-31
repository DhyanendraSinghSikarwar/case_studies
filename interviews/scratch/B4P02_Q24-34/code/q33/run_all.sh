cd "$(dirname "$0")"
echo "--- docker buildx build --help (cache flags)"
docker buildx build --help 2>&1 | grep -A3 -E "^\s+--cache-(from|to)"
echo "--- check_workflow.py"; python3 -I check_workflow.py build.yml
echo "--- cache_sim.py"; python3 -I cache_sim.py
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
