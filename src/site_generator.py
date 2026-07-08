import os, shutil

def static_to_public(path:str):
    visited = []
    
    if os.path.exists(os.path.join(path, "public")):
        shutil.rmtree(path)
    else:
            
