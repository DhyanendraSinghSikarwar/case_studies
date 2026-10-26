# run in a temp dir; needs network to PyPI. Tampers every hash of certifi, pip must refuse.
python3 -m venv v
python3 - <<'PY'
s = open("requirements.txt").read()
s = s.replace("a9895e6e2758b371e0545e321a3a8fd1fcfd9829ada8824a936dfb16aaaf36cd", "0"*64)
s = s.replace("e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1", "1"*64)
open("tampered.txt", "w").write(s)
PY
v/bin/pip install --require-hashes --no-deps --dry-run -r requirements.txt | tail -1
v/bin/pip install --require-hashes --no-deps --dry-run -r tampered.txt 2>&1 | grep -E "ERROR|Expected|Got"
