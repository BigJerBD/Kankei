import os
import shutil
from pathlib import Path
from subprocess import call

import kankei_context


def main():
    print('reseting  graph.db')
    reset_graphdb(kankei_context.KANKEI_CONFIG)
    print('importing csv to database...')
    import_to_database(kankei_context.KANKEI_CONFIG)


def reset_graphdb(conf):
    dbms = conf.get('dbms_config')
    graph_db_path = Path(dbms["basepath"], dbms["database"], dbms["version"], dbms["data_path"])
    shutil.rmtree(graph_db_path)


def import_to_database(conf):
    dbms = conf.get('dbms_config')
    node_path = Path(conf["node_path"])
    link_path = Path(conf["link_path"])
    node_files = os.listdir(node_path.absolute())
    link_files = os.listdir(link_path.absolute())
    neo4j_admin = str(Path(dbms["basepath"], dbms["database"], dbms["version"], dbms["neo4j_admin"]).absolute())

    return call(
        [neo4j_admin, 'import',
         *[f'--nodes {str((node_path/file).absolute())}' for file in node_files],
         *[f'--relationships {str((link_path/file).absolute())}' for file in link_files]
         ])


if __name__ == "__main__":
    main()
