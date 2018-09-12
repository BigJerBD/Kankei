# note :: this parser depend on the business rule  of how we generate the neo4j data
import csv
from pathlib import Path

import data


#todo Complete!

def parse_kkneo4jcsv(data_path):
    file_name = data_path.split("/")[-1].replace(".csv", "")
    with open(data_path) as f:
        csv_data = csv.DictReader(f)

        if "-" in file_name:
            element_cls = data.all_links
            params = {}
        else:
            element_cls = data.all_nodes[file_name]
            for line in csv_data:
                main_label, *other_labels = line.pop(":LABEL").split(";")
                # filter to proper argument_name
                args = {
                    k.split(":")[0]: v for k, v in line.items()
                    if not k.startswith(":")
                }

                raise NotImplemented
                #yield element_cls(
                #    subcomponents="",
                #    extra_labels=missed_components,
                #    **args,
                #)



def parse_kkneo4jcsv_folders(*folders):
    all_paths = (path for folder in folders for path in folder)
    for path in all_paths:
        yield from parse_kkneo4jcsv(Path(path))
