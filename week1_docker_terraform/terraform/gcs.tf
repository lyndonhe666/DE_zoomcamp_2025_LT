# GCS Bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "${var.bq_project_name}_data_lake_bucket"
  location      = var.region
  force_destroy = true

  storage_class = "STANDARD"
  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # days
    }
  }
} 