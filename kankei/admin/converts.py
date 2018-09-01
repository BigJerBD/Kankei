import subprocess
from collections import OrderedDict

import data_fetcher
from config import conf
from util.csv_util import dict_to_csv, get_csv_header

fetch_mapping = OrderedDict([
    ("kanji", data_fetcher.get_kanji),
    ("component", data_fetcher.get_components),
    ("radical", data_fetcher.get_radicals),
    ("word", data_fetcher.get_word)
])

descriptor = {
    "fetch": ["kanji","word","radical"],
    "excluded_links": [],
    "squished_links": [],
    "format": "csv" or "json"
}

def convert_csv_neo4j():
    print("converting csv files into neo4j")
    node_files = list(conf.csv.node.iterdir())
    link_files = list(conf.csv.link.iterdir())

    if node_files or link_files:
        subprocess.check_output(
            [conf.neo4j.admin, 'import',
             *[f'--nodes={(conf.csv.node/file).absolute()}' for file in node_files],
             *[f'--relationships={(conf.csv.link/file).absolute()}' for file in link_files],
             f"--report={conf.neo4j.report}"
             ],
        )


def convert_rawdata_csv(excludes=None):
    print("converting raw data files in csv")
    excludes = excludes or []
    kankei_dict = data_fetcher.kankeismartdict.KankeiSmartDict()
    data = conf.data

    for name, fetch in fetch_mapping.items():
        if name not in excludes:
            fetch(kankei_dict, getattr(data, name))

    _convert_cls_csv(conf.csv.node, kankei_dict.iter_node())
    _convert_cls_csv(conf.csv.link, kankei_dict.iter_link())


def convert_rawdata_json(excludes=None):
    ...


def _convert_cls_csv(base_path, data_sequence):
    for name, data in data_sequence:
        csv_data = [d.csv for d in data]
        dict_to_csv(
            (base_path / name).with_suffix(".csv"),
            get_csv_header(csv_data),
            csv_data,
        )
