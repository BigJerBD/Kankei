import os
from collections import OrderedDict
from pathlib import Path

import yaml

import data_parsers


# config structure definition
class SubConfig:
    ...


class Config:
    """
    empty class to make a configuration object simply
    """

    def __init__(self, source_dct):
        for key, value in source_dct.items():
            access_seq = key.split(".")
            _append_dot_path(self, access_seq, value)

    def __getattr__(self, item):
        # specifies that a get_attribute (.) call is dynamic
        return super().__getattribute__(item)


def _append_dot_path(dct, accesses, value):
    if accesses:
        subdict = getattr(dct, accesses[0], SubConfig())
        setattr(dct, accesses[0], _append_dot_path(subdict, accesses[1:], value))
        return dct
    else:
        return value


# configuration dictionary loading
configuration_file_path = f"{os.environ['KANKEI_HOME']}/etc/config.yaml"
base_configuration_file_path = f"{os.environ['KANKEI_HOME']}/etc/config.example.yaml"

# neo4j config
# neo4j_admin currently only work on linux, change to handle .bat if needed ....
conf = Config(yaml.load(open(configuration_file_path)))

conf.neo4j.bin = Path(conf.neo4j.bin)
conf.neo4j.data = Path(conf.neo4j.data)
conf.neo4j.auth = (conf.neo4j.user, conf.neo4j.password)

conf.neo4j.admin = conf.neo4j.bin / 'neo4j-admin'
conf.neo4j.graph = conf.neo4j.data / 'databases' / 'graph.db'

conf.csv.node = Path(conf.csv.node)
conf.csv.link = Path(conf.csv.link)

fetch_mapping = OrderedDict([
    ("monash_kanji", (data_parsers.parse_monash_kanji,
                      conf.data.kanji)),
    ("kanjivg", (data_parsers.parse_kanjivg,
                 conf.data.subkanji)),
    ("monash_radicals", (data_parsers.parse_monash_radicals,
                         conf.data.radical)),
    ("monash_words", (data_parsers.parse_monash_words,
                      conf.data.word)),
    ("parse_kkneo4jcsv", (data_parsers.parse_kkneo4jcsv,
                          conf.data.output))
])
