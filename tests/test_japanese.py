import unittest

import language.japanese as jp


class TestJapanese(unittest.TestCase):

    def test_has_kata(self):
        self.assertEqual(True, jp.has_katakana('カタカナ'))

    def test_has_no_kata(self):
        self.assertEqual(False, jp.has_katakana('ひらがな'))

    def test_has_hira(self):
        self.assertEqual(True, jp.has_hiragana('ひらがな'))

    def test_has_no_hira(self):
        self.assertEqual(True, jp.has_hiragana('かたかな'))

    def test_has_kanji(self):
        self.assertEqual(True, jp.has_kanji('漢字'))

    def test_has_no_kanji(self):
        self.assertEqual(False, jp.has_kanji('かなだ'))

if __name__ == '__main__':
    unittest.main()
