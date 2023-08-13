#!/bin/bash

INSTALL_PATH=${AWS_INSTALL_PATH:-"$HOME/.local"}
AWS_PROFILE_NAME="GitHub_Actions"
AWS_CREDENTIALS_FILE="$HOME/.aws/credentials"
AWS_CONFIG_FILE="$HOME/.aws/config"

install() {
  echo "aws CLI not found. Intalling to $INSTALL_PATH."
  mkdir -p $INSTALL_PATH
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip -q -o awscliv2.zip
  ./aws/install -i $INSTALL_PATH/aws-cli -b $INSTALL_PATH/bin
  rm -r awscliv2.zip ./aws

  if [ -z $(echo $PATH | grep -F "$INSTALL_PATH/bin") ]; then
    echo "$INSTALL_PATH/bin not in path. Adding to bashrc"
    echo "export PATH=\"$INSTALL_PATH:\$PATH\"" >> ~/.bashrc
    export PATH="$INSTALL_PATH/bin:$PATH"
  fi
}

configure() {
  echo -e "\nSetting up aws credentials\n"
  # Ensure all required variables are set
  if [ -z $AWS_ACCESS_KEY_ID ]; then
    echo 'AWS_ACCESS_KEY_ID not set. Exiting'
    exit 1
  elif [ -z $AWS_SECRET_ACCESS_KEY ];then
    echo 'AWS_SECRET_ACCESS_KEY not set. Exiting'
    exit 1
  elif [ -z $AWS_DEFAULT_REGION ]; then
    echo 'AWS_DEFAULT_REGION not set. Exiting'
    exit 1
  fi

  aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID" --profile "$AWS_PROFILE_NAME"
  aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY" --profile "$AWS_PROFILE_NAME"
  aws configure set region "$AWS_DEFAULT_REGION" --profile "$AWS_PROFILE_NAME"

  echo "aws set up with profile $AWS_PROFILE_NAME"
}

# If REMOVE_CREDENTIALS is set only clear the credentials file and exit
if [ ! -z $REMOVE_AWS_CREDENTIALS ]; then
  echo "Removing $AWS_PROFILE_NAME credentials from $HOME/.aws/credentials and $HOME/.aws/config"
  [ -f $AWS_CREDENTIALS_FILE ] && sed -i -e "/\[$AWS_PROFILE_NAME\]/,+2d" $AWS_CREDENTIALS_FILE
  [ -f $AWS_CONFIG_FILE ] && sed -i -e "/\[profile $AWS_PROFILE_NAME\]/,+1d" $HOME/.aws/config
  exit 0
fi

# Check if aws CLI is not currently available
if ! command -v aws &> /dev/null; then
  install
else
  echo "aws CLI installation found. Skipping install."
fi

# Set up credentials
configure