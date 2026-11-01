cd "$(dirname "$0")"
echo "--- docker compose version"; docker compose version
echo "--- docker compose config (base only), GPU part"
docker compose -f compose.yml config | sed -n '/devices:/,/count/p'
echo "--- check.py"; python3 -I check.py
echo "--- up was not run:"; docker compose -f compose.yml up -d 2>&1 | head -2
