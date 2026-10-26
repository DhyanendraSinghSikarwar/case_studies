import pendulum
from airflow.sdk import dag, task
from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.secret import Secret

db_pw = Secret(deploy_type="env", deploy_target="DB_PASSWORD", secret="ml-db", key="password")

@dag(dag_id="train_gpu", schedule=None, start_date=pendulum.datetime(2026, 1, 1), catchup=False,
     tags=["ml", "k8s"], default_args={"owner": "ml-platform", "retries": 1})
def train_gpu():
    train = KubernetesPodOperator(
        task_id="train",
        name="train-pod",
        namespace="ml-jobs",
        image="registry.example.com/ml/train:1.4.2",      # pinned tag (ideally a digest)
        cmds=["python", "-m", "train"],
        arguments=["--run-date", "{{ ds }}", "--out", "/out/result.json"],
        env_vars={"MODEL_NAME": "ranker"},
        secrets=[db_pw],                                    # mounted from a k8s Secret, not in the DAG
        container_resources=k8s.V1ResourceRequirements(
            requests={"cpu": "4", "memory": "16Gi"},
            limits={"memory": "16Gi", "nvidia.com/gpu": "1"}),
        node_selector={"pool": "gpu"},
        tolerations=[k8s.V1Toleration(key="nvidia.com/gpu", operator="Exists", effect="NoSchedule")],
        get_logs=True,                                      # stream container stdout into the task log
        do_xcom_push=True,                                  # reads /airflow/xcom/return.json via a sidecar
        on_finish_action="delete_pod",
        startup_timeout_seconds=600,
    )

    @task.virtualenv(requirements=["numpy==2.1.0"], system_site_packages=False)
    def small_check():
        import numpy as np
        return float(np.arange(3).sum())
    train >> small_check()
train_gpu()
