"""This module post standup to timelog sheets"""

# stand_up/sheet_api.py

import pygsheets
import typer
from datetime import date, timedelta

client = pygsheets.authorize(
    service_account_file="timelog-379717-26592c971bb5.json")


def post_to_timelog(task, in_office="Absent", hrs=8):
    today = date.today()
    month = today.strftime("%b")
    spreadsheet = client.open("Time Log Ankit Pariyar")
    worksheet = get_or_create_month_worksheet(spreadsheet, month)

    row = today.day
    worksheet.update_col(2, [[in_office], [task], [hrs]], row)
    typer.secho("Successfully updated Timelog", fg=typer.colors.GREEN)

def get_or_create_month_worksheet(spreadsheet, month):
    try:
        worksheet = spreadsheet.worksheet_by_title(month)
    except pygsheets.exceptions.WorksheetNotFound:
        typer.secho(f"Creating new worksheet {month}", fg=typer.colors.GREEN)
        worksheet = create_month_worksheet(spreadsheet, month)
    return worksheet

def create_month_worksheet(spreadsheet, month):
    worksht = spreadsheet.add_worksheet(month)
    worksht.update_col(1, [["Date"], ["In Office"], ["Task"], ["hrs"]])
    worksht.adjust_column_width(3, pixel_size=520)

    first_day_of_month, last_day_of_month = first_and_last_day_of_month()
    dates = [first_day_of_month + timedelta(days=x) for x in range((last_day_of_month - first_day_of_month).days + 1)]
    date_values = [[date.strftime('%m/%d/%Y')] for date in dates]

    worksht.update_row(2, date_values)
    return worksht

def first_and_last_day_of_month():
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=28) + timedelta(days=4)
    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
    return [first_day_of_month, last_day_of_month]
