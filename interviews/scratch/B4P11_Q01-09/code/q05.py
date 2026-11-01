import warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml.entities import AmlCompute, ComputeInstance
print("azure-ai-ml", m.__version__)

cluster = AmlCompute(name="gpu-nightly", size="Standard_NC6s_v3", min_instances=0, max_instances=2,
                     idle_time_before_scale_down=300, tier="dedicated")
assert cluster.min_instances == 0, "scale to zero needs min 0"
assert cluster.max_instances >= 1
assert cluster.idle_time_before_scale_down == 300
print("cluster:", cluster.name, cluster.type, cluster.size, "min", cluster.min_instances, "max", cluster.max_instances,
      "idle_s", cluster.idle_time_before_scale_down, "tier", cluster.tier)

ci = ComputeInstance(name="dev-asha", size="Standard_DS3_v2", idle_time_before_shutdown_minutes=60)
print("instance:", ci.name, ci.type, ci.size, "idle shutdown min", ci.idle_time_before_shutdown_minutes)

def pick(workload):
    """Toy rule used in the answer; the real inputs are your quota and team habits."""
    if workload["interactive"]:
        return "compute instance (one user, idle shutdown on)"
    if workload["duration_h"] >= 1 and workload["gpu"] and workload["runs_per_day"] <= 1:
        return "compute cluster min=0 (or serverless if quota is pooled and you want no cluster to manage)"
    if workload["runs_per_day"] > 24:
        return "cluster with min>0 (warm nodes) to avoid repeated start-up"
    return "serverless compute"
for w in ({"interactive": True, "gpu": False, "duration_h": 8, "runs_per_day": 1},
          {"interactive": False, "gpu": True, "duration_h": 4, "runs_per_day": 1},
          {"interactive": False, "gpu": False, "duration_h": 0.1, "runs_per_day": 100}):
    print(w, "->", pick(w))

# a bad config is caught only by our own check; the entity itself accepts it offline
bad = AmlCompute(name="oops", size="Standard_NC6s_v3", min_instances=2, max_instances=1)
print("entity accepts min>max offline:", bad.min_instances, bad.max_instances, "| our check:", "min <= max" if bad.min_instances <= bad.max_instances else "REJECT min>max")
