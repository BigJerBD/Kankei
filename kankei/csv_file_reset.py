import config
from util import file_util


def csv_file_reset():
    file_util.reset_dir(
        config.node_path,
        config.link_path
    )


if __name__ == '__main__':
    print('reseting neo4j csv data')
    csv_file_reset()
