"""This module get data from notion api."""

# stand_up/notion_api.py

import os
import requests
from datetime import date

from dotenv import load_dotenv

load_dotenv()

API_URL = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE_ID')}/query"
HEADERS = {
    'Notion-Version': '2022-06-28',
    'Authorization': f"Bearer {os.getenv('NOTION_API_KEY')}",
    "Content-Type": "application/json"
}


def get_tasks_for_standup():
    filter = {
        'filter': {
            'and': [
                {
                    'or': [
                        {
                            "property": "Status",
                            "status": {
                                "equals": status
                            }
                        } for status in ["In progress", "Done", "To Do"]
                    ]
                },
                {
                    "property": "Last edited time",
                    "last_edited_time": {
                        "on_or_after": str(date.today())
                    }
                }
            ]
        }
    }

    try:
        response = requests.post(API_URL, json=filter, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
    except Exception as error:
        print(f'Other error occurred: {error}')
    else:
        return response.json()['results']


def generate_stand_up():
    tasks = get_tasks_for_standup()
    today_section = []
    tomorrow_section = []
    today = date.today()
    formatted_today = today.strftime("%b %d" + ("th" if 11 <= today.day <= 13 else {
                                     1: "st", 2: "nd", 3: "rd"}.get(today.day % 10, "th")))

    for task in tasks:
        name = task['properties']['Name']['title'][0]['plain_text']
        status = task['properties']['Status']['status']['name']
        if status == 'Done':
            today_section.append(name)
        elif status == 'In progress':
            today_section.append(f"WIP {name}")
        else:
            tomorrow_section.append(name)
    today_tasks_str = "\n".join([" • {}".format(task)
                                for task in today_section])
    tomorrow_tasks_str = "\n".join(
        [" • {}".format(task) for task in tomorrow_section])
    return f"Stand-up {formatted_today}\nToday\n{today_tasks_str}\nTomorrow\n{tomorrow_tasks_str}\nBlocker\n • None"
