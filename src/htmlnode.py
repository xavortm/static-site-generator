from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered"
    ORDERED_LIST = "ordered"


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        To be implemented by child class
        """
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ''

        output = ''
        for key, value in self.props.items():
            output += f" {key}=\"{value}\""

        return output

    def __repr__(self) -> str:
        output = ''
        if self.tag:
            output += f"<{self.tag}"
        if self.props:
            output += f"{self.props_to_html()}>"
        else:
            output += f">"
        if self.value:
            output += f"{self.value}"
        if self.children:
            for child_tag in self.children:
                output += f"\n{child_tag}\n"
        if self.tag:
            output += f"</{self.tag}>"

        return output