"""Q43: policy checks on a compose file. Uses `docker compose config --format json` (no daemon needed).
Run: python3 -I validate.py compose.yml"""
import json, os, re, subprocess, sys
import yaml

def seconds(d):
    """'10m0s' -> 600. Compose prints durations in Go style."""
    return sum(float(n) * {'h': 3600, 'm': 60, 's': 1}[u] for n, u in re.findall(r'([\d.]+)([hms])', d))

env = dict(os.environ, VLLM_TAG="v0.0.0-example", MODEL_ID="org/model", HF_TOKEN="hf_FAKE_for_demo")
cfg = json.loads(subprocess.run(["docker", "compose", "-f", sys.argv[1], "config", "--format", "json"],
                                capture_output=True, text=True, env=env, check=True).stdout)
svc = cfg["services"]["llm"]
checks = {}
checks["image pinned (not latest, has tag)"] = ":" in svc["image"] and not svc["image"].endswith(":latest")
checks["GPU reserved"] = any("gpu" in d["capabilities"] for d in svc["deploy"]["resources"]["reservations"]["devices"])
checks["shm: ipc host or shm_size"] = svc.get("ipc") == "host" or "shm_size" in svc
checks["weights on a named volume"] = any(v["type"] == "volume" for v in svc["volumes"])
raw = yaml.safe_load(open(sys.argv[1]))["services"]["llm"]["environment"]
checks["HF_TOKEN has no value in the file (pass-through)"] = "HF_TOKEN" in raw and raw["HF_TOKEN"] is None
checks["healthcheck start_period >= 300s"] = seconds(svc["healthcheck"]["start_period"]) >= 300
checks["port bound to 127.0.0.1"] = svc["ports"][0].get("host_ip") == "127.0.0.1"
for k, v in checks.items(): print(("PASS" if v else "FAIL"), k)
sys.exit(0 if all(checks.values()) else 1)
