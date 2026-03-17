terraform {
  required_version = "~> 1.14.0"

  backend "s3" {
    bucket       = "currency-exchange-terraform-state"
    key          = "staging/terraform.tfstate"
    region       = "us-west-1"
    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
