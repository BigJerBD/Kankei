from xml.etree import ElementTree as Et

import requests


def xml_parse(method):
    """
    decorator for xml that give data in graph
    :param method:
    :return:
    """

    def wrap(smart_dict, xml_path):
        data_root = Et.parse(xml_path).getroot()
        method(data_root, smart_dict)
        return smart_dict

    return wrap


def web_api_fetch(method):
    """
    decorator to get data from a web api
    :param method:
    :return:
    """

    def wrap(smart_dict, url, **defaults):
        def request_get(params):
            return requests.get(url=url, params={**params, **defaults})
        return method(smart_dict, request_get)

    return wrap
