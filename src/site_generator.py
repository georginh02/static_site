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
        
    
    
def main():
    md = """
#Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
"""
    
    print(extract_title(md))
    
main()