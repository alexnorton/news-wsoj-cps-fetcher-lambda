import os
import json
import boto3
import urllib.request
import urllib.parse
import ssl


def handler(event, context):
    api_key = os.environ["CONTENT_API_KEY"]
    s3_bucket = os.environ["ARTICLES_S3_BUCKET"]

    message_str = event["Records"][0]["Sns"]["Message"]
    message = json.loads(message_str)

    if message["asset_type"] == "STY":
        story_uri = message["uri"].replace(
            "https://api.live.bbc.co.uk/content/asset", ""
        )

        if message["event_type"] == "PUBLISH":
            story = get_story(api_key, story_uri)
            save_story(s3_bucket, story)
        elif message["event_type"] == "WITHDRAW":
            delete_story(s3_bucket, story)


def get_story(api_key, uri):
    params = urllib.parse.urlencode({"api_key": api_key})

    headers = {
        "Accept": "application/json",
        "X-Candy-Audience": "Domestic",
        "X-Candy-Platform": "Desktop",
    }

    context = ssl.create_default_context(cafile="cloudservicesroot.pem")

    url = "https://content-api-a127.api.bbci.co.uk/asset{}?{}".format(uri, params)

    print(url)

    req = urllib.request.Request(url, headers=headers)

    response = urllib.request.urlopen(req, context=context)
    story = json.load(response)["results"][0]

    return story


def save_story(bucket, story):
    s3 = boto3.resource("s3")

    s3.Object(bucket, story["assetUri"][1:]).put(Body=json.dumps(story))


def delete_story(bucket, story):
    s3 = boto3.resource("s3")

    s3.Object(bucket, story["assetUri"][1:]).delete()
