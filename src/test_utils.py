from htmlnode import BlockType
from textnode import TextNode, TextType
import utils
import unittest

class TestUtils(unittest.TestCase):
    def test_eq_italic__double(self):
        test_notes = [
            TextNode("This is text with a __italic block__ word, __more__", TextType.TEXT)
        ]

        self.assertEqual(
            utils.split_nodes_delimiter(test_notes, "__", TextType.ITALIC),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word, ", TextType.TEXT),
                TextNode("more", TextType.ITALIC),
            ]
        )


    def test_eq_italic(self):
        test_notes = [
            TextNode("This is text with a __italic block__ word", TextType.TEXT)
        ]

        self.assertEqual(
            utils.split_nodes_delimiter(test_notes, "__", TextType.ITALIC),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_eq_bold(self):
        test_notes = [
            TextNode("This is text with a **bold block** word", TextType.TEXT)
        ]

        self.assertEqual(
            utils.split_nodes_delimiter(test_notes, "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_eq_code(self):
        test_notes = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]

        self.assertEqual(
            utils.split_nodes_delimiter(test_notes, "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_extract_markdown_links(self):
        matches = utils.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images(self):
        matches = utils.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = utils.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_full_split(self):
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),            ],
            utils.text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"),
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = utils.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading_fail(self):
        md = "#Not a heading"
        blocks = utils.block_to_block_type(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_1(self):
        md = "# Heading"
        blocks = utils.block_to_block_type(md)
        self.assertEqual(blocks, BlockType.HEADING)

    def test_block_to_block_type_heading_3(self):
        md = "### Heading 3"
        blocks = utils.block_to_block_type(md)
        self.assertEqual(blocks, BlockType.HEADING)

    def test_block_to_block_type_paragraph(self):
        md = "this is a paragraph"
        blocks = utils.block_to_block_type(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_block_to_block_type_code_block(self):
        md = """```
this is code
```"""
        blocks = utils.block_to_block_type(md)
        self.assertEqual(blocks, BlockType.CODE)
