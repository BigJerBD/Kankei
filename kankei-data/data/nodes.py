from data.elements.node import SimplifiedNode
from data.elements.proprety_types import List, String, Int, Boolean
from language import japanese as jp


def make_singlenode(name, field_name):
    class SingleValueNode(SimplifiedNode):
        __ignore_clsname__ = True
        base_labels = [name]
        type = name

        identifier = field_name
        indexes = [field_name]
        fields = {
            field_name: String()
        }

    return SingleValueNode


# -------- Language Tags ---------

japanese_tag = "Japanese"
chinese_tag = "Chinese"
korean_tag = "Korean"

french_tag = "French"
english_tag = "English"
spanish_tag = "Spanish"
portugese_tag = "Portugese"


# -------- Characters ---------

class Kanji(SimplifiedNode):
    base_labels = [japanese_tag]
    fields = {
        'kanji_grade': String(),
        'kanji_jlpt': String(),
        'kanji_frequency': String(),
        'kanji_joyo': Boolean()
    }

    def _post_init(self):
        self.props['kanji_joyo'] = self.props['kanji_grade'] is not ""


class CharacterPart(SimplifiedNode):
    fields = {
        'component_tag': String()
    }


class Radical(SimplifiedNode):
    indexes = ['radical_number']
    fields = {
        'frequency': Int()
    }


class Character(SimplifiedNode):
    identifier = 'writing'
    indexes = ['writing']
    fields = {
        'writing': String(),
        'stroke_count': List(Int()),
        'radical_number': String()
    }


class ChineseCharacter(Character):
    valid_subcomponents = [Kanji, CharacterPart, Radical]
    fields = {
        'radical_number': String()
    }


# -------- Readings ---------
class Reading(SimplifiedNode):
    ...


class JapaneseReading(Reading):
    __ignore_clsname__ = True
    base_labels = [japanese_tag]
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
    base_labels = [korean_tag]
    identifier = 'latin_read'
    indexes = ['latin_read']
    fields = {
        'hangul': String(),
        'latin_read': String()
    }


class ChineseReading(Reading):
    __ignore_clsname__ = True
    base_labels = [chinese_tag]
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


# --------- SingleValue Node ----------
# confirm if this work

Definition = make_singlenode("Definition", "entry_sequence")
Stroke = make_singlenode("Stroke", "writing")
Dialect = make_singlenode("Dialect", "value")
WordMisc = make_singlenode("WordMisc", "value")
PartOfSpeech = make_singlenode("PartOfSpeech", "value")
Field = make_singlenode("Field", "value")
Meaning = make_singlenode("Meaning","value")
Meaning.valid_extralabels = [english_tag, portugese_tag, french_tag, spanish_tag]
