variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  default     = "us-central1-a"
}

# ---------------------------
# Database variables
# ---------------------------
variable "db_name" {
  description = "Postgres database name"
  default     = "insight"
}

variable "db_user" {
  description = "Postgres username"
  default     = "insight_user"
}

variable "db_password" {
  description = "Postgres password"
  type        = string
  sensitive   = true
}

