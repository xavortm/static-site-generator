import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    # Add more tests :
    def test_to_html_with_parent_node(self):
        parent_node = ParentNode("div", [
            LeafNode("span", "child"),
            LeafNode("span", "child")
        ])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span></div>")
