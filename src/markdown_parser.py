from textnode import TextType, TextNode

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