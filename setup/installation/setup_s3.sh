#!/bin/bash

# Load environment variables from .env file

if [ -f .env ]; then
    source .env

else
    echo "Error .env file not found." 
    exit 1
fi

aws s3api create-bucket --bucket "$BUCKET_NAME" --region "$REGION"

echo "S3 bucket '$BUCKET_NAME' create in region '$REGION'"

aws s3 cp s3_upload_files s3://$BUCKET_NAME/config_files/ --recursive