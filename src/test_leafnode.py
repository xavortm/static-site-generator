import unittest

from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_2(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Hello, world!</a>')
