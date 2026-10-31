"""Q41: read-only lint of the Dockerfile text (the image was NOT built)."""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
lines = [l.strip() for l in open(os.path.join(here, "Dockerfile.lambda")) if l.strip() and not l.startswith("#")]
ins = [l.split()[0] for l in lines]
checks = {
  "starts with FROM": ins[0] == "FROM",
  "CMD is handler.handler (module.function)": any(l.startswith("CMD") and "handler.handler" in l for l in lines),
  "deps copied before code (cache friendly)": ins.index("RUN") < max(i for i, x in enumerate(ins) if x == "COPY"),
  "pip --no-cache-dir": any("--no-cache-dir" in l for l in lines),
  "no secrets (KEY/SECRET/PASSWORD)": not any(w in l.upper() for l in lines for w in ("SECRET", "PASSWORD", "AWS_ACCESS_KEY")),
}
for k, v in checks.items(): print(("ok   " if v else "FAIL ") + k)
sys.exit(0 if all(checks.values()) else 1)
