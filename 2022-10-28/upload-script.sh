mkdir build

zip ./build/api-server.zip requirements.txt
zip -r ./build/api-server.zip job_api 
zip -d ./build/api-server.zip __pycache__/
zip -T ./build/api-server.zip

aws s3 cp build/api-server.zip s3://jobs-api-bucket-2022-10-28/
