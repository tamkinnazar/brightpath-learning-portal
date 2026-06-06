terraform {
  required_version = ">= 1.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# =========================
# INFRA REMOTE STATE
# =========================
data "terraform_remote_state" "infra" {
  backend = "gcs"
  config = {
    bucket = "cis410-nandar-tfstate"
    prefix = "terraform/infrastructure"
  }
}

# =========================
# CLOUD RUN SERVICE
# =========================
resource "google_cloud_run_v2_service" "app" {
  name     = "brightpath-app"
  location = var.region

  template {
    service_account = var.sa_email

    containers {
      image = var.image_url

      ports {
        container_port = 8080
      }

      # Standard App Config via Remote State
      env {
        name  = "DB_CONNECTION_NAME"
        value = data.terraform_remote_state.infra.outputs.db_connection_name
      }

      env {
        name  = "DB_NAME"
        value = var.db_name
      }

      env {
        name  = "BUCKET_NAME"
        value = data.terraform_remote_state.infra.outputs.bucket_name
      }

      # Secure Secrets References directly from GCP Secret Manager
      env {
        name = "DB_USER"
        value_source {
          secret_key_ref {
            secret  = "db_user" # Must match the secret ID in Secret Manager
            version = "latest"
          }
        }
      }

      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = "db-password" # Must match the secret ID in Secret Manager
            version = "latest"
          }
        }
      }
    }

    vpc_access {
      connector = "projects/${var.project_id}/locations/${var.region}/connectors/${var.vpc_connector}"
      egress    = "ALL_TRAFFIC"
    }
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
}

# PUBLIC ACCESS
resource "google_cloud_run_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  service  = google_cloud_run_v2_service.app.name

  role   = "roles/run.invoker"
  member = "allUsers"
}