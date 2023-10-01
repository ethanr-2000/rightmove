import os
os.environ["RIGHTMOVE_URL"] = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E87490"
os.environ["TABLE_NAME"] = "rightmove"
os.environ["SNS_TOPIC_ARN"] = "TOPIC_ARN"

from src.main import lambda_handler

lambda_handler({}, {})