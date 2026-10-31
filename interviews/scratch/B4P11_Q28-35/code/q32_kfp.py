# q32_kfp.py - compile a KFP pipeline once, inspect the spec. Offline: no submit.
import sys, warnings; warnings.filterwarnings("ignore")
import kfp, yaml
from kfp import dsl, compiler
@dsl.component(base_image="python:3.11")
def train(lr: float, model: dsl.Output[dsl.Model]):
    open(model.path, "w").write(f"lr={lr}")
@dsl.pipeline(name="portable-train")
def pipe(lr: float = 0.1):
    train(lr=lr)
out = sys.argv[1]
compiler.Compiler().compile(pipe, out)
spec = yaml.safe_load(open(out))
print("kfp", kfp.__version__)
print("top-level keys:", sorted(spec))
print("schemaVersion:", spec["schemaVersion"], "| pipeline:", spec["pipelineInfo"]["name"])
ex = spec["deploymentSpec"]["executors"]["exec-train"]["container"]
print("executor image:", ex["image"], "| args[0..1]:", ex["args"][:2])
print("cloud-specific strings in spec:", [k for k in ("aiplatform", "googleapis", "sagemaker", "azureml") if k in open(out).read()])
