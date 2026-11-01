"""Used by HEALTHCHECK: exit 0 if /ready returns 200, else 1. No curl needed."""
import sys, urllib.request
url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/ready"
try:
    sys.exit(0 if urllib.request.urlopen(url, timeout=2).status == 200 else 1)
except Exception:
    sys.exit(1)
