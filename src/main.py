import os
import shutil
import sys

from deploy_utils import deploy_site
from generate_html import generate_page, generate_page_recursive
from config import SITE_DIRECTORY, TEMPLATE_FILE, CONTENT_DIRECTORY

def main():
    if len(sys.argv) > 0:
        base_path = sys.argv[0]
    else:
        base_path = "/"
    deploy_site()
    print("Generating content")
    generate_page_recursive(CONTENT_DIRECTORY, TEMPLATE_FILE, SITE_DIRECTORY, base_path)


if __name__ == "__main__":
    main()
