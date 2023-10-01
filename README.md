# Rightmove Email Notifications
Get emails within 5 minutes of a property being available on the website!
Uses the [rightmove-webscraper](https://github.com/toby-p/rightmove_webscraper.py) Python package, for which I am very grateful.

## Local Development
### Pre-Requisites
* Python 3.11
* AWS account credentials

### Setting Up
#### Windows
```powershell
pip install pipenv
pip install aws-sam-cli
pipenv sync

$env:RIGHTMOVE_URL="<your rightmove url>"
$env:ALERT_EMAIL="<your email>"
$env:AWS_ACCESS_KEY_ID="<your access key id>"
$env:AWS_SECRET_ACCESS_KEY="<your secret access key>"
```

#### Mac/Linux
```powershell
pip install pipenv
pip install aws-sam-cli
pipenv sync

export RIGHTMOVE_URL="<your rightmove url>"
export ALERT_EMAIL="<your email>"
export AWS_ACCESS_KEY_ID="<your access key id>"
export AWS_SECRET_ACCESS_KEY="<your secret access key>"
```

### Running Locally
The handler can be triggered using the `trigger_lambda.py` script. Modify the environment variables set in this file to ones accurate for you.

`python trigger_lambda.py`


### Deploying
#### GitHub Actions
GitHub Actions is currently set up to deploy with every push to main. This requires the following secrets to be set in the repository:
* RIGHTMOVE_URL="\<your rightmove url\>"
* ALERT_EMAIL="\<your email\>"
* AWS_ACCESS_KEY_ID="\<your access key id\>"
* AWS_SECRET_ACCESS_KEY="\<your secret access key\>"

#### Windows
```powershell
.\deploy\deploy.bat
```

#### Mac/Linux
```shell
./deploy/deploy.sh
```


## Future Improvements
* Make the emails more presentable
* Parsing the listings for more granular features e.g. garage, en-suite