"""This module post standup to slack."""

# stand_up/slack.py

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv

load_dotenv()

# Create a new WebClient instance
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))


def send_message(message):
    try:
        response = client.chat_postMessage(
            channel=os.getenv("SLACK_CHANNEL_ID"),
            blocks=[
                    {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                                "text": message,
                        }
                    }
            ],
            text=message
        )
        print("Message sent: ", response["ts"])
    except SlackApiError as e:
        print("Error sending message: {}".format(e))
