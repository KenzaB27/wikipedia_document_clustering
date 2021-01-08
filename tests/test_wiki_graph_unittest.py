
import unittest
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from clustering.wiki_graph import WikiNode, WikiGraph, WikiCluster

class WikiNodeTest(unittest.TestCase):

    def test_create_wiki_node(self):
        """Test that we can create a node properly."""

        wiki_node1 = WikiNode(0, 't1', ['c1', 'c2', 'c3'], 'top1')
        self.assertEqual(wiki_node1.get_topic(),
                         'top1', 'Topic should be top1')
        self.assertEqual(wiki_node1.get_id(), 0, 'Id should be 0')

    def test_constraint_on_nb_tokens(self):
        """ Test min number of tokens constraint """
        n1 = WikiNode(0, 't1', ['c1', 'c2', 'c3'], 'top1')
        n2 = WikiNode(1, 't2', ['d1', 'c2', 'c3'], 'top2')
        n3 = WikiNode(2, 't3', ['mo', 'c2', 'l3', 'lj'], 'top3')

        n1.add_wiki_neighbor(n2, constraint=2)
        n1.add_wiki_neighbor(n3, constraint=2)
        self.assertTrue(n3 not in n1.wiki_neighbors)
        self.assertTrue(n2 in n1.wiki_neighbors)

    def test_weight_of_edges(self):
        """ Test min number of tokens constraint """
        n1 = WikiNode(0, 't1', ['c1', 'c2', 'c3',
                                'c3', 'c3', 'c4', 'c5'], 'top1')
        n2 = WikiNode(1, 't2', ['d1', 'c2', 'c3'], 'top2')
        n3 = WikiNode(2, 't3', ['mo', 'c2', 'l3', 'lj', 'c3', 'c4'], 'top3')

        n1.add_wiki_neighbor(n2)
        n1.add_wiki_neighbor(n3)
        self.assertEqual(n1.get_weight(n3), 3,
                         "Number of common topics should be 3")
        self.assertEqual(n1.get_weight(n2), 2,
                         "Number of common topics should be 2")

class WikiGraphTest(unittest.TestCase):

    def test_create_wiki_graph(self):
        """Test that we can create a graph properly."""
        g = WikiGraph()
        num_nodes = 15
        n = {"title": 't1', "content": [
            'c1', 'c2', 'c3'], "topic": 'top1'}
        nodes = [n]*num_nodes
        for i, n in enumerate(nodes):
            g.add_wiki_node(i, n)
        self.assertEqual(g.num_wiki_nodes, 15, "Num of nodes should be 15")

    def test_create_wiki_graph(self):
        """Test that we can build a graph properly."""
        g = WikiGraph()
        num_nodes = 20
        n = {"title": 't1', "content": [
            'c1', 'c2', 'c3'], "topic": 'top1'}
        pages = [n]*num_nodes
        g.build_graph(pages)
        num_edges = sum([len(g.wiki_nodes[n].wiki_neighbors)
                         for n in g.wiki_nodes])
        self.assertEqual(num_edges, 380, "Num of edges should be 380")

class WikiClusterTest(unittest.TestCase):
    def test_create_cluster(self):
        """ Test that we can create a cluster properly"""
        n1 = WikiNode(0, 't1', ['c1', 'c2', 'c3',
                                'c3', 'c3', 'c4', 'c5'], 'top1')
        n2 = WikiNode(1, 't2', ['d1', 'c2', 'c3'], 'top2')
        n3 = WikiNode(2, 't3', ['mo', 'c2', 'l3', 'lj', 'c3', 'c4'], 'top3')
        wiki_cluster = WikiCluster()
        wiki_cluster.add_wiki_node(n1)
        wiki_cluster.add_wiki_node(n2)
        wiki_cluster.add_wiki_node(n3)
        self.assertEqual(len(wiki_cluster.wiki_nodes),3)
        
if __name__ == '__main__':
    unittest.main()
