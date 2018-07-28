import inspect
from collections import defaultdict

from data.elements.node import Node
from get_data.get_component import get_components
from get_data.get_kanji import get_kanji
from get_data.get_radical import get_radicals
from get_data.get_word import get_word, Link
from get_data.util import import_data

def get_csv_data(config):
    data = get_data(**config)
    data = merge_dct_from_grp(data, node_group)
    data = remove_duplicate(data)
    data = split_data(data, **config)
    data = make_csv(data)
    return data


def get_data(component_file, kanji_file, radical_file, word_file, **_):
    all_data = defaultdict(list)

    def update(method, file):
        for elems in method(file).values():
            import_data(all_data, elems)


    # this part need to be parameterable
    update(get_components, component_file)
    update(get_kanji, kanji_file)
    update(get_radicals, radical_file)
    update(get_word, word_file)
    return all_data


def merge_dct_from_grp(all_data, groups):
    for grp_prnt, grp_chld in groups.items():

        indexed_data = defaultdict(Node)
        for chld in grp_chld:
            for elem in all_data.pop(chld):
                indexed_data[elem.id] += elem
        all_data[grp_prnt] = list(indexed_data.values())
    return all_data


def remove_duplicate(data):
    # simplify by hashing node and non-mut them?
    # -> could replace the middle line by a simple ( set(data[key_cls]) )
    for key_cls in data:
        if Node in inspect.getmro(key_cls):
            data[key_cls] = list(
                {node.id: node for node in data[key_cls]
                 }.values())
    return data


def split_data(data, node_path, link_path, **_):
    result = {}
    for key_cls in data:
        name = key_cls.__name__
        if Link in inspect.getmro(key_cls):
            # split link by their different begin and end point
            different_link = defaultdict(list)

            for elem in data[key_cls]:
                begin_type = elem.begin_node.label_id_pos
                end_type = elem.end_node.label_id_pos
                different_link[begin_type, end_type].append(elem)

            if len(different_link) > 1:
                for i, values in enumerate(different_link.values()):
                    result[link_path + '/%s_%s' % (name, str(i))] = values

            else:
                result[link_path + '/' + name] = data[key_cls]
        else:
            result[node_path + '/' + name] = data[key_cls]
    return result


def make_csv(data):
    return {key: [val.csv for val in lst] for key, lst in data.items()}



