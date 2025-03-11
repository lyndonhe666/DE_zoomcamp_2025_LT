from datetime import timedelta
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="ny_taxi_dag",
    description="Load data from Yellow Taxi to Postgres",
    start_date=days_ago(1),
    schedule_interval="@daily",
) as dag:
    # download_data = BashOperator(
    #     task_id="download_data",
    #     bash_command=f"curl -o /tmp/yellow_tripdata_{ds}.csv https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{ds}.csv",
    # )

    download_data = BashOperator(
        task_id="print_hello",
        bash_command= "echo hello world"
    )

    end_task = BashOperator(
        task_id="end_task",
        bash_command= "echo end task"
    )

    download_data >> end_task

