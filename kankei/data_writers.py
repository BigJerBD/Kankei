import os
import shutil

from util.csv_util import dict_to_csv, get_csv_header


def csv_writer(data_it, path, reset=False):
    reset and os.path.exists(path) and shutil.rmtree(path)
    os.mkdir(path)

    for name, data in data_it:
        csv_data = [d.neo4j_csv for d in data]
        dict_to_csv(
            (path / name).with_suffix(".csv"),
            get_csv_header(csv_data),
            csv_data,
        )


def json_writer(data_it, reset=False):
    ...


def neo4j_writer(link_path, node_path, graph_path, report_path, admin_path, reset=False):
    reset and os.path.exists(graph_path) and shutil.rmtree(graph_path)

    node_files = list(node_path.iterdir())
    link_files = list(link_path.iterdir())

    if node_files or link_files:
        os.subprocess.check_output(
            [admin_path, 'import',
             *[f'--nodes={(node_path/file).absolute()}' for file in node_files],
             *[f'--relationships={(link_path/file).absolute()}' for file in link_files],
             f"--report={report_path}"
             ],
        )