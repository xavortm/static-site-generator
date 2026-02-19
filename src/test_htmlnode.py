import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", None, None, None)
        node2 = HTMLNode("div", None, None, None)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_eq_2(self):
        node = HTMLNode("div", None, None, {"id": 'test'})
        node2 = HTMLNode("div", None, None, {"id": 'test'})
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_eq_3(self):
        node = HTMLNode("div", None, None, {"id": "test", "class": "hello"})
        node2 = HTMLNode("div", None, None, {"id": "test", "class": "hello"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_diff_3(self):
        node = HTMLNode("div", None, None, {"id": "test", "class": "hello"})
        node2 = HTMLNode("div", None, None, {"id": "test"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

if __name__ == "__main__":
    unittest.main()