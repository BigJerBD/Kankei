import subprocess

import config
from util import file_util


def import_to_database():
    print('resetting graph.db')
    file_util.delete_if_exist(config.neo4j_graph)
    print('importing csv to neo4j')
    csv_to_db()


def csv_to_db():
    node_files = list(config.node_path.iterdir())
    link_files = list(config.link_path.iterdir())

    if node_files or link_files:
        subprocess.check_output(
            [config.neo4j_admin, 'import',
             *[f'--nodes {(config.node_path/file).absolute()}' for file in node_files],
             *[f'--relationships {(config.link_path/file).absolute()}' for file in link_files]
             ],
            shell=True
        )


if __name__ == "__main__":
    print("importing csv files to database")
    import_to_database()
