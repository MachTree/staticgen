import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        pieces = node.text.split(delimeter)
        if len(pieces) % 2 == 0:
            raise ValueError(f'Invalid Markdown Syntax: delimeter "{delimeter}"')
        for i in range(len(pieces)):
            if pieces[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(pieces[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(pieces[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for match in matches:
            prefix, remaining_text = remaining_text.split(f"![{match[0]}]({match[1]})", 1)
            if len(prefix.strip()) > 0:
                new_nodes.append(TextNode(prefix, TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
        if len(remaining_text.strip()) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for match in matches:
            prefix, remaining_text = remaining_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(prefix.strip()) > 0:
                new_nodes.append(TextNode(prefix, TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
        if len(remaining_text.strip()) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):
    starting_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([starting_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
