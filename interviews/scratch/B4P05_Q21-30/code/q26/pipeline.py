from typing import List
from kfp import compiler, dsl
from kfp import kubernetes


@dsl.component(base_image="python:3.12")
def train(lr: float) -> float:
    # toy "validation score": best near lr=0.01
    return round(1.0 - abs(lr - 0.01) * 10, 3)


@dsl.component(base_image="python:3.12")
def pick_best(scores: List[float]) -> float:
    return max(scores)


@dsl.component(base_image="python:3.12")
def deploy(score: float):
    print("deploying model with score", score)


@dsl.component(base_image="python:3.12")
def cleanup():
    print("always runs: delete scratch data")


@dsl.pipeline(name="train-select-deploy")
def train_select_deploy(lrs: List[float] = [0.1, 0.01, 0.001], min_score: float = 0.8):
    exit_task = cleanup()
    with dsl.ExitHandler(exit_task):
        with dsl.ParallelFor(items=lrs, parallelism=2) as lr:
            t = train(lr=lr)
            t.set_cpu_limit("2").set_memory_limit("4G")
            t.set_accelerator_type("NVIDIA_TESLA_T4").set_accelerator_limit(1)
            kubernetes.add_node_selector(t, label_key="pool", label_value="gpu")
            kubernetes.add_toleration(t, key="nvidia.com/gpu", operator="Exists", effect="NoSchedule")
            kubernetes.use_secret_as_env(t, secret_name="wandb-key", secret_key_to_env={"api_key": "WANDB_API_KEY"})
        best = pick_best(scores=dsl.Collected(t.output))
        with dsl.If(best.output >= min_score):
            deploy(score=best.output)


if __name__ == "__main__":
    compiler.Compiler().compile(train_select_deploy, "pipeline.yaml")
    print("compiled pipeline.yaml")
