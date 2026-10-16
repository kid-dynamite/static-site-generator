import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("Hello **world** extract this", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" extract this", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_missing_delimiter(self):
        node = TextNode("This is **broken markdown", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://imgur.com)"
        )
        self.assertListEqual([("image", "https://imgur.com")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://boot.dev")], matches)


    # Füge diese Testmethoden in deine bestehende Test-Klasse (z. B. class TestTextNode(unittest.TestCase):) ein

    def test_split_images(self):
        # Der offizielle Test aus der Aufgabenstellung
        node = TextNode(
            "This is text with an ![image](https://imgur.com) and another ![second image](https://imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://imgur.com"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        # Test für normale Links aus dem Beispiel der Aufgabe
        node = TextNode(
            "This is text with a link [to boot dev](https://boot.dev) and [to youtube](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_split_no_images_or_links(self):
        # Testet, ob Text ohne Links/Bilder einfach unverändert bleibt
        node = TextNode("This is just plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_consecutive_links(self):
        # Wichtiger Edge-Case: Zwei Links direkt hintereinander ohne Text dazwischen
        node = TextNode("[first](https://link1.com)[second](https://link2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://link1.com"),
                TextNode("second", TextType.LINK, "https://link2.com"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all_markdown_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_plain_text(self):
        text = "Just plain text without markdown elements."
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text without markdown elements.", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_consecutive_formatting(self):
        text = "**Bold**_Italic_`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
