terraform {
  required_version = "~> 1.14.0"

  backend "s3" {
    bucket       = "currency-converter-api-tfstate-756316131141-eu-west-1-an"
    key          = "production/terraform.tfstate"
    region       = "eu-west-1"
    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

locals {
  environment  = "production"
  project_name = "currency-converter-api"
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Application = local.project_name
      Environment = local.environment
    }
  }
}
