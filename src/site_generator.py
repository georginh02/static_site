import os, shutil
from markdown_blocks import markdown_to_blocks

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
        
    
    
