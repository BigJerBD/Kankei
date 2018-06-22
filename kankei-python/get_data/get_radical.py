from data.nodes import Radical
from get_data.util import load_and_parse, import_data


@load_and_parse
def get_radicals(xml, data):
    """
    create a node_collection containing radical data
    """
    for cells in (rad.findall('td') for rad in xml):
        import_data(data, _make_radical(cells))

def _make_radical(xml):
    return Radical(
        writing=xml[1].find('span').text.split(' ')[0],
        stroke_count=[int(xml[2].text.replace(',', ''))],
        radical_number=xml[0].find('a').text,
        frequency=int(xml[8].text.replace(',', ''))
    )
