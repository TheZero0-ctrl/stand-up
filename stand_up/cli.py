"""This module provides the stand_up CLI."""
# stand_up/cli.py

#!/venv/bin/python3

from typing import Optional

import typer

from stand_up import notion_api, slack_api, sheet_api, __app_name__, __version__

app = typer.Typer()


@app.command()
def generate_stand_up(
    send_to_slack: bool = typer.Option(
        False,
        '--slack',
        '-s'
    ),
    send_to_timelog: bool = typer.Option(
        False,
        '--timelog',
        '-t'
    ),
    in_office: str = typer.Option(
        "Absent",
        '--in-office',
        '-io'
    ),
    hours: int = typer.Option(
        8,
        "--hrs",
        "-h"
    )
) -> None:
    stand_up = notion_api.generate_stand_up()
    typer.secho(stand_up, fg=typer.colors.GREEN)

    if send_to_slack:
        slack_api.send_message(stand_up)
    if send_to_timelog:
        task = get_task_from_stand_up(stand_up)
        sheet_api.post_to_timelog(task, in_office, hours)


def get_task_from_stand_up(stand_up: str) -> str:
    today_str = 'Today\n'
    tomorrow_str = '\nTomorrow'
    start_index = stand_up.find(today_str) + len(today_str)
    end_index = stand_up.find(tomorrow_str, start_index)
    return stand_up[start_index:end_index]

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(

    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
