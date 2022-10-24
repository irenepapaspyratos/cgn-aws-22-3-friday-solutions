import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-west-2'
boto_client_s3 = boto3.client('s3', region_name=AWS_REGION)
boto_resource_s3 = boto3.resource('s3')

def botoCreate_s3Bucket(bucket_name, aws_region=AWS_REGION, client=boto_client_s3, resource=boto_resource_s3):
    if(resource.Bucket(bucket_name)in resource.buckets.all()):
        print('S3 Bucket ' + bucket_name + ' is already existing in region: ' + aws_region)
    else:
        response = client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': aws_region})
        if response['Location'] == 'http://' + bucket_name + '.s3.amazonaws.com/': 
            print('New S3 Bucket ' + bucket_name + ' created in region: ' + aws_region)

def botoUpload_s3Bucket(file_path_local, file_name_remote, bucket_name, client=boto_client_s3):
    response = client.upload_file(file_path_local, bucket_name, file_name_remote)
    if not response: print('File ' + file_name_remote + ' successfully uploaded to ' + bucket_name)
