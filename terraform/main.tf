locals {
  service_name = "tomboonedotcom"
  site_name = "Tom Boone | Application Developer & DevOps Engineer"
}

data "azurerm_resource_group" "existing" {
  name = var.existing_resource_group_name
}

data "azurerm_service_plan" "existing" {
  name = var.existing_service_plan_name
  resource_group_name = data.azurerm_resource_group.existing.name
}

resource "azurerm_storage_account" "main" {
  name                     = "tomboonedotcomstg"
  resource_group_name      = data.azurerm_resource_group.existing.name
  location                 = data.azurerm_resource_group.existing.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = false
  https_traffic_only_enabled = true
  min_tls_version = "TLS1_2"
  large_file_share_enabled = true
}

resource "azurerm_storage_container" "tbcdata" {
  name                  = "tbcdata"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}

resource "azurerm_linux_web_app" "main" {
  name                = local.service_name
  location            = data.azurerm_resource_group.existing.location
  resource_group_name = data.azurerm_resource_group.existing.name
  service_plan_id     = data.azurerm_service_plan.existing.id

  client_affinity_enabled    = false
  client_certificate_enabled = false
  client_certificate_mode    = "Required"
  https_only                 = true
  public_network_access_enabled = true

  app_settings = {
    "FLASK_SECRET_KEY"              = var.flask_secret_key
    "FLASK_SITE_NAME"               = local.site_name
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "false"
    "SQLALCHEMY_DATABASE_URI"       = "sqlite:////mnt/tbcdata/tbc.db"
  }

  site_config {
    always_on           = true
    ftps_state          = "FtpsOnly"
    http2_enabled       = false
    minimum_tls_version = "1.2"
    scm_minimum_tls_version = "1.2"
    use_32_bit_worker   = true
    worker_count        = 1

    application_stack {
      python_version = "3.13"
    }
  }

  storage_account {
    name         = "tbc-data"
    type         = "AzureBlob"
    account_name = azurerm_storage_account.main.name
    share_name   = azurerm_storage_container.tbcdata.name
    mount_path   = "/mnt/tbcdata"
    access_key   = azurerm_storage_account.main.primary_access_key
  }
}