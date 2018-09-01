from data.links import KanjiIsPronounced, HasMeaning
from data.nodes import Kanji, Meaning, JapaneseReading, KoreanReading, ChineseReading
from data_fetcher.fetch_decorator import xml_parse

lang_tag_dict = {
    "fr": "French",
    "es": "Spanish",
    "pt": "Portugese",
    None: "English"
}


@xml_parse
def get_kanji(xml):
    """
    create a node_collection and link_collection containing kanji data
    """
    for char_xml in xml.iter('character'):
        kanji = make_kanji(char_xml)
        readings = list(make_readingstuple(char_xml))
        meanings = list(make_meanings(char_xml))
        yield kanji
        yield from meanings
        yield from [read for read, _ in readings]
        yield from make_readlinks(kanji, readings)
        yield from make_meanlinks(kanji, meanings)


def make_kanji(xml):
    misc = xml.find('misc')
    radical_number = [rad.text for rad in xml.iter('rad_value') if rad.attrib['rad_type'] == 'classical'][0]
    return Kanji(writing=xml.find('literal').text,
                 stroke_count=[int(strk.text) for strk in misc.findall('stroke_count')],
                 radical_number=radical_number,
                 kanji_frequency=misc.find('freq').text if misc.findall('freq') else "",
                 kanji_grade=misc.find('grade').text if misc.findall('grade') else "",
                 kanji_jlpt=misc.find('jlpt').text if misc.findall('jlpt') else ""
                 )


def make_meanings(character_xml):
    yield from [Meaning(value=m.text, tags=[lang_tag_dict[m.attrib.get('m_lang', None)] or []])
                for m in character_xml.iter('meaning')]


def make_readingstuple(character_xml):
    for read in character_xml.iter("reading"):
        if read.attrib['r_type'] in ['ja_on', 'ja_kun']:
            yield (JapaneseReading(reading=read.text),
                   {'type_reading': read.attrib['r_type'].replace('ja_', '')})
        if read.attrib['r_type'] in ['korean_r', 'korean_h']:
            yield (KoreanReading(reading=read.text), {})
        if read.attrib['r_type'] == "pinyin":
            yield (ChineseReading(reading=read.text), {})


def make_readlinks(kanji, readings):
    yield from (KanjiIsPronounced(begin_node=kanji, end_node=reading, **props)
                for reading, props in readings)


def make_meanlinks(kanji, meanings):
    yield from (HasMeaning(begin_node=kanji, end_node=meaning)
                for meaning in meanings)
