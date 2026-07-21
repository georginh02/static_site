from site_generator import static_to_public, generate_page , generate_pages_recursive
import sys

source_dir = "./static"
dest_dir = "./docs"
from_path = "./content"
template_path = "template.html"
dest_path = "./docs"


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    static_to_public(source_dir, dest_dir)
    generate_pages_recursive(from_path, template_path, dest_path, base_path)
main()