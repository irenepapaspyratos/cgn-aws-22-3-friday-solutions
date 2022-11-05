#!/bin/bash

# Update linux
yum update -y

# Copy python files from bucket
S3_BUCKET_NAME=jobs-api-bucket-2022-10-28
aws s3 cp "s3://jobs-api-bucket-2022-10-28/api-server.zip" api-server.zip
unzip api-server.zip

# Install python modules
python3 -m pip install -r requirements.txt