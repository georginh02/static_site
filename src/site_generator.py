import os, shutil

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