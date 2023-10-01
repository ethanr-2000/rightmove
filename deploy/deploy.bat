@echo off
setlocal

rem Your AWS region
set AWS_DEFAULT_REGION=eu-west-2

rem Generate requirements.txt from Pipfile.lock
pipenv requirements > src/requirements.txt

rem Package and Deploy the application
sam build --use-container

cd .aws-sam/build

sam package ^
    --template-file template.yaml ^
    --output-template-file packaged.yaml ^
    --resolve-s3

sam deploy ^
    --template-file packaged.yaml ^
    --stack-name rightmove ^
    --capabilities CAPABILITY_IAM ^
    --region $env:AWS_DEFAULT_REGION ^
    --parameter-overrides "ParameterKey=RightmoveUrl,ParameterValue=$env:RIGHTMOVE_URL" ^
    --parameter-overrides "ParameterKey=AlertEmail,ParameterValue=$env:ALERT_EMAIL"

endlocal
