module "ingestion" {
  source       = "./ingestion"
  environment  = var.environment
  project_name = var.project_name
}
