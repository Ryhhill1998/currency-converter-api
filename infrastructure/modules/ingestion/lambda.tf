# resource "aws_lambda_function" "ingestion_lambda" {
#   function_name = "${var.project_name}-ingestion-${var.environment}"
#   role          = aws_iam_role.ingestion_lambda.arn
#
#   package_type  = "Image"
#   image_uri     = "${aws_ecr_repository.ingestion_lambda.repository_url}:latest"
#
#   environment {
#     variables = {
#       S3_BUCKET_NAME = aws_s3_bucket.data_storage_bucket.id
#     }
#   }
# }
