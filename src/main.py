import os
import json
import boto3
import pandas as pd
from rightmove_webscraper import RightmoveData
from datetime import datetime, timedelta

sns = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    known_listings = load_known_listings()
    rightmove_df = scrape_rightmove()

    new_listings = find_new_listings(known_listings, rightmove_df)

    if not new_listings:
        print("No new listings since last check")
        return

    send_notification(new_listings)
    update_previous_state(new_listings)


def load_known_listings():
    print("Loading known listings")

    response = table.scan()
    items = response.get("Items", [{"url": ""}])
    return items


def scrape_rightmove():
    url = os.environ["RIGHTMOVE_URL"]
    print(f"Getting current listings from {url}")

    rm = RightmoveData(url)
    rm_df = rm.get_results
    rm_df = rm_df.drop(
        columns=["search_date", "agent_url", "full_postcode", "number_bedrooms"]
    )
    return rm_df


def find_new_listings(known_listings, rightmove_df):
    print("Filtering for new properties")
    previous_state_df = pd.DataFrame(known_listings)
    if not previous_state_df.empty:
        rightmove_df = rightmove_df[~rightmove_df["url"].isin(previous_state_df["url"])]

    new_listings_dict = rightmove_df.to_dict(orient="records")
    deduplicated_new_listings = list(map(dict, set(frozenset(d.items()) for d in new_listings_dict)))
    return deduplicated_new_listings


def send_notification(new_listings):
    print("New properties found! Sending email")

    message = f"New Rightmove listings found:\n{json.dumps(new_listings, indent=2)}"
    sns.publish(
        TopicArn=os.environ.get("SNS_TOPIC_ARN"),
        Subject="New Rightmove Listings",
        Message=message,
    )


def update_previous_state(new_listings):
    print("Saving new properties to database")

    new_urls = [listing["url"] for listing in new_listings]
    new_urls = list(set(new_urls))

    ttl_timestamp = int((datetime.now() + timedelta(days=60)).timestamp())

    with table.batch_writer() as batch:
        for url in new_urls:
            item = {"url": url, "TTL": ttl_timestamp}
            batch.put_item(Item=item)
