from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list["HTMLNode"], props: dict[str, str] = None):
        super().__init__(tag=tag, children=children, props=props)

    def __repr__(self) -> str:
        return f"<{self.tag}>"

    def to_html(self):
        if not self.tag:
            raise ValueError('Missing tag')

        if not self.children:
            raise ValueError('Missing children')

        output = ''

        if self.tag:
            output += f"<{self.tag}"

        if self.props:
            output += f"{self.props_to_html()}>"
        else:
            output += f">"

        if self.value:
            output += f"{self.value}"

        for child in self.children:
            output += child.to_html()

        if self.tag:
            output += f"</{self.tag}>"

        return output
