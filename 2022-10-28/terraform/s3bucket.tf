resource "aws_s3_bucket" "jobs-api" {
  bucket = "jobs-ee"
  
  tags = {
    Description = "Bucket for jobs api"
  }
}

resource "aws_s3_bucket_object" "jobs-api-script" {
  content = "jobs-api/ZIP"
  key = "jobs_api.py"
  bucket = aws_s3_bucket.jobs-api.id
}
