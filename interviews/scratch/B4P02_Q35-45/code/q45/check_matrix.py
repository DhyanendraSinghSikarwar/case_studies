"""Q45: check every project's Dockerfile against the platform compatibility matrix.
Run: python3 -I check_matrix.py matrix.yaml demo/projects"""
import glob, os, re, sys
import yaml

def v(s): return tuple(int(x) for x in s.split("."))

def check(matrix, projects_dir):
    fleet = matrix["fleet_driver_min_cuda"]
    problems, rows = [], []
    for path in sorted(glob.glob(os.path.join(projects_dir, "*", "Dockerfile"))):
        proj = os.path.basename(os.path.dirname(path))
        m = re.search(r"^FROM\s+\S*ml-base:(\S+)", open(path).read(), re.M)
        if not m:
            problems.append((proj, "does not start from the platform base image")); continue
        tag = m.group(1); b = matrix["bases"].get(tag)
        if b is None:
            problems.append((proj, f"base tag {tag} not in matrix")); continue
        notes = []
        if b["status"] == "deprecated": notes.append("deprecated base")
        if v(b["cuda"]) > v(fleet): notes.append(f"CUDA {b['cuda']} newer than fleet driver supports ({fleet})")
        if b["cuda"] != b["torch_cuda"]: notes.append("torch wheel CUDA differs from base CUDA")
        rows.append((proj, tag, b["cuda"], b["status"], "; ".join(notes) or "ok"))
        if notes: problems.append((proj, "; ".join(notes)))
    return rows, problems

if __name__ == "__main__":
    matrix = yaml.safe_load(open(sys.argv[1]))
    rows, problems = check(matrix, sys.argv[2])
    print(f"{'project':<8} {'base':<8} {'cuda':<5} {'status':<11} result")
    for r in rows: print(f"{r[0]:<8} {r[1]:<8} {r[2]:<5} {r[3]:<11} {r[4]}")
    for p, why in problems: print("PROBLEM:", p, "->", why)
    sys.exit(1 if problems else 0)
