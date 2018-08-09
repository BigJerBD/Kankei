import logging
import os
from pathlib import Path

import yaml

# general config
import data_fetcher

kankei_home = os.environ['KANKEI_HOME']
conf_path = f"{kankei_home}/etc/config.yaml"
ex_conf_path = f"{kankei_home}/etc/config.example.yaml"
with open(conf_path) as conf_file:
    kankei_config = yaml.load(conf_file)

# neo4j config

neo4j_bin = Path(kankei_config['neo4j_bin'])
neo4j_data = Path(kankei_config['neo4j_data'])
# neo4j_admin currently only work on linux, change to handle .bat if needed ....
neo4j_admin = neo4j_bin / 'neo4j-admin'
neo4j_graph = neo4j_data / 'databases' / 'graph.db'

# neo4j http config
db_dst = kankei_config['db_dst']

# csv dst config
csv_dst = kankei_config['csv_dst']
node_path = Path(csv_dst['node'])
link_path = Path(csv_dst['link'])

# src_data configs
data_src = kankei_config['data_src']

