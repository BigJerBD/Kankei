import contextlib
import csv
import itertools
import os
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


@contextlib.contextmanager
def open_csvs(base_path, names, mode, encoding):
    yield {
        name: csv.writer(open(Path(base_path, name).with_suffix('.csv'), mode, encoding=encoding))
        for name in names
    }


def stream_csv_data(csv_path, encoding, delimiter=","):
    with open(csv_path, "r", encoding=encoding) as fs:
        reader = csv.reader(fs, delimiter=delimiter)
        for collumn in reader:
            yield from (cell for cell in collumn if cell)

