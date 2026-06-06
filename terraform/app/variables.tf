variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "image_url" {
  description = "Docker image URL for Cloud Run"
  type        = string
}

variable "sa_email" {
  type = string
}

variable "db_name" {
  type    = string
  default = "appdb"
}

variable "vpc_connector" {
  type    = string
  default = "cis410-connector"
}