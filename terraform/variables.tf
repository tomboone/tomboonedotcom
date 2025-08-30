variable "existing_resource_group_name" {
  type = string
}

variable "existing_service_plan_name" {
  type = string
}

variable "flask_secret_key" {
  type = string
  sensitive = true
}