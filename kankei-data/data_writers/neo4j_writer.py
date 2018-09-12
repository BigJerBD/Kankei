import os
import shutil


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

