# BigQuery Dataset
# resource "google_bigquery_dataset" "dataset" {
#   dataset_id = var.bq_dataset_name
#   project    = var.bq_project_name
#   location   = var.region
#   delete_contents_on_destroy = true
# }

# Example table
# resource "google_bigquery_table" "trips_data_table" {
#   dataset_id = var.bq_dataset_name
#   project    = var.bq_project_name
#   table_id   = "ny_taxi_trips"
#   deletion_protection = false
# } 