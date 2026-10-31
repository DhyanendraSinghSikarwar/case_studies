cd "$(dirname "$0")"
echo "--- docker compose config (needs env vars; no daemon needed)"
HOST_UID=1001 HOST_GID=1001 JUPYTER_TOKEN=demo-token docker compose -f compose.yml config 2>&1 | grep -E "user:|host_ip|published|source:|read_only|driver|count|shm_size"
echo "--- missing token must fail"
HOST_UID=1001 docker compose -f compose.yml config 2>&1 | head -3
echo "--- pyyaml check"
python3 -I validate.py compose.yml; echo "exit=$?"
echo "--- UID/GID of this sandbox user, to show what --user would get"
id -u; id -g
echo "--- bash -n syntax check of run.sh"
bash -n run.sh && echo "run.sh syntax OK"
