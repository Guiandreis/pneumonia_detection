#!/bin/bash

# Load environment variables from .env file

if [ -f .env ]; then
    source .env

else
    echo "Error .env file not found." 
    exit 1
fi

aws ec2 create-key-pair \
    --key-name KEY_PAIR_NAME \
    --query 'KeyMaterial' \
    --output text > KEY_PAIR_NAME.pem

echo "ec2 create-key-pair '$KEY_PAIR_NAME' "

aws ec2 create-security-group \
    --group-name SECURITY_GROUP_NAME \
    --description 'Pneumonia project security group'

echo "ec2 create-security-group  '$SECURITY_GROUP_NAME' "

aws ec2 authorize-security-group-ingress  \
    --group-name SECURITY_GROUP_NAME \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

echo "ec2 authorize-security-group-ingress '$SECURITY_GROUP_NAME' "

aws ec2 run-instances \
    --image-id "$IMAGE_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_PAIR_NAME" \
    --security-group-ids "$SECURITY_GROUP_NAME" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value='$INSTANCE_NAME'}]"

echo "ec2 instance '$INSTANCE_NAME' '$IMAGE_ID' "