import typer
import sys
import csv
from datetime import datetime
from time import sleep

app = typer.Typer()


@app.command()
def main(hourly_rate: float, activity: str):
    start_time = datetime.now()
    while True:
        try:
            sleep(1)
            current_time = datetime.now() - start_time
            billed_time = current_time.total_seconds() * (hourly_rate/3600)
            print(f"Activity: {activity} "
                  f"- Current time tracked: {current_time} "
                  f"- Billed time: ${round(billed_time, 2)}", end="", flush=True)
            print("\r", end="", flush=True)
        except KeyboardInterrupt:
            with open('report.csv', 'a+', newline='') as file:
                fieldnames = ['activity', 'current_time', 'billed_time']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow({'activity': activity, 'current_time': current_time, 'billed_time': billed_time})

            print("\nBye")
            sys.exit()


if __name__ == "__main__":
    app()
