import unittest

import language.japanese as jp
from data.elements.proprety_types import List, Int


class TestTypes(unittest.TestCase):


    def test_same_type_generic_list(self):
        self.assertTrue(List() == List(Int) )

    def test_not_same_type_generic_list(self):
        self.assertTrue( List() != Int() )

    def test_same_type(self):
        x = List(Int())
        self.assertEqual( x, x )

    def test_not_same_type(self):
        self.assertTrue( List(Int) != (Int()))

if __name__ == '__main__':
    unittest.main()
