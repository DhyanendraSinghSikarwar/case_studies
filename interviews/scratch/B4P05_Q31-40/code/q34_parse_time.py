"""Time DagBag parsing of N generated DAG files. Run with the Airflow venv python."""
import os, sys, tempfile, time, pathlib
home = tempfile.mkdtemp(prefix="q34home_", dir="/tmp/claude-0/b5p05_q31_40")
os.environ.update(AIRFLOW_HOME=home, AIRFLOW__CORE__LOAD_EXAMPLES="False")
TEMPLATE = '''import pendulum
{heavy}
from airflow.sdk import dag, task

@dag(dag_id="gen_{i}", schedule="@daily", start_date=pendulum.datetime(2026, 1, 1), catchup=False, tags=["gen"])
def gen_{i}():
    @task
    def a(): return 1
    @task
    def b(x): return x
    @task
    def c(x): return x
    c(b(a()))
gen_{i}()
'''
def make(n, heavy=""):
    d = pathlib.Path(tempfile.mkdtemp(prefix="dags_", dir="/tmp/claude-0/b5p05_q31_40"))
    for i in range(n):
        (d / f"gen_{i}.py").write_text(TEMPLATE.format(i=i, heavy=heavy))
    return d
from airflow.models.dagbag import DagBag
DagBag(dag_folder=str(make(1)))            # warm-up: pays the one-off import cost
for label, n, heavy in [("10 light files", 10, ""), ("500 light files", 500, ""),
                        ("10 files, 0.2 s top-level sleep each", 10, "import time; time.sleep(0.2)")]:
    d = make(n, heavy)
    t = time.perf_counter(); bag = DagBag(dag_folder=str(d)); dt = time.perf_counter() - t
    print(f"{label:40s} dags={len(bag.dags):4d} errors={len(bag.import_errors)} total={dt:6.2f}s per_file={dt/n*1000:7.1f}ms")
