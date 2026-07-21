import os, shutil, pathlib
from markdown_blocks import markdown_to_blocks , markdown_to_html_node


def static_to_public(source_dir: str, dest_dir: str) -> list[str]:
    visited = []
    if os.path.exists(dest_dir) and dest_dir.endswith("public"):
        shutil.rmtree(dest_dir)
    
    if os.path.exists(source_dir):
        items = os.listdir(source_dir)
        for item in items:
            source_path = os.path.join(source_dir, item)
            dest_path = os.path.join(dest_dir, item)
            visited.append(source_path)
            if os.path.isfile(source_path):
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                shutil.copy(source_path, dest_dir)
            else:
                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                visited.extend(static_to_public(source_path, dest_path))
    return visited

def extract_title(markdown) -> str:
    blocks = markdown_to_blocks(markdown)
    count = 0
    header_string = ""
    
    for char in blocks[0]:
        if char == "#":
            count += 1
            continue
        header_string += char
    if count != 1:
        raise Exception(f"No header or wrong header type mentioned, number of #: {count}")
    return header_string.strip()
        
    
def generate_page(from_path:str, template_path:str, dest_path:str):
    markdown_file = ""
    template_file = ""
    
    with open (from_path, "r") as file:
        markdown_file = file.read()
    
    with open (template_path, "r") as file:
        template_file = file.read()
        
    page_content = markdown_to_html_node(markdown_file).to_html()
    page_tite = extract_title(markdown_file)   
    template_file = template_file.replace("{{ Title }}", page_tite)
    template_file = template_file.replace("{{ Content }}", page_content)
    parent_directory = os.path.dirname(dest_path)
    
    if not os.path.exists(dest_path):
        if os.path.exists(parent_directory):
            with open(dest_path, "x") as file:
                file.write(template_file)
        else:
            os.makedirs(parent_directory)
            with open(dest_path, "x") as file:
                file.write(template_file)
    return f"Generating page from {from_path} to {dest_path} using {template_path}"
            
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> list[str]:
    paths = os.listdir(dir_path_content)
    
    for path in paths:
        dir_p = os.path.join(dir_path_content, path)
        dest_p = os.path.join(dest_dir_path, path)
        
        if os.path.isfile(dir_p):
            dest = pathlib.Path(dest_p).with_suffix(".html")
            print(generate_page(dir_p, template_path, dest))
        else:
            generate_pages_recursive(dir_p, template_path, dest_p) 
    