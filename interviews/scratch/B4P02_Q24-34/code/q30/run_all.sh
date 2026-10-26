cd "$(dirname "$0")"
python3 -I check_daemon.py daemon.json bad_daemon.json; echo "exit=$?"
echo "--- rotation model"; python3 -I rotation_sim.py
echo "--- real flag names from the CLI help (no daemon needed)"
docker system prune --help 2>&1 | grep -E "^\s+(-a, --all|--volumes|--filter|-f, --force)"
docker volume prune --help 2>&1 | grep -E "^\s+(-a, --all|--filter)"
docker image prune --help 2>&1 | grep -E "^\s+(-a, --all|--filter)"
echo "--- docker system df (no daemon here)"; docker system df 2>&1 | head -2
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
