from datetime import datetime

from airflow import DAG

from airflow.operators.python import PythonOperator

from src.database.load_staging import load_staging
from src.transformation.transform import transform_videos


with DAG(
    dag_id="youtube_dw_update",
    start_date=datetime(2026, 9, 17),
    schedule=None,
    catchup=False,
    tags=["youtube", "datawarehouse"],
) as dag:

    staging_task = PythonOperator(
        task_id="load_staging",
        python_callable=load_staging,
    )

    transformation_task = PythonOperator(
        task_id="transform_and_load_core",
        python_callable=transform_videos,
    )

    staging_task >> transformation_task