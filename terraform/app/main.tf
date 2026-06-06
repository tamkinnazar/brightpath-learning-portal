terraform {
  required_version = ">= 1.0"
}

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

      env {
        name  = "DB_USER"
        value = var.db_user
      }

      env {
        name  = "DB_PASSWORD"
        value = var.db_password
      }

      env {
        name  = "DB_NAME"
        value = var.db_name
      }

      env {
        name  = "DB_CONNECTION_NAME"
        value = var.db_connection_name
      }

      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }
    }
  }

traffic {
  percent = 100
  type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
}
}