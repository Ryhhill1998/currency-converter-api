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

resource "aws_ecr_lifecycle_policy" "ingestion_lambda" {
  repository = aws_ecr_repository.ingestion_lambda.name
  policy     = file("${path.module}/policies/ecr_lifecycle_policy.json")
}
