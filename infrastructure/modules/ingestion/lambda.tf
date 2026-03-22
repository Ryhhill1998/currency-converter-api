# resource "aws_lambda_function" "ingestion_lambda" {
#   function_name = "${var.project_name}-ingestion-lambda-${var.environment}"
#   role          = aws_iam_role.ingestion_lambda.arn
#   package_type  = "Image"
#   image_uri     = "${aws_ecr_repository.ingestion_lambda.repository_url}:latest"
#
#   timeout     = 30
#   memory_size = 128
#
#   architectures = ["arm64"]
#
#   lifecycle {
#     ignore_changes = [
#       image_uri,
#     ]
#   }
# }
