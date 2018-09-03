import os
from collections import OrderedDict
from pathlib import Path

import yaml

import data_parsers
from util.config_util import Config

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
    ("monash_kanji", data_parsers.parse_monash_kanji),
    ("kanjivg", data_parsers.parse_kanjivg),
    ("monash_radicals", data_parsers.parse_monash_radicals),
    ("monash_words", data_parsers.parse_monash_words)
])
