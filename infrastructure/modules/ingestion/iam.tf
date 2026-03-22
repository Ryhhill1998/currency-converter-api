resource "aws_iam_role" "lambda_exec" {
  name               = "ingestion-lambda-role"

  # Loads the JSON content from the file
  assume_role_policy = file("${path.module}/policies/lambda-assume-role.json")
}

# Standard execution role for logging (AWS Managed)
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
