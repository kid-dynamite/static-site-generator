import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(props= {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')
    
    def test_props_to_html_multiple(self):
        node2 = HTMLNode(props= {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node2.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_none(self):
        node3 = HTMLNode()
        self.assertEqual(node3.props_to_html(), "")

class TestHTMLNode(unittest.TestCase):
    def test_to_html_with_children(self):
        
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_multiple_children(self):
        # Testet, ob mehrere Kinder auf derselben Ebene korrekt kombiniert werden
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i></p>"
        )

    def test_to_html_with_props(self):
        # Testet, ob Attribute (wie href oder class) richtig gerendert werden
        node = ParentNode(
            "a",
            [LeafNode("span", "Click me")],
            {"href": "https://google.com", "class": "link-style"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://google.com" class="link-style"><span>Click me</span></a>'
        )

    def test_headings(self):
        # Ein einfacherer Test mit Überschriften
        node = ParentNode(
            "h1",
            [LeafNode("b", "Big Title")],
        )
        self.assertEqual(node.to_html(), "<h1><b>Big Title</b></h1>")


