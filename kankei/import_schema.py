from neo4j.v1 import GraphDatabase

import config
from data import all_nodes


def import_schema():
    print('writing indexes')
    import_indexes()
    print('writing constraint')
    import_constaints()


def import_indexes():
    db = config.db_dst
    neo4j = GraphDatabase.driver(db['uri'], auth=(db['user'], db['password']))

    with neo4j.session() as session:
        write_all_index(session, all_nodes())


def import_constaints():
    ...


def create_index(tx, label, prop):
    query = f'CREATE INDEX ON :{label}({prop})'
    print(query)
    return tx.run(f'CREATE INDEX ON :{label}({prop})')


def write_all_index(session, nodes):
    for node in nodes:
        for idx in node.indexes:
            session.write_transaction(create_index, node.type, idx)


if __name__ == '__main__':
    import_schema()
