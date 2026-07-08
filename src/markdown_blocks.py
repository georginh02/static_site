from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode , TextType,  text_to_textnodes ,  text_node_to_html_node 

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# allows us to strip the markdown and into blocks / basically each 
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if not block:
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

# returns the type of the block eg (Headding , paragraph, etc)
def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

# checks for inline and formats it accordingly if nothing is found it will just become of text type
def inline_to_textnodes(text) -> list[TextNode]:
    return text_to_textnodes(text)

# takes textnodes and converts them to leafnodes
def textnodes_to_leafnodes(textnodes: list[TextNode]) -> list[LeafNode]:
    list_of_hnodes = []
    for node in textnodes:
        textnode = text_node_to_html_node(node)
        list_of_hnodes.append(textnode)
    return list_of_hnodes

# converts an unordered list to a parentnode
def unordered_list_to_html_node(text:str) -> ParentNode:
    split_text_by_newlines = text.split("\n")
    list_of_pnodes = []
    
    for text in split_text_by_newlines:
        stripped_hyphen = text.strip("- ")
        tnodes = inline_to_textnodes(stripped_hyphen)
        lnodes = textnodes_to_leafnodes(tnodes)
        list_of_pnodes.append(ParentNode("li", lnodes))
    return ParentNode("ul", list_of_pnodes)

# converts an ordered list to a parentnode
def ordered_list_to_html_node(text:str) -> ParentNode:
    split_text_by_newlines = text.split("\n")
    ordered_list_length = len(split_text_by_newlines)
    list_of_pnodes = []
    
    for i in range(1 , ordered_list_length + 1 , 1):
        stripped_begining = split_text_by_newlines[i-1].strip(f"{i}. ")
        tnodes = inline_to_textnodes(stripped_begining)
        lnodes = textnodes_to_leafnodes(tnodes)
        list_of_pnodes.append(ParentNode("li", lnodes))
    return ParentNode("ol", list_of_pnodes)

def code_to_html_node(text:str) -> ParentNode:
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("invalid code block")
    stripped_backticks = text[4:-3]
    tnode = TextNode(stripped_backticks, TextType.CODE)
    lnode = text_node_to_html_node(tnode)
    return ParentNode("pre", [lnode])

# based on the type type of text (eg texttype) all the logic is done through helpers and this function returns a complete parentnode with its corresponding type
def block_to_children(text) -> ParentNode:
    block_type = block_to_block_type(text)
    match block_type:
        case BlockType.PARAGRAPH:
            replaced_text_with_spaces = text.replace("\n", " ")
            tnodes = inline_to_textnodes(replaced_text_with_spaces)
            lnodes = textnodes_to_leafnodes(tnodes)
            return ParentNode("p", lnodes)

        case BlockType.HEADING:
            count = text.count("#")
            stripped_text = text.strip("# ")
            tnodes = inline_to_textnodes(stripped_text)
            lnodes = textnodes_to_leafnodes(tnodes)
            return ParentNode(f'h{count}', lnodes)

        case BlockType.CODE:
            return code_to_html_node(text)

        case BlockType.QUOTE:
            stripped_text = text.strip("> ")
            tnodes = inline_to_textnodes(stripped_text)
            lnodes = textnodes_to_leafnodes(tnodes)
            return ParentNode("blockquote", lnodes)

        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(text)
        
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(text)
        
        case _:
            raise Exception("Improper blocktype was specified")

# Main func
def markdown_to_html_node(markdown):
    list_of_htmlnodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block != "":
            list_of_htmlnodes.append(block_to_children(block))
    return ParentNode("div", list_of_htmlnodes)
    
