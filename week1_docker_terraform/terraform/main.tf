terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.21.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials) 
  project     = var.project
  region      = var.region
} 