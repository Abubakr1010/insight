output "fastapi_url" {
  description = "External URL to access FastAPI app"
  value       = "http://${google_compute_instance.fastapi_vm.network_interface[0].access_config[0].nat_ip}:8080"
}