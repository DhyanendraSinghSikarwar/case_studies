"""Q22 Azure sweep job offline + the parallel-vs-Bayesian arithmetic (pure Python)."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md
from azure.ai.ml import command
from azure.ai.ml.sweep import Uniform, Choice, BanditPolicy
print("azure-ai-ml", md.version("azure-ai-ml"))
base = command(code=".", command="python train.py --lr ${{inputs.lr}} --depth ${{inputs.depth}}",
               inputs={"lr": 0.1, "depth": 4}, environment="azureml:train-env:1", compute="cpu-cluster")
sw = base(lr=Uniform(min_value=0.001, max_value=0.1), depth=Choice(values=[3, 4, 6])).sweep(
        sampling_algorithm="bayesian", primary_metric="auc", goal="maximize")
sw.set_limits(max_total_trials=20, max_concurrent_trials=4, timeout=3600)
print(type(sw).__name__, "| sampling:", sw.sampling_algorithm, "| goal:", sw.objective.goal, "| metric:", sw.objective.primary_metric)
print("limits: total", sw.limits.max_total_trials, "concurrent", sw.limits.max_concurrent_trials)
print("search space:", {k: type(v).__name__ for k, v in sw.search_space.items()})

# Bandit early termination goes on a random-sampling sweep (docs say Bayesian does not support
# early-termination policies: check current docs).
sw2 = base(lr=Uniform(min_value=0.001, max_value=0.1), depth=Choice(values=[3, 4, 6])).sweep(
        sampling_algorithm="random", primary_metric="auc", goal="maximize")
sw2.set_limits(max_total_trials=20, max_concurrent_trials=4)
sw2.early_termination = BanditPolicy(slack_factor=0.1, evaluation_interval=1, delay_evaluation=2)
print("sweep2:", sw2.sampling_algorithm, "+", type(sw2.early_termination).__name__, "slack", sw2.early_termination.slack_factor)

# Why parallel trials and Bayesian search pull against each other: a Bayesian suggester only learns from
# FINISHED trials. With P trials running at once, trial i (1-based) starts after at most i-P finished.
def informed_trials(total, parallel):
    return [max(0, i - parallel) for i in range(1, total + 1)]   # finished results visible when trial i is proposed
for p in (1, 4, 20):
    seen = informed_trials(20, p)
    print(f"parallel={p:2d}: results seen by trial 5={seen[4]}, trial 10={seen[9]}, trial 20={seen[19]}, trials proposed blind={sum(1 for x in seen if x==0)}")
