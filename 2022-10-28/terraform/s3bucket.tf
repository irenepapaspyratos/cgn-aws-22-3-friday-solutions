resource "aws_s3_bucket" "jobs-api" {
  bucket = "jobs-api-bucket-2022-10-21"
  tags = {
    Description = "Bucket for jobs api"
  }
}
resource "aws_s3_bucket_object" "jobs-api-script" {
  content = "jobs-api/job_api.py"
  key = "jobs_api.py"
  bucket = aws_s3_bucket.jobs-api.id
}