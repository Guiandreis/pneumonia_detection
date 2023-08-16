#!/bin/bash

# Load environment variables from .env file

if [ -f .env ]; then
    source .env

else
    echo "Error .env file not found." 
    exit 1
fi


aws ec2 create-key-pair \
    --key-name $KEY_PAIR_NAME \
    --query 'KeyMaterial' \
    --output text > "$KEY_PAIR_NAME".pem

echo "ec2 create-key-pair '$KEY_PAIR_NAME' "

aws ec2 create-security-group \
    --group-name SECURITY_GROUP_NAME \
    --description 'Pneumonia project security group'

echo "ec2 create-security-group  '$SECURITY_GROUP_NAME' "

SECURITY_GROUP_ID=$(aws ec2 describe-security-groups \
    --filters Name=group-name,Values=SECURITY_GROUP_NAME \
    --query 'SecurityGroups[0].GroupId' --output text)

echo "ec2 security group id '$SECURITY_GROUP_ID'"

aws ec2 authorize-security-group-ingress  \
    --group-name "$SECURITY_GROUP_NAME" \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

echo "ec2 authorize-security-group-ingress '$SECURITY_GROUP_NAME' "

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$IMAGE_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids "$SECURITY_GROUP_ID" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value='$INSTANCE_NAME'}]" \
    --query 'Instances[0].InstanceId' --output text)

echo "ec2 instance '$INSTANCE_NAME' $INSTANCE_ID "