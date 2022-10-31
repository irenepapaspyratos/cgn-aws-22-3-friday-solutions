S3_BUCKET_NAME=jobs-api-bucket-2022-10-28
if aws s3 ls "s3://$S3_BUCKET_NAME" 2>&1 | grep -q 'An error occurred'
then
    aws s3api create-bucket --bucket $S3_BUCKET_NAME --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
else
    echo "Bucket already exists"
fi