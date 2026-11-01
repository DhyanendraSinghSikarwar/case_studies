import os, sys, tempfile, yaml
home = tempfile.mkdtemp(prefix="q35home_", dir="/tmp/claude-0/b5p05_q31_40")
os.environ.update(AIRFLOW_HOME=home, AIRFLOW__CORE__LOAD_EXAMPLES="False")
here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.environ["K8S_PROVIDER_DIR"])        # provider unpacked outside the Airflow venv
pod = yaml.safe_load(open(os.path.join(here, "q35_pod_template.yaml")))
c = pod["spec"]["containers"][0]
print("pod yaml parses: kind =", pod["kind"], "| container =", c["name"], "| gpu limit =", c["resources"]["limits"]["nvidia.com/gpu"])
from airflow.models.dagbag import DagBag
bag = DagBag(dag_folder=os.path.join(here, "q35_dags"))
print("import_errors:", bag.import_errors)
d = bag.dags["train_gpu"]
for t in d.tasks: print(" task", t.task_id, type(t).__name__)
k = d.get_task("train")
print(" train gpu limit:", k.container_resources.limits["nvidia.com/gpu"], "| namespace:", k.namespace)
