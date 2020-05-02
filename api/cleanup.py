import re
import shutil
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def clean_images(path_images, path_clean_images):
    directory = os.fsencode(path_images)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            id = re.split(r'-|\.', filename)[0]

            src_path = os.path.join(path_images, filename)
            dest_path = "{}{}.png".format(path_clean_images, id)

            try:
                file = open(dest_path)
                # if pass file exists
            except:
                if is_number(id):
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy(src_path, dest_path)
