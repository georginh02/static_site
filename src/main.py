from site_generator import static_to_public, generate_page

source_dir = "./static"
dest_dir = "./public"

from_path = "./content/index.md"
template_path = "template.html"
dest_path = "./public"


def main():
    # static_to_public(source_dir, dest_dir)
    print(generate_page(from_path, template_path, dest_path))
main()