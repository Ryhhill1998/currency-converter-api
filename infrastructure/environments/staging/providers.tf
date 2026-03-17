terraform {
  required_version = "~> 1.14.0"

  backend "s3" {
    bucket       = "currency-exchange-terraform-state"
    key          = "staging/terraform.tfstate"
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
  environment  = "staging"
  project_name = "currency-exchange-api"
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
