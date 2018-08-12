from xml.etree import ElementTree as Et

import requests


def xml_parse(method):
    """
    decorator for xml that give data in graph
    :param method:
    :return:
    """

    def wrap(fetch_helper, xml_path):
        data_root = Et.parse(xml_path).getroot()
        method(data_root, fetch_helper)
        return fetch_helper

    return wrap


def web_api_fetch(method):
    """
    decorator to get data from a web api
    :param method:
    :return:
    """

    def wrap(fetch_helper, url, **defaults):
        def request_get(params):
            return requests.get(url=url, params={**params, **defaults})
        return method(request_get, fetch_helper)

    return wrap
