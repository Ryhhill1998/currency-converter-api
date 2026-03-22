resource "aws_lambda_function" "ingestion_lambda" {
  function_name = "ingestion-service"
  role          = aws_iam_role.lambda_role.arn
  
  package_type  = "Image"
  
  # Reference the repo you already have in ecr.tf
  image_uri     = "${aws_ecr_repository.ingestion_lambda.repository_url}:latest"

  timeout     = 30
  memory_size = 128
}
