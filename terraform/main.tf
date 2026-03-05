resource "google_compute_instance" "fastapi_vm" {
  name         = "fastapi-vm"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  tags = ["fastapi"]

  metadata_startup_script = <<EOF
#!/bin/bash
set -e

# Update and install Docker
apt-get update
apt-get install -y docker.io
systemctl start docker
systemctl enable docker

# Wait a few seconds to ensure Docker is ready
sleep 5

# Pull the latest Docker image
docker pull abubakr1010/insight-app:latest

# Stop existing container if exists
if [ $(docker ps -q -f name=fastapi-app) ]; then
    docker stop fastapi-app
    docker rm fastapi-app
fi

# Run the FastAPI container
docker run -d --name fastapi-app -p 8080:6000 abubakr1010/insight-app:latest
EOF
}