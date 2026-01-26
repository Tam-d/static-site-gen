from textnode import TextType, TextNode
import re

#![image](https://i.imgur.com/zjjcJKZ.png)

IMAGE_EXTRACT_REGEX= r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_EXTRACT_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

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
        
def extract_markdown_images(text):
    return re.findall(IMAGE_EXTRACT_REGEX, text)

def extract_markdown_links(text):
    return re.findall(LINK_EXTRACT_REGEX, text)

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

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            image_tuples = extract_markdown_images(old_node.text)

            print(f"Image tuples: {image_tuples}")

            extraction_data = []

            for img_alt, img_link in image_tuples:
                extraction_data.append(
                    (img_alt, img_link, f"![{img_alt}]({img_link})", TextType.IMAGE)
                )

            new_nodes.extend(
                proccess_extraction_data(
                    extraction_data,
                    old_node.text,
                )
            )
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            link_tuples = extract_markdown_links(old_node.text)

            extraction_data = []

            for link_anchor, link in link_tuples:
                extraction_data.append(
                    (link_anchor, link, f"[{link_anchor}]({link})", TextType.LINK)
                )

            new_nodes.extend(
                proccess_extraction_data(
                    extraction_data,
                    old_node.text,
                )
            )
    return new_nodes

def proccess_extraction_data(extraction_data, text):
    new_nodes = []

    if len(extraction_data) > 0:
        for extracted_text, extracted_link, split_on, text_type in extraction_data:
            
            text_after_split = text.split(split_on, 1)
            
            new_nodes.extend(
                process_split(
                    extracted_text, 
                    extracted_link, 
                    text_after_split, 
                    text_type
                )
            )

            # set the text to the rest of the split
            text = text_after_split[1]

        #if anything is left over, create a text node for it
        if len(text) >= 2 and text[1] != "":
            new_nodes.append(TextNode(text,TextType.TEXT))

    else:
        new_nodes.append(TextNode(
            text,
            TextType.TEXT
        ))

    return new_nodes

def process_split(extracted_text, extracted_link, text, text_type):
    new_nodes = []

    # if there is text at the beginning (not empty) add it first
    if text[0] != "":
        new_nodes.append(TextNode(text[0], TextType.TEXT))
    
    # the image can be the at beginning or middle
    new_nodes.append(TextNode(extracted_text, text_type, extracted_link))

    
    return new_nodes



