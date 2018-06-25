import csv
import itertools
import os
import shutil
from pathlib import Path


def csv_reset(csv_path, node_path, link_path, **_):
    if os.path.exists(csv_path):
        shutil.rmtree(csv_path)
    Path(csv_path).mkdir()
    Path(csv_path,node_path).mkdir()
    Path(csv_path,link_path).mkdir()


def dict_in_csv(data_dct, csv_path, **_):
    csv_path = Path(csv_path)
    for name, data in data_dct.items():
        path = (csv_path / name).with_suffix('.csv')
        _write_in_csv(path, _get_csv_header(data), data)


def _get_csv_header(data_lst):
    return list({key for key in itertools.chain.from_iterable(data_lst)})


def _write_in_csv(path, header, elems):
    write_method = 'a+' if os.path.isfile(path) else 'w'
    with open(path, write_method, encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(header))
        if write_method == 'w':
            writer.writeheader()
        for line in elems:
            writer.writerow(line)
