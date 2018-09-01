from data.nodes import Radical
from data_fetcher.fetch_decorator import xml_parse


@xml_parse
def get_radicals(xml):
    """
    create a node_collection containing radical data
    """
    for cells in (rad.findall('td') for rad in xml):
        yield make_radical(cells)


def make_radical(xml):
    return Radical(
        writing=xml[1].find('span').text.split(' ')[0],
        stroke_count=[int(xml[2].text.replace(',', ''))],
        radical_number=xml[0].find('a').text,
        frequency=int(xml[8].text.replace(',', ''))
    )
