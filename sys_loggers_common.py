"""
sys-loggers-common.py

functions common to the different sys loggers


by: Calacuda | MIT Licence | Epoch: Apr 16, 2022
"""


from os.path import expanduser, exists
from os import makedirs


def make_csv(csv, order):
    try:
        makedirs("/".join(csv.split("/")[0:-1]))
    except FileExistsError:
        pass

    with open(csv, "w+") as csv_file:
        csv_file.write(",".join(order))
        csv_file.write("\n")


def write_line(data, order, csv):
    csv = expanduser(csv)
    if not exists(csv):
        make_csv(csv, order)

    with open(csv, "a") as csv_file:
        line = ""
        for data_name in order:
            line = f"{line}{',' if line else ''}{data.get(data_name)}"
        csv_file.write(line)
        csv_file.write("\n")
