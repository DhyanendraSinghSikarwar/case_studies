import os, warnings, json, tempfile
os.environ["NO_GCE_CHECK"] = "True"
warnings.filterwarnings("ignore")
import kfp, google.cloud.aiplatform as aip
from kfp import dsl, compiler, local
from google.auth.credentials import AnonymousCredentials
print("kfp", kfp.__version__, "| google-cloud-aiplatform", aip.__version__)

@dsl.component(base_image="python:3.11")
def prep(n: int, out: dsl.Output[dsl.Dataset]):
    open(out.path, "w").write(str(n))
@dsl.component(base_image="python:3.11")
def train(d: dsl.Input[dsl.Dataset], m: dsl.Output[dsl.Model], lr: float = 0.1):
    open(m.path, "w").write("model")
@dsl.pipeline(name="churn-pipe", pipeline_root="gs://fake-bucket-name/pipeline-root")
def pl(n: int = 5, lr: float = 0.1):
    p = prep(n=n)
    train(d=p.outputs["out"], lr=lr).set_cpu_limit("2").set_memory_limit("4G")

work = tempfile.mkdtemp()
js, ym = os.path.join(work, "pipe.json"), os.path.join(work, "pipe.yaml")
compiler.Compiler().compile(pl, js); compiler.Compiler().compile(pl, ym)
spec = json.load(open(js))
print("top-level sections:", sorted(spec))
print("pipelineInfo:", spec["pipelineInfo"])
print("defaultPipelineRoot:", spec["defaultPipelineRoot"])
print("root DAG tasks:", list(spec["root"]["dag"]["tasks"]))
print("train depends on:", spec["root"]["dag"]["tasks"]["train"]["dependentTasks"])
print("root input parameters:", spec["root"]["inputDefinitions"]["parameters"])
print("executors:", list(spec["deploymentSpec"]["executors"]))
print("YAML compiled too, first line:", open(ym).read().splitlines()[0])

aip.init(project="fake-project", location="asia-south1", credentials=AnonymousCredentials())
pj = aip.PipelineJob(display_name="churn-pipe", template_path=js, parameter_values={"n": 3, "lr": 0.05},
                     enable_caching=False, labels={"team": "ml"})
print("PipelineJob built offline:", type(pj).__name__, "| pipeline_root:", pj.pipeline_spec["defaultPipelineRoot"])
print("submit(): NOT called (it would go to the regional Vertex API).")

# local run of one component: no service, no GCS, subprocess on this machine
local.init(runner=local.SubprocessRunner(), pipeline_root=os.path.join(work, "local_root"))
@dsl.component
def add(a: int, b: int) -> int:
    return a + b
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    t = add(a=1, b=2)
print("runner log lines hidden:", len(buf.getvalue().splitlines()), "| task status line:", [l.strip() for l in buf.getvalue().splitlines() if "finished with status" in l][0].split(" - ")[-1].replace("\x1b[96m","").replace("\x1b[0m","").replace("\x1b[92m",""))
print("kfp.local SubprocessRunner result:", t.output)
