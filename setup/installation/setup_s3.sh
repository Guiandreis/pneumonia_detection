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