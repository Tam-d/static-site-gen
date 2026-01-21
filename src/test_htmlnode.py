import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "this is a heading")
        self.assertEqual(node.to_html(), "<h1>this is a heading</h1>")

    def test_leaf_to_html_h2(self):
        node = LeafNode("h2", "this is a heading")
        self.assertEqual(node.to_html(), "<h2>this is a heading</h2>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child1</span><span>child2</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("span", "grandchild1")
        grandchild_node2 = LeafNode("span", "grandchild2")

        grandchild_node3 = LeafNode("span", "grandchild3")
        grandchild_node4 = LeafNode("span", "grandchild4")

        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node3, grandchild_node4])

        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div>" +
                "<span>" +
                    "<span>grandchild1</span>" +
                    "<span>grandchild2</span>" +
                "</span>" +
                "<span>" +
                    "<span>grandchild3</span>" +
                    "<span>grandchild4</span>" +
                "</span>" +
            "</div>",
        )
if __name__ == "__main__":
    unittest.main()