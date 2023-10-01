#!/bin/bash

# Generate requirements.txt from Pipfile.lock
pipenv requirements > src/requirements.txt

# Package and Deploy the application
sam build --use-container

cd .aws-sam/build

sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --resolve-s3

sam deploy \
    --template-file packaged.yaml \
    --stack-name rightmove \
    --capabilities CAPABILITY_IAM \
    --region "$AWS_DEFAULT_REGION" \
    --parameter-overrides "ParameterKey=RightmoveUrl,ParameterValue=$RIGHTMOVE_URL" \
    --parameter-overrides "ParameterKey=AlertEmail,ParameterValue=$ALERT_EMAIL"
