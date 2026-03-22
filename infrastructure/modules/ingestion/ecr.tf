resource "aws_ecr_repository" "ingestion_lambda" {
  name                 = "${var.project_name}-ingestion-lambda-${var.environment}"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

data "aws_ecr_lifecycle_policy_document" "ingestion_lambda" {
  rule {
    priority    = 1
    description = "Delete untagged images to save costs"

    selection {
      tag_status      = "untagged"
      count_type      = "imageCountMoreThan"
      count_number    = 1
    }
  }
}

resource "aws_ecr_lifecycle_policy" "ingestion_lambda" {
  repository = aws_ecr_repository.ingestion_lambda.name

  policy = data.aws_ecr_lifecycle_policy_document.ingestion_lambda.json
}
