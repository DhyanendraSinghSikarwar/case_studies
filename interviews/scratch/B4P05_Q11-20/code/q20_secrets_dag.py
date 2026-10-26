import pendulum
import logging

from airflow.sdk import dag, task, Connection, Variable
from airflow.sdk.log import mask_secret


@dag(dag_id="secrets_demo", schedule=None, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def secrets_demo():
    @task
    def use_conn():
        c = Connection.get("warehouse")          # resolved: env var first, then secrets backend, then DB
        print("CONN host=", c.host, "login=", c.login, "type=", c.conn_type)
        print("LEAK_TEST password printed:", c.password)         # masked by Airflow's log masker
        print("LEAK_TEST in f-string:", f"postgresql://{c.login}:{c.password}@{c.host}")
        log = logging.getLogger("airflow.task")
        log.info("LEAK_TEST via logger: password=%s", c.password)
        mask_secret(c.password)                                  # explicit masking
        print("LEAK_TEST after mask_secret print:", c.password)
        log.info("LEAK_TEST after mask_secret logger: password=%s", c.password)
        return c.host                                           # safe value for XCom

    @task
    def use_var():
        api_key = Variable.get("model_api_key")      # name contains 'api_key' -> auto-masked
        plain = Variable.get("region")
        print("LEAK_TEST api key:", api_key, "| region:", plain)

    use_conn() >> use_var()


secrets_demo()
