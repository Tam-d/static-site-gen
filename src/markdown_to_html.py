from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode

from markdown_parser import BlockType
from markdown_parser import markdown_to_blocks
from markdown_parser import block_to_block_type
from markdown_parser import text_to_textnodes

def text_to_children_html_nodes(text):
    child_html_nodes = []
    
    child_text_nodes = text_to_textnodes(text)

    for child_text_node in child_text_nodes:
        child_html_nodes.append(
            text_node_to_html_node(child_text_node)
        )

    return child_html_nodes

def paragraph_to_html_node(md_block):
    child_html_nodes = text_to_children_html_nodes(md_block)
    return ParentNode("p", child_html_nodes, None)

def heading_to_html_node(md_block):
    heading_split = md_block.split(" ", 1)
    heading_value = len(heading_split[0])

    child_html_nodes = text_to_children_html_nodes(heading_split[1])
    return ParentNode(f"h{heading_value}", child_html_nodes, None)

def code_to_html_node(md_block):
    child_html_nodes = [
        text_node_to_html_node(
            TextNode(md_block.split('```', 2)[1], TextType.TEXT, None)
        )
    ]

    code_html_node = ParentNode("code", child_html_nodes, None)

    return ParentNode("pre", [code_html_node], None)

def quote_to_html_node(md_block):
    block_lines = md_block.split("\n")
    parsed_lines = []

    for line in block_lines:
        if not line.startswith(">"):
            raise ValueError("Not a valid quote line")
        stripped_line = line.lstrip(">").strip()
        parsed_lines.append(stripped_line) 

    block_content = " ".join(parsed_lines)
    child_html_nodes = text_to_children_html_nodes(block_content)

    return ParentNode("blockquote", child_html_nodes, None)

def ul_to_html_node(md_block):
    list_items = md_block.split("\n")
    list_item_nodes = []
    for li in list_items:
        if li != "":
            item_text = li[2:]
            item_child_nodes = text_to_children_html_nodes(item_text)
            list_item_nodes.append(ParentNode("li", item_child_nodes, None))
    
    return ParentNode("ul", list_item_nodes, None)

def ol_to_html_node(md_block):
    list_items = md_block.split("\n")
    list_item_nodes = []
    for li in list_items:
        if li != "":
            item_text = li.split(". ")[1]
            item_child_nodes = text_to_children_html_nodes(item_text)
            list_item_nodes.append(ParentNode("li", item_child_nodes, None))
    
    return ParentNode("ol", list_item_nodes, None)

def block_to_html_node(md_block):

    block_type = block_to_block_type(md_block)

    match(block_type):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(md_block)
        case BlockType.HEADING:
            return heading_to_html_node(md_block)
        case BlockType.CODE:
            return code_to_html_node(md_block)
        case BlockType.QUOTE:
            return quote_to_html_node(md_block)
        case BlockType.UNORDERED_LIST:
            return ul_to_html_node(md_block)
        case BlockType.ORDERED_LIST:
            return ol_to_html_node(md_block)
        case _:
            raise Exception("Unable to determine tag")

def markdown_to_html_node(markdown):

    markdown_blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for md_block in markdown_blocks:
        html_nodes.append(block_to_html_node(md_block))
    
    document_parent = ParentNode("div", html_nodes, None)

    return document_parent