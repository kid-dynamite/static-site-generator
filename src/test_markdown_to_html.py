import unittest
from htmlnode import HTMLNode, ParentNode
from markdown_blocks import (
    markdown_to_html_node,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    olist_to_html_node,
    ulist_to_html_node,
    quote_to_html_node
)

class TestMarkdownToHTML(unittest.TestCase):

    # --- Tests für die Hauptfunktion (Gesamtes Dokument) ---
    def test_markdown_to_html_node_full_document(self):
        md = """# Heading 1

This is a paragraph with **bold** text.

- Item 1
- Item 2"""
        
        node = markdown_to_html_node(md)
        
        # Das Ergebnis muss ein div-ParentNode sein
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        
        # Einzelne Blöcke prüfen
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "ul")

    # --- Tests für Überschriften (Headings) ---
    def test_heading_to_html_node_h1(self):
        block = "# Just H1"
        node = heading_to_html_node(block)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.children[0].value, "Just H1")

    def test_heading_to_html_node_h3(self):
        block = "### Heading Level 3"
        node = heading_to_html_node(block)
        self.assertEqual(node.tag, "h3")
        self.assertEqual(node.children[0].value, "Heading Level 3")

    # --- Tests für Absätze (Paragraphs) ---
    def test_paragraph_to_html_node(self):
        block = "This is a simple paragraph."
        node = paragraph_to_html_node(block)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children[0].value, "This is a simple paragraph.")

    def test_paragraph_with_inline_markdown(self):
        block = "Paragraph with **bold** and *italic*."
        node = paragraph_to_html_node(block)
        self.assertEqual(node.tag, "p")
        # Geprüft wird die Aufteilung durch text_to_children
        self.assertEqual(node.children[0].value, "Paragraph with ")
        self.assertEqual(node.children[1].tag, "b")
        self.assertEqual(node.children[1].value, "bold")

    # --- Tests für Code-Blöcke ---
    def test_code_to_html_node_bootdev_style(self):
        # Boot.dev verlangt exakt dieses Format (inkl. Newlines für den Index [4:-3])
        block = "```\nx = 10\nprint(x)\n```"
        node = code_to_html_node(block)
        
        # Äußerer Knoten muss <pre> sein
        self.assertEqual(node.tag, "pre")
        
        # Innerer Knoten muss <code> sein
        code_child = node.children[0]
        self.assertEqual(code_child.tag, "code")
        
        # Inhalt prüfen (Boot.dev-Slicing lässt das abschließende \n stehen)
        self.assertEqual(code_child.children[0].value, "x = 10\nprint(x)\n")

    # --- Tests für Listen (Ordered & Unordered) ---
    def test_ulist_to_html_node(self):
        block = "- Apple\n- Banana\n- Cherry"
        node = ulist_to_html_node(block)
        
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "Apple")

    def test_olist_to_html_node(self):
        block = "1. First\n2. Second"
        node = olist_to_html_node(block)
        
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(node.children[1].children[0].value, "Second")

    # --- Tests für Zitate (Quotes) ---
    def test_quote_to_html_node(self):
        block = "> Life is beautiful\n> - A Peacock"
        node = quote_to_html_node(block)
        
        self.assertEqual(node.tag, "blockquote")
        # Zeilenumbrüche werden laut Musterlösung durch Leerzeichen ersetzt
        self.assertEqual(node.children[0].value, "Life is beautiful - A Peacock")


if __name__ == "__main__":
    unittest.main()
