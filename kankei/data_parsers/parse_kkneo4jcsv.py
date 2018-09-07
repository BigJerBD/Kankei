# note :: this parser depend on the business rule  of how we generate the neo4j data
import csv
from pathlib import Path
import data

def parse_kkneo4jcsv(data_path):
    if "-" in data_path:
        element_group = data.all_links
    else:
        element_group = data.all_nodes

    with open(data_path) as f:
        csv_data = csv.DictReader(f)

    for line in csv_data:
        ...
        # create object from line,


def parse_kkneo4jcsv_folders(*folders):
    #todo complete
    all_paths = (path for folder in folders for path in folder)
    for path in all_paths:
        yield from parse_kkneo4jcsv(Path(path))
