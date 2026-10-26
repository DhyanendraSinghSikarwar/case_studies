set -u
cd "$(dirname "$0")"
pip install -q hadolint-py >/dev/null 2>&1
hadolint --version
echo "--- bad Dockerfile"
hadolint --no-color Dockerfile.bad; echo "exit=$?"
echo "--- good Dockerfile (no config)"
hadolint --no-color Dockerfile.good; echo "exit=$?"
echo "--- bad Dockerfile with repo config (DL3059 ignored, so fewer lines)"
hadolint --no-color --config cfg/hadolint.yaml Dockerfile.bad | sed "s/\x1b\[[0-9;]*m//g"; 
echo "--- good Dockerfile with repo config"
hadolint --no-color --config cfg/hadolint.yaml Dockerfile.good; echo "exit=$?"
echo "--- yaml parse of pre-commit and CI fragments"
python3 -I -c "
import yaml
for f in ['.pre-commit-config.yaml','ci_fragment.yml','cfg/hadolint.yaml']:
    d=yaml.safe_load(open(f)); print(f,'parses, top keys:',list(d))
"
