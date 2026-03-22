resource "aws_iam_role" "ingestion_lambda" {
  name               = "ingestion_lambda_role"
  assume_role_policy = file("${path.module}/policies/lambda_trust_policy.json")
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.ingestion_lambda.name
}
