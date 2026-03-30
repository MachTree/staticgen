import os
import shutil

SITE_DIRECTORY = "./public"
STATIC_DIRECTORY = "./static"

def deploy_site():
    print("Deleting site directory")
    if os.path.exists(SITE_DIRECTORY):
        shutil.rmtree(SITE_DIRECTORY)

    print("Deploying files to site directory")
    copy_directory_tree(STATIC_DIRECTORY, SITE_DIRECTORY)

def copy_directory_tree(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        print(f" * {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
        else:
            copy_directory_tree(src_path, dest_path)

def write_generated_html(content, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
