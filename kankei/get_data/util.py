from collections import defaultdict,Iterable

from xml.etree import ElementTree as Et



def load_and_parse(method):
    """
    decorator for xml that give data in graph
    #note :: bad dependency with NodeCollection?
    :param method:
    :return:
    """
    def wrap(xml_path):
        data_root = Et.parse(xml_path).getroot()
        data = defaultdict(list)
        method(data_root, data)
        return data

    return wrap


def import_data(dct, data):
    data_cls = type(data)
    if data:
        if data_cls == list or data_cls == tuple:
            data = [d for d in data if d]
            data_cls = type(data[0])
            dct[data_cls] += data
        else:
            dct[data_cls].append(data)
