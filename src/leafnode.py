from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def __repr__(self) -> str:
        return f"<{self.tag}>"

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return self.value

        output = ''
        if self.tag:
            output += f"<{self.tag}"
        if self.props:
            output += f"{self.props_to_html()}>"
        else:
            output += f">"
        if self.value:
            output += f"{self.value}"
        if self.tag:
            output += f"</{self.tag}>"

        return output
