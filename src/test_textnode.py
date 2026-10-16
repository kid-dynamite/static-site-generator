import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)
    
    def test_eq1(self):
        node5 = TextNode("This is a text node", TextType.BOLD, None)
        node6 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node5, node6)

    def test_not_not_eq1(self):
        node7 = TextNode("This is text node", TextType.BOLD)
        node8 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node7, node8)

    def test_not_not_eq2(self):
        node77 = TextNode("This is text node", TextType.BOLD, "https://www.boot.dev/")
        node88 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node77, node88)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a raw text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a raw text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("Cute cat picture", TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {"src": "https://example.com", "alt": "Cute cat picture"}
        )

    def test_invalid_type(self):
        # Falls ein ungültiger Typ durchrutscht (z. B. None oder ein String statt Enum)
        node = TextNode("Invalid node", "not_a_valid_enum_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    
    
    


if __name__ == "__main__":
    unittest.main()
