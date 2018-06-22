import os
import sys
from pathlib import Path
from subprocess import call

import yaml

import data_import
from csv_handling import dict_in_csv, csv_reset
from data import nodes_group

#todo add unit test and other things
#todo remove this yellow thing
#todo commit ! :D:D :D its getting somewhere

def main(path, skip_csv):
    print('reading_config...')
    config = get_config(path)
    print('importing data to csv...')
    if not skip_csv:
        print('getting parsing xml data...')
        data = get_csv_data(config)
        print('getting writing data in csv...')
        write_in_csv(data, config)
    else:
        print('skipped.')
    print('importing csv to database...')
    import_to_database(config)


def get_config(path):
    with open(path, 'r') as ymlfile:
        return yaml.load(ymlfile)


def get_csv_data(config):
    data = data_import.get_data(**config)
    data = data_import.merge_dct_from_grp(data, nodes_group)
    data = data_import.remove_duplicate(data)
    data = data_import.split_data(data, **config)
    data = data_import.make_csv(data)
    return data


def write_in_csv(data, config):
    csv_reset(**config)
    dict_in_csv(data, **config)


def import_to_database(conf):
    dbms = conf.get('dbms_config')
    node_path = Path(conf["csv_path"], conf["node_path"])
    link_path = Path(conf["csv_path"], conf["link_path"])
    node_files = os.listdir(node_path.absolute())
    link_files = os.listdir(link_path.absolute())
    neo4j_admin = str(Path(dbms["basepath"], dbms["database"], dbms["version"], dbms["neo4j_admin"]).absolute())

    return call([neo4j_admin, 'import',
                 *[f'--nodes {str((node_path/file).absolute())}' for file in node_files],
                 *[f'--relationships {str((link_path/file).absolute())}' for file in link_files]
                 ])

if __name__ == '__main__':
    _file_name, *_args = sys.argv
    if len(_args) < 1:
        print(f'usage = {os.path.basename(__file__)} <config_yaml>')
    else:
        main(_args[0], skip_csv = "--skip_csv" in _args)
