cd "$(dirname "$0")"
echo "--- docker buildx version"; docker buildx version 2>&1
echo "--- docker buildx build --help (platform and output lines)"
docker buildx build --help 2>&1 | grep -E "^\s+(--platform|--push|--load|-o, --output|--cache-from|--cache-to)\b"
echo "--- uname -m"; uname -m
echo "--- python3 -I arch_check.py"; python3 -I arch_check.py
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
echo "--- real build attempt:"; docker buildx build --platform linux/amd64,linux/arm64 . 2>&1 | head -3
