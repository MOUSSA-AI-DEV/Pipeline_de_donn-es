

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from src.extraction.youtube_api import extract_youtube_data



with DAG(
    dag_id="youtube_extraction",
    start_date=datetime(2026, 9, 17),
    schedule=None,
    catchup=False,
    tags=["youtube", "extraction"],
) as dag:

    extraction_task = PythonOperator(
        task_id="extract_youtube_data",
        python_callable=extract_youtube_data,
    )

    trigger_dw = TriggerDagRunOperator(
        task_id="trigger_dw_update",
        trigger_dag_id="youtube_dw_update",
        wait_for_completion=False,
    )

    extraction_task >> trigger_dw