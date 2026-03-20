module "infrastructure" {
  source = "../../modules"

  environment  = local.environment
  project_name = local.project_name
}
