"""This module get data from notion api."""

# stand_up/database.py

import os
import requests
import json

from dotenv import load_dotenv
from datetime import date

load_dotenv()


def get_tasks_for_standup():
    api_url = f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE_ID')}/query"
    filter = {
        'filter': {
            'and': [
                {
                    'or': [
                        {
                            "property": "Status",
                            "status": {
                                "equals": "In progress"
                            }
                        },
                        {
                            "property": "Status",
                            "status": {
                                "equals": "Done"
                            }
                        },
                        {
                            "property": "Status",
                            "status": {
                                "equals": "To Do"
                            }
                        }
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

    headers = {
        'Notion-Version': '2022-06-28',
        'Authorization': f"Bearer {os.getenv('NOTION_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, data=json.dumps(filter), headers=headers)
        response.raise_for_status() # Raises an exception if there was an HTTP error status code
    except requests.exceptions.HTTPError as http_error:
        print(f'HTTP error occurred: {http_error}')
    except Exception as error:
        print(f'Other error occurred: {error}')
    else:
        return response.json()['results']
    # [print(item['properties']['Name']['title'][0]["plain_text"])
    #  for item in response.json()['results']]

def generate_stand_up():
    tasks = get_tasks_for_standup()
    today_section = []
    tomorrow_section = []
    in_progress_section = []
    today = date.today()
    formatted_today = today.strftime("%b %d" + ("th" if 11<=today.day<=13 else {1:"st", 2:"nd", 3:"rd"}.get(today.day % 10, "th")))

    for task in tasks:
        if task['properties']['Status']['status']['name'] == 'Done':
            today_section.append(task['properties']['Name']['title'][0]['plain_text'])
        elif task['properties']['Status']['status']['name'] == 'In progress':
            in_progress_section.append(task['properties']['Name']['title'][0]['plain_text'])
        else:
            tomorrow_section.append(task['properties']['Name']['title'][0]['plain_text'])

    print(f"Stand-up {formatted_today}")
    print("Today")
    [print(f"- {today_task}") for today_task in today_section]
    [print(f"- WIP {in_progress_task}") for in_progress_task in in_progress_section]
    print("Tomorrow")
    [print(f"- {tomorrow_task}") for tomorrow_task in tomorrow_section]
    print("Blocker")
    print("None")