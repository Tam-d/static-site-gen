import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_full_node(self):

        list_item_tag = "li"
        list_item_value = "list item"
        list_item_nodes = []

        for i in range(1,5):
            list_item_node = HTMLNode(
                list_item_tag, 
                list_item_value + str(i)
            )

            list_item_nodes.append(list_item_node)

        html_node = HTMLNode(
            "ul", 
            "this is an unordered list", 
            list_item_nodes,
            {"type": "circle"}
        )

        self.assertNotEqual(html_node.tag, None)
        self.assertNotEqual(html_node.value, None)
        self.assertNotEqual(html_node.children, None)
        self.assertNotEqual(html_node.props, None)

        self.assertEqual(len(html_node.children), len(list_item_nodes))

    def test_empty_node(self):
        empty_node = HTMLNode()
        self.assertEqual(empty_node.tag, None)
        self.assertEqual(empty_node.value, None)
        self.assertEqual(empty_node.children, None)
        self.assertEqual(empty_node.props, None)

    def test_repr(self):
        html_node = HTMLNode("h1", "this is a heading")
        self.assertNotEqual(html_node.__repr__(), None)

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "this is a heading")
        self.assertEqual(node.to_html(), "<h1>this is a heading</h1>")

    def test_leaf_to_html_h2(self):
        node = LeafNode("h2", "this is a heading")
        self.assertEqual(node.to_html(), "<h2>this is a heading</h2>")

if __name__ == "__main__":
    unittest.main()