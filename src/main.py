from site_generator import static_to_public
import os

def main():
    source_dir = "./static"
    dest_dir = "./public"
    print(static_to_public(source_dir, dest_dir))
main()