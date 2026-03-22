resource "aws_s3_bucket" "data_storage_bucket" {
  bucket = "${var.project_name}_data_storage_bucket_${var.environment}"

  tags = {
    Name = "Data Storage Bucket"
  }
}
