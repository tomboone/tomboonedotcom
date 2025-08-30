output "app_service_name" {
  value       = azurerm_linux_web_app.main.name
  description = "The name of the app service"
}

output "python_version" {
  value       = azurerm_linux_web_app.main.site_config[0].application_stack[0].python_version
  description = "The Python version configured for the app service"
}
