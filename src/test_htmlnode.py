import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode("div", "This is a div")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "This is a div")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_eq_props_to_html_single(self):
        node = HTMLNode("a", "This is a link", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_eq_props_to_html_multiple(self):
        node = HTMLNode("a", "This is a link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)
    
    def test_eq_repr(self):
        node = HTMLNode("a", "This is a link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), "HTMLNode(a, This is a link, children: None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_leaf_values(self):
        node = LeafNode("div", "This is a div")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "This is a div")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_to_html_valueless(self):
        node = LeafNode("div", None, {"class": "standard"})
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_tagless(self):
        node = LeafNode(None, "This is some text")
        self.assertEqual(node.to_html(), "This is some text")

        node = LeafNode(None, "This is some text", {"class": "standard"})
        self.assertEqual(node.to_html(), "This is some text")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_eq_repr(self):
        node = LeafNode("p", "Hello world!", {"class": "greeting"})
        self.assertEqual(repr(node), "LeafNode(p, Hello world!, {'class': 'greeting'})")

    def test_parent_values(self):
        child_list = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            # LeafNode("i", "italic text"),
            # LeafNode(None, "Normal text"),
        ]
        node = ParentNode("p", child_list, {"class": "standard"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, child_list)
        self.assertEqual(node.props, {"class": "standard"})

    def test_parent_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        test_exception = cm.exception
        self.assertEqual(test_exception.args[0], "Invalid HTML: ParentNode() must have a tag")

    def test_parent_to_html_no_children(self):
        node = ParentNode("ul", None, {"class": "standard"})
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        test_exception = cm.exception
        self.assertEqual(test_exception.args[0], "Invalid HTML: ParentNode() must have children")

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_with_multiple_children(self):
        child_list = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text")
        ]
        node = ParentNode("p", child_list, {"class": "standard"})
        self.assertEqual(node.to_html(), '<p class="standard"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')


if __name__ == "__main__":
    unittest.main()