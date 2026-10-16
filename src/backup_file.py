from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        # Wenn es kein reiner TEXT-Knoten ist, ignorieren wir ihn und fügen ihn unverändert hinzu
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Wenn der Delimiter nicht im Text vorkommt, bleibt der Knoten wie er ist
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
            
        # Wir splitten den Text am Delimiter
        parts = old_node.text.split(delimiter)
        
        # Ein valides Markdown-Paar (z.B. `code`) sorgt immer für eine ungerade Anzahl an Teilen.
        # Wenn die Anzahl gerade ist, fehlt ein schließender Delimiter!
        if len(parts) % 2 == 0:
            raise ValueError(f"Ungültige Markdown-Syntax: Schließender Delimiter '{delimiter}' nicht gefunden.")
            
        # Wir gehen durch alle gesplitteten Teile
        for i, part in enumerate(parts):
            # Leere Strings (z.B. wenn der Delimiter ganz am Anfang/Ende steht) überspringen wir
            if part == "":
                continue
                
            # Gerade Indizes (0, 2, 4...) sind normaler Text
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            # Ungerade Indizes (1, 3, 5...) liegen zwischen den Delimitern -> Ziel-Typ
            else:
                new_nodes.append(TextNode(part, text_type))
                
    return new_nodes


def extract_markdown_images(text):
    # Findet Bilder im Format: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Findet normale Links im Format: [anchor text](url)
    # Nutzt einen negierten Lookbehind (?<!!), damit Bilder ignoriert werden
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # Wenn es kein reiner TEXT-Knoten ist, ignorieren wir ihn und fügen ihn unverändert hinzu
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        link_text = extract_markdown_links(old_node.text)
        if not link_text:
            new_nodes.append(old_node)
            continue
        #return link_text

        link_parts = []
        #parts = old_node.text.split()
        for link in link_text:
            full_link = f"[{link[0]}]({link[1]})"
            link_parts.append(full_link)
        #return link_parts
        # Wir starten mit dem vollen Text des Knotens
        current_text = old_node.text
        
        # Jetzt gehen wir durch JEDEN extrahierten Link einzeln durch
        for i, full_link in enumerate(link_parts):
            # Wir splitten den aktuellen Text am aktuellen Link in maximal 2 Teile:
            # parts[0] ist der Text VOR dem Link
            # parts[1] ist der gesamte RESTliche Text NACH dem Link
            parts = current_text.split(full_link, 1)
            
            # Wenn der Split fehlschlägt (sollte nicht passieren), abbrechen
            if len(parts) < 2:
                break
                
            # 1. Text VOR dem Link hinzufügen (falls er nicht leer ist)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # 2. Den eigentlichen Link-Knoten hinzufügen
            # link_text[i][0] ist der Anchor-Text, link_text[i][1] die URL
            new_nodes.append(TextNode(link_text[i][0], TextType.LINK, link_text[i][1]))
            
            # 3. Der RESTliche Text wird die Basis für den nächsten Schleifendurchlauf
            current_text = parts[1]
            
        # Wenn nach dem ALLERLETZTEN Link noch Text übrig ist, fügen wir ihn hinzu
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes
        

            from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        # Wenn es kein reiner TEXT-Knoten ist, ignorieren wir ihn und fügen ihn unverändert hinzu
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Wenn der Delimiter nicht im Text vorkommt, bleibt der Knoten wie er ist
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
            
        # Wir splitten den Text am Delimiter
        parts = old_node.text.split(delimiter)
        
        # Ein valides Markdown-Paar (z.B. `code`) sorgt immer für eine ungerade Anzahl an Teilen.
        # Wenn die Anzahl gerade ist, fehlt ein schließender Delimiter!
        if len(parts) % 2 == 0:
            raise ValueError(f"Ungültige Markdown-Syntax: Schließender Delimiter '{delimiter}' nicht gefunden.")
            
        # Wir gehen durch alle gesplitteten Teile
        for i, part in enumerate(parts):
            # Leere Strings (z.B. wenn der Delimiter ganz am Anfang/Ende steht) überspringen wir
            if part == "":
                continue
                
            # Gerade Indizes (0, 2, 4...) sind normaler Text
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            # Ungerade Indizes (1, 3, 5...) liegen zwischen den Delimitern -> Ziel-Typ
            else:
                new_nodes.append(TextNode(part, text_type))
                
    return new_nodes


def extract_markdown_images(text):
    # Findet Bilder im Format: ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Findet normale Links im Format: [anchor text](url)
    # Nutzt einen negierten Lookbehind (?<!!), damit Bilder ignoriert werden
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)



def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        # Wenn es kein reiner TEXT-Knoten ist, ignorieren wir ihn und fügen ihn unverändert hinzu
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        link_text = extract_markdown_links(old_node.text)
        if not link_text:
            new_nodes.append(old_node)
            continue
        #return link_text

        link_parts = []
        #parts = old_node.text.split()
        for link in link_text:
            full_link = f"[{link[0]}]({link[1]})"
            link_parts.append(full_link)
        #return link_parts
        # Wir starten mit dem vollen Text des Knotens
        current_text = old_node.text
        
        # Jetzt gehen wir durch JEDEN extrahierten Link einzeln durch
        for i, full_link in enumerate(link_parts):
            # Wir splitten den aktuellen Text am aktuellen Link in maximal 2 Teile:
            # parts[0] ist der Text VOR dem Link
            # parts[1] ist der gesamte RESTliche Text NACH dem Link
            parts = current_text.split(full_link, 1)
            
            # Wenn der Split fehlschlägt (sollte nicht passieren), abbrechen
            if len(parts) < 2:
                break
                
            # 1. Text VOR dem Link hinzufügen (falls er nicht leer ist)
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # 2. Den eigentlichen Link-Knoten hinzufügen
            # link_text[i][0] ist der Anchor-Text, link_text[i][1] die URL
            new_nodes.append(TextNode(link_text[i][0], TextType.LINK, link_text[i][1]))
            
            # 3. Der RESTliche Text wird die Basis für den nächsten Schleifendurchlauf
            current_text = parts[1]
            
        # Wenn nach dem ALLERLETZTEN Link noch Text übrig ist, fügen wir ihn hinzu
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes
        

            