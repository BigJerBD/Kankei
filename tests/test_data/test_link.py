import unittest

from data.elements.link import SimplifiedLink
from data.elements.node import SimplifiedNode
from data.elements.proprety_types import String


class TestLink(unittest.TestCase):
    class NodeData(SimplifiedNode):
        identifier = 'name'
        fields = {
            'name': String()
        }

    class LinkData(SimplifiedLink):
        fields = {
            'element1': String(),
            'element2': String()
        }

        def _post_init(self):
            if self.props['element2'] == 'value2':
                self.props['element2'] = 'new_value2'

    begin = NodeData(name='begin')
    end = NodeData(name='end')
    link = LinkData(begin_node=begin, end_node=end, element1='value1', element2='value2')

    result_csv = {
        'element1:string': 'value1',
        'element2:string': 'new_value2',
        ':TYPE': 'LinkData',
        ':START_ID(NodeData-ID)': 'begin',
        ':END_ID(NodeData-ID)': 'end'
    }

    def test_begin_node(self):
        self.assertEqual(self.link.begin_node.props['name'],
                         self.begin.props['name'])

    def test_end_node(self):
        self.assertEqual(self.link.end_node.props['name'],
                         self.end.props['name'])

    def test_first_data(self):
        self.assertEqual(self.link.props['element1'], 'value1')

    def test_second_modified_data(self):
        self.assertEqual(self.link.props['element2'], 'new_value2')

    def test_csv(self):
        self.assertEqual(self.link.neo4j_csv, self.result_csv)


if __name__ == '__main__':
    unittest.main()
