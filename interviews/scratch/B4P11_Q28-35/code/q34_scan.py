# q34_scan.py - find AWS/SageMaker-specific references in a code+config tree. Regex scan, so false positives and misses are possible.
import re, sys, os, collections
RULES = [
 ("storage path",      r"s3a?://[\w.\-/]+",                         "use a data-URI variable; Azure: azureml:// or abfss://, GCP: gs://"),
 ("sdk import",        r"^\s*(import|from)\s+(boto3|botocore|sagemaker)\b", "wrap behind an interface; Azure: azure-ai-ml, GCP: google-cloud-aiplatform"),
 ("IAM role ARN",      r"arn:aws:iam::\d{12}:[^\s\"']+",                  "map to managed identity (Azure) or service account (GCP); do not copy the string"),
 ("container contract",r"/opt/ml/[\w/]+|\bSM_[A-Z_]+",              "SageMaker paths and env vars; re-read the target's input/output contract"),
 ("endpoint URL",      r"https://runtime\.sagemaker\.[\w.\-]+/\S+", "clients must call a new URL and auth; put the URL in config or behind a gateway"),
 ("ECR image",         r"\d{12}\.dkr\.ecr\.[\w\-]+\.amazonaws\.com/\S+", "push to ACR (Azure) or Artifact Registry (GCP)"),
 ("instance type",     r"\bml\.[a-z0-9]+\.\w+",                     "no 1:1 mapping; pick the target's machine type from current docs"),
 ("AWS env var",       r"\bAWS_[A-Z_]+",                            "remove; use the target's identity mechanism"),
]
hits = []
for dp, _, fs in os.walk(sys.argv[1]):
    for f in sorted(fs):
        p = os.path.join(dp, f)
        for n, line in enumerate(open(p, errors="ignore"), 1):
            for name, rx, hint in RULES:
                for m in re.finditer(rx, line, re.M):
                    hits.append((os.path.relpath(p, sys.argv[1]), n, name, m.group(0).strip()[:60], hint))
for h in sorted(hits): print(f"{h[0]}:{h[1]:<3} [{h[2]}] {h[3]}")
c = collections.Counter(h[2] for h in hits)
print("\nsummary:", dict(c), "| files with hits:", len({h[0] for h in hits}), "| clean.py hits:", sum(h[0] == "clean.py" for h in hits))
