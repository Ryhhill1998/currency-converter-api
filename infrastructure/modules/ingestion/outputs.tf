output "data_storage_bucket_id" {
  description = "The name of the data bucket"
  value       = aws_s3_bucket.data_storage_bucket.id
}

output "data_storage_bucket_arn" {
  description = "The ARN of the data bucket"
  value       = aws_s3_bucket.data_storage_bucket.arn
}
