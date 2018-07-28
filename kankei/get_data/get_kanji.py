import functools

from data.links import KanjiIsPronounced, HasMeaning
from data.nodes import Kanji, Meaning, Reading
from get_data.util import load_and_parse, import_data


@load_and_parse
def get_kanji(xml, data):
    """
    create a node_collection and link_collection containing kanji data
    """
    for char_xml in xml.iter('character'):
        kanji = _make_kanji(char_xml)
        readings = _make_readings_tuple(char_xml)
        meanings = _make_meanings(char_xml)

        import_elem = functools.partial(import_data,data)
        import_elem(kanji)
        import_elem([read for read, prop in readings])
        import_elem(meanings)
        import_elem(_make_kanji_read_links(kanji, readings))
        import_elem(_make_kanji_mean_links(kanji, meanings))


def _make_kanji(xml):
    misc = xml.find('misc')
    radical_number = [rad.text for rad in xml.iter('rad_value') if rad.attrib['rad_type'] == 'classical'][0]
    return Kanji(writing=xml.find('literal').text,
                 stroke_count=[int(strk.text) for strk in misc.findall('stroke_count')],
                 radical_number=radical_number,
                 kanji_frequency=misc.find('freq').text if misc.findall('freq') else "",
                 kanji_grade=misc.find('grade').text if misc.findall('grade') else "",
                 kanji_jlpt=misc.find('jlpt').text if misc.findall('jlpt') else ""
                 )


def _make_meanings(character_xml):
    return [Meaning(value=m.text)
            for m in character_xml.iter('meaning') if 'm_lang' not in m.attrib]


def _make_readings_tuple(character_xml):
    return [
        (Reading(reading=r.text),
         {'type_reading': 'on' if r.attrib['r_type'] == 'ja_on' else 'kun'})
        for r in character_xml.iter('reading') if r.attrib['r_type'] in ['ja_on', 'ja_kun']
    ]



def _make_kanji_read_links(kanji, readings):
    return [KanjiIsPronounced(begin_node=kanji, end_node=reading, **props)
            for reading, props in readings]


def _make_kanji_mean_links(kanji, meanings):
    return [HasMeaning(begin_node=kanji, end_node=meaning)
            for meaning in meanings]
