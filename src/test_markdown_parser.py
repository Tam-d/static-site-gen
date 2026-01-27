import unittest
from textnode import TextType, TextNode
from markdown_parser import match_delimiter, split_nodes_delimiter
from markdown_parser import extract_markdown_images, extract_markdown_links
from markdown_parser import split_nodes_image, split_nodes_link
from markdown_parser import text_to_textnodes, markdown_to_blocks

class TestMarkdownParser(unittest.TestCase):
    def test_match_delimiter(self):
        self.assertEqual(match_delimiter("**"), TextType.BOLD)
        self.assertEqual(match_delimiter("_"), TextType.ITALIC)
        self.assertEqual(match_delimiter("`"), TextType.CODE)
    
    def test_match_delimiter(self):
        self.assertRaises(Exception, match_delimiter, "")

    def test_split_nodes_delimiter_bold(self):
        result_node1 = TextNode("This is text with a ", TextType.TEXT)
        result_node2 = TextNode("bolded phrase", TextType.BOLD)
        result_node3 = TextNode(" in the middle", TextType.TEXT)
        result_nodes = [result_node1, result_node2, result_node3]
        
        test_node = TextNode(
            "This is text with a **bolded phrase** in the middle", 
            TextType.TEXT
        )
        
        new_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], result_nodes[i])

    def test_split_nodes_delimiter_italic(self):
        result_node1 = TextNode("This is text with a ", TextType.TEXT)
        result_node2 = TextNode("italics", TextType.ITALIC)
        result_node3 = TextNode(" in the middle", TextType.TEXT)
        result_nodes = [result_node1, result_node2, result_node3]
        
        test_node = TextNode(
            "This is text with a _italics_ in the middle", 
            TextType.TEXT
        )
        
        new_nodes = split_nodes_delimiter([test_node], "_", TextType.ITALIC)

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], result_nodes[i])

    def test_split_nodes_delimiter_code(self):
        result_node1 = TextNode("This is text with a ", TextType.TEXT)
        result_node2 = TextNode("code block", TextType.CODE)
        result_node3 = TextNode(" word", TextType.TEXT)
        result_nodes = [result_node1, result_node2, result_node3]
        
        test_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([test_node], "`", TextType.CODE)

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], result_nodes[i])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)

        self.assertEqual(2, len(result))

        self.assertEqual(result[0][0], "rick roll")
        self.assertEqual(result[0][1], "https://i.imgur.com/aKaOqIh.gif")

        self.assertEqual(result[1][0], "obi wan")
        self.assertEqual(result[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)

        self.assertEqual(2, len(result))

        self.assertEqual(result[0][0], "to boot dev")
        self.assertEqual(result[0][1], "https://www.boot.dev")

        self.assertEqual(result[1][0], "to youtube")
        self.assertEqual(result[1][1], "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_image(self):
        result_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", 
                TextType.IMAGE, 
                "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" the end", TextType.TEXT)
        ]

        test_node = TextNode(
             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([test_node])

        for i in range(0, len(result_nodes)):
            self.assertEqual(result_nodes[i], new_nodes[i])

    def test_split_nodes_link(self):
        result_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "link2", 
                TextType.LINK, 
                "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" the end", TextType.TEXT)
        ]

        test_node = TextNode(
             "This is text with a [link1](https://i.imgur.com/zjjcJKZ.png) and another [link2](https://i.imgur.com/3elNhQu.png) the end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([test_node])

        for i in range(0, len(result_nodes)):
            self.assertEqual(result_nodes[i], new_nodes[i])

    def test_text_to_textnodes(self):
        result_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(test_text)

        for i in range(0, len(result_nodes)):
            print(result_nodes[i])
            print(new_nodes[i])
            self.assertEqual(result_nodes[i], new_nodes[i])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()