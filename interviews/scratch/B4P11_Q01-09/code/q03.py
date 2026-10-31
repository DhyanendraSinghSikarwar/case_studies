import os, warnings, tempfile, json
os.environ["NO_GCE_CHECK"] = "True"      # do not probe the GCE metadata server
for k in ("GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_CLOUD_PROJECT"):
    os.environ.pop(k, None)
warnings.filterwarnings("ignore")
import google.cloud.aiplatform as aip, kfp
from kfp import dsl, compiler
from google.auth.credentials import AnonymousCredentials
print("google-cloud-aiplatform", aip.__version__, "| kfp", kfp.__version__)

@dsl.component(base_image="python:3.11")
def hello(x: int) -> int:
    return x + 1
@dsl.pipeline(name="demo", pipeline_root="gs://fake-bucket-name/root")
def pl(x: int = 1):
    hello(x=x)
d = tempfile.mkdtemp()
tpl = os.path.join(d, "demo.json")
compiler.Compiler().compile(pl, tpl)

def attempt(label, fn):
    try:
        fn(); print(label, "-> built")
    except Exception as e:
        print(label, "->", type(e).__name__ + ":", str(e).replace("\n", " ")[:120])

mk_pj = lambda **kw: aip.PipelineJob(display_name="x", template_path=tpl, pipeline_root="gs://fake-bucket-name/r", **kw)
attempt("1. no init, PipelineJob", mk_pj)
aip.init(project="fake-project", location="asia-south1", staging_bucket="gs://fake-bucket-name")
print("2. init(project, location, staging_bucket) ok:", aip.initializer.global_config.project,
      aip.initializer.global_config.location, aip.initializer.global_config.staging_bucket)
attempt("3. init without creds, PipelineJob", mk_pj)
aip.init(project="fake-project", location="asia-south1", staging_bucket="gs://fake-bucket-name",
         credentials=AnonymousCredentials())
attempt("4. init + AnonymousCredentials, PipelineJob", mk_pj)
cj = lambda: aip.CustomJob(display_name="cj", worker_pool_specs=[{"machine_spec": {"machine_type": "n1-standard-4"},
     "replica_count": 1, "container_spec": {"image_uri": "gcr.io/fake/i:1"}}])
attempt("5. init + AnonymousCredentials, CustomJob", cj)
print("6. regional API host the client would call:", f"{aip.initializer.global_config.location}-aiplatform.googleapis.com", "(string only, not contacted)")
print("7. submit(): NOT called here. It would send the job to that host and, with anonymous credentials, be rejected (401).")
