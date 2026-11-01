import sys
from pathlib import Path

import pytest
from airflow.dag_processing.dagbag import DagBag

DAGS = Path(__file__).resolve().parents[1] / "dags"
sys.path.insert(0, str(DAGS))


@pytest.fixture(scope="session")
def bag():
    return DagBag(dag_folder=str(DAGS))   # Airflow 3: no include_examples argument


def test_no_import_errors(bag):
    assert bag.import_errors == {}


def test_expected_dag_and_tasks(bag):
    dag = bag.get_dag("good_train")
    assert sorted(dag.task_ids) == ["extract", "train"]
    assert dag.tags and "ml" in dag.tags


@pytest.mark.parametrize("dag_id", ["good_train", "bad_no_retries"])
def test_every_task_has_retries(bag, dag_id):
    dag = bag.get_dag(dag_id)
    missing = [t.task_id for t in dag.tasks if (t.retries or 0) < 1]
    assert not missing, f"{dag_id}: tasks without retries: {missing}"


def test_plain_function_logic():
    from good_dag import clean_rows
    assert clean_rows([1, None, -2, 3]) == [1, 3]
