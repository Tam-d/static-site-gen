

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props or len(self.props) == 0:
            return ""
        
        prop_strings = []

        for key, val in self.props.items():
            prop_strings.append(f"{key}={val}")

        return " " + " ".join(prop_strings)
    
    def __repr__(self):
        return f"tag {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):

        if self.value is None:
            raise ValueError("Leaf node has no value")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"tag {self.tag}, value: {self.value},  props: {self.props}"
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        
        if not self.tag:
            raise ValueError("Parent node has no tag")
        if not self.children or len(self.children) == 0:
            raise ValueError("Parent node has no children")

        children_html = ""

        for childNode in self.children:
            children_html += childNode.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"