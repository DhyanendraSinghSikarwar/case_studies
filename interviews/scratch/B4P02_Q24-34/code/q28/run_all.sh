cd "$(dirname "$0")"
echo "--- hadolint on both variants"
hadolint --no-color Dockerfile.pip; echo "pip variant exit=$?"
hadolint --no-color Dockerfile.uv;  echo "uv variant exit=$?"
echo "--- uv version"; uv --version
echo "--- uv pip compile --generate-hashes (a real lockfile with hashes, tiny example)"
uv pip compile requirements.in --generate-hashes -q --no-header -o "${TMPDIR:-/tmp}/q28_req.txt" 2>&1 | tail -3
sed -E 's/(sha256:[0-9a-f]{12})[0-9a-f]+/\1.../' "${TMPDIR:-/tmp}/q28_req.txt"
echo "--- pip's own check that hashes are enforced: wrong hash must fail"
printf 'packaging==24.1 --hash=sha256:0000000000000000000000000000000000000000000000000000000000000000\n' > "${TMPDIR:-/tmp}/bad_req.txt"
python3 -m pip install --dry-run --no-deps --require-hashes -r "${TMPDIR:-/tmp}/bad_req.txt" 2>&1 | grep -iE "hash|error" | head -4
