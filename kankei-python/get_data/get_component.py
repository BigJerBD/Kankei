import itertools

from data.links import IsWrittenWith, HasStroke
from data.nodes import Kanji, Stroke, Component
from get_data.util import load_and_parse, import_data


@load_and_parse
def get_components(xml, data):
    """
    create a node_collection and link_collection containing component_data
    """
    valid_cpn_xml = _get_cpn_xmls(xml)
    for cpn_xml in valid_cpn_xml:
        current_comp = _get_component(cpn_xml)

        import_data(data, current_comp)
        for elem in itertools.chain(_get_sub_components(current_comp, cpn_xml, []),
                                    _get_strokes(current_comp, cpn_xml, [])):
            import_data(data, elem)


def _get_cpn_xmls(xml):
    cpn_xmls = {}
    # get all componenent marked as element and get them 1 time
    for component_xml in xml.iter('g'):
        if 'element' in component_xml.attrib and component_xml.attrib['element'] not in cpn_xmls:
            cpn_xmls[component_xml.attrib['element']] = component_xml

    # fetch all part that can be kanji, then cpn
    kan_xmls = {c.find('g').attrib['element']: c.find('g') for c in xml.iter('kanji')}
    return {kan_xmls.get(key, None) or value for key, value in cpn_xmls.items()}


def _get_sub_components(origin_cpn, cur_cpn, position):
    if 'position' in cur_cpn.attrib:
        position.append(cur_cpn.attrib['position'])

    if 'element' in cur_cpn.attrib and cur_cpn.attrib['element'] != origin_cpn.props['writing']:
        yield from [_get_component_link(origin_cpn, cur_cpn, position)]

    result = (_get_sub_components(origin_cpn, child, position) for child in cur_cpn.findall('g'))
    yield from list(itertools.chain.from_iterable(result))


def _get_strokes(original_cpn, current_cpn, position):
    if current_cpn.tag == 'path':
        strk_node, strk_link = zip(*[
            (_get_stroke(strk),
             _get_stroke_link(original_cpn, strk, current_cpn, position))
            for strk in current_cpn.attrib['type'].split('/')])
        yield from strk_node
        yield from strk_link

    if 'position' in current_cpn.attrib:
        position.append(current_cpn.attrib.get('position'))

    result = (_get_strokes(original_cpn, child, position) for child in current_cpn)
    yield from list(itertools.chain.from_iterable(result))


def _get_component(xml):
    return Component(component_tag=xml.attrib['id'],
                     writing=xml.attrib['element'],
                     stroke_count=[len([c for c in xml.iter('path')])]
                     )


def _get_component_link(cpn, xml, position):
    return IsWrittenWith(begin_node=cpn,
                         end_node=Kanji(writing=xml.attrib['element']),
                         position=position
                         )


def _get_stroke(strk):
    return Stroke(writing=strk)


def _get_stroke_link(cpn, strk, xml, position):
    return HasStroke(begin_node=cpn,
                     end_node=Stroke(writing=strk),
                     position=position,
                     stroke_number=xml.attrib['id'].split('-')[1][1:],
                     vec_coord=xml.attrib['d']
                     )
