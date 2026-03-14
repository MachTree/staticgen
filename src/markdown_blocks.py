import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(text):
    sections = text.split("\n\n")
    blocks = []
    for section in sections:
        section = section.strip()
        if section == "":
            continue
        blocks.append(section)
    return blocks

def block_to_block_type(block):
    if block[0] == "#" and block[block.rfind("#", 0, 6) + 1] == " ":
    # if re.match(r"#{1,6} ", block) != None:
        return BlockType.HEADING
    if block[0:4] == "```\n" and block[-3:] == "```":
    # if re.fullmatch(r"```\n[^]*?```", block) != None:
        return BlockType.CODE
    if block[0] == ">":
        well_formed = True
        for line in block.split("\n"):
            if line[0] != ">":
                well_formed = False
        if well_formed:
            return BlockType.QUOTE
    if block[:2] == "- ":
        well_formed = True
        for line in block.split("\n"):
            if line[:2] != "- ":
                well_formed = False
        if well_formed:
            return BlockType.UNORDERED_LIST
    if block[:3] == "1. ":
        well_formed = True
        lines = block.split("\n")
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                well_formed = False
        if well_formed:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


