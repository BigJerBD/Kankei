import csv
import itertools
import os


def get_csv_header(data_lst):
    return list({key for key in itertools.chain.from_iterable(data_lst)})


def write_in_csv(path, header, elems):
    write_method = 'a+' if os.path.isfile(path) else 'w'
    with open(path, write_method, encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(header))
        if write_method == 'w':
            writer.writeheader()
        for line in elems:
            writer.writerow(line)

