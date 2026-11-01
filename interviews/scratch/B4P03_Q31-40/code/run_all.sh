#!/bin/sh
# Re-runs every snippet and stores real output in out/. Run from this folder.
mkdir -p out
V() { kubernetes-validate --strict "$@" 2>&1 | grep -v '^INFO /'; }
python3 -I q31_decide.py > out/q31.txt 2>&1
V q31_job.yaml > out/q31v.txt
python3 -I q32_portfolio_check.py > out/q32.txt 2>&1
python3 -I -c "import yaml;print(yaml.safe_load(open('q32_kind.yaml')))" > out/q32v.txt 2>&1
python3 -I q33_names.py > out/q33.txt 2>&1
V q33_statefulset.yaml > out/q33v.txt
python3 -I q34_reconcile.py > out/q34.txt 2>&1
V q34_daemonset.yaml > out/q34v.txt
python3 -I q35_score.py q35_hardened.yaml q35_bad.yaml > out/q35.txt 2>&1
V q35_hardened.yaml q35_bad.yaml > out/q35v.txt
python3 -I q36_idle.py > out/q36.txt 2>&1
python3 -I q37_check.py > out/q37.txt 2>&1
V q37_sa.yaml > out/q37v.txt
python3 -I q38_parse.py > out/q38.txt 2>&1
python3 -I -c "import yaml;d=yaml.safe_load(open('q38_servicemonitor.yaml'));print(d['kind'],d['spec']['endpoints'][0])" > out/q38v.txt 2>&1
python3 -I q39_check.py > out/q39.txt 2>&1
V q39_quota.yaml > out/q39v.txt
python3 -I q40_scan.py > out/q40.txt 2>&1
V q40_manifests/ok_deploy.yaml > out/q40v.txt
