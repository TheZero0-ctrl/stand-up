"""This module post standup to timelog sheets"""

# stand_up/sheet_api.py

import pygsheets
import typer
from datetime import date, timedelta, datetime

client = pygsheets.authorize(
    service_account_file="timelog-379717-26592c971bb5.json")


def post_to_timelog(task, in_office="Absent", hrs=8):
    today = date.today()
    month = today.strftime("%b")
    year = today.year
    spreadsheet = client.open("Time Log Ankit Pariyar")
    new_worksheet_name = f"{month}({year})"
    worksheet = get_or_create_month_worksheet(spreadsheet, new_worksheet_name)

    row = today.day
    worksheet.update_col(2, [[in_office], [task], [hrs]], row)
    typer.secho("Successfully updated Timelog", fg=typer.colors.GREEN)

def get_or_create_month_worksheet(spreadsheet, worksheet_name):
    try:
        worksheet = spreadsheet.worksheet_by_title(worksheet_name)
    except pygsheets.exceptions.WorksheetNotFound:
        typer.secho(f"Creating new worksheet {worksheet_name}", fg=typer.colors.GREEN)
        worksheet = create_month_worksheet(spreadsheet, worksheet_name)
    return worksheet

def create_month_worksheet(spreadsheet, worksheet_name):
    worksht = spreadsheet.add_worksheet(worksheet_name, index=0)
    worksht.update_col(1, [["Date"], ["In Office"], ["Task"], ["hrs"]])
    worksht.adjust_column_width(3, pixel_size=520)

    first_day_of_month, last_day_of_month = first_and_last_day_of_month()
    dates = [first_day_of_month + timedelta(days=x) for x in range((last_day_of_month - first_day_of_month).days + 1)]
    date_values = [[date.strftime('%m/%d/%Y')] for date in dates]

    worksht.update_row(2, date_values)

    num_rows = len(date_values) + 1
    cell_updates = []

    for row_num in range(2, num_rows + 1):
        date_cell = worksht.cell((row_num, 1))
        date_value = datetime.strptime(date_cell.value, '%m/%d/%Y')
        if date_value.weekday() == 5 or date_value.weekday() == 6:
            row_range = f"A{row_num}:Z{row_num}"
            cell_updates.append(
                {
                    "repeatCell": {
                        "range": worksht.get_gridrange(f"A{row_num}", f"Z{row_num}"),
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {"red": 1, "green": 0.65, "blue": 0}
                                }
                            },
                        "fields": "userEnteredFormat.backgroundColor",
                        }
                    }         
                )

    # Batch update cell formatting
    if cell_updates:
        client.sheet.batch_update(spreadsheet.id, cell_updates)
    return worksht

def first_and_last_day_of_month():
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=28) + timedelta(days=4)
    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
    return [first_day_of_month, last_day_of_month]
