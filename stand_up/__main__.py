"""stand_up entry point script."""
# stand_up/__main__.py

from stand_up import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()
