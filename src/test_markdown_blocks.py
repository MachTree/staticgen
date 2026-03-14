import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_whitespace(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_heading(self):
        returned_type = block_to_block_type("# Heading")
        self.assertEqual(returned_type, BlockType.HEADING)

        returned_type = block_to_block_type("#Heading")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("#### Heading")
        self.assertEqual(returned_type, BlockType.HEADING)

        returned_type = block_to_block_type("######## Heading")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        returned_type = block_to_block_type("```This is some code yo```")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("```\nThis is some real code```")
        self.assertEqual(returned_type, BlockType.CODE)

        returned_type = block_to_block_type("```\nThis is some code\nAnd some more code\nAnd even more code\n```")
        self.assertEqual(returned_type, BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        returned_type = block_to_block_type(">Ask not what your code can do for you\nBut what you can do for your code")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type(">Ask not what your code can do for you\n>But what you can do for your code\n> Ich Bin Ein Pythonista")
        self.assertEqual(returned_type, BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        returned_type = block_to_block_type("- A thing\n- A wossname\n- A doohickey")
        self.assertEqual(returned_type, BlockType.UNORDERED_LIST)

        returned_type = block_to_block_type("-A Dinglehopper\n- A wossname\n- A doohickey")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("- A thing\n-A Dinglehopper\n- A wossname\n- A doohickey")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("- A thing\n- A Dinglehopper\n- A wossname\n- A doohickey")
        self.assertEqual(returned_type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        returned_type = block_to_block_type("1. One\n2. Two\n3. Three\n4. Four")
        self.assertEqual(returned_type, BlockType.ORDERED_LIST)

        returned_type = block_to_block_type("1. One\n2. Two\n3.Three\n4. Four\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten\n11. Eleven\n12. Twelve")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("1. One\n2. Two\n3. Three\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten\n11. Eleven\n12. Twelve")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("1. One\n2 Two\n3. Three\n4. Four\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten\n11. Eleven\n12. Twelve")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("1. One\n2. Two\n3. Three\nFour\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten\n11. Eleven\n12. Twelve")
        self.assertEqual(returned_type, BlockType.PARAGRAPH)

        returned_type = block_to_block_type("1. One\n2. Two\n3. Three\n4. Four\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten\n11. Eleven\n12. Twelve")
        self.assertEqual(returned_type, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()