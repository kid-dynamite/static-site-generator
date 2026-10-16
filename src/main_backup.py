from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
from blocks import markdown_to_blocks, block_to_block_type

def main():
    # Test-Knoten erstellen
    node = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    #print(node) #__repr__ Methode
    """
    node = TextNode("**This** is text with a code block word", TextType.TEXT)
    node_1 = TextNode("This is text with a **code block** word", TextType.TEXT)
    node_2 = TextNode("This is text with a code block **word**", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node, node_1, node_2], "**", TextType.BOLD)
    print(node)
    print(f"new_node: {new_nodes}")
    
    node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
    new_nodes = split_nodes_link([node])
    print(new_nodes)
    

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))
    """

    md = """
# Das ist eine Überschrift mit extra Newlines am Anfang

Hier ist ein normaler Textabschnitt mit **fettem** Inhalt.
Der Absatz geht hier auf der nächsten Zeile weiter.



- Das hier ist der erste Punkt einer Liste
- Und das hier ist der zweite Punkt
"""

    #print(markdown_to_blocks(md))

#unorderd_lst = '- Das hier ist der erste Punkt einer Liste\n- Und das hier ist der zweite Punkt'

#print(block_to_block_type(unorderd_lst))

    
    

if __name__ == "__main__":
    main()

