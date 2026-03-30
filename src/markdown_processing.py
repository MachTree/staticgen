from markdown_blocks import(
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

from inline_markdown import(
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    document = ParentNode("div", [])
    for block in block_list:
        block_node = block_to_html_node(block)
        document.children.append(block_node)
    return document


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return process_heading_block(block)
        case BlockType.CODE:
            return process_code_block(block)
        case BlockType.QUOTE:
            return process_quote_block(block)
        case BlockType.UNORDERED_LIST:
            return process_unordered_list_block(block)
        case BlockType.ORDERED_LIST:
            return process_ordered_list_block(block)
        case BlockType.PARAGRAPH:
            return process_paragraph_block(block)
        case _:
            raise ValueError(f"Invalid BlockType: {block_type}")
        
def process_heading_block(block):
    sections = block.split(" ", 1)
    children = text_to_children(sections[1].replace("\n", " "))
    return ParentNode(f"h{len(sections[0])}", children)

def process_code_block(block):
    code_text = TextNode(block[4:-3], TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(code_text)])

def process_quote_block(block):
    content = []
    lines = block.split("\n")
    for line in lines:
        content.append(line[1:].strip())
    children = text_to_children(" ".join(content))
    return ParentNode("blockquote", children)

def process_unordered_list_block(block):
    items = []
    lines = block.split("\n")
    for line in lines:
        children = text_to_children(line[2:].strip())
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)

def process_ordered_list_block(block):
    items = []
    lines = block.split("\n")
    for line in lines:
        children = text_to_children(line.split(".", 1)[1].strip())
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)

def process_paragraph_block(block):
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for node in textnodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes
