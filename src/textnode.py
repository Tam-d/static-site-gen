from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

def match_delimiter(delimiter):
    match(delimiter):

        case "**":
            return TextType.BOLD
        case "_":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case _:
            raise Exception("Invalid delimiter provided")

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
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_list = old_node.text.split(delimiter, 2)

            if len(split_list) != 3:
                raise Exception("Unable to split, invalid Markdown syntax")
            
            new_nodes.extend(
                [
                    TextNode(split_list[0], TextType.TEXT),
                    TextNode(split_list[1], match_delimiter(delimiter)),
                    TextNode(split_list[2], TextType.TEXT),
                ]               
            )
            
    return new_nodes

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


