# usage: source env.sh N
export AIRFLOW_HOME=/tmp/claude-0/b5p05_q1_10/q$1/home
export AIRFLOW__CORE__DAGS_FOLDER=/tmp/claude-0/b5p05_q1_10/q$1/dags
export AIRFLOW__CORE__LOAD_EXAMPLES=False
mkdir -p $AIRFLOW_HOME $AIRFLOW__CORE__DAGS_FOLDER
export PATH=/tmp/claude-0/b5p05/af/bin:$PATH
