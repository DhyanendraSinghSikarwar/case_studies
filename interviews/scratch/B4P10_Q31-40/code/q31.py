# Q31: which credential source does boto3 pick? Each case runs in a child process with a clean env and a temp HOME.
import json, os, subprocess, sys, tempfile, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

CHILD = r'''
import boto3, botocore.credentials as c
s = boto3.session.Session()
names = [p.METHOD for p in c.create_credential_resolver(s._session).providers]
try:
    cr = s.get_credentials()
    print("resolved method:", None if cr is None else cr.method, "| key:", None if cr is None else cr.access_key)
except Exception as e:
    print("error:", type(e).__name__)
print("chain order in this botocore:", names) if %r else None
'''

tmp = tempfile.mkdtemp(dir="/tmp/claude-0/b10_q31_40")
creds_file = os.path.join(tmp, "credentials")
open(creds_file, "w").write("[default]\naws_access_key_id = AKIAFAKEFILEKEY0000\naws_secret_access_key = fakesecretfile\n")
tok = os.path.join(tmp, "token"); open(tok, "w").write("fake.jwt.token")

class H(BaseHTTPRequestHandler):  # stands in for the ECS/container credentials endpoint (loopback only)
    def do_GET(self):
        body = json.dumps({"AccessKeyId": "ASIAFAKECONTAINER00", "SecretAccessKey": "fakesecretcontainer",
                           "Token": "faketoken", "Expiration": "2099-01-01T00:00:00Z"}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass
srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()

base = {"PATH": os.environ["PATH"], "HOME": tmp, "AWS_DEFAULT_REGION": "us-east-1",
        "AWS_EC2_METADATA_DISABLED": "true",             # no IMDS call: keeps the sandbox off the network
        "AWS_SHARED_CREDENTIALS_FILE": os.path.join(tmp, "nope"), "AWS_CONFIG_FILE": os.path.join(tmp, "nope2")}
cases = [
  ("1 env vars", {"AWS_ACCESS_KEY_ID": "AKIAFAKEENVKEY00000", "AWS_SECRET_ACCESS_KEY": "fakesecretenv"}),
  ("2 shared credentials file", {"AWS_SHARED_CREDENTIALS_FILE": creds_file}),
  ("3 env vars AND file (env wins)", {"AWS_ACCESS_KEY_ID": "AKIAFAKEENVKEY00000", "AWS_SECRET_ACCESS_KEY": "fakesecretenv", "AWS_SHARED_CREDENTIALS_FILE": creds_file}),
  ("4 container credentials (local fake endpoint)", {"AWS_CONTAINER_CREDENTIALS_FULL_URI": f"http://127.0.0.1:{srv.server_port}/creds"}),
  ("5 nothing at all", {}),
]
for i, (name, extra) in enumerate(cases):
    env = dict(base, **extra)
    print("==", name)
    out = subprocess.run([sys.executable, "-I", "-c", CHILD % (i == 0)], env=env, capture_output=True, text=True)
    print((out.stdout + out.stderr).strip())
srv.shutdown()
print("NOT executed: IMDS (disabled), web identity / IRSA / Pod Identity (need an STS endpoint and an issuer).")
