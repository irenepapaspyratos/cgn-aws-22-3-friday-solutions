resource "aws_s3_bucket" "bucket_20221021" {
    bucket = "bucket-20221021"
    object_lock_enabled = false
}

resource "aws_s3_bucket_acl" "bucketAcl_20221021" {
    bucket = aws_s3_bucket.bucket_20221021.id
    acl    = "private"
}
