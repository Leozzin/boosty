import os
import csv


filename = "additifs.csv"

with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["description"])
