import os
from pathlib import Path

from markdown_to_html import markdown_to_html_node
from markdown_parser import extract_title

def get_file_content(file_path):
    file_content = ""

    try:
        fp = Path(file_path)

        with open(fp, "r") as f:
            file_content = f.read()
        
        return file_content
    except Exception as e:
        print("Error while retrieving file content for \"{file_path}\"")

def get_template_content(template_path):
    return get_file_content(template_path)

def get_markdown_content(markdown_path):
    return get_file_content(markdown_path)

def generate_html(template, title, html, base_path):
    titled_template = template.replace("{{ Title }}", title)
    content = titled_template.replace("{{ Content }}", html)

    html_links = content.replace(f"href=\"/", f"href=\"{base_path}")
    html_images = html_links.replace(f"src=\"/", f"src=\"{base_path}")

    return html_images

def write_to_file(content, destination):
    dest_path = Path(destination)

    try:
        if Path.is_dir(dest_path):
            print(f"{dest_path} is a directory")
            raise Exception(
                "Error: Cannot write to file as it is a directory"
            )

        if Path.is_file(dest_path):
            print(f"{dest_path} file exists, and is a file. Attempting to write...")
            with open(dest_path, "w") as f:
                f.write(content)
            return

        print(f"{dest_path} does not exist, attempting to create directory structure...")
        os.makedirs(destination.rsplit("/", 1)[0], exist_ok=True)
        
        if not Path.exists(dest_path):
            Path.touch(dest_path)

        with open(dest_path, "w") as f:
            f.write(content)

    except Exception as e:
        print(e)

def generate_page(from_path, template_path, dest_path, base_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_content = get_markdown_content(from_path)
    template_content = get_template_content(template_path)

    markdown_title = extract_title(markdown_content)

    markdown_html_nodes = markdown_to_html_node(markdown_content)
    markdown_to_html = markdown_html_nodes.to_html()

    print(markdown_to_html)

    html_content = generate_html(
        template_content, markdown_title, markdown_to_html, base_path
    )

    print(html_content)

    write_to_file(html_content, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):

    print(f"Checking {dir_path_content}")

    content_path = Path(dir_path_content)

    if Path.is_file(content_path):
        #create the file in the dest dir
        print(f"{content_path} is a file")
        write_path = dest_dir_path.replace(".md", ".html")
        generate_page(content_path, template_path, write_path, base_path)

    if Path.is_dir(content_path):
        print(f"{content_path} is a directory")
        for child in Path.iterdir(content_path):
            print(f"Child Path: {child}")
            print(f"Child Name: {child.name}")
            generate_pages_recursive(child, template_path, dest_dir_path + f"/{child.name}", base_path)