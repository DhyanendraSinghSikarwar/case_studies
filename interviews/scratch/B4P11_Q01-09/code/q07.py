import warnings; warnings.filterwarnings("ignore")
import azure.ai.ml as m
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration, Environment
print("azure-ai-ml", m.__version__)

ep = ManagedOnlineEndpoint(name="churn-ep", auth_mode="key", description="offline entity")
env = Environment(name="sk", version="1", image="mcr.microsoft.com/azureml/minimal-ubuntu22.04-py311-cpu-inference:latest")
blue = ManagedOnlineDeployment(name="blue", endpoint_name="churn-ep", model="azureml:churn-model:1", environment=env,
        code_configuration=CodeConfiguration(code=".", scoring_script="score.py"), instance_type="Standard_DS3_v2", instance_count=1)
green = ManagedOnlineDeployment(name="green", endpoint_name="churn-ep", model="azureml:churn-model:2",
        instance_type="Standard_DS3_v2", instance_count=1)   # MLflow model: no scoring script, no environment
print("endpoint:", ep.name, "auth_mode =", ep.auth_mode)
print("blue  (custom scoring):", blue.code_configuration.scoring_script, "| env:", blue.environment.name)
print("green (MLflow no-code): scoring script =", green.code_configuration, "| env =", green.environment)

def check_traffic(traffic, existing):
    """Same rules the answer states: only known deployments, 0-100 each, total 0 or 100."""
    unknown = set(traffic) - set(existing)
    if unknown:
        raise ValueError(f"deployments not created yet: {sorted(unknown)}")
    if any(not 0 <= v <= 100 for v in traffic.values()):
        raise ValueError("each share must be 0..100")
    total = sum(traffic.values())
    if total not in (0, 100):
        raise ValueError(f"traffic must sum to 0 or 100, got {total}")
    return True

existing = ["blue"]
cases = [("only blue", {"blue": 100}, existing),
         ("canary before green exists", {"blue": 90, "green": 10}, existing),
         ("canary after green exists", {"blue": 90, "green": 10}, ["blue", "green"]),
         ("sums to 95", {"blue": 85, "green": 10}, ["blue", "green"]),
         ("all zero (pause)", {"blue": 0, "green": 0}, ["blue", "green"])]
for label, t, ex in cases:
    try:
        print(f"{label:28}", t, "->", check_traffic(t, ex))
    except ValueError as e:
        print(f"{label:28}", t, "-> REJECT:", e)
ep.traffic = {"blue": 90, "green": 10}
print("entity holds traffic map:", ep.traffic, "(the service, not the entity, enforces the rule)")
