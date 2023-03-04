"""This module get data from notion api."""

# stand_up/database.py

import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()


def get_tasks():
    api_url = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE_ID')}/query"
    headers = {
        'Notion-Version': '2022-06-28',
        'Authorization': f"Bearer {os.getenv('NOTION_API_KEY')}",
        "Content-Type": "application/json"
    }
    response = requests.post(api_url, headers=headers)
    [print(item['properties']['Name']['title'][0]["plain_text"]) for item in response.json()['results']]