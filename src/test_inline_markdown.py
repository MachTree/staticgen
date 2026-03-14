import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT)
            ]
        )

    def test_split_italic(self):
        node = TextNode("This is text with an _italicized phrase_ in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italicized phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.TEXT)
            ]
        )

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_bold_multiple(self):
        node = TextNode("This is text with **several important phrases** and so they are **brought to your attention** through the use of **font styling** for emphasis", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("several important phrases", TextType.BOLD),
                TextNode(" and so they are ", TextType.TEXT),
                TextNode("brought to your attention", TextType.BOLD),
                TextNode(" through the use of ", TextType.TEXT),
                TextNode("font styling", TextType.BOLD),
                TextNode(" for emphasis", TextType.TEXT)
            ]
        )

    def test_split_multiple_delimiters(self):
        node = TextNode("This is text with a **bolded phrase** and an _italicized phrase_ as well.", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(first_pass), 3)
        self.assertEqual(
            first_pass,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" and an _italicized phrase_ as well.", TextType.TEXT)
            ]
        )
        second_pass = split_nodes_delimiter(first_pass, "_", TextType.ITALIC)
        self.assertEqual(len(second_pass), 5)
        self.assertEqual(
            second_pass,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" and an ", TextType.TEXT),
                TextNode("italicized phrase", TextType.ITALIC),
                TextNode(" as well.", TextType.TEXT)
            ]
        )

    def test_split_multiple_nested_delimiters(self):
        node = TextNode("This is text with a **_slightly extended_ bolded phrase** and an _italicized phrase_ as well.", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(first_pass), 3)
        self.assertEqual(
            first_pass,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("_slightly extended_ bolded phrase", TextType.BOLD),
                TextNode(" and an _italicized phrase_ as well.", TextType.TEXT)
            ]
        )
        second_pass = split_nodes_delimiter(first_pass, "_", TextType.ITALIC)
        self.assertEqual(len(second_pass), 5)
        self.assertEqual(
            second_pass,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("_slightly extended_ bolded phrase", TextType.BOLD),
                TextNode(" and an ", TextType.TEXT),
                TextNode("italicized phrase", TextType.ITALIC),
                TextNode(" as well.", TextType.TEXT)
            ]
        )

    def test_split_missing_delimiter(self):
        node = TextNode("This is invalid markdown with a **bolded phrase", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_exception = cm.exception
        self.assertEqual(test_exception.args[0][:24], "Invalid Markdown Syntax:")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                )
            ],
            new_nodes
        )

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [a link](https://www.google.com) to more information.",
            TextType.TEXT
        )
        first_pass = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and [a link](https://www.google.com) to more information.", TextType.TEXT)
            ],
            first_pass
        )
        second_pass = split_nodes_link(first_pass)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://www.google.com"),
                TextNode(" to more information.", TextType.TEXT)
            ],
            second_pass
        )

    def test_split_links_and_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [a link](https://www.google.com) to more information.",
            TextType.TEXT
        )
        first_pass = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://www.google.com"),
                TextNode(" to more information.", TextType.TEXT)
            ],
            first_pass
        )
        second_pass = split_nodes_image(first_pass)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://www.google.com"),
                TextNode(" to more information.", TextType.TEXT)
            ],
            second_pass
        )
    
    def test_text_to_textnodes_one_of_each(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
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
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes           
        )


if __name__ == "__main__":
    unittest.main()