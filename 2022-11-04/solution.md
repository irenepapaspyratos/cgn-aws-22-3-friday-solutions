# Solution for Challenge of 04.11.2022

## Task 1.1

-   start lab, update credentials, download .pem and give permissions
-   in terminal:

    ```
    aws s3api create-bucket
                 --bucket ip-lamda-bucket
                 --region us-west-2
                 --create-bucket-configuration LocationConstraint=us-west-2
    ```

## Task 1.2

-   create a .zip of requests to import in layer for lambda by executing the following commands one after another:

    ```
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

-   replace the default lambda-code with one that does the job of the task:

    ```
    code coming
    ```
