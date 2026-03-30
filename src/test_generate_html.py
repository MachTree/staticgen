import unittest

from generate_html import extract_title

class TestGenerateHTML(unittest.TestCase):
    def test_extract_title(self):
        md = """

# A Test of Markdown

This is a **bolded** paragraph preceeding a list of items

- item 1
- **item 2**
- _item 3_
- **odds** and _ends_

This is another paragraph with _italic_ text and `code` here

"""
        title = extract_title(md)
        self.assertEqual(title, "A Test of Markdown")
    
    def test_extract_title_malformed(self):
        md = """
This is a **bolded** paragraph preceeding a list of items

- item 1
- **item 2**
- _item 3_
- **odds** and _ends_

This is another paragraph with _italic_ text and `code` here

"""
        with self.assertRaises(ValueError) as cm:
            title = extract_title(md)
        test_exception = cm.exception
        self.assertEqual(test_exception.args[0], "Error: Markdown does not begin with a valid h1 header")


if __name__ == "__main__":
    unittest.main()