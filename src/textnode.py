from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self , text: str , text_type: TextType , url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self , other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type 
            and self.url == other.url
        )
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type} , {self.url})"
    

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text , {"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text} )        
        case _:
            raise ValueError("invalid text type")
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    list_of_TextNodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list_of_TextNodes.append(node)
            continue
        list_of_split_new_nodes = []
        split_node = node.text.split(delimiter)
        if len(node.text.split(delimiter)) % 2 == 0:
            raise Exception("invalid markdown syntax specified")
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                list_of_split_new_nodes.append(TextNode(split_node[i] , TextType.TEXT))
            else:
                list_of_split_new_nodes.append(TextNode(split_node[i] , text_type))   
        list_of_TextNodes.extend(list_of_split_new_nodes)
    return list_of_TextNodes

def extract_markdown_images(text) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return matches

def extract_markdown_links(text) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return matches

def split_nodes_image(old_nodes):
    list_of_all_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            list_of_all_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_images(original_text)
        
        if not matches: 
            list_of_all_nodes.append(node)
            continue
        
        for image_alt , image_link in matches:
            section = original_text.split(f"![{image_alt}]({image_link})", 1)
            if section[0] != "":
                list_of_all_nodes.append(TextNode(section[0] , TextType.TEXT))
            list_of_all_nodes.append(TextNode(image_alt, TextType.IMAGE , image_link))
            original_text = section[1]     
                       
        if original_text != "":
            list_of_all_nodes.append(TextNode(original_text , TextType.TEXT))
            
    return list_of_all_nodes


def split_nodes_link(old_nodes):
    list_of_all_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            list_of_all_nodes.append(node)
            continue
        original_text = node.text
        matches = extract_markdown_links(original_text)
        
        if not matches: 
            list_of_all_nodes.append(node)
            continue
        
        for image_alt , image_link in matches:
            section = original_text.split(f"[{image_alt}]({image_link})", 1)
            if section[0] != "":
                list_of_all_nodes.append(TextNode(section[0] , TextType.TEXT))
            list_of_all_nodes.append(TextNode(image_alt, TextType.LINK , image_link))
            original_text = section[1]     
                       
        if original_text != "":
            list_of_all_nodes.append(TextNode(original_text , TextType.TEXT))
            
    return list_of_all_nodes
           

def text_to_textnodes(text:str) -> list[TextNode]:
    main_node = TextNode(text, TextType.TEXT)
    n1 = split_nodes_delimiter([main_node], '**', TextType.BOLD)
    n2 = split_nodes_delimiter(n1, '_', TextType.ITALIC)
    n3 = split_nodes_delimiter(n2, '`', TextType.CODE)
    n4 = split_nodes_image(n3)
    n5 = split_nodes_link(n4)
    return n5


