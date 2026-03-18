variable "environment" {
  type        = string
  description = "The environment to which the app should be deployed"

  validation {
    condition     = var.environment == "staging" || var.environment == "production"
    error_message = "Environment must be one of 'staging' or 'production' exactly"
  }
}

variable "project_name" {
  type        = string
  description = "The name of the application"
}
