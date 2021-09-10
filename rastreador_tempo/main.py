import typer
from datetime import datetime
from time import sleep

app = typer.Typer()


@app.command()
def main(hourly_rate: float, activity: str):
    start_time = datetime.now()
    while True:
        sleep(1)
        current_time = datetime.now() - start_time
        print(f"Activity: {activity} "
              f"- Current time tracked: {current_time} "
              f"- Billed time: ${round(current_time.total_seconds() * (hourly_rate/3600), 2)}", end="", flush=True)
        print("\r", end="", flush=True)


if __name__ == "__main__":
    app()
