import os
import shutil

from deploy_utils import deploy_site
from generate_html import generate_page, generate_page_recursive

SITE_DIRECTORY = "./public"
STATIC_DIRECTORY = "./static"
CONTENT_DIRECTORY = "./content"
TEMPLATE_FILE = "./template.html"

def main():
    deploy_site()
    print("Generating content")
    generate_page_recursive(CONTENT_DIRECTORY, TEMPLATE_FILE, SITE_DIRECTORY)


if __name__ == "__main__":
    main()
