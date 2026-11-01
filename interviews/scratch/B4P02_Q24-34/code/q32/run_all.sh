cd "$(dirname "$0")"
echo "--- tools present?"; for t in trivy grype syft cosign; do command -v $t >/dev/null && echo "$t: found" || echo "$t: not installed"; done
docker scout version 2>&1 | head -1
echo "--- policy check, today = 2026-10-26"
python3 -I policy_check.py scan_sample.json waivers.json 2026-10-26; echo "exit=$?"
echo "--- same report with an empty waiver list"
W=$(mktemp); echo '[]' > "$W"; python3 -I policy_check.py scan_sample.json "$W" 2026-10-26 | sed -n '1,5p;$p'
echo "--- bash -n commands.sh"; bash -n commands.sh && echo OK
