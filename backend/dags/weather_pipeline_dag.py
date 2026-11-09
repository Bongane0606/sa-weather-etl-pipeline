from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "sa-weather-etl",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sa_weather_etl_pipeline",
    description="Extract -> transform -> validate -> load SA weather data",
    default_args=default_args,
    schedule="0 */6 * * *",  # every 6 hours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["weather", "etl"],
) as dag:

    run_pipeline = BashOperator(
        task_id="run_weather_pipeline",
        # Reuses the exact same pipeline.py your Docker app service already runs --
        # nothing pipeline-specific lives in the DAG itself.
        bash_command="cd /opt/airflow/weather_etl && python pipeline.py",
    )