"""This module provides the stand_up CLI."""
# stand_up/cli.py

from typing import Optional

import typer

from stand_up import notion_api, slack_api, __app_name__, __version__

app = typer.Typer()


# @app.command()
# def init(
#     db_path: str = typer.Option(
#         "hello",
#         "--db-path",
#         "-db",
#         prompt="to-do database location?",
#     ),
# ) -> None:
#     typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)

@app.command()
def generate_stand_up(
    send_to_slack: bool = typer.Option(
        False,
        '--slack',
        '-s'
    )
) -> None:
    stand_up = notion_api.generate_stand_up()
    typer.secho(stand_up, fg=typer.colors.GREEN)
    if send_to_slack:
        slack_api.send_message(stand_up)
    else:
        send_to_slack = typer.confirm("Do you want to send the stand-up message to slack?")
        if send_to_slack:
            slack_api.send_message(stand_up)


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
