import corona_script
import boto_script


# Needed variables
urlBase = 'https://api.covid19api.com'
urlVariable = '/country/germany?from=2020-10-14T00:00:00Z&to=2020-10-21T00:00:00Z'
url = urlBase + urlVariable
file_nameLocal = 'corona-data.json'
file_path_toSave = './' + file_nameLocal

aws_region = 'us-west-2'
bucket_name = 'corona-bucket-20221021'
file_pathLocal = file_path_toSave # if pathToFile not known, import os & pathlib and use this: os.path.join(pathlib.Path(__file__).parent.resolve(), file_nameLocal)
file_nameRemote = file_nameLocal


# Task 1
# ---------------------------
# Done via Terminal

# Task 2
# ---------------------------
# 2.1 + 2.2
corona_script.saveJsonFileLocal(file_path_toSave, url)

# 2.3
boto_script.botoCreate_s3Bucket(bucket_name, aws_region)
boto_script.botoUpload_s3Bucket(file_pathLocal, file_nameRemote, bucket_name)

# Task 3
# ---------------------------
# Done via Terraform project -> use terraform apply with -auto-approve for pipeline
# ToDo: get Script, run cron

# Task 4
# ---------------------------
# ToDo via .github/workflows
