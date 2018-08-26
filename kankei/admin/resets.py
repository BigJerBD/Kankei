import os
import shutil

from config import conf


def reset_csv():
    print('reseting neo4j csv data')
    for path in [conf.csv.node,conf.csv.link]:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)


def reset_neo4j():
    print('resetting graph.db')
    if conf.neo4j.graph.exists():
        shutil.rmtree(conf.neo4j.graph)



