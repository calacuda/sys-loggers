"""
battery_logger.py

this program save historical battery data to a csv formatted file,
it is designed to be run at regular intervals by a cron job.


By: Calacuda | MIT Licence | Epoch April 11, 2022
"""


import psutil
import configparser
from datetime import date
import time
import datetime
from os.path import expanduser, exists
from os import makedirs


CONFIG_FILE = expanduser('~/.config/sys-loggers/sys-loggers.conf')
CSV_FILE = expanduser("~/.log/sys-logs/battery.csv")
ORDER = ["date", "time", "percent", "charging"]
HEADER = ",".join(ORDER)


def get_configs(fname):
    cfg = configparser.ConfigParser()
    cfg.read(fname)
    # [print(thing) for thing in cfg.sections()]
    return cfg["BATTERY"]


def get_data():
    #human_date = date.today().strftime("%B %d %Y")
    unix_time = int(time.time())
    human_date = datetime.datetime.fromtimestamp(unix_time).isoformat()
    bat = psutil.sensors_battery()
    bat_percent = bat.percent
    bat_plugged = bat.power_plugged
    return {"date": human_date, "time": unix_time, "percent": bat_percent, "charging": bat_plugged}


def make_csv(csv):
    try:
        makedirs("/".join(csv.split("/")[0:-1]))
    except FileExistsError:
        pass

    with open(csv, "w+") as csv_file:
        csv_file.write(HEADER)
        csv_file.write("\n")


def write_line(cfg, data, csv):
    if not exists(csv):
        make_csv(csv)

    with open(csv, "a") as csv_file:
        line = ""
        for data_name in ORDER:
            line = f"{line}{',' if line else ''}{data.get(data_name)}"
        csv_file.write(line)
        csv_file.write("\n")


def main():
    if not exists(CONFIG_FILE):
        print("no config file found!")
        return

    cfg = get_configs(CONFIG_FILE)
    data = get_data()
    csv = expanduser(cfg["csv-file"].strip('"').strip("'")) if cfg["csv-file"] else CSV_FILE
    write_line(cfg, data, csv)


if __name__ == "__main__":
    main()
