import json
import typer
import sys
import csv
import pathlib
from typing import Optional
from datetime import datetime, date
from time import sleep

app = typer.Typer()


@app.command()
def main(activity: str,
         hourly_rate: Optional[float] = typer.Option(None, "--hourly_rate", "-h", help="Hourly rate"),
         currency: Optional[str] = typer.Option("USD", "--currency", "-c", help="Currency used"),
         requested_from: Optional[str] = typer.Option(None, "--requested_from", "-r",
                                                      help="Developer/Company requesting payment"),
         bill_to: Optional[str] = typer.Option(None, "--bill_to", "-b", help="Company to bill to"),
         finish_report: Optional[bool] = typer.Option(False, "--finish_report", "-f",
                                                      help="Add business metadata to the final version of the report"),
         due_date: Optional[str] = typer.Option(None, "--due_date", "-d", help="Due date for payment")):
    file_path = pathlib.Path.cwd() / "rastreador.json"
    if file_path.is_file():
        with open(file_path, mode='r+') as fid:
            data = json.load(fid)
            if hourly_rate is None:
                hourly_rate = data["hourly_rate"]

            if finish_report:
                if requested_from is None:
                    requested_from = data["requested_from"]

                if bill_to is None:
                    bill_to = data["bill_to"]

    start_time = datetime.now()
    print("Press CTRL+C to stop timer")
    while True:
        try:
            sleep(1)
            current_time = datetime.now() - start_time
            billed_time = round(current_time.total_seconds() * (hourly_rate/3600), 2)
            print(f"Activity: {activity} "
                  f"- Current time tracked: {current_time} "
                  f"- Billed time: ${billed_time}", end="", flush=True)
            print("\r", end="", flush=True)
        except KeyboardInterrupt:
            with open('report.csv', 'a+', newline='') as file:
                fieldnames = ['activity', 'current_time', 'billed_time']
                writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow({'activity': activity, 'current_time': current_time, 'billed_time': billed_time})

            if finish_report:
                with open("report.csv", "r") as fi:
                    reader = csv.DictReader(fi)
                    total = round(sum(float(row["billed_time"]) for row in reader), 2)

                with open('report.csv', 'a+', newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(['currency', currency])
                    writer.writerow(['requested_from', requested_from])
                    writer.writerow(['bill_to', bill_to])
                    writer.writerow(['total', total])
                    writer.writerow(['date', date.today()])
                    writer.writerow(['due_date', due_date])

            print("\nGood job")
            sys.exit()


if __name__ == "__main__":
    app()
