# Solution for Challenge of 04.11.2022

## Task 1.1

-   start lab, update credentials, download .pem and give permissions

-   in terminal:

    ```
    aws s3api create-bucket \
        --bucket ip-lamda-bucket \
        --region us-west-2 \
        --create-bucket-configuration  LocationConstraint=us-west-2
    ```

## Task 1.2

-   create a .zip of requests to import in layer for lambda by executing the following commands one after another:

    ```bash
    mkdir python
    cd python
    pip3 install requests -t .
    cd ..
    zip -r requests_layer.zip python
    rm -rf python
    ```

-   update .gitignore with FOLDERNAME/\*.zip

-   in AWS Console go to  
     Services > Lambda > Create function

-   create a new function (in AWS Console go to Services > Lambda > Create function) from scratch with

    -   latest python available
    -   x86_64
    -   Use an existing role: LabRole

-   create a new layer (Services > Lambda > Layers > Create layer) by uploading requests_layer.zip with x86_64 and everything else as is - except name and description of course

-   on the lambda-dashboard select the desired lambda and add the new created custom layer to it

-   set a sufficient time-out in the configuration-tab of the lambda

-   replace the default lambda-code with one that does the job of the task -> in the following function also including a pagination (here limited to 5) and the return of a json-object with successfully saved or failed-to-saved jobs:

    ```py
    import json
    import requests
    import boto3

    api_url = "https://www.arbeitnow.com/api/job-board-api?page="

    def get_json(urlVar):
        try:
            res = requests.get(urlVar)
            return res.json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def create_job(singleJsonObject):
        return {
            "id": singleJsonObject["slug"],
            "title": singleJsonObject["title"],
            "description": singleJsonObject["description"]
        }

    def save_job(jsonJob):
        s3_client = boto3.client('s3')
        #object = s3_client.Object('ip-lamda-bucket', jsonJob['id']+'.json')
        #object.put(Body=jsonJob)
        return s3_client.put_object(Body=json.dumps(jsonJob), Bucket='ip-lamda-bucket', Key=jsonJob['id']+'.json')

    def lambda_handler(event, context):
        result_array = {"saved": [], "failed": []}
        page = '1'
        while True:
            json = get_json(api_url + page)
            jobsArray = json["data"]
            for job in jobsArray:
                try:
                    jobJson = create_job(job)
                    save_job(jobJson)
                    result_array['saved'].append(jobJson)
                except:
                    result_array['saved'].append(job)

            if json['links']['next'] and int(page) < 5:
                page = str(int(page) + 1)
            else:
                break
        return result_array
    ```

## Task 2.1

-   online: fork the given repo

## Task 2.2

-   clone the forked repo locally

-   create new branch and checkout to it

## Task 2.3

-   in setup_src_bucket.sh, upload-src.sh and infrastructure > script > userdata.sh replace the srcBucket-name with a personal one

-   do add & commit

-   in setup_terraform_bucket.sh and infrastructure > main.tf replace the terraformBucket-name with a personal one

-   do add & commit

-   open terminal in main-folder and

    -   run src-bucket-scripts to create the src-bucket and upload it's content in S3

-   open terminal in terraform-folder and

    -   run terraform-bucket-script to create the terraform-bucket in S3

    -   do `terraform init`

    -   do `terraform plan` to confirm everything works, then `terraform apply`
