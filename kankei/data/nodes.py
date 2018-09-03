from data.elements.node import SimplifiedNode
from data.elements.proprety_types import List, String, Int, Boolean
from language import japanese as jp


class Character(SimplifiedNode):
    identifier = 'writing'
    indexes = ['writing']
    fields = {
        'writing': String(),
        'stroke_count': List(Int()),
        'radical_number': String()
    }


class Kanji(Character):
    __ignore_clsname__ = True
    labels = ["Japanese"]
    fields = {
        'kanji_grade': String(),
        'kanji_jlpt': String(),
        'kanji_frequency': String(),
        'kanji_joyo': Boolean()
    }

    def _post_init(self):
        self.props['kanji_joyo'] = self.props['kanji_grade'] is not ""


class Component(Character):
    fields = {
        'component_tag': String()
    }


class Radical(Character):
    indexes = ['radical_number']
    fields = {
        'frequency': Int()
    }


class Reading(SimplifiedNode): ...


class JapaneseReading(Reading):
    __ignore_clsname__ = True
    labels = ["Japanese"]
    identifier = 'hiragana'
    indexes = ['hiragana']
    fields = {
        'hiragana': String(),
        'katakana': String(),
        'romaji': String()
    }
    parameters = ['reading']

    def _post_init(self, reading):
        reading = reading.replace('-', '').replace('.', '')

        if jp.has_hiragana(reading):
            self.props['hiragana'] = reading
            self.props['katakana'] = jp.hira_to_kata(reading)
            self.props['romaji'] = jp.to_romaji(reading)
        elif jp.has_katakana(reading):
            self.props['hiragana'] = jp.kata_to_hira(reading)
            self.props['katakana'] = reading
            self.props['romaji'] = jp.to_romaji(reading)
        else:
            self.props['romaji'] = reading
            self.props['hiragana'] = jp.roma_to_hira(reading)
            self.props['katakana'] = jp.roma_to_kata(reading)


class KoreanReading(Reading):
    __ignore_clsname__ = True
    labels = ["Korean"]
    identifier = 'reading'
    indexes = ['reading']
    fields = {
        'reading': String()
    }

    def _post_init(self):
        ...
        # parse hangul reading


class ChineseReading(Reading):
    __ignore_clsname__ = True
    labels = ['Chinese']
    identifier = 'reading'
    indexes = ['reading']
    fields = {
        'reading': String()
    }


class Word(SimplifiedNode):
    identifier = 'word_id'
    indexes = ['entry_sequence', 'writing', 'word_id']
    fields = {
        'entry_sequence': String(),
        'writing': String(),
        'word_id': String(),
        'information': String(),
        'priority': String(),
        'has_kanji': Boolean(),
    }

    def _post_init(self):
        self.props['word_id'] = self.props['entry_sequence'] + self.props['writing']


class Definition(SimplifiedNode):
    indexes = ['entry_sequence']
    identifier = 'entry_sequence'
    fields = {
        'entry_sequence': String()
    }


class Stroke(SimplifiedNode):
    identifier = 'writing'
    indexes = ['writing']
    fields = {
        'writing': String()
    }


class Meaning(SimplifiedNode):
    identifier = 'value'
    indexes = ['value']
    fields = {
        'value': String()
    }


class Dialect(SimplifiedNode):
    identifier = 'value'
    indexes = ['value']
    fields = {
        'value': String()
    }


class WordMisc(SimplifiedNode):
    identifier = 'value'
    indexes = ['value']
    fields = {
        'value': String()
    }


class PartOfSpeech(SimplifiedNode):
    identifier = 'value'
    indexes = ['value']
    fields = {
        'value': String()
    }


class Field(SimplifiedNode):
    identifier = 'value'
    indexes = ['value']
    fields = {
        'value': String()
    }
