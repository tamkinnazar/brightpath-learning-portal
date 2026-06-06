variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "sa_email" {
  description = "Service account email for Cloud Run"
  type        = string
}

variable "db_user" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_name" {
  type = string
}

variable "vpc_connector" {
  description = "VPC connector name"
  type        = string
}

variable "image_url" {
  description = "Docker image URL for Cloud Run"
  type        = string
}