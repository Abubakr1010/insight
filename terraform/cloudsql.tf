resource "google_sql_database_instance" "insight" {
  name             = "insight-db"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled = true

      authorized_networks {
        name  = "allow-all-temp"
        value = "0.0.0.0/0" 
      }
    } 

    backup_configuration {
      enabled = true
    }
  }

  deletion_protection = false
}

# Database inside the instance
resource "google_sql_database" "insight" {
  name     = var.db_name
  instance = google_sql_database_instance.insight.name
}

# DB user
resource "google_sql_user" "insight" {
  name     = var.db_user
  password = var.db_password
  instance = google_sql_database_instance.insight.name
}

output "cloudsql_public_ip" {
  value = google_sql_database_instance.insight.public_ip_address
}