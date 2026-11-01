"""(1) Does a PyTorchJob's total GPU ask fit a ClusterQueue quota? (2) Why gang scheduling matters."""
import yaml

docs = {d["kind"]: d for d in yaml.safe_load_all(open("train.yaml"))}

def job_gpu_ask(job):
    total = 0
    for name, spec in job["spec"]["pytorchReplicaSpecs"].items():
        per_pod = int(spec["template"]["spec"]["containers"][0]["resources"]["limits"].get("nvidia.com/gpu", 0))
        total += spec["replicas"] * per_pod
        print(f"  {name}: {spec['replicas']} pod(s) x {per_pod} GPU")
    return total

def quota(cq, resource="nvidia.com/gpu"):
    for g in cq["spec"]["resourceGroups"]:
        for f in g["flavors"]:
            for r in f["resources"]:
                if r["name"] == resource: return int(r["nominalQuota"])

ask = job_gpu_ask(docs["PyTorchJob"])
q = quota(docs["ClusterQueue"])
for used in (0, 2, 4):
    free = q - used
    print(f"queue quota {q}, already used {used}, job asks {ask}: " + ("ADMIT" if ask <= free else f"WAIT in queue (short by {ask - free})"))

print("\n--- gang vs no gang: 4 free GPUs, two jobs each need 4 (2 pods x 2 GPUs). Each pod takes 2.")
def run(gang):
    free, jobs = 4, {"A": 2, "B": 2}            # pods still needed per job
    held = {"A": 0, "B": 0}
    if gang:
        for j in jobs:                          # admit a job only if ALL its pods fit
            if jobs[j] * 2 <= free:
                free -= jobs[j] * 2; held[j] = jobs[j]; jobs[j] = 0
    else:
        while free >= 2 and any(jobs.values()):
            for j in jobs:                      # pods trickle in one at a time, alternating
                if jobs[j] and free >= 2:
                    free -= 2; held[j] += 1; jobs[j] -= 1
    running = [j for j in held if held[j] == 2]
    stuck = [j for j in held if 0 < held[j] < 2]
    print(f"gang={gang}: held pods {held}, free GPUs {free}, running {running or 'none'}, stuck-holding {stuck or 'none'}")
run(False); run(True)
