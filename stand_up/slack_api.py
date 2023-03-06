"""This module post standup to slack."""

# stand_up/slack_api.py

import os
import typer
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
        typer.secho(f"Message sent: {response['ts']}", fg=typer.colors.GREEN)
    except SlackApiError as e:
        typer.secho(f"Error sending message: {format(e)}", fg=typer.colors.RED)