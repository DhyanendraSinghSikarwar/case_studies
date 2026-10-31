cd "$(dirname "$0")"
echo "--- docker version (client part works; no server here)"; docker version 2>&1 | grep -E 'Client|^ Version|Server|failed'
echo "--- find_sock.py"; python3 -I find_sock.py pod_bad.yaml pod_ok.yaml
echo "--- oci_types.py"; python3 -I oci_types.py
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
