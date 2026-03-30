import os
from markdown_processing import markdown_to_html_node
from htmlnode import ParentNode
from deploy_utils import write_generated_html

def extract_title(markdown):
    if not markdown.lstrip().startswith("# "):
        raise ValueError("Error: Markdown does not begin with a valid h1 header")
    title = markdown.lstrip().split("\n", 1)[0][2:]
    return title

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    body = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Content }}", body).replace("{{ Title }}", title).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')
    write_generated_html(page, dest_path)

def generate_page_recursive(dir_path_content, template, dest_dir_path, base_path):
    if not os.path.exists(dir_path_content) or not os.path.isdir(dir_path_content):
        raise ValueError(f"Error: Invalid source path - {dir_path_content}")
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isdir(from_path):
            generate_page_recursive(from_path, template, dest_path, base_path)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = os.path.splitext(dest_path)[0] + ".html"
                generate_page(from_path, template, dest_path, base_path)
    
    