import os

from markdown_blocks import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path, basepath: str) -> None:
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath: str
) -> None:
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if entry.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(source_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(source_path, template_path, dest_path, basepath)


def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")