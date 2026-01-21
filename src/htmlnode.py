

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

        for key, val in self.props:
            prop_strings.append(f"{key}={val}")

        return " " + " ".join(prop_strings)
    
    def __repr__(self):
        return f"tag {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"