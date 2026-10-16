import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p1(self):
        node = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<p>Hllo, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        # Außen einfache Anführungszeichen verwenden:
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p3(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")
