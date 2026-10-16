import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_standard(self):
        # Testet den normalen Ablauf mit Überschrift, Absatz und Liste
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        # Testet, ob multiple Newlines (\n\n\n\n) korrekt ignoriert werden
        md = """
# Heading


Another paragraph here after three newlines.




- List item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Another paragraph here after three newlines.",
                "- List item"
            ]
        )

    def test_markdown_to_blocks_whitespace_handling(self):
        # Testet, ob Leerzeichen am Rand der Blöcke sauber weggeschnitten (.strip()) werden
        md = "   # Heading with leading spaces   \n\n\n   Paragraph with leading spaces   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with leading spaces",
                "Paragraph with leading spaces"
            ]
        )


class TestMarkdownParser(unittest.TestCase):

    # --- Tests für markdown_to_blocks ---
    def test_markdown_to_blocks(self):
        md = """# Das ist eine Überschrift

Dies ist ein normaler Paragraph mit etwas Text.

* Ein Listenpunkt (wird hier als Paragraph gewertet, da kein '-')
* Noch ein Punkt"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# Das ist eine Überschrift")
        self.assertEqual(blocks[1], "Dies ist ein normaler Paragraph mit etwas Text.")

    def test_markdown_to_blocks_excess_whitespace(self):
        md = "\n\n  # Überschrift mit Leerzeichen  \n\n\nParagraph text.  \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "# Überschrift mit Leerzeichen")
        self.assertEqual(blocks[1], "Paragraph text.")


    # --- Tests für block_to_block_type ---
    def test_block_to_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Ungültige Überschriften (Fallback zu Paragraph)
        self.assertEqual(block_to_block_type("####### Zu viele Hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#KeinLeerzeichen"), BlockType.PARAGRAPH)

    def test_block_to_code(self):
        code_block = "```\ndef mein_code():\n    return True\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        # Ungültiger Code-Block laut Boot.dev (da len(lines) == 1)
        self.assertEqual(block_to_block_type("```inline code```"), BlockType.PARAGRAPH)

    def test_block_to_quote(self):
        quote_block = "> Zitat Zeile 1\n> Zitat Zeile 2"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        # Fehlerhaftes Zitat (Zeile 2 hat kein '>')
        invalid_quote = "> Erste Zeile passt\nZweite Zeile bricht die Regel"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_block_to_unordered_list(self):
        ul_block = "- Punkt A\n- Punkt B\n- Punkt C"
        self.assertEqual(block_to_block_type(ul_block), BlockType.ULIST)
        # Fehlerhafte Liste (Zeile 2 fehlt das Leerzeichen nach dem '-')
        invalid_ul = "- Punkt A\n-Punkt B"
        self.assertEqual(block_to_block_type(invalid_ul), BlockType.PARAGRAPH)

    def test_block_to_ordered_list(self):
        ol_block = "1. Erster Eintrag\n2. Zweiter Eintrag\n3. Dritter Eintrag"
        self.assertEqual(block_to_block_type(ol_block), BlockType.OLIST)
        
        # Falsche Nummerierung (Reihenfolge springt)
        invalid_seq = "1. Erster Eintrag\n3. Dritter Eintrag"
        self.assertEqual(block_to_block_type(invalid_seq), BlockType.PARAGRAPH)
        
        # Startet nicht bei 1
        invalid_start = "2. Zweiter Eintrag\n3. Dritter Eintrag"
        self.assertEqual(block_to_block_type(invalid_start), BlockType.PARAGRAPH)

    def test_block_to_paragraph(self):
        paragraph = "Ein ganz normaler Textblock,\nder sich über zwei Zeilen erstreckt."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
