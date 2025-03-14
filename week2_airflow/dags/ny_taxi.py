from datetime import timedelta, datetime
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import os
from dateutil.relativedelta import relativedelta
import pandas as pd

# get the environment variables
GCP_GCS_BUCKET = os.getenv("GCP_GCS_BUCKET")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")


def generate_date_string(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    current_date = start_date

    while current_date <= end_date:
        yield current_date.strftime("%Y-%m")
        current_date += relativedelta(months=1)

base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_"
start_date = "2021-04-01"
end_date = "2021-07-01"
source_urls = [base_url + date_month + ".csv.gz" for date_month in generate_date_string(start_date, end_date)]


def format_parquet_file(source_file, output_file):
    df = pd.read_csv(source_file)
    df.to_parquet(output_file, engine="pyarrow")


with DAG(
    dag_id="ny_taxi_dag",
    description="Load data from Yellow Taxi to Google Bigquery",
    start_date=days_ago(1),
    schedule_interval="@daily",
) as dag:
    
    for ds in generate_date_string(start_date, end_date):
        download_data = BashOperator(
            task_id=f"download_data_{ds}",
            bash_command=f"curl -o /tmp/yellow_tripdata_{ds}.csv https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{ds}.csv",
    )

        ingest_data = PythonOperator(
            task_id=f"ingest_data_{ds}",
            python_callable=format_parquet_file,
            op_args=[f"/tmp/yellow_tripdata_{ds}.csv", f"/tmp/yellow_tripdata_{ds}.parquet"]
        )
    
        upload_data = BashOperator(
            task_id=f"upload_data_{ds}",
            bash_command=f"gcloud storage cp /tmp/yellow_tripdata_{ds}.csv gs://{GCP_GCS_BUCKET}/raw/yellow_tripdata_{ds}.csv"
        )

        create_table = BigQueryCreateExternalTableOperator(
            task_id=f"create_table_{ds}",
            table_resource={
                "tableReference": {
                    "projectId": GCP_PROJECT_ID,
                    "datasetId": "ny_taxi",
                    "tableId": f"yellow_taxi_{ds}"
                },
                "externalDataConfiguration": {
                    "sourceFormat": "CSV",
                    "sourceUris": [f"gs://{GCP_GCS_BUCKET}/raw/yellow_tripdata_{ds}.csv"],
                    "schema": {
                        "fields": [
                            {"name": "VendorID", "type": "INTEGER"},
                            {"name": "tpep_pickup_datetime", "type": "TIMESTAMP"},
                            {"name": "tpep_dropoff_datetime", "type": "TIMESTAMP"},
                            {"name": "passenger_count", "type": "INTEGER"},
                            {"name": "trip_distance", "type": "FLOAT"},
                            {"name": "RatecodeID", "type": "INTEGER"},
                            {"name": "store_and_fwd_flag", "type": "STRING"},
                            {"name": "PULocationID", "type": "INTEGER"},
                            {"name": "DOLocationID", "type": "INTEGER"},
                            {"name": "payment_type", "type": "INTEGER"},
                            {"name": "fare_amount", "type": "FLOAT"},
                            {"name": "extra", "type": "FLOAT"},
                            {"name": "mta_tax", "type": "FLOAT"},
                            {"name": "tip_amount", "type": "FLOAT"},
                            {"name": "tolls_amount", "type": "FLOAT"},
                            {"name": "improvement_surcharge", "type": "FLOAT"},
                            {"name": "total_amount", "type": "FLOAT"},
                            {"name": "congestion_surcharge", "type": "FLOAT"}
                        ]
                    }
                }
            }
        )

        download_data >> ingest_data >> upload_data >> create_table