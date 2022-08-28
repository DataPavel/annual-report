# Group Overview

## Project Description

#### What it does

*Group Overview* is a Flask application where you can upload list of transactions and make forecasts using Tensor Flow LSTM
#### Technologies used
Please see requirements.txt

## Instructions:

To run this app you need to do the following:  
1. Clone the repo to your local  
2. This app uses AWS S3, you will need to sign up and create 2 buckets. You can use freetier plan so no charges expected. However, please read the AWS S3 documentation and pricing policies for more information. You will need to create IAM user and create user and create aws_access_key_id and aws_secret_access_key for the created user
3. To run the application you need to create environmental variables and include them into .env file. Please check [this tutorial](https://www.youtube.com/watch?v=CJjSOzb0IYs) for learning how to use the .env file. The variable you will need:  
    aws_access_key_id - key id for AWS IAM user  
    aws_secret_access_key - access key for AWS IAM user  
    region_name - region name of your buckets  
    bucket - bucket name where you will store lists of transactions  
    bucket2 - bucket name where you will store prediction dataframes  
4. The specimen list of transactions are included in the repo
5. Install the dependencies from requirements.txt  
6. You are ready to go


The link to the detailed explanation on medium will be provided later