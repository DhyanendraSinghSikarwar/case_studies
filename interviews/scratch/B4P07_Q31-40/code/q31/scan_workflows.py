"""Flag unpinned third-party actions, missing permissions, risky triggers, unhashed pip installs."""
import pathlib, re, sys
import yaml

SHA = re.compile(r"^[0-9a-f]{40}$")

def triggers(doc):
    on = doc.get("on", doc.get(True))      # YAML 1.1: the key `on` loads as True
    if isinstance(on, str):
        return [on]
    return list(on) if on else []

def scan_file(path):
    problems = []
    doc = yaml.safe_load(path.read_text())
    if "permissions" not in doc:
        jobs_without = [n for n, j in doc["jobs"].items() if "permissions" not in j]
        if jobs_without:
            problems.append(f"no permissions block (top level or job: {', '.join(jobs_without)})")
    if "pull_request_target" in triggers(doc):
        problems.append("trigger pull_request_target: never check out PR head code with it")
    for jname, job in doc["jobs"].items():
        for i, step in enumerate(job.get("steps", []), 1):
            uses = step.get("uses")
            if uses and not uses.startswith("./"):
                ref = uses.split("@", 1)[1] if "@" in uses else ""
                if not SHA.match(ref):
                    problems.append(f"{jname} step {i}: '{uses}' not pinned to a 40-char SHA")
            run = step.get("run", "")
            if "pip install" in run and "--require-hashes" not in run and " -e " not in run:
                problems.append(f"{jname} step {i}: pip install without --require-hashes")
    return problems

def main(root):
    bad = 0
    for f in sorted(pathlib.Path(root).glob(".github/workflows/*.y*ml")):
        problems = scan_file(f)
        print(f"{f.relative_to(root)}: {'OK' if not problems else str(len(problems)) + ' problem(s)'}")
        for p in problems:
            print("  -", p)
        bad += len(problems)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
