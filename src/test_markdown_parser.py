import unittest
from textnode import TextType, TextNode
from markdown_parser import match_delimiter, split_nodes_delimiter

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
        
        new_nodes = split_nodes_delimiter([test_node], "**", TextType.TEXT)

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], result_nodes[i])

    def test_split_nodes_delimiter_bold(self):
        result_node1 = TextNode("This is text with a ", TextType.TEXT)
        result_node2 = TextNode("italics", TextType.ITALIC)
        result_node3 = TextNode(" in the middle", TextType.TEXT)
        result_nodes = [result_node1, result_node2, result_node3]
        
        test_node = TextNode(
            "This is text with a _italics_ in the middle", 
            TextType.TEXT
        )
        
        new_nodes = split_nodes_delimiter([test_node], "_", TextType.TEXT)

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], result_nodes[i])

    def test_split_nodes_delimiter_code(self):
        result_node1 = TextNode("This is text with a ", TextType.TEXT)
        result_node2 = TextNode("code block", TextType.CODE)
        result_node3 = TextNode(" word", TextType.TEXT)
        result_nodes = [result_node1, result_node2, result_node3]
        
        test_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([test_node], "`", TextType.TEXT)

        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], result_nodes[i])

if __name__ == "__main__":
    unittest.main()