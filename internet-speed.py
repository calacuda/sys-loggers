"""
internet-speed.py

logs internet speed desined to be run as a cron job.


by: Calacuda | MIT Licence | epoch: Apr 16, 2022
"""


import time
import speedtest
import datetime
import sys_loggers_common as sys_log


def get_data():
    unix_time = int(time.time())
    human_date = datetime.datetime.fromtimestamp(unix_time).isoformat()
    speed = speedtest.Speedtest()
    dload = speed.download()/1024/1024  # in Mb/s
    uload = speed.upload()/1024/1024    # in Mb/s
    
    return {"date": human_date, "time": unix_time, "dload": f"{dload} Mb/s", "uload": f"{uload} Mb/s"}


def main():
    data = get_data()
    sys_log.write_line(data, ["date", "time", "dload", "uload"], "~/.log/sys-logs/internet.csv")


if __name__=="__main__":
    main()


