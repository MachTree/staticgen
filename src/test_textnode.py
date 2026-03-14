import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_full(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node,node2)

    def test_not_eq_url2(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/lessons")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node,node2)
    
    def test_not_eq_full(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_node_conversion_text(self):
        node = TextNode("This is plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(node.text, html_node.value)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.to_html(), "This is plain text")
    
    def test_node_conversion_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(node.text, html_node.value)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")
    
    def test_node_conversion_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(node.text, html_node.value)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is italic text</i>")
    
    def test_node_conversion_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(node.text, html_node.value)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is code text</code>")

    def test_node_conversion_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(node.text, html_node.value)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a link</a>')

    def test_node_conversion_img(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="https://www.boot.dev/img/bootdev-logo-full-small.webp" alt="This is an image"></img>')

    def test_node_conversion_undefined(self):
        node = TextNode("This is undefined", None)
        with self.assertRaises(ValueError) as cm:
            html_node = text_node_to_html_node(node)
        test_exception = cm.exception
        self.assertEqual(test_exception.args[0][:17], "Invalid TextType:")


if __name__ == "__main__":
    unittest.main()