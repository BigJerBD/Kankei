from data.links import *
from data.nodes import *
from data_collectors.fetch_decorator import xml_parse
from language.japanese import has_kanji


@xml_parse
def parse_monash_words(xml):
    """create a node_collection and link_collection containing word data
    """
    for xml in xml.iter('entry'):
        baseread_xmls = get_baseread_xmls(xml)
        words = list(make_words(xml))
        yield from words

        for word in words:
            # link all reading to words
            if baseread_xmls:
                nodes, links = make_readings_and_links(word, baseread_xmls)
                yield from nodes
                yield from links
            read_xmls = find_specific_reading_xml(word, xml)
            if read_xmls:
                nodes, links = make_readings_and_links(word, read_xmls)
                yield from nodes
                yield from links

        for word_semantic in xml.iter('sense'):
            # link all definition to word
            definition = make_definition(xml)
            yield definition

            for word in words:
                yield make_word_def_link(word, definition)

            for name, nodes, links in get_def_and_childs(definition, word_semantic):
                # link all category to definitions
                yield from nodes
                yield from links


def find_specific_reading_xml(word, xml):
    return [w
            for w in xml.findall('r_ele')
            if any(word.props['writing'] == re_restr.text for re_restr in w.findall('re_restr'))
            ]


def get_baseread_xmls(xml):
    return [r for r in xml.findall('r_ele') if not r.findall('re_restr')]


def get_def_and_childs(definition, xml):
    for name, tag, node, link in [
        ('meaning', 'gloss', Meaning, HasMeaning),
        ('pos', 'pos', PartOfSpeech, HasCategory),
        ('misc', 'misc', WordMisc, HasCategory),
        ('dialect', 'dial', Dialect, HasCategory),
        ('field', 'field', Field, HasCategory),
    ]:
        nodes = _make_value_nodes(node, xml, tag)
        links = _make_child_links(link, definition, nodes)
        yield name, nodes, links


def make_words(xml):
    entry_sequence = xml.find('ent_seq').text
    if xml.findall('k_ele'):
        yield from [Word(entry_sequence=entry_sequence,
                         writing=word.find('keb').text,
                         has_kanji=has_kanji(word.find('keb').text),
                         information=[inf.text for inf in word.findall('ke_inf')],
                         priority=[pri.text for pri in word.findall('ke_pri')],
                         ) for word in xml.findall('k_ele')]
    else:
        yield from [Word(entry_sequence=entry_sequence,
                         writing=word.find('reb').text,
                         has_kanji=False,
                         ) for word in xml.findall('r_ele')]


def make_readings_and_links(word, xmls):
    readings = (_make_reading(xml) for xml in xmls)
    return zip(*[(read, _make_reading_link(word, read)) for read in readings])


def make_definition(xml):
    return Definition(entry_sequence=xml.find('ent_seq').text)


def make_word_def_link(word, definition):
    return HasDefinition(begin_node=word, end_node=definition)


def _make_reading(xml):
    return Reading(reading=xml.find('reb').text)


def _make_reading_link(word, read):
    return WordIsPronounced(begin_node=word, end_node=read)


def _make_child_links(cls, begin, end_list):
    return [cls(begin_node=begin, end_node=end) for end in end_list]


def _make_value_nodes(cls, xml, tag):
    return [cls(value=mean.text) for mean in xml.findall(tag)]
