from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node
import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )


if __name__ == "__main__":
    main()
