from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def test_airflow():
    print("Airflow fonctionne !")


with DAG(
    dag_id="youtube_pipeline",
    start_date=datetime(2026, 9, 16),
    schedule=None,
    catchup=False,
    tags=["youtube"],
      params={},
) as dag:

    test_task = PythonOperator(
        task_id="test_airflow",
        python_callable=test_airflow,
    )