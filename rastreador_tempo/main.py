import typer
from datetime import datetime
from time import sleep

app = typer.Typer()


@app.command()
def main():
    start_time = datetime.now()
    while True:
        sleep(1)
        current_time = datetime.now() - start_time
        print(current_time, end="", flush=True)
        print("\r", end="", flush=True)


if __name__ == "__main__":
    app()
