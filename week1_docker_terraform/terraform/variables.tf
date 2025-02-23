variable "credentials" {
  description = "Path to the service account credentials file"
  default     = "./terraform_SA_credentials.json"
}

variable "project" {
  description = "GCP Project ID"
  default     = "LT-de-zoomcamp-2025"
}

variable "bq_project_name" {
  description = "bigquery project name, lower case"
  default     = "lt-de-zoomcamp-2025"
}

variable "region" {
  description = "Region for GCP resources"
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "trips_data_all"
} 