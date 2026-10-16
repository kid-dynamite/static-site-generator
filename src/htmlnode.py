class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list["HTMLNode"]=None, props: dict=None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""

        a_string : str= ""
        for key, value in self.props.items():
            a_string += f' {key}="{value}"'
        return a_string

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("object doesn't have a tag")
        if self.children is None:
            raise ValueError("children is missing")
        children_html = ""
        for child in self.children:
            # Hier passiert die Magie: Jedes Kind wandelt sich selbst in HTML um
            children_html += child.to_html()
            
        # 3. Den Eltern-Tag um die gesammelten Kinder herumschließen
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
        
    
    
    def print_node(self):           
        
        return self.children


"""
===============================================================================
ZUSAMMENFASSUNG: WIE PYTHON OBJEKTE IN LISTEN DARSTELLT (__repr__ & print)
===============================================================================

1. DAS PROBLEM MIT .join()
   - Die Methode `", ".join(lst)` funktioniert NUR, wenn in der Liste reine 
     Strings (Text) liegen.
   - Wenn du mit `lst.append(child)` die rohen HTMLNode-Objekte in die Liste packst,
     kann `.join()` damit nichts anfangen und wirft einen `TypeError`.

2. DIE LÖSUNG ÜBER DIE LISTE (Warum `return lst` funktionierte)
   - Wenn du `return lst` schreibst und diese Liste mit `print()` ausgibst,
     übernimmt Python die Arbeit für dich.
   - Python geht automatisch durch die Liste und ruft für JEDES darin enthaltene
     Objekt dessen eigene `__repr__`-Methode auf, um es als Text anzuzeigen.

3. DER UNSICHTBARE ZWISCHENSCHRITT (Warum dort "HTMLNode" stand)
   - In deinem Code hattest du die `__repr__`-Methode in der Unterklasse 
     `ParentNode` auskommentiert.
   - Wenn Python ein `ParentNode`-Objekt in der Liste darstellen will, sucht es 
     nach dessen `__repr__`. Da keine da war, griff die Vererbung: Python sprang 
     eine Ebene höher in die Hauptklasse `HTMLNode`.
   - Weil dort das Wort "HTMLNode" fest im Text stand, wurde für dein `ParentNode` 
     fälschlicherweise "HTMLNode(...)" ausgegeben.

4. BEST PRACTICE FÜR EINE DYNAMISCHE __repr__ IN DER HAUPTKLASSE:
   Anstatt den Namen der Klasse fest in den String zu schreiben, kannst du
   Python den Namen der aktuellen Klasse (auch der Unterklassen!) automatisch
   herausfinden lassen:

   def __repr__(self):
       class_name = self.__class__.__name__  # Holt dynamisch "ParentNode", "LeafNode" etc.
       return f"{class_name}({self.tag}, {self.value}, {self.children}, {self.props})"
===============================================================================
"""


    
        




