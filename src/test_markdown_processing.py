import unittest

from markdown_processing import markdown_to_html_node

class TestMarkdownProcessing(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
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

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
This is a **bolded** paragraph preceeding a list of items

- item 1
- **item 2**
- _item 3_
- **odds** and _ends_

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a <b>bolded</b> paragraph preceeding a list of items</p><ul><li>item 1</li><li><b>item 2</b></li><li><i>item 3</i></li><li><b>odds</b> and <i>ends</i></li></ul><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_ordered_list(self):
        md = """
This is a **bolded** paragraph preceeding a list of items

1. this item
2. **that item**
3. _the other item_
4.  **odds** and _ends_ and [whatnot](https://www.google.com)

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a <b>bolded</b> paragraph preceeding a list of items</p><ol><li>this item</li><li><b>that item</b></li><li><i>the other item</i></li><li><b>odds</b> and <i>ends</i> and <a href=\"https://www.google.com\">whatnot</a></li></ol><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_quote_block(self):
        md = """
This is a **bolded** paragraph preceeding a block quote

> "**Ask not what your country can do for you, ask what you can do for your country**" - JFK
> "I speak _softly_, but carry a **big** stick" - Teddy Roosevelt
>"apex predator of grug is complexity" - Grug

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a <b>bolded</b> paragraph preceeding a block quote</p><blockquote>\"<b>Ask not what your country can do for you, ask what you can do for your country</b>\" - JFK\"I speak <i>softly</i>, but carry a <b>big</b> stick\" - Teddy Roosevelt\"apex predator of grug is complexity\" - Grug</blockquote><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )
    
    def test_multiple_block_types(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Tolkien Fan Club</h1><p><img src="/images/tolkien.png" alt="JRR Tolkien sitting"></img></p><p>Here\'s the deal, <b>I like Tolkien</b>.</p></div>'
        )


if __name__ == "__main__":
    unittest.main()