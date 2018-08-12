import subprocess

from config import conf
from util import file_util


def import_to_database():
    print('resetting graph.db')
    file_util.delete_if_exist(conf.neo4j.graph)
    print('importing csv to neo4j')
    csv_to_db()


def csv_to_db():
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


if __name__ == "__main__":
    print("importing csv files to database")
    import_to_database()
