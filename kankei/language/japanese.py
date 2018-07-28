import re

from jaconv import jaconv
from kanaconv import KanaConv

_HIRAGANA_REGEX= re.compile(r'[\u3040-\u309F]')
_KATAKANA_REGEX = re.compile(r'[\u30A0-\u30FF]')
_KANJI_REGEX = re.compile(r'[\u4E00-\u9FAF]')


def has_hiragana(string):
    """
    :param string:
    :return: boolean saying if word has hiragana
    """
    return bool(_HIRAGANA_REGEX.search(string))


def has_katakana(string):
    """
    :param string:
    :return: boolean saying if word has katakana
    """
    return bool(_KATAKANA_REGEX.search(string))


def has_kanji(string):
    """
    :param string:
    :return: boolean represna
    """
    return bool(_KANJI_REGEX.search(string))


def to_romaji(kana):
    """
    :param kana:
    :return: romaji conversion
    """
    return KanaConv().to_romaji(kana)


def roma_to_kata(roma):
    """
    :param roma:
    :return: katakana conversion
    """
    return jaconv.hira2kata(jaconv.alphabet2kana(roma))


def roma_to_hira(roma):
    """
    :param roma:
    :return: hira conversion
    """
    return jaconv.alphabet2kana(roma)


def kata_to_hira(kata):
    """
    :param kata:
    :return: hira conversion
    """
    return jaconv.kata2hira(kata)


def hira_to_kata(hira):
    """
    :param hira:
    :return: katakana conversion
    """
    return jaconv.hira2kata(hira)


def normalise_character(char):
    """
    normalize japanese character base syntax

    :param char:
    :return: a normalised japanese character
    """
    return char.replace('.', '').replace('-', '')