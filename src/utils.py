import re

from src.leafnode import LeafNode
from textnode import TextNode, TextType
from htmlnode import BlockType, HTMLNode

def text_type_test_to_html(text: str, tag: str) -> HTMLNode:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return HTMLNode(tag, children=html_nodes)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    output: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            output.append(node)
            continue

        found = node.text.split(delimiter)

        if len(found) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for idx, item in enumerate(found):
            if len(item) == 0:
                continue
            if idx % 2 == 0:
                output.append(TextNode(item, text_type=TextType.TEXT))
            else:
                output.append(TextNode(item, text_type=text_type))

    return output


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise ValueError(f"text_type {text_node.text_type} not supported")

    if text_node.text_type is TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)

    if text_node.text_type is TextType.BOLD:
        return LeafNode(tag='b', value=text_node.text)

    if text_node.text_type is TextType.ITALIC:
        return LeafNode(tag='i', value=text_node.text)

    if text_node.text_type is TextType.CODE:
        return LeafNode(tag='code', value=text_node.text)

    if text_node.text_type is TextType.LINK:
        return LeafNode(tag='a', value=text_node.text, props={'href': text_node.url})

    if text_node.text_type is TextType.IMAGE:
        return LeafNode(tag='img', value='', props={'src': text_node.url, 'alt': text_node.text})

    return ''

def text_blockquote_to_html_node(text):
    lines = []
    for line in text.splitlines():
        clean_line = line.lstrip('>').lstrip()
        lines.append(clean_line)

    markdown = '\n'.join(lines)
    return markdown_to_html_node(markdown, 'blockquote')

def text_heading_to_html_node(text):
    (level, content) = text.split(' ', 1)
    return text_type_test_to_html(content, f'h{len(level)}')


def text_ul_to_html_node(text):
    lines = []

    # Trying for a little smarter indentation support:
    # Does not support indented list items
    for line in text.splitlines():
        clean_line = line.lstrip()

        # Check if the line actually starts with a valid bullet
        if not clean_line.startswith(('* ', '- ')):
            raise ValueError(f"Invalid markdown: '{line}' is not a valid list item.")

        content = clean_line[2:].strip()
        html_tag = text_type_test_to_html(content, 'li')
        lines.append(html_tag)
    return HTMLNode('ul', children=lines)

def text_ol_to_html_node(text):
    lines = []

    # Trying for a little smarter indentation support:
    # Does not support indented list items
    for line in text.splitlines():
        clean_line = line.lstrip()
        matches = re.match(r"^\d*\. ", line)

        # Check if the line actually starts with a valid bullet
        if not matches:
            raise ValueError(f"Invalid markdown: '{line}' is not a valid list item.")

        content = clean_line.split('. ', maxsplit=1)[1]
        html_tag = text_type_test_to_html(content, 'li')
        lines.append(html_tag)
    return HTMLNode('ol', children=lines)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(rf'!\[(.*?)]\((.*?)\)', text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(rf'(?<!\!)\[(.*?)]\((.*?)\)', text)


def generate_tags(matches, original_text, text_type):
    output = []
    for (text, url) in matches:
        if text_type == TextType.IMAGE:
            sections = original_text.split(f"![{text}]({url})", 1)
        elif text_type == TextType.LINK:
            sections = original_text.split(f"[{text}]({url})", 1)
        original_text = sections[1]
        if len(sections[0]) > 0:
            output.append(TextNode(sections[0], text_type=TextType.TEXT))
        output.append(TextNode(text, text_type=text_type, url=url))

    if original_text != "":
        output.append(TextNode(original_text, TextType.TEXT))

    return output


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            output.append(node)
            continue

        original_text = node.text
        matches = extract_markdown_images(original_text)
        output.extend(generate_tags(matches, original_text, TextType.IMAGE))

    return output


def split_nodes_link(old_nodes):
    output: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            output.append(node)
            continue

        original_text = node.text
        matches = extract_markdown_links(original_text)
        output.extend(generate_tags(matches, original_text, TextType.LINK))

    return output


def text_to_textnodes(text) -> list[TextNode]:
    # I am adding this to mimic the results from the course, but I don't recall this being required.
    text = text.replace('\n', ' ').replace('\r', ' ')

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def markdown_to_blocks(markdown) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    return [block.strip() for block in raw_blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # quote
    if block.startswith(">"):
        return BlockType.QUOTE

    # unordered
    clean_block = block.lstrip()
    if clean_block.startswith(("-", "*")):
        return BlockType.UNORDERED_LIST

    # ordered
    if re.match(r"^\d*\. ", block):
        return BlockType.ORDERED_LIST

    # paragraph
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown, root='div'):
    blocks = markdown_to_blocks(markdown)
    child_tags = []
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            child_tags.append(text_heading_to_html_node(block))

        elif block_to_block_type(block) == BlockType.QUOTE:
            child_tags.append(text_blockquote_to_html_node(block))

        elif block_to_block_type(block) == BlockType.ORDERED_LIST:
            child_tags.append(text_ol_to_html_node(block))

        elif block_to_block_type(block) == BlockType.UNORDERED_LIST:
            child_tags.append(text_ul_to_html_node(block))

        elif block_to_block_type(block) == BlockType.CODE:
            lines = block.splitlines()
            content_lines = [line for line in lines if not line.strip().startswith('```')]
            clean_code = '\n'.join(content_lines) + '\n'
            inner = text_node_to_html_node(TextNode(clean_code, text_type=TextType.CODE))
            child_tags.append(HTMLNode('pre', children=[inner]))

        elif block_to_block_type(block) == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            child_tags.append(HTMLNode(tag="p", children=html_nodes))

    return HTMLNode(root, children=child_tags)