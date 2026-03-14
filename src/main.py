import os
import shutil

SITE_DIRECTORY = "./public"
STATIC_DIRECTORY = "./static"


def clear_destination(purge=False):
    if not os.path.exists(SITE_DIRECTORY):
        raise ValueError(f"Unknown path: {SITE_DIRECTORY}")
    print(f"{SITE_DIRECTORY} exists")
    dirlist = []
    contents = os.listdir(SITE_DIRECTORY)
    prev_level = SITE_DIRECTORY
    cur_level = SITE_DIRECTORY
    for entity in contents:
        ent_path = os.path.join(cur_level, entity)
        print (f"{entity} :: {ent_path} :: {os.path.isdir(ent_path)} || {os.path.exists(ent_path)}")
    shutil.rmtree(SITE_DIRECTORY)


def main():
    print("In main()")
    clear_destination()

if __name__ == "__main__":
    main()
