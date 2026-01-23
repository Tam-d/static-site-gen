from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}" })
        case TextType.IMAGE:
            return LeafNode("img", "", {"alt": f"{text_node.text}"})
        case _:
            raise Exception("Text node's type is not valid")
        


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        for key, val in self.__dict__.items():
            if not val == other.__dict__[key]:
                return False
        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}{f", {self.url}" if self.url else ""})"


