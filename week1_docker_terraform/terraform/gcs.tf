# GCS Bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name          = "data_lake_bucket_test"
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