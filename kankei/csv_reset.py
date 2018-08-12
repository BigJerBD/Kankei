from config import conf
from util import file_util


def csv_file_reset():
    file_util.reset_dir(
        conf.csv.node,
        conf.csv.node
    )


if __name__ == '__main__':
    print('reseting neo4j csv data')
    csv_file_reset()
