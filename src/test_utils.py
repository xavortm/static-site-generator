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


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_listblock(self):
        md = """
- one
- two
"""

        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li></ul></div>",
        )

    def test_paragraph_block(self):
        md = """
This is a simple paragraph of text.
"""
        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a simple paragraph of text.</p></div>",
        )

    def test_paragraph_with_inline(self):
        md = """
This has **bold**, *italic*, and `inline code`.
"""
        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        # Note: Using r"" here isn't strictly needed unless you use \n,
        # but it's good practice for consistency in tests.
        self.assertEqual(
            html,
            "<div><p>This has <b>bold</b>, <i>italic</i>, and <code>inline code</code>.</p></div>",
        )

    def test_headings(self):
        # Testing H1
        md_h1 = "# Main Title"
        node_h1 = utils.markdown_to_html_node(md_h1)
        self.assertEqual(
            node_h1.to_html(),
            "<div><h1>Main Title</h1></div>"
        )

        # Testing H3
        md_h3 = "### Sub Heading"
        node_h3 = utils.markdown_to_html_node(md_h3)
        self.assertEqual(
            node_h3.to_html(),
            "<div><h3>Sub Heading</h3></div>"
        )

    def test_heading_with_bold(self):
        md = "## This is **Bold**"
        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is <b>Bold</b></h2></div>"
        )

    def test_not_a_heading(self):
        md = "#NoSpace"
        node = utils.markdown_to_html_node(md)
        # This should likely be a paragraph, not an h1
        self.assertIn("<p>", node.to_html())

    def test_multi_block(self):
        md = """
# Title

This is a paragraph.

* item 1
* item 2
"""
        node = utils.markdown_to_html_node(md)
        html = node.to_html()

        # We expect a single div containing h1, p, and ul in order
        expected = (
            "<div>"
            "<h1>Title</h1>"
            "<p>This is a paragraph.</p>"
            "<ul><li>item 1</li><li>item 2</li></ul>"
            "</div>"
        )
        self.assertEqual(html, expected)

    def test_list_with_inline(self):
        md = """
- normal
- **bold**
- *italic*
"""
        node = utils.markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>normal</li><li><b>bold</b></li><li><i>italic</i></li></ul></div>"
        self.assertEqual(html, expected)