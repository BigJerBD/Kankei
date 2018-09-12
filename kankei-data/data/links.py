from data.elements.link import SimplifiedLink
from data.elements.proprety_types import Int, String, List
from language import japanese as jp

HasCategory = SimplifiedLink
HasDefinition = SimplifiedLink
HasMeaning = SimplifiedLink
HasRadical = SimplifiedLink


class HasStroke(SimplifiedLink):
    fields = {
        'position': List(String()),
        'stroke': String(),
        'vec_coord': String(),
        'stroke_number': Int()
    }


class HasWord(SimplifiedLink):
    fields = {
        'position': String()
    }


class IsWrittenWith(SimplifiedLink):
    fields = {
        'position': List(String()),

    }


class IsRelated(SimplifiedLink):
    fields = {
        'score': Int(),
        'type': String()
    }


class KanjiIsPronounced(SimplifiedLink):
    fields = {
        'type_reading': String()
    }


class WordIsPronounced(SimplifiedLink):
    fields = {
        'type_reading': String(),
        'information': String(),
        'priority': String(),
        'reading': String()
    }

    def _post_init(self):
        reading = self.props['reading']
        self.props['type_reading'] = (
            'both' if jp.has_katakana(reading) and jp.has_hiragana(reading) else
            'katakana' if jp.has_katakana(reading) else
            'hiragana'
        )
