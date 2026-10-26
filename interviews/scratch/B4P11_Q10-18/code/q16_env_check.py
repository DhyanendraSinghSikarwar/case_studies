import sys, re, warnings, yaml; warnings.filterwarnings("ignore")
from azure.ai.ml import load_environment
import azure.ai.ml as m
print("azure-ai-ml", m.__version__)
e = load_environment("q16/env.yml")
print("loaded:", e.name, e.version, "| image:", e.image, "| conda_file type:", type(e.conda_file).__name__)
d = load_environment("q16/docker_env.yml")
print("docker env:", d.name, "| build context:", d.build.path.name if hasattr(d.build.path, "name") else d.build.path, "| image:", d.image)

PIN = re.compile(r"^[A-Za-z0-9_.\-]+(\[[^\]]+\])?==[^=\s]+$")     # name==version
def unpinned(conda_path):
    c = yaml.safe_load(open(conda_path)); bad = []
    for dep in c["dependencies"]:
        if isinstance(dep, str):
            if not re.search(r"=", dep): bad.append(dep)              # conda: need name=ver
        else:
            for p in dep["pip"]:
                if not PIN.match(p): bad.append("pip:" + p)
    return bad
files = sys.argv[1:] or ["q16/conda.yml", "q16/conda_good.yml"]
rc = 0
for f in files:
    b = unpinned(f)
    print(f, "->", "OK all pinned" if not b else f"FAIL unpinned: {b}")
    rc |= bool(b)
sys.exit(rc)      # non-zero fails the CI step
