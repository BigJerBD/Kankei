import unittest

from data import SimplifiedNode
from data.elements.proprety_types import String, List, Int


class TestNode(unittest.TestCase):
    class NodeData(SimplifiedNode):
        identifier = 'writing'
        indexes = ['writing']
        fields = {'writing': String(), 'stroke_count': List(Int())}

    class ChildNodeData(NodeData):
        identifier = 'writing2'
        indexes = ['writing2']
        fields = {'writing2': String()}

    class ChildNodeData2(NodeData):
        fields = {'writing3': String()}

    node = NodeData(writing='writing1', stroke_count=[7, 8])
    childnode = ChildNodeData(writing2='writing2', writing='writing1', stroke_count=[8, 9])
    childnode2 = ChildNodeData2(writing3='writing3', writing='writing1', stroke_count=[8, 9])

    def test_node_data(self):
        res_props = {'writing': 'writing1', 'stroke_count': [7, 8]}
        self.assertEqual(res_props, self.node.props)

    def test_node_csv(self):
        res_csv = {':LABEL': 'NodeData',
                   'ID(NodeData-ID)': 'writing1',
                   'stroke_count:int[]': '7;8'}
        self.assertEqual(res_csv, self.node.csv)

    def test_childnode_data(self):
        res_props = {'writing': 'writing1','writing2':'writing2', 'stroke_count': [8, 9]}
        self.assertEqual(res_props, self.childnode.props)

    def test_childnode_csv(self):
        res_csv = {':LABEL': 'ChildNodeData;NodeData',
                   'ID(ChildNodeData-ID)': 'writing2',
                   'writing:string': 'writing1',
                   'stroke_count:int[]': '8;9'}
        self.assertEqual(res_csv, self.childnode.csv)

    def test_childnode2_csv(self):
        res_csv = {':LABEL': 'ChildNodeData2;NodeData',
                   'ID(NodeData-ID)': 'writing1',
                   'writing3:string': 'writing3',
                   'stroke_count:int[]': '8;9'}
        self.assertEqual(res_csv, self.childnode2.csv)


if __name__ == '__main__':
    unittest.main()
