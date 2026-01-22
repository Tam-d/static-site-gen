import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        #print(node)
        self.assertEqual("TextNode(This is a text node, bold)", node.__repr__())

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("anchor text", TextType.LINK,"https://www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.props["href"], "https://www.test.com")

    def test_link(self):
        node = TextNode("anchor text", TextType.LINK,"https://www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.props["href"], "https://www.test.com")

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