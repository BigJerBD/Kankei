import csv
import itertools
import os
import shutil
from pathlib import Path


def get_csv_header(data_lst):
    return list({key for key in itertools.chain.from_iterable(data_lst)})


def dict_to_csv(path, header, elems):
    write_method = 'a+' if os.path.isfile(path) else 'w'
    with open(path, write_method, encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(header))
        if write_method == 'w':
            writer.writeheader()
        for line in elems:
            writer.writerow(line)


def csv_writer(data_it, path, reset=False):
    path = Path(path)
    reset and os.path.exists(path) and shutil.rmtree(path)
    os.mkdir(path)

    for name, data in data_it:
        csv_data = [d.neo4j_csv for d in data]
        dict_to_csv(
            (path / name).with_suffix(".csv"),
            get_csv_header(csv_data),
            csv_data,
        )
